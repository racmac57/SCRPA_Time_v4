// ===========================================
// STAGING QUERY: Cycle Calendar
// Purpose: Load and buffer cycle calendar CSV
// Disable Load: Yes (referenced by Updated_All_Crimes)
// Updated: 2026-01-06 - File includes 2026 cycle data (filename: 7Day_28Day_Cycle_20260106.csv)
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
                              {"Report_Name", type text}}),
    CycleCalendar = Table.Buffer(CycleCalendarTyped) in CycleCalendar