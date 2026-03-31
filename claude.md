# SCRPA Crime Reporting System - Claude AI Specification

## System Overview

The Strategic Crime Reduction Plan Analysis (SCRPA) system processes crime incident data from the Hackensack Police Department Records Management System (RMS) into structured reports for bi-weekly executive briefings.

**Architecture**: Python-First Processing
- All data transformations occur in Python (`scripts/scrpa_transform.py`)
- Power BI imports pre-processed CSV files (no complex M code)
- Bi-weekly reporting cycles with 7-day and 28-day analysis windows

**HTML:** ArcPy combined reports use `08_Templates/Themes/HTML/scrpa_html.md`. ChatGPT tactical briefings use per-cycle **`HPD_REPORT_STYLE_BLOCK.md`** (START–END excerpt) or the full **`08_Templates/Report_Styles/html/HPD_Report_Style_Prompt.md`** as attachment **#4**.

**PDF / print (tactical HTML):** After Lag Day, **close** `<div class="content">`. Wrap **7-Day Incident Highlights** (`h2` + **`table.incident-highlights`**) and the **`.footer`** in `<div class="report-tail">` (optional **`report-tail-landscape`** for landscape). The **`.footer` must stay inside** that same `div` so browser PDF does not place the footer alone on the next portrait page. Full CSS (`@page`, `.report-tail`, `table.incident-highlights`) comes from the style file above.

## Critical Logic Rules

### 1. Cycle Resolution (3-Tier Lookup)

When determining the current reporting cycle:
1. **Tier 1**: Exact match on Report_Due_Date (most accurate)
2. **Tier 2**: Date falls within a 7-Day cycle window
3. **Tier 3**: Most recent cycle where 7_Day_End <= date

```python
def resolve_cycle(calendar_df, report_due_date):
    # Tier 1: Exact Report_Due_Date match
    match1 = calendar_df[calendar_df['Report_Due_Date'] == report_due_date]
    if len(match1) > 0:
        return match1.iloc[0]

    # Tier 2: Date within 7-Day window
    match2 = calendar_df[
        (calendar_df['7_Day_Start'] <= report_due_date) &
        (report_due_date <= calendar_df['7_Day_End'])
    ]
    if len(match2) > 0:
        return match2.iloc[0]

    # Tier 3: Most recent cycle
    eligible = calendar_df[calendar_df['7_Day_End'] <= report_due_date]
    return eligible.sort_values('7_Day_End').iloc[-1]
```

### 2. LagDays Calculation

**CRITICAL**: LagDays = CycleStart_7Day - Incident_Date

This is NOT `Report_Date - Incident_Date`. The LagDays represents how many days before the cycle start the incident occurred.

For each incident:
1. Find the cycle containing `Report_Date_ForLagday` (using 3-tier lookup)
2. Get that cycle's `7_Day_Start`
3. Calculate: `LagDays = 7_Day_Start - Incident_Date`

### 3. Report_Date_ForLagday

**CRITICAL**: Only uses Report_Date or EntryDate (NO Incident_Date fallback)

```python
Report_Date_ForLagday = Coalesce(Report_Date, EntryDate)
```

When both are null, lag logic correctly yields `IsLagDay=False` and `LagDays=0`.

### 4. Period Classification

Based on **Incident_Date** (not Report_Date), with this priority:
1. **7-Day**: Incident within current 7-day cycle window
2. **Prior Year**: Incident in previous calendar year (e.g., 2025 when current year is 2026)
3. **28-Day**: Incident within current 28-day window (current year only)
4. **YTD**: Incident in current year, outside 7/28-Day windows
5. **Historical**: Older incidents (2024 and earlier)

**Important**: Prior Year is checked BEFORE 28-Day to prevent 2025 incidents from appearing in 28-Day period.

### 5. Backfill_7Day Flag

Identifies late-reported incidents:
```python
Backfill_7Day = (
    Incident_Date < CycleStart_7Day AND
    Report_Date_ForLagday >= CycleStart_7Day AND
    Report_Date_ForLagday <= CycleEnd_7Day
)
```

## Key Data Files

| File | Purpose |
|------|---------|
| `SCRPA_All_Crimes_Enhanced.csv` | Full enriched dataset |
| `SCRPA_7Day_With_LagFlags.csv` | IsCurrent7DayCycle=TRUE filter (includes backfill rows) |
| `SCRPA_7Day_Summary.json` | Lag day statistics and period counts |
| `EMAIL_TEMPLATE.txt` | Bi-weekly report email (ready to send) |
| `CHATGPT_BRIEFING_PROMPT.md` | **Attach** to ChatGPT — cycle params + 7-day narratives |
| `CHATGPT_SESSION_PROMPT.md` | **Paste** into ChatGPT chat — the per-cycle prompt |
| `SCRPA_Report_Summary.md` | **Attach** to ChatGPT — authoritative counts + category table |
| `HPD_REPORT_STYLE_BLOCK.md` | **Attach** — START–END excerpt from `HPD_Report_Style_Prompt.md` |

> Note: `SCRPA_7Day_Lag_Only.csv` and `SCRPA_7Day_Summary.yaml` are no longer generated.
> Backfill rows are included in `SCRPA_7Day_With_LagFlags.csv` (Backfill_7Day=TRUE).

## ChatGPT 7-Day Tactical Briefing Workflow

Each cycle, after the pipeline runs:
1. Open a new chat in the SCRPA ChatGPT project
2. Copy all text from `CHATGPT_SESSION_PROMPT.md` → paste into the chat (or attach it)
3. Attach `CHATGPT_BRIEFING_PROMPT.md`, `SCRPA_Report_Summary.md`, and **one** style file: `HPD_REPORT_STYLE_BLOCK.md` (recommended) **or** full `HPD_Report_Style_Prompt.md` — whichever is attachment **#4**, per `CHATGPT_SESSION_PROMPT.md`
4. Send — ChatGPT generates the HTML tactical briefing
5. Save output as `[CYCLE]_scrpa_tac.html` in `Reports/`
6. Run `Clean_ChatGPT_HTML.bat` on the file to remove any ``` artifacts

## clean_chatgpt_html.py / Clean_ChatGPT_HTML.bat

Removes ChatGPT formatting artifacts from saved HTML files:
- Leading/trailing ` ``` ` or ` ```html ` code fences
- Inline ` ``` ` occurrences inside the HTML body
- ChatGPT citation comments (`<!-- :contentReference[...] -->`)

Usage: drag any `.html` file onto `Clean_ChatGPT_HTML.bat`, or double-click
to scan all HTML files in the `Time_Based/` folder.

## Lag Incident Counts — Two Scopes

The pipeline reports lag counts in two scopes; both are correct:

| Scope | Location | Meaning |
|-------|----------|---------|
| Pipeline console "Lag incidents: N" | Run summary | All IsLagDay=TRUE rows across the full dataset |
| SCRPA_Report_Summary.md "Lag Incidents: N" | Cycle docs | Lag rows within the 7-day window only |

## Bi-Weekly Reporting

For bi-weekly cycles, the reporting period spans two 7-day windows:

| Cycle | Report Due | 7-Day Window | Bi-Weekly Period |
|-------|------------|--------------|------------------|
| 26BW01 | 01/13/2026 | 01/06 - 01/12 | 12/30/2025 - 01/12/2026 |
| 26BW02 | 01/27/2026 | 01/20 - 01/26 | 01/13/2026 - 01/26/2026 |
| 26BW03 | 02/10/2026 | 02/03 - 02/09 | 01/27/2026 - 02/09/2026 |
| 26BW04 | 02/24/2026 | 02/17 - 02/23 | 02/10/2026 - 02/23/2026 |

Formula: `Bi-Weekly Period = (7_Day_Start - 7 days) to 7_Day_End`

## Script Execution Order

```bash
# Run entire pipeline (recommended):
python scripts/run_scrpa_pipeline.py input.xlsx --report-date 02/24/2026

# Or run steps individually:
# 1. Transform raw data
python scripts/scrpa_transform.py input.xlsx -o Data/SCRPA_All_Crimes_Enhanced.csv

# 2. Generate 7-day outputs
python scripts/prepare_7day_outputs.py Data/SCRPA_All_Crimes_Enhanced.csv -o Data/

# 3. Generate cycle documentation (per-cycle, called by pipeline)
python scripts/generate_documentation.py -o Documentation/

# 4. Regenerate canonical docs (run from SCRPA root when docs change)
python scripts/generate_documentation.py -o Documentation/

# 5. Quick validation (automatic via bat, or manual)
python scripts/validate_cycle_quick.py Time_Based/2026/<cycle_folder>
```

## Quick Validation (validate_cycle_quick.py)

Post-pipeline validator called automatically by `Run_SCRPA_Pipeline.bat` after a successful run. Can also be run manually. Performs 3 checks:

1. **File Existence** — Verifies `Data/SCRPA_7Day_Summary.json`, `Data/SCRPA_All_Crimes_Enhanced.csv`, and `Documentation/SCRPA_Report_Summary.md` exist in the cycle folder.
2. **Row Count** — Confirms row count > 0 and `Period` column exists. Notes 0 7-Day rows as expected for early-cycle runs.
3. **Lag/Backfill Alignment** — Verifies `lag_incidents` and `backfill_7day` in JSON match computed counts from the CSV.

Exit code 0 = all passed, exit code 1 = one or more failed.

## Validation Checks

When validating Python output:
1. Row count must match expected (check SCRPA_Report_Summary.md Data Summary)
2. Period sum (7-Day + 28-Day + YTD + Prior Year) must equal Total Incidents
3. LagDays: Verify `(CycleStart_7Day - Incident_Date).days == LagDays`
4. Backfill_7Day=TRUE rows must also have IsLagDay=TRUE
5. All IsCurrent7DayCycle=TRUE rows appear in SCRPA_7Day_With_LagFlags.csv
