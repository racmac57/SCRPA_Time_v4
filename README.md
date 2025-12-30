# SCRPA Reporting System

**Strategic Crime Reduction and Problem Analysis (SCRPA) Automated Reporting Workflow**

---

## Overview

The SCRPA Reporting System automates the generation of weekly crime analysis reports from RMS (Records Management System) data exports. The system processes Excel exports, converts them to CSV, generates Power BI dashboards, creates HTML/PDF reports, and organizes all files into a structured folder hierarchy.

---

## Quick Start

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
├── Time_Based\
│   └── 2025\
│       └── 25C12W49_25_12_09\          # Report folder (date-based)
│           ├── 25C12W49_25_12_09.pbix  # Power BI template
│           ├── Data\                    # CSV files
│           ├── Reports\                 # HTML and PDF files
│           └── Documentation\           # Markdown files and prompts
├── doc\                                  # System documentation
├── README.md                             # This file
├── CHANGELOG.md                          # Version history
└── SUMMARY.md                            # System summary
```

---

## Report Naming Convention

Reports follow this naming pattern:
- **Format**: `YYCMMWww_YY_MM_DD`
- **Example**: `25C12W49_25_12_09`
  - `25` = Year (2025)
  - `C` = Calendar
  - `12` = Month (December)
  - `W49` = Week number (with -1 offset)
  - `_25_12_09` = Date suffix (YY_MM_DD)

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
- **`generate_weekly_report.py`** - Creates folder structure and copies template
- **`organize_report_files.py`** - Organizes files into report folder
- **`generate_all_reports.bat`** - Generates HTML/PDF reports

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
- **`CHATGPT_BRIEFING_PROMPT.md`** - Complete prompt for ChatGPT (includes embedded CSV data)
- **`CHATGPT_USAGE_INSTRUCTIONS.md`** - Quick reference guide for using ChatGPT prompt
- **`SCRPA_Report_Summary.md`** - Consolidated report summary
- **`CHATGPT_PROMPT_GUIDE.md`** - Detailed usage guide

---

## Configuration

### Paths
- **Reports Base**: `16_Reports\SCRPA\Time_Based\`
- **Template Source**: `15_Templates\Base_Report.pbix`
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

### Access Denied Errors
- **Cause**: OneDrive sync conflicts
- **Solution**: Wait for sync to complete, or close OneDrive temporarily

### Missing CSV Files
- **Cause**: Excel file archived before conversion
- **Solution**: Check `archive\` folder and manually convert if needed

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

#### Cycle and Range Data Issue (Fixed in v1.2.0)
- **Status**: Fixed
- **Solution**: Added CSV fallback support, fixed path case sensitivity, moved archive timing, enhanced debugging
- **See**: `docs/CYCLE_FIX_SOLUTION.md` for details

---

## Recent Updates

### v1.4.0 (Latest)
- ✅ **Zone Formatting Fix**: Zone values now display as whole numbers (5, 8) instead of decimals (5.0, 8.0)
- ✅ **Date Filtering Fix**: Incidents outside cycle date range are now correctly excluded
- ✅ **Data Dictionary Optimization**: Dictionary now stored once in reference location and reused for all reports
- ✅ **Enhanced Narrative Extraction**: Improved ChatGPT prompt with explicit narrative extraction instructions
- ✅ **Documentation Cleanup Guide**: Created guide explaining which documentation files are needed vs historical

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

**Current Version**: 1.4.0  
**Last Updated**: December 29, 2025  
**Maintained By**: R. A. Carucci

---

## License

Internal use only - City of Hackensack Police Department

