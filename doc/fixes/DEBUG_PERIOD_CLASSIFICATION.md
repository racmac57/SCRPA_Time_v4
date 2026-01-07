# Debugging Period Classification Issues

## Current Situation

**Two incidents reported:**
1. **Burglary - Auto**: Lag day of 1 → Should appear in lagday table
2. **Burglary - Residence**: Should show in 7-Day period → Should appear in 7-Day charts

## Current Cycle (26C01W01)

Based on the cycle calendar:
- **7-Day window**: 12/30/25 - 1/05/26
- **28-Day window**: 12/09/25 - 1/05/26

## How Period Classification Works

### Period = "7-Day"
**Condition**: `Incident_Date` falls within current 7-day cycle boundaries
- `Incident_Date >= 12/30/25 AND Incident_Date <= 1/05/26`

### Period = "28-Day"  
**Condition**: `Incident_Date` falls within current 28-day cycle boundaries (but not 7-Day)
- `Incident_Date >= 12/09/25 AND Incident_Date <= 1/05/26`
- AND `Incident_Date` is NOT in 7-Day window

### Backfill_7Day = True
**Condition**: 
- `Incident_Date < CurrentCycleStart` (before 12/30/25)
- AND `Report_Date >= CurrentCycleStart` (reported during cycle: 12/30/25 - 1/05/26)

### IsLagDay = True
**Condition**:
- Find the cycle where `Report_Date` falls
- `Incident_Date < CycleStartForReport` (incident occurred before the cycle where it was reported)

## Debugging Steps

### Step 1: Check the Data

In Power BI, create a table showing both incidents with these columns:
- Case Number
- Incident Date
- Report Date
- Period
- Backfill_7Day
- IsLagDay
- LagDays
- Crime Category

### Step 2: Verify Dates

**For Burglary - Residence (should be 7-Day):**
- What is the `Incident_Date`?
- If `Incident_Date` is between 12/30/25 and 1/05/26 → Should be Period = "7-Day"
- If `Incident_Date` is outside this range → Will NOT be "7-Day"

**For Burglary - Auto (lag day 1):**
- What is the `Incident_Date`?
- What is the `Report_Date`?
- If `Incident_Date < 12/30/25` AND `Report_Date` is between 12/30/25-1/05/26 → Backfill_7Day = True
- If `Report_Date` falls in a cycle AND `Incident_Date < CycleStart` → IsLagDay = True

### Step 3: Check Current Cycle Detection

The M code uses `Today` to find the current cycle. Verify:
- What is "Today" when the query runs?
- Is it finding cycle 26C01W01 correctly?

**Current Cycle Logic:**
```m
// First tries: Today within a cycle
InCycle = Today >= 7_Day_Start AND Today <= 7_Day_End

// If not, finds most recent completed cycle
MostRecent = Cycle where 7_Day_End <= Today (sorted descending)
```

### Step 4: Common Issues

**Issue 1: Incident_Date is null**
- If `Incident_Date` is null → Period = "Historical"
- Check if dates are being parsed correctly

**Issue 2: Date format mismatch**
- Ensure dates are actual date type, not text
- Check `Incident_Date_Date` column (the parsed version)

**Issue 3: Cycle not found**
- If `HasCurrentCycle = false`, Period will default to YTD or Historical
- Verify cycle calendar has entry for 26C01W01

**Issue 4: Time component causing issues**
- Dates should be date-only (no time)
- Check if `Date.From()` is being applied correctly

## Quick Diagnostic Query

Add this to Power BI to see what's happening:

```m
// Diagnostic table
Diagnostic = Table.SelectColumns(
    All_Crimes,
    {
        "Case Number",
        "Incident_Date_Date",
        "Report_Date",
        "Period",
        "Backfill_7Day",
        "IsLagDay",
        "LagDays",
        "Crime_Category"
    }
)
```

Filter to your two cases and check:
1. Are the dates correct?
2. What Period is assigned?
3. What are Backfill_7Day and IsLagDay values?

## Expected Results

**Burglary - Residence (should be 7-Day):**
- `Incident_Date` = between 12/30/25 - 1/05/26
- `Period` = "7-Day"
- `Backfill_7Day` = False (unless incident was before cycle)
- Should appear in 7-Day charts

**Burglary - Auto (lag day 1):**
- `Incident_Date` = before 12/30/25 (or before cycle where reported)
- `Report_Date` = between 12/30/25 - 1/05/26
- `Period` = "Prior Year" or "Historical" (depending on incident date)
- `Backfill_7Day` = True (if incident before cycle start)
- `IsLagDay` = True
- `LagDays` = 1
- Should appear in lagday table

## Next Steps

1. Export the data to CSV and check the actual dates
2. Verify the cycle calendar has the correct entry
3. Check if dates are being parsed correctly
4. Verify "Today" is being calculated correctly in Power BI
