01/06/2026  0:04:00.16 - Starting SCRPA workflow automation...
01/06/2026  0:04:01.04 - Checking Python availability...
01/06/2026  0:04:01.82 - Python cmd : py -3
01/06/2026  0:04:01.83 - Python path: C:\Users\carucci_r\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe
01/06/2026  0:04:01.85 - Python ver : Python 3.13.9

Enter REPORT DATE [MM/DD/YYYY] (default 01/06/2026): 01/06/2026
01/06/2026  0:04:13.52 - REPORT_DATE = 01/06/2026 (normalized)
01/06/2026  0:04:13.54 - Creating year folder: C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026
01/06/2026  0:04:13.55 - [OK] Year folder ready
01/06/2026  0:04:14.27 - STEP 0 - Sanity checks
01/06/2026  0:04:14.28 - Listing C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA:
01/06/2026  0:04:14.29 - Listing C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\06_Output:
01/06/2026  0:04:14.31 - [OK] Required scripts found
01/06/2026  0:04:14.32 - STEP 0.5: CONVERT EXCEL FILES TO CSV
01/06/2026  0:04:14.33 - Changing to directory: C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa
01/06/2026  0:04:14.35 - Current directory: C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa
01/06/2026  0:04:14.36 - Running Excel to CSV conversion (auto): C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\convert_all_xlsx_auto.bat
01/06/2026  0:04:18.62 - [OK] Excel conversion completed
01/06/2026  0:04:18.64 - STEP 1: CREATE/SEED WEEKLY INPUTS
01/06/2026  0:04:18.66 - Changing to directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA
01/06/2026  0:04:18.68 - Current directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA
01/06/2026  0:04:18.69 - Running weekly script with REPORT_DATE=01/06/2026
--- SCRPA Report Generator ---
[WARNING] No cycle found for Report_Due_Date: 01/06/2026
[WARNING] Using fallback calculation method - cycle calendar lookup failed

Processing for Year: 2026
Target Path:         C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06
New File Name:       26C01W01_26_01_06.pbix
[SUCCESS] Verified/Created folder structure.
[SUCCESS] Created subfolders: Data/, Reports/, Documentation/
[SUCCESS] Template copied and renamed: 26C01W01_26_01_06.pbix

Done.
01/06/2026  0:04:23.11 - [OK] Weekly script completed
01/06/2026  0:04:23.12 - STEP 2: RUN FULL REPORT GENERATION
01/06/2026  0:04:23.14 - Changing to directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\06_Output
01/06/2026  0:04:23.15 - Current directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\06_Output
01/06/2026  0:04:23.16 - Running child batch (env REPORT_DATE=01/06/2026): C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\generate_all_reports.bat
01/06/2026  0:04:29.06 - [OK] STEP 2 completed
01/06/2026  0:04:29.08 - STEP 3: ORGANIZE FILES INTO REPORT FOLDER
01/06/2026  0:04:29.11 - Changing to directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA
01/06/2026  0:04:29.13 - Current directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA
01/06/2026  0:04:29.17 - Running: py -3 "C:\Users\carucci_r\OneDrive
============================================================
SCRPA REPORT FILE ORGANIZATION
============================================================

✅ Found latest report folder: 26C01W01_26_01_06

📁 Organizing files into: 26C01W01_26_01_06

📅 Report date detected: 2026-01-06 (from folder name)
📊 Copying CSV files to Data/ folder...
⚠️  No CSV files found matching date 2026-01-06
   Found 0 total CSV file(s), but none match the report date
   Note: Excel files must be converted to CSV first using convert_all_xlsx.bat

📊 Copying Excel files to Data/ folder...
⚠️  No Excel files found matching date 2026-01-06
   Found 27 total Excel file(s), but none match the report date
⚠️  No briefing CSV found matching date 2026-01-06, using latest available
✅ Found briefing CSV: SCRPA_Briefing_Ready_2025_12_30_00_34_17.csv

📋 Copying briefing CSV...
  ✓ Copied: SCRPA_Briefing_Ready_2025_12_30_00_34_17.csv

🧹 Removing 1 old briefing CSV file(s) that don't match report date...
  ✓ Removed: SCRPA_Briefing_Ready_2025_12_30_00_34_17.csv

🧹 Cleaning up old report files...

📄 Copying HTML and PDF reports...
📄 Found 2 report file(s) to copy (latest versions only)
  ✓ Copied: 2026_01_06_00_04_28_rms_summary.html
  ✓ Copied: SCRPA_Combined_Executive_Summary_20251230_003415.html
⚠️  Found ChatGPT prompt: CHATGPT_BRIEFING_PROMPT.md (may be from different date)
   Report date: 2026-01-06
   Prompt file may need to be regenerated for this report date

📝 Copying ChatGPT prompt...
  ✓ Copied: CHATGPT_BRIEFING_PROMPT.md

📚 Copying essential documentation files...
   ℹ️  Guide files (CHATGPT_PROMPT_GUIDE.md, SCRPA_WORKFLOW_USER_GUIDE.md) are not copied
      These are optional reference guides, not needed for report generation
      Only CHATGPT_BRIEFING_PROMPT.md and SCRPA_Report_Summary.md are essential in Documentation/

📝 Creating consolidated markdown file...
✅ Created consolidated MD file: SCRPA_Report_Summary.md

✅ File organization complete! 5 file(s) copied/organized.

============================================================
✅ FILE ORGANIZATION COMPLETE
============================================================

📂 Report Folder: C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06

📁 Folder Structure:
   ├── Data/          (CSV files)
   ├── Reports/      (HTML and PDF files)
   └── Documentation/ (MD files and prompts)

============================================================

Press Enter to exit...