# Period Calculation Fix - Diagnostic Steps

## Issue
Period column not calculating correctly. Case 26-001094 (Incident Date 01/04/2026) should be "7-Day" but may not be.

## Current Cycle (26C01W01)
- **7-Day**: 12/30/2025 - 1/05/2026 ✅ (confirmed in cycle calendar)
- **28-Day**: 12/09/2025 - 1/05/2026 ✅

## Expected Results

### Case 26-001094 (Burglary - Residence)
- **Incident Date**: 01/04/2026
- **Expected Period**: "7-Day" (01/04/26 is between 12/30/25 and 1/05/26)

### Case 25-113412 (Burglary - Auto)  
- **Incident Date**: 12/29/2025
- **Expected Period**: "Prior Year" (12/29/25 is before cycle start 12/30/25)

## Diagnostic: Check in Power BI

1. **Create a table** with these columns:
   - Case Number
   - Incident_Date_Date
   - Report_Date
   - Period
   - Backfill_7Day
   - LagDays

2. **Filter to your two cases** and check:
   - What Period value is assigned?
   - What is the actual Incident_Date_Date value?

3. **Check cycle detection** - Add a calculated column:
   ```m
   _Debug_Cycle = 
       if HasCurrentCycle then
           Text.From(CurrentCycleStart) & " to " & Text.From(CurrentCycleEnd)
       else "NO CYCLE"
   ```

## Potential Issues

### Issue 1: Current Cycle Not Detected
If `HasCurrentCycle = false`, Period will default to YTD/Historical.

**Check**: Verify cycle 26C01W01 exists and dates are correct.

### Issue 2: Date Comparison Failing
Date comparison `dI >= CurrentCycleStart and dI <= CurrentCycleEnd` might fail if:
- Dates have time components
- Date types don't match
- Year boundary issue

### Issue 3: Date Parsing Issue
`Incident_Date_Date` might not be parsed correctly from source.

**Check**: Verify `Incident_Date_Date` is type `Date`, not `Text`.

## Quick Test

In Power BI, create a measure to test the comparison:

```m
Test_Period = 
VAR IncidentDate = DATE(2026, 1, 4)  // 01/04/2026
VAR CycleStart = DATE(2025, 12, 30)  // 12/30/2025
VAR CycleEnd = DATE(2026, 1, 5)      // 01/05/2026
RETURN
    IF(
        IncidentDate >= CycleStart && IncidentDate <= CycleEnd,
        "7-Day",
        "NOT 7-Day"
    )
```

This should return "7-Day". If it doesn't, there's a date comparison issue.
