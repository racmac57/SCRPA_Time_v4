# Period Calculation Issue - Analysis

## Problem
Period column is not calculating correctly. Case 26-001094 (Incident Date 01/04/2026) should show as "7-Day" but may not be.

## Current Cycle (26C01W01)
- **7-Day Window**: 12/30/25 - 1/05/26
- **28-Day Window**: 12/09/25 - 1/05/26

## Expected Results

### Case 26-001094 (Burglary - Residence)
- **Incident Date**: 01/04/2026
- **Should be**: Period = "7-Day" (01/04/26 is between 12/30/25 and 1/05/26)

### Case 25-113412 (Burglary - Auto)
- **Incident Date**: 12/29/2025
- **Should be**: Period = "Prior Year" (12/29/25 is before cycle start 12/30/25)

## Potential Issues

### Issue 1: Date Type Mismatch
The `Incident_Date_Date` column might not be a proper date type, causing comparison failures.

**Check**: In Power BI, verify `Incident_Date_Date` is type `Date`, not `Text`.

### Issue 2: Year Boundary Problem
The cycle spans 2025-2026. Date comparisons might fail if dates are stored incorrectly.

**Check**: Verify dates are:
- 12/30/2025 (not 12/30/2026)
- 01/04/2026 (not 01/04/2025)

### Issue 3: Current Cycle Detection
If `HasCurrentCycle = false`, the Period will default to YTD or Historical.

**Check**: Verify the cycle calendar has entry for 26C01W01 with dates:
- 7_Day_Start: 12/30/2025
- 7_Day_End: 1/05/2026

### Issue 4: Date Comparison Logic
The comparison `dI >= CurrentCycleStart and dI <= CurrentCycleEnd` might fail if:
- Dates have time components (should be date-only)
- Dates are in different formats
- Year is being compared incorrectly

## Debugging Steps

### Step 1: Verify Current Cycle Detection

Add a diagnostic column to see what cycle is being detected:

```m
// Add after CurrentCycleName
Diagnostic_CurrentCycle = Table.AddColumn(
    Period_Added,
    "_Debug_CurrentCycle",
    each 
        if HasCurrentCycle then
            Text.From(CurrentCycleStart) & " to " & Text.From(CurrentCycleEnd)
        else "NO CYCLE FOUND",
    type text
)
```

### Step 2: Verify Date Values

Check the actual date values being compared:

```m
Diagnostic_Dates = Table.AddColumn(
    Period_Added,
    "_Debug_Dates",
    each 
        let
            dI = [Incident_Date_Date],
            dIYear = if dI = null then null else Date.Year(dI),
            dIDay = if dI = null then null else Date.Day(dI),
            dIMonth = if dI = null then null else Date.Month(dI)
        in
            if dI = null then "NULL"
            else Text.From(dIYear) & "/" & Text.From(dIMonth) & "/" & Text.From(dIDay),
    type text
)
```

### Step 3: Verify Period Logic

Add diagnostic to see why Period is assigned:

```m
Diagnostic_Period = Table.AddColumn(
    Period_Added,
    "_Debug_Period",
    each
        let 
            dI = [Incident_Date_Date],
            incidentYear = if dI = null then null else Date.Year(dI),
            currentYear = Date.Year(Today),
            in7Day = HasCurrentCycle and dI >= CurrentCycleStart and dI <= CurrentCycleEnd,
            in28Day = HasCurrentCycle and CurrentCycle28DayStart <> null and CurrentCycle28DayEnd <> null and dI >= CurrentCycle28DayStart and dI <= CurrentCycle28DayEnd
        in
            "dI=" & (if dI = null then "NULL" else Text.From(dI)) 
            & " | HasCycle=" & Text.From(HasCurrentCycle)
            & " | in7Day=" & Text.From(in7Day)
            & " | in28Day=" & Text.From(in28Day)
            & " | Year=" & (if incidentYear = null then "NULL" else Text.From(incidentYear)),
    type text
)
```

## Most Likely Issue

**Date parsing or type issue**: The `Incident_Date_Date` column might not be correctly parsed from the source data, or the dates might be stored as text instead of date type.

**Solution**: Verify in Power BI that:
1. `Incident_Date_Date` is type `Date`
2. The dates are correct (01/04/2026, not 01/04/2025)
3. The cycle calendar dates are correct (12/30/2025, not 12/30/2024)

## Quick Fix to Test

If dates are the issue, you can add explicit date conversion in the Period calculation:

```m
// In Period_Added, ensure dI is a date:
dI = if [Incident_Date_Date] is date then [Incident_Date_Date] 
     else if [Incident_Date_Date] is text then Date.FromText([Incident_Date_Date])
     else null
```
