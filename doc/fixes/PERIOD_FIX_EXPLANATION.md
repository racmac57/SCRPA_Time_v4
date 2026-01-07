# Period Calculation Fix - Explanation

## Problem Found

From the CSV, both cases are showing **"28-Day"** instead of expected values:
- **Case 26-001094** (01/04/2026): Shows "28-Day" but should be **"7-Day"**
- **Case 25-113412** (12/29/2025): Shows "28-Day" but should be **"Prior Year"**

## Root Cause

The 7-Day period check was failing, causing incidents to fall through to the 28-Day check. The 28-Day window (12/09/2025 - 1/05/2026) is wider, so it was catching both cases.

## Fix Applied

1. **Improved cycle detection logic** - Better handling when Today is after cycle end
2. **Explicit null checks** - Added validation for cycle boundary values
3. **Clearer logic flow** - Separated 7-Day and 28-Day checks with explicit variables
4. **Prevented 28-Day from matching if 7-Day should match** - Added `not in7Day` condition

## Updated Logic

```m
// 7-Day check: Incident_Date falls within current 7-day cycle boundaries
in7Day = cycleStartValid and cycleEndValid and dI <> null 
         and dI >= CurrentCycleStart and dI <= CurrentCycleEnd

// 28-Day check: Only if NOT in 7-Day
in28Day = not in7Day and cycle28StartValid and cycle28EndValid 
          and dI <> null and dI >= CurrentCycle28DayStart and dI <= CurrentCycle28DayEnd
```

## Expected Results After Fix

### Case 26-001094 (Burglary - Residence)
- **Incident Date**: 01/04/2026
- **Expected**: Period = **"7-Day"** ✅
- **Reason**: 01/04/2026 is within 7-Day window (12/30/2025 - 1/05/2026)

### Case 25-113412 (Burglary - Auto)
- **Incident Date**: 12/29/2025
- **Expected**: Period = **"Prior Year"** ✅
- **Reason**: 12/29/2025 is before cycle start (12/30/2025) and is 2025 (prior year)

## Next Steps

1. **Update Power BI template** with the fixed M code
2. **Refresh the query** in Power BI
3. **Verify Period values** for both cases:
   - Case 26-001094 should show "7-Day"
   - Case 25-113412 should show "Prior Year"
4. **Check diagnostic column** `_Period_Debug` to see the calculation details

## Diagnostic Column

The `_Period_Debug` column will show:
- The incident date being compared
- Whether current cycle was found
- Cycle start/end dates
- Whether it matches 7-Day or 28-Day
- The incident year

This helps verify the fix is working correctly.
