#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRPA Crime-Type Breakdown and LagDay Report

Reads SCRPA_7Day_Detailed.csv (or latest 7-day export), breaks down counts by:
  - Burglary - Auto - 2C:18-2
  - Motor Vehicle Theft - 2C:20-3
  - Burglary - Commercial - 2C:18-2
  - Burglary - Residence - 2C:18-2
  - Sexual Offenses
  - Robbery - 2C:15-1

Adds LagDays to each incident (reported within 7-day cycle; incident before cycle = lagday).
Outputs markdown report and optional CSV with LagDays column.
"""

from pathlib import Path
import pandas as pd
from datetime import datetime

BASE = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA")
TIME_BASED = BASE / "Time_Based"

# Map Incident Type_1 (or Crime_Category) to report category
CATEGORIES = [
    "Burglary - Auto - 2C:18-2",
    "Motor Vehicle Theft - 2C:20-3",
    "Burglary - Commercial - 2C:18-2",
    "Burglary - Residence - 2C:18-2",
    "Sexual Offenses",
    "Robbery - 2C:15-1",
]

def _categorize_better(row: pd.Series) -> str | None:
    """Map row to exactly one of CATEGORIES. Prefer Incident Type_1."""
    it1 = str(row.get("Incident Type_1", "") or "")
    cc = str(row.get("Crime_Category", "") or "")
    it1_upper = it1.upper()
    cc_upper = cc.upper()
    # Order matters: check more specific first
    if "MOTOR VEHICLE THEFT" in it1_upper:
        return "Motor Vehicle Theft - 2C:20-3"
    if "ROBBERY" in it1_upper:
        return "Robbery - 2C:15-1"
    if "BURGLARY - COMMERCIAL" in it1_upper:
        return "Burglary - Commercial - 2C:18-2"
    if "BURGLARY - RESIDENCE" in it1_upper:
        return "Burglary - Residence - 2C:18-2"
    if "BURGLARY - AUTO" in it1_upper:
        return "Burglary - Auto - 2C:18-2"
    if "SEXUAL" in it1_upper or "CRIMINAL SEXUAL CONTACT" in it1_upper or "FONDLING" in cc_upper or cc == "Sexual Offenses":
        return "Sexual Offenses"
    return None

def find_latest_7day_detailed() -> Path:
    year_folders = [d for d in TIME_BASED.iterdir() if d.is_dir() and d.name.isdigit()]
    all_data = []
    for yf in year_folders:
        for rf in yf.iterdir():
            if not rf.is_dir():
                continue
            p = rf / "Data" / "SCRPA_7Day_Detailed.csv"
            if p.exists():
                all_data.append((p, p.stat().st_mtime))
    if not all_data:
        raise FileNotFoundError("No SCRPA_7Day_Detailed.csv found under Time_Based")
    return max(all_data, key=lambda x: x[1])[0]

def run(
    csv_path: Path | None = None,
    out_md: Path | None = None,
    out_csv: Path | None = None,
) -> None:
    path = csv_path or find_latest_7day_detailed()
    df = pd.read_csv(path)
    df["_Category"] = df.apply(_categorize_better, axis=1)
    df["LagDays"] = df.get("LagDays", pd.Series(0, index=df.index)).fillna(0).astype(int)
    df["IsLagDay"] = df.get("IsLagDay", pd.Series(False, index=df.index)).fillna(False)

    cycle_start = df["CycleStartDate"].iloc[0] if "CycleStartDate" in df.columns and len(df) else ""
    cycle_end = df["CycleEndDate"].iloc[0] if "CycleEndDate" in df.columns and len(df) else ""

    # Summary by category
    rows = []
    for cat in CATEGORIES:
        sub = df[df["_Category"] == cat]
        n = len(sub)
        lag = int(sub["IsLagDay"].sum())
        rows.append({"Category": cat, "Total": n, "LagDayCount": lag})

    summary = pd.DataFrame(rows)

    # Build markdown
    lines = [
        "# SCRPA Crime-Type Breakdown and LagDays",
        "",
        f"**Source:** `{path.name}`  ",
        f"**Cycle:** {cycle_start} – {cycle_end}  ",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## Summary by Category",
        "",
        "| Category | Total | LagDay Count |",
        "|----------|-------|--------------|",
    ]
    for _, r in summary.iterrows():
        lines.append(f"| {r['Category']} | {r['Total']} | {r['LagDayCount']} |")
    total_n = int(summary["Total"].sum())
    total_lag = int(summary["LagDayCount"].sum())
    lines.append(f"| **TOTAL** | **{total_n}** | **{total_lag}** |")
    lines.append("")
    lines.append("**LagDay** = incident reported within the 7-day cycle, but **incident date** is **before** the 7-day cycle start.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Incidents with LagDays (reported this cycle, incident before cycle)")
    lines.append("")

    laggers = df[df["IsLagDay"] == True].copy()
    if len(laggers) == 0:
        lines.append("*None.*")
    else:
        lines.append("| Case Number | Incident Date | Report Date | Category | LagDays |")
        lines.append("|-------------|---------------|-------------|----------|--------|")
        for _, r in laggers.iterrows():
            cat = r["_Category"] or "—"
            lines.append(f"| {r['Case Number']} | {r['Incident Date']} | {r['Report Date']} | {cat} | {r['LagDays']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## All Incidents (with LagDays)")
    lines.append("")
    lines.append("| Case Number | Incident Date | Report Date | Category | LagDays |")
    lines.append("|-------------|---------------|-------------|----------|--------|")
    for _, r in df.iterrows():
        cat = r["_Category"] or "—"
        lines.append(f"| {r['Case Number']} | {r['Incident Date']} | {r['Report Date']} | {cat} | {r['LagDays']} |")
    lines.append("")

    md_text = "\n".join(lines)

    # Write MD
    if out_md is None:
        out_md = path.parent / "CRIME_BREAKDOWN_AND_LAGDAYS.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md_text, encoding="utf-8")
    print(f"Wrote: {out_md}")

    out_df = df.copy()
    out_df["Report_Category"] = out_df["_Category"]
    out_df = out_df.drop(columns=["_Category"], errors="ignore")

    # CSV with LagDays to same folder as MD
    csv_out = out_md.parent / "CRIME_BREAKDOWN_WITH_LAGDAYS.csv"
    out_df.to_csv(csv_out, index=False)
    print(f"Wrote: {csv_out}")

    # Copy MD to Documentation if it exists
    docs = path.parent.parent / "Documentation"
    if docs.is_dir():
        md_docs = docs / "CRIME_BREAKDOWN_AND_LAGDAYS.md"
        md_docs.write_text(md_text, encoding="utf-8")
        print(f"Wrote: {md_docs}")

    if out_csv is not None and out_csv != csv_out:
        out_df.to_csv(out_csv, index=False)
        print(f"Wrote: {out_csv}")

    return None

if __name__ == "__main__":
    run()
