**Open your project in Claude Code (or Cursor) at this workspace root:**

```
C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA
```

Alternatively, you can use the ETL scripts root:

```
C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts
```

Use the **SCRPA** workspace root if you want to focus on report outputs and verification docs; use **02_ETL_Scripts** if you want to focus on the automation scripts themselves. Both contain overlapping context.

---

## Full Paths Reference

| Purpose | Full Path |
|--------|-----------|
| **Main workflow batch** | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Run_SCRPA_Report_Folder.bat` |
| **Report folder (this run)** | `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W04_26_01_27` |
| **RMS exports (CSV/Excel)** | `C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa` |
| **Exports archive** | `C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa\archive` |
| **Stats + briefing output** | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\06_Output` |
| **Run log (check most recent)** | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\logs\SCRPA_run_YYYY-MM-DD_HH-MM.log` |
| **Generate-all-reports batch** | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\generate_all_reports.bat` |
| **Organize script** | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\organize_report_files.py` |
| **Stats script** | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator\RMS_Statistical_Export_FINAL_COMPLETE.py` |
| **Briefing script** | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\prepare_briefing_csv.py` |
| **Excel→CSV script** | `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\export_excel_sheets_to_csv.py` |
| **Verification doc** | `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\VERIFICATION_01_27_2026_REPORT.md` |

---

## What To Do

1. **Diagnose** why `26C01W04_26_01_27` is created but **Data**, **Reports**, and **Documentation** stay empty (or nearly empty) after running `Run_SCRPA_Report_Folder.bat` with report date **01/27/2026**.
2. **Fix** the root cause(s).
3. **Improve** the workflow so this doesn’t recur (e.g. clearer logging, path handling, or error handling).

---

## Workflow Summary

1. **Step 0.5** – Excel → CSV in `05_EXPORTS\_RMS\scrpa`. Uses `convert_all_xlsx_auto.bat` and `export_excel_sheets_to_csv.py`. Produces `*_SCRPA_RMS.csv` and `*_ReportDate_Last7.csv`.
2. **Step 1** – `generate_weekly_report.py` creates `Time_Based\2026\26C01W04_26_01_27`, subfolders **Data**, **Reports**, **Documentation**, and copies the Power BI template.
3. **Step 2** – `generate_all_reports.bat` runs (stats → briefing → HTML → PDF). **All of its output is redirected to the main run log.** It uses `REPORT_DATE` from the environment (set by the parent batch).
4. **Step 3** – `organize_report_files.py` copies CSVs, HTML, PDFs, etc. from exports and `06_Output` **into** the latest report folder (by mtime). This is what **populates** Data, Reports, Documentation.
5. **Step 4** – Email template generation (optional).

If Step 2 fails or produces no outputs, or Step 3 can’t find/copy files, the report folder remains empty.

---

## Known Gotchas

### 1. “REPORT_DATE format check” log line

The main batch logs **`REPORT_DATE format check: 01/27/2026 (should be MM/DD/YYYY)`** immediately before calling `generate_all_reports.bat`. The user consistently sees this line when the report folder ends up empty. **That line is only a log message**—it is not an error. The real failures are in Step 2 or Step 3. The phrase “format check” is misleading; consider renaming or removing it once you’ve improved logging.

### 2. Step 2 output hidden in the log

`generate_all_reports.bat` is invoked with `>>"%LOG%" 2>&1`. All stdout/stderr from that batch (including stats and briefing Python scripts) goes **only** to the log file. To see what failed, **inspect the run log** (path above) for `[ERROR]`, `[WARNING]`, “No Excel or CSV”, “No 7-day CSV”, “No CSV files found matching date”, or Python tracebacks.

### 3. RMS export path case: `SCRPA` vs `scrpa`

- **Actual folder:** `05_EXPORTS\_RMS\scrpa` (lowercase).
- **`generate_all_reports.bat`** uses `RMS_EXPORT_DIR = ...\05_EXPORTS\_RMS\SCRPA` (uppercase). It `cd`s there and runs briefing from that directory.
- **`RMS_Statistical_Export_FINAL_COMPLETE.py`** hardcodes `05_EXPORTS\_RMS\scrpa` (lowercase).
- **`organize_report_files.py`** checks both and uses whichever exists.

On Windows, `SCRPA` vs `scrpa` usually resolve to the same folder, but path comparison or explicit `exist` checks could theoretically differ. Prefer using the **actual** folder name (`scrpa`) everywhere for consistency.

### 4. WinError 5 (Access denied) on report subfolders

When **Step 1** overwrites an existing report folder, it may try to delete **Data**, **Documentation**, and **Reports**. The user has seen:

```text
[WARNING] Could not delete Data: [WinError 5] Access is denied: '...\26C01W04_26_01_27\Data'
```

(or same for Documentation, Reports). The script then reports “Folder cleared” and recreates structure. If those directories (or files inside) are locked—e.g. by Explorer, OneDrive, or an open app—**organize** might also fail to write into them. Check:

- Nothing has the report folder or its subfolders open (Explorer, OneDrive, antivirus).
- Antivirus/OneDrive aren’t blocking deletes or writes.
- If needed, run the batch from an elevated prompt (Run as administrator) as a test.

### 5. Stats script inputs

The stats script looks for **CSV** (and optionally Excel) in `05_EXPORTS\_RMS\scrpa` via patterns like `*SCRPA_RMS*.csv` and `*.csv`. It writes HTML to `SCRPA_ArcPy\06_Output`. If CSVs are missing (e.g. still in archive, or wrong location), stats won’t run correctly and no HTML will be produced for organize to copy.

### 6. Briefing script inputs

The briefing script expects **`*_ReportDate_Last7.csv`** in the exports directory (or archive fallback). It runs with `cd` = `RMS_EXPORT_DIR`. If that directory is wrong or the 7-day CSV isn’t found, briefing fails and tactical outputs are missing.

### 7. Organize script logic

- Chooses the **latest** report folder under `Time_Based\YYYY` by **modification time**.
- Filters CSVs (and Excel) by **report date** derived from the folder name (e.g. `26C01W04_26_01_27` → 2026-01-27). Filenames must contain `2026_01_27` or `26_01_27`.
- Copies from **exports** and **`06_Output`** into **Data**, **Reports**, **Documentation**.

If stats/briefing produce nothing, or outputs are written elsewhere, organize will have nothing to copy and the folder stays empty.

---

## Specific Tasks for Claude

1. **Inspect the latest run log**  
   Path: `02_ETL_Scripts\SCRPA\logs\SCRPA_run_YYYY-MM-DD_HH-MM.log`. Find the section for the run where the user entered `01/27/2026`. Look for Step 2 (`generate_all_reports`) output: stats, briefing, any `[ERROR]`/`[WARNING]`, and Python errors. Note what failed or produced no output.

2. **Verify paths**  
   Ensure `generate_all_reports.bat` and all Python scripts use the **same** exports directory (`scrpa`) and that `06_Output` is where stats/briefing write. Fix any `SCRPA` vs `scrpa` or other path mismatches.

3. **Ensure REPORT_DATE is passed**  
   The parent batch sets `REPORT_DATE` before calling `generate_all_reports.bat`. Confirm the child batch and Python scripts that need it actually receive it (env inheritance). Fix if not.

4. **Clarify or remove “REPORT_DATE format check”**  
   In `Run_SCRPA_Report_Folder.bat`, that log line confuses the user. Either remove it or change it to something like “Passing REPORT_DATE to generate_all_reports” so it’s clear it’s not a format validation step.

5. **Improve Step 2 visibility**  
   Consider logging a clear “Step 2 started” / “Step 2 finished” and, if possible, a short summary (e.g. “Stats OK”, “Briefing OK”) in the main log. Optionally, allow a **debug mode** that prints Step 2 output to the console instead of (or in addition to) the log, to make failures easier to spot.

6. **Address Access Denied on report subfolders**  
   If WinError 5 persists, consider:
   - Retrying deletes with a short delay.
   - Skipping delete and only creating subdirs if missing (overwrite contents instead of deleting folders).
   - Logging explicit “Access denied” guidance for the user (close Explorer/OneDrive, etc.).

7. **Re-run and validate**  
   After changes, the user should run `Run_SCRPA_Report_Folder.bat`, enter `01/27/2026`, and confirm that `26C01W04_26_01_27` ends up with files in **Data**, **Reports**, and **Documentation**. Check the new log to ensure Step 2 and Step 3 complete without errors.

---

## References

- **Verification doc:** `16_Reports\SCRPA\VERIFICATION_01_27_2026_REPORT.md` (troubleshooting, archive fallback, CSV-only re-run, watchdog).
- **Bi-weekly / cycle context:** `README.md`, `SUMMARY.md`, `CHANGELOG.md` in the SCRPA repo; cycle calendar `09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv`.

---

*Generated for SCRPA workflow troubleshooting. Report date: 01/27/2026; folder: 26C01W04_26_01_27.*
