# SCRPA workflow automation output review
_Exported on 1/6/2026 at 00:56:10 EST from Cursor (2.3.21)_

---

**User**

I ran the C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Run_SCRPA_Report_Folder.bat and got below message: Does the output look correct?
C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06


01/06/2026  0:35:48.56 - Starting SCRPA workflow automation...
01/06/2026  0:35:48.90 - Checking Python availability...
01/06/2026  0:35:49.55 - Python cmd : py -3
01/06/2026  0:35:49.56 - Python path: C:\Users\carucci_r\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe
01/06/2026  0:35:49.57 - Python ver : Python 3.13.9

Enter REPORT DATE [MM/DD/YYYY] (default 01/06/2026): 01/06/2026
01/06/2026  0:35:57.42 - REPORT_DATE = 01/06/2026 (normalized)
01/06/2026  0:35:57.44 - Year folder exists: C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026
01/06/2026  0:35:57.65 - STEP 0 - Sanity checks
01/06/2026  0:35:57.67 - Listing C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA:
01/06/2026  0:35:57.68 - Listing C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\06_Output:
01/06/2026  0:35:57.70 - [OK] Required scripts found
01/06/2026  0:35:57.71 - STEP 0.5: CONVERT EXCEL FILES TO CSV
01/06/2026  0:35:57.73 - Changing to directory: C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa
01/06/2026  0:35:57.75 - Current directory: C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa
01/06/2026  0:35:57.76 - Running Excel to CSV conversion (auto): C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\convert_all_xlsx_auto.bat
01/06/2026  0:36:00.96 - [OK] Excel conversion completed
01/06/2026  0:36:00.97 - STEP 1: CREATE/SEED WEEKLY INPUTS
01/06/2026  0:36:00.99 - Changing to directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA
01/06/2026  0:36:01.00 - Current directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA
01/06/2026  0:36:01.01 - Running weekly script with REPORT_DATE=01/06/2026
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
01/06/2026  0:36:02.20 - [OK] Weekly script completed
01/06/2026  0:36:02.21 - STEP 2: RUN FULL REPORT GENERATION
01/06/2026  0:36:02.22 - Changing to directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\06_Output
01/06/2026  0:36:02.23 - Current directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\06_Output
01/06/2026  0:36:02.24 - Running child batch (env REPORT_DATE=01/06/2026): C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\generate_all_reports.bat
01/06/2026  0:36:06.98 - [OK] STEP 2 completed
01/06/2026  0:36:06.99 - STEP 3: ORGANIZE FILES INTO REPORT FOLDER
01/06/2026  0:36:07.01 - Changing to directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA
01/06/2026  0:36:07.02 - Current directory: C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA
01/06/2026  0:36:07.06 - Running: py -3 "C:\Users\carucci_r\OneDrive
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
📊 Found 2 Excel file(s) matching report date 2026-01-06
  ✓ Copied: 2026_01_06_00_33_09_SCRPA_RMS.xlsx
  ✓ Copied: 2026_01_06_00_33_09_SCRPA_RMS_20260106_003600.xlsx
⚠️  No briefing CSV found matching date 2026-01-06, using latest available
✅ Found briefing CSV: SCRPA_Briefing_Ready_2025_12_30_00_34_17.csv

📋 Copying briefing CSV...
  ✓ Copied: SCRPA_Briefing_Ready_2025_12_30_00_34_17.csv

🧹 Removing 1 old briefing CSV file(s) that don't match report date...
  ✓ Removed: SCRPA_Briefing_Ready_2025_12_30_00_34_17.csv

🧹 Cleaning up old report files...

📄 Copying HTML and PDF reports...
📄 Found 2 report file(s) to copy (latest versions only)
  ✓ Copied: 2026_01_06_00_36_06_rms_summary.html
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

✅ File organization complete! 7 file(s) copied/organized.

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

---

**Cursor**


Reviewing the output folder to verify the generated files and identify any issues.



Checking the cycle calendar and file organization script:



Checking the file organization script and searching for the cycle calendar:



Checking the cycle calendar file and locating the file organization script:



Reviewing the file organization script and checking generated files:



Checking for CSV files and reviewing the generated report:



## Summary

The workflow completed, but there are issues to address:

### What worked
1. Folder structure created: `26C01W01_26_01_06`
2. Excel files copied: Both Excel files for 2026-01-06 are in `Data/`
3. Tactical report generated: `2026_01_06_00_36_06_rms_summary.html` is correct
4. File organization completed: 7 files copied

### Issues found

1. Cycle calendar missing 2026 entries
   - Warning: `[WARNING] No cycle found for Report_Due_Date: 01/06/2026`
   - Cause: The cycle calendar CSV (`7Day_28Day_Cycle_20250414.csv`) only goes through 12/30/2025
   - Impact: Script falls back to calculated cycle name (which worked: `26C01W01`)
   - Action needed: Add 2026 entries to the cycle calendar CSV

2. Briefing CSV from wrong date
   - Found: `SCRPA_Briefing_Ready_2025_12_30_00_34_17.csv` (from 12/30/2025)
   - Expected: A briefing CSV for 2026-01-06
   - Cause: No briefing CSV was generated for this report date
   - Action needed: Run `prepare_briefing_csv.py` for 2026-01-06

3. Strategic HTML report from wrong date
   - Found: `SCRPA_Combined_Executive_Summary_20251230_003415.html` (from 12/30/2025)
   - Expected: A strategic report for 2026-01-06
   - Cause: Strategic report generation didn't run or failed for this date
   - Action needed: Verify strategic report generation step

4. No CSV files found
   - Warning: `No CSV files found matching date 2026-01-06`
   - Cause: Excel files were converted but CSVs may have been archived or not created
   - Note: Excel files are present, so this may be acceptable

### Recommendations

1. Update the cycle calendar: Add 2026 entries to `09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20250414.csv`
2. Generate briefing CSV: Run the briefing preparation step for 2026-01-06
3. Verify strategic report generation: Check why the strategic report wasn't generated for 2026-01-06

The output is mostly correct, but the cycle calendar needs updating and the briefing/strategic reports need to be generated for the new year. Should I help update the cycle calendar or investigate why the briefing/strategic reports weren't generated?

---

**User**

The date range is off there is no filtered 7-day csv.  do you have the logic to contine the pattern for the cycle. actually we made it already C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\26_scrpa_cycle.txt

---

**Cursor**


Reading the 2026 cycle file and updating the cycle calendar CSV with 2026 entries. Checking why the 7-day filtered CSV wasn't created.



Converting the 2026 cycle data to the CSV format and appending it. Checking how the Excel conversion script uses the cycle calendar to understand why the 7-day CSV wasn't created.



Updating the cycle calendar CSV with 2026 entries. Checking the Excel conversion script to see how it uses the cycle calendar:



Updating the cycle calendar CSV with 2026 entries. Converting dates from 2-digit to 4-digit years and adding the "26" prefix to Report_Name.


```csv
Report_Due_Date,7_Day_Start,7_Day_End,28_Day_Start,28_Day_End,Report_Name
01/07/2025,12/31/2024,01/06/2025,12/10/2024,01/06/2025,25C01W01
01/14/2025,01/07/2025,01/13/2025,12/17/2024,01/13/2025,25C01W02
01/21/2025,01/14/2025,01/20/2025,12/24/2024,01/20/2025,25C01W03
01/28/2025,01/21/2025,01/27/2025,12/31/2024,01/27/2025,25C01W04
02/04/2025,01/28/2025,02/03/2025,01/07/2025,02/03/2025,25C02W05
02/11/2025,02/04/2025,02/10/2025,01/14/2025,02/10/2025,25C02W06
02/18/2025,02/11/2025,02/17/2025,01/21/2025,02/17/2025,25C02W07
02/25/2025,02/18/2025,02/24/2025,01/28/2025,02/24/2025,25C02W08
03/04/2025,02/25/2025,03/03/2025,02/04/2025,03/03/2025,25C03W09
03/11/2025,03/04/2025,03/10/2025,02/11/2025,03/10/2025,25C03W10
03/18/2025,03/11/2025,03/17/2025,02/18/2025,03/17/2025,25C03W11
03/25/2025,03/18/2025,03/24/2025,02/25/2025,03/24/2025,25C03W12
04/01/2025,03/25/2025,03/31/2025,03/04/2025,03/31/2025,25C04W13
04/08/2025,04/01/2025,04/07/2025,03/11/2025,04/07/2025,25C04W14
04/15/2025,04/08/2025,04/14/2025,03/18/2025,04/14/2025,25C04W15
04/22/2025,04/15/2025,04/21/2025,03/25/2025,04/21/2025,25C04W16
04/29/2025,04/22/2025,04/28/2025,04/01/2025,04/28/2025,25C05W17
05/06/2025,04/29/2025,05/05/2025,04/08/2025,05/05/2025,25C05W18
05/13/2025,05/06/2025,05/12/2025,04/15/2025,05/12/2025,25C05W19
05/20/2025,05/13/2025,05/19/2025,04/22/2025,05/19/2025,25C05W20
05/27/2025,05/20/2025,05/26/2025,04/29/2025,05/26/2025,25C06W21
06/03/2025,05/27/2025,06/02/2025,05/06/2025,06/02/2025,25C06W23
06/10/2025,06/03/2025,06/09/2025,05/13/2025,06/09/2025,25C06W23
06/17/2025,06/10/2025,06/16/2025,05/20/2025,06/16/2025,25C06W24
06/24/2025,06/17/2025,06/23/2025,05/27/2025,06/23/2025,25C07W25
07/01/2025,06/24/2025,06/30/2025,06/03/2025,06/30/2025,25C07W26
07/08/2025,07/01/2025,07/07/2025,06/10/2025,07/07/2025,25C07W27
07/15/2025,07/08/2025,07/14/2025,06/17/2025,07/14/2025,25C07W28
07/22/2025,07/15/2025,07/21/2025,06/24/2025,07/21/2025,25C08W29
07/29/2025,07/22/2025,07/28/2025,07/01/2025,07/28/2025,25C08W30
08/05/2025,07/29/2025,08/04/2025,07/08/2025,08/04/2025,25C08W31
08/12/2025,08/05/2025,08/11/2025,07/15/2025,08/11/2025,25C08W32
08/19/2025,08/12/2025,08/18/2025,07/22/2025,08/18/2025,25C09W33
08/26/2025,08/19/2025,08/25/2025,07/29/2025,08/25/2025,25C09W34
09/02/2025,08/26/2025,09/01/2025,08/05/2025,09/01/2025,25C09W35
09/09/2025,09/02/2025,09/08/2025,08/12/2025,09/08/2025,25C09W36
09/16/2025,09/09/2025,09/15/2025,08/19/2025,09/15/2025,25C10W37
09/23/2025,09/16/2025,09/22/2025,08/26/2025,09/22/2025,25C10W38
09/30/2025,09/23/2025,09/29/2025,09/02/2025,09/29/2025,25C10W39
10/07/2025,09/30/2025,10/06/2025,09/09/2025,10/06/2025,25C10W40
10/14/2025,10/07/2025,10/13/2025,09/16/2025,10/13/2025,25C11W41
10/21/2025,10/14/2025,10/20/2025,09/23/2025,10/20/2025,25C11W42
10/28/2025,10/21/2025,10/27/2025,09/30/2025,10/27/2025,25C11W43
11/04/2025,10/28/2025,11/03/2025,10/07/2025,11/03/2025,25C11W44
11/11/2025,11/04/2025,11/10/2025,10/14/2025,11/10/2025,25C12W45
11/18/2025,11/11/2025,11/17/2025,10/21/2025,11/17/2025,25C12W46
11/25/2025,11/18/2025,11/24/2025,10/28/2025,11/24/2025,25C12W47
12/02/2025,11/25/2025,12/01/2025,11/04/2025,12/01/2025,25C12W48
12/09/2025,12/02/2025,12/08/2025,11/11/2025,12/08/2025,25C13W49
12/16/2025,12/09/2025,12/15/2025,11/18/2025,12/15/2025,25C13W50
12/23/2025,12/16/2025,12/22/2025,11/25/2025,12/22/2025,25C13W51
12/30/2025,12/23/2025,12/29/2025,12/02/2025,12/29/2025,25C13W52
01/06/2026,12/30/2025,01/05/2026,12/09/2025,01/05/2026,26C01W01
01/13/2026,01/06/2026,01/12/2026,12/16/2025,01/12/2026,26C01W02
01/20/2026,01/13/2026,01/19/2026,12/23/2025,01/19/2026,26C01W03
01/27/2026,01/20/2026,01/26/2026,12/30/2025,01/26/2026,26C01W04
02/03/2026,01/27/2026,02/02/2026,01/06/2026,02/02/2026,26C02W05
02/10/2026,02/03/2026,02/09/2026,01/13/2026,02/09/2026,26C02W06
02/17/2026,02/10/2026,02/16/2026,01/20/2026,02/16/2026,26C02W07
02/24/2026,02/17/2026,02/23/2026,01/27/2026,02/23/2026,26C02W08
03/03/2026,02/24/2026,03/02/2026,02/03/2026,03/02/2026,26C03W09
03/10/2026,03/03/2026,03/09/2026,02/10/2026,03/09/2026,26C03W10
03/17/2026,03/10/2026,03/16/2026,02/17/2026,03/16/2026,26C03W11
03/24/2026,03/17/2026,03/23/2026,02/24/2026,03/23/2026,26C03W12
03/31/2026,03/24/2026,03/30/2026,03/03/2026,03/30/2026,26C04W13
04/07/2026,03/31/2026,04/06/2026,03/10/2026,04/06/2026,26C04W14
04/14/2026,04/07/2026,04/13/2026,03/17/2026,04/13/2026,26C04W15
04/21/2026,04/14/2026,04/20/2026,03/24/2026,04/20/2026,26C04W16
04/28/2026,04/21/2026,04/27/2026,03/31/2026,04/27/2026,26C05W17
05/05/2026,04/28/2026,05/04/2026,04/07/2026,05/04/2026,26C05W18
05/12/2026,05/05/2026,05/11/2026,04/14/2026,05/11/2026,26C05W19
05/19/2026,05/12/2026,05/18/2026,04/21/2026,05/18/2026,26C05W20
05/26/2026,05/19/2026,05/25/2026,04/28/2026,05/25/2026,26C06W21
06/02/2026,05/26/2026,06/01/2026,05/05/2026,06/01/2026,26C06W22
06/09/2026,06/02/2026,06/08/2026,05/12/2026,06/08/2026,26C06W23
06/16/2026,06/09/2026,06/15/2026,05/19/2026,06/15/2026,26C06W24
06/23/2026,06/16/2026,06/22/2026,05/26/2026,06/22/2026,26C07W25
06/30/2026,06/23/2026,06/29/2026,06/02/2026,06/29/2026,26C07W26
07/07/2026,06/30/2026,07/06/2026,06/09/2026,07/06/2026,26C07W27
07/14/2026,07/07/2026,07/13/2026,06/16/2026,07/13/2026,26C07W28
07/21/2026,07/14/2026,07/20/2026,06/23/2026,07/20/2026,26C08W29
07/28/2026,07/21/2026,07/27/2026,06/30/2026,07/27/2026,26C08W30
08/04/2026,07/28/2026,08/03/2026,07/07/2026,08/03/2026,26C08W31
08/11/2026,08/04/2026,08/10/2026,07/14/2026,08/10/2026,26C08W32
08/18/2026,08/11/2026,08/17/2026,07/21/2026,08/17/2026,26C09W33
08/25/2026,08/18/2026,08/24/2026,07/28/2026,08/24/2026,26C09W34
09/01/2026,08/25/2026,08/31/2026,08/04/2026,08/31/2026,26C09W35
09/08/2026,09/01/2026,09/07/2026,08/11/2026,09/07/2026,26C09W36
09/15/2026,09/08/2026,09/14/2026,08/18/2026,09/14/2026,26C10W37
09/22/2026,09/15/2026,09/21/2026,08/25/2026,09/21/2026,26C10W38
09/29/2026,09/22/2026,09/28/2026,09/01/2026,09/28/2026,26C10W39
10/06/2026,09/29/2026,10/05/2026,09/08/2026,10/05/2026,26C10W40
10/13/2026,10/06/2026,10/12/2026,09/15/2026,10/12/2026,26C11W41
10/20/2026,10/13/2026,10/19/2026,09/22/2026,10/19/2026,26C11W42
10/27/2026,10/20/2026,10/26/2026,09/29/2026,10/26/2026,26C11W43
11/03/2026,10/27/2026,11/02/2026,10/06/2026,11/02/2026,26C11W44
11/10/2026,11/03/2026,11/09/2026,10/13/2026,11/09/2026,26C12W45
11/17/2026,11/10/2026,11/16/2026,10/20/2026,11/16/2026,26C12W46
11/24/2026,11/17/2026,11/23/2026,10/27/2026,11/23/2026,26C12W47
12/01/2026,11/24/2026,11/30/2026,11/03/2026,11/30/2026,26C12W48
12/08/2026,12/01/2026,12/07/2026,11/10/2026,12/07/2026,26C13W49
12/15/2026,12/08/2026,12/14/2026,11/17/2026,12/14/2026,26C13W50
12/22/2026,12/15/2026,12/21/2026,11/24/2026,12/21/2026,26C13W51
12/29/2026,12/22/2026,12/28/2026,12/01/2026,12/28/2026,26C13W52

```


Appending 2026 entries to the cycle calendar CSV:



The cycle calendar CSV already includes 2026 entries (lines 54-105). The dates are in MM/DD/YYYY format and Report_Name includes the "26" prefix.

Since the cycle calendar is updated, the missing 7-day filtered CSV is likely because:
1. The Excel conversion ran before the calendar was updated, so it couldn't find the cycle for 01/06/2026.
2. The conversion script needs the cycle calendar to determine the date range for the 7-day filter.

**Next steps:**
1. Re-run the Excel conversion step now that the cycle calendar has 2026 entries. This should create the `*_ReportDate_Last7.csv` file.
2. Re-run the full workflow to regenerate the briefing CSV and strategic report for 2026-01-06.

The cycle calendar is correct. For 01/06/2026:
- **Report_Due_Date**: 01/06/2026
- **7-Day Range**: 12/30/2025 to 01/05/2026
- **28-Day Range**: 12/09/2025 to 01/05/2026
- **Cycle Name**: 26C01W01

Should I check the Excel conversion script to see how it uses the cycle calendar, or do you want to re-run the conversion step first?

---

**User**

check before we run

---

**Cursor**


Checking how the Excel conversion script uses the cycle calendar to understand why the 7-day filtered CSV wasn't created.



Locating and reading the Excel conversion script to see how it uses the cycle calendar:



Reading the relevant sections of the Excel conversion script:



Searching for where the script filters the last 7 days:



Found the issue. The `_write_last7_by_reportdate_csv` function (lines 608-639) uses a simple "last 7 days from today" calculation instead of the cycle calendar:

```python
today = datetime.now().date()
start_date = today - timedelta(days=7)
```

This doesn't use the cycle calendar, so it filters the last 7 days from today rather than the cycle's 7-day range.

Checking if the script can access the cycle calendar or if we need to modify it:


```python
today = datetime.now().date()
start_date = today - timedelta(days=7)
```


## Issue found

The `export_excel_sheets_to_csv.py` script does not use the cycle calendar. The `_write_last7_by_reportdate_csv` function (lines 608-639) uses a simple "last 7 days from today" calculation:

```python
today = datetime.now().date()
start_date = today - timedelta(days=7)  # ❌ Not using cycle calendar!
```

This means:
- It filters the last 7 days from today, not the cycle's 7-day range
- It ignores the cycle calendar, even though 2026 entries are present
- For 01/06/2026, it would filter 12/30/2025-01/06/2026 (today - 7 days) instead of the cycle range 12/30/2025-01/05/2026

## What needs to be fixed

The script should:
1. Check for a `REPORT_DATE` environment variable (already set by the batch file)
2. Use the cycle calendar to look up the correct 7-day range for that date
3. Filter using the cycle's `7_Day_Start` and `7_Day_End` dates instead of "today - 7 days"

## Current status

- Cycle calendar: updated with 2026 entries
- Export script: needs modification to use the cycle calendar

Should I update `export_excel_sheets_to_csv.py` to use the cycle calendar for the 7-day filter? This will ensure it uses the correct cycle boundaries instead of a simple "today - 7 days" calculation.

```python
today = datetime.now().date()
start_date = today - timedelta(days=7)  # ❌ Not using cycle calendar!
```

---

**User**

yes update and then  run it

---

**Cursor**


Updating the script to use the cycle calendar, then running it.



Updating the export script to use the cycle calendar:


```python
# export_excel_sheets_to_csv.py
# Changes: Added --all-sheets flag, timeouts, custom exceptions, JSON logging, tqdm progress, streaming writer

import argparse
import os
import re
import json
import hashlib
import time
import psutil
import shutil
from pathlib import Path
from datetime import datetime, time as dtime, date, timedelta as dtdelta
import fnmatch
import csv
import logging
import signal
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=UserWarning, module="dateutil.parser")

from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries, get_column_letter
from openpyxl.utils import column_index_from_string
import pandas as pd

# Custom Exceptions
class ExportTimeoutError(Exception):
    pass

class ExportError(Exception):
    pass

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('export_log.json')
handler.setFormatter(logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'))
logger.addHandler(handler)

# Timeout Handler (Windows compatible)
import threading
import time

def timeout_handler(timeout_seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)
            
            if thread.is_alive():
                raise ExportTimeoutError(f"Export timed out after {timeout_seconds} seconds")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        return wrapper
    return decorator

BASE_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack"
OUT_SUBFOLDER_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack\14_Excel\xlsx_to_csv"

# Archive configuration
ARCHIVE_BASE = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS")
RMS_ARCHIVE = ARCHIVE_BASE / "_RMS" / "SCRPA" / "archive"
CAD_ARCHIVE = ARCHIVE_BASE / "_CAD" / "SCRPA" / "archive"

_TIME_RE = re.compile(r"^\s*\d{1,2}:\d{2}(:\d{2})?\s*$")

def get_archive_folder(filepath: Path) -> Path:
    """Determine archive folder based on file path (CAD or RMS)"""
    folder = CAD_ARCHIVE if "_CAD" in str(filepath) else RMS_ARCHIVE
    folder.mkdir(parents=True, exist_ok=True)
    
    # Extract date from filename if present, else use today
    date_match = re.search(r"(\d{4}[-_]\d{2}[-_]\d{2})|(\d{8})", filepath.name)
    if date_match:
        date_str = date_match.group(0).replace("_", "-")
        # Normalize to YYYY-MM-DD format
        if len(date_str) == 8:  # YYYYMMDD
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    dated_folder = folder / date_str
    dated_folder.mkdir(exist_ok=True)
    return dated_folder

def archive_old_files(folder: Path, dry_run: bool = False, exclude_file: str = None):
    """Archive old .xlsx and .csv files from the working directory
    
    Args:
        folder: Directory to archive files from
        dry_run: If True, only show what would be archived
        exclude_file: Path to file to exclude from archiving (e.g., file being processed)
    """
    if not folder.exists():
        logger.info(f"Archive folder does not exist: {folder}")
        return 0
    
    script_name = Path(__file__).name
    archive_count = 0
    files_to_archive = []
    
    # Normalize exclude_file path for comparison
    exclude_path = None
    if exclude_file:
        exclude_path = Path(exclude_file).resolve()
    
    # Build set of Excel file timestamp prefixes to keep matching CSV files
    excel_timestamps = set()
    try:
        for item in folder.iterdir():
            try:
                if item.is_file() and item.suffix.lower() == ".xlsx" and item.name != script_name:
                    if "archive" not in str(item.parent):
                        # Extract timestamp prefix (format: YYYY_MM_DD_HH_MM_SS_SCRPA_RMS)
                        # CSV files will have same prefix: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                        stem = item.stem  # e.g., "2025_12_02_01_14_15_SCRPA_RMS"
                        excel_timestamps.add(stem)
            except (OSError, PermissionError) as e:
                logger.warning(f"Could not access file {item.name}: {e}")
                continue
    except Exception as e:
        logger.error(f"Error building Excel timestamp set: {e}")
        # Continue anyway - worst case we archive everything
    
    for item in folder.iterdir():
        try:
            if not item.is_file() or item.suffix.lower() not in {".xlsx", ".csv"} or item.name == script_name:
                continue
            
            # Skip files that are already in archive subdirectories
            if "archive" in str(item.parent):
                continue
            
            # Skip the file being processed
            try:
                if exclude_path and item.resolve() == exclude_path:
                    logger.debug(f"Skipping current file from archive: {item.name}")
                    continue
            except (OSError, PermissionError):
                # If we can't resolve the path, skip it
                continue
            
            # For CSV files: keep if they match an existing Excel file timestamp
            if item.suffix.lower() == ".csv":
                try:
                    csv_stem = item.stem
                    # Check if this CSV matches any Excel file timestamp
                    # CSV names: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                    # Excel names: {timestamp}_SCRPA_RMS.xlsx
                    matches_excel = False
                    for excel_stem in excel_timestamps:
                        # Check if CSV stem starts with Excel stem (handles both full CSV and Last7 CSV)
                        if csv_stem.startswith(excel_stem):
                            matches_excel = True
                            break
                    if matches_excel:
                        logger.debug(f"Keeping CSV file (matches Excel): {item.name}")
                        continue
                except Exception as e:
                    logger.warning(f"Error checking CSV file {item.name}: {e}")
                    # If we can't check, err on the side of caution and archive it
                    pass
            
            files_to_archive.append(item)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not process file {item.name}: {e}")
            continue
        except Exception as e:
            logger.warning(f"Unexpected error processing {item.name}: {e}")
            continue
    
    if not files_to_archive:
        logger.info("No files to archive")
        return 0
    
    if dry_run:
        print(f"\n[DRY-RUN] Would archive {len(files_to_archive)} file(s):")
        for item in files_to_archive:
            dest = get_archive_folder(item)
            print(f"  {item.name} -> {dest / item.name}")
        return len(files_to_archive)
    
    for item in files_to_archive:
        try:
            dest = get_archive_folder(item)
            dest_file = dest / item.name
            
            # Handle duplicates by adding timestamp
            if dest_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                stem = dest_file.stem
                suffix = dest_file.suffix
                dest_file = dest / f"{stem}_{timestamp}{suffix}"
            
            shutil.move(str(item), str(dest_file))
            archive_count += 1
            logger.info(f"Archived: {item.name} -> {dest_file}")
        except Exception as e:
            logger.warning(f"Failed to archive {item.name}: {e}")
    
    if archive_count > 0:
        logger.info(f"Archived {archive_count} file(s)")
    
    return archive_count

def sanitize_filename(name: str, used: set) -> str:
    fn = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name).strip().strip('.')
    fn = re.sub(r'[\s_]+', '_', fn)[:150] or "Sheet"
    original = fn
    i = 2
    while fn.lower() in used:
        fn = f"{original}_{i}"
        i += 1
    used.add(fn.lower())
    return fn

def resolve_output_parent(base: str, out_subfolder: str) -> str:
    base_abs = os.path.abspath(base)
    parent = out_subfolder
    if not os.path.isabs(parent):
        parent = os.path.join(base_abs, parent)
    parent = os.path.abspath(parent)
    norm_parent = os.path.normcase(parent)
    norm_base = os.path.normcase(base_abs)
    if not norm_parent.startswith(norm_base):
        raise ValueError(f"Output path must be inside the OneDrive base.\nBase: {base_abs}\nOutput: {parent}")
    return parent

def get_used(ws):
    try:
        dim = ws.calculate_dimension()
    except ValueError:
        # Handle unsized worksheets
        dim = ws.calculate_dimension(force=True)
    
    if dim in ("A1:A1", None):
        return 0, 0
    min_c, min_r, max_c, max_r = range_boundaries(dim)
    return max_r, max_c

def get_file_hash(path):
    if not os.path.exists(path):
        return None
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_adaptive_chunksize(file_size, available_memory):
    memory_threshold = available_memory * 0.5  # Use 50% of available memory
    if file_size > 100 * 1024 * 1024:
        return 1000
    elif file_size > 50 * 1024 * 1024:
        return 2000
    elif file_size > 10 * 1024 * 1024:
        return 5000
    return 10000

def benchmark_engine_performance(file_path, sheet_name, engine, is_detailed=False):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    start_mem = process.memory_info().rss / (1024 * 1024)  # MB
    start_cpu = process.cpu_percent(interval=0.1)

    load_start = time.time()
    if engine == 'calamine':
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
    else:
        wb = load_workbook(file_path, read_only=True, data_only=True)
        ws = wb[sheet_name]
    load_end = time.time()
    load_duration = load_end - load_start

    process_start = time.time()
    if engine == 'calamine':
        for _, row in df.iterrows():
            pass
    else:
        for row in ws.iter_rows():
            pass
    process_end = time.time()
    process_duration = process_end - process_start

    write_start = time.time()
    with open(os.devnull, 'w') as f:
        writer = csv.writer(f)
        if engine == 'calamine':
            for _, row in df.iterrows():
                writer.writerow(row)
        else:
            for row in ws.iter_rows(values_only=True):
                writer.writerow(row)
    write_end = time.time()
    write_duration = write_end - write_start

    end_time = time.time()
    end_mem = process.memory_info().rss / (1024 * 1024)
    end_cpu = process.cpu_percent(interval=0.1)

    total_duration = end_time - start_time
    rows, _ = _get_used_range(df if engine == 'calamine' else ws)
    throughput = rows / total_duration if total_duration > 0 else 0
    mem_peak = max(start_mem, end_mem)
    cpu_avg = (start_cpu + end_cpu) / 2

    results = {
        "total_duration": total_duration,
        "throughput_rows_sec": throughput,
        "memory_peak_mb": mem_peak,
        "cpu_avg_percent": cpu_avg
    }
    if is_detailed:
        results.update({
            "load_duration": load_duration,
            "process_duration": process_duration,
            "write_duration": write_duration,
            "file_size_mb": os.path.getsize(file_path) / (1024 * 1024)
        })
    return results

def _parse_af_columns(spec: str):
    """
    Accept 'A,B,C,D,E,F' or 'A-F' (case-insensitive). Return sorted 1-based column indexes.
    """
    spec = spec.strip().upper().replace(" ", "")
    cols = []
    if "-" in spec and "," not in spec:
        start, end = spec.split("-", 1)
        s = column_index_from_string(start)
        e = column_index_from_string(end)
        if s > e: s, e = e, s
        cols = list(range(s, e + 1))
    else:
        parts = [p for p in spec.split(",") if p]
        for p in parts:
            cols.append(column_index_from_string(p))
    return sorted(set(cols))

def _cell_value_as_text(ws, rr, cc, as_formulas: bool, date_fmt, dt_fmt, t_fmt, force_text=False):
    """
    Shared converter used by the gate: when as_formulas=True, emit '=...' for formula cells,
    else use normal _to_text() logic. 'force_text' only matters in formulas exporter.
    """
    cell = ws.cell(row=rr, column=cc)
    if as_formulas:
        is_formula = (getattr(cell, "data_type", None) == 'f') or (isinstance(cell.value, str) and cell.value.startswith("="))
        if is_formula:
            s = str(cell.value)
            return s if s.startswith("=") else "=" + s
        # fall through to normal text for non-formula
    # call the existing _to_text() in this file
    return _to_text(cell.value, date_fmt, dt_fmt, t_fmt)

def _to_text(value, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S"):
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return value
    # Handle pandas/calamine time-only values that may come as timedelta
    try:
        import pandas as _pd
        if isinstance(value, getattr(_pd, 'Timedelta', ())) or isinstance(value, dtdelta):
            total_seconds = int(value.total_seconds())
            # Normalize to within a day
            total_seconds = total_seconds % (24 * 3600)
            hh = total_seconds // 3600
            mm = (total_seconds % 3600) // 60
            ss = total_seconds % 60
            return f"{hh:02d}:{mm:02d}:{ss:02d}"
    except Exception:
        pass
    if isinstance(value, datetime):
        # If Excel stored a time-only value, the date part is often 1899-12-30
        if value.date().isoformat() == "1899-12-30":
            return value.strftime(t_fmt)
        # If time component is midnight, treat as date-only
        if value.hour == 0 and value.minute == 0 and value.second == 0 and value.microsecond == 0:
            return value.strftime(date_fmt)
        return value.strftime(dt_fmt)
    if isinstance(value, date):
        return value.strftime(date_fmt)
    if isinstance(value, dtime):
        return value.strftime(t_fmt)
    if isinstance(value, str) and _TIME_RE.match(value):
        parts = [int(p) for p in value.strip().split(":")]
        while len(parts) < 3:
            parts.append(0)
        return dtime(parts[0], parts[1], parts[2]).strftime(t_fmt)
    return str(value)

def _get_used_range(data):
    """Get used range for both openpyxl worksheets and pandas DataFrames"""
    if hasattr(data, 'calculate_dimension'):  # openpyxl worksheet
        try:
            dim = data.calculate_dimension()
        except ValueError:
            # Handle unsized worksheets
            dim = data.calculate_dimension(force=True)
        
        if dim in ("A1:A1", None):
            return 0, 0
        min_c, min_r, max_c, max_r = range_boundaries(dim)
        return max_r, max_c
    else:  # pandas DataFrame
        if data.empty:
            return 0, 0
        return len(data), len(data.columns)


def _iter_rows_pandas(df, visible_only, date_fmt, dt_fmt, t_fmt, af_columns, min_af_nonempty, af_gate_visible_only):
    """Iterate over pandas DataFrame rows for calamine engine"""
    af_cols = _parse_af_columns(af_columns)
    max_r, max_c = _get_used_range(df)
    if max_r == 0 or max_c == 0:
        return
    
    # Optionally emit header row when using pandas engine
    if getattr(df, "_include_headers", False):
        yield [str(col) for col in df.columns]

    for r, row in enumerate(df.itertuples(index=False), 1):
        if visible_only:
            # For pandas, we can't easily check row/column visibility
            # This would require additional metadata
            pass
            
        # A-F gate logic
        non_empty = 0
        af_values = []
        for c in af_cols:
            if c < len(row):
                val = row[c]
                af_values.append(val)
                if pd.notna(val) and val != "":
                    non_empty += 1
        
        if non_empty < min_af_nonempty:
            continue
        
        # Convert row to text
        row_out = []
        for val in row:
            formatted_val = _to_text(val, date_fmt, dt_fmt, t_fmt)
            row_out.append(formatted_val)
        
        if row_out and any(v != "" for v in row_out):
            yield row_out

def process_sheet_parallel(sheet_name, xlsx_path, out_dir, args, engine, used_names, benchmark_results, single_csv_basename=None):
    """Process a single sheet in parallel"""
    try:
        # Load sheet data based on engine
        if engine == "openpyxl":
            wb = load_workbook(xlsx_path, read_only=True, data_only=True)
            ws = wb[sheet_name]
            max_r, max_c = _get_used_range(ws)
            is_df = False
        else:  # calamine
            df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
            # Mark to include headers in pandas iteration
            setattr(df, "_include_headers", True)
            max_r, max_c = _get_used_range(df)
            is_df = True
        
        if not args.include_empty and (max_r == 0 or max_c == 0):
            return {"sheet_name": sheet_name, "status": "skipped", "reason": "empty"}
        
        safe = sanitize_filename(sheet_name, used_names)
        # If only one sheet is being exported, use the workbook name for CSV
        if single_csv_basename:
            csv_path = os.path.join(out_dir, f"{single_csv_basename}.csv")
        else:
            csv_path = os.path.join(out_dir, f"{safe}.csv")
        
        # Benchmark this sheet if requested
        if args.benchmark:
            benchmark_start = time.time()
        
        @timeout_handler(300)  # 5 min timeout
        def export_with_timeout():
            if args.engine == "openpyxl":
                return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
            else:  # calamine
                return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
        
        row_count, col_count = export_with_timeout()
        # Optional last-7 CSV for calamine path
        last7_path = None
        if is_df and args.report_last7:
            last7_path = _write_last7_by_reportdate_csv(df, csv_path, args.encoding, args.bom)
        
        # Record benchmark if requested
        if args.benchmark:
            benchmark_end = time.time()
            benchmark_results.append({
                "sheet_name": sheet_name,
                "engine": engine,
                "duration_seconds": round(benchmark_end - benchmark_start, 3),
                "rows": row_count,
                "cols": col_count,
                "rows_per_second": round(row_count / (benchmark_end - benchmark_start), 1) if (benchmark_end - benchmark_start) > 0 else 0
            })
        
        if engine == "openpyxl":
            wb.close()
        
        return {
            "sheet_name": sheet_name,
            "sanitized_name": safe,
            "file": csv_path,
            "file_sha256": get_file_hash(csv_path),
            "rows": row_count,
            "cols": col_count,
            "last7_file": last7_path,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error processing sheet {sheet_name}: {str(e)}")
        return {"sheet_name": sheet_name, "status": "error", "error": str(e)}

def _iter_rows(ws, visible_only: bool, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S", af_columns="A,B,C,D,E,F", min_af_nonempty=4, af_gate_visible_only=False):
    max_r, max_c = get_used(ws)
    merged_top_left = {}
    if hasattr(ws, 'merged_cells') and ws.merged_cells:
        for rng in ws.merged_cells.ranges:
            tl_r, tl_c = rng.min_row, rng.min_col
            for rr in range(rng.min_row, rng.max_row + 1):
                for cc in range(rng.min_col, rng.max_col + 1):
                    merged_top_left[(rr, cc)] = (tl_r, tl_c)
    
    af_cols = _parse_af_columns(af_columns)
    
    for r in tqdm(range(1, max_r + 1), desc="Processing rows"):
        if visible_only and ws.row_dimensions[r].hidden:
            continue
            
        # --- A–F gate (VALUES) ---
        try:
            nonempty = 0
            af_values = []
            for c in af_cols:
                # if visible-only gate, ignore hidden columns
                if af_gate_visible_only and visible_only:
                    col_letter = get_column_letter(c)
                    if ws.column_dimensions[col_letter].hidden:
                        continue
                rr, cc = merged_top_left.get((r, c), (r, c))
                txt = _cell_value_as_text(ws, rr, cc, as_formulas=False,
                                          date_fmt=date_fmt,
                                          dt_fmt=dt_fmt,
                                          t_fmt=t_fmt)
                af_values.append(txt)
                if txt != "":
                    nonempty += 1
            if nonempty < min_af_nonempty:
                continue
        except Exception:
            # fail-safe: if something odd, don't skip the row
            pass
        # --- end A–F gate ---
        
        row_out = []
        for c in range(1, max_c + 1):
            if visible_only and ws.column_dimensions[get_column_letter(c)].hidden:
                continue
            rr, cc = merged_top_left.get((r, c), (r, c))
            val = _to_text(ws.cell(row=rr, column=cc).value, date_fmt, dt_fmt, t_fmt)
            row_out.append(val)
        if row_out and any(v != "" for v in row_out):
            yield row_out

def _stream_write_csv(path, rows_iterable, encoding: str, bom: bool):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    row_count = 0
    max_cols_seen = 0
    with open(path, "w", encoding=final_encoding, newline="") as f:
        writer = csv.writer(f)
        for row in rows_iterable:
            if row is None:
                row = []
            writer.writerow(row)
            row_count += 1
            if isinstance(row, (list, tuple)):
                if len(row) > max_cols_seen:
                    max_cols_seen = len(row)
    return row_count, max_cols_seen

def _get_cycle_dates_from_calendar(report_date_str=None):
    """
    Get cycle 7-day start and end dates from cycle calendar.
    
    Args:
        report_date_str: Report date in MM/DD/YYYY format (from REPORT_DATE env var)
                        If None, uses today's date
    
    Returns:
        tuple (start_date, end_date) as date objects, or (None, None) if not found
    """
    CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20250414.csv"
    
    try:
        if not os.path.exists(CYCLE_CSV):
            logger.warning(f"Cycle calendar not found: {CYCLE_CSV}, using fallback calculation")
            return None, None
        
        cycle_df = pd.read_csv(CYCLE_CSV)
        
        # Determine lookup date
        if report_date_str:
            try:
                # Parse MM/DD/YYYY format
                lookup_date = pd.to_datetime(report_date_str, format="%m/%d/%Y").date()
                lookup_date_str = report_date_str
            except:
                logger.warning(f"Invalid REPORT_DATE format: {report_date_str}, using today")
                lookup_date = datetime.now().date()
                lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        else:
            lookup_date = datetime.now().date()
            lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        
        # Try exact match on Report_Due_Date first
        matching_row = cycle_df[cycle_df['Report_Due_Date'] == lookup_date_str]
        
        if not matching_row.empty:
            row = matching_row.iloc[0]
            start_date = pd.to_datetime(row['7_Day_Start']).date()
            end_date = pd.to_datetime(row['7_Day_End']).date()
            logger.info(f"✅ Using cycle calendar: {row['Report_Name']} ({start_date} to {end_date})")
            return start_date, end_date
        
        # Fallback: find cycle where lookup_date falls within 7-day range
        for _, row in cycle_df.iterrows():
            try:
                start_date = pd.to_datetime(row['7_Day_Start']).date()
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if start_date <= lookup_date <= end_date:
                    logger.info(f"✅ Using cycle calendar (range match): {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        # If no match found, try most recent cycle where end_date <= lookup_date
        for _, row in cycle_df.iterrows():
            try:
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if end_date <= lookup_date:
                    start_date = pd.to_datetime(row['7_Day_Start']).date()
                    logger.info(f"✅ Using most recent cycle: {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        logger.warning(f"⚠️  No cycle found for date {lookup_date_str}, using fallback calculation")
        return None, None
        
    except Exception as e:
        logger.warning(f"⚠️  Error loading cycle calendar: {e}, using fallback calculation")
        return None, None

def _write_last7_by_reportdate_csv(df: pd.DataFrame, base_csv_path: str, encoding: str, bom: bool):
    """Write a filtered CSV with rows whose 'Report Date' falls within the cycle's 7-day range (from cycle calendar)."""
    if "Report Date" not in df.columns:
        return None
    
    # Get cycle dates from calendar (preferred) or fallback to simple calculation
    report_date_str = os.environ.get('REPORT_DATE', None)
    start_date, end_date = _get_cycle_dates_from_calendar(report_date_str)
    
    # Fallback to simple "last 7 days" if cycle calendar lookup failed
    if start_date is None or end_date is None:
        today = datetime.now().date()
        from datetime import timedelta
        start_date = today - timedelta(days=7)
        end_date = today
        logger.info(f"Using fallback: filtering last 7 days ({start_date} to {end_date})")
    
    dates = pd.to_datetime(df["Report Date"], errors="coerce")
    mask = (dates.dt.date >= start_date) & (dates.dt.date <= end_date)
    filtered = df[mask]
    
    # Use our custom formatting instead of pandas to_csv
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    out_path = os.path.splitext(base_csv_path)[0] + "_ReportDate_Last7.csv"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # Apply custom formatting and write using our streaming method
    def _iter_filtered_rows():
        # Emit headers first
        yield [str(col) for col in filtered.columns]
        # Emit formatted data rows
        for _, row in filtered.iterrows():
            row_out = []
            for val in row:
                formatted_val = _to_text(val, "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%H:%M:%S")
                row_out.append(formatted_val)
            yield row_out
    
    _stream_write_csv(out_path, _iter_filtered_rows(), encoding, bom)
    return out_path

def main():
    ap = argparse.ArgumentParser(description="Export all Excel sheets to individual CSV files.")
    ap.add_argument("--xlsx", required=False, help="Path to the source .xlsx (required unless --archive-only)")
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--out-subfolder", default=OUT_SUBFOLDER_DEFAULT)
    ap.add_argument("--encoding", default="utf-8")
    ap.add_argument("--no-bom", dest="bom", action="store_false")
    ap.add_argument("--visible-only", action="store_true", help="Export only visible rows and columns")
    ap.add_argument("--all-sheets", action="store_true", help="Export all sheets, ignoring include/exclude")
    ap.set_defaults(bom=True)
    ap.add_argument("--report-last7", action="store_true", help="Also write a *_ReportDate_Last7.csv filtered to last 7 days of Report Date (calamine engine only)")
    ap.add_argument("--include-empty", action="store_true")
    ap.add_argument("--na-rep", default="")
    ap.add_argument("--include", default=[], nargs="*", help="Include sheet patterns (substring match)")
    ap.add_argument("--exclude", default=[], nargs="*", help="Exclude sheet patterns (substring match)")
    ap.add_argument("--date-format", default="%Y-%m-%d", help="Date format string")
    ap.add_argument("--datetime-format", default="%Y-%m-%d %H:%M:%S", help="DateTime format string")
    ap.add_argument("--time-format", default="%H:%M:%S", help="Time format string")
    ap.add_argument("--af-columns", default="A,B,C",
                    help="Comma-separated list or Excel span (e.g., 'A-F') of columns to check for density gate.")
    ap.add_argument("--min-af-nonempty", type=int, default=2,
                    help="Minimum number of non-empty cells among --af-columns required to export a row.")
    ap.add_argument("--af-gate-visible-only", action="store_true",
                    help="If set, only visible cells among --af-columns count toward the threshold.")
    ap.add_argument("--disable-af-gate", action="store_true",
                    help="Disable A-F gate filtering (export all rows).")
    ap.add_argument("--engine", default="auto", choices=["auto", "calamine", "openpyxl"], 
                    help="Engine for reading Excel files (auto selects based on file size)")
    ap.add_argument("--chunksize", type=int, default=None, 
                    help="Read file in chunks of this size for large files (auto-enabled for 50MB+ files)")
    ap.add_argument("--benchmark", action="store_true", 
                    help="Enable performance benchmarking and include results in manifest")
    ap.add_argument("--parallel", action="store_true", 
                    help="Enable parallel sheet processing for better performance")
    ap.add_argument("--max-parallel-sheets", type=int, default=4, 
                    help="Maximum number of sheets to process in parallel (default: 4)")
    ap.add_argument("--archive-only", action="store_true",
                    help="Only archive old files and exit (no conversion)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Preview what would be archived without actually moving files")
    args = ap.parse_args()

    # Validate arguments
    if not args.archive_only and not args.xlsx:
        ap.error("--xlsx is required unless --archive-only is specified")

    # Handle archive-only mode
    if args.archive_only:
        working_dir = Path.cwd()
        exclude_file = None
        if args.xlsx:
            # If xlsx provided, use its parent directory and exclude this file
            xlsx_path = Path(args.xlsx).resolve()
            working_dir = xlsx_path.parent
            exclude_file = str(xlsx_path)
        count = archive_old_files(working_dir, dry_run=args.dry_run, exclude_file=exclude_file)
        if args.dry_run:
            print(f"\n[DRY-RUN] Would archive {count} file(s). Run without --dry-run to archive.")
        else:
            print(f"\nArchived {count} file(s).")
        return

    # Handle disable-af-gate option
    if args.disable_af_gate:
        args.min_af_nonempty = 0
        logger.info("A-F gate disabled - exporting all rows")

    xlsx_path = os.path.abspath(args.xlsx)
    
    # Auto-select engine and chunksize based on file size
    file_size = os.path.getsize(xlsx_path)
    available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
    
    if args.engine == "auto":
        # Use calamine for better performance on most files
        args.engine = "calamine"
    
    if args.chunksize is None:
        args.chunksize = get_adaptive_chunksize(file_size, available_memory)
        if file_size > 50 * 1024 * 1024:  # 50MB+
            logger.info(f"Large file detected ({file_size / (1024*1024):.1f}MB), enabling adaptive chunking with size {args.chunksize}")
    
    logger.info(f"Using engine: {args.engine}, chunksize: {args.chunksize}, available memory: {available_memory:.1f}MB")
    if not os.path.isfile(xlsx_path):
        logger.error(f"File not found: {xlsx_path}")
        raise FileNotFoundError(f"File not found: {xlsx_path}")

    out_parent = resolve_output_parent(args.base, args.out_subfolder)
    os.makedirs(out_parent, exist_ok=True)

    # Archive old files from the working directory (where xlsx files are)
    # EXCLUDE the current file being processed to prevent archiving it before conversion
    working_dir = Path(xlsx_path).parent
    if not args.dry_run:
        archive_old_files(working_dir, dry_run=False, exclude_file=xlsx_path)

    if args.out_subfolder != OUT_SUBFOLDER_DEFAULT:
        out_dir = out_parent
    else:
        wb_stem = os.path.splitext(os.path.basename(xlsx_path))[0]
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        out_dir = os.path.join(out_parent, f"{wb_stem}_{stamp}")
        os.makedirs(out_dir, exist_ok=True)

    # Initialize workbook based on engine
    wb = None
    if args.engine == "openpyxl":
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)
        sheet_names = wb.sheetnames
    else:  # calamine
        excel_file = pd.ExcelFile(xlsx_path, engine='calamine')
        sheet_names = excel_file.sheet_names
    
    used_names = set()
    exported = 0
    skipped = 0
    stats = {"rows_skipped_af_gate": 0}
    benchmark_results = []
    
    manifest = {
        "workbook": xlsx_path,
        "timestamp": datetime.now().isoformat(),
        "output_dir": out_dir,
        "workbook_sha256": get_file_hash(xlsx_path),
        "engine": args.engine,
        "chunksize": args.chunksize,
        "benchmark_enabled": bool(args.benchmark),
        "parallel_enabled": bool(args.parallel),
        "max_parallel_sheets": args.max_parallel_sheets,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "available_memory_mb": round(available_memory, 2),
        "rows_skipped_af_gate": stats.get("rows_skipped_af_gate", 0),
        "af_gate": {
            "columns": args.af_columns,
            "min_nonempty": args.min_af_nonempty,
            "visible_only": bool(args.af_gate_visible_only),
            "disabled": bool(args.disable_af_gate)
        },
        "sheets": [],
        "benchmark_results": []
    }

    # Filter sheets based on include/exclude
    filtered_sheets = []
    for sheet_name in sheet_names:
        if not args.all_sheets:
            if args.exclude and any(pat.lower() in sheet_name.lower() for pat in args.exclude):
                continue
            if args.include and not any(pat.lower() in sheet_name.lower() for pat in args.include):
                continue
        filtered_sheets.append(sheet_name)
    
    if args.parallel and len(filtered_sheets) > 1:
        # Parallel processing
        logger.info(f"Processing {len(filtered_sheets)} sheets in parallel (max {args.max_parallel_sheets} workers)")
        with ThreadPoolExecutor(max_workers=args.max_parallel_sheets) as executor:
            # Submit all tasks
            future_to_sheet = {
                executor.submit(process_sheet_parallel, sheet_name, xlsx_path, out_dir, args, args.engine, used_names, benchmark_results, None if len(filtered_sheets) != 1 else os.path.splitext(os.path.basename(xlsx_path))[0]): sheet_name 
                for sheet_name in filtered_sheets
            }
            
            # Process completed tasks
            for future in tqdm(as_completed(future_to_sheet), total=len(filtered_sheets), desc="Processing sheets"):
                sheet_name = future_to_sheet[future]
                try:
                    result = future.result()
                    if result["status"] == "success":
                        exported += 1
                        manifest["sheets"].append(result)
                    elif result["status"] == "skipped":
                        skipped += 1
                    else:
                        logger.error(f"Error processing {sheet_name}: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    logger.error(f"Exception processing {sheet_name}: {str(e)}")
    else:
        # Sequential processing (original logic)
        for sheet_name in tqdm(filtered_sheets, desc="Exporting sheets"):
            # Benchmarking
            if args.benchmark:
                benchmark_results = {}
                for eng in ['calamine', 'openpyxl']:
                    duration = benchmark_engine_performance(xlsx_path, sheet_name, eng, is_detailed=True)
                    benchmark_results[eng] = duration
                    logger.info(f"Benchmark: {sheet_name} with {eng} - {json.dumps(duration)}")
                manifest["benchmark_results"].append({"sheet_name": sheet_name, "results": benchmark_results})
            
            # Load sheet data based on engine
            if args.engine == "openpyxl":
                ws = wb[sheet_name]
                max_r, max_c = _get_used_range(ws)
                is_df = False
            else:  # calamine
                df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
                setattr(df, "_include_headers", True)
                max_r, max_c = _get_used_range(df)
                is_df = True
            
            if not args.include_empty and (max_r == 0 or max_c == 0):
                skipped += 1
                continue

            safe = sanitize_filename(sheet_name, used_names)
            # If only one sheet is being exported, use the workbook base name
            if len(filtered_sheets) == 1:
                csv_name = os.path.splitext(os.path.basename(xlsx_path))[0] + ".csv"
            else:
                csv_name = f"{safe}.csv"
            csv_path = os.path.join(out_dir, csv_name)
            try:
                @timeout_handler(300)  # 5 min timeout
                def export_with_timeout():
                    if args.engine == "openpyxl":
                        return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                    else:  # calamine
                        return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                
                row_count, col_count = export_with_timeout()
                if row_count == 0:
                    skipped += 1
                    continue
                exported += 1
                # Optional last-7 CSV for calamine path
                last7_path = None
                if is_df and args.report_last7:
                    last7_path = _write_last7_by_reportdate_csv(df, csv_path, args.encoding, args.bom)
                manifest["sheets"].append({
                    "sheet_name": sheet_name,
                    "sanitized_name": safe,
                    "file": csv_path,
                    "file_sha256": get_file_hash(csv_path),
                    "rows": row_count,
                    "cols": col_count,
                    "last7_file": last7_path
                })
            except ExportTimeoutError:
                logger.error(f"Timeout during export of {safe}")
                raise ExportError(f"Timeout exporting {safe}")
            except Exception as e:
                logger.error(f"Error exporting {safe}: {str(e)}")
                raise ExportError(f"Error exporting {safe}: {str(e)}")

    # Add benchmark results to manifest
    if args.benchmark and manifest["benchmark_results"]:
        # Calculate summary from benchmark results
        total_duration = 0
        total_rows = 0
        for benchmark in manifest["benchmark_results"]:
            for engine, results in benchmark["results"].items():
                total_duration += results.get("total_duration", 0)
                # Estimate rows from throughput
                if results.get("throughput_rows_sec", 0) > 0:
                    total_rows += results.get("throughput_rows_sec", 0) * results.get("total_duration", 0)
        
        manifest["benchmark_summary"] = {
            "total_duration_seconds": round(total_duration, 3),
            "total_rows_processed": round(total_rows, 0),
            "average_rows_per_second": round(total_rows / total_duration, 1) if total_duration > 0 else 0,
            "sheets_benchmarked": len(manifest["benchmark_results"])
        }

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Source workbook : {xlsx_path}")
    print(f"Output folder   : {out_dir}")
    print(f"Sheets exported : {exported}")
    print(f"Sheets skipped  : {skipped} (empty or no columns)")
    print(f"Manifest        : {os.path.join(out_dir, 'manifest.json')}")

if __name__ == "__main__":
    main()
```


Checking for linting errors, then running the conversion:



Running the Excel conversion with the updated script. Setting REPORT_DATE and converting the Excel file:



Calamine engine isn't available. Checking available engines and using an alternative:



Conversion completed. Checking if the 7-day filtered CSV was created:



The 7-day CSV wasn't created because `--report-last7` only works with the calamine engine, and we used openpyxl. Updating the code to support creating the 7-day CSV with openpyxl as well:


```python
# export_excel_sheets_to_csv.py
# Changes: Added --all-sheets flag, timeouts, custom exceptions, JSON logging, tqdm progress, streaming writer

import argparse
import os
import re
import json
import hashlib
import time
import psutil
import shutil
from pathlib import Path
from datetime import datetime, time as dtime, date, timedelta as dtdelta
import fnmatch
import csv
import logging
import signal
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=UserWarning, module="dateutil.parser")

from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries, get_column_letter
from openpyxl.utils import column_index_from_string
import pandas as pd

# Custom Exceptions
class ExportTimeoutError(Exception):
    pass

class ExportError(Exception):
    pass

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('export_log.json')
handler.setFormatter(logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'))
logger.addHandler(handler)

# Timeout Handler (Windows compatible)
import threading
import time

def timeout_handler(timeout_seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)
            
            if thread.is_alive():
                raise ExportTimeoutError(f"Export timed out after {timeout_seconds} seconds")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        return wrapper
    return decorator

BASE_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack"
OUT_SUBFOLDER_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack\14_Excel\xlsx_to_csv"

# Archive configuration
ARCHIVE_BASE = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS")
RMS_ARCHIVE = ARCHIVE_BASE / "_RMS" / "SCRPA" / "archive"
CAD_ARCHIVE = ARCHIVE_BASE / "_CAD" / "SCRPA" / "archive"

_TIME_RE = re.compile(r"^\s*\d{1,2}:\d{2}(:\d{2})?\s*$")

def get_archive_folder(filepath: Path) -> Path:
    """Determine archive folder based on file path (CAD or RMS)"""
    folder = CAD_ARCHIVE if "_CAD" in str(filepath) else RMS_ARCHIVE
    folder.mkdir(parents=True, exist_ok=True)
    
    # Extract date from filename if present, else use today
    date_match = re.search(r"(\d{4}[-_]\d{2}[-_]\d{2})|(\d{8})", filepath.name)
    if date_match:
        date_str = date_match.group(0).replace("_", "-")
        # Normalize to YYYY-MM-DD format
        if len(date_str) == 8:  # YYYYMMDD
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    dated_folder = folder / date_str
    dated_folder.mkdir(exist_ok=True)
    return dated_folder

def archive_old_files(folder: Path, dry_run: bool = False, exclude_file: str = None):
    """Archive old .xlsx and .csv files from the working directory
    
    Args:
        folder: Directory to archive files from
        dry_run: If True, only show what would be archived
        exclude_file: Path to file to exclude from archiving (e.g., file being processed)
    """
    if not folder.exists():
        logger.info(f"Archive folder does not exist: {folder}")
        return 0
    
    script_name = Path(__file__).name
    archive_count = 0
    files_to_archive = []
    
    # Normalize exclude_file path for comparison
    exclude_path = None
    if exclude_file:
        exclude_path = Path(exclude_file).resolve()
    
    # Build set of Excel file timestamp prefixes to keep matching CSV files
    excel_timestamps = set()
    try:
        for item in folder.iterdir():
            try:
                if item.is_file() and item.suffix.lower() == ".xlsx" and item.name != script_name:
                    if "archive" not in str(item.parent):
                        # Extract timestamp prefix (format: YYYY_MM_DD_HH_MM_SS_SCRPA_RMS)
                        # CSV files will have same prefix: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                        stem = item.stem  # e.g., "2025_12_02_01_14_15_SCRPA_RMS"
                        excel_timestamps.add(stem)
            except (OSError, PermissionError) as e:
                logger.warning(f"Could not access file {item.name}: {e}")
                continue
    except Exception as e:
        logger.error(f"Error building Excel timestamp set: {e}")
        # Continue anyway - worst case we archive everything
    
    for item in folder.iterdir():
        try:
            if not item.is_file() or item.suffix.lower() not in {".xlsx", ".csv"} or item.name == script_name:
                continue
            
            # Skip files that are already in archive subdirectories
            if "archive" in str(item.parent):
                continue
            
            # Skip the file being processed
            try:
                if exclude_path and item.resolve() == exclude_path:
                    logger.debug(f"Skipping current file from archive: {item.name}")
                    continue
            except (OSError, PermissionError):
                # If we can't resolve the path, skip it
                continue
            
            # For CSV files: keep if they match an existing Excel file timestamp
            if item.suffix.lower() == ".csv":
                try:
                    csv_stem = item.stem
                    # Check if this CSV matches any Excel file timestamp
                    # CSV names: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                    # Excel names: {timestamp}_SCRPA_RMS.xlsx
                    matches_excel = False
                    for excel_stem in excel_timestamps:
                        # Check if CSV stem starts with Excel stem (handles both full CSV and Last7 CSV)
                        if csv_stem.startswith(excel_stem):
                            matches_excel = True
                            break
                    if matches_excel:
                        logger.debug(f"Keeping CSV file (matches Excel): {item.name}")
                        continue
                except Exception as e:
                    logger.warning(f"Error checking CSV file {item.name}: {e}")
                    # If we can't check, err on the side of caution and archive it
                    pass
            
            files_to_archive.append(item)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not process file {item.name}: {e}")
            continue
        except Exception as e:
            logger.warning(f"Unexpected error processing {item.name}: {e}")
            continue
    
    if not files_to_archive:
        logger.info("No files to archive")
        return 0
    
    if dry_run:
        print(f"\n[DRY-RUN] Would archive {len(files_to_archive)} file(s):")
        for item in files_to_archive:
            dest = get_archive_folder(item)
            print(f"  {item.name} -> {dest / item.name}")
        return len(files_to_archive)
    
    for item in files_to_archive:
        try:
            dest = get_archive_folder(item)
            dest_file = dest / item.name
            
            # Handle duplicates by adding timestamp
            if dest_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                stem = dest_file.stem
                suffix = dest_file.suffix
                dest_file = dest / f"{stem}_{timestamp}{suffix}"
            
            shutil.move(str(item), str(dest_file))
            archive_count += 1
            logger.info(f"Archived: {item.name} -> {dest_file}")
        except Exception as e:
            logger.warning(f"Failed to archive {item.name}: {e}")
    
    if archive_count > 0:
        logger.info(f"Archived {archive_count} file(s)")
    
    return archive_count

def sanitize_filename(name: str, used: set) -> str:
    fn = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name).strip().strip('.')
    fn = re.sub(r'[\s_]+', '_', fn)[:150] or "Sheet"
    original = fn
    i = 2
    while fn.lower() in used:
        fn = f"{original}_{i}"
        i += 1
    used.add(fn.lower())
    return fn

def resolve_output_parent(base: str, out_subfolder: str) -> str:
    base_abs = os.path.abspath(base)
    parent = out_subfolder
    if not os.path.isabs(parent):
        parent = os.path.join(base_abs, parent)
    parent = os.path.abspath(parent)
    norm_parent = os.path.normcase(parent)
    norm_base = os.path.normcase(base_abs)
    if not norm_parent.startswith(norm_base):
        raise ValueError(f"Output path must be inside the OneDrive base.\nBase: {base_abs}\nOutput: {parent}")
    return parent

def get_used(ws):
    try:
        dim = ws.calculate_dimension()
    except ValueError:
        # Handle unsized worksheets
        dim = ws.calculate_dimension(force=True)
    
    if dim in ("A1:A1", None):
        return 0, 0
    min_c, min_r, max_c, max_r = range_boundaries(dim)
    return max_r, max_c

def get_file_hash(path):
    if not os.path.exists(path):
        return None
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_adaptive_chunksize(file_size, available_memory):
    memory_threshold = available_memory * 0.5  # Use 50% of available memory
    if file_size > 100 * 1024 * 1024:
        return 1000
    elif file_size > 50 * 1024 * 1024:
        return 2000
    elif file_size > 10 * 1024 * 1024:
        return 5000
    return 10000

def benchmark_engine_performance(file_path, sheet_name, engine, is_detailed=False):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    start_mem = process.memory_info().rss / (1024 * 1024)  # MB
    start_cpu = process.cpu_percent(interval=0.1)

    load_start = time.time()
    if engine == 'calamine':
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
    else:
        wb = load_workbook(file_path, read_only=True, data_only=True)
        ws = wb[sheet_name]
    load_end = time.time()
    load_duration = load_end - load_start

    process_start = time.time()
    if engine == 'calamine':
        for _, row in df.iterrows():
            pass
    else:
        for row in ws.iter_rows():
            pass
    process_end = time.time()
    process_duration = process_end - process_start

    write_start = time.time()
    with open(os.devnull, 'w') as f:
        writer = csv.writer(f)
        if engine == 'calamine':
            for _, row in df.iterrows():
                writer.writerow(row)
        else:
            for row in ws.iter_rows(values_only=True):
                writer.writerow(row)
    write_end = time.time()
    write_duration = write_end - write_start

    end_time = time.time()
    end_mem = process.memory_info().rss / (1024 * 1024)
    end_cpu = process.cpu_percent(interval=0.1)

    total_duration = end_time - start_time
    rows, _ = _get_used_range(df if engine == 'calamine' else ws)
    throughput = rows / total_duration if total_duration > 0 else 0
    mem_peak = max(start_mem, end_mem)
    cpu_avg = (start_cpu + end_cpu) / 2

    results = {
        "total_duration": total_duration,
        "throughput_rows_sec": throughput,
        "memory_peak_mb": mem_peak,
        "cpu_avg_percent": cpu_avg
    }
    if is_detailed:
        results.update({
            "load_duration": load_duration,
            "process_duration": process_duration,
            "write_duration": write_duration,
            "file_size_mb": os.path.getsize(file_path) / (1024 * 1024)
        })
    return results

def _parse_af_columns(spec: str):
    """
    Accept 'A,B,C,D,E,F' or 'A-F' (case-insensitive). Return sorted 1-based column indexes.
    """
    spec = spec.strip().upper().replace(" ", "")
    cols = []
    if "-" in spec and "," not in spec:
        start, end = spec.split("-", 1)
        s = column_index_from_string(start)
        e = column_index_from_string(end)
        if s > e: s, e = e, s
        cols = list(range(s, e + 1))
    else:
        parts = [p for p in spec.split(",") if p]
        for p in parts:
            cols.append(column_index_from_string(p))
    return sorted(set(cols))

def _cell_value_as_text(ws, rr, cc, as_formulas: bool, date_fmt, dt_fmt, t_fmt, force_text=False):
    """
    Shared converter used by the gate: when as_formulas=True, emit '=...' for formula cells,
    else use normal _to_text() logic. 'force_text' only matters in formulas exporter.
    """
    cell = ws.cell(row=rr, column=cc)
    if as_formulas:
        is_formula = (getattr(cell, "data_type", None) == 'f') or (isinstance(cell.value, str) and cell.value.startswith("="))
        if is_formula:
            s = str(cell.value)
            return s if s.startswith("=") else "=" + s
        # fall through to normal text for non-formula
    # call the existing _to_text() in this file
    return _to_text(cell.value, date_fmt, dt_fmt, t_fmt)

def _to_text(value, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S"):
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return value
    # Handle pandas/calamine time-only values that may come as timedelta
    try:
        import pandas as _pd
        if isinstance(value, getattr(_pd, 'Timedelta', ())) or isinstance(value, dtdelta):
            total_seconds = int(value.total_seconds())
            # Normalize to within a day
            total_seconds = total_seconds % (24 * 3600)
            hh = total_seconds // 3600
            mm = (total_seconds % 3600) // 60
            ss = total_seconds % 60
            return f"{hh:02d}:{mm:02d}:{ss:02d}"
    except Exception:
        pass
    if isinstance(value, datetime):
        # If Excel stored a time-only value, the date part is often 1899-12-30
        if value.date().isoformat() == "1899-12-30":
            return value.strftime(t_fmt)
        # If time component is midnight, treat as date-only
        if value.hour == 0 and value.minute == 0 and value.second == 0 and value.microsecond == 0:
            return value.strftime(date_fmt)
        return value.strftime(dt_fmt)
    if isinstance(value, date):
        return value.strftime(date_fmt)
    if isinstance(value, dtime):
        return value.strftime(t_fmt)
    if isinstance(value, str) and _TIME_RE.match(value):
        parts = [int(p) for p in value.strip().split(":")]
        while len(parts) < 3:
            parts.append(0)
        return dtime(parts[0], parts[1], parts[2]).strftime(t_fmt)
    return str(value)

def _get_used_range(data):
    """Get used range for both openpyxl worksheets and pandas DataFrames"""
    if hasattr(data, 'calculate_dimension'):  # openpyxl worksheet
        try:
            dim = data.calculate_dimension()
        except ValueError:
            # Handle unsized worksheets
            dim = data.calculate_dimension(force=True)
        
        if dim in ("A1:A1", None):
            return 0, 0
        min_c, min_r, max_c, max_r = range_boundaries(dim)
        return max_r, max_c
    else:  # pandas DataFrame
        if data.empty:
            return 0, 0
        return len(data), len(data.columns)


def _iter_rows_pandas(df, visible_only, date_fmt, dt_fmt, t_fmt, af_columns, min_af_nonempty, af_gate_visible_only):
    """Iterate over pandas DataFrame rows for calamine engine"""
    af_cols = _parse_af_columns(af_columns)
    max_r, max_c = _get_used_range(df)
    if max_r == 0 or max_c == 0:
        return
    
    # Optionally emit header row when using pandas engine
    if getattr(df, "_include_headers", False):
        yield [str(col) for col in df.columns]

    for r, row in enumerate(df.itertuples(index=False), 1):
        if visible_only:
            # For pandas, we can't easily check row/column visibility
            # This would require additional metadata
            pass
            
        # A-F gate logic
        non_empty = 0
        af_values = []
        for c in af_cols:
            if c < len(row):
                val = row[c]
                af_values.append(val)
                if pd.notna(val) and val != "":
                    non_empty += 1
        
        if non_empty < min_af_nonempty:
            continue
        
        # Convert row to text
        row_out = []
        for val in row:
            formatted_val = _to_text(val, date_fmt, dt_fmt, t_fmt)
            row_out.append(formatted_val)
        
        if row_out and any(v != "" for v in row_out):
            yield row_out

def process_sheet_parallel(sheet_name, xlsx_path, out_dir, args, engine, used_names, benchmark_results, single_csv_basename=None):
    """Process a single sheet in parallel"""
    try:
        # Load sheet data based on engine
        if engine == "openpyxl":
            wb = load_workbook(xlsx_path, read_only=True, data_only=True)
            ws = wb[sheet_name]
            max_r, max_c = _get_used_range(ws)
            is_df = False
        else:  # calamine
            df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
            # Mark to include headers in pandas iteration
            setattr(df, "_include_headers", True)
            max_r, max_c = _get_used_range(df)
            is_df = True
        
        if not args.include_empty and (max_r == 0 or max_c == 0):
            return {"sheet_name": sheet_name, "status": "skipped", "reason": "empty"}
        
        safe = sanitize_filename(sheet_name, used_names)
        # If only one sheet is being exported, use the workbook name for CSV
        if single_csv_basename:
            csv_path = os.path.join(out_dir, f"{single_csv_basename}.csv")
        else:
            csv_path = os.path.join(out_dir, f"{safe}.csv")
        
        # Benchmark this sheet if requested
        if args.benchmark:
            benchmark_start = time.time()
        
        @timeout_handler(300)  # 5 min timeout
        def export_with_timeout():
            if args.engine == "openpyxl":
                return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
            else:  # calamine
                return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
        
        row_count, col_count = export_with_timeout()
        # Optional last-7 CSV for calamine path
        last7_path = None
        if is_df and args.report_last7:
            last7_path = _write_last7_by_reportdate_csv(df, csv_path, args.encoding, args.bom)
        
        # Record benchmark if requested
        if args.benchmark:
            benchmark_end = time.time()
            benchmark_results.append({
                "sheet_name": sheet_name,
                "engine": engine,
                "duration_seconds": round(benchmark_end - benchmark_start, 3),
                "rows": row_count,
                "cols": col_count,
                "rows_per_second": round(row_count / (benchmark_end - benchmark_start), 1) if (benchmark_end - benchmark_start) > 0 else 0
            })
        
        if engine == "openpyxl":
            wb.close()
        
        return {
            "sheet_name": sheet_name,
            "sanitized_name": safe,
            "file": csv_path,
            "file_sha256": get_file_hash(csv_path),
            "rows": row_count,
            "cols": col_count,
            "last7_file": last7_path,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error processing sheet {sheet_name}: {str(e)}")
        return {"sheet_name": sheet_name, "status": "error", "error": str(e)}

def _iter_rows(ws, visible_only: bool, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S", af_columns="A,B,C,D,E,F", min_af_nonempty=4, af_gate_visible_only=False):
    max_r, max_c = get_used(ws)
    merged_top_left = {}
    if hasattr(ws, 'merged_cells') and ws.merged_cells:
        for rng in ws.merged_cells.ranges:
            tl_r, tl_c = rng.min_row, rng.min_col
            for rr in range(rng.min_row, rng.max_row + 1):
                for cc in range(rng.min_col, rng.max_col + 1):
                    merged_top_left[(rr, cc)] = (tl_r, tl_c)
    
    af_cols = _parse_af_columns(af_columns)
    
    for r in tqdm(range(1, max_r + 1), desc="Processing rows"):
        if visible_only and ws.row_dimensions[r].hidden:
            continue
            
        # --- A–F gate (VALUES) ---
        try:
            nonempty = 0
            af_values = []
            for c in af_cols:
                # if visible-only gate, ignore hidden columns
                if af_gate_visible_only and visible_only:
                    col_letter = get_column_letter(c)
                    if ws.column_dimensions[col_letter].hidden:
                        continue
                rr, cc = merged_top_left.get((r, c), (r, c))
                txt = _cell_value_as_text(ws, rr, cc, as_formulas=False,
                                          date_fmt=date_fmt,
                                          dt_fmt=dt_fmt,
                                          t_fmt=t_fmt)
                af_values.append(txt)
                if txt != "":
                    nonempty += 1
            if nonempty < min_af_nonempty:
                continue
        except Exception:
            # fail-safe: if something odd, don't skip the row
            pass
        # --- end A–F gate ---
        
        row_out = []
        for c in range(1, max_c + 1):
            if visible_only and ws.column_dimensions[get_column_letter(c)].hidden:
                continue
            rr, cc = merged_top_left.get((r, c), (r, c))
            val = _to_text(ws.cell(row=rr, column=cc).value, date_fmt, dt_fmt, t_fmt)
            row_out.append(val)
        if row_out and any(v != "" for v in row_out):
            yield row_out

def _stream_write_csv(path, rows_iterable, encoding: str, bom: bool):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    row_count = 0
    max_cols_seen = 0
    with open(path, "w", encoding=final_encoding, newline="") as f:
        writer = csv.writer(f)
        for row in rows_iterable:
            if row is None:
                row = []
            writer.writerow(row)
            row_count += 1
            if isinstance(row, (list, tuple)):
                if len(row) > max_cols_seen:
                    max_cols_seen = len(row)
    return row_count, max_cols_seen

def _get_cycle_dates_from_calendar(report_date_str=None):
    """
    Get cycle 7-day start and end dates from cycle calendar.
    
    Args:
        report_date_str: Report date in MM/DD/YYYY format (from REPORT_DATE env var)
                        If None, uses today's date
    
    Returns:
        tuple (start_date, end_date) as date objects, or (None, None) if not found
    """
    CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20250414.csv"
    
    try:
        if not os.path.exists(CYCLE_CSV):
            logger.warning(f"Cycle calendar not found: {CYCLE_CSV}, using fallback calculation")
            return None, None
        
        cycle_df = pd.read_csv(CYCLE_CSV)
        
        # Determine lookup date
        if report_date_str:
            try:
                # Parse MM/DD/YYYY format
                lookup_date = pd.to_datetime(report_date_str, format="%m/%d/%Y").date()
                lookup_date_str = report_date_str
            except:
                logger.warning(f"Invalid REPORT_DATE format: {report_date_str}, using today")
                lookup_date = datetime.now().date()
                lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        else:
            lookup_date = datetime.now().date()
            lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        
        # Try exact match on Report_Due_Date first
        matching_row = cycle_df[cycle_df['Report_Due_Date'] == lookup_date_str]
        
        if not matching_row.empty:
            row = matching_row.iloc[0]
            start_date = pd.to_datetime(row['7_Day_Start']).date()
            end_date = pd.to_datetime(row['7_Day_End']).date()
            logger.info(f"✅ Using cycle calendar: {row['Report_Name']} ({start_date} to {end_date})")
            return start_date, end_date
        
        # Fallback: find cycle where lookup_date falls within 7-day range
        for _, row in cycle_df.iterrows():
            try:
                start_date = pd.to_datetime(row['7_Day_Start']).date()
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if start_date <= lookup_date <= end_date:
                    logger.info(f"✅ Using cycle calendar (range match): {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        # If no match found, try most recent cycle where end_date <= lookup_date
        for _, row in cycle_df.iterrows():
            try:
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if end_date <= lookup_date:
                    start_date = pd.to_datetime(row['7_Day_Start']).date()
                    logger.info(f"✅ Using most recent cycle: {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        logger.warning(f"⚠️  No cycle found for date {lookup_date_str}, using fallback calculation")
        return None, None
        
    except Exception as e:
        logger.warning(f"⚠️  Error loading cycle calendar: {e}, using fallback calculation")
        return None, None

def _write_last7_by_reportdate_csv(df: pd.DataFrame, base_csv_path: str, encoding: str, bom: bool):
    """Write a filtered CSV with rows whose 'Report Date' falls within the cycle's 7-day range (from cycle calendar)."""
    if "Report Date" not in df.columns:
        return None
    
    # Get cycle dates from calendar (preferred) or fallback to simple calculation
    report_date_str = os.environ.get('REPORT_DATE', None)
    start_date, end_date = _get_cycle_dates_from_calendar(report_date_str)
    
    # Fallback to simple "last 7 days" if cycle calendar lookup failed
    if start_date is None or end_date is None:
        today = datetime.now().date()
        from datetime import timedelta
        start_date = today - timedelta(days=7)
        end_date = today
        logger.info(f"Using fallback: filtering last 7 days ({start_date} to {end_date})")
    
    dates = pd.to_datetime(df["Report Date"], errors="coerce")
    mask = (dates.dt.date >= start_date) & (dates.dt.date <= end_date)
    filtered = df[mask]
    
    # Use our custom formatting instead of pandas to_csv
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    out_path = os.path.splitext(base_csv_path)[0] + "_ReportDate_Last7.csv"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # Apply custom formatting and write using our streaming method
    def _iter_filtered_rows():
        # Emit headers first
        yield [str(col) for col in filtered.columns]
        # Emit formatted data rows
        for _, row in filtered.iterrows():
            row_out = []
            for val in row:
                formatted_val = _to_text(val, "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%H:%M:%S")
                row_out.append(formatted_val)
            yield row_out
    
    _stream_write_csv(out_path, _iter_filtered_rows(), encoding, bom)
    return out_path

def main():
    ap = argparse.ArgumentParser(description="Export all Excel sheets to individual CSV files.")
    ap.add_argument("--xlsx", required=False, help="Path to the source .xlsx (required unless --archive-only)")
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--out-subfolder", default=OUT_SUBFOLDER_DEFAULT)
    ap.add_argument("--encoding", default="utf-8")
    ap.add_argument("--no-bom", dest="bom", action="store_false")
    ap.add_argument("--visible-only", action="store_true", help="Export only visible rows and columns")
    ap.add_argument("--all-sheets", action="store_true", help="Export all sheets, ignoring include/exclude")
    ap.set_defaults(bom=True)
    ap.add_argument("--report-last7", action="store_true", help="Also write a *_ReportDate_Last7.csv filtered to last 7 days of Report Date (calamine engine only)")
    ap.add_argument("--include-empty", action="store_true")
    ap.add_argument("--na-rep", default="")
    ap.add_argument("--include", default=[], nargs="*", help="Include sheet patterns (substring match)")
    ap.add_argument("--exclude", default=[], nargs="*", help="Exclude sheet patterns (substring match)")
    ap.add_argument("--date-format", default="%Y-%m-%d", help="Date format string")
    ap.add_argument("--datetime-format", default="%Y-%m-%d %H:%M:%S", help="DateTime format string")
    ap.add_argument("--time-format", default="%H:%M:%S", help="Time format string")
    ap.add_argument("--af-columns", default="A,B,C",
                    help="Comma-separated list or Excel span (e.g., 'A-F') of columns to check for density gate.")
    ap.add_argument("--min-af-nonempty", type=int, default=2,
                    help="Minimum number of non-empty cells among --af-columns required to export a row.")
    ap.add_argument("--af-gate-visible-only", action="store_true",
                    help="If set, only visible cells among --af-columns count toward the threshold.")
    ap.add_argument("--disable-af-gate", action="store_true",
                    help="Disable A-F gate filtering (export all rows).")
    ap.add_argument("--engine", default="auto", choices=["auto", "calamine", "openpyxl"], 
                    help="Engine for reading Excel files (auto selects based on file size)")
    ap.add_argument("--chunksize", type=int, default=None, 
                    help="Read file in chunks of this size for large files (auto-enabled for 50MB+ files)")
    ap.add_argument("--benchmark", action="store_true", 
                    help="Enable performance benchmarking and include results in manifest")
    ap.add_argument("--parallel", action="store_true", 
                    help="Enable parallel sheet processing for better performance")
    ap.add_argument("--max-parallel-sheets", type=int, default=4, 
                    help="Maximum number of sheets to process in parallel (default: 4)")
    ap.add_argument("--archive-only", action="store_true",
                    help="Only archive old files and exit (no conversion)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Preview what would be archived without actually moving files")
    args = ap.parse_args()

    # Validate arguments
    if not args.archive_only and not args.xlsx:
        ap.error("--xlsx is required unless --archive-only is specified")

    # Handle archive-only mode
    if args.archive_only:
        working_dir = Path.cwd()
        exclude_file = None
        if args.xlsx:
            # If xlsx provided, use its parent directory and exclude this file
            xlsx_path = Path(args.xlsx).resolve()
            working_dir = xlsx_path.parent
            exclude_file = str(xlsx_path)
        count = archive_old_files(working_dir, dry_run=args.dry_run, exclude_file=exclude_file)
        if args.dry_run:
            print(f"\n[DRY-RUN] Would archive {count} file(s). Run without --dry-run to archive.")
        else:
            print(f"\nArchived {count} file(s).")
        return

    # Handle disable-af-gate option
    if args.disable_af_gate:
        args.min_af_nonempty = 0
        logger.info("A-F gate disabled - exporting all rows")

    xlsx_path = os.path.abspath(args.xlsx)
    
    # Auto-select engine and chunksize based on file size
    file_size = os.path.getsize(xlsx_path)
    available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
    
    if args.engine == "auto":
        # Use calamine for better performance on most files
        args.engine = "calamine"
    
    if args.chunksize is None:
        args.chunksize = get_adaptive_chunksize(file_size, available_memory)
        if file_size > 50 * 1024 * 1024:  # 50MB+
            logger.info(f"Large file detected ({file_size / (1024*1024):.1f}MB), enabling adaptive chunking with size {args.chunksize}")
    
    logger.info(f"Using engine: {args.engine}, chunksize: {args.chunksize}, available memory: {available_memory:.1f}MB")
    if not os.path.isfile(xlsx_path):
        logger.error(f"File not found: {xlsx_path}")
        raise FileNotFoundError(f"File not found: {xlsx_path}")

    out_parent = resolve_output_parent(args.base, args.out_subfolder)
    os.makedirs(out_parent, exist_ok=True)

    # Archive old files from the working directory (where xlsx files are)
    # EXCLUDE the current file being processed to prevent archiving it before conversion
    working_dir = Path(xlsx_path).parent
    if not args.dry_run:
        archive_old_files(working_dir, dry_run=False, exclude_file=xlsx_path)

    if args.out_subfolder != OUT_SUBFOLDER_DEFAULT:
        out_dir = out_parent
    else:
        wb_stem = os.path.splitext(os.path.basename(xlsx_path))[0]
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        out_dir = os.path.join(out_parent, f"{wb_stem}_{stamp}")
        os.makedirs(out_dir, exist_ok=True)

    # Initialize workbook based on engine
    wb = None
    if args.engine == "openpyxl":
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)
        sheet_names = wb.sheetnames
    else:  # calamine
        excel_file = pd.ExcelFile(xlsx_path, engine='calamine')
        sheet_names = excel_file.sheet_names
    
    used_names = set()
    exported = 0
    skipped = 0
    stats = {"rows_skipped_af_gate": 0}
    benchmark_results = []
    
    manifest = {
        "workbook": xlsx_path,
        "timestamp": datetime.now().isoformat(),
        "output_dir": out_dir,
        "workbook_sha256": get_file_hash(xlsx_path),
        "engine": args.engine,
        "chunksize": args.chunksize,
        "benchmark_enabled": bool(args.benchmark),
        "parallel_enabled": bool(args.parallel),
        "max_parallel_sheets": args.max_parallel_sheets,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "available_memory_mb": round(available_memory, 2),
        "rows_skipped_af_gate": stats.get("rows_skipped_af_gate", 0),
        "af_gate": {
            "columns": args.af_columns,
            "min_nonempty": args.min_af_nonempty,
            "visible_only": bool(args.af_gate_visible_only),
            "disabled": bool(args.disable_af_gate)
        },
        "sheets": [],
        "benchmark_results": []
    }

    # Filter sheets based on include/exclude
    filtered_sheets = []
    for sheet_name in sheet_names:
        if not args.all_sheets:
            if args.exclude and any(pat.lower() in sheet_name.lower() for pat in args.exclude):
                continue
            if args.include and not any(pat.lower() in sheet_name.lower() for pat in args.include):
                continue
        filtered_sheets.append(sheet_name)
    
    if args.parallel and len(filtered_sheets) > 1:
        # Parallel processing
        logger.info(f"Processing {len(filtered_sheets)} sheets in parallel (max {args.max_parallel_sheets} workers)")
        with ThreadPoolExecutor(max_workers=args.max_parallel_sheets) as executor:
            # Submit all tasks
            future_to_sheet = {
                executor.submit(process_sheet_parallel, sheet_name, xlsx_path, out_dir, args, args.engine, used_names, benchmark_results, None if len(filtered_sheets) != 1 else os.path.splitext(os.path.basename(xlsx_path))[0]): sheet_name 
                for sheet_name in filtered_sheets
            }
            
            # Process completed tasks
            for future in tqdm(as_completed(future_to_sheet), total=len(filtered_sheets), desc="Processing sheets"):
                sheet_name = future_to_sheet[future]
                try:
                    result = future.result()
                    if result["status"] == "success":
                        exported += 1
                        manifest["sheets"].append(result)
                    elif result["status"] == "skipped":
                        skipped += 1
                    else:
                        logger.error(f"Error processing {sheet_name}: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    logger.error(f"Exception processing {sheet_name}: {str(e)}")
    else:
        # Sequential processing (original logic)
        for sheet_name in tqdm(filtered_sheets, desc="Exporting sheets"):
            # Benchmarking
            if args.benchmark:
                benchmark_results = {}
                for eng in ['calamine', 'openpyxl']:
                    duration = benchmark_engine_performance(xlsx_path, sheet_name, eng, is_detailed=True)
                    benchmark_results[eng] = duration
                    logger.info(f"Benchmark: {sheet_name} with {eng} - {json.dumps(duration)}")
                manifest["benchmark_results"].append({"sheet_name": sheet_name, "results": benchmark_results})
            
            # Load sheet data based on engine
            if args.engine == "openpyxl":
                ws = wb[sheet_name]
                max_r, max_c = _get_used_range(ws)
                is_df = False
            else:  # calamine
                df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
                setattr(df, "_include_headers", True)
                max_r, max_c = _get_used_range(df)
                is_df = True
            
            if not args.include_empty and (max_r == 0 or max_c == 0):
                skipped += 1
                continue

            safe = sanitize_filename(sheet_name, used_names)
            # If only one sheet is being exported, use the workbook base name
            if len(filtered_sheets) == 1:
                csv_name = os.path.splitext(os.path.basename(xlsx_path))[0] + ".csv"
            else:
                csv_name = f"{safe}.csv"
            csv_path = os.path.join(out_dir, csv_name)
            try:
                @timeout_handler(300)  # 5 min timeout
                def export_with_timeout():
                    if args.engine == "openpyxl":
                        return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                    else:  # calamine
                        return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                
                row_count, col_count = export_with_timeout()
                if row_count == 0:
                    skipped += 1
                    continue
                exported += 1
                # Optional last-7 CSV (works with both engines now)
                last7_path = None
                if args.report_last7:
                    # Load the CSV we just created to filter it
                    try:
                        df_for_filter = pd.read_csv(csv_path, encoding=args.encoding)
                        last7_path = _write_last7_by_reportdate_csv(df_for_filter, csv_path, args.encoding, args.bom)
                    except Exception as e:
                        logger.warning(f"Could not create 7-day filtered CSV: {e}")
                        last7_path = None
                manifest["sheets"].append({
                    "sheet_name": sheet_name,
                    "sanitized_name": safe,
                    "file": csv_path,
                    "file_sha256": get_file_hash(csv_path),
                    "rows": row_count,
                    "cols": col_count,
                    "last7_file": last7_path
                })
            except ExportTimeoutError:
                logger.error(f"Timeout during export of {safe}")
                raise ExportError(f"Timeout exporting {safe}")
            except Exception as e:
                logger.error(f"Error exporting {safe}: {str(e)}")
                raise ExportError(f"Error exporting {safe}: {str(e)}")

    # Add benchmark results to manifest
    if args.benchmark and manifest["benchmark_results"]:
        # Calculate summary from benchmark results
        total_duration = 0
        total_rows = 0
        for benchmark in manifest["benchmark_results"]:
            for engine, results in benchmark["results"].items():
                total_duration += results.get("total_duration", 0)
                # Estimate rows from throughput
                if results.get("throughput_rows_sec", 0) > 0:
                    total_rows += results.get("throughput_rows_sec", 0) * results.get("total_duration", 0)
        
        manifest["benchmark_summary"] = {
            "total_duration_seconds": round(total_duration, 3),
            "total_rows_processed": round(total_rows, 0),
            "average_rows_per_second": round(total_rows / total_duration, 1) if total_duration > 0 else 0,
            "sheets_benchmarked": len(manifest["benchmark_results"])
        }

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Source workbook : {xlsx_path}")
    print(f"Output folder   : {out_dir}")
    print(f"Sheets exported : {exported}")
    print(f"Sheets skipped  : {skipped} (empty or no columns)")
    print(f"Manifest        : {os.path.join(out_dir, 'manifest.json')}")

if __name__ == "__main__":
    main()
```


Re-running the conversion to create the 7-day CSV:



Cycle calendar lookup succeeded: `26C01W01 (2025-12-30 to 2026-01-05)`. Verifying the 7-day CSV was created:



7-day CSV created: `2026_01_06_00_33_09_SCRPA_RMS_20260106_003600_ReportDate_Last7.csv`. Fixing the Unicode encoding issue in the logger, then verifying the date range:


```python
# export_excel_sheets_to_csv.py
# Changes: Added --all-sheets flag, timeouts, custom exceptions, JSON logging, tqdm progress, streaming writer

import argparse
import os
import re
import json
import hashlib
import time
import psutil
import shutil
from pathlib import Path
from datetime import datetime, time as dtime, date, timedelta as dtdelta
import fnmatch
import csv
import logging
import signal
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=UserWarning, module="dateutil.parser")

from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries, get_column_letter
from openpyxl.utils import column_index_from_string
import pandas as pd

# Custom Exceptions
class ExportTimeoutError(Exception):
    pass

class ExportError(Exception):
    pass

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('export_log.json')
handler.setFormatter(logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'))
logger.addHandler(handler)

# Timeout Handler (Windows compatible)
import threading
import time

def timeout_handler(timeout_seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)
            
            if thread.is_alive():
                raise ExportTimeoutError(f"Export timed out after {timeout_seconds} seconds")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        return wrapper
    return decorator

BASE_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack"
OUT_SUBFOLDER_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack\14_Excel\xlsx_to_csv"

# Archive configuration
ARCHIVE_BASE = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS")
RMS_ARCHIVE = ARCHIVE_BASE / "_RMS" / "SCRPA" / "archive"
CAD_ARCHIVE = ARCHIVE_BASE / "_CAD" / "SCRPA" / "archive"

_TIME_RE = re.compile(r"^\s*\d{1,2}:\d{2}(:\d{2})?\s*$")

def get_archive_folder(filepath: Path) -> Path:
    """Determine archive folder based on file path (CAD or RMS)"""
    folder = CAD_ARCHIVE if "_CAD" in str(filepath) else RMS_ARCHIVE
    folder.mkdir(parents=True, exist_ok=True)
    
    # Extract date from filename if present, else use today
    date_match = re.search(r"(\d{4}[-_]\d{2}[-_]\d{2})|(\d{8})", filepath.name)
    if date_match:
        date_str = date_match.group(0).replace("_", "-")
        # Normalize to YYYY-MM-DD format
        if len(date_str) == 8:  # YYYYMMDD
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    dated_folder = folder / date_str
    dated_folder.mkdir(exist_ok=True)
    return dated_folder

def archive_old_files(folder: Path, dry_run: bool = False, exclude_file: str = None):
    """Archive old .xlsx and .csv files from the working directory
    
    Args:
        folder: Directory to archive files from
        dry_run: If True, only show what would be archived
        exclude_file: Path to file to exclude from archiving (e.g., file being processed)
    """
    if not folder.exists():
        logger.info(f"Archive folder does not exist: {folder}")
        return 0
    
    script_name = Path(__file__).name
    archive_count = 0
    files_to_archive = []
    
    # Normalize exclude_file path for comparison
    exclude_path = None
    if exclude_file:
        exclude_path = Path(exclude_file).resolve()
    
    # Build set of Excel file timestamp prefixes to keep matching CSV files
    excel_timestamps = set()
    try:
        for item in folder.iterdir():
            try:
                if item.is_file() and item.suffix.lower() == ".xlsx" and item.name != script_name:
                    if "archive" not in str(item.parent):
                        # Extract timestamp prefix (format: YYYY_MM_DD_HH_MM_SS_SCRPA_RMS)
                        # CSV files will have same prefix: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                        stem = item.stem  # e.g., "2025_12_02_01_14_15_SCRPA_RMS"
                        excel_timestamps.add(stem)
            except (OSError, PermissionError) as e:
                logger.warning(f"Could not access file {item.name}: {e}")
                continue
    except Exception as e:
        logger.error(f"Error building Excel timestamp set: {e}")
        # Continue anyway - worst case we archive everything
    
    for item in folder.iterdir():
        try:
            if not item.is_file() or item.suffix.lower() not in {".xlsx", ".csv"} or item.name == script_name:
                continue
            
            # Skip files that are already in archive subdirectories
            if "archive" in str(item.parent):
                continue
            
            # Skip the file being processed
            try:
                if exclude_path and item.resolve() == exclude_path:
                    logger.debug(f"Skipping current file from archive: {item.name}")
                    continue
            except (OSError, PermissionError):
                # If we can't resolve the path, skip it
                continue
            
            # For CSV files: keep if they match an existing Excel file timestamp
            if item.suffix.lower() == ".csv":
                try:
                    csv_stem = item.stem
                    # Check if this CSV matches any Excel file timestamp
                    # CSV names: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                    # Excel names: {timestamp}_SCRPA_RMS.xlsx
                    matches_excel = False
                    for excel_stem in excel_timestamps:
                        # Check if CSV stem starts with Excel stem (handles both full CSV and Last7 CSV)
                        if csv_stem.startswith(excel_stem):
                            matches_excel = True
                            break
                    if matches_excel:
                        logger.debug(f"Keeping CSV file (matches Excel): {item.name}")
                        continue
                except Exception as e:
                    logger.warning(f"Error checking CSV file {item.name}: {e}")
                    # If we can't check, err on the side of caution and archive it
                    pass
            
            files_to_archive.append(item)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not process file {item.name}: {e}")
            continue
        except Exception as e:
            logger.warning(f"Unexpected error processing {item.name}: {e}")
            continue
    
    if not files_to_archive:
        logger.info("No files to archive")
        return 0
    
    if dry_run:
        print(f"\n[DRY-RUN] Would archive {len(files_to_archive)} file(s):")
        for item in files_to_archive:
            dest = get_archive_folder(item)
            print(f"  {item.name} -> {dest / item.name}")
        return len(files_to_archive)
    
    for item in files_to_archive:
        try:
            dest = get_archive_folder(item)
            dest_file = dest / item.name
            
            # Handle duplicates by adding timestamp
            if dest_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                stem = dest_file.stem
                suffix = dest_file.suffix
                dest_file = dest / f"{stem}_{timestamp}{suffix}"
            
            shutil.move(str(item), str(dest_file))
            archive_count += 1
            logger.info(f"Archived: {item.name} -> {dest_file}")
        except Exception as e:
            logger.warning(f"Failed to archive {item.name}: {e}")
    
    if archive_count > 0:
        logger.info(f"Archived {archive_count} file(s)")
    
    return archive_count

def sanitize_filename(name: str, used: set) -> str:
    fn = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name).strip().strip('.')
    fn = re.sub(r'[\s_]+', '_', fn)[:150] or "Sheet"
    original = fn
    i = 2
    while fn.lower() in used:
        fn = f"{original}_{i}"
        i += 1
    used.add(fn.lower())
    return fn

def resolve_output_parent(base: str, out_subfolder: str) -> str:
    base_abs = os.path.abspath(base)
    parent = out_subfolder
    if not os.path.isabs(parent):
        parent = os.path.join(base_abs, parent)
    parent = os.path.abspath(parent)
    norm_parent = os.path.normcase(parent)
    norm_base = os.path.normcase(base_abs)
    if not norm_parent.startswith(norm_base):
        raise ValueError(f"Output path must be inside the OneDrive base.\nBase: {base_abs}\nOutput: {parent}")
    return parent

def get_used(ws):
    try:
        dim = ws.calculate_dimension()
    except ValueError:
        # Handle unsized worksheets
        dim = ws.calculate_dimension(force=True)
    
    if dim in ("A1:A1", None):
        return 0, 0
    min_c, min_r, max_c, max_r = range_boundaries(dim)
    return max_r, max_c

def get_file_hash(path):
    if not os.path.exists(path):
        return None
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_adaptive_chunksize(file_size, available_memory):
    memory_threshold = available_memory * 0.5  # Use 50% of available memory
    if file_size > 100 * 1024 * 1024:
        return 1000
    elif file_size > 50 * 1024 * 1024:
        return 2000
    elif file_size > 10 * 1024 * 1024:
        return 5000
    return 10000

def benchmark_engine_performance(file_path, sheet_name, engine, is_detailed=False):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    start_mem = process.memory_info().rss / (1024 * 1024)  # MB
    start_cpu = process.cpu_percent(interval=0.1)

    load_start = time.time()
    if engine == 'calamine':
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
    else:
        wb = load_workbook(file_path, read_only=True, data_only=True)
        ws = wb[sheet_name]
    load_end = time.time()
    load_duration = load_end - load_start

    process_start = time.time()
    if engine == 'calamine':
        for _, row in df.iterrows():
            pass
    else:
        for row in ws.iter_rows():
            pass
    process_end = time.time()
    process_duration = process_end - process_start

    write_start = time.time()
    with open(os.devnull, 'w') as f:
        writer = csv.writer(f)
        if engine == 'calamine':
            for _, row in df.iterrows():
                writer.writerow(row)
        else:
            for row in ws.iter_rows(values_only=True):
                writer.writerow(row)
    write_end = time.time()
    write_duration = write_end - write_start

    end_time = time.time()
    end_mem = process.memory_info().rss / (1024 * 1024)
    end_cpu = process.cpu_percent(interval=0.1)

    total_duration = end_time - start_time
    rows, _ = _get_used_range(df if engine == 'calamine' else ws)
    throughput = rows / total_duration if total_duration > 0 else 0
    mem_peak = max(start_mem, end_mem)
    cpu_avg = (start_cpu + end_cpu) / 2

    results = {
        "total_duration": total_duration,
        "throughput_rows_sec": throughput,
        "memory_peak_mb": mem_peak,
        "cpu_avg_percent": cpu_avg
    }
    if is_detailed:
        results.update({
            "load_duration": load_duration,
            "process_duration": process_duration,
            "write_duration": write_duration,
            "file_size_mb": os.path.getsize(file_path) / (1024 * 1024)
        })
    return results

def _parse_af_columns(spec: str):
    """
    Accept 'A,B,C,D,E,F' or 'A-F' (case-insensitive). Return sorted 1-based column indexes.
    """
    spec = spec.strip().upper().replace(" ", "")
    cols = []
    if "-" in spec and "," not in spec:
        start, end = spec.split("-", 1)
        s = column_index_from_string(start)
        e = column_index_from_string(end)
        if s > e: s, e = e, s
        cols = list(range(s, e + 1))
    else:
        parts = [p for p in spec.split(",") if p]
        for p in parts:
            cols.append(column_index_from_string(p))
    return sorted(set(cols))

def _cell_value_as_text(ws, rr, cc, as_formulas: bool, date_fmt, dt_fmt, t_fmt, force_text=False):
    """
    Shared converter used by the gate: when as_formulas=True, emit '=...' for formula cells,
    else use normal _to_text() logic. 'force_text' only matters in formulas exporter.
    """
    cell = ws.cell(row=rr, column=cc)
    if as_formulas:
        is_formula = (getattr(cell, "data_type", None) == 'f') or (isinstance(cell.value, str) and cell.value.startswith("="))
        if is_formula:
            s = str(cell.value)
            return s if s.startswith("=") else "=" + s
        # fall through to normal text for non-formula
    # call the existing _to_text() in this file
    return _to_text(cell.value, date_fmt, dt_fmt, t_fmt)

def _to_text(value, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S"):
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return value
    # Handle pandas/calamine time-only values that may come as timedelta
    try:
        import pandas as _pd
        if isinstance(value, getattr(_pd, 'Timedelta', ())) or isinstance(value, dtdelta):
            total_seconds = int(value.total_seconds())
            # Normalize to within a day
            total_seconds = total_seconds % (24 * 3600)
            hh = total_seconds // 3600
            mm = (total_seconds % 3600) // 60
            ss = total_seconds % 60
            return f"{hh:02d}:{mm:02d}:{ss:02d}"
    except Exception:
        pass
    if isinstance(value, datetime):
        # If Excel stored a time-only value, the date part is often 1899-12-30
        if value.date().isoformat() == "1899-12-30":
            return value.strftime(t_fmt)
        # If time component is midnight, treat as date-only
        if value.hour == 0 and value.minute == 0 and value.second == 0 and value.microsecond == 0:
            return value.strftime(date_fmt)
        return value.strftime(dt_fmt)
    if isinstance(value, date):
        return value.strftime(date_fmt)
    if isinstance(value, dtime):
        return value.strftime(t_fmt)
    if isinstance(value, str) and _TIME_RE.match(value):
        parts = [int(p) for p in value.strip().split(":")]
        while len(parts) < 3:
            parts.append(0)
        return dtime(parts[0], parts[1], parts[2]).strftime(t_fmt)
    return str(value)

def _get_used_range(data):
    """Get used range for both openpyxl worksheets and pandas DataFrames"""
    if hasattr(data, 'calculate_dimension'):  # openpyxl worksheet
        try:
            dim = data.calculate_dimension()
        except ValueError:
            # Handle unsized worksheets
            dim = data.calculate_dimension(force=True)
        
        if dim in ("A1:A1", None):
            return 0, 0
        min_c, min_r, max_c, max_r = range_boundaries(dim)
        return max_r, max_c
    else:  # pandas DataFrame
        if data.empty:
            return 0, 0
        return len(data), len(data.columns)


def _iter_rows_pandas(df, visible_only, date_fmt, dt_fmt, t_fmt, af_columns, min_af_nonempty, af_gate_visible_only):
    """Iterate over pandas DataFrame rows for calamine engine"""
    af_cols = _parse_af_columns(af_columns)
    max_r, max_c = _get_used_range(df)
    if max_r == 0 or max_c == 0:
        return
    
    # Optionally emit header row when using pandas engine
    if getattr(df, "_include_headers", False):
        yield [str(col) for col in df.columns]

    for r, row in enumerate(df.itertuples(index=False), 1):
        if visible_only:
            # For pandas, we can't easily check row/column visibility
            # This would require additional metadata
            pass
            
        # A-F gate logic
        non_empty = 0
        af_values = []
        for c in af_cols:
            if c < len(row):
                val = row[c]
                af_values.append(val)
                if pd.notna(val) and val != "":
                    non_empty += 1
        
        if non_empty < min_af_nonempty:
            continue
        
        # Convert row to text
        row_out = []
        for val in row:
            formatted_val = _to_text(val, date_fmt, dt_fmt, t_fmt)
            row_out.append(formatted_val)
        
        if row_out and any(v != "" for v in row_out):
            yield row_out

def process_sheet_parallel(sheet_name, xlsx_path, out_dir, args, engine, used_names, benchmark_results, single_csv_basename=None):
    """Process a single sheet in parallel"""
    try:
        # Load sheet data based on engine
        if engine == "openpyxl":
            wb = load_workbook(xlsx_path, read_only=True, data_only=True)
            ws = wb[sheet_name]
            max_r, max_c = _get_used_range(ws)
            is_df = False
        else:  # calamine
            df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
            # Mark to include headers in pandas iteration
            setattr(df, "_include_headers", True)
            max_r, max_c = _get_used_range(df)
            is_df = True
        
        if not args.include_empty and (max_r == 0 or max_c == 0):
            return {"sheet_name": sheet_name, "status": "skipped", "reason": "empty"}
        
        safe = sanitize_filename(sheet_name, used_names)
        # If only one sheet is being exported, use the workbook name for CSV
        if single_csv_basename:
            csv_path = os.path.join(out_dir, f"{single_csv_basename}.csv")
        else:
            csv_path = os.path.join(out_dir, f"{safe}.csv")
        
        # Benchmark this sheet if requested
        if args.benchmark:
            benchmark_start = time.time()
        
        @timeout_handler(300)  # 5 min timeout
        def export_with_timeout():
            if args.engine == "openpyxl":
                return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
            else:  # calamine
                return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
        
        row_count, col_count = export_with_timeout()
        # Optional last-7 CSV for calamine path
        last7_path = None
        if is_df and args.report_last7:
            last7_path = _write_last7_by_reportdate_csv(df, csv_path, args.encoding, args.bom)
        
        # Record benchmark if requested
        if args.benchmark:
            benchmark_end = time.time()
            benchmark_results.append({
                "sheet_name": sheet_name,
                "engine": engine,
                "duration_seconds": round(benchmark_end - benchmark_start, 3),
                "rows": row_count,
                "cols": col_count,
                "rows_per_second": round(row_count / (benchmark_end - benchmark_start), 1) if (benchmark_end - benchmark_start) > 0 else 0
            })
        
        if engine == "openpyxl":
            wb.close()
        
        return {
            "sheet_name": sheet_name,
            "sanitized_name": safe,
            "file": csv_path,
            "file_sha256": get_file_hash(csv_path),
            "rows": row_count,
            "cols": col_count,
            "last7_file": last7_path,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error processing sheet {sheet_name}: {str(e)}")
        return {"sheet_name": sheet_name, "status": "error", "error": str(e)}

def _iter_rows(ws, visible_only: bool, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S", af_columns="A,B,C,D,E,F", min_af_nonempty=4, af_gate_visible_only=False):
    max_r, max_c = get_used(ws)
    merged_top_left = {}
    if hasattr(ws, 'merged_cells') and ws.merged_cells:
        for rng in ws.merged_cells.ranges:
            tl_r, tl_c = rng.min_row, rng.min_col
            for rr in range(rng.min_row, rng.max_row + 1):
                for cc in range(rng.min_col, rng.max_col + 1):
                    merged_top_left[(rr, cc)] = (tl_r, tl_c)
    
    af_cols = _parse_af_columns(af_columns)
    
    for r in tqdm(range(1, max_r + 1), desc="Processing rows"):
        if visible_only and ws.row_dimensions[r].hidden:
            continue
            
        # --- A–F gate (VALUES) ---
        try:
            nonempty = 0
            af_values = []
            for c in af_cols:
                # if visible-only gate, ignore hidden columns
                if af_gate_visible_only and visible_only:
                    col_letter = get_column_letter(c)
                    if ws.column_dimensions[col_letter].hidden:
                        continue
                rr, cc = merged_top_left.get((r, c), (r, c))
                txt = _cell_value_as_text(ws, rr, cc, as_formulas=False,
                                          date_fmt=date_fmt,
                                          dt_fmt=dt_fmt,
                                          t_fmt=t_fmt)
                af_values.append(txt)
                if txt != "":
                    nonempty += 1
            if nonempty < min_af_nonempty:
                continue
        except Exception:
            # fail-safe: if something odd, don't skip the row
            pass
        # --- end A–F gate ---
        
        row_out = []
        for c in range(1, max_c + 1):
            if visible_only and ws.column_dimensions[get_column_letter(c)].hidden:
                continue
            rr, cc = merged_top_left.get((r, c), (r, c))
            val = _to_text(ws.cell(row=rr, column=cc).value, date_fmt, dt_fmt, t_fmt)
            row_out.append(val)
        if row_out and any(v != "" for v in row_out):
            yield row_out

def _stream_write_csv(path, rows_iterable, encoding: str, bom: bool):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    row_count = 0
    max_cols_seen = 0
    with open(path, "w", encoding=final_encoding, newline="") as f:
        writer = csv.writer(f)
        for row in rows_iterable:
            if row is None:
                row = []
            writer.writerow(row)
            row_count += 1
            if isinstance(row, (list, tuple)):
                if len(row) > max_cols_seen:
                    max_cols_seen = len(row)
    return row_count, max_cols_seen

def _get_cycle_dates_from_calendar(report_date_str=None):
    """
    Get cycle 7-day start and end dates from cycle calendar.
    
    Args:
        report_date_str: Report date in MM/DD/YYYY format (from REPORT_DATE env var)
                        If None, uses today's date
    
    Returns:
        tuple (start_date, end_date) as date objects, or (None, None) if not found
    """
    CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20250414.csv"
    
    try:
        if not os.path.exists(CYCLE_CSV):
            logger.warning(f"Cycle calendar not found: {CYCLE_CSV}, using fallback calculation")
            return None, None
        
        cycle_df = pd.read_csv(CYCLE_CSV)
        
        # Determine lookup date
        if report_date_str:
            try:
                # Parse MM/DD/YYYY format
                lookup_date = pd.to_datetime(report_date_str, format="%m/%d/%Y").date()
                lookup_date_str = report_date_str
            except:
                logger.warning(f"Invalid REPORT_DATE format: {report_date_str}, using today")
                lookup_date = datetime.now().date()
                lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        else:
            lookup_date = datetime.now().date()
            lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        
        # Try exact match on Report_Due_Date first
        matching_row = cycle_df[cycle_df['Report_Due_Date'] == lookup_date_str]
        
        if not matching_row.empty:
            row = matching_row.iloc[0]
            start_date = pd.to_datetime(row['7_Day_Start']).date()
            end_date = pd.to_datetime(row['7_Day_End']).date()
            logger.info(f"Using cycle calendar: {row['Report_Name']} ({start_date} to {end_date})")
            return start_date, end_date
        
        # Fallback: find cycle where lookup_date falls within 7-day range
        for _, row in cycle_df.iterrows():
            try:
                start_date = pd.to_datetime(row['7_Day_Start']).date()
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if start_date <= lookup_date <= end_date:
                    logger.info(f"✅ Using cycle calendar (range match): {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        # If no match found, try most recent cycle where end_date <= lookup_date
        for _, row in cycle_df.iterrows():
            try:
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if end_date <= lookup_date:
                    start_date = pd.to_datetime(row['7_Day_Start']).date()
                    logger.info(f"✅ Using most recent cycle: {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        logger.warning(f"⚠️  No cycle found for date {lookup_date_str}, using fallback calculation")
        return None, None
        
    except Exception as e:
        logger.warning(f"⚠️  Error loading cycle calendar: {e}, using fallback calculation")
        return None, None

def _write_last7_by_reportdate_csv(df: pd.DataFrame, base_csv_path: str, encoding: str, bom: bool):
    """Write a filtered CSV with rows whose 'Report Date' falls within the cycle's 7-day range (from cycle calendar)."""
    if "Report Date" not in df.columns:
        return None
    
    # Get cycle dates from calendar (preferred) or fallback to simple calculation
    report_date_str = os.environ.get('REPORT_DATE', None)
    start_date, end_date = _get_cycle_dates_from_calendar(report_date_str)
    
    # Fallback to simple "last 7 days" if cycle calendar lookup failed
    if start_date is None or end_date is None:
        today = datetime.now().date()
        from datetime import timedelta
        start_date = today - timedelta(days=7)
        end_date = today
        logger.info(f"Using fallback: filtering last 7 days ({start_date} to {end_date})")
    
    dates = pd.to_datetime(df["Report Date"], errors="coerce")
    mask = (dates.dt.date >= start_date) & (dates.dt.date <= end_date)
    filtered = df[mask]
    
    # Use our custom formatting instead of pandas to_csv
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    out_path = os.path.splitext(base_csv_path)[0] + "_ReportDate_Last7.csv"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # Apply custom formatting and write using our streaming method
    def _iter_filtered_rows():
        # Emit headers first
        yield [str(col) for col in filtered.columns]
        # Emit formatted data rows
        for _, row in filtered.iterrows():
            row_out = []
            for val in row:
                formatted_val = _to_text(val, "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%H:%M:%S")
                row_out.append(formatted_val)
            yield row_out
    
    _stream_write_csv(out_path, _iter_filtered_rows(), encoding, bom)
    return out_path

def main():
    ap = argparse.ArgumentParser(description="Export all Excel sheets to individual CSV files.")
    ap.add_argument("--xlsx", required=False, help="Path to the source .xlsx (required unless --archive-only)")
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--out-subfolder", default=OUT_SUBFOLDER_DEFAULT)
    ap.add_argument("--encoding", default="utf-8")
    ap.add_argument("--no-bom", dest="bom", action="store_false")
    ap.add_argument("--visible-only", action="store_true", help="Export only visible rows and columns")
    ap.add_argument("--all-sheets", action="store_true", help="Export all sheets, ignoring include/exclude")
    ap.set_defaults(bom=True)
    ap.add_argument("--report-last7", action="store_true", help="Also write a *_ReportDate_Last7.csv filtered to last 7 days of Report Date (calamine engine only)")
    ap.add_argument("--include-empty", action="store_true")
    ap.add_argument("--na-rep", default="")
    ap.add_argument("--include", default=[], nargs="*", help="Include sheet patterns (substring match)")
    ap.add_argument("--exclude", default=[], nargs="*", help="Exclude sheet patterns (substring match)")
    ap.add_argument("--date-format", default="%Y-%m-%d", help="Date format string")
    ap.add_argument("--datetime-format", default="%Y-%m-%d %H:%M:%S", help="DateTime format string")
    ap.add_argument("--time-format", default="%H:%M:%S", help="Time format string")
    ap.add_argument("--af-columns", default="A,B,C",
                    help="Comma-separated list or Excel span (e.g., 'A-F') of columns to check for density gate.")
    ap.add_argument("--min-af-nonempty", type=int, default=2,
                    help="Minimum number of non-empty cells among --af-columns required to export a row.")
    ap.add_argument("--af-gate-visible-only", action="store_true",
                    help="If set, only visible cells among --af-columns count toward the threshold.")
    ap.add_argument("--disable-af-gate", action="store_true",
                    help="Disable A-F gate filtering (export all rows).")
    ap.add_argument("--engine", default="auto", choices=["auto", "calamine", "openpyxl"], 
                    help="Engine for reading Excel files (auto selects based on file size)")
    ap.add_argument("--chunksize", type=int, default=None, 
                    help="Read file in chunks of this size for large files (auto-enabled for 50MB+ files)")
    ap.add_argument("--benchmark", action="store_true", 
                    help="Enable performance benchmarking and include results in manifest")
    ap.add_argument("--parallel", action="store_true", 
                    help="Enable parallel sheet processing for better performance")
    ap.add_argument("--max-parallel-sheets", type=int, default=4, 
                    help="Maximum number of sheets to process in parallel (default: 4)")
    ap.add_argument("--archive-only", action="store_true",
                    help="Only archive old files and exit (no conversion)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Preview what would be archived without actually moving files")
    args = ap.parse_args()

    # Validate arguments
    if not args.archive_only and not args.xlsx:
        ap.error("--xlsx is required unless --archive-only is specified")

    # Handle archive-only mode
    if args.archive_only:
        working_dir = Path.cwd()
        exclude_file = None
        if args.xlsx:
            # If xlsx provided, use its parent directory and exclude this file
            xlsx_path = Path(args.xlsx).resolve()
            working_dir = xlsx_path.parent
            exclude_file = str(xlsx_path)
        count = archive_old_files(working_dir, dry_run=args.dry_run, exclude_file=exclude_file)
        if args.dry_run:
            print(f"\n[DRY-RUN] Would archive {count} file(s). Run without --dry-run to archive.")
        else:
            print(f"\nArchived {count} file(s).")
        return

    # Handle disable-af-gate option
    if args.disable_af_gate:
        args.min_af_nonempty = 0
        logger.info("A-F gate disabled - exporting all rows")

    xlsx_path = os.path.abspath(args.xlsx)
    
    # Auto-select engine and chunksize based on file size
    file_size = os.path.getsize(xlsx_path)
    available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
    
    if args.engine == "auto":
        # Use calamine for better performance on most files
        args.engine = "calamine"
    
    if args.chunksize is None:
        args.chunksize = get_adaptive_chunksize(file_size, available_memory)
        if file_size > 50 * 1024 * 1024:  # 50MB+
            logger.info(f"Large file detected ({file_size / (1024*1024):.1f}MB), enabling adaptive chunking with size {args.chunksize}")
    
    logger.info(f"Using engine: {args.engine}, chunksize: {args.chunksize}, available memory: {available_memory:.1f}MB")
    if not os.path.isfile(xlsx_path):
        logger.error(f"File not found: {xlsx_path}")
        raise FileNotFoundError(f"File not found: {xlsx_path}")

    out_parent = resolve_output_parent(args.base, args.out_subfolder)
    os.makedirs(out_parent, exist_ok=True)

    # Archive old files from the working directory (where xlsx files are)
    # EXCLUDE the current file being processed to prevent archiving it before conversion
    working_dir = Path(xlsx_path).parent
    if not args.dry_run:
        archive_old_files(working_dir, dry_run=False, exclude_file=xlsx_path)

    if args.out_subfolder != OUT_SUBFOLDER_DEFAULT:
        out_dir = out_parent
    else:
        wb_stem = os.path.splitext(os.path.basename(xlsx_path))[0]
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        out_dir = os.path.join(out_parent, f"{wb_stem}_{stamp}")
        os.makedirs(out_dir, exist_ok=True)

    # Initialize workbook based on engine
    wb = None
    if args.engine == "openpyxl":
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)
        sheet_names = wb.sheetnames
    else:  # calamine
        excel_file = pd.ExcelFile(xlsx_path, engine='calamine')
        sheet_names = excel_file.sheet_names
    
    used_names = set()
    exported = 0
    skipped = 0
    stats = {"rows_skipped_af_gate": 0}
    benchmark_results = []
    
    manifest = {
        "workbook": xlsx_path,
        "timestamp": datetime.now().isoformat(),
        "output_dir": out_dir,
        "workbook_sha256": get_file_hash(xlsx_path),
        "engine": args.engine,
        "chunksize": args.chunksize,
        "benchmark_enabled": bool(args.benchmark),
        "parallel_enabled": bool(args.parallel),
        "max_parallel_sheets": args.max_parallel_sheets,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "available_memory_mb": round(available_memory, 2),
        "rows_skipped_af_gate": stats.get("rows_skipped_af_gate", 0),
        "af_gate": {
            "columns": args.af_columns,
            "min_nonempty": args.min_af_nonempty,
            "visible_only": bool(args.af_gate_visible_only),
            "disabled": bool(args.disable_af_gate)
        },
        "sheets": [],
        "benchmark_results": []
    }

    # Filter sheets based on include/exclude
    filtered_sheets = []
    for sheet_name in sheet_names:
        if not args.all_sheets:
            if args.exclude and any(pat.lower() in sheet_name.lower() for pat in args.exclude):
                continue
            if args.include and not any(pat.lower() in sheet_name.lower() for pat in args.include):
                continue
        filtered_sheets.append(sheet_name)
    
    if args.parallel and len(filtered_sheets) > 1:
        # Parallel processing
        logger.info(f"Processing {len(filtered_sheets)} sheets in parallel (max {args.max_parallel_sheets} workers)")
        with ThreadPoolExecutor(max_workers=args.max_parallel_sheets) as executor:
            # Submit all tasks
            future_to_sheet = {
                executor.submit(process_sheet_parallel, sheet_name, xlsx_path, out_dir, args, args.engine, used_names, benchmark_results, None if len(filtered_sheets) != 1 else os.path.splitext(os.path.basename(xlsx_path))[0]): sheet_name 
                for sheet_name in filtered_sheets
            }
            
            # Process completed tasks
            for future in tqdm(as_completed(future_to_sheet), total=len(filtered_sheets), desc="Processing sheets"):
                sheet_name = future_to_sheet[future]
                try:
                    result = future.result()
                    if result["status"] == "success":
                        exported += 1
                        manifest["sheets"].append(result)
                    elif result["status"] == "skipped":
                        skipped += 1
                    else:
                        logger.error(f"Error processing {sheet_name}: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    logger.error(f"Exception processing {sheet_name}: {str(e)}")
    else:
        # Sequential processing (original logic)
        for sheet_name in tqdm(filtered_sheets, desc="Exporting sheets"):
            # Benchmarking
            if args.benchmark:
                benchmark_results = {}
                for eng in ['calamine', 'openpyxl']:
                    duration = benchmark_engine_performance(xlsx_path, sheet_name, eng, is_detailed=True)
                    benchmark_results[eng] = duration
                    logger.info(f"Benchmark: {sheet_name} with {eng} - {json.dumps(duration)}")
                manifest["benchmark_results"].append({"sheet_name": sheet_name, "results": benchmark_results})
            
            # Load sheet data based on engine
            if args.engine == "openpyxl":
                ws = wb[sheet_name]
                max_r, max_c = _get_used_range(ws)
                is_df = False
            else:  # calamine
                df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
                setattr(df, "_include_headers", True)
                max_r, max_c = _get_used_range(df)
                is_df = True
            
            if not args.include_empty and (max_r == 0 or max_c == 0):
                skipped += 1
                continue

            safe = sanitize_filename(sheet_name, used_names)
            # If only one sheet is being exported, use the workbook base name
            if len(filtered_sheets) == 1:
                csv_name = os.path.splitext(os.path.basename(xlsx_path))[0] + ".csv"
            else:
                csv_name = f"{safe}.csv"
            csv_path = os.path.join(out_dir, csv_name)
            try:
                @timeout_handler(300)  # 5 min timeout
                def export_with_timeout():
                    if args.engine == "openpyxl":
                        return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                    else:  # calamine
                        return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                
                row_count, col_count = export_with_timeout()
                if row_count == 0:
                    skipped += 1
                    continue
                exported += 1
                # Optional last-7 CSV (works with both engines now)
                last7_path = None
                if args.report_last7:
                    # Load the CSV we just created to filter it
                    try:
                        df_for_filter = pd.read_csv(csv_path, encoding=args.encoding)
                        last7_path = _write_last7_by_reportdate_csv(df_for_filter, csv_path, args.encoding, args.bom)
                    except Exception as e:
                        logger.warning(f"Could not create 7-day filtered CSV: {e}")
                        last7_path = None
                manifest["sheets"].append({
                    "sheet_name": sheet_name,
                    "sanitized_name": safe,
                    "file": csv_path,
                    "file_sha256": get_file_hash(csv_path),
                    "rows": row_count,
                    "cols": col_count,
                    "last7_file": last7_path
                })
            except ExportTimeoutError:
                logger.error(f"Timeout during export of {safe}")
                raise ExportError(f"Timeout exporting {safe}")
            except Exception as e:
                logger.error(f"Error exporting {safe}: {str(e)}")
                raise ExportError(f"Error exporting {safe}: {str(e)}")

    # Add benchmark results to manifest
    if args.benchmark and manifest["benchmark_results"]:
        # Calculate summary from benchmark results
        total_duration = 0
        total_rows = 0
        for benchmark in manifest["benchmark_results"]:
            for engine, results in benchmark["results"].items():
                total_duration += results.get("total_duration", 0)
                # Estimate rows from throughput
                if results.get("throughput_rows_sec", 0) > 0:
                    total_rows += results.get("throughput_rows_sec", 0) * results.get("total_duration", 0)
        
        manifest["benchmark_summary"] = {
            "total_duration_seconds": round(total_duration, 3),
            "total_rows_processed": round(total_rows, 0),
            "average_rows_per_second": round(total_rows / total_duration, 1) if total_duration > 0 else 0,
            "sheets_benchmarked": len(manifest["benchmark_results"])
        }

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Source workbook : {xlsx_path}")
    print(f"Output folder   : {out_dir}")
    print(f"Sheets exported : {exported}")
    print(f"Sheets skipped  : {skipped} (empty or no columns)")
    print(f"Manifest        : {os.path.join(out_dir, 'manifest.json')}")

if __name__ == "__main__":
    main()
```

```python
# export_excel_sheets_to_csv.py
# Changes: Added --all-sheets flag, timeouts, custom exceptions, JSON logging, tqdm progress, streaming writer

import argparse
import os
import re
import json
import hashlib
import time
import psutil
import shutil
from pathlib import Path
from datetime import datetime, time as dtime, date, timedelta as dtdelta
import fnmatch
import csv
import logging
import signal
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=UserWarning, module="dateutil.parser")

from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries, get_column_letter
from openpyxl.utils import column_index_from_string
import pandas as pd

# Custom Exceptions
class ExportTimeoutError(Exception):
    pass

class ExportError(Exception):
    pass

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('export_log.json')
handler.setFormatter(logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'))
logger.addHandler(handler)

# Timeout Handler (Windows compatible)
import threading
import time

def timeout_handler(timeout_seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)
            
            if thread.is_alive():
                raise ExportTimeoutError(f"Export timed out after {timeout_seconds} seconds")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        return wrapper
    return decorator

BASE_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack"
OUT_SUBFOLDER_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack\14_Excel\xlsx_to_csv"

# Archive configuration
ARCHIVE_BASE = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS")
RMS_ARCHIVE = ARCHIVE_BASE / "_RMS" / "SCRPA" / "archive"
CAD_ARCHIVE = ARCHIVE_BASE / "_CAD" / "SCRPA" / "archive"

_TIME_RE = re.compile(r"^\s*\d{1,2}:\d{2}(:\d{2})?\s*$")

def get_archive_folder(filepath: Path) -> Path:
    """Determine archive folder based on file path (CAD or RMS)"""
    folder = CAD_ARCHIVE if "_CAD" in str(filepath) else RMS_ARCHIVE
    folder.mkdir(parents=True, exist_ok=True)
    
    # Extract date from filename if present, else use today
    date_match = re.search(r"(\d{4}[-_]\d{2}[-_]\d{2})|(\d{8})", filepath.name)
    if date_match:
        date_str = date_match.group(0).replace("_", "-")
        # Normalize to YYYY-MM-DD format
        if len(date_str) == 8:  # YYYYMMDD
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    dated_folder = folder / date_str
    dated_folder.mkdir(exist_ok=True)
    return dated_folder

def archive_old_files(folder: Path, dry_run: bool = False, exclude_file: str = None):
    """Archive old .xlsx and .csv files from the working directory
    
    Args:
        folder: Directory to archive files from
        dry_run: If True, only show what would be archived
        exclude_file: Path to file to exclude from archiving (e.g., file being processed)
    """
    if not folder.exists():
        logger.info(f"Archive folder does not exist: {folder}")
        return 0
    
    script_name = Path(__file__).name
    archive_count = 0
    files_to_archive = []
    
    # Normalize exclude_file path for comparison
    exclude_path = None
    if exclude_file:
        exclude_path = Path(exclude_file).resolve()
    
    # Build set of Excel file timestamp prefixes to keep matching CSV files
    excel_timestamps = set()
    try:
        for item in folder.iterdir():
            try:
                if item.is_file() and item.suffix.lower() == ".xlsx" and item.name != script_name:
                    if "archive" not in str(item.parent):
                        # Extract timestamp prefix (format: YYYY_MM_DD_HH_MM_SS_SCRPA_RMS)
                        # CSV files will have same prefix: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                        stem = item.stem  # e.g., "2025_12_02_01_14_15_SCRPA_RMS"
                        excel_timestamps.add(stem)
            except (OSError, PermissionError) as e:
                logger.warning(f"Could not access file {item.name}: {e}")
                continue
    except Exception as e:
        logger.error(f"Error building Excel timestamp set: {e}")
        # Continue anyway - worst case we archive everything
    
    for item in folder.iterdir():
        try:
            if not item.is_file() or item.suffix.lower() not in {".xlsx", ".csv"} or item.name == script_name:
                continue
            
            # Skip files that are already in archive subdirectories
            if "archive" in str(item.parent):
                continue
            
            # Skip the file being processed
            try:
                if exclude_path and item.resolve() == exclude_path:
                    logger.debug(f"Skipping current file from archive: {item.name}")
                    continue
            except (OSError, PermissionError):
                # If we can't resolve the path, skip it
                continue
            
            # For CSV files: keep if they match an existing Excel file timestamp
            if item.suffix.lower() == ".csv":
                try:
                    csv_stem = item.stem
                    # Check if this CSV matches any Excel file timestamp
                    # CSV names: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                    # Excel names: {timestamp}_SCRPA_RMS.xlsx
                    matches_excel = False
                    for excel_stem in excel_timestamps:
                        # Check if CSV stem starts with Excel stem (handles both full CSV and Last7 CSV)
                        if csv_stem.startswith(excel_stem):
                            matches_excel = True
                            break
                    if matches_excel:
                        logger.debug(f"Keeping CSV file (matches Excel): {item.name}")
                        continue
                except Exception as e:
                    logger.warning(f"Error checking CSV file {item.name}: {e}")
                    # If we can't check, err on the side of caution and archive it
                    pass
            
            files_to_archive.append(item)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not process file {item.name}: {e}")
            continue
        except Exception as e:
            logger.warning(f"Unexpected error processing {item.name}: {e}")
            continue
    
    if not files_to_archive:
        logger.info("No files to archive")
        return 0
    
    if dry_run:
        print(f"\n[DRY-RUN] Would archive {len(files_to_archive)} file(s):")
        for item in files_to_archive:
            dest = get_archive_folder(item)
            print(f"  {item.name} -> {dest / item.name}")
        return len(files_to_archive)
    
    for item in files_to_archive:
        try:
            dest = get_archive_folder(item)
            dest_file = dest / item.name
            
            # Handle duplicates by adding timestamp
            if dest_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                stem = dest_file.stem
                suffix = dest_file.suffix
                dest_file = dest / f"{stem}_{timestamp}{suffix}"
            
            shutil.move(str(item), str(dest_file))
            archive_count += 1
            logger.info(f"Archived: {item.name} -> {dest_file}")
        except Exception as e:
            logger.warning(f"Failed to archive {item.name}: {e}")
    
    if archive_count > 0:
        logger.info(f"Archived {archive_count} file(s)")
    
    return archive_count

def sanitize_filename(name: str, used: set) -> str:
    fn = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name).strip().strip('.')
    fn = re.sub(r'[\s_]+', '_', fn)[:150] or "Sheet"
    original = fn
    i = 2
    while fn.lower() in used:
        fn = f"{original}_{i}"
        i += 1
    used.add(fn.lower())
    return fn

def resolve_output_parent(base: str, out_subfolder: str) -> str:
    base_abs = os.path.abspath(base)
    parent = out_subfolder
    if not os.path.isabs(parent):
        parent = os.path.join(base_abs, parent)
    parent = os.path.abspath(parent)
    norm_parent = os.path.normcase(parent)
    norm_base = os.path.normcase(base_abs)
    if not norm_parent.startswith(norm_base):
        raise ValueError(f"Output path must be inside the OneDrive base.\nBase: {base_abs}\nOutput: {parent}")
    return parent

def get_used(ws):
    try:
        dim = ws.calculate_dimension()
    except ValueError:
        # Handle unsized worksheets
        dim = ws.calculate_dimension(force=True)
    
    if dim in ("A1:A1", None):
        return 0, 0
    min_c, min_r, max_c, max_r = range_boundaries(dim)
    return max_r, max_c

def get_file_hash(path):
    if not os.path.exists(path):
        return None
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_adaptive_chunksize(file_size, available_memory):
    memory_threshold = available_memory * 0.5  # Use 50% of available memory
    if file_size > 100 * 1024 * 1024:
        return 1000
    elif file_size > 50 * 1024 * 1024:
        return 2000
    elif file_size > 10 * 1024 * 1024:
        return 5000
    return 10000

def benchmark_engine_performance(file_path, sheet_name, engine, is_detailed=False):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    start_mem = process.memory_info().rss / (1024 * 1024)  # MB
    start_cpu = process.cpu_percent(interval=0.1)

    load_start = time.time()
    if engine == 'calamine':
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
    else:
        wb = load_workbook(file_path, read_only=True, data_only=True)
        ws = wb[sheet_name]
    load_end = time.time()
    load_duration = load_end - load_start

    process_start = time.time()
    if engine == 'calamine':
        for _, row in df.iterrows():
            pass
    else:
        for row in ws.iter_rows():
            pass
    process_end = time.time()
    process_duration = process_end - process_start

    write_start = time.time()
    with open(os.devnull, 'w') as f:
        writer = csv.writer(f)
        if engine == 'calamine':
            for _, row in df.iterrows():
                writer.writerow(row)
        else:
            for row in ws.iter_rows(values_only=True):
                writer.writerow(row)
    write_end = time.time()
    write_duration = write_end - write_start

    end_time = time.time()
    end_mem = process.memory_info().rss / (1024 * 1024)
    end_cpu = process.cpu_percent(interval=0.1)

    total_duration = end_time - start_time
    rows, _ = _get_used_range(df if engine == 'calamine' else ws)
    throughput = rows / total_duration if total_duration > 0 else 0
    mem_peak = max(start_mem, end_mem)
    cpu_avg = (start_cpu + end_cpu) / 2

    results = {
        "total_duration": total_duration,
        "throughput_rows_sec": throughput,
        "memory_peak_mb": mem_peak,
        "cpu_avg_percent": cpu_avg
    }
    if is_detailed:
        results.update({
            "load_duration": load_duration,
            "process_duration": process_duration,
            "write_duration": write_duration,
            "file_size_mb": os.path.getsize(file_path) / (1024 * 1024)
        })
    return results

def _parse_af_columns(spec: str):
    """
    Accept 'A,B,C,D,E,F' or 'A-F' (case-insensitive). Return sorted 1-based column indexes.
    """
    spec = spec.strip().upper().replace(" ", "")
    cols = []
    if "-" in spec and "," not in spec:
        start, end = spec.split("-", 1)
        s = column_index_from_string(start)
        e = column_index_from_string(end)
        if s > e: s, e = e, s
        cols = list(range(s, e + 1))
    else:
        parts = [p for p in spec.split(",") if p]
        for p in parts:
            cols.append(column_index_from_string(p))
    return sorted(set(cols))

def _cell_value_as_text(ws, rr, cc, as_formulas: bool, date_fmt, dt_fmt, t_fmt, force_text=False):
    """
    Shared converter used by the gate: when as_formulas=True, emit '=...' for formula cells,
    else use normal _to_text() logic. 'force_text' only matters in formulas exporter.
    """
    cell = ws.cell(row=rr, column=cc)
    if as_formulas:
        is_formula = (getattr(cell, "data_type", None) == 'f') or (isinstance(cell.value, str) and cell.value.startswith("="))
        if is_formula:
            s = str(cell.value)
            return s if s.startswith("=") else "=" + s
        # fall through to normal text for non-formula
    # call the existing _to_text() in this file
    return _to_text(cell.value, date_fmt, dt_fmt, t_fmt)

def _to_text(value, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S"):
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return value
    # Handle pandas/calamine time-only values that may come as timedelta
    try:
        import pandas as _pd
        if isinstance(value, getattr(_pd, 'Timedelta', ())) or isinstance(value, dtdelta):
            total_seconds = int(value.total_seconds())
            # Normalize to within a day
            total_seconds = total_seconds % (24 * 3600)
            hh = total_seconds // 3600
            mm = (total_seconds % 3600) // 60
            ss = total_seconds % 60
            return f"{hh:02d}:{mm:02d}:{ss:02d}"
    except Exception:
        pass
    if isinstance(value, datetime):
        # If Excel stored a time-only value, the date part is often 1899-12-30
        if value.date().isoformat() == "1899-12-30":
            return value.strftime(t_fmt)
        # If time component is midnight, treat as date-only
        if value.hour == 0 and value.minute == 0 and value.second == 0 and value.microsecond == 0:
            return value.strftime(date_fmt)
        return value.strftime(dt_fmt)
    if isinstance(value, date):
        return value.strftime(date_fmt)
    if isinstance(value, dtime):
        return value.strftime(t_fmt)
    if isinstance(value, str) and _TIME_RE.match(value):
        parts = [int(p) for p in value.strip().split(":")]
        while len(parts) < 3:
            parts.append(0)
        return dtime(parts[0], parts[1], parts[2]).strftime(t_fmt)
    return str(value)

def _get_used_range(data):
    """Get used range for both openpyxl worksheets and pandas DataFrames"""
    if hasattr(data, 'calculate_dimension'):  # openpyxl worksheet
        try:
            dim = data.calculate_dimension()
        except ValueError:
            # Handle unsized worksheets
            dim = data.calculate_dimension(force=True)
        
        if dim in ("A1:A1", None):
            return 0, 0
        min_c, min_r, max_c, max_r = range_boundaries(dim)
        return max_r, max_c
    else:  # pandas DataFrame
        if data.empty:
            return 0, 0
        return len(data), len(data.columns)


def _iter_rows_pandas(df, visible_only, date_fmt, dt_fmt, t_fmt, af_columns, min_af_nonempty, af_gate_visible_only):
    """Iterate over pandas DataFrame rows for calamine engine"""
    af_cols = _parse_af_columns(af_columns)
    max_r, max_c = _get_used_range(df)
    if max_r == 0 or max_c == 0:
        return
    
    # Optionally emit header row when using pandas engine
    if getattr(df, "_include_headers", False):
        yield [str(col) for col in df.columns]

    for r, row in enumerate(df.itertuples(index=False), 1):
        if visible_only:
            # For pandas, we can't easily check row/column visibility
            # This would require additional metadata
            pass
            
        # A-F gate logic
        non_empty = 0
        af_values = []
        for c in af_cols:
            if c < len(row):
                val = row[c]
                af_values.append(val)
                if pd.notna(val) and val != "":
                    non_empty += 1
        
        if non_empty < min_af_nonempty:
            continue
        
        # Convert row to text
        row_out = []
        for val in row:
            formatted_val = _to_text(val, date_fmt, dt_fmt, t_fmt)
            row_out.append(formatted_val)
        
        if row_out and any(v != "" for v in row_out):
            yield row_out

def process_sheet_parallel(sheet_name, xlsx_path, out_dir, args, engine, used_names, benchmark_results, single_csv_basename=None):
    """Process a single sheet in parallel"""
    try:
        # Load sheet data based on engine
        if engine == "openpyxl":
            wb = load_workbook(xlsx_path, read_only=True, data_only=True)
            ws = wb[sheet_name]
            max_r, max_c = _get_used_range(ws)
            is_df = False
        else:  # calamine
            df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
            # Mark to include headers in pandas iteration
            setattr(df, "_include_headers", True)
            max_r, max_c = _get_used_range(df)
            is_df = True
        
        if not args.include_empty and (max_r == 0 or max_c == 0):
            return {"sheet_name": sheet_name, "status": "skipped", "reason": "empty"}
        
        safe = sanitize_filename(sheet_name, used_names)
        # If only one sheet is being exported, use the workbook name for CSV
        if single_csv_basename:
            csv_path = os.path.join(out_dir, f"{single_csv_basename}.csv")
        else:
            csv_path = os.path.join(out_dir, f"{safe}.csv")
        
        # Benchmark this sheet if requested
        if args.benchmark:
            benchmark_start = time.time()
        
        @timeout_handler(300)  # 5 min timeout
        def export_with_timeout():
            if args.engine == "openpyxl":
                return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
            else:  # calamine
                return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
        
        row_count, col_count = export_with_timeout()
        # Optional last-7 CSV for calamine path
        last7_path = None
        if is_df and args.report_last7:
            last7_path = _write_last7_by_reportdate_csv(df, csv_path, args.encoding, args.bom)
        
        # Record benchmark if requested
        if args.benchmark:
            benchmark_end = time.time()
            benchmark_results.append({
                "sheet_name": sheet_name,
                "engine": engine,
                "duration_seconds": round(benchmark_end - benchmark_start, 3),
                "rows": row_count,
                "cols": col_count,
                "rows_per_second": round(row_count / (benchmark_end - benchmark_start), 1) if (benchmark_end - benchmark_start) > 0 else 0
            })
        
        if engine == "openpyxl":
            wb.close()
        
        return {
            "sheet_name": sheet_name,
            "sanitized_name": safe,
            "file": csv_path,
            "file_sha256": get_file_hash(csv_path),
            "rows": row_count,
            "cols": col_count,
            "last7_file": last7_path,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error processing sheet {sheet_name}: {str(e)}")
        return {"sheet_name": sheet_name, "status": "error", "error": str(e)}

def _iter_rows(ws, visible_only: bool, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S", af_columns="A,B,C,D,E,F", min_af_nonempty=4, af_gate_visible_only=False):
    max_r, max_c = get_used(ws)
    merged_top_left = {}
    if hasattr(ws, 'merged_cells') and ws.merged_cells:
        for rng in ws.merged_cells.ranges:
            tl_r, tl_c = rng.min_row, rng.min_col
            for rr in range(rng.min_row, rng.max_row + 1):
                for cc in range(rng.min_col, rng.max_col + 1):
                    merged_top_left[(rr, cc)] = (tl_r, tl_c)
    
    af_cols = _parse_af_columns(af_columns)
    
    for r in tqdm(range(1, max_r + 1), desc="Processing rows"):
        if visible_only and ws.row_dimensions[r].hidden:
            continue
            
        # --- A–F gate (VALUES) ---
        try:
            nonempty = 0
            af_values = []
            for c in af_cols:
                # if visible-only gate, ignore hidden columns
                if af_gate_visible_only and visible_only:
                    col_letter = get_column_letter(c)
                    if ws.column_dimensions[col_letter].hidden:
                        continue
                rr, cc = merged_top_left.get((r, c), (r, c))
                txt = _cell_value_as_text(ws, rr, cc, as_formulas=False,
                                          date_fmt=date_fmt,
                                          dt_fmt=dt_fmt,
                                          t_fmt=t_fmt)
                af_values.append(txt)
                if txt != "":
                    nonempty += 1
            if nonempty < min_af_nonempty:
                continue
        except Exception:
            # fail-safe: if something odd, don't skip the row
            pass
        # --- end A–F gate ---
        
        row_out = []
        for c in range(1, max_c + 1):
            if visible_only and ws.column_dimensions[get_column_letter(c)].hidden:
                continue
            rr, cc = merged_top_left.get((r, c), (r, c))
            val = _to_text(ws.cell(row=rr, column=cc).value, date_fmt, dt_fmt, t_fmt)
            row_out.append(val)
        if row_out and any(v != "" for v in row_out):
            yield row_out

def _stream_write_csv(path, rows_iterable, encoding: str, bom: bool):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    row_count = 0
    max_cols_seen = 0
    with open(path, "w", encoding=final_encoding, newline="") as f:
        writer = csv.writer(f)
        for row in rows_iterable:
            if row is None:
                row = []
            writer.writerow(row)
            row_count += 1
            if isinstance(row, (list, tuple)):
                if len(row) > max_cols_seen:
                    max_cols_seen = len(row)
    return row_count, max_cols_seen

def _get_cycle_dates_from_calendar(report_date_str=None):
    """
    Get cycle 7-day start and end dates from cycle calendar.
    
    Args:
        report_date_str: Report date in MM/DD/YYYY format (from REPORT_DATE env var)
                        If None, uses today's date
    
    Returns:
        tuple (start_date, end_date) as date objects, or (None, None) if not found
    """
    CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20250414.csv"
    
    try:
        if not os.path.exists(CYCLE_CSV):
            logger.warning(f"Cycle calendar not found: {CYCLE_CSV}, using fallback calculation")
            return None, None
        
        cycle_df = pd.read_csv(CYCLE_CSV)
        
        # Determine lookup date
        if report_date_str:
            try:
                # Parse MM/DD/YYYY format
                lookup_date = pd.to_datetime(report_date_str, format="%m/%d/%Y").date()
                lookup_date_str = report_date_str
            except:
                logger.warning(f"Invalid REPORT_DATE format: {report_date_str}, using today")
                lookup_date = datetime.now().date()
                lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        else:
            lookup_date = datetime.now().date()
            lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        
        # Try exact match on Report_Due_Date first
        matching_row = cycle_df[cycle_df['Report_Due_Date'] == lookup_date_str]
        
        if not matching_row.empty:
            row = matching_row.iloc[0]
            start_date = pd.to_datetime(row['7_Day_Start']).date()
            end_date = pd.to_datetime(row['7_Day_End']).date()
            logger.info(f"Using cycle calendar: {row['Report_Name']} ({start_date} to {end_date})")
            return start_date, end_date
        
        # Fallback: find cycle where lookup_date falls within 7-day range
        for _, row in cycle_df.iterrows():
            try:
                start_date = pd.to_datetime(row['7_Day_Start']).date()
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if start_date <= lookup_date <= end_date:
                    logger.info(f"Using cycle calendar (range match): {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        # If no match found, try most recent cycle where end_date <= lookup_date
        for _, row in cycle_df.iterrows():
            try:
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if end_date <= lookup_date:
                    start_date = pd.to_datetime(row['7_Day_Start']).date()
                    logger.info(f"✅ Using most recent cycle: {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        logger.warning(f"⚠️  No cycle found for date {lookup_date_str}, using fallback calculation")
        return None, None
        
    except Exception as e:
        logger.warning(f"⚠️  Error loading cycle calendar: {e}, using fallback calculation")
        return None, None

def _write_last7_by_reportdate_csv(df: pd.DataFrame, base_csv_path: str, encoding: str, bom: bool):
    """Write a filtered CSV with rows whose 'Report Date' falls within the cycle's 7-day range (from cycle calendar)."""
    if "Report Date" not in df.columns:
        return None
    
    # Get cycle dates from calendar (preferred) or fallback to simple calculation
    report_date_str = os.environ.get('REPORT_DATE', None)
    start_date, end_date = _get_cycle_dates_from_calendar(report_date_str)
    
    # Fallback to simple "last 7 days" if cycle calendar lookup failed
    if start_date is None or end_date is None:
        today = datetime.now().date()
        from datetime import timedelta
        start_date = today - timedelta(days=7)
        end_date = today
        logger.info(f"Using fallback: filtering last 7 days ({start_date} to {end_date})")
    
    dates = pd.to_datetime(df["Report Date"], errors="coerce")
    mask = (dates.dt.date >= start_date) & (dates.dt.date <= end_date)
    filtered = df[mask]
    
    # Use our custom formatting instead of pandas to_csv
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    out_path = os.path.splitext(base_csv_path)[0] + "_ReportDate_Last7.csv"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # Apply custom formatting and write using our streaming method
    def _iter_filtered_rows():
        # Emit headers first
        yield [str(col) for col in filtered.columns]
        # Emit formatted data rows
        for _, row in filtered.iterrows():
            row_out = []
            for val in row:
                formatted_val = _to_text(val, "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%H:%M:%S")
                row_out.append(formatted_val)
            yield row_out
    
    _stream_write_csv(out_path, _iter_filtered_rows(), encoding, bom)
    return out_path

def main():
    ap = argparse.ArgumentParser(description="Export all Excel sheets to individual CSV files.")
    ap.add_argument("--xlsx", required=False, help="Path to the source .xlsx (required unless --archive-only)")
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--out-subfolder", default=OUT_SUBFOLDER_DEFAULT)
    ap.add_argument("--encoding", default="utf-8")
    ap.add_argument("--no-bom", dest="bom", action="store_false")
    ap.add_argument("--visible-only", action="store_true", help="Export only visible rows and columns")
    ap.add_argument("--all-sheets", action="store_true", help="Export all sheets, ignoring include/exclude")
    ap.set_defaults(bom=True)
    ap.add_argument("--report-last7", action="store_true", help="Also write a *_ReportDate_Last7.csv filtered to last 7 days of Report Date (calamine engine only)")
    ap.add_argument("--include-empty", action="store_true")
    ap.add_argument("--na-rep", default="")
    ap.add_argument("--include", default=[], nargs="*", help="Include sheet patterns (substring match)")
    ap.add_argument("--exclude", default=[], nargs="*", help="Exclude sheet patterns (substring match)")
    ap.add_argument("--date-format", default="%Y-%m-%d", help="Date format string")
    ap.add_argument("--datetime-format", default="%Y-%m-%d %H:%M:%S", help="DateTime format string")
    ap.add_argument("--time-format", default="%H:%M:%S", help="Time format string")
    ap.add_argument("--af-columns", default="A,B,C",
                    help="Comma-separated list or Excel span (e.g., 'A-F') of columns to check for density gate.")
    ap.add_argument("--min-af-nonempty", type=int, default=2,
                    help="Minimum number of non-empty cells among --af-columns required to export a row.")
    ap.add_argument("--af-gate-visible-only", action="store_true",
                    help="If set, only visible cells among --af-columns count toward the threshold.")
    ap.add_argument("--disable-af-gate", action="store_true",
                    help="Disable A-F gate filtering (export all rows).")
    ap.add_argument("--engine", default="auto", choices=["auto", "calamine", "openpyxl"], 
                    help="Engine for reading Excel files (auto selects based on file size)")
    ap.add_argument("--chunksize", type=int, default=None, 
                    help="Read file in chunks of this size for large files (auto-enabled for 50MB+ files)")
    ap.add_argument("--benchmark", action="store_true", 
                    help="Enable performance benchmarking and include results in manifest")
    ap.add_argument("--parallel", action="store_true", 
                    help="Enable parallel sheet processing for better performance")
    ap.add_argument("--max-parallel-sheets", type=int, default=4, 
                    help="Maximum number of sheets to process in parallel (default: 4)")
    ap.add_argument("--archive-only", action="store_true",
                    help="Only archive old files and exit (no conversion)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Preview what would be archived without actually moving files")
    args = ap.parse_args()

    # Validate arguments
    if not args.archive_only and not args.xlsx:
        ap.error("--xlsx is required unless --archive-only is specified")

    # Handle archive-only mode
    if args.archive_only:
        working_dir = Path.cwd()
        exclude_file = None
        if args.xlsx:
            # If xlsx provided, use its parent directory and exclude this file
            xlsx_path = Path(args.xlsx).resolve()
            working_dir = xlsx_path.parent
            exclude_file = str(xlsx_path)
        count = archive_old_files(working_dir, dry_run=args.dry_run, exclude_file=exclude_file)
        if args.dry_run:
            print(f"\n[DRY-RUN] Would archive {count} file(s). Run without --dry-run to archive.")
        else:
            print(f"\nArchived {count} file(s).")
        return

    # Handle disable-af-gate option
    if args.disable_af_gate:
        args.min_af_nonempty = 0
        logger.info("A-F gate disabled - exporting all rows")

    xlsx_path = os.path.abspath(args.xlsx)
    
    # Auto-select engine and chunksize based on file size
    file_size = os.path.getsize(xlsx_path)
    available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
    
    if args.engine == "auto":
        # Use calamine for better performance on most files
        args.engine = "calamine"
    
    if args.chunksize is None:
        args.chunksize = get_adaptive_chunksize(file_size, available_memory)
        if file_size > 50 * 1024 * 1024:  # 50MB+
            logger.info(f"Large file detected ({file_size / (1024*1024):.1f}MB), enabling adaptive chunking with size {args.chunksize}")
    
    logger.info(f"Using engine: {args.engine}, chunksize: {args.chunksize}, available memory: {available_memory:.1f}MB")
    if not os.path.isfile(xlsx_path):
        logger.error(f"File not found: {xlsx_path}")
        raise FileNotFoundError(f"File not found: {xlsx_path}")

    out_parent = resolve_output_parent(args.base, args.out_subfolder)
    os.makedirs(out_parent, exist_ok=True)

    # Archive old files from the working directory (where xlsx files are)
    # EXCLUDE the current file being processed to prevent archiving it before conversion
    working_dir = Path(xlsx_path).parent
    if not args.dry_run:
        archive_old_files(working_dir, dry_run=False, exclude_file=xlsx_path)

    if args.out_subfolder != OUT_SUBFOLDER_DEFAULT:
        out_dir = out_parent
    else:
        wb_stem = os.path.splitext(os.path.basename(xlsx_path))[0]
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        out_dir = os.path.join(out_parent, f"{wb_stem}_{stamp}")
        os.makedirs(out_dir, exist_ok=True)

    # Initialize workbook based on engine
    wb = None
    if args.engine == "openpyxl":
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)
        sheet_names = wb.sheetnames
    else:  # calamine
        excel_file = pd.ExcelFile(xlsx_path, engine='calamine')
        sheet_names = excel_file.sheet_names
    
    used_names = set()
    exported = 0
    skipped = 0
    stats = {"rows_skipped_af_gate": 0}
    benchmark_results = []
    
    manifest = {
        "workbook": xlsx_path,
        "timestamp": datetime.now().isoformat(),
        "output_dir": out_dir,
        "workbook_sha256": get_file_hash(xlsx_path),
        "engine": args.engine,
        "chunksize": args.chunksize,
        "benchmark_enabled": bool(args.benchmark),
        "parallel_enabled": bool(args.parallel),
        "max_parallel_sheets": args.max_parallel_sheets,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "available_memory_mb": round(available_memory, 2),
        "rows_skipped_af_gate": stats.get("rows_skipped_af_gate", 0),
        "af_gate": {
            "columns": args.af_columns,
            "min_nonempty": args.min_af_nonempty,
            "visible_only": bool(args.af_gate_visible_only),
            "disabled": bool(args.disable_af_gate)
        },
        "sheets": [],
        "benchmark_results": []
    }

    # Filter sheets based on include/exclude
    filtered_sheets = []
    for sheet_name in sheet_names:
        if not args.all_sheets:
            if args.exclude and any(pat.lower() in sheet_name.lower() for pat in args.exclude):
                continue
            if args.include and not any(pat.lower() in sheet_name.lower() for pat in args.include):
                continue
        filtered_sheets.append(sheet_name)
    
    if args.parallel and len(filtered_sheets) > 1:
        # Parallel processing
        logger.info(f"Processing {len(filtered_sheets)} sheets in parallel (max {args.max_parallel_sheets} workers)")
        with ThreadPoolExecutor(max_workers=args.max_parallel_sheets) as executor:
            # Submit all tasks
            future_to_sheet = {
                executor.submit(process_sheet_parallel, sheet_name, xlsx_path, out_dir, args, args.engine, used_names, benchmark_results, None if len(filtered_sheets) != 1 else os.path.splitext(os.path.basename(xlsx_path))[0]): sheet_name 
                for sheet_name in filtered_sheets
            }
            
            # Process completed tasks
            for future in tqdm(as_completed(future_to_sheet), total=len(filtered_sheets), desc="Processing sheets"):
                sheet_name = future_to_sheet[future]
                try:
                    result = future.result()
                    if result["status"] == "success":
                        exported += 1
                        manifest["sheets"].append(result)
                    elif result["status"] == "skipped":
                        skipped += 1
                    else:
                        logger.error(f"Error processing {sheet_name}: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    logger.error(f"Exception processing {sheet_name}: {str(e)}")
    else:
        # Sequential processing (original logic)
        for sheet_name in tqdm(filtered_sheets, desc="Exporting sheets"):
            # Benchmarking
            if args.benchmark:
                benchmark_results = {}
                for eng in ['calamine', 'openpyxl']:
                    duration = benchmark_engine_performance(xlsx_path, sheet_name, eng, is_detailed=True)
                    benchmark_results[eng] = duration
                    logger.info(f"Benchmark: {sheet_name} with {eng} - {json.dumps(duration)}")
                manifest["benchmark_results"].append({"sheet_name": sheet_name, "results": benchmark_results})
            
            # Load sheet data based on engine
            if args.engine == "openpyxl":
                ws = wb[sheet_name]
                max_r, max_c = _get_used_range(ws)
                is_df = False
            else:  # calamine
                df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
                setattr(df, "_include_headers", True)
                max_r, max_c = _get_used_range(df)
                is_df = True
            
            if not args.include_empty and (max_r == 0 or max_c == 0):
                skipped += 1
                continue

            safe = sanitize_filename(sheet_name, used_names)
            # If only one sheet is being exported, use the workbook base name
            if len(filtered_sheets) == 1:
                csv_name = os.path.splitext(os.path.basename(xlsx_path))[0] + ".csv"
            else:
                csv_name = f"{safe}.csv"
            csv_path = os.path.join(out_dir, csv_name)
            try:
                @timeout_handler(300)  # 5 min timeout
                def export_with_timeout():
                    if args.engine == "openpyxl":
                        return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                    else:  # calamine
                        return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                
                row_count, col_count = export_with_timeout()
                if row_count == 0:
                    skipped += 1
                    continue
                exported += 1
                # Optional last-7 CSV (works with both engines now)
                last7_path = None
                if args.report_last7:
                    # Load the CSV we just created to filter it
                    try:
                        df_for_filter = pd.read_csv(csv_path, encoding=args.encoding)
                        last7_path = _write_last7_by_reportdate_csv(df_for_filter, csv_path, args.encoding, args.bom)
                    except Exception as e:
                        logger.warning(f"Could not create 7-day filtered CSV: {e}")
                        last7_path = None
                manifest["sheets"].append({
                    "sheet_name": sheet_name,
                    "sanitized_name": safe,
                    "file": csv_path,
                    "file_sha256": get_file_hash(csv_path),
                    "rows": row_count,
                    "cols": col_count,
                    "last7_file": last7_path
                })
            except ExportTimeoutError:
                logger.error(f"Timeout during export of {safe}")
                raise ExportError(f"Timeout exporting {safe}")
            except Exception as e:
                logger.error(f"Error exporting {safe}: {str(e)}")
                raise ExportError(f"Error exporting {safe}: {str(e)}")

    # Add benchmark results to manifest
    if args.benchmark and manifest["benchmark_results"]:
        # Calculate summary from benchmark results
        total_duration = 0
        total_rows = 0
        for benchmark in manifest["benchmark_results"]:
            for engine, results in benchmark["results"].items():
                total_duration += results.get("total_duration", 0)
                # Estimate rows from throughput
                if results.get("throughput_rows_sec", 0) > 0:
                    total_rows += results.get("throughput_rows_sec", 0) * results.get("total_duration", 0)
        
        manifest["benchmark_summary"] = {
            "total_duration_seconds": round(total_duration, 3),
            "total_rows_processed": round(total_rows, 0),
            "average_rows_per_second": round(total_rows / total_duration, 1) if total_duration > 0 else 0,
            "sheets_benchmarked": len(manifest["benchmark_results"])
        }

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Source workbook : {xlsx_path}")
    print(f"Output folder   : {out_dir}")
    print(f"Sheets exported : {exported}")
    print(f"Sheets skipped  : {skipped} (empty or no columns)")
    print(f"Manifest        : {os.path.join(out_dir, 'manifest.json')}")

if __name__ == "__main__":
    main()
```

```python
# export_excel_sheets_to_csv.py
# Changes: Added --all-sheets flag, timeouts, custom exceptions, JSON logging, tqdm progress, streaming writer

import argparse
import os
import re
import json
import hashlib
import time
import psutil
import shutil
from pathlib import Path
from datetime import datetime, time as dtime, date, timedelta as dtdelta
import fnmatch
import csv
import logging
import signal
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=UserWarning, module="dateutil.parser")

from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries, get_column_letter
from openpyxl.utils import column_index_from_string
import pandas as pd

# Custom Exceptions
class ExportTimeoutError(Exception):
    pass

class ExportError(Exception):
    pass

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.FileHandler('export_log.json')
handler.setFormatter(logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'))
logger.addHandler(handler)

# Timeout Handler (Windows compatible)
import threading
import time

def timeout_handler(timeout_seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)
            
            if thread.is_alive():
                raise ExportTimeoutError(f"Export timed out after {timeout_seconds} seconds")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        return wrapper
    return decorator

BASE_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack"
OUT_SUBFOLDER_DEFAULT = r"C:\Users\carucci_r\OneDrive - City of Hackensack\14_Excel\xlsx_to_csv"

# Archive configuration
ARCHIVE_BASE = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS")
RMS_ARCHIVE = ARCHIVE_BASE / "_RMS" / "SCRPA" / "archive"
CAD_ARCHIVE = ARCHIVE_BASE / "_CAD" / "SCRPA" / "archive"

_TIME_RE = re.compile(r"^\s*\d{1,2}:\d{2}(:\d{2})?\s*$")

def get_archive_folder(filepath: Path) -> Path:
    """Determine archive folder based on file path (CAD or RMS)"""
    folder = CAD_ARCHIVE if "_CAD" in str(filepath) else RMS_ARCHIVE
    folder.mkdir(parents=True, exist_ok=True)
    
    # Extract date from filename if present, else use today
    date_match = re.search(r"(\d{4}[-_]\d{2}[-_]\d{2})|(\d{8})", filepath.name)
    if date_match:
        date_str = date_match.group(0).replace("_", "-")
        # Normalize to YYYY-MM-DD format
        if len(date_str) == 8:  # YYYYMMDD
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    dated_folder = folder / date_str
    dated_folder.mkdir(exist_ok=True)
    return dated_folder

def archive_old_files(folder: Path, dry_run: bool = False, exclude_file: str = None):
    """Archive old .xlsx and .csv files from the working directory
    
    Args:
        folder: Directory to archive files from
        dry_run: If True, only show what would be archived
        exclude_file: Path to file to exclude from archiving (e.g., file being processed)
    """
    if not folder.exists():
        logger.info(f"Archive folder does not exist: {folder}")
        return 0
    
    script_name = Path(__file__).name
    archive_count = 0
    files_to_archive = []
    
    # Normalize exclude_file path for comparison
    exclude_path = None
    if exclude_file:
        exclude_path = Path(exclude_file).resolve()
    
    # Build set of Excel file timestamp prefixes to keep matching CSV files
    excel_timestamps = set()
    try:
        for item in folder.iterdir():
            try:
                if item.is_file() and item.suffix.lower() == ".xlsx" and item.name != script_name:
                    if "archive" not in str(item.parent):
                        # Extract timestamp prefix (format: YYYY_MM_DD_HH_MM_SS_SCRPA_RMS)
                        # CSV files will have same prefix: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                        stem = item.stem  # e.g., "2025_12_02_01_14_15_SCRPA_RMS"
                        excel_timestamps.add(stem)
            except (OSError, PermissionError) as e:
                logger.warning(f"Could not access file {item.name}: {e}")
                continue
    except Exception as e:
        logger.error(f"Error building Excel timestamp set: {e}")
        # Continue anyway - worst case we archive everything
    
    for item in folder.iterdir():
        try:
            if not item.is_file() or item.suffix.lower() not in {".xlsx", ".csv"} or item.name == script_name:
                continue
            
            # Skip files that are already in archive subdirectories
            if "archive" in str(item.parent):
                continue
            
            # Skip the file being processed
            try:
                if exclude_path and item.resolve() == exclude_path:
                    logger.debug(f"Skipping current file from archive: {item.name}")
                    continue
            except (OSError, PermissionError):
                # If we can't resolve the path, skip it
                continue
            
            # For CSV files: keep if they match an existing Excel file timestamp
            if item.suffix.lower() == ".csv":
                try:
                    csv_stem = item.stem
                    # Check if this CSV matches any Excel file timestamp
                    # CSV names: {timestamp}_SCRPA_RMS.csv or {timestamp}_SCRPA_RMS_ReportDate_Last7.csv
                    # Excel names: {timestamp}_SCRPA_RMS.xlsx
                    matches_excel = False
                    for excel_stem in excel_timestamps:
                        # Check if CSV stem starts with Excel stem (handles both full CSV and Last7 CSV)
                        if csv_stem.startswith(excel_stem):
                            matches_excel = True
                            break
                    if matches_excel:
                        logger.debug(f"Keeping CSV file (matches Excel): {item.name}")
                        continue
                except Exception as e:
                    logger.warning(f"Error checking CSV file {item.name}: {e}")
                    # If we can't check, err on the side of caution and archive it
                    pass
            
            files_to_archive.append(item)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not process file {item.name}: {e}")
            continue
        except Exception as e:
            logger.warning(f"Unexpected error processing {item.name}: {e}")
            continue
    
    if not files_to_archive:
        logger.info("No files to archive")
        return 0
    
    if dry_run:
        print(f"\n[DRY-RUN] Would archive {len(files_to_archive)} file(s):")
        for item in files_to_archive:
            dest = get_archive_folder(item)
            print(f"  {item.name} -> {dest / item.name}")
        return len(files_to_archive)
    
    for item in files_to_archive:
        try:
            dest = get_archive_folder(item)
            dest_file = dest / item.name
            
            # Handle duplicates by adding timestamp
            if dest_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                stem = dest_file.stem
                suffix = dest_file.suffix
                dest_file = dest / f"{stem}_{timestamp}{suffix}"
            
            shutil.move(str(item), str(dest_file))
            archive_count += 1
            logger.info(f"Archived: {item.name} -> {dest_file}")
        except Exception as e:
            logger.warning(f"Failed to archive {item.name}: {e}")
    
    if archive_count > 0:
        logger.info(f"Archived {archive_count} file(s)")
    
    return archive_count

def sanitize_filename(name: str, used: set) -> str:
    fn = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', name).strip().strip('.')
    fn = re.sub(r'[\s_]+', '_', fn)[:150] or "Sheet"
    original = fn
    i = 2
    while fn.lower() in used:
        fn = f"{original}_{i}"
        i += 1
    used.add(fn.lower())
    return fn

def resolve_output_parent(base: str, out_subfolder: str) -> str:
    base_abs = os.path.abspath(base)
    parent = out_subfolder
    if not os.path.isabs(parent):
        parent = os.path.join(base_abs, parent)
    parent = os.path.abspath(parent)
    norm_parent = os.path.normcase(parent)
    norm_base = os.path.normcase(base_abs)
    if not norm_parent.startswith(norm_base):
        raise ValueError(f"Output path must be inside the OneDrive base.\nBase: {base_abs}\nOutput: {parent}")
    return parent

def get_used(ws):
    try:
        dim = ws.calculate_dimension()
    except ValueError:
        # Handle unsized worksheets
        dim = ws.calculate_dimension(force=True)
    
    if dim in ("A1:A1", None):
        return 0, 0
    min_c, min_r, max_c, max_r = range_boundaries(dim)
    return max_r, max_c

def get_file_hash(path):
    if not os.path.exists(path):
        return None
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_adaptive_chunksize(file_size, available_memory):
    memory_threshold = available_memory * 0.5  # Use 50% of available memory
    if file_size > 100 * 1024 * 1024:
        return 1000
    elif file_size > 50 * 1024 * 1024:
        return 2000
    elif file_size > 10 * 1024 * 1024:
        return 5000
    return 10000

def benchmark_engine_performance(file_path, sheet_name, engine, is_detailed=False):
    process = psutil.Process(os.getpid())
    start_time = time.time()
    start_mem = process.memory_info().rss / (1024 * 1024)  # MB
    start_cpu = process.cpu_percent(interval=0.1)

    load_start = time.time()
    if engine == 'calamine':
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
    else:
        wb = load_workbook(file_path, read_only=True, data_only=True)
        ws = wb[sheet_name]
    load_end = time.time()
    load_duration = load_end - load_start

    process_start = time.time()
    if engine == 'calamine':
        for _, row in df.iterrows():
            pass
    else:
        for row in ws.iter_rows():
            pass
    process_end = time.time()
    process_duration = process_end - process_start

    write_start = time.time()
    with open(os.devnull, 'w') as f:
        writer = csv.writer(f)
        if engine == 'calamine':
            for _, row in df.iterrows():
                writer.writerow(row)
        else:
            for row in ws.iter_rows(values_only=True):
                writer.writerow(row)
    write_end = time.time()
    write_duration = write_end - write_start

    end_time = time.time()
    end_mem = process.memory_info().rss / (1024 * 1024)
    end_cpu = process.cpu_percent(interval=0.1)

    total_duration = end_time - start_time
    rows, _ = _get_used_range(df if engine == 'calamine' else ws)
    throughput = rows / total_duration if total_duration > 0 else 0
    mem_peak = max(start_mem, end_mem)
    cpu_avg = (start_cpu + end_cpu) / 2

    results = {
        "total_duration": total_duration,
        "throughput_rows_sec": throughput,
        "memory_peak_mb": mem_peak,
        "cpu_avg_percent": cpu_avg
    }
    if is_detailed:
        results.update({
            "load_duration": load_duration,
            "process_duration": process_duration,
            "write_duration": write_duration,
            "file_size_mb": os.path.getsize(file_path) / (1024 * 1024)
        })
    return results

def _parse_af_columns(spec: str):
    """
    Accept 'A,B,C,D,E,F' or 'A-F' (case-insensitive). Return sorted 1-based column indexes.
    """
    spec = spec.strip().upper().replace(" ", "")
    cols = []
    if "-" in spec and "," not in spec:
        start, end = spec.split("-", 1)
        s = column_index_from_string(start)
        e = column_index_from_string(end)
        if s > e: s, e = e, s
        cols = list(range(s, e + 1))
    else:
        parts = [p for p in spec.split(",") if p]
        for p in parts:
            cols.append(column_index_from_string(p))
    return sorted(set(cols))

def _cell_value_as_text(ws, rr, cc, as_formulas: bool, date_fmt, dt_fmt, t_fmt, force_text=False):
    """
    Shared converter used by the gate: when as_formulas=True, emit '=...' for formula cells,
    else use normal _to_text() logic. 'force_text' only matters in formulas exporter.
    """
    cell = ws.cell(row=rr, column=cc)
    if as_formulas:
        is_formula = (getattr(cell, "data_type", None) == 'f') or (isinstance(cell.value, str) and cell.value.startswith("="))
        if is_formula:
            s = str(cell.value)
            return s if s.startswith("=") else "=" + s
        # fall through to normal text for non-formula
    # call the existing _to_text() in this file
    return _to_text(cell.value, date_fmt, dt_fmt, t_fmt)

def _to_text(value, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S"):
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return value
    # Handle pandas/calamine time-only values that may come as timedelta
    try:
        import pandas as _pd
        if isinstance(value, getattr(_pd, 'Timedelta', ())) or isinstance(value, dtdelta):
            total_seconds = int(value.total_seconds())
            # Normalize to within a day
            total_seconds = total_seconds % (24 * 3600)
            hh = total_seconds // 3600
            mm = (total_seconds % 3600) // 60
            ss = total_seconds % 60
            return f"{hh:02d}:{mm:02d}:{ss:02d}"
    except Exception:
        pass
    if isinstance(value, datetime):
        # If Excel stored a time-only value, the date part is often 1899-12-30
        if value.date().isoformat() == "1899-12-30":
            return value.strftime(t_fmt)
        # If time component is midnight, treat as date-only
        if value.hour == 0 and value.minute == 0 and value.second == 0 and value.microsecond == 0:
            return value.strftime(date_fmt)
        return value.strftime(dt_fmt)
    if isinstance(value, date):
        return value.strftime(date_fmt)
    if isinstance(value, dtime):
        return value.strftime(t_fmt)
    if isinstance(value, str) and _TIME_RE.match(value):
        parts = [int(p) for p in value.strip().split(":")]
        while len(parts) < 3:
            parts.append(0)
        return dtime(parts[0], parts[1], parts[2]).strftime(t_fmt)
    return str(value)

def _get_used_range(data):
    """Get used range for both openpyxl worksheets and pandas DataFrames"""
    if hasattr(data, 'calculate_dimension'):  # openpyxl worksheet
        try:
            dim = data.calculate_dimension()
        except ValueError:
            # Handle unsized worksheets
            dim = data.calculate_dimension(force=True)
        
        if dim in ("A1:A1", None):
            return 0, 0
        min_c, min_r, max_c, max_r = range_boundaries(dim)
        return max_r, max_c
    else:  # pandas DataFrame
        if data.empty:
            return 0, 0
        return len(data), len(data.columns)


def _iter_rows_pandas(df, visible_only, date_fmt, dt_fmt, t_fmt, af_columns, min_af_nonempty, af_gate_visible_only):
    """Iterate over pandas DataFrame rows for calamine engine"""
    af_cols = _parse_af_columns(af_columns)
    max_r, max_c = _get_used_range(df)
    if max_r == 0 or max_c == 0:
        return
    
    # Optionally emit header row when using pandas engine
    if getattr(df, "_include_headers", False):
        yield [str(col) for col in df.columns]

    for r, row in enumerate(df.itertuples(index=False), 1):
        if visible_only:
            # For pandas, we can't easily check row/column visibility
            # This would require additional metadata
            pass
            
        # A-F gate logic
        non_empty = 0
        af_values = []
        for c in af_cols:
            if c < len(row):
                val = row[c]
                af_values.append(val)
                if pd.notna(val) and val != "":
                    non_empty += 1
        
        if non_empty < min_af_nonempty:
            continue
        
        # Convert row to text
        row_out = []
        for val in row:
            formatted_val = _to_text(val, date_fmt, dt_fmt, t_fmt)
            row_out.append(formatted_val)
        
        if row_out and any(v != "" for v in row_out):
            yield row_out

def process_sheet_parallel(sheet_name, xlsx_path, out_dir, args, engine, used_names, benchmark_results, single_csv_basename=None):
    """Process a single sheet in parallel"""
    try:
        # Load sheet data based on engine
        if engine == "openpyxl":
            wb = load_workbook(xlsx_path, read_only=True, data_only=True)
            ws = wb[sheet_name]
            max_r, max_c = _get_used_range(ws)
            is_df = False
        else:  # calamine
            df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
            # Mark to include headers in pandas iteration
            setattr(df, "_include_headers", True)
            max_r, max_c = _get_used_range(df)
            is_df = True
        
        if not args.include_empty and (max_r == 0 or max_c == 0):
            return {"sheet_name": sheet_name, "status": "skipped", "reason": "empty"}
        
        safe = sanitize_filename(sheet_name, used_names)
        # If only one sheet is being exported, use the workbook name for CSV
        if single_csv_basename:
            csv_path = os.path.join(out_dir, f"{single_csv_basename}.csv")
        else:
            csv_path = os.path.join(out_dir, f"{safe}.csv")
        
        # Benchmark this sheet if requested
        if args.benchmark:
            benchmark_start = time.time()
        
        @timeout_handler(300)  # 5 min timeout
        def export_with_timeout():
            if args.engine == "openpyxl":
                return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
            else:  # calamine
                return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
        
        row_count, col_count = export_with_timeout()
        # Optional last-7 CSV for calamine path
        last7_path = None
        if is_df and args.report_last7:
            last7_path = _write_last7_by_reportdate_csv(df, csv_path, args.encoding, args.bom)
        
        # Record benchmark if requested
        if args.benchmark:
            benchmark_end = time.time()
            benchmark_results.append({
                "sheet_name": sheet_name,
                "engine": engine,
                "duration_seconds": round(benchmark_end - benchmark_start, 3),
                "rows": row_count,
                "cols": col_count,
                "rows_per_second": round(row_count / (benchmark_end - benchmark_start), 1) if (benchmark_end - benchmark_start) > 0 else 0
            })
        
        if engine == "openpyxl":
            wb.close()
        
        return {
            "sheet_name": sheet_name,
            "sanitized_name": safe,
            "file": csv_path,
            "file_sha256": get_file_hash(csv_path),
            "rows": row_count,
            "cols": col_count,
            "last7_file": last7_path,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error processing sheet {sheet_name}: {str(e)}")
        return {"sheet_name": sheet_name, "status": "error", "error": str(e)}

def _iter_rows(ws, visible_only: bool, date_fmt="%Y-%m-%d", dt_fmt="%Y-%m-%d %H:%M:%S", t_fmt="%H:%M:%S", af_columns="A,B,C,D,E,F", min_af_nonempty=4, af_gate_visible_only=False):
    max_r, max_c = get_used(ws)
    merged_top_left = {}
    if hasattr(ws, 'merged_cells') and ws.merged_cells:
        for rng in ws.merged_cells.ranges:
            tl_r, tl_c = rng.min_row, rng.min_col
            for rr in range(rng.min_row, rng.max_row + 1):
                for cc in range(rng.min_col, rng.max_col + 1):
                    merged_top_left[(rr, cc)] = (tl_r, tl_c)
    
    af_cols = _parse_af_columns(af_columns)
    
    for r in tqdm(range(1, max_r + 1), desc="Processing rows"):
        if visible_only and ws.row_dimensions[r].hidden:
            continue
            
        # --- A–F gate (VALUES) ---
        try:
            nonempty = 0
            af_values = []
            for c in af_cols:
                # if visible-only gate, ignore hidden columns
                if af_gate_visible_only and visible_only:
                    col_letter = get_column_letter(c)
                    if ws.column_dimensions[col_letter].hidden:
                        continue
                rr, cc = merged_top_left.get((r, c), (r, c))
                txt = _cell_value_as_text(ws, rr, cc, as_formulas=False,
                                          date_fmt=date_fmt,
                                          dt_fmt=dt_fmt,
                                          t_fmt=t_fmt)
                af_values.append(txt)
                if txt != "":
                    nonempty += 1
            if nonempty < min_af_nonempty:
                continue
        except Exception:
            # fail-safe: if something odd, don't skip the row
            pass
        # --- end A–F gate ---
        
        row_out = []
        for c in range(1, max_c + 1):
            if visible_only and ws.column_dimensions[get_column_letter(c)].hidden:
                continue
            rr, cc = merged_top_left.get((r, c), (r, c))
            val = _to_text(ws.cell(row=rr, column=cc).value, date_fmt, dt_fmt, t_fmt)
            row_out.append(val)
        if row_out and any(v != "" for v in row_out):
            yield row_out

def _stream_write_csv(path, rows_iterable, encoding: str, bom: bool):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    row_count = 0
    max_cols_seen = 0
    with open(path, "w", encoding=final_encoding, newline="") as f:
        writer = csv.writer(f)
        for row in rows_iterable:
            if row is None:
                row = []
            writer.writerow(row)
            row_count += 1
            if isinstance(row, (list, tuple)):
                if len(row) > max_cols_seen:
                    max_cols_seen = len(row)
    return row_count, max_cols_seen

def _get_cycle_dates_from_calendar(report_date_str=None):
    """
    Get cycle 7-day start and end dates from cycle calendar.
    
    Args:
        report_date_str: Report date in MM/DD/YYYY format (from REPORT_DATE env var)
                        If None, uses today's date
    
    Returns:
        tuple (start_date, end_date) as date objects, or (None, None) if not found
    """
    CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20250414.csv"
    
    try:
        if not os.path.exists(CYCLE_CSV):
            logger.warning(f"Cycle calendar not found: {CYCLE_CSV}, using fallback calculation")
            return None, None
        
        cycle_df = pd.read_csv(CYCLE_CSV)
        
        # Determine lookup date
        if report_date_str:
            try:
                # Parse MM/DD/YYYY format
                lookup_date = pd.to_datetime(report_date_str, format="%m/%d/%Y").date()
                lookup_date_str = report_date_str
            except:
                logger.warning(f"Invalid REPORT_DATE format: {report_date_str}, using today")
                lookup_date = datetime.now().date()
                lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        else:
            lookup_date = datetime.now().date()
            lookup_date_str = datetime.now().strftime("%m/%d/%Y")
        
        # Try exact match on Report_Due_Date first
        matching_row = cycle_df[cycle_df['Report_Due_Date'] == lookup_date_str]
        
        if not matching_row.empty:
            row = matching_row.iloc[0]
            start_date = pd.to_datetime(row['7_Day_Start']).date()
            end_date = pd.to_datetime(row['7_Day_End']).date()
            logger.info(f"Using cycle calendar: {row['Report_Name']} ({start_date} to {end_date})")
            return start_date, end_date
        
        # Fallback: find cycle where lookup_date falls within 7-day range
        for _, row in cycle_df.iterrows():
            try:
                start_date = pd.to_datetime(row['7_Day_Start']).date()
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if start_date <= lookup_date <= end_date:
                    logger.info(f"Using cycle calendar (range match): {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        # If no match found, try most recent cycle where end_date <= lookup_date
        for _, row in cycle_df.iterrows():
            try:
                end_date = pd.to_datetime(row['7_Day_End']).date()
                if end_date <= lookup_date:
                    start_date = pd.to_datetime(row['7_Day_Start']).date()
                    logger.info(f"Using most recent cycle: {row['Report_Name']} ({start_date} to {end_date})")
                    return start_date, end_date
            except:
                continue
        
        logger.warning(f"⚠️  No cycle found for date {lookup_date_str}, using fallback calculation")
        return None, None
        
    except Exception as e:
        logger.warning(f"⚠️  Error loading cycle calendar: {e}, using fallback calculation")
        return None, None

def _write_last7_by_reportdate_csv(df: pd.DataFrame, base_csv_path: str, encoding: str, bom: bool):
    """Write a filtered CSV with rows whose 'Report Date' falls within the cycle's 7-day range (from cycle calendar)."""
    if "Report Date" not in df.columns:
        return None
    
    # Get cycle dates from calendar (preferred) or fallback to simple calculation
    report_date_str = os.environ.get('REPORT_DATE', None)
    start_date, end_date = _get_cycle_dates_from_calendar(report_date_str)
    
    # Fallback to simple "last 7 days" if cycle calendar lookup failed
    if start_date is None or end_date is None:
        today = datetime.now().date()
        from datetime import timedelta
        start_date = today - timedelta(days=7)
        end_date = today
        logger.info(f"Using fallback: filtering last 7 days ({start_date} to {end_date})")
    
    dates = pd.to_datetime(df["Report Date"], errors="coerce")
    mask = (dates.dt.date >= start_date) & (dates.dt.date <= end_date)
    filtered = df[mask]
    
    # Use our custom formatting instead of pandas to_csv
    final_encoding = ("utf-8-sig" if bom and encoding.lower().replace("-", "") == "utf8" else encoding)
    out_path = os.path.splitext(base_csv_path)[0] + "_ReportDate_Last7.csv"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # Apply custom formatting and write using our streaming method
    def _iter_filtered_rows():
        # Emit headers first
        yield [str(col) for col in filtered.columns]
        # Emit formatted data rows
        for _, row in filtered.iterrows():
            row_out = []
            for val in row:
                formatted_val = _to_text(val, "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%H:%M:%S")
                row_out.append(formatted_val)
            yield row_out
    
    _stream_write_csv(out_path, _iter_filtered_rows(), encoding, bom)
    return out_path

def main():
    ap = argparse.ArgumentParser(description="Export all Excel sheets to individual CSV files.")
    ap.add_argument("--xlsx", required=False, help="Path to the source .xlsx (required unless --archive-only)")
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--out-subfolder", default=OUT_SUBFOLDER_DEFAULT)
    ap.add_argument("--encoding", default="utf-8")
    ap.add_argument("--no-bom", dest="bom", action="store_false")
    ap.add_argument("--visible-only", action="store_true", help="Export only visible rows and columns")
    ap.add_argument("--all-sheets", action="store_true", help="Export all sheets, ignoring include/exclude")
    ap.set_defaults(bom=True)
    ap.add_argument("--report-last7", action="store_true", help="Also write a *_ReportDate_Last7.csv filtered to last 7 days of Report Date (calamine engine only)")
    ap.add_argument("--include-empty", action="store_true")
    ap.add_argument("--na-rep", default="")
    ap.add_argument("--include", default=[], nargs="*", help="Include sheet patterns (substring match)")
    ap.add_argument("--exclude", default=[], nargs="*", help="Exclude sheet patterns (substring match)")
    ap.add_argument("--date-format", default="%Y-%m-%d", help="Date format string")
    ap.add_argument("--datetime-format", default="%Y-%m-%d %H:%M:%S", help="DateTime format string")
    ap.add_argument("--time-format", default="%H:%M:%S", help="Time format string")
    ap.add_argument("--af-columns", default="A,B,C",
                    help="Comma-separated list or Excel span (e.g., 'A-F') of columns to check for density gate.")
    ap.add_argument("--min-af-nonempty", type=int, default=2,
                    help="Minimum number of non-empty cells among --af-columns required to export a row.")
    ap.add_argument("--af-gate-visible-only", action="store_true",
                    help="If set, only visible cells among --af-columns count toward the threshold.")
    ap.add_argument("--disable-af-gate", action="store_true",
                    help="Disable A-F gate filtering (export all rows).")
    ap.add_argument("--engine", default="auto", choices=["auto", "calamine", "openpyxl"], 
                    help="Engine for reading Excel files (auto selects based on file size)")
    ap.add_argument("--chunksize", type=int, default=None, 
                    help="Read file in chunks of this size for large files (auto-enabled for 50MB+ files)")
    ap.add_argument("--benchmark", action="store_true", 
                    help="Enable performance benchmarking and include results in manifest")
    ap.add_argument("--parallel", action="store_true", 
                    help="Enable parallel sheet processing for better performance")
    ap.add_argument("--max-parallel-sheets", type=int, default=4, 
                    help="Maximum number of sheets to process in parallel (default: 4)")
    ap.add_argument("--archive-only", action="store_true",
                    help="Only archive old files and exit (no conversion)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Preview what would be archived without actually moving files")
    args = ap.parse_args()

    # Validate arguments
    if not args.archive_only and not args.xlsx:
        ap.error("--xlsx is required unless --archive-only is specified")

    # Handle archive-only mode
    if args.archive_only:
        working_dir = Path.cwd()
        exclude_file = None
        if args.xlsx:
            # If xlsx provided, use its parent directory and exclude this file
            xlsx_path = Path(args.xlsx).resolve()
            working_dir = xlsx_path.parent
            exclude_file = str(xlsx_path)
        count = archive_old_files(working_dir, dry_run=args.dry_run, exclude_file=exclude_file)
        if args.dry_run:
            print(f"\n[DRY-RUN] Would archive {count} file(s). Run without --dry-run to archive.")
        else:
            print(f"\nArchived {count} file(s).")
        return

    # Handle disable-af-gate option
    if args.disable_af_gate:
        args.min_af_nonempty = 0
        logger.info("A-F gate disabled - exporting all rows")

    xlsx_path = os.path.abspath(args.xlsx)
    
    # Auto-select engine and chunksize based on file size
    file_size = os.path.getsize(xlsx_path)
    available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
    
    if args.engine == "auto":
        # Use calamine for better performance on most files
        args.engine = "calamine"
    
    if args.chunksize is None:
        args.chunksize = get_adaptive_chunksize(file_size, available_memory)
        if file_size > 50 * 1024 * 1024:  # 50MB+
            logger.info(f"Large file detected ({file_size / (1024*1024):.1f}MB), enabling adaptive chunking with size {args.chunksize}")
    
    logger.info(f"Using engine: {args.engine}, chunksize: {args.chunksize}, available memory: {available_memory:.1f}MB")
    if not os.path.isfile(xlsx_path):
        logger.error(f"File not found: {xlsx_path}")
        raise FileNotFoundError(f"File not found: {xlsx_path}")

    out_parent = resolve_output_parent(args.base, args.out_subfolder)
    os.makedirs(out_parent, exist_ok=True)

    # Archive old files from the working directory (where xlsx files are)
    # EXCLUDE the current file being processed to prevent archiving it before conversion
    working_dir = Path(xlsx_path).parent
    if not args.dry_run:
        archive_old_files(working_dir, dry_run=False, exclude_file=xlsx_path)

    if args.out_subfolder != OUT_SUBFOLDER_DEFAULT:
        out_dir = out_parent
    else:
        wb_stem = os.path.splitext(os.path.basename(xlsx_path))[0]
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        out_dir = os.path.join(out_parent, f"{wb_stem}_{stamp}")
        os.makedirs(out_dir, exist_ok=True)

    # Initialize workbook based on engine
    wb = None
    if args.engine == "openpyxl":
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)
        sheet_names = wb.sheetnames
    else:  # calamine
        excel_file = pd.ExcelFile(xlsx_path, engine='calamine')
        sheet_names = excel_file.sheet_names
    
    used_names = set()
    exported = 0
    skipped = 0
    stats = {"rows_skipped_af_gate": 0}
    benchmark_results = []
    
    manifest = {
        "workbook": xlsx_path,
        "timestamp": datetime.now().isoformat(),
        "output_dir": out_dir,
        "workbook_sha256": get_file_hash(xlsx_path),
        "engine": args.engine,
        "chunksize": args.chunksize,
        "benchmark_enabled": bool(args.benchmark),
        "parallel_enabled": bool(args.parallel),
        "max_parallel_sheets": args.max_parallel_sheets,
        "file_size_mb": round(file_size / (1024 * 1024), 2),
        "available_memory_mb": round(available_memory, 2),
        "rows_skipped_af_gate": stats.get("rows_skipped_af_gate", 0),
        "af_gate": {
            "columns": args.af_columns,
            "min_nonempty": args.min_af_nonempty,
            "visible_only": bool(args.af_gate_visible_only),
            "disabled": bool(args.disable_af_gate)
        },
        "sheets": [],
        "benchmark_results": []
    }

    # Filter sheets based on include/exclude
    filtered_sheets = []
    for sheet_name in sheet_names:
        if not args.all_sheets:
            if args.exclude and any(pat.lower() in sheet_name.lower() for pat in args.exclude):
                continue
            if args.include and not any(pat.lower() in sheet_name.lower() for pat in args.include):
                continue
        filtered_sheets.append(sheet_name)
    
    if args.parallel and len(filtered_sheets) > 1:
        # Parallel processing
        logger.info(f"Processing {len(filtered_sheets)} sheets in parallel (max {args.max_parallel_sheets} workers)")
        with ThreadPoolExecutor(max_workers=args.max_parallel_sheets) as executor:
            # Submit all tasks
            future_to_sheet = {
                executor.submit(process_sheet_parallel, sheet_name, xlsx_path, out_dir, args, args.engine, used_names, benchmark_results, None if len(filtered_sheets) != 1 else os.path.splitext(os.path.basename(xlsx_path))[0]): sheet_name 
                for sheet_name in filtered_sheets
            }
            
            # Process completed tasks
            for future in tqdm(as_completed(future_to_sheet), total=len(filtered_sheets), desc="Processing sheets"):
                sheet_name = future_to_sheet[future]
                try:
                    result = future.result()
                    if result["status"] == "success":
                        exported += 1
                        manifest["sheets"].append(result)
                    elif result["status"] == "skipped":
                        skipped += 1
                    else:
                        logger.error(f"Error processing {sheet_name}: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    logger.error(f"Exception processing {sheet_name}: {str(e)}")
    else:
        # Sequential processing (original logic)
        for sheet_name in tqdm(filtered_sheets, desc="Exporting sheets"):
            # Benchmarking
            if args.benchmark:
                benchmark_results = {}
                for eng in ['calamine', 'openpyxl']:
                    duration = benchmark_engine_performance(xlsx_path, sheet_name, eng, is_detailed=True)
                    benchmark_results[eng] = duration
                    logger.info(f"Benchmark: {sheet_name} with {eng} - {json.dumps(duration)}")
                manifest["benchmark_results"].append({"sheet_name": sheet_name, "results": benchmark_results})
            
            # Load sheet data based on engine
            if args.engine == "openpyxl":
                ws = wb[sheet_name]
                max_r, max_c = _get_used_range(ws)
                is_df = False
            else:  # calamine
                df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine='calamine', keep_default_na=False)
                setattr(df, "_include_headers", True)
                max_r, max_c = _get_used_range(df)
                is_df = True
            
            if not args.include_empty and (max_r == 0 or max_c == 0):
                skipped += 1
                continue

            safe = sanitize_filename(sheet_name, used_names)
            # If only one sheet is being exported, use the workbook base name
            if len(filtered_sheets) == 1:
                csv_name = os.path.splitext(os.path.basename(xlsx_path))[0] + ".csv"
            else:
                csv_name = f"{safe}.csv"
            csv_path = os.path.join(out_dir, csv_name)
            try:
                @timeout_handler(300)  # 5 min timeout
                def export_with_timeout():
                    if args.engine == "openpyxl":
                        return _stream_write_csv(csv_path, _iter_rows(ws, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                    else:  # calamine
                        return _stream_write_csv(csv_path, _iter_rows_pandas(df, args.visible_only, args.date_format, args.datetime_format, args.time_format, args.af_columns, args.min_af_nonempty, args.af_gate_visible_only), args.encoding, args.bom)
                
                row_count, col_count = export_with_timeout()
                if row_count == 0:
                    skipped += 1
                    continue
                exported += 1
                # Optional last-7 CSV (works with both engines now)
                last7_path = None
                if args.report_last7:
                    # Load the CSV we just created to filter it
                    try:
                        df_for_filter = pd.read_csv(csv_path, encoding=args.encoding)
                        last7_path = _write_last7_by_reportdate_csv(df_for_filter, csv_path, args.encoding, args.bom)
                    except Exception as e:
                        logger.warning(f"Could not create 7-day filtered CSV: {e}")
                        last7_path = None
                manifest["sheets"].append({
                    "sheet_name": sheet_name,
                    "sanitized_name": safe,
                    "file": csv_path,
                    "file_sha256": get_file_hash(csv_path),
                    "rows": row_count,
                    "cols": col_count,
                    "last7_file": last7_path
                })
            except ExportTimeoutError:
                logger.error(f"Timeout during export of {safe}")
                raise ExportError(f"Timeout exporting {safe}")
            except Exception as e:
                logger.error(f"Error exporting {safe}: {str(e)}")
                raise ExportError(f"Error exporting {safe}: {str(e)}")

    # Add benchmark results to manifest
    if args.benchmark and manifest["benchmark_results"]:
        # Calculate summary from benchmark results
        total_duration = 0
        total_rows = 0
        for benchmark in manifest["benchmark_results"]:
            for engine, results in benchmark["results"].items():
                total_duration += results.get("total_duration", 0)
                # Estimate rows from throughput
                if results.get("throughput_rows_sec", 0) > 0:
                    total_rows += results.get("throughput_rows_sec", 0) * results.get("total_duration", 0)
        
        manifest["benchmark_summary"] = {
            "total_duration_seconds": round(total_duration, 3),
            "total_rows_processed": round(total_rows, 0),
            "average_rows_per_second": round(total_rows / total_duration, 1) if total_duration > 0 else 0,
            "sheets_benchmarked": len(manifest["benchmark_results"])
        }

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Source workbook : {xlsx_path}")
    print(f"Output folder   : {out_dir}")
    print(f"Sheets exported : {exported}")
    print(f"Sheets skipped  : {skipped} (empty or no columns)")
    print(f"Manifest        : {os.path.join(out_dir, 'manifest.json')}")

if __name__ == "__main__":
    main()
```


Fixing the command syntax:



## Summary

**Updates completed:**

1. Updated `export_excel_sheets_to_csv.py` to use the cycle calendar:
   - Added `_get_cycle_dates_from_calendar()` to look up cycle dates from the calendar CSV
   - Modified `_write_last7_by_reportdate_csv()` to use cycle calendar dates instead of "today - 7 days"
   - Updated to work with both openpyxl and calamine engines
   - Fixed Unicode encoding issues in logger messages

2. Verified the 7-day CSV was created correctly:
   - File: `2026_01_06_00_33_09_SCRPA_RMS_20260106_003600_ReportDate_Last7.csv`
   - Date range: 2025-12-30 to 2026-01-04 (matches cycle calendar: 12/30/2025 to 01/05/2026)
   - Total rows: 2 incidents in the cycle period

**Results:**
- Cycle calendar lookup: `26C01W01` (2025-12-30 to 2026-01-05)
- 7-day filtered CSV created with correct date range
- Script now uses cycle calendar for all future conversions

The script now correctly filters data using the cycle calendar's 7-day boundaries instead of a simple "last 7 days" calculation. The workflow should now work correctly for 2026 dates.

---

**User**

now I just have to run @c:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Run_SCRPA_Report_Folder.bat ?

---

**Cursor**


Yes. The batch file should work. Verifying that `REPORT_DATE` is passed to the conversion script:



Yes. Run the batch file. It should work because:

1. The main batch file sets `REPORT_DATE` as an environment variable (line 122, 199)
2. `convert_all_xlsx_auto.bat` inherits this environment variable when called
3. The updated `export_excel_sheets_to_csv.py` reads `REPORT_DATE` from the environment
4. The cycle calendar has 2026 entries

**What will happen:**
1. You'll be prompted for the report date (default: today = 01/06/2026)
2. Excel files will be converted to CSV using the cycle calendar for the 7-day filter
3. The weekly report folder will be created
4. Reports will be generated
5. Files will be organized into the report folder

**Note:** The conversion script will use the cycle calendar to filter the 7-day data correctly. For 01/06/2026, it will use:
- **Cycle**: 26C01W01
- **7-Day Range**: 12/30/2025 to 01/05/2026

Run the batch file and it should complete the workflow with the correct date ranges.

---

**User**

check the output C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06

---

**Cursor**


Checking the output folder to verify what was generated:



Verifying the key files to confirm everything is correct:



Checking cycle information in the files:



## Output verification

### Data files
- 7-day filtered CSV: `2026_01_06_00_33_09_SCRPA_RMS_20260106_003600_ReportDate_Last7.csv`
  - 2 records
  - Date range: 2025-12-30 to 2026-01-04 (matches cycle calendar)
- Briefing CSV: `SCRPA_Briefing_Ready_2026_01_06_00_50_57.csv`
  - Cycle: `26C01W01`
  - Date range: `12/30/2025` to `01/05/2026`
- Detailed/Summary CSVs: `SCRPA_7Day_Detailed.csv` and `SCRPA_7Day_Summary.csv`

### Reports
- Tactical report: `2026_01_06_00_50_58_rms_summary.html`
  - Cycle: `26C01W01`
  - Date range: `12/30/2025 - 01/05/2026`
- Strategic report: `SCRPA_Combined_Executive_Summary_20260106_005056.html`
  - Cycle: `26C01W01`
  - Date range: `12/30/2025 - 01/05/2026`
  - Generated: 2026-01-06 00:50:56

### Documentation
- `CHATGPT_BRIEFING_PROMPT.md` — present
- `SCRPA_Report_Summary.md` — present with correct data

## Summary

All files are correct:
- Cycle calendar lookup working (26C01W01)
- 7-day CSV created with correct date range
- Briefing CSV generated for 2026-01-06
- Strategic report generated for 2026-01-06
- All dates and cycles match the cycle calendar

The workflow is functioning correctly with the updated cycle calendar and the modified Excel conversion script.

---

**User**

**Goal**
- Update CHANGELOG.md, README.md, SUMMARY.md
- Sync version fields
- Commit and push to GitHub
- Optional tag and PR

**Auto-detect or infer**
- repo_root: current working directory or git root
- version: increment from last tag or VERSION file
- change_scope: summarize recent commits
- commit_to: default to new branch unless specified
- tag_release: default no
- open_pr: default yes if branch != main
- docs_subdir: optional, auto-detect if present
- dry_run: default no

**Rules**
- Work only inside repo_root
- No edits outside repo_root
- Short sentences. No em dashes
- Conventional Commits
- UTC dates in YYYY-MM-DD
- Respect .editorconfig and existing style

**Tasks**

1. Preflight: Verify git repo, print branch/remote, git status (stop if unrelated changes), print user.name/email, confirm auth. If dry_run, print planned steps and wait for approval.

2. Branch: If commit_to=main, checkout main and `git pull --ff-only`. Else create and switch to `docs/update-{YYYYMMDD-HHMM}` from main.

3. Version sync: Update version in VERSION, package.json, pyproject.toml, setup.cfg, or `**/__init__.py`. List changed files.

4. CHANGELOG.md: Create if missing. Keep "Unreleased" at top. Move "Unreleased" to v{version} with today's UTC date. Auto-build notes from Conventional Commits since last tag. Group by feat, fix, docs, refactor, perf, chore. Add compare link last_tag…v{version}. Add fresh "Unreleased" stub at top.

5. README.md: Update commands, paths, badges, version pins. Add "What changed in v{version}" with changelog link. Rebuild TOC if marker exists.

6. SUMMARY.md: Ensure concise project summary. List key directories and entry points. Add 3–6 bullets for changes in v{version}.

7. Formatting and lint: Enforce LF endings. Run markdownlint if present (apply safe fixes). Run prettier or mdformat if present.

8. Links: Check internal links and anchors across the three files. Fix or report broken links.

9. Git commit: Stage only edited docs and version files. Commit message: `docs: update CHANGELOG, README, SUMMARY for v{version} - {change_scope}`. Add footer lines: Refs (issue/PR links if any), Affects (list of files/dirs). Sign commit if GPG configured.

10. Tag and push: If tag_release=yes, create annotated tag v{version} with release notes from changelog (sign if possible). Push current branch. Push tags.

11. Pull request: If open_pr=yes and branch != main, create PR with title `docs: v{version} docs update - {change_scope}`. PR body includes changelog excerpt and checklist. Print PR URL.

12. CI: Print CI run URL if available. Poll once. Report status.

13. Report: Print branch, commit hash, tag, PR URL, CI status. Print JSON block: `{ "version": "...", "branch": "...", "commit": "...", "tag": "...", "pr_url": "...", "ci_status": "...", "files_changed": [...] }`

**Rollbacks**
- If staged only: `git restore --staged .` and restore backups
- If committed only: `git reset --soft HEAD~1`
- If pushed on branch: force push only after approval

Begin by auto-detecting parameters, then proceed with the workflow.

---

**Cursor**


Starting the documentation update workflow. Detecting repository state and parameters.



Checking recent commits and determining the next version:



Checking modified files and preparing the documentation update:



Updating the documentation. Latest version is 1.5.0; bumping to 1.6.0 for the new features. Creating a branch and updating the docs:



Updating CHANGELOG.md with the new version:


```markdown
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

**Last Updated**: 2025-12-29  
**Current Version**: 1.5.0  
**Maintained By**: R. A. Carucci


```

```markdown
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


```

```markdown
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

### v1.6.0 (Latest)
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

**Current Version**: 1.5.0  
**Last Updated**: December 29, 2025  
**Maintained By**: R. A. Carucci

---

## License

Internal use only - City of Hackensack Police Department


```

```markdown
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

### v1.6.0 (Latest)
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

**Current Version**: 1.6.0  
**Last Updated**: January 6, 2026  
**Maintained By**: R. A. Carucci

---

## License

Internal use only - City of Hackensack Police Department


```

```markdown
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

#### v1.6.0 (Latest)
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
**Last Updated**: December 29, 2025

---

**Version**: 1.5.0  
**Status**: Production  
**License**: Internal Use Only


```

```markdown
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

#### v1.6.0 (Latest)
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

**Version**: 1.6.0  
**Status**: Production  
**License**: Internal Use Only


```


Checking for linting errors and verifying links:



Committing the changes:



Generating the final report:



## Documentation update complete

**Summary:**
- Version: 1.6.0
- Branch: `docs/update-20260106-0050`
- Commit: `d8a9e09`
- Date: 2026-01-06

**Changes committed:**
- `CHANGELOG.md` - Added v1.6.0 section with cycle calendar 2026 support and 7-day CSV date range fix
- `README.md` - Updated version to 1.6.0 and added recent updates section
- `SUMMARY.md` - Updated version to 1.6.0 and added v1.6.0 improvements

**What changed in v1.6.0:**
- Cycle calendar extended with 2026 entries (all 52 weeks)
- 7-day CSV filtering now uses cycle calendar for accurate date ranges
- Excel conversion script enhanced with cycle calendar integration

**Status:**
- Documentation updated
- Changes committed to branch `docs/update-20260106-0050`
- No remote configured (cannot push to GitHub)
- No version files found in repo (no VERSION, package.json, etc.)

**Next steps:**
1. Configure remote if you want to push: `git remote add origin <url>`
2. Push branch: `git push -u origin docs/update-20260106-0050`
3. Create PR manually if needed

**JSON Report:**
```json
{
  "version": "1.6.0",
  "branch": "docs/update-20260106-0050",
  "commit": "d8a9e092a25752982b3ab39e4a1b594a1019db32",
  "tag": null,
  "pr_url": null,
  "ci_status": "N/A - No remote configured",
  "files_changed": ["CHANGELOG.md", "README.md", "SUMMARY.md"]
}
```

Documentation is updated and committed. Since no remote is configured, push and PR steps are skipped.

```json
{
  "version": "1.6.0",
  "branch": "docs/update-20260106-0050",
  "commit": "d8a9e092a25752982b3ab39e4a1b594a1019db32",
  "tag": null,
  "pr_url": null,
  "ci_status": "N/A - No remote configured",
  "files_changed": ["CHANGELOG.md", "README.md", "SUMMARY.md"]
}
```

---

**User**

I'm preparing to export this chat. Please generate a descriptive filename that summarizes the main topic or task of this conversation.

Requirements:
• 4-8 words
• Title Case (capitalize major words)
• Replace spaces with underscores
• Include .md extension
• No dates or special characters

Output only the filename, nothing else.

After export, I'll process it using: scripts\quick_process_chatlog.bat

---

**Cursor**


Cycle_Calendar_2026_Support_And_Date_Range_Fix.md

