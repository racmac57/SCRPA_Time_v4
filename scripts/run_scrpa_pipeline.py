# 2026_01_28
# Project: scripts/run_scrpa_pipeline.py
# Author: R. A. Carucci
# Purpose: Main orchestration script for SCRPA Python-first processing pipeline.

"""
SCRPA Pipeline Orchestrator

This script is the main entry point that runs the entire SCRPA data processing pipeline:
1. Load RMS export and cycle calendar
2. Run scrpa_transform.py -> SCRPA_All_Crimes_Enhanced.csv
3. Run prepare_7day_outputs.py -> 7-day filtered CSVs + metadata
4. Run generate_documentation.py -> Documentation folder contents
5. Optionally validate outputs against reference CSV
6. Generate summary report

Usage:
    python run_scrpa_pipeline.py input.csv --report-date 01/27/2026 -o Time_Based/2026/26C01W04_26_01_27

Output Structure:
    {output_dir}/
    ├── Data/
    │   ├── SCRPA_All_Crimes_Enhanced.csv
    │   ├── SCRPA_7Day_With_LagFlags.csv
    │   ├── SCRPA_7Day_Lag_Only.csv
    │   └── SCRPA_7Day_Summary.yaml/json
    ├── Documentation/
    │   ├── data_dictionary.yaml/json
    │   ├── PROJECT_SUMMARY.yaml/json
    │   ├── claude.md
    │   ├── SCRPA_Report_Summary.md
    │   └── EMAIL_TEMPLATE.txt
    └── Reports/
        └── (placeholder for Power BI exports)
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any
import argparse
import pandas as pd

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import our modules
from scrpa_transform import (
    read_rms_export,
    load_cycle_calendar,
    build_all_crimes_enhanced,
    resolve_cycle,
    CYCLE_CALENDAR_PATH
)
from prepare_7day_outputs import save_7day_outputs
from generate_documentation import generate_all_documentation


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA")
TIME_BASED_DIR = BASE_DIR / "Time_Based"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_output_structure(base_dir: Path, cycle_name: str, report_date: date) -> Dict[str, Path]:
    """
    Create the output folder structure for a reporting cycle.

    Args:
        base_dir: Base output directory (e.g., Time_Based/2026)
        cycle_name: Cycle name (e.g., 26C01W04)
        report_date: Report due date

    Returns:
        Dictionary with paths to Data, Documentation, Reports folders
    """
    # Format: CYCLE_YY_MM_DD
    date_suffix = report_date.strftime('%y_%m_%d')
    folder_name = f"{cycle_name}_{date_suffix}"

    root = base_dir / folder_name
    paths = {
        'root': root,
        'data': root / 'Data',
        'documentation': root / 'Documentation',
        'reports': root / 'Reports'
    }

    # Create directories
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)

    return paths


def get_biweekly_info(calendar_df: pd.DataFrame, cycle: pd.Series) -> Dict[str, Any]:
    """
    Extract bi-weekly information from cycle data.

    Args:
        calendar_df: Cycle calendar DataFrame
        cycle: Series with current cycle info

    Returns:
        Dictionary with bi-weekly details
    """
    info = {
        'name': cycle['Report_Name'],
        'report_due': cycle['Report_Due_Date'].strftime('%m/%d/%Y') if isinstance(cycle['Report_Due_Date'], date) else str(cycle['Report_Due_Date']),
        'start_7': cycle['7_Day_Start'].strftime('%m/%d/%Y') if isinstance(cycle['7_Day_Start'], date) else str(cycle['7_Day_Start']),
        'end_7': cycle['7_Day_End'].strftime('%m/%d/%Y') if isinstance(cycle['7_Day_End'], date) else str(cycle['7_Day_End']),
        'start_28': cycle['28_Day_Start'].strftime('%m/%d/%Y') if isinstance(cycle['28_Day_Start'], date) else str(cycle['28_Day_Start']),
        'end_28': cycle['28_Day_End'].strftime('%m/%d/%Y') if isinstance(cycle['28_Day_End'], date) else str(cycle['28_Day_End']),
        'biweekly': None,
        'start_bw': None,
        'end_bw': None
    }

    # Check for bi-weekly name
    if 'BiWeekly_Report_Name' in cycle.index:
        bw_name = cycle['BiWeekly_Report_Name']
        if pd.notna(bw_name) and str(bw_name).strip():
            info['biweekly'] = str(bw_name).strip()

            # Calculate bi-weekly period
            start_7_date = cycle['7_Day_Start']
            if isinstance(start_7_date, date):
                start_bw_date = start_7_date - timedelta(days=7)
                info['start_bw'] = start_bw_date.strftime('%m/%d/%Y')
                info['end_bw'] = info['end_7']

    return info


def create_email_template(
    output_dir: Path,
    cycle_info: Dict[str, Any],
    generation_date: str
) -> Path:
    """
    Create email template for bi-weekly report distribution.

    Args:
        output_dir: Documentation folder path
        cycle_info: Cycle information dictionary
        generation_date: Date string for email

    Returns:
        Path to created email template
    """
    cycle_name = cycle_info['name']
    biweekly = cycle_info.get('biweekly')

    # Determine date range for email
    if biweekly and cycle_info.get('start_bw') and cycle_info.get('end_bw'):
        date_range = f"{cycle_info['start_bw']} - {cycle_info['end_bw']}"
        cycle_display = biweekly
        body_cycle = f"Bi-Weekly Cycle {biweekly} ({cycle_name})"
    else:
        date_range = f"{cycle_info['start_7']} - {cycle_info['end_7']}"
        cycle_display = cycle_name
        body_cycle = f"Cycle {cycle_name}"

    email_template = f"""Subject: SCRPA Bi-Weekly Report - Cycle {cycle_display} | {date_range}

Sir,

Please find attached the Strategic Crime Reduction Plan Analysis Combined Executive Summary for {body_cycle}.

Report Period: {date_range}
Date Generated: {generation_date}

The report includes:
- 7-Day Executive Summary with detailed incident summaries
- ArcGIS Map visuals showing incidents occurring in the last 7 days
- Statistical charts and visualizations by crime type
- 28-Day Executive Summary (operational planning)
- YTD Executive Summary (strategic analysis)

Please let me know if you have any questions or require additional information.
"""

    email_path = output_dir / 'EMAIL_TEMPLATE.txt'
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(email_template)

    return email_path


def print_summary(
    df_enhanced: pd.DataFrame,
    cycle_info: Dict[str, Any],
    paths: Dict[str, Path]
) -> None:
    """Print pipeline execution summary."""
    print("\n" + "=" * 70)
    print("SCRPA PIPELINE EXECUTION SUMMARY")
    print("=" * 70)

    print(f"\nCycle: {cycle_info['name']}")
    if cycle_info.get('biweekly'):
        print(f"Bi-Weekly: {cycle_info['biweekly']}")
    print(f"Report Due: {cycle_info['report_due']}")
    print(f"7-Day Window: {cycle_info['start_7']} - {cycle_info['end_7']}")
    if cycle_info.get('start_bw'):
        print(f"Bi-Weekly Period: {cycle_info['start_bw']} - {cycle_info['end_bw']}")

    print(f"\nOutput Directory: {paths['root']}")

    print(f"\nData Summary:")
    print(f"  Total incidents: {len(df_enhanced)}")
    if 'Period' in df_enhanced.columns:
        print(f"  Period breakdown:")
        for period, count in df_enhanced['Period'].value_counts().items():
            print(f"    {period}: {count}")

    if 'IsLagDay' in df_enhanced.columns:
        lag_count = df_enhanced['IsLagDay'].sum()
        print(f"  Lag incidents: {lag_count}")

    if 'Backfill_7Day' in df_enhanced.columns:
        backfill_count = df_enhanced['Backfill_7Day'].sum()
        print(f"  Backfill 7-Day: {backfill_count}")

    print("\nGenerated Files:")
    print(f"  Data/")
    for f in paths['data'].iterdir():
        print(f"    - {f.name}")
    print(f"  Documentation/")
    for f in paths['documentation'].iterdir():
        print(f"    - {f.name}")

    print("=" * 70)


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_pipeline(
    rms_path: Path,
    output_dir: Optional[Path] = None,
    report_due_date: Optional[date] = None,
    calendar_path: Path = CYCLE_CALENDAR_PATH,
    validate_reference: Optional[Path] = None,
    today_override: Optional[date] = None
) -> Dict[str, Any]:
    """
    Run the complete SCRPA data processing pipeline.

    Args:
        rms_path: Path to RMS export file
        output_dir: Optional output directory (auto-generated if not provided)
        report_due_date: Optional report due date (defaults to today)
        calendar_path: Path to cycle calendar CSV
        validate_reference: Optional path to reference CSV for validation
        today_override: Optional override for "today" (for testing)

    Returns:
        Dictionary with pipeline results
    """
    start_time = datetime.now()
    results = {
        'success': False,
        'start_time': start_time.isoformat(),
        'end_time': None,
        'files_created': []
    }

    try:
        # =================================================================
        # STEP 1: Load data
        # =================================================================
        print("=" * 70)
        print("SCRPA PIPELINE - Python-First Crime Data Processing")
        print("=" * 70)

        print(f"\n[1/5] Loading data...")
        print(f"  RMS Export: {rms_path}")
        rms_df = read_rms_export(rms_path)
        print(f"  Loaded {len(rms_df)} rows from RMS export")

        print(f"  Cycle Calendar: {calendar_path}")
        calendar_df = load_cycle_calendar(calendar_path)
        print(f"  Loaded {len(calendar_df)} cycles")

        # Set today
        today = today_override or date.today()

        # Resolve cycle
        if report_due_date:
            cycle = resolve_cycle(calendar_df, report_due_date)
        else:
            cycle = resolve_cycle(calendar_df, today)
            report_due_date = today

        if cycle is None:
            raise ValueError(f"Could not resolve cycle for date: {report_due_date}")

        cycle_info = get_biweekly_info(calendar_df, cycle)
        print(f"  Resolved cycle: {cycle_info['name']}")
        if cycle_info.get('biweekly'):
            print(f"  Bi-Weekly cycle: {cycle_info['biweekly']}")

        # =================================================================
        # STEP 2: Create output structure
        # =================================================================
        print(f"\n[2/5] Creating output structure...")

        if output_dir:
            paths = {
                'root': Path(output_dir),
                'data': Path(output_dir) / 'Data',
                'documentation': Path(output_dir) / 'Documentation',
                'reports': Path(output_dir) / 'Reports'
            }
            for path in paths.values():
                path.mkdir(parents=True, exist_ok=True)
        else:
            year = report_due_date.year
            year_dir = TIME_BASED_DIR / str(year)
            paths = create_output_structure(year_dir, cycle_info['name'], report_due_date)

        print(f"  Output directory: {paths['root']}")

        # =================================================================
        # STEP 3: Transform data
        # =================================================================
        print(f"\n[3/5] Transforming data (scrpa_transform)...")
        df_enhanced = build_all_crimes_enhanced(
            rms_df,
            calendar_df,
            report_due_date=cycle['Report_Due_Date'] if isinstance(cycle['Report_Due_Date'], date) else report_due_date,
            today=today
        )
        print(f"  Generated {len(df_enhanced)} enriched rows")

        # Save main enhanced CSV
        enhanced_csv = paths['data'] / 'SCRPA_All_Crimes_Enhanced.csv'
        df_enhanced.to_csv(enhanced_csv, index=False)
        results['files_created'].append(str(enhanced_csv))
        print(f"  Saved: {enhanced_csv.name}")

        # Also save timestamped version
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        enhanced_csv_ts = paths['data'] / f'SCRPA_All_Crimes_Enhanced_{ts}.csv'
        df_enhanced.to_csv(enhanced_csv_ts, index=False)
        results['files_created'].append(str(enhanced_csv_ts))

        # =================================================================
        # STEP 4: Generate 7-day outputs
        # =================================================================
        print(f"\n[4/5] Generating 7-day outputs (prepare_7day_outputs)...")
        csv_7day, csv_lag, yaml_summary, json_summary = save_7day_outputs(
            df_enhanced,
            paths['data'],
            cycle_info=cycle_info,
            timestamp=True
        )
        results['files_created'].extend([str(csv_7day), str(csv_lag), str(yaml_summary), str(json_summary)])

        # =================================================================
        # STEP 5: Generate documentation
        # =================================================================
        print(f"\n[5/5] Generating documentation (generate_documentation)...")
        doc_results = generate_all_documentation(paths['documentation'], cycle_info)
        for doc_files in doc_results.values():
            results['files_created'].extend([str(f) for f in doc_files])

        # Create email template
        generation_date = datetime.now().strftime('%m/%d/%Y')
        email_path = create_email_template(paths['documentation'], cycle_info, generation_date)
        results['files_created'].append(str(email_path))
        print(f"  Created: {email_path.name}")

        # =================================================================
        # OPTIONAL: Validate against reference
        # =================================================================
        if validate_reference:
            print(f"\n[VALIDATION] Comparing against: {validate_reference}")
            try:
                from validate_parity import validate_parity
                validation_result = validate_parity(enhanced_csv, validate_reference)
                results['validation'] = validation_result
                if validation_result.get('passed'):
                    print("  Validation PASSED")
                else:
                    print("  Validation FAILED - see validation report")
            except ImportError:
                print("  Validation script not available - skipping")

        # =================================================================
        # Summary
        # =================================================================
        print_summary(df_enhanced, cycle_info, paths)

        results['success'] = True
        results['cycle_info'] = cycle_info
        results['output_dir'] = str(paths['root'])
        results['row_count'] = len(df_enhanced)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        results['error'] = str(e)

    finally:
        end_time = datetime.now()
        results['end_time'] = end_time.isoformat()
        results['duration_seconds'] = (end_time - start_time).total_seconds()

    return results


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """Command-line interface for run_scrpa_pipeline."""
    parser = argparse.ArgumentParser(
        description='SCRPA Pipeline - Python-First Crime Data Processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process with auto-detected cycle (based on today)
  python run_scrpa_pipeline.py rms_export.csv

  # Process for specific report date
  python run_scrpa_pipeline.py rms_export.csv --report-date 01/27/2026

  # Process with custom output directory
  python run_scrpa_pipeline.py rms_export.csv -o Time_Based/2026/26C01W04_26_01_27

  # Process and validate against reference
  python run_scrpa_pipeline.py rms_export.csv --validate reference.csv
"""
    )
    parser.add_argument(
        'input',
        help='Path to RMS export CSV or Excel file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output directory (auto-generated if not provided)',
        default=None
    )
    parser.add_argument(
        '--report-date',
        help='Report due date (MM/DD/YYYY format)',
        default=None
    )
    parser.add_argument(
        '--calendar',
        help='Path to cycle calendar CSV',
        default=str(CYCLE_CALENDAR_PATH)
    )
    parser.add_argument(
        '--validate',
        help='Path to reference CSV for validation',
        default=None
    )
    parser.add_argument(
        '--today',
        help='Override today date (MM/DD/YYYY format) for testing',
        default=None
    )

    args = parser.parse_args()

    # Parse dates
    report_due_date = None
    if args.report_date:
        report_due_date = datetime.strptime(args.report_date, '%m/%d/%Y').date()

    today_override = None
    if args.today:
        today_override = datetime.strptime(args.today, '%m/%d/%Y').date()

    # Run pipeline
    results = run_pipeline(
        rms_path=Path(args.input),
        output_dir=Path(args.output) if args.output else None,
        report_due_date=report_due_date,
        calendar_path=Path(args.calendar),
        validate_reference=Path(args.validate) if args.validate else None,
        today_override=today_override
    )

    # Exit code
    return 0 if results['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
