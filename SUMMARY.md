# SCRPA Reporting System - Summary

**Strategic Crime Reduction and Problem Analysis (SCRPA) Automated Reporting Workflow**

---

## System Purpose

The SCRPA Reporting System automates the bi-weekly generation of crime analysis reports from RMS data exports. It transforms raw Excel exports into organized, structured reports with Power BI dashboards, HTML/PDF summaries, and ChatGPT-ready briefing formats.

**Note**: As of 2026, reporting frequency changed from weekly to bi-weekly (every other week). The system supports both formats and maintains historical weekly data for reference.

---

## Architecture Overview

### Core Components

1. **Data Ingestion**
   - Excel file exports from RMS
   - Automatic conversion to CSV format
   - 7-day filtered data extraction

2. **Report Generation**
   - Power BI dashboard templates
   - HTML tactical summaries
   - PDF executive summaries
   - ChatGPT briefing formats

3. **File Organization**
   - Date-based folder structure
   - Automatic file categorization
   - Consolidated documentation

4. **Automation Workflow**
   - Single batch file execution
   - Multi-step process automation
   - Error handling and logging

---

## Key Features

### ✅ Automation
- **One-Click Execution**: Single batch file runs entire workflow
- **Date-Aware**: Automatically handles report dates and naming
- **Error Recovery**: Continues processing even if individual steps fail

### ✅ Organization
- **Structured Folders**: Year → Date-based report folders
- **File Categorization**: Data, Reports, Documentation separation
- **Consolidated Summaries**: Single markdown file with all report info

### ✅ Flexibility
- **Multiple Report Types**: Tactical, Strategic, Briefing formats
- **Configurable Paths**: Easy to update folder locations
- **Extensible**: Modular scripts for easy enhancement

### ✅ Documentation
- **Auto-Generated Prompts**: ChatGPT-ready briefing instructions with embedded CSV data
- **Usage Guides**: Step-by-step documentation and quick reference guides
- **Version Tracking**: Changelog and summary files
- **Self-Contained Prompts**: All data and instructions in one file for easy ChatGPT usage

---

## Workflow Diagram

### Python-first pipeline (16_Reports/SCRPA)

```
1. RMS Export (Excel or CSV)
   └─> 05_EXPORTS\_RMS\scrpa\

2. Run Pipeline
   └─> Run_SCRPA_Pipeline.bat  OR  python scripts/run_scrpa_pipeline.py
       │
       ├─> scrpa_transform.py     → SCRPA_All_Crimes_Enhanced.csv
       ├─> prepare_7day_outputs   → SCRPA_7Day_With_LagFlags.csv, SCRPA_7Day_Summary.json
       ├─> Generate HTML          → Calls SCRPA_ArcPy to generate fresh HTML
       ├─> Cycle Documentation    → SCRPA_Report_Summary.md (populated), HPD_REPORT_STYLE_BLOCK.md, CHATGPT_BRIEFING_PROMPT.md, CHATGPT_SESSION_PROMPT.md, EMAIL_TEMPLATE.txt; copies PROJECT_SUMMARY from canonical Documentation
       └─> Copy Reports           → SCRPA_Combined_Executive_Summary.html (from SCRPA_ArcPy/06_Output, patched)

3. Report Folder (cycle docs; canonical claude.md/data_dictionary stay in repo `Documentation/` only)
   └─> 16_Reports\SCRPA\Time_Based\YYYY\<cycle>_<date>\
       ├─> Data/          (Enhanced CSV, 7-day CSV, JSON summary)
       ├─> Documentation/ (report summary, ChatGPT prompts, HPD style block, email template, PROJECT_SUMMARY copy)
       └─> Reports/       (HTML/PDF from ArcPy)
```

Canonical docs (data_dictionary, PROJECT_SUMMARY, claude.md) live in `16_Reports/SCRPA/Documentation` and are not copied to each cycle. Update with: `python scripts/generate_documentation.py -o path/to/SCRPA/Documentation`.

### Legacy 02_ETL_Scripts workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    SCRPA REPORT WORKFLOW (Legacy)            │
└─────────────────────────────────────────────────────────────┘

1. Excel Export → 05_EXPORTS\_RMS\scrpa\*.xlsx
   ├─> convert_all_xlsx.bat → CSV
   └─> prepare_briefing_csv.py → SCRPA_Briefing_Ready_*.csv

2. Run_SCRPA_Report_Folder.bat
   ├─> STEP 1: generate_weekly_report.py (folder + template)
   ├─> STEP 2: generate_all_reports.bat (HTML/PDF)
   └─> STEP 3: organize_report_files.py (copy + documentation)

3. Report Folder → Time_Based\YYYY\25C12W49_25_12_09\
   ├─> Data/
   ├─> Reports/
   └─> Documentation/
```

---

## File Types and Locations

### Input Files
- **Excel Exports**: `05_EXPORTS\_RMS\scrpa\*.xlsx`
- **Templates**: `08_Templates\Base_Report.pbix`

### Processing Locations
- **ETL Scripts**: `02_ETL_Scripts\SCRPA\`
- **Output**: `SCRPA_ArcPy\06_Output\`

### Final Output
- **Reports**: `16_Reports\SCRPA\Time_Based\YYYY\ReportFolder\`
- **Archives**: `05_EXPORTS\_RMS\scrpa\archive\`

---

## Report Types

### 1. Power BI Dashboard
- **File**: `25C12W49_25_12_09.pbix`
- **Purpose**: Interactive data visualization
- **Location**: Report folder root

### 2. Tactical Summary
- **Format**: HTML and PDF
- **Naming**: `*_rms_summary.html/pdf`
- **Purpose**: Day-to-day operational briefings
- **Location**: `Reports/` folder

### 3. Executive Summary
- **Format**: HTML and PDF
- **Naming**: `SCRPA_Combined_Executive_Summary_*.html/pdf`
- **Purpose**: High-level strategic analysis
- **Location**: `Reports/` folder

### 4. Briefing CSV
- **Format**: CSV
- **Naming**: `SCRPA_Briefing_Ready_*.csv`
- **Purpose**: ChatGPT processing for narrative extraction
- **Location**: `Data/` folder

---

## Naming Conventions

### Report Folders
- **Pattern**: `YYCMMWww_YY_MM_DD` (weekly format, used for folder names)
- **Bi-Weekly Format**: `YYBW##` (e.g., `26BW01`, `26BW02`) - used in cycle calendar
- **Example**: `26C01W04_26_01_27`
- **Breakdown**:
  - `26` = Year (2026)
  - `C` = Calendar indicator
  - `01` = Month (January)
  - `W04` = Week number (ISO week -1 offset)
  - `_26_01_27` = Date suffix
- **Bi-Weekly Example**: `26BW02` = 2026 Bi-Weekly Report #2 (01/27/26)

**Note**: Folder names continue to use weekly format for consistency. Bi-weekly names are available in the cycle calendar for display/reporting purposes.

### Data Files
- **Full Export**: `YYYY_MM_DD_HH_MM_SS_SCRPA_RMS.csv`
- **7-Day Filter**: `YYYY_MM_DD_HH_MM_SS_SCRPA_RMS_ReportDate_Last7.csv`
- **Briefing**: `SCRPA_Briefing_Ready_YYYY_MM_DD_HH_MM_SS.csv`

---

## Technology Stack

### Languages
- **Python 3.13+** - Core processing scripts
- **Batch Scripts** - Windows automation
- **Power BI** - Data visualization

### Key Libraries
- **pandas** - Data manipulation
- **openpyxl/calamine** - Excel processing
- **Standard Library** - File operations, datetime handling

### Tools
- **Power BI Desktop** - Dashboard creation
- **ChatGPT** - Narrative extraction and briefing generation
- **OneDrive** - File storage and sync

---

## Performance Metrics

### Processing Times (Typical)
- **Excel Conversion**: 5-30 seconds per file
- **Report Generation**: 10-60 seconds
- **File Organization**: 2-5 seconds
- **Total Workflow**: ~1-2 minutes

### File Sizes (Typical)
- **Excel Export**: 1-10 MB
- **CSV Files**: 500 KB - 5 MB
- **HTML Reports**: 100-500 KB
- **PDF Reports**: 200 KB - 1 MB
- **Power BI**: 2-10 MB

---

## Maintenance

### Regular Tasks
- **Weekly**: Run report generation
- **Monthly**: Review archive folder
- **Quarterly**: Update templates and scripts
- **Annually**: Review folder structure and cleanup

### Updates
- **Python pipeline**: `16_Reports\SCRPA\scripts\run_scrpa_pipeline.py` (primary); batch: `Run_SCRPA_Pipeline.bat`
- **Legacy scripts**: `02_ETL_Scripts\SCRPA\`
- **Templates**: Located in `08_Templates\`
- **Canonical documentation**: `16_Reports\SCRPA\Documentation\` (data_dictionary, PROJECT_SUMMARY, claude.md)
- **Project docs**: `16_Reports\SCRPA\doc\`

---

## Known Issues

### ✅ Resolved Issues

#### Report Folder Empty (Fixed in v1.9.2)
- **Status**: Resolved
- **Fixes Applied**:
  - Briefing script: `<nul` stdin redirection so it does not block on input when run from batch
  - Weekly report: Batch-mode detection; reuses existing folder without overwrite prompt in automation
  - Organize script: `<nul` and log redirection to avoid blocking
  - Path case: `generate_all_reports.bat` uses lowercase `scrpa` to match actual folder
  - Logging: "REPORT_DATE format check" → "Passing REPORT_DATE=..."; Step 1/2/3 markers and output in run log
  - WinError 5: Reuse existing report subfolders in batch mode instead of delete/recreate
- **Impact**: Data, Reports, and Documentation now populate correctly in the report folder when running the full workflow.

#### Cycle and Range Data Issue (Fixed in v1.2.0)
- **Status**: Resolved
- **Fixes Applied**:
  - Path case sensitivity corrected (`SCRPA` vs `scrpa`)
  - CSV file fallback support added
  - Archive timing moved to after HTML generation
  - Enhanced DEBUG logging throughout HTML generation
- **Impact**: HTML files now regenerate correctly with accurate cycle and date range information

---

## Success Metrics

### Automation Success
- ✅ Reduced manual steps from 5+ to 1
- ✅ Processing time reduced by 80%
- ✅ Error rate decreased significantly
- ✅ Consistent folder structure and naming
- ✅ Improved error handling and debugging

### User Benefits
- ✅ Easy to use (single batch file)
- ✅ Consistent output format
- ✅ Complete documentation
- ✅ Error recovery and logging
- ✅ Support for both Excel and CSV file formats

### Recent Improvements

#### v2.0.0 (Latest - 2026-02-10)
- ✅ **HTML Auto-Generation Integration**: Pipeline now automatically calls SCRPA_ArcPy to generate fresh HTML reports before copying. Eliminates stale data issues.
- ✅ **Dynamic M Code**: Power BI M code automatically finds latest cycle folder. No more manual path editing.
- ✅ **YAML → JSON Migration**: Replaced YAML with JSON for 7-day summary. Faster, built-in, no external dependencies.
- ✅ **7-Day Counting Bug Fixed**: Crime category breakdown now correctly excludes backfill incidents from 7-Day totals. Lag statistics calculated from actual 7-Day period incidents only.

#### v1.9.4
- ✅ **Documentation streamlining**: Pipeline no longer writes `data_dictionary`, `PROJECT_SUMMARY`, or `claude.md` into each cycle's Documentation folder. Canonical docs live in `16_Reports/SCRPA/Documentation`; update with `generate_documentation.py -o <path>`.
- ✅ **Cycle-only docs**: Each cycle Documentation/ now gets only `SCRPA_Report_Summary.md` (populated from pipeline data), `CHATGPT_BRIEFING_PROMPT.md` (placeholders filled from cycle_info), and `EMAIL_TEMPLATE.txt`.
- ✅ **SCRPA_Report_Summary.md populated**: Total incidents, period counts (7-Day, 28-Day, YTD, Prior Year), lag/backfill counts, lag mean/median/max, and 7-day-by-crime-category table filled from enhanced data and 7-day JSON.
- ✅ **CHATGPT_BRIEFING_PROMPT.md generated**: Pipeline writes per-cycle briefing prompt with cycle ID, bi-weekly, report due, 7-day and bi-weekly date ranges; footer "HPD | SSOCC | SCRPA Report | Cycle: …".

#### v1.9.3
- ✅ **LagDays fix**: `Report_Date_ForLagday` used for LagDays/IsLagDay; lagday tables filter on `Backfill_7Day = TRUE`.
- ✅ **Bi-weekly email and briefing**: Full bi-weekly period and cycle (e.g. 26BW02, 01/13–01/26) in email and ChatGPT prompt.
- ✅ **Crime breakdown script**: `scripts/crime_breakdown_and_lagdays.py` outputs category counts and LagDays; writes to Data/ and Documentation/.
- ✅ **Full-dataset export**: `SCRPA_All_Crimes_Full.csv` added to Data/ when running enriched export.
- ✅ **7-day restructure**: Prefers 2026 cycle calendar; briefing and restructure aligned with bi-weekly.

#### v1.9.2
- ✅ **Report Folder Empty Fix**: Data/Reports/Documentation now populate when running the workflow
  - Briefing/organize scripts no longer block on stdin (`<nul`); weekly report reuses folder in batch mode
  - Path `scrpa` normalized; logging clarified; Step 1/2/3 output and markers in run log; WinError 5 mitigated

#### v1.9.1
- ✅ **Cycle Calendar Gap Fix**: Fixed missing 01/06/2026 entry that created date lookup gap
- ✅ **Validation Logic Fix**: Fixed overly permissive bi-weekly validation to require exact format

#### v1.9.0
- ✅ **Bi-Weekly Reporting Transition**
  - System updated to support bi-weekly reporting (every other week) starting 2026
  - Cycle calendar updated with `BiWeekly_Report_Name` column (26 bi-weekly cycles for 2026)
  - Historical 2025 data preserved with weekly format
  - Power BI M code updated to support bi-weekly cycle detection
  - Scripts updated to use updated cycle calendar file
  - Email template terminology updated: "Weekly Report" → "Bi-Weekly Report"
  - Lagday logic verified correct - works perfectly with bi-weekly cycles
  - Analysis periods (7-Day, 28-Day) remain unchanged - only reporting frequency changed
- ✅ **Cycle Calendar Enhancements**
  - Added `BiWeekly_Report_Name` column to cycle calendar CSV
  - Updated cycle calendar filename: `7Day_28Day_Cycle_20260106.csv`
  - All 26 bi-weekly cycles for 2026 added (01/13/26 through 12/29/26)
- ✅ **M Code Updates**
  - `q_CycleCalendar.m`: Added `BiWeekly_Report_Name` column type definition
  - `Export_Formatting.m`: Updated validation to accept both weekly and bi-weekly formats
  - `all_crimes.m`: Verified correct - no changes needed
- ✅ **Script Updates**
  - Updated `generate_weekly_report.py`, `export_excel_sheets_to_csv.py`, and `export_enriched_data_and_email.py`
  - All scripts now use updated cycle calendar file

#### v1.8.0
- ✅ LagDays calculation bug fix using three-tier approach
- ✅ Standardized code headers added to all M code files
- ✅ Automated email template generation in workflow

#### v1.7.0
- ✅ **Project Structure Reorganization**
  - Organized M code into `m_code/` directory with `archive/` subdirectory
  - Created `preview_tables/` directory for Power BI CSV previews
  - Moved documentation files to `doc/` directory
  - Improved project organization and maintainability
- ✅ **Period Classification Fix**
  - Fixed Period calculation logic to correctly identify 7-Day vs 28-Day periods
  - Improved cycle detection when Today is after cycle end date
  - Added explicit null checks and clearer logic flow
  - Added diagnostic column for troubleshooting Period assignments
- ✅ **Period Label Improvements**
  - Changed "2025 Historical" to "Prior Year" for cleaner, shorter labels
  - Automatically applies to prior year (dynamic, not hardcoded)
- ✅ **Visual Color Scheme Update**
  - Prior Year: `#7F92A2` (gray-blue)
  - YTD: `#118DFF` (blue)
  - 28-Day: `#77C99A` (green)
  - 7-Day: (existing color)
- ✅ **Cycle Calendar Maintenance**
  - Updated filename: `7Day_28Day_Cycle_20260106.csv` (reflecting 2026 data)
  - Updated all M code references to new filename
- ✅ **M Code Quality Improvements**
  - Fixed broken file paths (single continuous strings)
  - Configured VS Code to prevent auto-formatting of M files
  - Improved code organization and maintainability

#### v1.6.0
- ✅ Cycle calendar extended with 2026 entries (all 52 weeks)
- ✅ 7-day CSV filtering now uses cycle calendar for accurate date ranges
  - Fixed to use actual cycle boundaries instead of simple "today - 7 days" calculation
  - Reads REPORT_DATE environment variable and looks up correct cycle dates
  - 7-day filtered CSV files now match cycle calendar dates exactly
- ✅ Excel conversion script enhanced with cycle calendar integration
  - Added cycle calendar lookup function
  - Supports both openpyxl and calamine engines
  - Falls back to simple calculation if cycle calendar lookup fails

#### v1.5.0
- ✅ Zone formatting fixed - displays as whole numbers instead of decimals
- ✅ Date filtering fixed - correctly excludes incidents outside cycle range
  - Fixed in both `prepare_briefing_csv.py` and `scrpa_7day_restructure.py`
  - `scrpa_7day_restructure.py` now uses cycle calendar CSV lookup instead of min/max Report Date
  - Properly excludes incidents from previous cycles based on cycle calendar dates
- ✅ Data Dictionary optimization - stored once in reference location, reused for all reports
- ✅ Enhanced narrative extraction - improved ChatGPT prompt with explicit extraction instructions
- ✅ Documentation cleanup guide - explains which files are needed vs historical notes
- ✅ Documentation file limiting - only essential files copied, historical development notes excluded

#### v1.3.0
- ✅ ChatGPT prompt enhanced with Reporting Parameters section
- ✅ Added explicit Loss And Monetary Rules (5-step calculation process)
- ✅ Added Cycle And Date Rules for consistency
- ✅ Added Summary Table Rules for data alignment
- ✅ CSV data embedded in prompt file (no separate upload needed)
- ✅ Created usage instructions guide

#### v1.2.0
- ✅ Path case sensitivity issues resolved
- ✅ CSV file support added for better compatibility
- ✅ Archive timing optimized to prevent file conflicts
- ✅ Enhanced debugging for easier troubleshooting
- ✅ CHATGPT prompt improvements (removed em dashes, added Loss Total calculation)

---

## Future Roadmap

### Short Term
- Enhanced error handling
- Improved logging
- Config file support

### Medium Term
- Web interface
- Automated scheduling
- Email distribution

### Long Term
- Database integration
- Real-time updates
- Advanced analytics

---

## Contact & Support

**System Owner**: R. A. Carucci  
**Department**: City of Hackensack Police Department  
**Last Updated**: February 10, 2026

---

**Version**: 2.0.0  
**Status**: Production  
**License**: Internal Use Only

