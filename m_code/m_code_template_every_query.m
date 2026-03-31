// All_Crimes
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

// Export_Formatting
// =============================================================================
// EXPORT FORMATTING WITH CYCLE-BASED FILENAME GENERATION
// =============================================================================

let
    // CYCLE-BASED FILENAME GENERATION FUNCTION
    GenerateCycleFilename = (cycleName as text, dataType as text, optional customSuffix as text) as text =>
        let
            currentDate = Date.ToText(Date.From(DateTime.LocalNow()), "yyyy_MM_dd"),
            suffix = if customSuffix <> null then customSuffix else "7Day_Data_Standardized",
            filename = cycleName & "_" & currentDate & "_" & suffix & ".csv"
        in
            filename,
    
    // STANDARDIZED COLUMN ORDERING FUNCTION
    StandardizeColumnOrder = (inputTable as table, dataSourceType as text) as table =>
        let
            // Define standard column orders for different data types
            CADColumnOrder = {
                "case_number",
                "cycle_name",
                "incident_date",
                "incident_time",
                "response_type",
                "how_reported",
                "location",
                "block",
                "grid",
                "post",
                "time_dispatched",
                "time_out",
                "time_in",
                "time_spent_minutes",
                "time_response_minutes",
                "officer",
                "disposition",
                "cad_notes_cleaned"
            },
            
            RMSColumnOrder = {
                "case_number",
                "cycle_name",
                "incident_date",
                "incident_time",
                "time_of_day",
                "period",
                "location",
                "block",
                "grid",
                "post",
                "all_incidents",
                "incident_type",
                "narrative",
                "total_value_stolen",
                "total_value_recovered",
                "squad",
                "officer_of_record",
                "nibrs_classification"
            },
            
            // Select appropriate column order
            targetOrder = if dataSourceType = "CAD" then CADColumnOrder else RMSColumnOrder,
            
            // Get available columns from input table
            availableColumns = Table.ColumnNames(inputTable),
            
            // Filter target order to only include available columns
            orderedColumns = List.Select(targetOrder, (col) => List.Contains(availableColumns, col)),
            
            // Add any additional columns not in the standard order
            additionalColumns = List.Select(availableColumns, (col) => not List.Contains(targetOrder, col)),
            
            finalColumnOrder = List.Combine({orderedColumns, additionalColumns}),
            
            // Reorder the table
            reorderedTable = Table.SelectColumns(inputTable, finalColumnOrder)
        in
            reorderedTable,
    
    // EXPORT PATH MANAGEMENT FUNCTION
    GenerateExportPath = (basePath as text, cycleName as text, dataType as text) as record =>
        let
            // Clean and validate base path
            cleanBasePath = Text.Replace(Text.Replace(basePath, "/", "\"), "\\", "\"),
            
            // Ensure base path ends with backslash
            normalizedBasePath = if Text.EndsWith(cleanBasePath, "\") then cleanBasePath else cleanBasePath & "\",
            
            // Create cycle-specific subdirectory
            cycleDirectory = normalizedBasePath & cycleName & "\",
            
            // Generate filename
            filename = GenerateCycleFilename(cycleName, dataType),
            
            // Full export path
            fullPath = cycleDirectory & filename,
            
            pathInfo = [
                BasePath = normalizedBasePath,
                CycleDirectory = cycleDirectory,
                Filename = filename,
                FullPath = fullPath,
                DataType = dataType,
                CycleName = cycleName,
                GeneratedDateTime = DateTime.ToText(DateTime.LocalNow())
            ]
        in
            pathInfo,
    
    // COMPREHENSIVE EXPORT PREPARATION FUNCTION  
    PrepareForExport = (inputTable as table, dataSourceType as text, exportBasePath as text) as record =>
        let
            // Ensure cycle_name column exists
            tableWithCycle = if List.Contains(Table.ColumnNames(inputTable), "cycle_name") then
                inputTable
            else
                Table.AddColumn(inputTable, "cycle_name", each "C25W31", type text),
            
            // Get cycle name from first row
            cycleName = if Table.RowCount(tableWithCycle) > 0 then
                Table.FirstN(tableWithCycle, 1){0}[cycle_name]
            else
                "C25W31",
            
            // Standardize column order with cycle_name as 2nd column
            orderedTable = StandardizeColumnOrder(tableWithCycle, dataSourceType),
            
            // Generate export path information
            exportInfo = GenerateExportPath(exportBasePath, cycleName, dataSourceType),
            
            // Add export metadata to each row
            tableWithExportInfo = Table.AddColumn(orderedTable, "export_metadata", each
                [
                    ExportPath = exportInfo[FullPath],
                    ExportDateTime = DateTime.ToText(DateTime.LocalNow()),
                    RecordCount = Table.RowCount(orderedTable),
                    DataSourceType = dataSourceType
                ], type record),
            
            exportPreparation = [
                PreparedTable = orderedTable,
                ExportInformation = exportInfo,
                TableWithMetadata = tableWithExportInfo,
                RecordCount = Table.RowCount(orderedTable),
                ColumnCount = List.Count(Table.ColumnNames(orderedTable)),
                DataSourceType = dataSourceType,
                CycleName = cycleName,
                ReadyForExport = Table.RowCount(orderedTable) > 0
            ]
        in
            exportPreparation,
    
    // BATCH EXPORT PREPARATION FOR MULTIPLE TABLES
    PrepareBatchExport = (tableList as list, exportBasePath as text) as record =>
        let
            // Process each table in the list
            processedTables = List.Transform(tableList, (tableInfo) =>
                let
                    tableName = tableInfo[TableName],
                    tableData = tableInfo[TableData],
                    dataType = tableInfo[DataType],
                    
                    prepared = PrepareForExport(tableData, dataType, exportBasePath)
                in
                    [
                        TableName = tableName,
                        DataType = dataType,
                        OriginalTable = tableData,
                        PreparedExport = prepared
                    ]
            ),
            
            // Generate batch summary
            totalRecords = List.Sum(List.Transform(processedTables, (t) => t[PreparedExport][RecordCount])),
            successfulPreparations = List.Count(List.Select(processedTables, (t) => t[PreparedExport][ReadyForExport])),
            
            batchInfo = [
                BatchProcessedDateTime = DateTime.ToText(DateTime.LocalNow()),
                TotalTables = List.Count(processedTables),
                SuccessfulPreparations = successfulPreparations,
                FailedPreparations = List.Count(processedTables) - successfulPreparations,
                TotalRecordsForExport = totalRecords,
                ProcessedTables = processedTables,
                BatchReadyForExport = successfulPreparations = List.Count(processedTables)
            ]
        in
            batchInfo,
    
    // EXPORT VALIDATION FUNCTION
    ValidateExportReadiness = (preparedExport as record) as record =>
        let
            table = preparedExport[PreparedTable],
            exportInfo = preparedExport[ExportInformation],
            
            validationChecks = [
                HasData = Table.RowCount(table) > 0,
                HasCycleColumn = List.Contains(Table.ColumnNames(table), "cycle_name"),
                HasValidCycleName = if Table.RowCount(table) > 0 then 
                    Table.FirstN(table, 1){0}[cycle_name] <> null and Table.FirstN(table, 1){0}[cycle_name] <> ""
                else false,
                HasValidPath = exportInfo[FullPath] <> null and exportInfo[FullPath] <> "",
                CycleNameFormat = if Table.RowCount(table) > 0 then
                    let cycleName = Table.FirstN(table, 1){0}[cycle_name] in
                    // Accept both weekly format (C##W##) and bi-weekly format (##BW##)
                    // Weekly: Must start with "C", contain "W", and be 7 characters (e.g., "26C01W02")
                    // Bi-weekly: Must match pattern ##BW## where ## is 2-digit year and 2-digit number (e.g., "26BW01")
                    let
                        isWeekly = Text.StartsWith(cycleName, "C") and Text.Contains(cycleName, "W") and Text.Length(cycleName) = 7,
                        isBiWeekly = Text.Length(cycleName) = 6 and Text.Middle(cycleName, 2, 2) = "BW"
                    in
                        isWeekly or isBiWeekly
                else false
            ],
            
            validationResult = [
                ValidationDateTime = DateTime.ToText(DateTime.LocalNow()),
                AllChecksPass = validationChecks[HasData] and validationChecks[HasCycleColumn] and 
                               validationChecks[HasValidCycleName] and validationChecks[HasValidPath] and 
                               validationChecks[CycleNameFormat],
                ValidationChecks = validationChecks,
                ExportRecommendation = if validationChecks[HasData] and validationChecks[HasCycleColumn] and 
                                         validationChecks[HasValidCycleName] and validationChecks[HasValidPath] and 
                                         validationChecks[CycleNameFormat] then
                    "READY_FOR_EXPORT"
                else if not validationChecks[HasData] then
                    "NO_DATA_TO_EXPORT"
                else if not validationChecks[HasCycleColumn] then
                    "MISSING_CYCLE_COLUMN"
                else if not validationChecks[HasValidCycleName] then
                    "INVALID_CYCLE_NAME"
                else
                    "VALIDATION_FAILED",
                Issues = List.Select(Record.FieldNames(validationChecks), (field) => 
                    if Record.Field(validationChecks, field) = false then field else null)
            ]
        in
            validationResult,
    
    // MAIN FUNCTIONS EXPORT
    ExportFunctions = [
        GenerateCycleFilename = GenerateCycleFilename,
        StandardizeColumnOrder = StandardizeColumnOrder,
        GenerateExportPath = GenerateExportPath,
        PrepareForExport = PrepareForExport,
        PrepareBatchExport = PrepareBatchExport,
        ValidateExportReadiness = ValidateExportReadiness
    ]
in
    ExportFunctions

// q_CallTypeCategories
// 🕒 2026_01_13_11_11_31
// Project: m_code/q_CallTypeCategories.m
// Author: R. A. Carucci
// Purpose: Staging query to load and buffer call type mapping CSV for category and response type classification

// ===========================================
// STAGING QUERY: Call Type Categories
// Purpose: Load and buffer call type mapping CSV
// Disable Load: Yes (referenced by Updated_All_Crimes)
// Optimized: Removed PromoteAllScalars, simplified transformation
// ===========================================
let CallTypeCategoriesRaw = Csv.Document(
        File.Contents("C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Classifications\CallTypes\CallType_Categories.csv"),
        [ Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv ]),
    CallTypeCategories0 = Table.PromoteHeaders(CallTypeCategoriesRaw),
    CallTypeCategories = Table.Buffer(Table.TransformColumnTypes(
        CallTypeCategories0, {{"Incident", type text},
                              {"Incident_Norm", type text},
                              {"Category_Type", type text},
                              {"Response_Type", type text}}))
                             in CallTypeCategories

// q_CycleCalendar
// 🕒 2026_01_26_17_45_00
// Project: m_code/q_CycleCalendar.m
// Author: R. A. Carucci
// Purpose: Staging query to load and buffer cycle calendar CSV with 7-day and 28-day cycle date ranges for period classification and lagday calculations

// ===========================================
// STAGING QUERY: Cycle Calendar
// Purpose: Load and buffer cycle calendar CSV
// Disable Load: Yes (referenced by Updated_All_Crimes)
// Updated: 2026-01-26 - Added BiWeekly_Report_Name column for bi-weekly reporting (filename: 7Day_28Day_Cycle_20260106.csv)
// ===========================================
let CycleCalendarRaw = Csv.Document(
        File.Contents("C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv"),
        [ Encoding = 65001, Delimiter = ",", QuoteStyle = QuoteStyle.Csv ]),
    CycleCalendarTable0 = Table.PromoteHeaders(CycleCalendarRaw),
    CycleCalendarTyped = Table.TransformColumnTypes(
        CycleCalendarTable0, {{"Report_Due_Date", type date},
                              {"7_Day_Start", type date},
                              {"7_Day_End", type date},
                              {"28_Day_Start", type date},
                              {"28_Day_End", type date},
                              {"Report_Name", type text},
                              {"BiWeekly_Report_Name", type nullable text}}),
    CycleCalendar = Table.Buffer(CycleCalendarTyped) in CycleCalendar

// q_RMS_Source
// 🕒 2026_01_13_11_11_31
// Project: m_code/q_RMS_Source.m
// Author: R. A. Carucci
// Purpose: Staging query to automatically load the most recent RMS Excel export file from the designated folder for processing

// ===========================================
// STAGING QUERY: RMS Source Data
// Purpose: Load latest Excel file from folder
// Disable Load: Yes (referenced by Updated_All_Crimes)
// ===========================================
let FolderPath = "C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa",
    AllFiles = Folder.Files(FolderPath),
    XlsxFiles = Table.SelectRows(
        AllFiles,
        each Text.EndsWith([Name], ".xlsx", Comparer.OrdinalIgnoreCase)),
    SortedFiles = Table.Sort(XlsxFiles, {{"Date modified", Order.Descending}}),
    LatestFilePath = SortedFiles{0}[Folder Path] & SortedFiles{0}[Name],
    Source = Excel.Workbook(File.Contents(LatestFilePath), true),
    FirstTable = Source{0}[Data],
    #"Changed Type" = Table.TransformColumnTypes(FirstTable,{{"Incident Time", type time}, {"Incident Time_Between", type time}, {"Report Time", type time}}),
    #"Trimmed Text" = Table.TransformColumns(#"Changed Type",{{"Narrative", Text.Trim, type text}}),
    #"Cleaned Text" = Table.TransformColumns(#"Trimmed Text",{{"Narrative", Text.Clean, type text}}) in #"Cleaned Text"