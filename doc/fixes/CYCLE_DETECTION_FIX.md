# Cycle Detection Fix - Report_Due_Date Implementation

## Problem Identified

The cycle detection logic was finding the wrong cycle, causing incorrect Period classifications:

**Case 26-001094** (01/04/2026):
- Expected: "7-Day" (incident within current cycle 12/30/2025 - 01/05/2026)
- Actual: "28-Day" (wrong cycle detected: 01/06/2026 - 01/12/2026)

**Case 25-113412** (12/29/2025):
- Expected: "Prior Year" (2025 incident, before cycle start)
- Actual: "28-Day" (wrong cycle detected)

## Root Cause

The cycle calendar CSV has a `Report_Due_Date` column that indicates which cycle should be used for a given report date. However:

1. **`q_CycleCalendar.m` was NOT loading `Report_Due_Date`** - Only loading 7_Day_Start, 7_Day_End, 28_Day_Start, 28_Day_End, Report_Name
2. **Cycle detection logic was not using `Report_Due_Date`** - It was trying to find cycles where Today falls within the 7-day range, which could match the wrong cycle

## Solution Applied

### 1. Updated `q_CycleCalendar.m`
- Added `Report_Due_Date` to the column type transformation
- Now loads: Report_Due_Date, 7_Day_Start, 7_Day_End, 28_Day_Start, 28_Day_End, Report_Name

### 2. Updated Cycle Detection Logic in `all_crimes.m`
Changed from:
```m
// First: Check if Today is within a cycle
// Second: Find most recent cycle that ended on/before Today
```

To:
```m
// First: Match Report_Due_Date = Today (most accurate - report day lookup)
// Second: Check if Today is within a cycle (for mid-cycle refreshes)
// Third: Find most recent cycle that ended on/before Today (edge cases)
```

### 3. Updated Diagnostic Column
- Added `CurrentCycleReportDueDate` variable
- Diagnostic output now shows `ReportDue=` to verify correct cycle match

## Expected Results After Fix

### When Today = 01/06/2026:
- **Cycle Detected**: 26C01W01 (Report_Due_Date = 01/06/2026)
- **7-Day Range**: 12/30/2025 to 01/05/2026
- **28-Day Range**: 12/09/2025 to 01/05/2026

### Case 26-001094 (01/04/2026):
- **Period**: "7-Day" ✅
- **Reason**: 01/04/2026 is within 7-Day range (12/30/2025 - 01/05/2026)

### Case 25-113412 (12/29/2025):
- **Period**: "Prior Year" ✅
- **Reason**: 12/29/2025 is before cycle start (12/30/2025) and is 2025 (prior year)

## Verification Steps

1. **Update Power BI template** with fixed M code
2. **Refresh query** in Power BI
3. **Check diagnostic column** `_Period_Debug`:
   - Should show `ReportDue=1/6/2026`
   - Should show `CycleStart=12/30/2025` and `CycleEnd=1/5/2026`
4. **Verify Period values**:
   - Case 26-001094: Period = "7-Day"
   - Case 25-113412: Period = "Prior Year"

## Technical Details

The cycle calendar CSV structure:
```
Report_Due_Date,7_Day_Start,7_Day_End,28_Day_Start,28_Day_End,Report_Name
01/06/2026,12/30/2025,01/05/2026,12/09/2025,01/05/2026,26C01W01
```

When Today = 01/06/2026, the cycle detection should:
1. Find row where `Report_Due_Date = 01/06/2026`
2. Use that row's 7_Day_Start and 7_Day_End for Period calculation
3. This ensures the correct cycle is used for report generation

---

**Date**: 2026-01-06  
**Status**: ✅ Fixed  
**Files Modified**: `m_code/q_CycleCalendar.m`, `m_code/all_crimes.m`
