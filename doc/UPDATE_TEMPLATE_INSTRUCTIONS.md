# URGENT: Update Base_Report.pbix Template

**Date:** 2026-02-10  
**Purpose:** Add automatic path detection to Power BI template

---

## What This Fixes

✅ **No more manual path editing** - Template will automatically find the correct data file  
✅ **Works for every cycle** - Just copy, open, and refresh  
✅ **Saves 2-3 minutes** per report  

---

## Instructions

### Step 1: Open the Template

1. Navigate to: `C:\Users\carucci_r\OneDrive - City of Hackensack\08_Templates\`
2. Open: `Base_Report.pbix`

---

### Step 2: Update the M Code

1. Click **Home** > **Transform Data** (opens Power Query Editor)

2. In the left pane, find your data query (probably named `All_Crimes` or `All_Crimes_Simple`)

3. Click **Advanced Editor** (top ribbon)

4. **Replace the entire M code** with the new version below

---

### Step 3: New M Code (Copy This)

```m
// 2026_02_10 - AUTOMATIC PATH DETECTION VERSION
// No manual path editing needed - automatically finds most recent cycle data!

let
    // ===========================================
    // AUTOMATIC PATH DETECTION
    // ===========================================
    // Base directory for all SCRPA reports
    BaseDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based",
    
    // Get the current year
    CurrentYear = Number.ToText(Date.Year(DateTime.LocalNow())),
    
    // Build path to current year's folder
    YearFolder = BaseDir & "\" & CurrentYear,
    
    // Get all folders in the year directory and find the most recent one
    AllFolders = Folder.Files(YearFolder),
    
    // Filter to only cycle folders (start with year, e.g., "26C" or "26BW")
    CycleFolders = Table.SelectRows(AllFolders, each Text.StartsWith([Name], Text.End(CurrentYear, 2))),
    
    // Sort by date modified (most recent first)
    SortedFolders = Table.Sort(CycleFolders, {{"Date modified", Order.Descending}}),
    
    // Get the most recent cycle folder path
    LatestCyclePath = SortedFolders{0}[Folder Path],
    
    // Build full path to CSV
    FilePath = LatestCyclePath & "Data\SCRPA_All_Crimes_Enhanced.csv",

    // ===========================================
    // LOAD CSV
    // ===========================================
    Source = Csv.Document(
        File.Contents(FilePath),
        [
            Delimiter = ",",
            Columns = 66,
            Encoding = 65001,
            QuoteStyle = QuoteStyle.Csv
        ]
    ),

    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

    // ===========================================
    // TYPE CONVERSIONS
    // ===========================================
    TypedTable = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"Case Number", type text},
            {"Incident Date", type text},
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
            {"BestTimeValue", type time},
            {"TimeSource", type text},
            {"Incident_Time", type text},
            {"Incident_Date", type text},
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

    Result = TypedTable

in
    Result
```

---

### Step 4: Apply and Test

1. Click **Done** (closes Advanced Editor)

2. Click **Close & Apply** (saves and refreshes data)

3. **Test it:** 
   - It should load data from your most recent cycle folder
   - Check the record count (bottom right) - should match your latest cycle

4. **Save the template:**
   - Go to **File** > **Save As**
   - Save back to: `C:\Users\carucci_r\OneDrive - City of Hackensack\08_Templates\Base_Report.pbix`
   - ⚠️ **Important:** Overwrite the existing template

---

### Step 5: Verify It Works

1. Close Power BI

2. Go to your current cycle folder:
   ```
   Time_Based\2026\26C02W06_26_02_10\
   ```

3. Delete the old PBIX file if it exists

4. Copy the updated template:
   ```
   From: 08_Templates\Base_Report.pbix
   To: Time_Based\2026\26C02W06_26_02_10\26C02W06_26_02_10.pbix
   ```

5. Open the copied PBIX

6. Click **Refresh**

7. It should automatically load the correct data (252 records)

---

## How It Works

The new M code:
1. Looks in the `Time_Based\[CURRENT_YEAR]\` folder
2. Finds all cycle folders (start with year code like "26")
3. Sorts by last modified date
4. Loads CSV from the **most recent** cycle folder's Data subfolder

**Benefits:**
- ✅ No manual path editing
- ✅ Always uses the most recent data
- ✅ Template works across all cycles
- ✅ Just copy and refresh!

---

## Troubleshooting

### Error: "We couldn't find any Data"

**Cause:** M code can't find the Time_Based folder

**Solution:** 
Check the `BaseDir` path in line 6 of the M code:
```m
BaseDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based",
```

Make sure this matches your actual folder structure.

---

### Error: "Expression.Error: We cannot apply field access"

**Cause:** No cycle folders found in the year directory

**Solution:**
1. Make sure you have at least one cycle folder for the current year
2. Cycle folders must start with the year code (e.g., "26C" or "26BW")

---

## Next Steps

After updating the template:
1. ✅ Run your next bi-weekly report
2. ✅ Just open PBIX and click Refresh (no path editing!)
3. ✅ Charts should display correctly automatically

**This is a one-time update** - you'll never need to manually edit paths again!

---

## Questions?

See the full workflow documentation:
```
16_Reports\SCRPA\BI_WEEKLY_WORKFLOW.md
```
