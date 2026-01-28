// 2026_01_28
// Project: m_code/All_Crimes_Simple.m
// Author: R. A. Carucci
// Purpose: Simplified Power Query that imports Python-generated SCRPA_All_Crimes_Enhanced.csv.
//          All transformations are done in Python - this query only loads and types the data.
//
// MIGRATION NOTES:
// - This replaces the complex 742-line All_Crimes.m
// - All data enrichment (cycle detection, lag days, period, crime category, etc.) is done in Python
// - Python script: scripts/scrpa_transform.py
// - This query just imports the pre-processed CSV and applies correct column types
//
// USAGE:
// 1. Run Python pipeline: python scripts/run_scrpa_pipeline.py rms_export.csv --report-date MM/DD/YYYY
// 2. Copy SCRPA_All_Crimes_Enhanced.csv to the expected location
// 3. Refresh this Power BI query
//
// DATA SOURCE:
// The CSV path should point to the latest SCRPA_All_Crimes_Enhanced.csv in the current cycle folder.
// Update the FilePath parameter or use a folder-based dynamic path.

let
    // ===========================================
    // CONFIGURATION
    // ===========================================
    // Option 1: Direct file path (update for each cycle)
    // FilePath = "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W04_26_01_27\Data\SCRPA_All_Crimes_Enhanced.csv",

    // Option 2: Use a parameter (recommended for production)
    // FilePath = SCRPA_DataPath,

    // Option 3: Dynamic path based on latest folder (advanced)
    // This example uses a fixed path for simplicity
    // UPDATE THIS PATH when running pipeline with different report dates
    FilePath = "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W04_26_01_28\Data\SCRPA_All_Crimes_Enhanced.csv",

    // ===========================================
    // LOAD CSV
    // ===========================================
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 65,  // Adjust based on actual column count
            Encoding = 65001,  // UTF-8
            QuoteStyle = QuoteStyle.Csv
        ]
    ),

    // Promote first row to headers
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

    // ===========================================
    // TYPE CONVERSIONS
    // ===========================================
    // Apply correct types to columns - no transformations, just typing
    TypedTable = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            // Original RMS columns
            {"Case Number", type text},
            {"Incident Date", type text},  // Keep as text, Python has formatted it
            {"Incident Time", type text},
            {"Incident Date_Between", type text},
            {"Incident Time_Between", type text},
            {"Report Date", type text},
            {"Report Time", type text},
            {"Incident Type_1", type text},
            {"Incident Type_2", type text},
            {"Incident Type_3", type text},
            {"FullAddress", type text},
            {"Grid", type text},
            {"Zone", type text},
            {"Narrative", type text},
            {"Total Value Stolen", type number},
            {"Total Value Recover", type number},
            {"Registration 1", type text},
            {"Make1", type text},
            {"Model1", type text},
            {"Reg State 1", type text},
            {"Registration 2", type text},
            {"Reg State 2", type text},
            {"Make2", type text},
            {"Model2", type text},
            {"Reviewed By", type text},
            {"CompleteCalc", type text},
            {"Officer of Record", type text},
            {"Squad", type text},
            {"Det_Assigned", type text},
            {"Case_Status", type text},
            {"NIBRS Classification", type text},

            // Computed columns from Python
            {"BestTimeValue", type time},
            {"TimeSource", type text},
            {"Incident_Time", type text},  // HH:MM:SS formatted
            {"Incident_Date", type text},  // MM/DD/YY formatted
            {"Incident_Date_Date", type date},
            {"Report_Date", type date},
            {"Report_Date_ForLagday", type date},
            {"Report_Date_Text", type text},
            {"IncidentToReportDays", Int64.Type},
            {"Period", type text},
            {"_Period_Debug", type text},
            {"Period_SortKey", Int64.Type},
            {"cycle_name", type text},
            {"Backfill_7Day", type logical},
            {"cycle_name_adjusted", type text},
            {"IsCurrent7DayCycle", type logical},
            {"IsLagDay", type logical},
            {"LagDays", Int64.Type},
            {"StartOfHour", type text},
            {"TimeOfDay", type text},
            {"TimeOfDay_SortKey", Int64.Type},
            {"ALL_INCIDENTS", type text},
            {"Crime_Category", type text},
            {"Incident_Type_1_Norm", type text},
            {"Incident_Type_2_Norm", type text},
            {"Incident_Type_3_Norm", type text},
            {"Vehicle_1", type text},
            {"Vehicle_2", type text},
            {"Vehicle_1_and_Vehicle_2", type text},
            {"Clean_Address", type text},
            {"IncidentKey", type text},
            {"Category_Type", type text},
            {"Response_Type", type text},
            {"Time_Validation", type text}
        }
    ),

    // ===========================================
    // RESULT
    // ===========================================
    Result = TypedTable

in
    Result


// ===========================================
// NOTES FOR POWER BI DEVELOPERS
// ===========================================
//
// This query replaces the original All_Crimes.m which contained 742 lines of
// complex M code for data transformation. The new Python-first architecture:
//
// 1. ALL data transformations now happen in Python (scripts/scrpa_transform.py)
// 2. This M code query simply loads the pre-processed CSV
// 3. No calculation logic is duplicated - Python is the single source of truth
//
// Key computed columns now available directly from Python:
// - Period: 7-Day, 28-Day, YTD, Prior Year, Historical (based on Incident_Date)
// - LagDays: CycleStart_7Day - Incident_Date (NOT Report_Date - Incident_Date)
// - IsLagDay: True if incident occurred before the report cycle
// - Backfill_7Day: True if incident before cycle, reported during current 7-day
// - Crime_Category: Motor Vehicle Theft, Burglary Auto, Robbery, etc.
// - TimeOfDay: Late Night, Early Morning, Morning, Afternoon, Evening Peak, Night
//
// To update the data source:
// 1. Run: python scripts/run_scrpa_pipeline.py input.csv --report-date MM/DD/YYYY
// 2. Update FilePath in this query to point to the new SCRPA_All_Crimes_Enhanced.csv
// 3. Refresh the Power BI model
//
// For questions or issues, see:
// - Documentation: Time_Based/YYYY/CYCLE/Documentation/claude.md
// - Data Dictionary: Time_Based/YYYY/CYCLE/Documentation/data_dictionary.yaml
