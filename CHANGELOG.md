# SCRPA Reporting System - Changelog

All notable changes to the SCRPA Reporting System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Enhanced error handling
- Improved logging
- Config file support

---

## [2.0.0] - 2026-02-10

### Added
- **HTML Report Auto-Generation Integration**
  - Pipeline now automatically calls SCRPA_ArcPy to generate fresh HTML reports before copying
  - Added `_generate_html_report_via_arcpy()` function to `run_scrpa_pipeline.py`
  - Sets `REPORT_DATE` environment variable for correct cycle lookup
  - 5-minute timeout with graceful error handling
  - Ensures HTML reports always contain current cycle data
  - Eliminates need for manual SCRPA_ArcPy execution

- **Dynamic M Code for Power BI Template**
  - M code (`All_Crimes_Simple.m`) now automatically finds the latest cycle folder
  - Uses `Folder.Contents()` to scan `Time_Based/[CURRENT_YEAR]` directory
  - Identifies most recently modified cycle folder
  - Constructs path to `SCRPA_All_Crimes_Enhanced.csv` dynamically
  - Eliminates manual path editing each cycle

### Changed
- **YAML to JSON Migration**
  - Replaced YAML with JSON for 7-day summary output
  - Changed `SCRPA_7Day_Summary.yaml` → `SCRPA_7Day_Summary.json`
  - Updated `prepare_7day_outputs.py` to write JSON (`json.dump()`)
  - Updated `run_scrpa_pipeline.py` to read JSON (`json.load()`)
  - Benefits: Built-in Python support, faster parsing, better compatibility, no external dependencies

- **Pipeline Structure - Step 6 Enhanced**
  - Step 6 now has two sub-steps:
    - 6a: Generate HTML report via SCRPA_ArcPy (NEW)
    - 6b: Copy HTML to cycle folder (existing)
  - Ensures HTML is freshly generated before copying

### Fixed
- **LagDays vs IncidentToReportDays Confusion (Critical Fix - 2026-02-10)**
  - Fixed `prepare_7day_outputs.py` using wrong field for reporting delay statistics
  - **Root Cause**: System has two "lag" concepts that were confused:
    - `LagDays` = CycleStart - Incident_Date (backfill metric, ≤0 for 7-Day incidents)
    - `IncidentToReportDays` = Report_Date - Incident_Date (reporting delay metric)
  - Crime category breakdown now uses `IncidentToReportDays` (was using `LagDays`)
  - Lag statistics now use `IncidentToReportDays` (was using `LagDays`)
  - **Impact**: Previously, lag counts were always 0 for 7-Day incidents; now correctly shows reporting delays
  - See `doc/raw/LAGDAYS_REPORTING_DELAY_FIX_2026_02_10.md` for detailed analysis

- **7-Day Counting Bug (Critical Fix)**
  - Fixed `prepare_7day_outputs.py` incorrectly counting backfill incidents in 7-Day totals
  - Crime category breakdown now filters to `Period='7-Day'` only (excludes backfill)
  - Lag statistics now calculated from actual 7-Day period incidents (not backfill)
  - Changed from `IsLagDay` flag (broken) to `IncidentToReportDays > 0` check (correct)
  - Fixed lag statistics calculation to exclude backfill incidents

- **HTML Report Data Mismatch**
  - HTML reports were showing stale data from previous cycles
  - Root cause: Pipeline only copied existing HTML, didn't ensure fresh generation
  - Fixed by integrating SCRPA_ArcPy HTML generation into pipeline
  - HTML now generated automatically with correct cycle data

- **Documentation Data Errors**
  - Fixed EMAIL_TEMPLATE.txt showing wrong date range (01/27 instead of 02/03)
  - Fixed SCRPA_Report_Summary.md showing incorrect 7-Day counts (3 instead of 2)
  - Fixed lag statistics showing backfill data (14 days) instead of actual 7-Day lag (3.0 days)

- **Configuration Management Issues (2026-02-10 PM)**
  - Removed `.claude/settings.local.json` from version control (developer-specific file)
  - Fixed malformed file paths in copy commands (missing backslash separators)
  - Updated `.gitignore` to prevent future commits of `.local` configuration files
  - See `doc/raw/LOCAL_CONFIG_REMOVAL_2026_02_10.md` for configuration best practices

### Breaking Changes
- **Output Format Change**: `SCRPA_7Day_Summary.yaml` no longer generated per cycle; replaced with `SCRPA_7Day_Summary.json`
- **Reduced YAML Dependency**: `pyyaml` now only required for canonical documentation generation (`generate_documentation.py`), not for cycle-specific outputs

### Documentation
- Created `LAGDAYS_REPORTING_DELAY_FIX_2026_02_10.md` - Complete analysis of LagDays vs IncidentToReportDays confusion
- Created `LOCAL_CONFIG_REMOVAL_2026_02_10.md` - Configuration management best practices and local file removal rationale
- Created `HTML_INTEGRATION_IMPLEMENTATION.md` - Complete documentation of HTML generation integration
- Created `PIPELINE_BUG_FIX_2026_02_10.md` - Details of 7-day counting bug fix
- Created `YAML_TO_JSON_MIGRATION.md` - Migration documentation and benefits
- Created `ROOT_CAUSE_HTML_MISMATCH.md` - Analysis of HTML data mismatch issue
- Updated `BI_WEEKLY_WORKFLOW.md` - Added HTML auto-generation step

### Technical
- **Subprocess Integration**: Pipeline now uses `subprocess.run()` to execute SCRPA_ArcPy script
- **Environment Variables**: Passes `REPORT_DATE` to SCRPA_ArcPy for cycle-aware processing
- **Error Handling**: Graceful degradation if HTML generation fails (falls back to copying existing)
- **Timeout Protection**: 5-minute timeout prevents hanging on SCRPA_ArcPy execution

[2.0.0]: https://github.com/racmac57/SCRPA_Time_v4/compare/v1.9.4...v2.0.0

---

## [1.9.4] - 2026-01-28

### Changed
- **Documentation streamlining**: The pipeline (`run_scrpa_pipeline.py`) no longer writes `data_dictionary.yaml/json`, `PROJECT_SUMMARY.yaml/json`, or `claude.md` into each cycle's Documentation folder. These canonical docs live only in `16_Reports/SCRPA/Documentation`. Regenerate with `python scripts/generate_documentation.py -o path/to/SCRPA/Documentation`.
- **Cycle Documentation contents**: Each cycle's Documentation/ now receives only: `SCRPA_Report_Summary.md` (populated from pipeline data), `CHATGPT_BRIEFING_PROMPT.md` (cycle placeholders filled), and `EMAIL_TEMPLATE.txt`.

### Added
- **SCRPA_Report_Summary.md populated**: Report summary is now filled with real counts (total incidents, 7-Day/28-Day/YTD/Prior Year, lag/backfill counts, lag mean/median/max) and the 7-day-by-crime-category table from the 7-day YAML. Implemented via `write_report_summary_with_data()` and `get_report_summary_with_data()` in `generate_documentation.py`.
- **CHATGPT_BRIEFING_PROMPT.md per cycle**: Pipeline generates `CHATGPT_BRIEFING_PROMPT.md` in each cycle's Documentation/ with cycle ID, bi-weekly, report due, and 7-day/bi-weekly date ranges; footer "HPD | SSOCC | SCRPA Report | Cycle: …". Implemented via `write_chatgpt_briefing_prompt()` and `CHATGPT_BRIEFING_TEMPLATE` in `generate_documentation.py`.

### Documentation
- README: Canonical vs per-cycle documentation clarified; Python pipeline Quick Start and File Types > Documentation updated.
- SUMMARY: Python-first workflow diagram added; v1.9.4 improvements and Maintenance/Updates sections updated; version set to 1.9.4.

[1.9.4]: https://github.com/racmac57/SCRPA_Time_v4/compare/v1.9.3...v1.9.4

---

## [1.9.3] - 2026-01-27

### Fixed
- **LagDays calculation**: Introduced `Report_Date_ForLagday` (no fallback to `Incident_Date`) so LagDays and `IsLagDay` are correct when Report Date is missing. Lagday detail tables should filter on `Backfill_7Day = TRUE` (reported this cycle, incident before cycle), not only `IsLagDay`.

### Added
- **Crime-type breakdown and LagDays**: `scripts/crime_breakdown_and_lagdays.py` produces `CRIME_BREAKDOWN_AND_LAGDAYS.md` and `CRIME_BREAKDOWN_WITH_LAGDAYS.csv` from `SCRPA_7Day_Detailed.csv` (categories: Burglary Auto, MVT, Burglary Commercial/Residence, Sexual Offenses, Robbery). Writes to Data/ and Documentation/.
- **Full-dataset export**: `export_enriched_data_and_email.py` now writes `SCRPA_All_Crimes_Full.csv` (stable-name copy of full preview-style data) to the report Data/ folder.

### Changed
- **Bi-weekly email period**: Email template uses full bi-weekly reporting period (e.g. 01/13–01/26 for 26BW02) when `BiWeekly_Report_Name` is present. `get_date_range_and_biweekly_from_calendar` returns bi-weekly start/end; subject and body use bi-weekly cycle and date range.
- **Bi-weekly briefing prompt**: `prepare_briefing_csv.py` uses `BiWeekly_Report_Name` and bi-weekly date range in cycle info. `cycle_display` (e.g. `26BW02 (26C01W04)`), `range_start_display`, `range_end_display` used in `CHATGPT_BRIEFING_PROMPT.md` and briefing CSV.
- **7-day restructure calendar**: `scrpa_7day_restructure.py` prefers `7Day_28Day_Cycle_20260106.csv`; falls back to legacy calendar if missing.

[1.9.3]: https://github.com/racmac57/SCRPA_Time_v4/compare/v1.9.2...v1.9.3

---

## [1.9.2] - 2026-01-27

### Fixed
- **Report Folder Empty (Data/Reports/Documentation not populated)**
  - **Briefing script blocked on stdin** (`generate_all_reports.bat`): `prepare_briefing_csv.py` was run without `<nul` stdin redirection, causing `safe_input()` to block waiting for Enter. Added `<nul` when invoking the briefing script.
  - **Weekly report script blocked in batch mode** (`generate_weekly_report.py`): When the report folder already existed and stdin was a TTY, the script blocked on "Overwrite? (y/n)". Added batch-mode detection; when stdin is not a TTY (automation), the script reuses the existing folder without prompting.
  - **Organize script blocked on stdin** (`Run_SCRPA_Report_Folder.bat`): `organize_report_files.py` was called without `<nul`, which could block on prompts. Added `<nul` and output redirection to the run log.
- **Path case inconsistency** (`generate_all_reports.bat`): `RMS_EXPORT_DIR` used `SCRPA` (uppercase) vs actual folder `scrpa` (lowercase). Changed to lowercase `scrpa`.
- **Confusing log message** (`Run_SCRPA_Report_Folder.bat`): "REPORT_DATE format check" sounded like an error. Changed to "Passing REPORT_DATE=... to report generation scripts".
- **Step 1/2/3 output not visible in logs** (`Run_SCRPA_Report_Folder.bat`): Step 1 output went to console only; no step markers. Added `>>"%LOG%" 2>&1` for Step 1 and START/END markers for all steps.

### Changed
- **WinError 5 Access Denied mitigation**: In batch mode, scripts now reuse existing report folders instead of trying to delete/recreate subfolders (Data, Reports, Documentation), avoiding Access Denied when those folders are in use (e.g. Explorer, OneDrive).

---

## [1.9.1] - 2026-01-26

### Fixed
- **Cycle Calendar Date Lookup Gap**
  - Fixed missing entry for 01/06/2026 that created a lookup gap between 01/06-01/12/2026
  - Added back weekly entry `01/06/2026,12/30/2025,01/05/2026,12/09/2025,01/05/2026,26C01W01,` with empty `BiWeekly_Report_Name`
  - Ensures all dates in 2026 can be looked up correctly
  - Maintains backward compatibility while preserving bi-weekly reporting structure

- **Overly Permissive Cycle Name Validation**
  - Fixed validation logic in `Export_Formatting.m` that was too loose
  - Previous logic accepted any string containing "BW" with 5+ characters (e.g., "TestBW", "XBWabc")
  - New validation requires:
    - Weekly: Must start with "C", contain "W", and be exactly 7 characters (e.g., `26C01W02`)
    - Bi-weekly: Must be exactly 6 characters with "BW" at positions 2-3 (e.g., `26BW01`)
  - Prevents data integrity issues in downstream processes

### Added
- **Issue Fix Documentation**
  - Created `ISSUE_FIXES_v1.9.1.md` documenting both fixes with testing recommendations

---

## [1.9.0] - 2026-01-26

### Added
- **Bi-Weekly Reporting Support**
  - Added `BiWeekly_Report_Name` column to cycle calendar CSV
  - Bi-weekly naming convention: `YYBW##` (e.g., `26BW01`, `26BW02`)
  - 26 bi-weekly cycles for 2026 (01/13/26 through 12/29/26)
  - Historical 2025 data preserved with weekly format for reference
  - Cycle calendar filename updated: `7Day_28Day_Cycle_20260106.csv`

- **Bi-Weekly Cycle Calendar Integration**
  - Updated `q_CycleCalendar.m` to include `BiWeekly_Report_Name` column type definition
  - Updated `Export_Formatting.m` to accept both weekly (`C##W##`) and bi-weekly (`##BW##`) formats
  - All scripts updated to use new cycle calendar file

- **Documentation**
  - Created `BI_WEEKLY_CYCLE_SETUP.md` - Comprehensive bi-weekly transition guide
  - Created `STEP1_CYCLE_CALENDAR_UPDATE.md` - Cycle calendar update documentation
  - Created `STEP2_M_CODE_UPDATES.md` - M code update instructions
  - Created `STEP3_SCRIPT_VERIFICATION.md` - Script verification and updates
  - Created `LAGDAY_LOGIC_VERIFICATION.md` - Detailed lagday logic analysis
  - Created `FINAL_VERIFICATION_SUMMARY.md` - Complete verification summary
  - Created `POWER_BI_UPDATE_QUICK_REFERENCE.md` - Quick reference for Power BI updates
  - Created `PRE_SAVE_CHECKLIST.md` - Pre-save verification checklist

### Changed
- **Reporting Frequency**
  - Changed from weekly to bi-weekly reporting (every other week) starting 2026
  - Analysis periods (7-Day, 28-Day) remain unchanged - only reporting frequency changed
  - Folder naming continues to use weekly format for consistency with existing folders

- **Cycle Calendar**
  - Updated cycle calendar CSV with bi-weekly entries for 2026
  - Added `BiWeekly_Report_Name` column populated for 2026 entries
  - 2025 entries have null `BiWeekly_Report_Name` (expected - historical weekly data)
  - Updated cycle calendar filename to reflect 2026 data: `7Day_28Day_Cycle_20260106.csv`

- **Power BI M Code**
  - `q_CycleCalendar.m`: Added `BiWeekly_Report_Name` column to type definitions
  - `Export_Formatting.m`: Updated cycle name validation to accept both weekly and bi-weekly formats
  - `all_crimes.m`: Verified correct - no changes needed (works with bi-weekly cycles)

- **Python Scripts**
  - `generate_weekly_report.py`: Updated cycle calendar path to `7Day_28Day_Cycle_20260106.csv`
  - `export_excel_sheets_to_csv.py`: Updated cycle calendar path for 7-day CSV filtering
  - `export_enriched_data_and_email.py`: Updated email template terminology ("Weekly" → "Bi-Weekly")
  - `prepare_briefing_csv.py`: Already had smart fallback - no changes needed

- **Email Template**
  - Updated subject line: "SCRPA Weekly Report" → "SCRPA Bi-Weekly Report"
  - Template generation script uses correct cycle calendar file

### Verified
- **Lagday Logic Verification**
  - Verified lagday logic is correct and works perfectly with bi-weekly cycles
  - Three-tier approach (Report_Due_Date match, date range match, most recent cycle) works correctly
  - No changes needed to lagday calculation logic
  - Period classification (7-Day, 28-Day, YTD, Prior Year) works correctly with bi-weekly cycles

### Technical
- **Backward Compatibility**
  - `Report_Name` column still exists and is used by `all_crimes.m`
  - System works with both weekly and bi-weekly cycles
  - Historical data (2025) continues to use weekly names
  - Folder naming maintains weekly format for consistency

- **Date Range Logic**
  - Analysis periods (7-Day, 28-Day) remain unchanged
  - Date ranges continue to roll forward every 7 days regardless of bi-weekly reporting
  - Only reporting frequency changed, not analysis windows

---

## [1.8.0] - 2026-01-13

### Fixed
- **LagDays Calculation Bug (Critical Fix)**
  - Fixed incorrect LagDays calculation that was showing values 2 days off
  - Changed from simple cycle lookup to three-tier approach matching CurrentCycleTbl logic
  - Now uses: (1) Report_Due_Date match, (2) Report Date within cycle range, (3) Most recent cycle fallback
  - Fixes cases where LagDays showed 4 instead of 2, and 2 instead of 0
  - Updated both `all_crimes.m` and `ALL_QUERY_M_CODE.m` with consistent logic
  - Ensures correct cycle start date is used for lagday calculations

### Added
- **Standardized Code Headers**
  - Added standardized headers to all M code files with timestamp, project path, author, and purpose
  - Headers follow format: timestamp (EST), project path, author (R. A. Carucci), purpose description
  - Applied to: `all_crimes.m`, `q_CallTypeCategories.m`, `q_CycleCalendar.m`, `q_RMS_Source.m`
  - Headers use M code comment syntax (`//`) and include emoji timestamp indicator

- **Email Template Generation Enhancement**
  - Enhanced email template format with bullet points (•) for better readability
  - Updated date formatting to MM/DD/YYYY format for Date Generated field
  - Email template now automatically generated during report workflow
  - Template includes: Subject line with cycle name and date range, formatted body with all report sections

- **Automated Email Template Generation in Workflow**
  - Added Step 4 to `Run_SCRPA_Report_Folder.bat` to automatically generate email template
  - Script runs after file organization step
  - Gracefully handles cases where All_Crime CSV hasn't been exported from Power BI yet
  - Email template saved to `Documentation/EMAIL_TEMPLATE.txt` in report folder

### Changed
- **Email Template Script Updates**
  - Updated `export_enriched_data_and_email.py` with improved email template format
  - Added standardized header to Python script
  - Enhanced date parsing to handle multiple date formats
  - Improved error handling for missing cycle calendar data

- **Power BI Template Updated**
  - Updated `Base_Report.pbix` template with new M code versions
  - All queries updated: `all_crimes`, `q_CallTypeCategories`, `q_CycleCalendar`, `q_RMS_Source`
  - Template location: `C:\Users\carucci_r\OneDrive - City of Hackensack\15_Templates\Base_Report.pbix`
  - New template includes: LagDays calculation fix, standardized headers, and all recent improvements
  - Future reports generated from this template will automatically include all fixes

---

## [1.7.0] - 2026-01-06

### Added
- **Project Structure Reorganization**
  - Created `m_code/` directory for active Power BI M code queries
  - Created `m_code/archive/` subdirectory for archived/deprecated M code
  - Created `preview_tables/` directory for Power BI CSV preview exports
  - Organized documentation files into `doc/` directory
  - Added README files to each directory explaining purpose and usage
  - Created `PROJECT_STRUCTURE.md` for comprehensive structure documentation

- **Period Classification Diagnostic Column**
  - Added `_Period_Debug` column to All_Crimes query for troubleshooting
  - Shows incident date, cycle detection status, cycle boundaries, and classification logic
  - Helps identify why Period values are assigned

- **Documentation Files**
  - `TEMPLATE_UPDATE_CHECKLIST.md` - Step-by-step guide for updating Power BI template
  - `COLOR_SCHEME_RECOMMENDATIONS.md` - Final color assignments and implementation guide
  - `DISABLE_M_CODE_FORMATTING.md` - Guide for preventing auto-formatting in VS Code
  - `ACCESS_VS_CODE_SETTINGS.md` - Alternative methods to access settings when Ctrl+Shift+P is blocked
  - `PERIOD_FIX_EXPLANATION.md` - Explanation of Period calculation fixes
  - `YTD_VERIFICATION_EXPLANATION.md` - Why YTD doesn't appear early in the year

### Changed
- **Period Label Update**
  - Changed "2025 Historical" to "Prior Year" for cleaner, shorter labels
  - Automatically applies to prior year (dynamic, not hardcoded to 2025)
  - Updated Period_SortKey logic to handle new label

- **Period Calculation Logic**
  - Improved cycle detection when Today is after cycle end date
  - Added explicit null checks for cycle boundary values
  - Separated 7-Day and 28-Day checks with clear variables
  - Ensured 28-Day only matches if 7-Day doesn't (`not in7Day` condition)
  - Fixed issue where incidents were incorrectly classified as "28-Day" instead of "7-Day"

- **Cycle Calendar Filename**
  - Updated: `7Day_28Day_Cycle_20250414.csv` → `7Day_28Day_Cycle_20260106.csv`
  - Reflects when 2026 data was added to the calendar
  - Updated all M code references (`q_CycleCalendar.m`) to new filename

- **Visual Color Scheme**
  - Prior Year: Changed from `#118DFF` (blue) to `#7F92A2` (gray-blue)
  - YTD: Now uses `#118DFF` (blue, moved from Prior Year)
  - 28-Day: `#77C99A` (green - unchanged)
  - 7-Day: (existing color - unchanged)

- **M Code File Organization**
  - Moved all active M code files to `m_code/` directory
  - Archived dated/legacy M code to `m_code/archive/`
  - Moved preview CSV files to `preview_tables/` directory
  - Moved documentation/analysis files to `doc/` directory

### Fixed
- **M Code File Paths**
  - Fixed broken file paths in `q_CallTypeCategories.m` and `q_RMS_Source.m`
  - All file paths now single continuous strings (no line breaks)
  - Prevents syntax errors and incorrect path construction

- **Period Classification**
  - Fixed issue where Case 26-001094 (01/04/2026) was showing "28-Day" instead of "7-Day"
  - Fixed issue where Case 25-113412 (12/29/2025) was showing "28-Day" instead of "Prior Year"
  - Improved cycle detection logic to correctly find current cycle when Today is after cycle end

- **VS Code Auto-Formatting**
  - Configured `.vscode/settings.json` to prevent auto-formatting of M code files
  - Disabled format on save, paste, and type for M files
  - Disabled Prettier for M files
  - Prevents file paths from being broken by auto-formatting

### Technical
- **Query Performance**
  - Query load times: ~2 minutes (acceptable performance)
  - Staging queries optimized with Table.Buffer
  - Removed PromoteAllScalars for better performance

---

## [1.6.0] - 2026-01-06

### Fixed
- **7-Day CSV Date Range Calculation**
  - Fixed `export_excel_sheets_to_csv.py` to use cycle calendar for 7-day filtering instead of simple "today - 7 days" calculation
  - Script now reads `REPORT_DATE` environment variable and looks up correct cycle dates from cycle calendar CSV
  - 7-day filtered CSV files now use actual cycle boundaries (e.g., 12/30/2025 to 01/05/2026 for cycle 26C01W01)
  - Falls back to simple calculation only if cycle calendar lookup fails
  - Works with both openpyxl and calamine engines

### Changed
- **Cycle Calendar Extended**
  - Updated cycle calendar CSV (`7Day_28Day_Cycle_20250414.csv`) with 2026 entries
  - Added all 52 weeks for 2026 (01/06/2026 through 12/29/2026)
  - Cycle names follow pattern: `26C01W01` through `26C13W52`
  - Dates formatted as MM/DD/YYYY for consistency

### Added
- **Cycle Calendar Integration in Excel Conversion**
  - Added `_get_cycle_dates_from_calendar()` function to `export_excel_sheets_to_csv.py`
  - Function reads cycle calendar CSV and looks up 7-day start/end dates based on REPORT_DATE
  - Supports exact match on Report_Due_Date, fallback to date range matching, and most recent cycle lookup
  - Logs cycle information when successfully found

---

## [1.5.0] - 2025-12-29

### Fixed
- **Zone Formatting Issue**
  - Fixed Zone values displaying as decimals (5.0, 8.0) instead of whole numbers (5, 8)
  - Updated `generate_briefing_html.py` to convert Zone values to integers before display
  - Updated `prepare_briefing_csv.py` to format Zone as whole number during CSV transformation
  - Added instructions to ChatGPT prompt to format Zone as whole number

- **Date Filtering Issue (Multiple Scripts)**
  - Fixed incidents with Report Date outside cycle range being included in reports
  - Added filtering logic in `prepare_briefing_csv.py` to exclude incidents with Report Date before cycle start or after cycle end
  - **Fixed `scrpa_7day_restructure.py` date filtering**: Script now uses cycle calendar CSV to determine correct cycle dates instead of min/max Report Date from data
  - Script looks up cycle from calendar using `REPORT_DATE` environment variable
  - Filters incidents to only include those with Report Date within the cycle range (e.g., 12/23 to 12/29 for report date 12/30)
  - Excludes incidents from previous cycles (e.g., 12/22 incidents excluded when cycle is 12/23-12/29)
  - Reports how many records were excluded if any fall outside the cycle range

### Changed
- **Version Standardization**
  - Updated version format from `1.5` to `1.5.0` (standardized to semantic versioning)
  - All output files (HTML reports, ChatGPT prompts) now display version 1.5.0

- **Data Dictionary Storage**
  - Data Dictionary now stored once in reference location: `09_Reference\Standards\RMS\SCRPA\SCRPA_7Day_Data_Dictionary.md`
  - Script checks for existing reference dictionary and copies from there instead of regenerating
  - Ensures consistency across all reports and eliminates redundant generation
  - First run creates the dictionary in reference location, all future runs copy from there

- **ChatGPT Prompt Enhancement**
  - Enhanced narrative extraction instructions with explicit "CRITICAL - NARRATIVE EXTRACTION" section
  - Added detailed list of what to extract from Narrative column (suspect descriptions, vehicles, loss items, methods, etc.)
  - Emphasized that Narrative column contains more complete information than structured fields
  - Added note: "DO NOT rely solely on pre-processed columns"

### Added
- **Documentation Guide**
  - Created `DOCUMENTATION_FILES_EXPLAINED.md` explaining which files are needed vs historical notes
  - Clarified that only `CHATGPT_BRIEFING_PROMPT.md` is needed for ChatGPT usage
  - Documented which historical development files can be removed from Documentation/ folder

- **Documentation File Limiting**
  - Updated `organize_report_files.py` to only copy essential documentation files
  - Excludes historical development notes (e.g., `CHATGPT_PROMPT_UPDATE_REVIEW.md`, `CYCLE_FIX_PROMPT.md`, `FIX_PROMPT_AND_REPORTS_FOLDER.md`, `CSV_RETENTION_AND_PROMPT_FIX.md`)
  - Only copies essential guides like `CHATGPT_PROMPT_GUIDE.md` and `SCRPA_WORKFLOW_USER_GUIDE.md` (if they exist)
  - Reduces clutter in Documentation/ folder by excluding development history files

---

## [1.3.0] - 2025-12-09

### Added
- **ChatGPT Prompt Enhancements (Based on ChatGPT Recommendations)**
  - Added "Reporting Parameters For This Run" section with Cycle ID, Date Range (ISO format), Version, Prepared By, Submitted To
  - Added "Loss And Monetary Rules" section with 5-step process for calculating Loss Total
  - Added "Cycle And Date Rules" section ensuring consistency across HTML output
  - Added "Summary Table Rules" section ensuring Loss Total matches between bullets and table
  - Created `CHATGPT_USAGE_INSTRUCTIONS.md` quick reference guide
  - Clarified that CSV data is embedded in prompt file (no separate upload required)

### Changed
- **CHATGPT_BRIEFING_PROMPT Instructions**
  - Updated instructions to clarify CSV data is already embedded
  - Added Option 1 (recommended): Copy entire prompt file
  - Added Option 2 (alternative): Upload CSV separately
  - Improved clarity on what to provide to ChatGPT

### Fixed
- **Date Format Handling**
  - Reporting Parameters section uses ISO format (YYYY-MM-DD) as recommended by ChatGPT
  - HTML template continues to use MM/DD/YYYY format for display
  - Date conversion function handles edge cases gracefully

---

## [1.2.0] - 2025-12-09

### Fixed
- **Path Case Sensitivity**
  - Fixed case mismatch in config paths (`SCRPA` vs `scrpa`)
  - Updated `config.py` to use lowercase `scrpa` folder name
  - Updated fallback paths in `RMS_Statistical_Export_FINAL_COMPLETE.py`
  - Scripts now correctly find Excel/CSV files in exports folder

- **CSV File Support**
  - Added CSV file fallback when Excel files not found
  - Updated `get_latest_rms_file()` to search for CSV files if Excel unavailable
  - Updated `load_and_analyze_rms_data()` to handle both Excel and CSV formats
  - Added case-insensitive file search for better compatibility

- **Archive Timing**
  - Moved archive function to run AFTER HTML generation (was running before)
  - Prevents archiving newly generated HTML files
  - Archive now runs after all reports are generated

- **Batch File Syntax Error**
  - Fixed "may was unexpected at this time" error in `generate_all_reports.bat`
  - Escaped parentheses in echo statements for proper batch parsing
  - Improved error message formatting

- **Enhanced Debugging**
  - Added extensive DEBUG logging throughout HTML generation process
  - Added file path verification and existence checks
  - Added file size verification after write operations
  - Improved error messages with full tracebacks

### Changed
- **CHATGPT_BRIEFING_PROMPT Generation**
  - Removed em dashes (—) and replaced with regular hyphens (-)
  - Updated HTML template to use standard ASCII characters
  - Added explicit Loss Total calculation instructions
  - Loss Total now clearly documented as sum of individual loss items
  - Updated all HTML template sections with Loss Total calculation guidance

### Added
- **Loss Total Calculation Logic**
  - Added instructions that Loss Total = sum of all individual loss items
  - Updated all HTML template sections with calculation guidance
  - Added verification instructions in data processing section

---

## [1.1.0] - 2025-12-09

### Changed
- **Project Reorganization**
  - Moved scripts to `SCRPA\scripts\` folder
  - Moved logs to `SCRPA\logs\` folder
  - Moved documentation to `SCRPA\docs\` folder
  - Created archive folder for old/broken scripts

- **Cycle Lookup System**
  - Updated scripts to use cycle calendar CSV (`7Day_28Day_Cycle_20250414.csv`)
  - Replaced calculated cycle names with calendar-based lookup
  - Added REPORT_DATE environment variable support

- **Version Numbering**
  - Updated Combined Executive Summary HTML version from v1.0 to v1.1

### Fixed
- **Folder Overwrite Prompt**
  - Fixed prompt to always appear when folder exists
  - Improved handling of non-interactive mode

- **Path References**
  - Updated batch file paths after script reorganization
  - Fixed PowerShell script path references
  - Updated log file location to `SCRPA\logs\`

### Fixed (by Claude AI)
- **✅ Cycle/Range Data Issue - Root Cause Fixed**
  - **Root Cause**: Output suppression (`>nul 2>&1`) hid all errors - script reported success even when HTML wasn't created
  - **Fix Applied**: Added output capture to temporary log file with error display
  - **Fix Applied**: Added extensive DEBUG logging throughout HTML generation
  - **Fix Applied**: Added file creation verification with size check
  - **Status**: Fixes applied - Testing required to verify HTML generation works correctly
  - **See**: `docs/CYCLE_FIX_SOLUTION.md` and `docs/CLAUDE_FIX_SUMMARY.md` for details

---

## [1.0.0] - 2025-12-09

### Added
- **Complete Automation Workflow**
  - `Run_SCRPA_Report_Folder.bat` - Comprehensive automation script
  - Handles all 4 steps: folder creation, report generation, file organization
  - Date-aware workflow with user prompts

- **Folder Structure Generation**
  - `generate_weekly_report.py` - Creates report folders with naming convention
  - Automatic Power BI template copying
  - Subfolder creation (Data/, Reports/, Documentation/)

- **File Organization System**
  - `organize_report_files.py` - Automatically organizes all report files
  - Copies CSV files, reports, and documentation to appropriate folders
  - Creates consolidated markdown summaries

- **Excel to CSV Conversion**
  - `convert_all_xlsx.bat` - Batch conversion script
  - `export_excel_sheets_to_csv.py` - Excel processing engine
  - Support for 7-day filtered exports (`--report-last7`)

- **Briefing Preparation**
  - `prepare_briefing_csv.py` - Transforms CSV for ChatGPT processing
  - Automatic prompt generation (`CHATGPT_BRIEFING_PROMPT.md`)
  - Cycle-aware data processing

- **Report Generation**
  - HTML and PDF report generation
  - Tactical summaries (`*_rms_summary.html/pdf`)
  - Strategic executive summaries (`SCRPA_Combined_Executive_Summary_*.html/pdf`)

- **Documentation**
  - README.md - System overview and quick start guide
  - CHANGELOG.md - Version history
  - SUMMARY.md - System summary
  - In-folder documentation (CHATGPT_PROMPT_GUIDE.md, etc.)

### Changed
- **Report Folder Structure**
  - Moved from `SCRPA_ArcPy` to `16_Reports\SCRPA\Time_Based\`
  - Organized by year and date-based folders
  - Standardized subfolder structure

- **Naming Convention**
  - Implemented `YYCMMWww_YY_MM_DD` format
  - Week offset adjustment (-1) for SCRPA cycle alignment

- **Workflow Integration**
  - Consolidated multiple scripts into single automation
  - Reduced manual steps from 5+ to 1 batch file execution

### Fixed
- **File Archiving**
  - Fixed archive step running before conversion
  - Improved error handling for archived files

- **OneDrive Sync Issues**
  - Added handling for "Access Denied" errors during folder operations
  - Improved folder clearing logic

- **Python Detection**
  - Enhanced Python path detection in batch files
  - Support for multiple Python installations

### Security
- **Path Validation**
  - Ensures output stays within OneDrive directory
  - Prevents accidental file system access outside workspace

---

## [0.9.0] - 2025-12-02

### Added
- Initial folder structure creation
- Power BI template copying
- Basic CSV file organization

### Changed
- Reorganized ETL scripts structure
- Separated SCRPA scripts from SCRPA_ArcPy production folder

---

## [0.8.0] - 2025-12-01

### Added
- Excel to CSV conversion scripts
- Briefing CSV preparation
- ChatGPT prompt generation

---

## [0.7.0] - 2025-11-25

### Added
- Initial report generation scripts
- HTML/PDF report templates
- Basic file organization

---

## Future Enhancements

### Planned
- [ ] Dry-run mode for archiving
- [ ] Config file for path management
- [ ] Log rotation for better log management
- [ ] ProcessPoolExecutor for CPU-bound operations
- [ ] Airflow pipeline orchestration
- [ ] Automated email distribution
- [ ] Report scheduling

### Under Consideration
- [ ] Multi-user support
- [ ] Web-based interface
- [ ] Database integration
- [ ] Real-time data updates
- [ ] Advanced analytics features

---

## Notes

- Version numbers follow Semantic Versioning (MAJOR.MINOR.PATCH)
- Dates follow ISO 8601 format (YYYY-MM-DD)
- All changes are documented with clear descriptions

---

**Last Updated**: 2026-02-10  
**Current Version**: 2.0.0  
**Maintained By**: R. A. Carucci

