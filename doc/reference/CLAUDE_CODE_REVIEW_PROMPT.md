# Claude Code Review Prompt: SCRPA Report Process Optimization

## Objective

Review the complete SCRPA (Strategic Crime Reduction and Problem Analysis) report generation workflow from RMS export to final folder organization. Identify improvements, address blind spots, and optimize file outputs to meet current requirements.

---

## Context: Current Workflow

### Workflow Entry Point
**Batch Script**: `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Run_SCRPA_Report_Folder.bat`

This script orchestrates the following steps:
1. **STEP 0.5**: Excel to CSV conversion (from `05_EXPORTS\_RMS\scrpa\*.xlsx`)
2. **STEP 1**: Create report folder structure (`generate_weekly_report.py`)
3. **STEP 2**: Generate HTML/PDF reports (`generate_all_reports.bat`)
4. **STEP 3**: Organize files into report folder (`organize_report_files.py`)
5. **STEP 4**: Open year folder

### Current Output Location
**Report Folder**: `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\YYYY\YYCMMWww_YY_MM_DD\`

**Example**: `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06\`

### Current Data Processing
**M Code File**: `Time_Based\2026\26C01W01_26_01_06\Data\m_code_all_queries.m`

This Power BI M code performs extensive data transformations including:
- Time processing (BestTimeValue, TimeSource, TimeOfDay, StartOfHour)
- Lag day calculations (IsLagDay, LagDays)
- Cycle assignment (cycle_name, cycle_name_adjusted, IsCurrent7DayCycle)
- Incident consolidation (ALL_INCIDENTS)
- Crime categorization (Crime_Category)
- Address cleaning (Clean_Address)
- Vehicle information consolidation
- Incident key generation for joins

**Reference Documentation**: `Time_Based\2026\26C01W01_26_01_06\Data\README_7day_outputs.md`

---

## Requirements Analysis

### 1. Required CSV Output Files

#### A. 7-Day Detailed CSV (Filtered to Last 7 Days Only)
**Location**: `{ReportFolder}\Data\SCRPA_7Day_Detailed.csv`

**Requirements**:
- ✅ **Filter**: Only incidents from the last 7 days (based on Report Date)
- ✅ **Must Include**:
  - All original RMS columns (Case Number, Incident Date, Incident Time, Report Date, Incident Type_1/2/3, FullAddress, Grid, Zone, Narrative, etc.)
  - All M code enhanced columns:
    - `IsLagDay` (boolean)
    - `LagDays` (integer)
    - `BestTimeValue` (time)
    - `TimeSource` (text: "Incident Time", "Incident Time_Between", "Report Time", "None")
    - `Incident_Time` (formatted time string)
    - `Incident_Date` (date)
    - `Incident_Date_Date` (date type)
    - `Report_Date` (date)
    - `Report_Date_Text` (text)
    - `IncidentToReportDays` (integer)
    - `Period` (text: "7-Day", "28-Day", etc.)
    - `Period_SortKey` (integer)
    - `cycle_name` (text)
    - `Backfill_7Day` (boolean)
    - `cycle_name_adjusted` (text)
    - `IsCurrent7DayCycle` (boolean)
    - `StartOfHour` (time string)
    - `TimeOfDay` (text: "Late Night (00:00–03:59)", "Early Morning (04:00–07:59)", etc.)
    - `TimeOfDay_SortKey` (integer)
    - `ALL_INCIDENTS` (text: concatenated Incident Type_1, Type_2, Type_3)
    - `Crime_Category` (text: "Burglary Auto", "Burglary - Comm & Res", "Robbery", "Motor Vehicle Theft", "Sexual Offenses", "Other")
    - `Incident_Type_1_Norm`, `Incident_Type_2_Norm`, `Incident_Type_3_Norm` (cleaned, statute suffix removed)
    - `Vehicle_1`, `Vehicle_2`, `Vehicle_1_and_Vehicle_2` (consolidated vehicle info)
    - `Clean_Address` (address with "Hackensack, NJ" suffix removed)
    - `IncidentKey` (text: for joins)
    - `Category_Type` (text: from CallTypeCategories join)
    - `Response_Type` (text: from CallTypeCategories join)
    - `Time_Validation` (text: validation details)
    - `CycleStartDate`, `CycleEndDate` (dates)
- ✅ **Must Include Narrative Column**: Full narrative text for each incident
- ✅ **Purpose**: Detailed incident-level data for 7-day period with all analytical enhancements

#### B. Full Export Enhanced CSV (All Incidents, No Date Filter)
**Location**: `{ReportFolder}\Data\SCRPA_Full_Export_Enhanced.csv`

**Requirements**:
- ✅ **Filter**: ALL incidents (no date filtering)
- ✅ **Must Include**: Same columns as 7-Day Detailed CSV above
- ✅ **Purpose**: Complete historical dataset with all M code enhancements for analysis

#### C. 7-Day Summary CSV (Keep As-Is)
**Location**: `{ReportFolder}\Data\SCRPA_7Day_Summary.csv`

**Requirements**:
- ✅ **Keep existing format** (no changes needed)
- ✅ **Purpose**: High-level counts and aggregations

### 2. Files to Remove from Data Folder

**Remove ALL Excel files** from `{ReportFolder}\Data\`:
- ❌ `*.xlsx` files (not needed in Data folder)
- ✅ **Keep**: All CSV files
- ✅ **Keep**: `m_code_all_queries.m` (M code reference)
- ✅ **Keep**: `README_7day_outputs.md` (documentation)

**Note**: Original Excel exports remain in `05_EXPORTS\_RMS\scrpa\` (source location)

### 3. ChatGPT Prompt Enhancement

**Current Prompt Location**: `{ReportFolder}\Documentation\CHATGPT_BRIEFING_PROMPT.md`

**Current Format**: See `Time_Based\2026\26C01W01_26_01_06\Documentation\CHATGPT_BRIEFING_PROMPT.md` for reference

**Required Changes**:

1. **Data Source Update**:
   - Change from `SCRPA_Briefing_Ready_*.csv` to `SCRPA_7Day_Detailed.csv`
   - Reference the enhanced columns (IsLagDay, LagDays, TimeOfDay, Crime_Category, etc.)
   - Include full Narrative column in the embedded CSV data section

2. **HTML Output Requirements**:
   - Generate **TWO HTML files** from the same prompt:
     - **Portrait**: Standard 8.5" x 11" page (current format)
     - **Landscape**: 11" x 8.5" page (rotated layout)
   - Both should use the same data and content
   - Both should be print-ready (CSS @media print rules)
   - File naming:
     - Portrait: `SCRPA_Briefing_Portrait_YYYY_MM_DD.html`
     - Landscape: `SCRPA_Briefing_Landscape_YYYY_MM_DD.html`

3. **Prompt Instructions Update**:
   - Add explicit instruction: "Generate TWO HTML outputs: one portrait (8.5" x 11") and one landscape (11" x 8.5")"
   - Update CSS to support both orientations
   - Ensure landscape version uses appropriate page breaks and layout

---

## Tasks for Claude Code

### Task 1: Review Current Workflow
1. **Examine** the batch script (`Run_SCRPA_Report_Folder.bat`)
2. **Examine** the organize script (`organize_report_files.py`)
3. **Examine** the M code export functions (`m_code_all_queries.m`)
4. **Trace** the data flow from RMS export → CSV conversion → M code processing → file organization
5. **Identify** where Excel files are being copied to Data folder
6. **Identify** where CSV exports are generated from M code

### Task 2: Identify Required Changes

#### A. CSV Export Generation
- **Current State**: Determine how `SCRPA_7Day_Detailed.csv` and `SCRPA_7Day_Summary.csv` are currently generated
- **Required**: Add `SCRPA_Full_Export_Enhanced.csv` export (all incidents, same columns)
- **Question**: Are these exports generated from Power BI M code, or from a separate Python script?
- **Action**: Identify the export mechanism and recommend how to add the full export

#### B. File Organization Script
- **Current State**: Review `organize_report_files.py` to see what files it copies
- **Required**: 
  - Remove Excel files (`.xlsx`) from Data folder copy operation
  - Ensure all three CSV files are copied (7Day_Detailed, 7Day_Summary, Full_Export_Enhanced)
- **Action**: Identify code changes needed

#### C. ChatGPT Prompt Generation
- **Current State**: Review how `CHATGPT_BRIEFING_PROMPT.md` is generated
- **Required**:
  - Update to reference `SCRPA_7Day_Detailed.csv` instead of `SCRPA_Briefing_Ready_*.csv`
  - Include all enhanced columns in the embedded CSV data
  - Add instructions for generating both portrait and landscape HTML
  - Update HTML template CSS to support both orientations
- **Action**: Identify script that generates the prompt and recommend changes

### Task 3: Address Blind Spots

Review and address these potential issues:

1. **Data Completeness**:
   - Are all M code columns being exported to CSV? (Verify column list matches requirements)
   - Is the Narrative column preserved correctly in exports? (Check for truncation, encoding issues)
   - Are date/time fields formatted correctly for CSV export?

2. **File Naming Consistency**:
   - Are file names consistent across the workflow?
   - Do timestamps in filenames match the report date?
   - Are there naming conflicts?

3. **Data Filtering Logic**:
   - How is the "7-day" filter applied? (Report Date? Incident Date?)
   - Is the filter logic consistent between M code and any Python scripts?
   - Are lag day incidents correctly included in 7-day filtered data?

4. **Export Performance**:
   - How large are the CSV files? (Full export could be very large)
   - Are exports optimized for file size?
   - Is there a risk of memory issues with full export?

5. **Error Handling**:
   - What happens if M code export fails?
   - What happens if a required CSV file is missing?
   - Are there validation checks for data completeness?

6. **Dependencies**:
   - What external dependencies are required? (Power BI Desktop? Python packages?)
   - Are all paths correctly configured?
   - Are there any hardcoded paths that should be parameterized?

7. **Version Control**:
   - How are M code changes tracked?
   - Are there version numbers in the outputs?
   - Is there a way to roll back if something breaks?

### Task 4: Provide Recommendations

For each identified issue or improvement opportunity, provide:

1. **Current State**: What exists now
2. **Issue/Enhancement**: What needs to change
3. **Recommended Solution**: Specific code changes or process improvements
4. **Implementation Priority**: High/Medium/Low
5. **Risk Assessment**: Potential impact of changes

### Task 5: Review ChatGPT Prompt Format

**Current Prompt Structure** (from `Time_Based\2026\26C01W01_26_01_06\Documentation\CHATGPT_BRIEFING_PROMPT.md`):

1. Header with metadata (Cycle, Date Range, Version)
2. CSV Data Summary (case counts, types)
3. Reporting Parameters
4. Complete CSV Data (embedded)
5. Raw 7-Day Filtered CSV Data (source reference)
6. Instructions for ChatGPT
7. Strategic Crime Reduction Briefing Prompt
8. Global Instructions
9. Category Templates
10. HTML Template (currently portrait only)

**Required Enhancements**:
- Update CSV references to use `SCRPA_7Day_Detailed.csv`
- Include all enhanced columns in embedded CSV
- Add landscape HTML template variant
- Update instructions to generate both orientations
- Ensure CSS supports both page sizes

**Questions for Claude**:
1. Should the prompt include both HTML templates (portrait and landscape) in the same file?
2. Should the prompt instruct ChatGPT to generate two separate HTML files, or one file with both?
3. Are there any improvements to the current prompt structure that would make it more effective?
4. Should the embedded CSV include all columns, or can some be omitted for brevity?

---

## Files to Review

### Primary Scripts
1. `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Run_SCRPA_Report_Folder.bat`
2. `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\organize_report_files.py`
3. `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06\Data\m_code_all_queries.m`

### Reference Files
4. `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06\Data\README_7day_outputs.md`
5. `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06\Data\SCRPA_7Day_Detailed.csv` (current example)
6. `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W01_26_01_06\Documentation\CHATGPT_BRIEFING_PROMPT.md` (current example)

### Additional Scripts to Locate
- Script that generates `SCRPA_7Day_Detailed.csv` and `SCRPA_7Day_Summary.csv`
- Script that generates `CHATGPT_BRIEFING_PROMPT.md`
- Any Power BI export scripts or queries

---

## Expected Deliverables

1. **Workflow Analysis Document**: 
   - Current process flow diagram
   - File locations and dependencies
   - Data transformation steps

2. **Change Recommendations**:
   - Specific code changes needed
   - File modifications required
   - Process improvements

3. **Implementation Plan**:
   - Step-by-step changes
   - Testing recommendations
   - Rollback procedures

4. **Enhanced ChatGPT Prompt**:
   - Updated prompt with new CSV references
   - Dual-orientation HTML templates
   - Improved instructions

5. **Blind Spot Analysis**:
   - Identified risks and issues
   - Mitigation strategies
   - Monitoring recommendations

---

## Success Criteria

✅ **CSV Files**:
- `SCRPA_7Day_Detailed.csv` exists with all required columns (including Narrative, IsLagDay, LagDays, TimeOfDay, Crime_Category, etc.)
- `SCRPA_Full_Export_Enhanced.csv` exists with all incidents and all required columns
- `SCRPA_7Day_Summary.csv` remains unchanged

✅ **File Organization**:
- No Excel files (`.xlsx`) in Data folder
- All required CSV files present
- M code and README files present

✅ **ChatGPT Prompt**:
- References `SCRPA_7Day_Detailed.csv`
- Includes all enhanced columns in embedded data
- Generates both portrait and landscape HTML outputs
- Both HTML files are print-ready (8.5" x 11" and 11" x 8.5")

✅ **Process**:
- Workflow runs without errors
- All files generated correctly
- No data loss or truncation
- Performance acceptable

---

## Notes

- **Standard Page Size**: 8.5" x 11" (portrait) and 11" x 8.5" (landscape)
- **HTML Only**: No PDF generation needed (user will convert HTML to PDF if needed)
- **File Naming**: Use consistent naming with timestamps where appropriate
- **Backward Compatibility**: Ensure changes don't break existing reports or processes

---

## Questions for Claude

1. **Export Mechanism**: How are the CSV files currently exported from Power BI? Is it manual, automated, or scripted?

2. **M Code Columns**: Are all the enhanced columns listed in the requirements actually available in the M code output, or do some need to be added?

3. **File Size Concerns**: The full export could be very large. Should we implement any filtering, compression, or chunking strategies?

4. **Prompt Structure**: Would it be better to have two separate prompt files (one for portrait, one for landscape) or one prompt that generates both?

5. **Data Validation**: Should we add validation checks to ensure all required columns are present before generating the ChatGPT prompt?

6. **Error Recovery**: What happens if the M code fails or produces incomplete data? How should the workflow handle this?

7. **Performance Optimization**: Are there any optimizations we can make to the M code or export process to improve performance?

8. **Documentation**: Should we update the README or other documentation files to reflect these changes?

---

**Please review the entire workflow, identify all required changes, address blind spots, and provide a comprehensive implementation plan with specific code recommendations.**

