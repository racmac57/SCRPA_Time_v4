Shared context preamble for all SCRPA Claude skills. Every skill references this file and must read the listed files before acting.

## Required Files — Read Before Every Skill Invocation

### 1. CLAUDE.md (repo root)

**Path:** `CLAUDE.md`
**Why:** Contains the five critical logic rules that govern all SCRPA data transformations. Every validation, review, and generation skill must respect these rules exactly:

1. **Report_Date_ForLagday** = `Coalesce(Report_Date, EntryDate)` — NO `Incident_Date` fallback
2. **LagDays** = `CycleStart_7Day - Incident_Date` (NOT `Report_Date - Incident_Date`)
3. **IsLagDay** derived from `Report_Date_ForLagday` cycle resolution (3-tier)
4. **Backfill_7Day**: `Incident_Date < CycleStart AND Report_Date_ForLagday IN [CycleStart, CycleEnd]`
5. **Period priority**: `7-Day > Prior Year > 28-Day > YTD > Historical` (based on `Incident_Date`, NOT `Report_Date`)

Also contains: key data files table, validation checks, bi-weekly cycle table, ChatGPT workflow, script execution order.

**Read instruction:** Read the full file. Pay special attention to "Critical Logic Rules" and "Validation Checks" sections.

### 2. Documentation/data_dictionary.json

**Path:** `Documentation/data_dictionary.json`
**Why:** Defines every column in the enhanced CSV with exact names, types, and computation logic. Skills that validate data or review code must use these exact column names:

- `Report_Date_ForLagday`, `IsCurrent7DayCycle`, `Backfill_7Day`, `IsLagDay`, `LagDays`
- `Period`, `_Period_Debug`, `Period_SortKey`
- `cycle_name`, `cycle_name_adjusted`, `BiWeekly_Report_Name`
- `Incident_Date_Date`, `Report_Date`, `IncidentToReportDays`
- `Crime_Category`, `Incident_Type_1_Norm`, `Category_Type`, `Response_Type`
- `BestTimeValue`, `TimeSource`, `Incident_Time`, `StartOfHour`, `TimeOfDay`

**Read instruction:** Read the `computed_fields` section to understand derivation logic.

### 3. Documentation/PROJECT_SUMMARY.json

**Path:** `Documentation/PROJECT_SUMMARY.json`
**Why:** Defines the pipeline architecture: data flow steps, script purposes, output folder structure, and critical logic summaries. Skills that audit documentation or review architecture need this.

**Read instruction:** Read the `architecture.data_flow`, `scripts`, and `output_structure` sections.

### 4. scripts/run_scrpa_pipeline.py

**Path:** `scripts/run_scrpa_pipeline.py`
**Why:** The main orchestrator that defines:
- Step execution order (1-6)
- `cycle_info` dict shape (keys: `name`, `report_due`, `start_7`, `end_7`, `start_28`, `end_28`, `biweekly`, `start_bw`, `end_bw`)
- File copy and patching logic
- `create_email_template()` format
- Output folder structure creation

**Read instruction:** Read the `run_pipeline()` function to understand the full step sequence and data flow.

### 5. Cycle Calendar CSV

**Path:** `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv`
**Why:** The source of truth for all cycle date windows. Required by any skill that resolves dates to cycles or validates date ranges.

**Columns:** `Report_Due_Date`, `7_Day_Start`, `7_Day_End`, `28_Day_Start`, `28_Day_End`, `Report_Name`, `BiWeekly_Report_Name`

**Read instruction:** Load and parse date columns when cycle resolution or calendar validation is needed.

### 6. CHANGELOG.md

**Path:** `CHANGELOG.md`
**Why:** Contains the version history and known bug patterns. Required by `review_pipeline_change` and `update_changelog` to avoid re-introducing fixed bugs. Key regression patterns:
- v2.0.0: LagDays vs IncidentToReportDays confusion
- v2.0.0: Backfill leaking into 7-Day crime category counts
- v2.0.0: Stale HTML data mismatch
- v1.9.2: Scripts blocking on stdin in batch mode
- v1.9.1: Cycle calendar date gap (missing 01/06/2026)
- v1.2.0: Path case sensitivity (`SCRPA` vs `scrpa` in export paths)

**Read instruction:** Read the `[2.0.0]`, `[1.9.x]`, and `[1.2.0]` sections for regression patterns when reviewing code changes.

## Column Name Reference (Quick Lookup)

When validating or reviewing, use these exact Python column names from the data dictionary:

| Column | Type | Key Rule |
|--------|------|----------|
| `Report_Date_ForLagday` | date | `Coalesce(Report_Date, EntryDate)` — NO Incident_Date |
| `LagDays` | integer | `CycleStart_7Day - Incident_Date` |
| `IsLagDay` | boolean | Incident before cycle containing Report_Date_ForLagday |
| `Backfill_7Day` | boolean | Incident before cycle, reported during current 7-day window |
| `IsCurrent7DayCycle` | boolean | Report_Date_ForLagday in current 7-day window |
| `Period` | string | 7-Day / 28-Day / YTD / Prior Year / Historical |
| `IncidentToReportDays` | integer | Report_Date - Incident_Date (reporting delay, NOT LagDays) |
| `Crime_Category` | string | MVT / Burglary Auto / Burglary - Comm & Res / Robbery / Sexual Offenses / Other |
| `Incident_Date_Date` | date | Best incident date: Coalesce(Incident Date, Incident Date_Between, Report Date) |

## Path Constants Reference

| Constant | Defined In | Value |
|----------|-----------|-------|
| `BASE_DIR` | `run_scrpa_pipeline.py` | `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA` |
| `CYCLE_CALENDAR_PATH` | `scrpa_transform.py` | `09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv` |
| `SCRPA_ARCPY_OUTPUT` | `run_scrpa_pipeline.py` | `02_ETL_Scripts\SCRPA_ArcPy\06_Output` |
| `HPD_REPORT_STYLE_PROMPT_PATH` | `generate_documentation.py` | `08_Templates\Report_Styles\html\HPD_Report_Style_Prompt.md` |
| `TEMPLATE_DIR` | `run_scrpa_pipeline.py` | `08_Templates` |
