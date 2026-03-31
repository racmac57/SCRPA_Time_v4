# Why SCRPA_Combined_Executive_Summary.html Is Not Generated Correctly

## What’s wrong in the current file

For cycle **26C02W06** (report date 02/10/2026), the HTML report shows:

| Section   | HTML shows (wrong) | Should show (from Python pipeline) |
|----------|---------------------|------------------------------------|
| **7-Day incidents** | **1** | **2** |
| **7-Day primary**   | Burglary - Commercial only | Burglary Auto + Burglary - Comm & Res |
| **7-Day list**      | Empty / 1 incident only | Both incidents (e.g. 26-012829, 26-012181) |

So the **attached file is not being generated correctly** because the **7-Day section undercounts by one** and **misses one incident** (Burglary Auto, case 26-012829, incident date 02/03/2026).

---

## Why it happens: two different systems

The HTML file is **not** built by the SCRPA Python pipeline in `16_Reports/SCRPA`. It is built by **SCRPA_ArcPy**, a separate process under `02_ETL_Scripts/SCRPA_ArcPy`.

Rough flow:

1. **Python pipeline** (`run_scrpa_pipeline.py`)  
   - Reads RMS export → runs `scrpa_transform.py` → writes **CSV** (and JSON, docs).  
   - **7-Day logic:** fixed cycle window from the cycle calendar; incident in window ⇒ 7-Day.  
   - **Result:** 2 incidents in 7-Day (correct).

2. **SCRPA_ArcPy**  
   - Reads the **same** RMS export → builds the **HTML** report.  
   - **7-Day logic:** different (e.g. different date field or window).  
   - **Result:** 1 incident in 7-Day (missing Burglary Auto 26-012829).

3. **Pipeline then:**  
   - Calls SCRPA_ArcPy to generate HTML (when the script is found).  
   - Copies the generated `SCRPA_Combined_Executive_Summary_*.html` from `SCRPA_ArcPy/06_Output` into the cycle `Reports` folder.  
   - **Patches** the copied HTML only for **cycle label, date range, version, footer**. It does **not** rewrite the incident counts or tables inside the body.

So the file you attached is “not being generated correctly” because:

- The **content** (counts, incident list, tables) comes entirely from **SCRPA_ArcPy**.
- SCRPA_ArcPy’s 7-Day logic does **not** match the Python pipeline, so it excludes one 7-Day incident and the HTML shows 1 instead of 2.

---

## Root cause in one sentence

**SCRPA_ArcPy uses different 7-Day period logic than the Python pipeline**, so the HTML report’s 7-Day section is wrong even though the pipeline “generates” the file by running ArcPy and copying the result.

---

## What would fix it

1. **Preferred (single source of truth)**  
   Change SCRPA_ArcPy so it **does not** recompute 7-Day from the RMS export. Instead, have it **read the Python pipeline’s CSV** (e.g. `SCRPA_All_Crimes_Enhanced.csv`) and build the 7-Day section from that. Then the HTML will always match the CSV and the rest of the pipeline.

2. **Alternative (align logic)**  
   Keep SCRPA_ArcPy reading the RMS export, but change its **7-Day period logic** to match the Python pipeline exactly (same cycle calendar, same “incident in 7-Day window” rule, same date field). Then regenerate the HTML.

3. **Workaround for this cycle**  
   Manually run SCRPA_ArcPy after ensuring `REPORT_DATE` is set correctly (e.g. `02/10/2026`), and/or fix the ArcPy 7-Day logic so the next run produces 2 incidents; then copy the new HTML into `Time_Based/2026/26C02W06_26_02_10/Reports/SCRPA_Combined_Executive_Summary.html`. The pipeline’s patch step only fixes headers/footer; it cannot fix the wrong counts/tables.

---

## Summary

| Question | Answer |
|----------|--------|
| Why is the attached HTML wrong? | SCRPA_ArcPy’s 7-Day logic excluded one incident (26-012829), so the report showed 1 instead of 2. |
| Why doesn’t the pipeline fix it? | The pipeline only copies ArcPy’s HTML and patches cycle/range/version; it does not replace the body content. |
| How to fix for good? | Make SCRPA_ArcPy use the same cycle calendar and inclusive date logic as the pipeline (fix applied below). |

---

## Fix applied (2026-02-10)

**File:** `02_ETL_Scripts/SCRPA_ArcPy/05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py`

1. **Cycle calendar**  
   ArcPy now uses the same calendar as the Python pipeline: `7Day_28Day_Cycle_20260106.csv` (with 2026 rows). The previous fallback used `7Day_28Day_Cycle_20250414.csv`, which did not support report date 02/10/2026, so cycle lookup failed and 7-Day fell back to “rolling 7 days” and excluded 02/03.

2. **Robust cycle lookup**  
   `get_cycle_info()` now:
   - Tries exact string match on `Report_Due_Date` (MM/DD/YYYY).
   - Falls back to normalizing `Report_Due_Date` to date and comparing.
   - Falls back to “report date = 7_Day_End or 7_Day_End + 1 day”.
   - Falls back to “report date within 7-day range”.

3. **Inclusive end date for 7-Day and 28-Day**  
   The 7-Day (and 28-Day) filter now uses end-of-day for the range end (23:59:59.999) so incidents on the last day of the window are included.

**What you need to do:** Re-run the pipeline (or run SCRPA_ArcPy with `REPORT_DATE=02/10/2026` and copy the new HTML into the cycle Reports folder). The next generated HTML should show 2 incidents in the 7-Day section.
