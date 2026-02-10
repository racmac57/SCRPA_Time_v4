# 2026_01_28
# Project: scripts/prepare_7day_outputs.py
# Author: R. A. Carucci
# Purpose: Generate filtered 7-day datasets and lag day tracking metadata.

"""
SCRPA 7-Day Outputs - Filtered Data and Lag Day Metadata Generator

This module filters enriched SCRPA data for 7-day reporting and generates:
1. SCRPA_7Day_With_LagFlags.csv - All incidents reported in current 7-day window
2. SCRPA_7Day_Lag_Only.csv - Backfill lag incidents (Backfill_7Day = TRUE)
3. SCRPA_7Day_Summary.json - LagDay metadata (counts, date ranges)

The filtering logic matches what Power BI slicer filters would produce:
- IsCurrent7DayCycle = TRUE (Report_Date_ForLagday in current 7-day window)
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Any, Optional, Tuple
import argparse


# =============================================================================
# FILTERING FUNCTIONS
# =============================================================================

def filter_7day_by_report_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter for incidents where Report_Date_ForLagday falls within
    the current 7-day cycle window.

    This matches IsCurrent7DayCycle = TRUE in the M code.

    Args:
        df: Enriched DataFrame with IsCurrent7DayCycle column

    Returns:
        Filtered DataFrame
    """
    if 'IsCurrent7DayCycle' not in df.columns:
        raise ValueError("DataFrame must have IsCurrent7DayCycle column")

    return df[df['IsCurrent7DayCycle'] == True].copy()


def extract_backfill_lag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract only backfill lag incidents (Backfill_7Day = TRUE).

    These are incidents where:
    - Incident occurred BEFORE the current cycle start
    - Report was filed DURING the current 7-day window

    Args:
        df: Enriched DataFrame with Backfill_7Day column

    Returns:
        Filtered DataFrame with only backfill lag incidents
    """
    if 'Backfill_7Day' not in df.columns:
        raise ValueError("DataFrame must have Backfill_7Day column")

    return df[df['Backfill_7Day'] == True].copy()


def extract_7day_and_lag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract incidents that are either:
    - Period = "7-Day" (incident occurred in 7-day window)
    - IsLagDay = TRUE (incident before cycle, reported in cycle)

    This is what the executive summary reports include.

    Args:
        df: Enriched DataFrame

    Returns:
        Filtered DataFrame
    """
    mask = (df['Period'] == '7-Day') | (df['IsLagDay'] == True)
    return df[mask].copy()


# =============================================================================
# SUMMARY GENERATION
# =============================================================================

def generate_lagday_summary(
    df_full: pd.DataFrame,
    df_7day: pd.DataFrame,
    df_lag_only: pd.DataFrame,
    cycle_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate comprehensive summary metadata for lag day tracking.

    Args:
        df_full: Full enriched DataFrame
        df_7day: Filtered 7-day + lag DataFrame
        df_lag_only: Backfill lag only DataFrame
        cycle_info: Optional dict with cycle details

    Returns:
        Dictionary with summary metadata
    """
    # Extract date range from data
    if 'Incident_Date_Date' in df_7day.columns and len(df_7day) > 0:
        incident_dates = df_7day['Incident_Date_Date'].dropna()
        if len(incident_dates) > 0:
            # Convert to date if needed
            if hasattr(incident_dates.iloc[0], 'date'):
                incident_dates = incident_dates.apply(lambda x: x.date() if hasattr(x, 'date') else x)
            min_incident = min(incident_dates)
            max_incident = max(incident_dates)
        else:
            min_incident = max_incident = None
    else:
        min_incident = max_incident = None

    # Get cycle boundaries from debug column if available
    cycle_start = cycle_end = report_due = None
    if '_Period_Debug' in df_full.columns and len(df_full) > 0:
        debug_sample = df_full['_Period_Debug'].iloc[0]
        if isinstance(debug_sample, str) and 'CycleStart=' in debug_sample:
            import re
            start_match = re.search(r'CycleStart=(\d{1,2}/\d{1,2}/\d{4})', debug_sample)
            end_match = re.search(r'CycleEnd=(\d{1,2}/\d{1,2}/\d{4})', debug_sample)
            due_match = re.search(r'ReportDue=(\d{1,2}/\d{1,2}/\d{4})', debug_sample)

            if start_match:
                cycle_start = start_match.group(1)
            if end_match:
                cycle_end = end_match.group(1)
            if due_match:
                report_due = due_match.group(1)

    # Get unique cycle name from data
    cycle_name = None
    if 'cycle_name_adjusted' in df_7day.columns and len(df_7day) > 0:
        names = df_7day['cycle_name_adjusted'].dropna().unique()
        if len(names) > 0:
            cycle_name = names[0]

    # Crime category breakdown for lag incidents
    lag_by_category = {}
    if 'Crime_Category' in df_lag_only.columns and len(df_lag_only) > 0:
        lag_by_category = df_lag_only['Crime_Category'].value_counts().to_dict()

    # 7-Day by Crime_Category: TotalCount and LagDayCount per category + TOTAL row
    by_crime_category = []
    if 'Crime_Category' in df_7day.columns and len(df_7day) > 0:
        # Filter to only actual 7-Day period incidents (not backfill)
        df_7day_period_only = df_7day[df_7day['Period'] == '7-Day'].copy() if 'Period' in df_7day.columns else df_7day.copy()
        
        # Use IncidentToReportDays for reporting delay lag (not cycle-based LagDays)
        has_reporting_lag = 'IncidentToReportDays' in df_7day_period_only.columns
        for cat, grp in df_7day_period_only.groupby('Crime_Category', dropna=False):
            cat_name = str(cat) if pd.notna(cat) else 'Unknown'
            total = len(grp)
            # Count incidents with reporting delay (IncidentToReportDays > 0)
            lag_count = int((grp['IncidentToReportDays'] > 0).sum()) if has_reporting_lag else 0
            by_crime_category.append({
                'Crime_Category': cat_name,
                'LagDayCount': lag_count,
                'TotalCount': total,
            })
        by_crime_category.sort(key=lambda x: (-x['TotalCount'], x['Crime_Category']))
        total_lag = sum(r['LagDayCount'] for r in by_crime_category)
        total_all = sum(r['TotalCount'] for r in by_crime_category)
        by_crime_category.append({
            'Crime_Category': 'TOTAL',
            'LagDayCount': total_lag,
            'TotalCount': total_all,
        })

    # LagDays distribution (for actual 7-Day period incidents only, not backfill)
    lagdays_distribution = {}
    if 'Period' in df_7day.columns and 'IncidentToReportDays' in df_7day.columns and len(df_7day) > 0:
        # Filter to only 7-Day period incidents that have reporting delay
        df_7day_period_only = df_7day[df_7day['Period'] == '7-Day'].copy()
        if len(df_7day_period_only) > 0:
            # Use IncidentToReportDays for reporting delay (not cycle-based LagDays)
            lag_values = df_7day_period_only['IncidentToReportDays'].dropna()
            lag_values = lag_values[lag_values > 0]  # Only incidents with actual reporting delay
            if len(lag_values) > 0:
                lagdays_distribution = {
                    'min': int(lag_values.min()),
                    'max': int(lag_values.max()),
                    'mean': round(float(lag_values.mean()), 1),
                    'median': int(lag_values.median()),
                    'ranges': {
                        '1-7_days': int(((lag_values >= 1) & (lag_values <= 7)).sum()),
                        '8-14_days': int(((lag_values >= 8) & (lag_values <= 14)).sum()),
                        '15-28_days': int(((lag_values >= 15) & (lag_values <= 28)).sum()),
                        '29+_days': int((lag_values >= 29).sum()),
                    }
                }

    # Period breakdown in 7-day data
    period_breakdown = {}
    if 'Period' in df_7day.columns and len(df_7day) > 0:
        period_breakdown = df_7day['Period'].value_counts().to_dict()

    # Build summary
    summary = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'generator': 'scripts/prepare_7day_outputs.py',
            'version': '1.0.0'
        },
        'cycle': {
            'name': cycle_name or (cycle_info.get('name') if cycle_info else None),
            'report_due_date': report_due or (cycle_info.get('report_due') if cycle_info else None),
            '7_day_start': cycle_start or (cycle_info.get('start_7') if cycle_info else None),
            '7_day_end': cycle_end or (cycle_info.get('end_7') if cycle_info else None),
        },
        'counts': {
            'total_all_crimes': len(df_full),
            'total_7day_window': len(df_7day),
            'incidents_in_7day_period': len(df_7day[df_7day['Period'] == '7-Day']) if 'Period' in df_7day.columns else 0,
            'lag_incidents': len(df_lag_only),
            'backfill_7day': len(df_lag_only),
        },
        'lag_analysis': {
            'by_crime_category': lag_by_category,
            'lagdays_distribution': lagdays_distribution,
        },
        '7day_by_crime_category': by_crime_category,
        'period_breakdown': period_breakdown,
        'incident_date_range': {
            'earliest': str(min_incident) if min_incident else None,
            'latest': str(max_incident) if max_incident else None,
        }
    }

    return summary


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def save_7day_outputs(
    df_full: pd.DataFrame,
    output_dir: Path,
    cycle_info: Optional[Dict[str, Any]] = None,
    timestamp: bool = False
) -> Tuple[Path, Path]:
    """
    Generate and save 7-day output files (streamlined: 2 files only).

    Writes:
    1. SCRPA_7Day_With_LagFlags.csv - rows where Report Date falls within 7-Day period
    2. SCRPA_7Day_Summary.json - metadata including 7day_by_crime_category (Crime_Category, LagDayCount, TotalCount, TOTAL)

    Args:
        df_full: Full enriched DataFrame
        output_dir: Output directory path
        cycle_info: Optional cycle information dict
        timestamp: If True, also write timestamped copies (default False for clean Data folder)

    Returns:
        Tuple of (7day_csv_path, summary_json_path)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Filter: Report Date within 7-Day period (IsCurrent7DayCycle = TRUE)
    df_7day = filter_7day_by_report_date(df_full)
    df_lag_only = extract_backfill_lag(df_full)
    df_7day_and_lag = extract_7day_and_lag(df_full)

    # Generate summary (includes 7day_by_crime_category: Crime_Category, LagDayCount, TotalCount, TOTAL)
    summary = generate_lagday_summary(df_full, df_7day, df_lag_only, cycle_info)

    # Save 7-Day CSV only (no separate Lag-Only CSV)
    csv_7day_path = output_dir / 'SCRPA_7Day_With_LagFlags.csv'
    df_7day.to_csv(csv_7day_path, index=False)
    print(f"  Saved 7-Day filtered: {csv_7day_path.name} ({len(df_7day)} rows)")

    # Save JSON summary (replaces YAML for better compatibility)
    json_path = output_dir / 'SCRPA_7Day_Summary.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"  Saved JSON summary: {json_path.name}")

    return csv_7day_path, json_path


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """Command-line interface for prepare_7day_outputs."""
    parser = argparse.ArgumentParser(
        description='SCRPA 7-Day Outputs - Filter and generate lag day metadata'
    )
    parser.add_argument(
        'input',
        help='Path to enriched SCRPA CSV file (from scrpa_transform.py)'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='Output directory (default: same as input)',
        default=None
    )
    parser.add_argument(
        '--no-timestamp',
        action='store_true',
        help='Do not include timestamp in output filenames'
    )
    parser.add_argument(
        '--cycle-name',
        help='Cycle name for metadata (e.g., 26C01W04)',
        default=None
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir) if args.output_dir else input_path.parent

    print(f"Loading enriched data: {input_path}")
    df = pd.read_csv(input_path, low_memory=False)
    print(f"  {len(df)} rows loaded")

    # Parse boolean columns
    for col in ['IsCurrent7DayCycle', 'IsLagDay', 'Backfill_7Day']:
        if col in df.columns:
            df[col] = df[col].map({
                True: True, False: False,
                'TRUE': True, 'FALSE': False,
                'True': True, 'False': False,
                1: True, 0: False
            }).fillna(False)

    # Build cycle info if provided
    cycle_info = None
    if args.cycle_name:
        cycle_info = {'name': args.cycle_name}

    print(f"\nGenerating 7-day outputs to: {output_dir}")
    save_7day_outputs(
        df,
        output_dir,
        cycle_info=cycle_info,
        timestamp=not args.no_timestamp
    )

    # Print summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Total rows: {len(df)}")
    print(f"  IsCurrent7DayCycle=TRUE: {(df['IsCurrent7DayCycle'] == True).sum()}")
    print(f"  Backfill_7Day=TRUE: {(df['Backfill_7Day'] == True).sum()}")
    if 'Period' in df.columns:
        print(f"  Period=7-Day: {(df['Period'] == '7-Day').sum()}")
    print("=" * 50)


if __name__ == '__main__':
    main()
