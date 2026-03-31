"""
Quick validation: SCRPA_7Day_Summary.json vs SCRPA_All_Crimes_Enhanced.csv
Run from repo root: python scripts/validate_7day_json.py Time_Based/2026/26C02W06_26_02_10/Data
"""
import json
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_7day_json.py <data_dir>")
        sys.exit(1)
    data_dir = Path(sys.argv[1])
    json_path = data_dir / "SCRPA_7Day_Summary.json"
    csv_path = data_dir / "SCRPA_All_Crimes_Enhanced.csv"
    if not json_path.exists():
        print(f"Missing: {json_path}")
        sys.exit(1)
    if not csv_path.exists():
        print(f"Missing: {csv_path}")
        sys.exit(1)

    import pandas as pd
    with open(json_path, "r", encoding="utf-8") as f:
        js = json.load(f)
    df = pd.read_csv(csv_path, low_memory=False)

    # Checks from JSON_VALIDATION_FINDINGS
    period_7day = df[df["Period"] == "7-Day"] if "Period" in df.columns else pd.DataFrame()
    lag_in_period = period_7day[period_7day["IncidentToReportDays"] > 0] if "IncidentToReportDays" in period_7day.columns else pd.DataFrame()

    ok = True
    if js["counts"]["total_all_crimes"] != len(df):
        print(f"FAIL total_all_crimes: json={js['counts']['total_all_crimes']} csv={len(df)}")
        ok = False
    if js["counts"]["incidents_in_7day_period"] != len(period_7day):
        print(f"FAIL incidents_in_7day_period: json={js['counts']['incidents_in_7day_period']} csv={len(period_7day)}")
        ok = False
    if js["counts"]["lag_incidents"] != len(lag_in_period):
        print(f"FAIL lag_incidents: json={js['counts']['lag_incidents']} csv={len(lag_in_period)}")
        ok = False
    json_cats = set(js["lag_analysis"]["by_crime_category"].keys())
    csv_cats = set(lag_in_period["Crime_Category"].unique()) if len(lag_in_period) > 0 else set()
    if json_cats != csv_cats:
        print(f"FAIL lag_analysis.by_crime_category: json={json_cats} csv={csv_cats}")
        ok = False

    if ok:
        print("OK All checks passed (total_all_crimes, incidents_in_7day_period, lag_incidents, lag_by_category).")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
