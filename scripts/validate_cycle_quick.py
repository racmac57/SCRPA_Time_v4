"""
Quick post-pipeline validation for SCRPA cycle folders.
Runs 3 checks: file existence, row count, and lag/backfill alignment.

Usage:
    python validate_cycle_quick.py <cycle_folder_path>

Exit codes:
    0 = all 3 checks passed
    1 = one or more checks failed
"""
import sys
import json
from pathlib import Path

import pandas as pd


def check_file_existence(cycle_dir: Path) -> bool:
    """CHECK 1: Verify required output files exist."""
    required = [
        cycle_dir / "Data" / "SCRPA_7Day_Summary.json",
        cycle_dir / "Data" / "SCRPA_All_Crimes_Enhanced.csv",
        cycle_dir / "Documentation" / "SCRPA_Report_Summary.md",
    ]
    missing = [f.name for f in required if not f.is_file()]
    if missing:
        print(f"CHECK 1 File Existence: FAIL — missing: {', '.join(missing)}")
        return False
    print("CHECK 1 File Existence: PASS")
    return True


def check_row_count(cycle_dir: Path) -> bool:
    """CHECK 2: Row count > 0 and Period column exists with valid values."""
    csv_path = cycle_dir / "Data" / "SCRPA_All_Crimes_Enhanced.csv"
    df = pd.read_csv(csv_path, low_memory=False)
    total = len(df)
    if total == 0:
        print("CHECK 2 Row Count: FAIL — 0 rows")
        return False
    if "Period" not in df.columns:
        print(f"CHECK 2 Row Count: FAIL — {total} rows but Period column missing")
        return False
    seven_day_count = int((df["Period"] == "7-Day").sum())
    note = f", {seven_day_count} in 7-Day period"
    if seven_day_count == 0:
        note += " (expected if run early in cycle)"
    print(f"CHECK 2 Row Count: PASS — {total} rows{note}")
    return True


def check_lag_backfill(cycle_dir: Path) -> bool:
    """CHECK 3: JSON lag_incidents and backfill_7day match CSV counts."""
    csv_path = cycle_dir / "Data" / "SCRPA_All_Crimes_Enhanced.csv"
    json_path = cycle_dir / "Data" / "SCRPA_7Day_Summary.json"

    df = pd.read_csv(csv_path, low_memory=False)
    with open(json_path, encoding="utf-8") as f:
        summary = json.load(f)

    j_lag = summary["counts"]["lag_incidents"]
    j_bf = summary["counts"]["backfill_7day"]

    # lag_incidents = rows where Period=='7-Day' AND IncidentToReportDays > 0
    if "Period" in df.columns and "IncidentToReportDays" in df.columns:
        csv_lag = int(((df["Period"] == "7-Day") & (df["IncidentToReportDays"] > 0)).sum())
    else:
        csv_lag = 0

    # backfill_7day = rows where Backfill_7Day == True
    csv_bf = int((df["Backfill_7Day"] == True).sum()) if "Backfill_7Day" in df.columns else 0

    issues = []
    if j_lag != csv_lag:
        issues.append(f"lag_incidents JSON={j_lag} vs CSV={csv_lag}")
    if j_bf != csv_bf:
        issues.append(f"backfill_7day JSON={j_bf} vs CSV={csv_bf}")

    if issues:
        print(f"CHECK 3 Lag/Backfill: FAIL — {'; '.join(issues)}")
        return False
    print(f"CHECK 3 Lag/Backfill: PASS — lag={j_lag}, backfill={j_bf}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_cycle_quick.py <cycle_folder_path>")
        sys.exit(1)

    cycle_dir = Path(sys.argv[1])
    if not cycle_dir.is_dir():
        print(f"ERROR: Folder not found: {cycle_dir}")
        sys.exit(1)

    results = []

    # CHECK 1
    results.append(check_file_existence(cycle_dir))

    # Only run data checks if files exist
    if results[0]:
        results.append(check_row_count(cycle_dir))
        results.append(check_lag_backfill(cycle_dir))
    else:
        print("CHECK 2 Row Count: SKIP — missing files")
        print("CHECK 3 Lag/Backfill: SKIP — missing files")
        results.extend([False, False])

    passed = sum(results)
    print(f"\nQuick validation: {passed}/3 checks passed.")
    sys.exit(0 if passed == 3 else 1)


if __name__ == "__main__":
    main()
