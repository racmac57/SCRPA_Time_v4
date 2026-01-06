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

**Last Updated**: 2026-01-06  
**Current Version**: 1.6.0  
**Maintained By**: R. A. Carucci

