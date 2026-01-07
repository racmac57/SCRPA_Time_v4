# SCRPA Reporting System - Summary

**Strategic Crime Reduction and Problem Analysis (SCRPA) Automated Reporting Workflow**

---

## System Purpose

The SCRPA Reporting System automates the weekly generation of crime analysis reports from RMS data exports. It transforms raw Excel exports into organized, structured reports with Power BI dashboards, HTML/PDF summaries, and ChatGPT-ready briefing formats.

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

```
┌─────────────────────────────────────────────────────────────┐
│                    SCRPA REPORT WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

1. Excel Export
   └─> 05_EXPORTS\_RMS\scrpa\*.xlsx
       │
       ├─> convert_all_xlsx.bat
       │   └─> CSV Files (*.csv, *_ReportDate_Last7.csv)
       │
       └─> prepare_briefing_csv.py
           └─> SCRPA_Briefing_Ready_*.csv

2. Run Automation
   └─> Run_SCRPA_Report_Folder.bat
       │
       ├─> STEP 1: generate_weekly_report.py
       │   └─> Creates folder structure
       │   └─> Copies Power BI template
       │
       ├─> STEP 2: generate_all_reports.bat
       │   └─> Generates HTML/PDF reports
       │
       ├─> STEP 3: organize_report_files.py
       │   └─> Copies files to report folder
       │   └─> Creates documentation
       │
       └─> STEP 4: Opens year folder

3. Report Folder
   └─> 16_Reports\SCRPA\Time_Based\2025\25C12W49_25_12_09\
       ├─> Data/          (CSV files)
       ├─> Reports/       (HTML/PDF)
       └─> Documentation/ (MD files)
```

---

## File Types and Locations

### Input Files
- **Excel Exports**: `05_EXPORTS\_RMS\scrpa\*.xlsx`
- **Templates**: `15_Templates\Base_Report.pbix`

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
- **Pattern**: `YYCMMWww_YY_MM_DD`
- **Example**: `25C12W49_25_12_09`
- **Breakdown**:
  - `25` = Year (2025)
  - `C` = Calendar indicator
  - `12` = Month (December)
  - `W49` = Week number (ISO week -1 offset)
  - `_25_12_09` = Date suffix

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
- **Scripts**: Located in `02_ETL_Scripts\SCRPA\`
- **Templates**: Located in `15_Templates\`
- **Documentation**: Located in `16_Reports\SCRPA\doc\`

---

## Known Issues

### ✅ Resolved Issues

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

#### v1.7.0 (Latest)
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
**Last Updated**: January 6, 2026

---

**Version**: 1.7.0  
**Status**: Production  
**License**: Internal Use Only

