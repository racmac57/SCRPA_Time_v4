# SCRPA Reporting System

**Strategic Crime Reduction and Problem Analysis (SCRPA) Automated Reporting Workflow**

---

## Overview

The SCRPA Reporting System automates the generation of bi-weekly crime analysis reports from RMS (Records Management System) data exports. The system processes Excel exports, converts them to CSV, generates Power BI dashboards, creates HTML/PDF reports, and organizes all files into a structured folder hierarchy.

**Note**: As of 2026, reporting frequency changed from weekly to bi-weekly (every other week). Historical 2025 data remains weekly for reference.

---

## Project Structure

### Directory Organization

- **`m_code/`** - Active Power BI M code queries (staging and main queries)
  - **`m_code/archive/`** - Archived or deprecated M code queries
- **`preview_tables/`** - CSV preview exports from Power BI queries for validation
- **`time_based/`** - Organized report folders by cycle (YYYY/CCWWW_YY_MM_DD/)
- **`doc/`** - Documentation and analysis files
- **`Documentation/`** - **Canonical** project docs (data_dictionary, PROJECT_SUMMARY, claude.md). Not copied to each cycle; update with `python scripts/generate_documentation.py -o path/to/SCRPA/Documentation`.
- **`scripts/run_scrpa_pipeline.py`** - Python-first pipeline (transforms RMS, writes Data + cycle Documentation + copies Reports).

## Quick Start

### Python pipeline (16_Reports/SCRPA)

1. Place the latest RMS export in `05_EXPORTS\_RMS\scrpa\`.
2. Run `Run_SCRPA_Pipeline.bat` (in this repo) or `python scripts/run_scrpa_pipeline.py` with the CSV and report date.
3. Outputs go to `Time_Based/YYYY/<cycle>_<date>/` with Data/, Documentation/ (cycle-only: `SCRPA_Report_Summary.md`, `CHATGPT_BRIEFING_PROMPT.md`, `CHATGPT_SESSION_PROMPT.md`, `HPD_REPORT_STYLE_BLOCK.md`, `EMAIL_TEMPLATE.txt`, plus copied `PROJECT_SUMMARY.*`), and Reports/ (HTML from SCRPA_ArcPy, patched as configured). Power BI template is copied from `08_Templates\Base_Report.pbix`.

**ChatGPT tactical HTML → PDF:** Follow `CHATGPT_SESSION_PROMPT.md`: close **`.content`** after Lag Day, wrap **7-Day Incident Highlights** + **`.footer`** in **`.report-tail`**, use **`table.incident-highlights`**, and keep the footer inside any landscape wrapper (see `HPD_Report_Style_Prompt.md` / per-cycle style block).

Canonical docs (data_dictionary, PROJECT_SUMMARY, claude.md) live in `16_Reports/SCRPA/Documentation`; they are not written into each cycle folder.

## Quick Start (legacy 02_ETL_Scripts)

### Running a Complete Report

1. **Place Excel Export** in the exports folder:
   ```
   C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa\
   ```

2. **Run the Automation**:
   ```
   C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Run_SCRPA_Report_Folder.bat
   ```

3. **Enter Report Date** when prompted (MM/DD/YYYY format)

4. **Wait for Completion** - The automation will:
   - Convert Excel to CSV
   - Create report folder structure
   - Copy Power BI template
   - Generate HTML/PDF reports
   - Organize all files

---

## Folder Structure

```
16_Reports\SCRPA\
├── m_code\                               # Power BI M Code Queries
│   ├── all_crimes.m                     # Main transformation query
│   ├── q_RMS_Source.m                   # Staging: Loads Excel file
│   ├── q_CycleCalendar.m                # Staging: Loads cycle calendar
│   ├── q_CallTypeCategories.m           # Staging: Loads category mapping
│   ├── archive\                         # Archived/deprecated M code
│   └── README.md                        # M code documentation
├── preview_tables\                       # Power BI CSV Preview Exports
│   └── README.md                        # Preview tables documentation
├── time_based\                           # Organized Report Folders
│   ├── 2025\
│   │   └── 25C12W49_25_12_09\          # Report folder (date-based)
│   │       ├── 25C12W49_25_12_09.pbix  # Power BI template
│   │       ├── Data\                    # CSV files
│   │       ├── Reports\                 # HTML and PDF files
│   │       └── Documentation\           # Markdown files and prompts
│   └── 2026\
├── doc\                                  # System documentation & analysis
│   ├── raw\                             # Raw documentation files
│   └── chunked\                         # Chunked documentation
├── README.md                             # This file
├── CHANGELOG.md                          # Version history
├── SUMMARY.md                            # System summary
└── PROJECT_STRUCTURE.md                  # Detailed structure guide
```

---

## Report Naming Convention

Reports follow this naming pattern:
- **Format**: `YYCMMWww_YY_MM_DD` (weekly format, used for folder names)
- **Bi-Weekly Format**: `YYBW##` (e.g., `26BW01`, `26BW02`) - used in cycle calendar
- **Example**: `26C01W04_26_01_27`
  - `26` = Year (2026)
  - `C` = Calendar
  - `01` = Month (January)
  - `W04` = Week number (with -1 offset)
  - `_26_01_27` = Date suffix (YY_MM_DD)
- **Bi-Weekly Example**: `26BW02` = 2026 Bi-Weekly Report #2 (01/27/26)

**Note**: Folder names continue to use weekly format for consistency. Bi-weekly names are available in the cycle calendar for display/reporting purposes.

---

## Workflow Steps

### Step 1: Excel to CSV Conversion
- **Location**: `05_EXPORTS\_RMS\scrpa\`
- **Script**: `convert_all_xlsx.bat`
- **Output**: CSV files with `*_ReportDate_Last7.csv` for 7-day filtered data

### Step 2: Folder Structure Creation
- **Script**: `generate_weekly_report.py`
- **Creates**: Report folder with subfolders (Data/, Reports/, Documentation/)
- **Copies**: Power BI template (`Base_Report.pbix`)

### Step 3: Report Generation
- **Location**: `SCRPA_ArcPy\06_Output\`
- **Script**: `generate_all_reports.bat`
- **Generates**: HTML and PDF reports

### Step 4: File Organization
- **Script**: `organize_report_files.py`
- **Copies**: CSV files, reports, and documentation to report folder
- **Creates**: Consolidated markdown summary

---

## Key Scripts

### Main Automation
- **`Run_SCRPA_Report_Folder.bat`** - Complete workflow automation
  - Location: `02_ETL_Scripts\`
  - Handles all 4 steps automatically

### Data Processing
- **`convert_all_xlsx.bat`** - Converts Excel files to CSV
- **`export_excel_sheets_to_csv.py`** - Excel conversion engine
- **`prepare_briefing_csv.py`** - Transforms CSV for ChatGPT briefing

### Report Generation
- **`generate_weekly_report.py`** - Creates folder structure and copies template (supports bi-weekly cycles)
- **`organize_report_files.py`** - Organizes files into report folder
- **`generate_all_reports.bat`** - Generates HTML/PDF reports
- **`export_enriched_data_and_email.py`** - Exports enriched data and generates email template

---

## File Types

### Data Files
- **`*_SCRPA_RMS.csv`** - Full RMS export
- **`*_ReportDate_Last7.csv`** - 7-day filtered data
- **`SCRPA_Briefing_Ready_*.csv`** - ChatGPT-ready briefing format

### Reports
- **`*_rms_summary.html/pdf`** - Tactical summary reports
- **`SCRPA_Combined_Executive_Summary_*.html/pdf`** - Strategic executive summaries

### Documentation
- **Canonical** (in `16_Reports/SCRPA/Documentation/` only): `data_dictionary.yaml/json`, `PROJECT_SUMMARY.yaml/json`, `claude.md`. Not copied to each cycle; regenerate with `python scripts/generate_documentation.py -o path/to/SCRPA/Documentation`.
- **Per-cycle** (in each report folder `Documentation/`): `SCRPA_Report_Summary.md` (populated from pipeline data), `CHATGPT_BRIEFING_PROMPT.md` (cycle placeholders filled), `EMAIL_TEMPLATE.txt`.
- **Legacy**: `CHATGPT_USAGE_INSTRUCTIONS.md`, `CHATGPT_PROMPT_GUIDE.md` where present.

---

## Configuration

### Paths
- **Reports Base**: `16_Reports\SCRPA\Time_Based\`
- **Template Source**: `08_Templates\Base_Report.pbix`
- **Exports**: `05_EXPORTS\_RMS\scrpa\`
- **Output**: `SCRPA_ArcPy\06_Output\`

### Week Offset
- **Current**: `-1` (adjusts ISO week number to match SCRPA cycle)
- **Location**: `generate_weekly_report.py` line 16

---

## Dependencies

- **Python 3.13+** (or compatible version)
- **Power BI Desktop** (for `.pbix` files)
- **Required Python Packages**:
  - pandas
  - openpyxl (or calamine for Excel processing)
  - Other packages as needed by scripts

---

## Troubleshooting

### Report Folder Empty (Data/Reports/Documentation not populated)
- **Cause**: Scripts blocking on stdin (e.g. overwrite or input prompts) when run from batch; path case mismatch (`SCRPA` vs `scrpa`); Step 2 output only in log.
- **Solution**: Fixed in v1.9.2. Ensure you use the latest `Run_SCRPA_Report_Folder.bat`, `generate_all_reports.bat`, `generate_weekly_report.py`, and `organize_report_files.py`. Close Explorer/OneDrive on the report folder if you see Access Denied. Check the run log: `02_ETL_Scripts\SCRPA\logs\SCRPA_run_YYYY-MM-DD_HH-MM.log`.

### Access Denied Errors
- **Cause**: OneDrive sync, or Explorer/app holding report subfolders (Data, Reports, Documentation).
- **Solution**: Wait for sync to complete, or close OneDrive/Explorer on the report folder. v1.9.2 reuses existing folders in batch mode instead of delete/recreate.

### Missing CSV Files
- **Cause**: Excel file archived before conversion
- **Solution**: Check `archive\` folder and manually convert if needed. See `VERIFICATION_01_27_2026_REPORT.md` for archive fallback and CSV-only re-run steps.

### Python Not Found
- **Cause**: Python not in PATH
- **Solution**: Install Python or add to system PATH

### Report Date Format
- **Required**: MM/DD/YYYY (e.g., `12/09/2025`)
- **Error**: Script will prompt for correct format

---

## Support

For issues or questions:
1. Check the log file: `02_ETL_Scripts\SCRPA_run_YYYY-MM-DD_HH-MM.log`
2. Review documentation in `doc\` folder
3. Check individual script error messages

---

## Known Issues

### ✅ Resolved Issues

#### Report Folder Empty (Fixed in v1.9.2)
- **Status**: Fixed
- **Solution**: Briefing/organize scripts no longer block on stdin (`<nul` redirection); weekly report reuses folder in batch mode instead of overwrite prompt; path case `scrpa` normalized; log message clarified; Step 1/2/3 output and markers added to run log. WinError 5 mitigated by reusing folders.
- **See**: `CHANGELOG.md` [1.9.2], `VERIFICATION_01_27_2026_REPORT.md` troubleshooting section.

#### Cycle and Range Data Issue (Fixed in v1.2.0)
- **Status**: Fixed
- **Solution**: Added CSV fallback support, fixed path case sensitivity, moved archive timing, enhanced debugging
- **See**: `docs/CYCLE_FIX_SOLUTION.md` for details

---

## Recent Updates

### v2.0.0 (Latest - 2026-02-10)
- ✅ **HTML Auto-Generation**: Pipeline now automatically calls SCRPA_ArcPy to generate fresh HTML reports
- ✅ **Dynamic M Code**: Power BI template automatically finds latest cycle data (no manual editing)
- ✅ **YAML → JSON**: Replaced YAML with JSON for better compatibility and performance
- ✅ **7-Day Counting Fix**: Fixed bug where backfill incidents were counted in 7-Day totals

### v1.9.3 (Latest)
- ✅ **LagDays fix**: `Report_Date_ForLagday` used for LagDays/IsLagDay; lagday tables filter on `Backfill_7Day = TRUE`.
- ✅ **Bi-weekly email and briefing**: Email and ChatGPT prompt use full bi-weekly period and cycle (e.g. 26BW02, 01/13–01/26).
- ✅ **Crime breakdown script**: `scripts/crime_breakdown_and_lagdays.py` outputs category counts and LagDays; writes MD and CSV to Data/ and Documentation/.
- ✅ **Full-dataset export**: `SCRPA_All_Crimes_Full.csv` added to Data/ when running enriched export.
- ✅ **7-day restructure**: Prefers 2026 cycle calendar; briefing and restructure aligned with bi-weekly.

### v1.9.2
- ✅ **Report Folder Empty Fix**: Report folder (Data/Reports/Documentation) now populates correctly when running `Run_SCRPA_Report_Folder.bat`
  - **Briefing script**: Added `<nul` stdin redirection so `prepare_briefing_csv.py` does not block on input
  - **Weekly report**: Batch-mode detection; reuses existing folder without overwrite prompt when run from automation
  - **Organize script**: Added `<nul` and log redirection to avoid blocking
  - **Paths**: `generate_all_reports.bat` uses lowercase `scrpa` to match actual folder
  - **Logging**: "REPORT_DATE format check" → "Passing REPORT_DATE=..."; Step 1/2/3 output and markers in run log
  - **WinError 5**: Reuse existing subfolders in batch mode instead of delete/recreate

### v1.9.1
- ✅ **Cycle Calendar Date Lookup Gap Fix**: Fixed missing entry for 01/06/2026 that created a lookup gap
- ✅ **Validation Logic Fix**: Fixed overly permissive bi-weekly cycle name validation
  - Now requires exact format: weekly (7 chars) and bi-weekly (6 chars with "BW" at positions 2-3)
  - Prevents invalid formats like "TestBW" from passing validation

### v1.9.0
- ✅ **Bi-Weekly Reporting Transition**: System updated to support bi-weekly reporting (every other week) starting 2026
  - Cycle calendar updated with `BiWeekly_Report_Name` column (26 bi-weekly cycles for 2026)
  - Historical 2025 data preserved with weekly format
  - Power BI M code updated to support bi-weekly cycle detection
  - Scripts updated to use updated cycle calendar file (`7Day_28Day_Cycle_20260106.csv`)
  - Email template terminology updated: "Weekly Report" → "Bi-Weekly Report"
  - Lagday logic verified correct - works perfectly with bi-weekly cycles (no changes needed)
  - Analysis periods (7-Day, 28-Day) remain unchanged - only reporting frequency changed
- ✅ **Cycle Calendar Updates**:
  - Added `BiWeekly_Report_Name` column to cycle calendar CSV
  - Updated cycle calendar filename to reflect 2026 data: `7Day_28Day_Cycle_20260106.csv`
  - All 26 bi-weekly cycles for 2026 added (01/13/26 through 12/29/26)
- ✅ **M Code Updates**:
  - `q_CycleCalendar.m`: Added `BiWeekly_Report_Name` column type definition
  - `Export_Formatting.m`: Updated validation to accept both weekly (`C##W##`) and bi-weekly (`##BW##`) formats
  - `all_crimes.m`: Verified correct - no changes needed (works with bi-weekly cycles)
- ✅ **Script Updates**:
  - `generate_weekly_report.py`: Updated to use new cycle calendar file
  - `export_excel_sheets_to_csv.py`: Updated to use new cycle calendar file for 7-day filtering
  - `export_enriched_data_and_email.py`: Updated terminology and uses correct cycle calendar
  - `prepare_briefing_csv.py`: Already had smart fallback - no changes needed

### v1.8.0
- ✅ **LagDays Calculation Bug Fix**: Fixed incorrect LagDays calculation using three-tier approach
- ✅ **Standardized Code Headers**: Added headers to all M code files
- ✅ **Email Template Generation**: Automated email template generation in workflow

### v1.7.0
- ✅ **Project Structure Reorganization**: Organized M code and preview tables into dedicated directories
  - `m_code/` - Active Power BI M code queries
  - `m_code/archive/` - Archived/deprecated M code
  - `preview_tables/` - CSV preview exports from Power BI
  - `doc/` - Documentation and analysis files
- ✅ **Period Classification Fix**: Fixed Period calculation logic for accurate 7-Day/28-Day/YTD classification
  - Improved cycle detection when Today is after cycle end
  - Added explicit null checks for cycle boundaries
  - Fixed 7-Day period check to prevent incorrect 28-Day classification
  - Added diagnostic column (`_Period_Debug`) for troubleshooting
- ✅ **Period Label Update**: Changed "2025 Historical" to "Prior Year" for cleaner, shorter labels
  - Automatically applies to prior year (currently 2025, will be 2026 next year)
  - More intuitive and consistent naming
- ✅ **Color Scheme Update**: Updated visual color assignments
  - Prior Year: `#7F92A2` (gray-blue)
  - YTD: `#118DFF` (blue)
  - 28-Day: `#77C99A` (green - unchanged)
  - 7-Day: (existing color - unchanged)
- ✅ **Cycle Calendar Update**: Updated filename timestamp to reflect 2026 data
  - Renamed: `7Day_28Day_Cycle_20250414.csv` → `7Day_28Day_Cycle_20260106.csv`
  - Updated all M code references to new filename
- ✅ **M Code File Path Fixes**: Fixed broken file paths in M code queries
  - All file paths now single continuous strings (no line breaks)
  - Prevents syntax errors and incorrect path construction
  - Updated VS Code settings to prevent auto-formatting of M files

### v1.6.0
- ✅ **Cycle Calendar 2026 Support**: Added all 2026 cycle entries to cycle calendar CSV
- ✅ **7-Day CSV Date Range Fix**: Excel conversion now uses cycle calendar for accurate 7-day filtering
  - Fixed date range calculation to use actual cycle boundaries instead of "today - 7 days"
  - Script reads REPORT_DATE environment variable and looks up correct cycle dates
  - 7-day filtered CSV files now match cycle calendar dates exactly
  - Works with both openpyxl and calamine engines

### v1.5.0
- ✅ **Zone Formatting Fix**: Zone values now display as whole numbers (5, 8) instead of decimals (5.0, 8.0)
- ✅ **Date Filtering Fix**: Incidents outside cycle date range are now correctly excluded
  - Fixed in both `prepare_briefing_csv.py` and `scrpa_7day_restructure.py`
  - `scrpa_7day_restructure.py` now uses cycle calendar CSV to determine correct cycle dates
  - Filters incidents based on cycle calendar lookup (not min/max from data)
  - Excludes incidents from previous cycles (e.g., 12/22 incidents excluded when cycle is 12/23-12/29)
- ✅ **Data Dictionary Optimization**: Dictionary now stored once in reference location and reused for all reports
- ✅ **Enhanced Narrative Extraction**: Improved ChatGPT prompt with explicit narrative extraction instructions
- ✅ **Documentation Cleanup Guide**: Created guide explaining which documentation files are needed vs historical
- ✅ **Documentation File Limiting**: `organize_report_files.py` now only copies essential documentation files, excluding historical development notes

### v1.3.0
- ✅ **ChatGPT Prompt Enhancements**: Added Reporting Parameters section, Loss And Monetary Rules, Cycle And Date Rules, Summary Table Rules
- ✅ **Simplified Usage**: CSV data already embedded in prompt file - no separate upload needed
- ✅ **Usage Guide**: Created `CHATGPT_USAGE_INSTRUCTIONS.md` for quick reference

### v1.2.0
- ✅ **Path Case Sensitivity**: Fixed folder name case mismatch (`SCRPA` vs `scrpa`)
- ✅ **CSV Support**: Added fallback to CSV files when Excel files not available
- ✅ **Archive Timing**: Archive now runs after HTML generation to prevent conflicts
- ✅ **Enhanced Debugging**: Added extensive DEBUG logging throughout HTML generation
- ✅ **CHATGPT Prompt**: Removed em dashes, added Loss Total calculation instructions

### Technical Details
- Scripts now handle both Excel (`.xlsx`) and CSV (`.csv`) file formats
- Case-insensitive file search for better compatibility
- Improved error messages with full tracebacks
- File verification after write operations
- ChatGPT prompt is self-contained with embedded CSV data

---

## Using ChatGPT for Briefing Generation

### Quick Method
1. Open `CHATGPT_BRIEFING_PROMPT.md` from the report's `Documentation/` folder
2. Copy the **entire file** (Ctrl+A, Ctrl+C)
3. Paste into ChatGPT
4. ChatGPT will generate the HTML briefing

**Note**: The CSV data is already embedded in the prompt file - no separate upload needed!

For detailed instructions, see `CHATGPT_USAGE_INSTRUCTIONS.md` in the Documentation folder.

---

## Version

**Current Version**: 2.0.0  
**Last Updated**: 2026-02-10  
**Maintained By**: R. A. Carucci

**What changed in v2.0.0**: HTML auto-generation integration, dynamic M code (no manual path editing), YAML→JSON migration, 7-day counting bug fixed. See [CHANGELOG.md](CHANGELOG.md#200---2026-02-10).

---

## License

Internal use only - City of Hackensack Police Department

