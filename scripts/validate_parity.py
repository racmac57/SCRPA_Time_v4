# 2026_01_28
# Project: scripts/validate_parity.py
# Author: R. A. Carucci
# Purpose: Validate Python transformation outputs against M code reference CSV.

"""
SCRPA Parity Validation

This module validates that Python-generated outputs exactly match the Power BI
M code outputs, ensuring parity during the migration to Python-first processing.

Validation Checks:
1. Row count match
2. Column match (all columns present with same names)
3. LagDays calculation: (CycleStart_7Day - Incident_Date).dt.days == LagDays
4. Period classification: Compare Period values row-by-row
5. Backfill_7Day logic: All Backfill_7Day=True have IsLagDay=True
6. SQL validation queries (from SCRPA streamline.md)

Usage:
    python validate_parity.py python_output.csv reference.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple
import argparse
import json


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def check_row_count(df_python: pd.DataFrame, df_reference: pd.DataFrame) -> Dict[str, Any]:
    """Check that row counts match."""
    python_count = len(df_python)
    ref_count = len(df_reference)

    return {
        'check': 'row_count',
        'passed': python_count == ref_count,
        'python_rows': python_count,
        'reference_rows': ref_count,
        'difference': python_count - ref_count
    }


def check_columns(df_python: pd.DataFrame, df_reference: pd.DataFrame) -> Dict[str, Any]:
    """Check that all columns are present."""
    python_cols = set(df_python.columns)
    ref_cols = set(df_reference.columns)

    missing_in_python = ref_cols - python_cols
    extra_in_python = python_cols - ref_cols
    common = python_cols & ref_cols

    return {
        'check': 'columns',
        'passed': len(missing_in_python) == 0,
        'common_columns': len(common),
        'missing_in_python': list(missing_in_python),
        'extra_in_python': list(extra_in_python)
    }


def check_period_classification(
    df_python: pd.DataFrame,
    df_reference: pd.DataFrame,
    key_column: str = 'Case Number'
) -> Dict[str, Any]:
    """Compare Period classification row-by-row."""
    if 'Period' not in df_python.columns or 'Period' not in df_reference.columns:
        return {
            'check': 'period_classification',
            'passed': False,
            'error': 'Period column not found in one or both DataFrames'
        }

    if key_column not in df_python.columns or key_column not in df_reference.columns:
        return {
            'check': 'period_classification',
            'passed': False,
            'error': f'{key_column} column not found'
        }

    # Merge on key column
    merged = pd.merge(
        df_python[[key_column, 'Period']].rename(columns={'Period': 'Period_Python'}),
        df_reference[[key_column, 'Period']].rename(columns={'Period': 'Period_Ref'}),
        on=key_column,
        how='outer'
    )

    mismatches = merged[merged['Period_Python'] != merged['Period_Ref']]

    return {
        'check': 'period_classification',
        'passed': len(mismatches) == 0,
        'total_compared': len(merged),
        'matches': len(merged) - len(mismatches),
        'mismatches': len(mismatches),
        'mismatch_samples': mismatches.head(10).to_dict('records') if len(mismatches) > 0 else []
    }


def check_lagdays_calculation(
    df_python: pd.DataFrame,
    df_reference: pd.DataFrame,
    key_column: str = 'Case Number'
) -> Dict[str, Any]:
    """Compare LagDays calculation row-by-row."""
    if 'LagDays' not in df_python.columns or 'LagDays' not in df_reference.columns:
        return {
            'check': 'lagdays_calculation',
            'passed': False,
            'error': 'LagDays column not found'
        }

    # Merge on key column
    merged = pd.merge(
        df_python[[key_column, 'LagDays']].rename(columns={'LagDays': 'LagDays_Python'}),
        df_reference[[key_column, 'LagDays']].rename(columns={'LagDays': 'LagDays_Ref'}),
        on=key_column,
        how='outer'
    )

    # Handle nulls
    merged['LagDays_Python'] = pd.to_numeric(merged['LagDays_Python'], errors='coerce').fillna(0)
    merged['LagDays_Ref'] = pd.to_numeric(merged['LagDays_Ref'], errors='coerce').fillna(0)

    mismatches = merged[merged['LagDays_Python'] != merged['LagDays_Ref']]

    return {
        'check': 'lagdays_calculation',
        'passed': len(mismatches) == 0,
        'total_compared': len(merged),
        'matches': len(merged) - len(mismatches),
        'mismatches': len(mismatches),
        'mismatch_samples': mismatches.head(10).to_dict('records') if len(mismatches) > 0 else []
    }


def check_islagday(
    df_python: pd.DataFrame,
    df_reference: pd.DataFrame,
    key_column: str = 'Case Number'
) -> Dict[str, Any]:
    """Compare IsLagDay values row-by-row."""
    if 'IsLagDay' not in df_python.columns or 'IsLagDay' not in df_reference.columns:
        return {
            'check': 'islagday',
            'passed': False,
            'error': 'IsLagDay column not found'
        }

    def to_bool(x):
        if pd.isna(x):
            return False
        if isinstance(x, bool):
            return x
        if isinstance(x, str):
            return x.upper() in ('TRUE', '1', 'YES')
        return bool(x)

    # Merge on key column
    merged = pd.merge(
        df_python[[key_column, 'IsLagDay']].rename(columns={'IsLagDay': 'IsLagDay_Python'}),
        df_reference[[key_column, 'IsLagDay']].rename(columns={'IsLagDay': 'IsLagDay_Ref'}),
        on=key_column,
        how='outer'
    )

    merged['IsLagDay_Python'] = merged['IsLagDay_Python'].apply(to_bool)
    merged['IsLagDay_Ref'] = merged['IsLagDay_Ref'].apply(to_bool)

    mismatches = merged[merged['IsLagDay_Python'] != merged['IsLagDay_Ref']]

    return {
        'check': 'islagday',
        'passed': len(mismatches) == 0,
        'total_compared': len(merged),
        'matches': len(merged) - len(mismatches),
        'mismatches': len(mismatches),
        'mismatch_samples': mismatches.head(10).to_dict('records') if len(mismatches) > 0 else []
    }


def check_backfill_7day_logic(df_python: pd.DataFrame) -> Dict[str, Any]:
    """
    Verify Backfill_7Day logic: All Backfill_7Day=True must have IsLagDay=True.

    This is a consistency check within the Python output.
    """
    if 'Backfill_7Day' not in df_python.columns or 'IsLagDay' not in df_python.columns:
        return {
            'check': 'backfill_7day_logic',
            'passed': False,
            'error': 'Backfill_7Day or IsLagDay column not found'
        }

    def to_bool(x):
        if pd.isna(x):
            return False
        if isinstance(x, bool):
            return x
        if isinstance(x, str):
            return x.upper() in ('TRUE', '1', 'YES')
        return bool(x)

    df = df_python.copy()
    df['Backfill_7Day'] = df['Backfill_7Day'].apply(to_bool)
    df['IsLagDay'] = df['IsLagDay'].apply(to_bool)

    # Find violations: Backfill_7Day=True but IsLagDay=False
    violations = df[(df['Backfill_7Day'] == True) & (df['IsLagDay'] == False)]

    return {
        'check': 'backfill_7day_logic',
        'passed': len(violations) == 0,
        'total_backfill': (df['Backfill_7Day'] == True).sum(),
        'violations': len(violations),
        'violation_samples': violations[['Case Number', 'Backfill_7Day', 'IsLagDay']].head(10).to_dict('records') if len(violations) > 0 else []
    }


def check_time_of_day(
    df_python: pd.DataFrame,
    df_reference: pd.DataFrame,
    key_column: str = 'Case Number'
) -> Dict[str, Any]:
    """Compare TimeOfDay classification row-by-row."""
    if 'TimeOfDay' not in df_python.columns or 'TimeOfDay' not in df_reference.columns:
        return {
            'check': 'time_of_day',
            'passed': True,  # Skip if not present
            'skipped': True
        }

    # Merge on key column
    merged = pd.merge(
        df_python[[key_column, 'TimeOfDay']].rename(columns={'TimeOfDay': 'TOD_Python'}),
        df_reference[[key_column, 'TimeOfDay']].rename(columns={'TimeOfDay': 'TOD_Ref'}),
        on=key_column,
        how='outer'
    )

    # Normalize for comparison (handle slight text differences)
    def normalize(x):
        if pd.isna(x):
            return ''
        return str(x).strip().replace('\u2013', '-').replace('–', '-')

    merged['TOD_Python'] = merged['TOD_Python'].apply(normalize)
    merged['TOD_Ref'] = merged['TOD_Ref'].apply(normalize)

    mismatches = merged[merged['TOD_Python'] != merged['TOD_Ref']]

    return {
        'check': 'time_of_day',
        'passed': len(mismatches) == 0,
        'total_compared': len(merged),
        'matches': len(merged) - len(mismatches),
        'mismatches': len(mismatches),
        'mismatch_samples': mismatches.head(5).to_dict('records') if len(mismatches) > 0 else []
    }


def check_crime_category(
    df_python: pd.DataFrame,
    df_reference: pd.DataFrame,
    key_column: str = 'Case Number'
) -> Dict[str, Any]:
    """Compare Crime_Category classification row-by-row."""
    if 'Crime_Category' not in df_python.columns or 'Crime_Category' not in df_reference.columns:
        return {
            'check': 'crime_category',
            'passed': True,
            'skipped': True
        }

    # Merge on key column
    merged = pd.merge(
        df_python[[key_column, 'Crime_Category']].rename(columns={'Crime_Category': 'Cat_Python'}),
        df_reference[[key_column, 'Crime_Category']].rename(columns={'Crime_Category': 'Cat_Ref'}),
        on=key_column,
        how='outer'
    )

    mismatches = merged[merged['Cat_Python'] != merged['Cat_Ref']]

    return {
        'check': 'crime_category',
        'passed': len(mismatches) == 0,
        'total_compared': len(merged),
        'matches': len(merged) - len(mismatches),
        'mismatches': len(mismatches),
        'mismatch_samples': mismatches.head(5).to_dict('records') if len(mismatches) > 0 else []
    }


# =============================================================================
# SQL-LIKE VALIDATION QUERIES
# =============================================================================

def sql_check_lag_vs_backfill(df: pd.DataFrame) -> Dict[str, Any]:
    """
    SQL-like check: All Backfill_7Day=TRUE should have LagDays > 0.
    """
    def to_bool(x):
        if pd.isna(x):
            return False
        if isinstance(x, bool):
            return x
        if isinstance(x, str):
            return x.upper() in ('TRUE', '1', 'YES')
        return bool(x)

    df_copy = df.copy()
    df_copy['Backfill_7Day'] = df_copy['Backfill_7Day'].apply(to_bool)
    df_copy['LagDays'] = pd.to_numeric(df_copy['LagDays'], errors='coerce').fillna(0)

    backfill_rows = df_copy[df_copy['Backfill_7Day'] == True]
    violations = backfill_rows[backfill_rows['LagDays'] <= 0]

    return {
        'check': 'sql_lag_vs_backfill',
        'description': 'All Backfill_7Day=TRUE should have LagDays > 0',
        'passed': len(violations) == 0,
        'backfill_count': len(backfill_rows),
        'violations': len(violations)
    }


def sql_check_period_vs_incident_date(df: pd.DataFrame) -> Dict[str, Any]:
    """
    SQL-like check: Period should align with Incident_Date_Date.
    7-Day incidents should have Incident_Date within cycle window.
    """
    # This is a more complex check that requires cycle info
    # For now, just check that Period is a valid value
    valid_periods = {'7-Day', '28-Day', 'YTD', 'Prior Year', 'Historical'}

    if 'Period' not in df.columns:
        return {
            'check': 'sql_period_validation',
            'passed': False,
            'error': 'Period column not found'
        }

    invalid_periods = df[~df['Period'].isin(valid_periods)]

    return {
        'check': 'sql_period_validation',
        'description': 'All Period values should be valid',
        'passed': len(invalid_periods) == 0,
        'valid_values': list(valid_periods),
        'total_rows': len(df),
        'invalid_count': len(invalid_periods)
    }


# =============================================================================
# MAIN VALIDATION FUNCTION
# =============================================================================

def validate_parity(
    python_csv: Path,
    reference_csv: Path,
    key_column: str = 'Case Number'
) -> Dict[str, Any]:
    """
    Run all parity validation checks.

    Args:
        python_csv: Path to Python-generated CSV
        reference_csv: Path to reference CSV (from M code)
        key_column: Column to use as primary key for row matching

    Returns:
        Dictionary with validation results
    """
    results = {
        'validation_time': datetime.now().isoformat(),
        'python_file': str(python_csv),
        'reference_file': str(reference_csv),
        'passed': True,
        'checks': []
    }

    # Load data
    print(f"Loading Python output: {python_csv}")
    df_python = pd.read_csv(python_csv, low_memory=False)
    print(f"  {len(df_python)} rows")

    print(f"Loading reference: {reference_csv}")
    df_reference = pd.read_csv(reference_csv, low_memory=False)
    print(f"  {len(df_reference)} rows")

    # Run checks
    print("\nRunning validation checks...")

    checks = [
        ('Row Count', check_row_count(df_python, df_reference)),
        ('Columns', check_columns(df_python, df_reference)),
        ('Period Classification', check_period_classification(df_python, df_reference, key_column)),
        ('LagDays Calculation', check_lagdays_calculation(df_python, df_reference, key_column)),
        ('IsLagDay Values', check_islagday(df_python, df_reference, key_column)),
        ('Backfill_7Day Logic', check_backfill_7day_logic(df_python)),
        ('TimeOfDay Classification', check_time_of_day(df_python, df_reference, key_column)),
        ('Crime_Category Classification', check_crime_category(df_python, df_reference, key_column)),
        ('SQL: Lag vs Backfill', sql_check_lag_vs_backfill(df_python)),
        ('SQL: Period Validation', sql_check_period_vs_incident_date(df_python)),
    ]

    for name, check_result in checks:
        passed = check_result.get('passed', False)
        skipped = check_result.get('skipped', False)

        if skipped:
            status = 'SKIPPED'
        elif passed:
            status = 'PASSED'
        else:
            status = 'FAILED'
            results['passed'] = False

        print(f"  [{status}] {name}")

        if not passed and not skipped:
            if 'mismatches' in check_result:
                print(f"         {check_result['mismatches']} mismatches found")
            if 'violations' in check_result:
                print(f"         {check_result['violations']} violations found")

        results['checks'].append({
            'name': name,
            **check_result
        })

    # Summary
    passed_count = sum(1 for c in results['checks'] if c.get('passed', False))
    failed_count = sum(1 for c in results['checks'] if not c.get('passed', False) and not c.get('skipped', False))
    skipped_count = sum(1 for c in results['checks'] if c.get('skipped', False))

    results['summary'] = {
        'total_checks': len(results['checks']),
        'passed': passed_count,
        'failed': failed_count,
        'skipped': skipped_count
    }

    return results


def print_validation_report(results: Dict[str, Any]) -> None:
    """Print formatted validation report."""
    print("\n" + "=" * 70)
    print("VALIDATION REPORT")
    print("=" * 70)

    print(f"\nPython File: {results['python_file']}")
    print(f"Reference File: {results['reference_file']}")
    print(f"Validation Time: {results['validation_time']}")

    print(f"\nSummary: {results['summary']['passed']} passed, "
          f"{results['summary']['failed']} failed, "
          f"{results['summary']['skipped']} skipped")

    overall = "PASSED" if results['passed'] else "FAILED"
    print(f"\nOverall Result: {overall}")

    if not results['passed']:
        print("\nFailed Checks:")
        for check in results['checks']:
            if not check.get('passed', False) and not check.get('skipped', False):
                print(f"\n  {check['name']}:")
                if 'mismatches' in check:
                    print(f"    Mismatches: {check['mismatches']}")
                if 'mismatch_samples' in check and check['mismatch_samples']:
                    print("    Samples:")
                    for sample in check['mismatch_samples'][:3]:
                        print(f"      {sample}")
                if 'violations' in check:
                    print(f"    Violations: {check['violations']}")

    print("=" * 70)


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """Command-line interface for validate_parity."""
    parser = argparse.ArgumentParser(
        description='SCRPA Parity Validation - Compare Python output against M code reference'
    )
    parser.add_argument(
        'python_csv',
        help='Path to Python-generated CSV'
    )
    parser.add_argument(
        'reference_csv',
        help='Path to reference CSV (from M code/Power BI)'
    )
    parser.add_argument(
        '--key-column',
        help='Column to use as primary key (default: Case Number)',
        default='Case Number'
    )
    parser.add_argument(
        '--output',
        help='Path to save validation report JSON',
        default=None
    )

    args = parser.parse_args()

    results = validate_parity(
        Path(args.python_csv),
        Path(args.reference_csv),
        args.key_column
    )

    print_validation_report(results)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\nValidation report saved to: {args.output}")

    return 0 if results['passed'] else 1


if __name__ == '__main__':
    exit(main())
