// 2026_02_10
// Project: m_code/All_Crimes_Simple.m
// Author: R. A. Carucci
// Purpose: Simplified Power Query that imports Python-generated SCRPA_All_Crimes_Enhanced.csv.
//          AUTOMATIC PATH DETECTION - No manual editing needed each cycle!
//
// HOW IT WORKS:
// This M code automatically finds the CSV file in the most recent cycle folder.
// When you run the pipeline and open Power BI, it automatically uses the latest cycle's data.
//
// USAGE:
// 1. Run Python pipeline: python scripts/run_scrpa_pipeline.py rms_export.csv --report-date MM/DD/YYYY
// 2. Pipeline creates cycle folder with data (e.g., 26C02W06_26_02_10/)
// 3. Open ANY PBIX file and click Refresh - it automatically finds the latest cycle CSV!
//
// NO MANUAL PATH EDITING REQUIRED!

let
    // ===========================================
    // AUTOMATIC PATH DETECTION
    // ===========================================
    // Base directory for all SCRPA reports
    BaseDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based",
    
    // Get the current year (e.g., 2026)
    CurrentYear = Number.ToText(Date.Year(DateTime.LocalNow())),
    
    // Build path to current year's folder
    YearFolder = BaseDir & "\" & CurrentYear,
    
    // Get all items (files and folders) in the year directory
    AllItems = Folder.Contents(YearFolder),
    
    // Filter to only folders (not files) by checking if Folder Path is not null
    AllFolders = Table.SelectRows(AllItems, each [Folder Path] <> null),
    
    // Filter to only cycle folders (start with year suffix, e.g., "26C" or "26BW")
    CycleFolders = Table.SelectRows(AllFolders, each Text.StartsWith([Name], Text.End(CurrentYear, 2))),
    
    // Sort by date modified (most recent first)
    SortedFolders = Table.Sort(CycleFolders, {{"Date modified", Order.Descending}}),
    
    // Get the most recent cycle folder's full path
    LatestCycleFolder = SortedFolders{0}[Folder Path] & SortedFolders{0}[Name],
    
    // Build full path to CSV
    FilePath = LatestCycleFolder & "\Data\SCRPA_All_Crimes_Enhanced.csv",

    // ===========================================
    // LOAD CSV
    // ===========================================
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 66,  // Must match Python output (includes Report_Date_ForLagday)
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
// AUTOMATIC PATH DETECTION:
// This query automatically finds the most recent cycle folder in the current year
// and loads the SCRPA_All_Crimes_Enhanced.csv from its Data subfolder.
//
// HOW IT WORKS:
// 1. Looks in: C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\[CURRENT_YEAR]
// 2. Gets all folders (using Folder.Contents, not Folder.Files!)
// 3. Filters to cycle folders starting with year (e.g., "26C" or "26BW")
// 4. Sorts by last modified date (most recent first)
// 5. Loads CSV from: [Most Recent Folder]\Data\SCRPA_All_Crimes_Enhanced.csv
//
// BENEFITS:
// ✅ No manual path editing needed each cycle
// ✅ Always uses the most recent data automatically
// ✅ Template can be copied and refreshed without modification
//
// WORKFLOW:
// 1. Run pipeline: python scripts/run_scrpa_pipeline.py input.csv --report-date MM/DD/YYYY
// 2. Pipeline creates new cycle folder with data
// 3. Open ANY Power BI file and click Refresh - automatically uses latest cycle data!
//
// Key computed columns now available directly from Python:
// - Period: 7-Day, 28-Day, YTD, Prior Year, Historical (based on Incident_Date)
// - LagDays: CycleStart_7Day - Incident_Date (NOT Report_Date - Incident_Date)
// - IsLagDay: True if incident occurred before the report cycle
// - Backfill_7Day: True if incident before cycle, reported during current 7-day
// - Crime_Category: Motor Vehicle Theft, Burglary Auto, Robbery, etc.
// - TimeOfDay: Late Night, Early Morning, Morning, Afternoon, Evening Peak, Night
// - Clean_Address: Street address only (for map labels)
//
// For questions or issues, see:
// - Documentation: Time_Based/YYYY/CYCLE/Documentation/
// - Data Dictionary: Documentation/data_dictionary.yaml
