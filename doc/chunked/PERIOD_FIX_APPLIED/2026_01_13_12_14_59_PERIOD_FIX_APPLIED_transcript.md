# Period Fix Applied

**Processing Date:** 2026-01-13 12:14:59
**Source File:** PERIOD_FIX_APPLIED.md
**Total Chunks:** 1

---

# Period Classification Fix - Applied

**Date:** 2025-12-30  
**Issue:** 7-Day charts incorrectly showing backfill cases  
**Status:** ✅ Fixed

---

## 🔴 Problem Identified

The `Period` calculation in `all_crimes.m` was using **Report_Date** to determine if an incident should appear in the 7-Day chart. This caused backfill cases (incidents that occurred BEFORE the cycle but were reported DURING the cycle) to incorrectly appear in 7-Day charts. **Example:**
- Case 25-113076: Incident Date 12/20/25, Report Date 12/28/25
- Should appear: **ONLY in lagday table** (backfill case)
- Was appearing: **In 7-Day chart** (incorrect)

---

## ✅ Solution Applied

### 1. Updated `q_CycleCalendar.m`
- Added type conversion for `28_Day_Start` and `28_Day_End` columns
- Ensures 28-day cycle boundaries are properly typed

### 2. Updated `all_crimes.m` Period Calculation

**Changed from:**
```m
// OLD (INCORRECT): Based on Report_Date
IsInCurrent7DayCycle = if HasCurrentCycle and dR <> null then
    dR >= CurrentCycleStart and dR <= CurrentCycleEnd
else false,
...
else if IsInCurrent7DayCycle then "7-Day"
```

**Changed to:**
```m
// NEW (CORRECT): Based on Incident_Date vs Cycle Boundaries
if dI = null then "Historical"
// 7-Day period: Incident_Date falls within current 7-day cycle boundaries
else if HasCurrentCycle and dI >= CurrentCycleStart and dI <= CurrentCycleEnd then "7-Day"
// 28-Day period: Incident_Date falls within current 28-day cycle boundaries
else if HasCurrentCycle and CurrentCycle28DayStart <> null and CurrentCycle28DayEnd <> null 
    and dI >= CurrentCycle28DayStart and dI <= CurrentCycle28DayEnd then "28-Day"
// YTD: incident occurred in current year (based on Incident Date)
else if Date.Year(dI) = Date.Year(Today) then "YTD"
else "Historical"
```

---

## 📊 Expected Results

### For Cycle C13W51 (12/23/25 - 12/29/25):

**Burglary Chart:**
- **Before Fix:** 2 incidents (both backfill cases)
- **After Fix:** 0 incidents ✅

**Lagday Table:**
- **Before Fix:** 2 incidents
- **After Fix:** 2 incidents ✅ (unchanged - already correct)

**Logic:**
- 7-Day charts show only incidents that **OCCURRED** during the cycle (12/23-12/29)
- Backfill cases (incident before cycle, reported during cycle) appear **ONLY** in lagday table
- This provides accurate tactical analysis based on when crimes occurred, not when they were reported

---

## 🔍 Key Distinction

**Cycle Definition (Report Filtering):**
- Based on **Report_Date**
- Determines which incidents are included in the weekly report
- Uses `IsCurrent7DayCycle` column

**Period Classification (Chart Filtering):**
- Based on **Incident_Date**
- Determines which period bucket (7-Day, 28-Day, YTD) an incident appears in
- Uses `Period` column

**Why This Matters:**
- Charts should show **when crimes occurred** for tactical analysis
- Lagday tables show **reporting delays** for administrative tracking
- These are separate concepts and should not be conflated

---

## ✅ Verification Steps

1. **Refresh Power BI data** with updated M code
2. **Check Burglary chart:** Should show 0 in 7-Day period (not 2)
3. **Check lagday table:** Should show 2 burglary cases
4. **Run validation script** (if available) to compare counts:
   ```bash
   python validate_7day_backfill.py <rms_csv> 2025-12-23 2025-12-29
   ```
5. **Verify all crime categories** match expected counts

---

## 📝 Files Modified

1. `q_CycleCalendar.m` - Added 28_Day column type conversions
2. `all_crimes.m` - Fixed Period calculation to use Incident_Date

---

## 🎯 Next Steps

1. **Update Base_Report.pbix** template with corrected M code
2. **Test with current cycle data** to verify counts
3. **Document methodology change** in next report (if needed)
4. **Consider adding validation step** to weekly workflow

---

---

## 🔴 **CRITICAL UPDATE: Current Cycle Lookup Fix**

**Date:** 2025-12-30  
**Issue:** Cycle lookup failing on report due date (Today after cycle end)  
**Status:** ✅ Fixed

### Problem:
When refreshing Power BI on 12/30 (report due date), the cycle (12/23-12/29) has already ended. The lookup `Today >= [7_Day_Start] and Today <= [7_Day_End]` returns EMPTY, causing `HasCurrentCycle = FALSE` and all incidents to show as YTD instead of 7-Day. ### Solution:
Modified `CurrentCycleTbl` lookup to:
1. **First try:** Find cycle where Today is within date range (for mid-cycle refreshes)
2. **Second try:** If empty, find the most recent completed cycle (for report day refreshes)

This ensures the reporting cycle is always found, whether refreshing during the cycle or on/after the report due date. ### Code Change:
```m
// OLD (fails on report day):
CurrentCycleTbl = Table.SelectRows(CycleCalendar_Staged, each Today >= [7_Day_Start] and Today <= [7_Day_End]),

// NEW (works on report day):
CurrentCycleTbl = 
    let
        InCycle = Table.SelectRows(
            CycleCalendar_Staged, 
            each Today >= [7_Day_Start] and Today <= [7_Day_End]
        ),
        MostRecent = 
            if Table.IsEmpty(InCycle) then
                Table.FirstN(
                    Table.Sort(
                        Table.SelectRows(CycleCalendar_Staged, each [7_Day_End] <= Today),
                        {{"7_Day_End", Order.Descending}}
                    ),
                    1
                )
            else InCycle
    in
        MostRecent,
```

**Last Updated:** 2025-12-30  
**Applied By:** AI Assistant (based on Claude AI analysis)

