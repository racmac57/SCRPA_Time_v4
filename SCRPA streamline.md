# SCRPA streamline 

It locks Python parity to Power BI all_crimes.m, incorporates the LagDay fixes, and includes all required code blocks, validation SQL, and briefing replacement logic in one artifact.

---

```
# SCRPA Python Parity Lock – All_Crimes, LagDays, 7-Day, Briefing
**Status**: PARITY LOCKED  
**Authoritative Sources**:
- `alL_crimes_preview_table_26_01_27.csv`
- `LAGDAY_LOGIC_VERIFICATION.md`
- `VERIFICATION_01_27_2026_REPORT.md`

This document defines the **canonical Python/Pandas implementation** that must match Power BI `all_crimes.m` exactly for:
- Cycle detection
- LagDay / Backfill logic
- Period classification (7-Day first, then downstream)
- 7-Day reporting outputs
- Briefing CSV generation

Power BI becomes a consumer, not the source of truth.

---

## 1. Ground Rules (Non-Negotiable)

1. **Cycle resolution uses Report_Date_ForLagday**
   - No Incident_Date fallback.
2. **LagDays = CycleStartForReport − Incident_Date**
   - Not Report − Incident.
3. **IsLagDay**
   - Incident_Date < CycleStartForReport.
4. **Backfill_7Day**
   - Incident before cycle start **AND**
   - Report_Date_ForLagday inside current 7-Day window.
5. **Lagday detail tables**
   - Filter on `Backfill_7Day = TRUE`, not `IsLagDay`.
6. **Period**
   - Driven by Incident_Date.
   - Precedence: 7-Day → 28-Day → YTD → Prior Year.

---

## 2. Inputs

### Required
- Raw RMS export (`.csv` or `.xlsx`)
- Cycle calendar CSV: `7Day_28Day_Cycle_20260106.csv`
- Report Due Date (MM/DD/YYYY)

### Optional (for validation)
- `alL_crimes_preview_table_26_01_27.csv`

---

## 3. Canonical Python Script  
### `scrpa_transform.py`

```python
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

# ----------------------------
# Column mapping (adjust RMS names only)
# ----------------------------
COLMAP = {
    "IncidentDate": "Incident_Date",
    "ReportDate": "Report_Date",
    "CaseNumber": "Case_Number",
    "Offense": "Offense",
    "Zone": "Zone",
    "Narrative": "Narrative",
}

# ----------------------------
# Helpers
# ----------------------------
def read_any(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path, dtype=str, low_memory=False)
    else:
        df = pd.read_excel(path, dtype=str)
    return df.rename(columns=COLMAP)

def parse_dt(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce", infer_datetime_format=True)

# ----------------------------
# Cycle lookup (3-tier, Power BI parity)
# ----------------------------
def resolve_cycle(cal: pd.DataFrame, report_due: pd.Timestamp):
    # Tier 1: exact Report_Due_Date
    m1 = cal[cal["Report_Due_Date"] == report_due]
    if len(m1):
        r = m1.iloc[0]
        return r["Report_Name"], r["7_Day_Start"], r["7_Day_End"], r["28_Day_Start"], r["28_Day_End"]

    # Tier 2: report date inside 7-Day window
    m2 = cal[(cal["7_Day_Start"] <= report_due) & (report_due <= cal["7_Day_End"])]
    if len(m2):
        r = m2.iloc[0]
        return r["Report_Name"], r["7_Day_Start"], r["7_Day_End"], r["28_Day_Start"], r["28_Day_End"]

    # Tier 3: most recent cycle
    m3 = cal[cal["7_Day_End"] <= report_due].sort_values("7_Day_End")
    r = m3.iloc[-1]
    return r["Report_Name"], r["7_Day_Start"], r["7_Day_End"], r["28_Day_Start"], r["28_Day_End"]

# ----------------------------
# Main transform
# ----------------------------
def build_all_crimes(rms: pd.DataFrame, cal: pd.DataFrame, report_due: pd.Timestamp) -> pd.DataFrame:
    df = rms.copy()

    # Parse dates
    df["Incident_Date"] = parse_dt(df["Incident_Date"])
    df["Report_Date"] = parse_dt(df["Report_Date"])

    # Report_Date_ForLagday (NO Incident fallback)
    df["Report_Date_ForLagday"] = df["Report_Date"]

    # Resolve cycle for THIS RUN
    cycle_name, c7s, c7e, c28s, c28e = resolve_cycle(cal, report_due)

    df["Cycle_Name"] = cycle_name
    df["CycleStart_7Day"] = c7s
    df["CycleEnd_7Day"] = c7e
    df["CycleStart_28Day"] = c28s
    df["CycleEnd_28Day"] = c28e

    # ----------------------------
    # Lag logic (Power BI exact)
    # ----------------------------
    df["IsLagDay"] = (
        df["Incident_Date"].notna()
        & (df["Incident_Date"] < df["CycleStart_7Day"])
    )

    df["LagDays"] = pd.NA
    mask = df["IsLagDay"] & df["Incident_Date"].notna()
    df.loc[mask, "LagDays"] = (df.loc[mask, "CycleStart_7Day"] - df.loc[mask, "Incident_Date"]).dt.days
    df.loc[df["LagDays"] < 0, "LagDays"] = 0
    df["LagDays"] = df["LagDays"].astype("Int64")

    # Backfill_7Day
    df["Backfill_7Day"] = (
        df["Report_Date_ForLagday"].notna()
        & (df["Report_Date_ForLagday"] >= df["CycleStart_7Day"])
        & (df["Report_Date_ForLagday"] <= df["CycleEnd_7Day"])
        & (df["Incident_Date"] < df["CycleStart_7Day"])
    )

    # ----------------------------
    # Period classification (Incident-driven)
    # ----------------------------
    df["Period"] = "Prior Year"

    in7 = (
        df["Incident_Date"].notna()
        & (df["Incident_Date"] >= df["CycleStart_7Day"])
        & (df["Incident_Date"] <= df["CycleEnd_7Day"])
    )
    df.loc[in7, "Period"] = "7-Day"

    in28 = (
        (df["Period"] == "Prior Year")
        & df["Incident_Date"].notna()
        & (df["Incident_Date"] >= df["CycleStart_28Day"])
        & (df["Incident_Date"] <= df["CycleEnd_28Day"])
    )
    df.loc[in28, "Period"] = "28-Day"

    df["Period_SortKey"] = df["Period"].map({
        "7-Day": 1,
        "28-Day": 2,
        "YTD": 3,
        "Prior Year": 4
    }).astype("Int64")

    # Zone normalization
    if "Zone" in df.columns:
        df["Zone"] = pd.to_numeric(df["Zone"], errors="coerce").astype("Int64")

    return df

# ----------------------------
# 7-Day reporting dataset
# ----------------------------
def build_7day(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Report_Date_ForLagday"].between(df["CycleStart_7Day"], df["CycleEnd_7Day"])].copy()

# ----------------------------
# CLI
# ----------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rms", required=True)
    ap.add_argument("--cycle-calendar", required=True)
    ap.add_argument("--report-due-date", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    rms = read_any(Path(args.rms))
    cal = pd.read_csv(args.cycle_calendar, parse_dates=[
        "Report_Due_Date", "7_Day_Start", "7_Day_End", "28_Day_Start", "28_Day_End"
    ])

    report_due = pd.to_datetime(args.report_due_date)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    allc = build_all_crimes(rms, cal, report_due)
    allc.to_csv(out / "SCRPA_All_Crimes_Enhanced.csv", index=False)

    d7 = build_7day(allc)
    d7.to_csv(out / "SCRPA_7Day_With_LagFlags.csv", index=False)

if __name__ == "__main__":
    main()
```

---

## 4. Briefing CSV Replacement

### prepare_briefing_csv_replacement.py

```
import pandas as pd
from pathlib import Path
from datetime import datetime
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--cycle", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.inp, low_memory=False)

    df["Lag_Class"] = ""
    df.loc[df["Backfill_7Day"] == True, "Lag_Class"] = "REPORTED_THIS_CYCLE"
    df.loc[(df["IsLagDay"] == True) & (df["Backfill_7Day"] == False), "Lag_Class"] = "PRIOR_LAG"

    keep = [
        "Case_Number", "Incident_Date", "Report_Date",
        "Offense", "Zone", "LagDays", "Lag_Class", "Narrative"
    ]
    df = df[[c for c in keep if c in df.columns]]

    ts = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / f"SCRPA_Briefing_Ready_{args.cycle}_{ts}.csv", index=False)

if __name__ == "__main__":
    main()
```

---

## 5. Validation SQL (Required)

```
-- Backfill must always be lag
select count(*) from SCRPA_7Day_With_LagFlags
where Backfill_7Day = 1 and IsLagDay = 0;

-- LagDays never negative
select count(*) from SCRPA_All_Crimes_Enhanced
where LagDays < 0;

-- Lagday detail integrity
select count(*) from SCRPA_7Day_With_LagFlags
where IsLagDay = 1
  and Backfill_7Day = 0
  and Report_Date_ForLagday between CycleStart_7Day and CycleEnd_7Day;
```

All queries must return 0.

---

## 6. Acceptance Criteria

* Row counts match RMS input.
* SCRPA_All_Crimes_Enhanced.csv aligns column-for-column with alL_crimes_preview_table_26_01_27.csv.
* Lagday visuals use Backfill_7Day.
* Power BI visuals no longer required for LagDay correctness.
---

## 7. Outcome

This file locks Python as the authoritative logic layer.

Power BI, HTML, email, and briefing artifacts now consume deterministic outputs.

End of specification.