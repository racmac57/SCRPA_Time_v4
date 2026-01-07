let
    // -----------------------------
    // Helpers
    // -----------------------------
    CoalesceText = (a as nullable text, b as nullable text) as nullable text =>
        if a = null or a = "" then b else a,
    CoalesceAny = (a as any, b as any) as any =>
        if a = null then b else a,

    AsTime =
        (v as any) as nullable time =>
            if v = null or v = "" then null
            else if Value.Is(v, type time) then v
            else if Value.Is(v, type duration) then (try Time.From(v) otherwise null)
            else if Value.Is(v, type datetime) then Time.From(v)
            else if Value.Is(v, type number) then (try Time.From(v) otherwise null)
            else if Value.Is(v, type text) then
                let
                    t = Text.Trim(Text.From(v)),
                    t1 = (try Time.FromText(t) otherwise null),
                    t2 = if t1 = null then (try Time.FromText(t & ":00") otherwise null) else t1
                in
                    t2
            else null,

    AsTimeQuick =
        (v as any) as nullable time =>
            if v = null or v = "" then null
            else if Value.Is(v, type time) then v
            else if Value.Is(v, type datetime) then Time.From(v)
            else if Value.Is(v, type duration) then (try Time.From(v) otherwise null)
            else if Value.Is(v, type number) then (try Time.From(v) otherwise null)
            else if Value.Is(v, type text) then (try Time.FromText(Text.Trim(Text.From(v))) otherwise null)
            else null,

    AsDate =
        (v as any) as nullable date =>
            if v = null or v = "" then null
            else if Value.Is(v, type date) then v
            else if Value.Is(v, type datetime) then Date.From(v)
            else if Value.Is(v, type number) then (try Date.From(v) otherwise null)
            else if Value.Is(v, type text) then (try Date.FromText(Text.From(v)) otherwise null)
            else null,

    // ===========================================
    // STAGED SOURCES (NO File.Contents / Folder.Files HERE)
    // ===========================================
    FirstTable_Staged = Table.Buffer(q_RMS_Source),
    CycleCalendar_Staged = q_CycleCalendar,
    CallTypeCategories_Staged = q_CallTypeCategories,

    // Compute "Today" once
    Today = Date.From(DateTime.LocalNow()),


    // ===========================================
    // ENHANCED TIME PROCESSING WITH CASCADING LOGIC
    // ===========================================
    BestTimeValueAdded = Table.AddColumn(
        FirstTable_Staged,
        "BestTimeValue",
        each
            let
                IT = try [Incident Time] otherwise null,
                ITB = try [Incident Time_Between] otherwise null,
                RT = try [Report Time] otherwise null,

                PIT = AsTime(IT),
                PITB = AsTime(ITB),
                PRT = AsTime(RT)
            in
                if PIT <> null then PIT else if PITB <> null then PITB else PRT,
        type nullable time
    ),

    TimeSourceAdded = Table.AddColumn(
        BestTimeValueAdded,
        "TimeSource",
        each
            let
                PIT = AsTimeQuick(try [Incident Time] otherwise null),
                PITB = AsTimeQuick(try [Incident Time_Between] otherwise null),
                PRT = AsTimeQuick(try [Report Time] otherwise null)
            in
                if PIT <> null then "Incident Time"
                else if PITB <> null then "Incident Time_Between"
                else if PRT <> null then "Report Time"
                else "None",
        type text
    ),

    Incident_Time_Added = Table.AddColumn(
        TimeSourceAdded,
        "Incident_Time",
        each
            let bt = [BestTimeValue]
            in
                if bt <> null then
                    Text.PadStart(Text.From(Time.Hour(bt)), 2, "0")
                        & ":" & Text.PadStart(Text.From(Time.Minute(bt)), 2, "0")
                        & ":" & Text.PadStart(Text.From(Time.Second(bt)), 2, "0")
                else "00:00:00",
        type text
    ),

    // ===========================================
    // INCIDENT DATE (TEXT + DATE) WITH CASCADE
    // ===========================================
    Incident_Date_Added = Table.AddColumn(
        Incident_Time_Added,
        "Incident_Date",
        each
            let
                dIT = AsDate(try [Incident Date] otherwise null),
                dITB = AsDate(try [Incident Date_Between] otherwise null),
                dRT = AsDate(try [Report Date] otherwise null),
                Best = if dIT <> null then dIT else if dITB <> null then dITB else dRT
            in
                if Best <> null then Date.ToText(Best, "MM/dd/yy") else "Unknown",
        type text
    ),

    Incident_Date_Date_Added = Table.AddColumn(
        Incident_Date_Added,
        "Incident_Date_Date",
        each
            let
                dIT = AsDate(try [Incident Date] otherwise null),
                dITB = AsDate(try [Incident Date_Between] otherwise null),
                dRT = AsDate(try [Report Date] otherwise null)
            in
                if dIT <> null then dIT else if dITB <> null then dITB else dRT,
        type date
    ),

    // ===========================================
    // REPORT DATE (DATE + TEXT)
    // ===========================================
    Report_Date_Added = Table.AddColumn(
        Incident_Date_Date_Added,
        "Report_Date",
        each
            let
                dRD = AsDate(try [Report Date] otherwise null),
                dED = AsDate(try [EntryDate] otherwise null)
            in
                CoalesceAny(dRD, CoalesceAny(dED, [Incident_Date_Date])),
        type nullable date
    ),

    Report_Date_Text_Added = Table.AddColumn(
        Report_Date_Added,
        "Report_Date_Text",
        each if [Report_Date] <> null then Date.ToText([Report_Date], "MM/dd/yy") else null,
        type nullable text
    ),

    IncidentToReportDays_Added = Table.AddColumn(
        Report_Date_Text_Added,
        "IncidentToReportDays",
        each if [Report_Date] <> null and [Incident_Date_Date] <> null then Duration.Days([Report_Date] - [Incident_Date_Date]) else null,
        Int64.Type
    ),

    // ===========================================
    // CYCLE CALENDAR - FIND REPORTING CYCLE
    // ===========================================
    // CRITICAL: This handles both mid-cycle refreshes and report-day refreshes
    // - Mid-cycle: Today is within a cycle (e.g., Today = 12/27, cycle = 12/23-12/29)
    // - Report day: Today is after cycle ends (e.g., Today = 12/30, cycle ended 12/29)
    //   In this case, find the most recent completed cycle (the one we're reporting on)
    CurrentCycleTbl = 
        let
            // First try: Match Report_Due_Date (most accurate - report day lookup)
            // This is the primary method: find cycle where Report_Due_Date = Today
            MatchReportDate = Table.SelectRows(
                CycleCalendar_Staged,
                each [Report_Due_Date] = Today
            ),
            
            // Second try: Today within a cycle (for mid-cycle refreshes)
            InCycle = Table.SelectRows(
                CycleCalendar_Staged, 
                each Today >= [7_Day_Start] and Today <= [7_Day_End]
            ),
            
            // Third try: Find most recent cycle (for edge cases)
            // This gets the cycle where 7_Day_End is closest to (but not after) Today
            // IMPORTANT: Use <= Today to include cycles that ended on or before today
            MostRecent = 
                if not Table.IsEmpty(MatchReportDate) then
                    MatchReportDate
                else if not Table.IsEmpty(InCycle) then
                    InCycle
                else
                    let
                        EligibleCycles = Table.SelectRows(CycleCalendar_Staged, each [7_Day_End] <= Today),
                        Sorted = Table.Sort(EligibleCycles, {{"7_Day_End", Order.Descending}}),
                        Result = Table.FirstN(Sorted, 1)
                    in
                        Result,
            
            FinalResult = MostRecent
        in
            FinalResult,
    
    HasCurrentCycle = not Table.IsEmpty(CurrentCycleTbl),
    CurrentCycleReportDueDate = if HasCurrentCycle then CurrentCycleTbl{0}[Report_Due_Date] else null,
    CurrentCycleStart = if HasCurrentCycle then CurrentCycleTbl{0}[7_Day_Start] else null,
    CurrentCycleEnd = if HasCurrentCycle then CurrentCycleTbl{0}[7_Day_End] else null,
    CurrentCycle28DayStart = if HasCurrentCycle then CurrentCycleTbl{0}[28_Day_Start] else null,
    CurrentCycle28DayEnd = if HasCurrentCycle then CurrentCycleTbl{0}[28_Day_End] else null,
    CurrentCycleName = if HasCurrentCycle then CurrentCycleTbl{0}[Report_Name] else null,

    // ===========================================
    // PERIOD CALCULATION (Based on Incident_Date vs Cycle Boundaries)
    // ===========================================
    // CRITICAL: Period must be based on Incident_Date, NOT Report_Date
    // This ensures charts show when crimes OCCURRED, not when they were reported
    // Backfill cases (incident before cycle, reported during cycle) should NOT appear in 7-Day charts
    // YTD automatically includes all incidents from current year (2026) outside 7-Day/28-Day windows
    // Prior year incidents (2025) are labeled as "Prior Year" to distinguish from older years
    Period_Added = Table.AddColumn(
        IncidentToReportDays_Added,
        "Period",
        each
            let 
                dI = [Incident_Date_Date],
                incidentYear = if dI = null then null else Date.Year(dI),
                currentYear = Date.Year(Today),
                // Explicit null checks for cycle boundaries
                cycleStartValid = HasCurrentCycle and CurrentCycleStart <> null,
                cycleEndValid = HasCurrentCycle and CurrentCycleEnd <> null,
                cycle28StartValid = HasCurrentCycle and CurrentCycle28DayStart <> null,
                cycle28EndValid = HasCurrentCycle and CurrentCycle28DayEnd <> null,
                // 7-Day check: Incident_Date falls within current 7-day cycle boundaries
                in7Day = cycleStartValid and cycleEndValid and dI <> null and dI >= CurrentCycleStart and dI <= CurrentCycleEnd,
                // 28-Day check: Incident_Date falls within current 28-day cycle boundaries (but not 7-Day)
                in28Day = not in7Day and cycle28StartValid and cycle28EndValid and dI <> null and dI >= CurrentCycle28DayStart and dI <= CurrentCycle28DayEnd
            in
                if dI = null then "Historical"
                // 7-Day period: Check first (highest priority)
                else if in7Day then "7-Day"
                // Prior year (2025): Check before 28-Day to prevent prior year incidents from being classified as 28-Day
                // Prior year incidents should be "Prior Year" even if they fall within 28-Day window
                else if incidentYear = currentYear - 1 then "Prior Year"
                // 28-Day period: Check third (only for current year incidents, not prior year)
                else if in28Day then "28-Day"
                // YTD: incident occurred in current year (2026) but outside 7-Day/28-Day windows
                else if incidentYear = currentYear then "YTD"
                // Older years (2024 and earlier): Generic "Historical"
                else "Historical",
        type text
    ),

    // ===========================================
    // DIAGNOSTIC: Period Calculation Debug (can be removed after verification)
    // ===========================================
    Period_Debug_Added = Table.AddColumn(
        Period_Added,
        "_Period_Debug",
        each
            let 
                dI = [Incident_Date_Date],
                incidentYear = if dI = null then null else Date.Year(dI),
                currentYear = Date.Year(Today),
                in7Day = HasCurrentCycle and dI <> null and dI >= CurrentCycleStart and dI <= CurrentCycleEnd,
                in28Day = HasCurrentCycle and CurrentCycle28DayStart <> null and CurrentCycle28DayEnd <> null and dI <> null and dI >= CurrentCycle28DayStart and dI <= CurrentCycle28DayEnd
            in
                "dI=" & (if dI = null then "NULL" else Text.From(dI))
                & " | HasCycle=" & Text.From(HasCurrentCycle)
                & " | ReportDue=" & (if HasCurrentCycle then Text.From(CurrentCycleReportDueDate) else "NULL")
                & " | CycleStart=" & (if HasCurrentCycle then Text.From(CurrentCycleStart) else "NULL")
                & " | CycleEnd=" & (if HasCurrentCycle then Text.From(CurrentCycleEnd) else "NULL")
                & " | in7Day=" & Text.From(in7Day)
                & " | in28Day=" & Text.From(in28Day)
                & " | Year=" & (if incidentYear = null then "NULL" else Text.From(incidentYear)),
        type text
    ),

    Period_SortKey_Added = Table.AddColumn(
        Period_Debug_Added,
        "Period_SortKey",
        each 
            let p = [Period]
            in
                if p = "7-Day" then 1 
                else if p = "28-Day" then 2 
                else if p = "YTD" then 3 
                else if p = "Prior Year" then 4  // Prior year (e.g., 2025)
                else if p = "Historical" then 5  // Older years (2024 and earlier)
                else 99,
        Int64.Type
    ),

    CycleName_Added = Table.AddColumn(
        Period_SortKey_Added,
        "cycle_name",
        each
            let d = [Incident_Date_Date]
            in
                if d = null then "Unknown"
                else
                    let m = Table.SelectRows(CycleCalendar_Staged, each d >= [7_Day_Start] and d <= [7_Day_End])
                    in if Table.IsEmpty(m) then "Historical" else m{0}[Report_Name],
        type text
    ),

    Backfill_Flag_Added = Table.AddColumn(
        CycleName_Added,
        "Backfill_7Day",
        each
            let dI = [Incident_Date_Date], dR = [Report_Date]
            in
                HasCurrentCycle and dI <> null and dR <> null and dI < CurrentCycleStart and dR >= CurrentCycleStart and dR <= CurrentCycleEnd,
        type logical
    ),

    Cycle_Name_Adjusted = Table.AddColumn(
        Backfill_Flag_Added,
        "cycle_name_adjusted",
        each if [Backfill_7Day] then CoalesceText(CurrentCycleName, [cycle_name]) else [cycle_name],
        type text
    ),

    // ===========================================
    // IS CURRENT 7-DAY CYCLE (for dynamic filtering)
    // ===========================================
    IsCurrent7DayCycle_Added = Table.AddColumn(
        Cycle_Name_Adjusted,
        "IsCurrent7DayCycle",
        each
            let dR = [Report_Date]
            in
                if HasCurrentCycle and dR <> null then
                    dR >= CurrentCycleStart and dR <= CurrentCycleEnd
                else false,
        type logical
    ),

    IsLagDay_Added = Table.AddColumn(
        IsCurrent7DayCycle_Added,
        "IsLagDay",
        each
            let dI = [Incident_Date_Date], dR = [Report_Date]
            in
                if dI = null or dR = null then false
                else
                    let
                        ReportCycle = Table.SelectRows(CycleCalendar_Staged, each dR >= [7_Day_Start] and dR <= [7_Day_End]),
                        CycleStartForReport = if Table.IsEmpty(ReportCycle) then null else ReportCycle{0}[7_Day_Start]
                    in
                        CycleStartForReport <> null and dI < CycleStartForReport,
        type logical
    ),

    LagDays_Added = Table.AddColumn(
        IsLagDay_Added,
        "LagDays",
        each
            let dI = [Incident_Date_Date], dR = [Report_Date]
            in
                if dI = null or dR = null then null
                else if not [IsLagDay] then 0
                else
                    let
                        ReportCycle = Table.SelectRows(CycleCalendar_Staged, each dR >= [7_Day_Start] and dR <= [7_Day_End]),
                        CycleStartForReport = if Table.IsEmpty(ReportCycle) then null else ReportCycle{0}[7_Day_Start]
                    in
                        if CycleStartForReport <> null then Duration.Days(CycleStartForReport - dI) else 0,
        Int64.Type
    ),

    // ===========================================
    // TIME OF DAY
    // ===========================================
    StartOfHour_Added = Table.AddColumn(
        LagDays_Added,
        "StartOfHour",
        each
            let bt = [BestTimeValue]
            in if bt <> null then Time.ToText(#time(Time.Hour(bt), 0, 0), "hh:mm:ss") else "00:00:00",
        type text
    ),

    TimeOfDay_Added = Table.AddColumn(
        StartOfHour_Added,
        "TimeOfDay",
        each
            let bt = [BestTimeValue], hr = if bt = null then null else Time.Hour(bt)
            in
                if hr = null then "Unknown Time"
                else if hr >= 4 and hr < 8 then "Early Morning (04:00–07:59)"
                else if hr >= 8 and hr < 12 then "Morning (08:00–11:59)"
                else if hr >= 12 and hr < 16 then "Afternoon (12:00–15:59)"
                else if hr >= 16 and hr < 20 then "Evening Peak (16:00–19:59)"
                else if hr >= 20 and hr < 24 then "Night (20:00–23:59)"
                else "Late Night (00:00–03:59)",
        type text
    ),

    TimeOfDay_SortKey_Added = Table.AddColumn(
        TimeOfDay_Added,
        "TimeOfDay_SortKey",
        each
            let t = [TimeOfDay]
            in
                if t = "Late Night (00:00–03:59)" then 1
                else if t = "Early Morning (04:00–07:59)" then 2
                else if t = "Morning (08:00–11:59)" then 3
                else if t = "Afternoon (12:00–15:59)" then 4
                else if t = "Evening Peak (16:00–19:59)" then 5
                else if t = "Night (20:00–23:59)" then 6
                else if t = "Unknown Time" then 99
                else 0,
        Int64.Type
    ),

    // ===========================================
    // INCIDENT CONSOLIDATION & CATEGORY
    // ===========================================
    AllIncidents_Added = Table.AddColumn(
        TimeOfDay_SortKey_Added,
        "ALL_INCIDENTS",
        each
            let
                i1 = try [Incident Type_1] otherwise null,
                i2 = try [Incident Type_2] otherwise null,
                i3 = try [Incident Type_3] otherwise null
            in
                (if i1 = null then "" else i1)
                    & (if i2 = null or i2 = "" then "" else ", " & i2)
                    & (if i3 = null or i3 = "" then "" else ", " & i3),
        type text
    ),

    CrimeCategory_Added = Table.AddColumn(
        AllIncidents_Added,
        "Crime_Category",
        each
            let
                L = Text.Upper(CoalesceText([ALL_INCIDENTS], "")),
                N = Text.Upper(CoalesceText(try [Narrative] otherwise null, ""))
            in
                if Text.Contains(L, "MOTOR VEHICLE THEFT") and (Text.Contains(N, "THEFT OF HIS PROPERTY") or Text.Contains(N, "THEFT FROM MOTOR VEHICLE"))
                then "Burglary Auto"
                else if Text.Contains(L, "MOTOR VEHICLE THEFT") then "Motor Vehicle Theft"
                else if List.AnyTrue({Text.Contains(L, "BURGLARY - AUTO"), Text.Contains(L, "ATTEMPTED BURGLARY - AUTO"), Text.Contains(L, "THEFT FROM MOTOR VEHICLE")}) then "Burglary Auto"
                else if List.AnyTrue({Text.Contains(L, "BURGLARY - COMMERCIAL"), Text.Contains(L, "ATTEMPTED BURGLARY - COMMERCIAL"), Text.Contains(L, "BURGLARY - RESIDENCE"), Text.Contains(L, "ATTEMPTED BURGLARY - RESIDENCE")}) then "Burglary - Comm & Res"
                else if Text.Contains(L, "ROBBERY") then "Robbery"
                else if List.AnyTrue({Text.Contains(L, "SEXUAL"), Text.Contains(L, "RAPE")}) then "Sexual Offenses"
                else "Other",
        type text
    ),

    CleanIncidentTypes_Added = Table.TransformColumns(
        CrimeCategory_Added,
        {
            {"Incident Type_1", each if _ <> null then Text.BeforeDelimiter(_, " - 2C") else _, type text},
            {"Incident Type_2", each if _ <> null then Text.BeforeDelimiter(_, " - 2C") else _, type text},
            {"Incident Type_3", each if _ <> null then Text.BeforeDelimiter(_, " - 2C") else _, type text}
        }
    ),

    Incident_Type_1_Norm_Added = Table.AddColumn(
        CleanIncidentTypes_Added,
        "Incident_Type_1_Norm",
        each if [Incident Type_1] <> null then Text.Replace([Incident Type_1], "Attempted Burglary", "Burglary") else null,
        type nullable text
    ),
    Incident_Type_2_Norm_Added = Table.AddColumn(
        Incident_Type_1_Norm_Added,
        "Incident_Type_2_Norm",
        each if [Incident Type_2] <> null then Text.Replace([Incident Type_2], "Attempted Burglary", "Burglary") else null,
        type nullable text
    ),
    Incident_Type_3_Norm_Added = Table.AddColumn(
        Incident_Type_2_Norm_Added,
        "Incident_Type_3_Norm",
        each if [Incident Type_3] <> null then Text.Replace([Incident Type_3], "Attempted Burglary", "Burglary") else null,
        type nullable text
    ),

    Narrative_Cleaned = Table.TransformColumns(
        Incident_Type_3_Norm_Added,
        {
            {
                "Narrative",
                each
                    let
                        t = _,
                        step1 =
                            if t = null or t = "" then null
                            else Text.Replace(Text.Replace(Text.Replace(t, "#(cr)#(lf)", " "), "#(lf)", " "), "#(cr)", " "),
                        step2 =
                            if step1 = null then null
                            else Text.Replace(Text.Replace(Text.Replace(step1, "    ", " "), "   ", " "), "  ", " "),
                        step3 = if step2 = null then null else Text.Clean(step2),
                        step4 = if step3 = null then null else Text.Trim(step3)
                    in
                        if step4 = null or step4 = "" then null else step4,
                type text
            }
        }
    ),

    Vehicle_1_Added = Table.AddColumn(
        Narrative_Cleaned,
        "Vehicle_1",
        each
            let
                regState = CoalesceText(try Text.From([#"Reg State 1"]) otherwise null, ""),
                registration = CoalesceText(try Text.From([#"Registration 1"]) otherwise null, ""),
                make = CoalesceText(try Text.From([Make1]) otherwise null, ""),
                model = CoalesceText(try Text.From([Model1]) otherwise null, ""),
                stateReg =
                    if regState <> "" and registration <> "" then regState & " - " & registration
                    else if registration <> "" then registration
                    else regState,
                makeModel =
                    if make <> "" and model <> "" then make & "/" & model
                    else if make <> "" then make
                    else model,
                result =
                    if stateReg <> "" and makeModel <> "" then stateReg & ", " & makeModel
                    else if stateReg <> "" then stateReg
                    else makeModel
            in
                if result = null or result = "" then null else Text.Upper(result),
        type nullable text
    ),

    Vehicle_2_Added = Table.AddColumn(
        Vehicle_1_Added,
        "Vehicle_2",
        each
            let
                regState = CoalesceText(try Text.From([#"Reg State 2"]) otherwise null, ""),
                registration = CoalesceText(try Text.From([#"Registration 2"]) otherwise null, ""),
                make = CoalesceText(try Text.From([Make2]) otherwise null, ""),
                model = CoalesceText(try Text.From([Model2]) otherwise null, ""),
                stateReg =
                    if regState <> "" and registration <> "" then regState & " - " & registration
                    else if registration <> "" then registration
                    else regState,
                makeModel =
                    if make <> "" and model <> "" then make & "/" & model
                    else if make <> "" then make
                    else model,
                result =
                    if stateReg <> "" and makeModel <> "" then stateReg & ", " & makeModel
                    else if stateReg <> "" then stateReg
                    else makeModel
            in
                if result = null or result = "" then null else Text.Upper(result),
        type nullable text
    ),

    Vehicle_Combined_Added = Table.AddColumn(
        Vehicle_2_Added,
        "Vehicle_1_and_Vehicle_2",
        each if [Vehicle_1] <> null and [Vehicle_2] <> null then [Vehicle_1] & " | " & [Vehicle_2] else null,
        type nullable text
    ),

    Clean_Address_Added = Table.AddColumn(
        Vehicle_Combined_Added,
        "Clean_Address",
        each
            let addr = CoalesceText(Text.Trim(CoalesceText(try Text.From([FullAddress]) otherwise null, "")), "")
            in
                if addr = "" then null
                else
                    let cleaned = Text.BeforeDelimiter(addr, ", Hackensack, NJ", {0, RelativePosition.FromStart})
                    in if cleaned <> "" then cleaned else addr,
        type nullable text
    ),

    // ===========================================
    // FAST CATEGORY/RESPONSE MAPPING VIA JOINS (from staged CallTypeCategories)
    // ===========================================
    WithIncidentKey = Table.AddColumn(
        Clean_Address_Added,
        "IncidentKey",
        each CoalesceText([ALL_INCIDENTS], try [Incident Type_1] otherwise null),
        type text
    ),

    Join_Exact_Incident = Table.NestedJoin(WithIncidentKey, {"IncidentKey"}, CallTypeCategories_Staged, {"Incident"}, "CT_Exact", JoinKind.LeftOuter),
    Join_Exact_IncidentNorm = Table.NestedJoin(Join_Exact_Incident, {"IncidentKey"}, CallTypeCategories_Staged, {"Incident_Norm"}, "CT_ExactNorm", JoinKind.LeftOuter),

    NeedFuzzyFlag = Table.AddColumn(
        Join_Exact_IncidentNorm,
        "_NeedFuzzy",
        each (try Table.IsEmpty([CT_Exact]) otherwise true) and (try Table.IsEmpty([CT_ExactNorm]) otherwise true),
        type logical
    ),

    OnlyNeedFuzzy = Table.SelectRows(NeedFuzzyFlag, each [_NeedFuzzy] = true),

    FuzzyJoined = Table.FuzzyNestedJoin(
        OnlyNeedFuzzy,
        {"IncidentKey"},
        CallTypeCategories_Staged,
        {"Incident"},
        "CT_Fuzzy",
        JoinKind.LeftOuter,
        [IgnoreCase = true, IgnoreSpace = true, Threshold = 0.8]
    ),

    FuzzyMap = Table.SelectColumns(FuzzyJoined, {"IncidentKey", "CT_Fuzzy"}),

    Recombined = Table.NestedJoin(NeedFuzzyFlag, {"IncidentKey"}, FuzzyMap, {"IncidentKey"}, "CT_FuzzyMap", JoinKind.LeftOuter),

    Expanded = Table.TransformColumns(
        Recombined,
        {
            {"CT_Exact", each if _ is table and not Table.IsEmpty(_) then _ else null},
            {"CT_ExactNorm", each if _ is table and not Table.IsEmpty(_) then _ else null},
            {"CT_FuzzyMap", each if _ is table and not Table.IsEmpty(_) and _{0}[CT_Fuzzy] is table and not Table.IsEmpty(_{0}[CT_Fuzzy]) then _{0}[CT_Fuzzy] else null}
        }
    ),

    TakeCategory = Table.AddColumn(
        Expanded,
        "Category_Type",
        each
            let
                a = try [CT_Exact]{0}[Category_Type] otherwise null,
                b = if a = null then (try [CT_ExactNorm]{0}[Category_Type] otherwise null) else null,
                c = if a = null and b = null then (try [CT_FuzzyMap]{0}[Category_Type] otherwise null) else null
            in
                CoalesceText(a, CoalesceText(b, CoalesceText(c, "Unknown"))),
        type text
    ),

    TakeResponse = Table.AddColumn(
        TakeCategory,
        "Response_Type",
        each
            let
                a = try [CT_Exact]{0}[Response_Type] otherwise null,
                b = if a = null then (try [CT_ExactNorm]{0}[Response_Type] otherwise null) else null,
                c = if a = null and b = null then (try [CT_FuzzyMap]{0}[Response_Type] otherwise null) else null
            in
                CoalesceText(a, CoalesceText(b, CoalesceText(c, "Unknown"))),
        type text
    ),

    Category_Response_Added = Table.RemoveColumns(TakeResponse, {"CT_Exact", "CT_ExactNorm", "CT_FuzzyMap", "_NeedFuzzy"}),

    TimeValidation_Added = Table.AddColumn(
        Category_Response_Added,
        "Time_Validation",
        each
            "Source: " & [TimeSource]
                & " | Original IT: " & (if [Incident Time] <> null then Text.From([Incident Time]) else "null")
                & " | Original ITB: " & (if [Incident Time_Between] <> null then Text.From([Incident Time_Between]) else "null")
                & " | Original RT: " & (if [Report Time] <> null then Text.From([Report Time]) else "null")
                & " | Cascaded: " & (if [BestTimeValue] <> null then Time.ToText([BestTimeValue]) else "null"),
        type text
    ),

    FinalResult = TimeValidation_Added,

#"Sorted Rows" = Table.Sort(
        FinalResult,
        {{"Incident Date", Order.Ascending}, {"Period", Order.Descending}, {"Report Date", Order.Ascending}, {"Report_Date", Order.Ascending}}
    ),

#"Changed Type" = Table.TransformColumnTypes(
#"Sorted Rows",
        {{"Incident Time_Between", type time}, {"Incident Time", type time}, {"Report Time", type time}}
    )
in
#"Changed Type"