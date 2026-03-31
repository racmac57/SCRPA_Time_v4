# SCRPA Script Verification for Report Date 01/27/2026

**Report Date**: 01/27/2026  
**Bi-Weekly Cycle**: 26BW02  
**First bi-weekly report after transition**

---

## ✅ Cycle Calendar Verification

**File**: `09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv`

| Field | Value |
|-------|--------|
| **Report_Due_Date** | 01/27/2026 |
| **Report_Name** | 26C01W04 |
| **BiWeekly_Report_Name** | 26BW02 |
| **7-Day Start** | 01/20/2026 |
| **7-Day End** | 01/26/2026 |
| **28-Day Start** | 12/30/2025 |
| **28-Day End** | 01/26/2026 |

Lookup by `Report_Due_Date = 01/27/2026` returns this row. No gaps; v1.9.1 fix ensured 01/06/2026 entry exists.

---

## ✅ Script-by-Script Verification

### 1. `Run_SCRPA_Report_Folder.bat`

- Prompts for report date (default today); you will enter **01/27/2026**.
- Normalizes to `MM/DD/YYYY` and 4-digit year.
- Sets `REPORT_DATE` in environment before Step 0.5 and passes it to all child processes.
- **Verdict**: ✅ Ready for 01/27/2026.

### 2. Step 0.5 – Excel → CSV (`convert_all_xlsx_auto.bat`)

- Uses `export_excel_sheets_to_csv.py` with `--report-last7` and `--engine calamine`.
- Inherits `REPORT_DATE` from parent batch.
- **Verdict**: ✅ 7-day filtered CSV will use cycle 01/20–01/26.

### 3. `export_excel_sheets_to_csv.py`

- **Cycle calendar**: `7Day_28Day_Cycle_20260106.csv` ✅
- **Lookup**: `REPORT_DATE` from env → exact match on `Report_Due_Date` (01/27/2026) → 7-Day **01/20–01/26**.
- `_write_last7_by_reportdate_csv` filters rows by `Report Date` in that range.
- **Verdict**: ✅ Correct 7-day window for 01/27/2026.

### 4. Step 1 – `generate_weekly_report.py`

- **Cycle calendar**: `7Day_28Day_Cycle_20260106.csv` ✅
- **Input**: Report date from batch as `argv[1]` (01/27/2026).
- **Lookup**: `Report_Due_Date == 01/27/2026` → `Report_Name` **26C01W04**, 7-Day 01/20–01/26.
- **Output**: Folder `26C01W04_26_01_27`, template copied as `26C01W04_26_01_27.pbix`.
- **Verdict**: ✅ Folder and .pbix naming correct.

### 5. Step 2 – `generate_all_reports.bat`

- Receives `REPORT_DATE` from parent; uses it for stats and briefing steps.
- Step 0 (Excel convert) is skipped when no .xlsx (already converted/archived in Step 0.5).
- **Verdict**: ✅ Uses 01/27/2026 where needed.

### 6. `prepare_briefing_csv.py`

- **Cycle calendar**: Prefers `7Day_28Day_Cycle_20260106.csv` ✅
- **REPORT_DATE**: From environment; parsed as `01/27/2026` → `get_cycle_info_from_calendar` → **26C01W04**, 7-Day 01/20–01/26.
- **Verdict**: ✅ Briefing CSV and ChatGPT prompt will have correct cycle and dates.

### 7. Step 3 – `organize_report_files.py`

- Finds latest report folder by mtime (the one created in Step 1).
- Extracts date from folder `26C01W04_26_01_27` → `(2026, 1, 27)` for file filtering.
- No cycle calendar dependency.
- **Verdict**: ✅ Targets correct folder and date.

### 8. Step 4 – `export_enriched_data_and_email.py`

- **Cycle calendar**: `7Day_28Day_Cycle_20260106.csv` ✅
- Finds latest report folder → `26C01W04_26_01_27` → cycle **26C01W04**.
- Lookup by `Report_Name` → 7-Day **01/20–01/26**.
- Email template: **"SCRPA Bi-Weekly Report - Cycle 26C01W04 | 01/20/2026 - 01/26/2026"**.
- **Verdict**: ✅ Email template correct for 01/27/2026.

### 9. Power BI M Code

- **`q_CycleCalendar.m`**: Loads `7Day_28Day_Cycle_20260106.csv`, includes `BiWeekly_Report_Name` ✅
- **`Export_Formatting.m`**: Validates both weekly (`26C01W04`) and bi-weekly (`26BW02`) ✅
- **`all_crimes.m`**: Uses `Report_Name`, `7_Day_Start`, `7_Day_End`; LagDays three-tier logic uses Report_Due_Date / cycle range / most recent cycle. For 01/27/2026, Report_Due_Date match applies.
- **Verdict**: ✅ M code aligned with calendar and 01/27/2026.

---

## Pre-Run Checklist for 01/27/2026

- [ ] Latest RMS Excel export in `05_EXPORTS\_RMS\scrpa\`.
- [ ] Run `02_ETL_Scripts\Run_SCRPA_Report_Folder.bat`.
- [ ] Enter **01/27/2026** when prompted (or accept if default).
- [ ] After workflow: open `Time_Based\2026\26C01W04_26_01_27\`.
- [ ] In Power BI: point data source to correct Excel/CSV, refresh, export All_Crime preview if using email script.
- [ ] Optionally re-run `scripts\export_enriched_data_and_email.py` after All_Crime export to refresh email template.

---

## Troubleshooting: Report Folder Empty (No Data/Reports/Documentation)

If the report folder `26C01W04_26_01_27` is created but **no files** appear in `Data/`, `Reports/`, or `Documentation/`:

### 1. Check the run log

Step 2 (`generate_all_reports`) output is redirected to the log. Inspect:

- **Path**: `02_ETL_Scripts\SCRPA\logs\SCRPA_run_YYYY-MM-DD_HH-MM.log`
- **Look for**:  
  - `[ERROR]` / `[WARNING]` from stats, briefing, or organize  
  - `No Excel or CSV files found` (stats)  
  - `No 7-day CSV files found` (briefing)  
  - `No CSV files found matching date` (organize)

### 2. Excel export date vs report date

- Organize filters CSVs by **report date** (01/27/2026 → `2026_01_27` or `26_01_27` in filenames).
- The Excel (and thus CSV) filename uses the **export** timestamp. Use an export from **01/27/2026** when running the 01/27 report.

### 3. Archive fallback (as of this update)

- `organize_report_files` and `prepare_briefing_csv` now check the **archive** folder when the exports root has no matching CSVs (e.g. Excel archived after convert).
- If you previously ran the workflow and CSVs were archived, re-run the batch; organize/briefing will use archive.

### 5. CSV-only re-run: do not archive CSVs

- When there is **no Excel** in the exports folder (e.g. re-run after copying CSVs back from archive), the export script’s archive-only step **no longer archives CSV files**. Only Excel files are archived in that case, so stats/briefing/organize can use the CSVs in root.
- Updated in both `02_ETL_Scripts\SCRPA\scripts\export_excel_sheets_to_csv.py` and `05_EXPORTS\_RMS\scrpa\export_excel_sheets_to_csv.py`.

### 4. Re-run only the organize step (optional)

If Step 2 already produced files in `06_Output` and in the exports folder (or archive), you can re-run only the organize step:

1. `cd` to `02_ETL_Scripts\SCRPA`
2. Set `REPORT_DATE=01/27/2026`
3. Run: `py -3 organize_report_files.py`

### 5. CSV-only re-run: do not archive CSVs

- When there is **no Excel** in the exports folder (e.g. re-run after copying CSVs back from archive), the export script's archive-only step **no longer archives CSV files**. Only Excel files are archived in that case, so stats/briefing/organize can use the CSVs in root.
- Updated in both `02_ETL_Scripts\SCRPA\scripts\export_excel_sheets_to_csv.py` and `05_EXPORTS\_RMS\scrpa\export_excel_sheets_to_csv.py`.

### 6. Export File Watchdog and SCRPA

- The **Export File Watchdog** moves files named `SCRPA_RMS_Export*` from **Desktop** (and optionally Downloads) to `05_EXPORTS\_RMS\scrpa\`.
- On move, it **renames** the file to `YYYY_MM_DD_HH_MM_SS_SCRPA_RMS.xlsx` (timestamp at move time). The SCRPA workflow expects timestamped filenames, so this is **compatible**.
- The watchdog **does not** watch the scrpa folder. It only monitors Desktop and Downloads. So it will not move, rename, or delete files (Excel, CSVs) that are already in scrpa.
- **Recommended**: Export RMS data → rename to `SCRPA_RMS_Export.xlsx` → place on **Desktop** → let the watchdog move it to scrpa. Then run `Run_SCRPA_Report_Folder.bat`. The watchdog is **not** responsible for the “report folder empty” issues; those were due to archive logic and have been fixed.

---

## Post-run verification (01/27/2026)

After running the workflow for **01/27/2026**, the following was verified and corrected:

### Folder contents

| Location | Status |
|----------|--------|
| **Root** | `26C01W04_26_01_27.pbix` — added (was missing; template copied from `08_Templates\Base_Report.pbix`). |
| **Data/** | ✅ `SCRPA_7Day_Detailed.csv`, `SCRPA_7Day_Summary.csv`, `*_ReportDate_Last7` & full RMS CSVs, `SCRPA_Briefing_Ready_*`, `README_7day_outputs.md`. |
| **Reports/** | ✅ `2026_01_27_14_06_37_rms_summary.html`, `SCRPA_Combined_Executive_Summary_20260127_*.html`. Removed `2025_12_09_*_rms_summary.pdf` and `2026_01_12_*_rms_summary.html` (wrong cycles). |
| **Documentation/** | ✅ `CHATGPT_BRIEFING_PROMPT.md`, `SCRPA_Report_Summary.md`. |

### Prompt and cycle

- **`CHATGPT_BRIEFING_PROMPT.md`**: Contains full CSV data (5 cases), **Cycle 26C01W04**, **Date range 01/20/2026 – 01/26/2026**. Reporting Parameters match. ✅ **Correct** for the **7-day** window.
- **7-day vs bi-weekly**: The **7-day** window for this report is **01/20–01/26**. The **bi-weekly** 26BW02 spans **01/13–01/26** (two 7-day cycles). The briefing prompt and 7-day data use **01/20–01/26** only. If you need the full bi-weekly range (1/13–1/26) in the prompt, that would require including both weeks’ data and updating the prompt; the current setup is correct for 7-day briefing.

### Step 4 (email template)

- Step 4 failed with **All_Crime preview CSV not found**. This is expected until you **export the All_Crime preview table from Power BI** into the report folder. Open the report `.pbix`, refresh, export the preview, then run `scripts\export_enriched_data_and_email.py` (or re-run the full batch) to generate the email template.

### LagDays fix (2026-01-27)

- **Issue**: LagDays could show **0** when it should be &gt; 0 (e.g. incident 01/09, report 01/16 → expected 4). Cause: `Report_Date` fell back to **Incident_Date** when Report Date was null; lagday logic used that, so the “report” cycle was the incident’s cycle and many delayed reports were misclassified.
- **Fix**: Added **`Report_Date_ForLagday`** (Report Date or EntryDate only, no Incident_Date fallback). **IsLagDay**, **LagDays**, **Backfill_7Day**, and **IsCurrent7DayCycle** now use it. See `LAGDAY_LOGIC_VERIFICATION.md` addendum.
- **Action**: Update Power BI to use the revised `all_crimes.m`, refresh, then re-export the All_Crime preview.

### Lagday table filter (Motor Vehicle Theft / “Recently Reported”)

- **Issue**: Case **26-005319** (incident 01/09/26, report 01/16/26) appears in the Motor Vehicle Theft lagday table but **should not**. The incident happened before the cycle (01/20–01/26); the report date 01/16 is **before** the cycle, so it was not “recently reported” **this** cycle.
- **Fix**: Lagday **detail** tables (e.g. “Recently Reported”) must filter on **`Backfill_7Day = TRUE`**, not just **`IsLagDay = TRUE`**. `Backfill_7Day` = incident before cycle start **and** report date **in** the current 7‑day window. See **“Lagday Table Filter”** addendum in `LAGDAY_LOGIC_VERIFICATION.md`.
- **Action**: In Power BI, add a **Visual-level filter** on the lagday table(s): **`Backfill_7Day`** = **True**. Keep `Crime_Category` (e.g. Motor Vehicle Theft) as needed.

### Duplicate exports in Data

- **Why multiple copies?** Each workflow run can add new files: **Step 0.5** produces timestamped CSVs (e.g. `*_13_29_35_*`); **briefing** produces `SCRPA_Briefing_Ready_*` with its own timestamp; **organize** copies all matching exports into `Data/`. Re-runs add more timestamped files (e.g. `SCRPA_Briefing_Ready_2026_01_27_13_34_07` and `_14_06_36` from two runs).
- **What to do**: Keep the **latest** of each type (e.g. most recent Briefing_Ready, most recent 7-day CSVs). You can delete older timestamped duplicates if you want a single set; the workflow does not auto-cull them.

---

## Expected Outcomes

| Item | Expected |
|------|----------|
| **Report folder** | `Time_Based\2026\26C01W04_26_01_27\` |
| **7-Day range** | 01/20/2026 – 01/26/2026 |
| **Cycle IDs** | 26C01W04 (folder / Report_Name), 26BW02 (bi-weekly) |
| **\*_ReportDate_Last7.csv** | Rows with Report Date in 01/20–01/26 |
| **Email subject** | `SCRPA Bi-Weekly Report - Cycle 26C01W04 \| 01/20/2026 - 01/26/2026` |

---

## Summary

All scripts are configured for the 2026 bi-weekly cycle calendar and correctly handle **01/27/2026**:

- Cycle calendar has 01/27/2026 → 26BW02 / 26C01W04, 7-Day 01/20–01/26.
- Batch sets and passes `REPORT_DATE`.
- Excel conversion, folder creation, briefing, organization, and email template use the same calendar and dates.
- Power BI M code matches the calendar and validation rules.

**You can run the full workflow for 01/27/2026 as your first bi-weekly report.**

---

*Generated: 2026-01-27 | SCRPA v1.9.1*
