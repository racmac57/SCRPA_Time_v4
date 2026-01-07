# Verify Incident Classification - Quick Guide

## Current Cycle (26C01W01)
- **7-Day Window**: 12/30/25 - 1/05/26
- **28-Day Window**: 12/09/25 - 1/05/26

## What to Check in Power BI

### Step 1: Create Diagnostic Table

In Power BI, create a new table visual with these columns:
- Case Number
- Incident_Date_Date (the parsed date column)
- Report_Date
- Period
- Backfill_7Day
- IsLagDay
- LagDays
- Crime_Category

### Step 2: Filter to Your Two Cases

Filter the table to show only:
- Burglary - Auto
- Burglary - Residence

### Step 3: Check the Values

**For Burglary - Residence (should be 7-Day):**

Check these values:
- `Incident_Date_Date` = **Must be between 12/30/25 and 1/05/26** for Period = "7-Day"
- `Period` = Should be "7-Day" if incident date is in range
- If `Period` is NOT "7-Day", check:
  - Is `Incident_Date_Date` null?
  - Is `Incident_Date_Date` outside the 7-Day window?
  - Is the date being parsed correctly?

**For Burglary - Auto (lag day 1):**

Check these values:
- `Incident_Date_Date` = Should be before 12/30/25 (or before cycle where reported)
- `Report_Date` = Should be between 12/30/25 - 1/05/26
- `Backfill_7Day` = Should be True
- `IsLagDay` = Should be True
- `LagDays` = Should be 1
- `Period` = Will be "Prior Year" or "Historical" (not "7-Day")

## Common Issues

### Issue 1: Incident_Date is Outside 7-Day Window

**Symptom**: Burglary - Residence shows Period = "28-Day" or "Prior Year" instead of "7-Day"

**Cause**: The `Incident_Date` is not between 12/30/25 and 1/05/26

**Solution**: 
- Check the actual incident date in the source data
- If the incident occurred on 1/06/26 or later, it won't be "7-Day" (cycle ended 1/05/26)
- If the incident occurred before 12/30/25, it will be "Prior Year" or "Historical"

### Issue 2: Date Not Parsed Correctly

**Symptom**: `Incident_Date_Date` is null or wrong

**Check**: 
- Look at the original `Incident Date` column (text)
- Compare to `Incident_Date_Date` (parsed)
- Verify the date parsing logic is working

### Issue 3: Current Cycle Not Detected

**Symptom**: All incidents show wrong Period

**Check**:
- What is "Today" in Power BI? (should be 1/06/26 or later)
- Is the cycle calendar loading correctly?
- Does cycle 26C01W01 exist in the calendar?

## Expected Results

### Burglary - Residence (if occurred 12/30/25 - 1/05/26)
```
Incident_Date_Date: 1/03/26 (example)
Report_Date: 1/06/26 (example)
Period: "7-Day" ✅
Backfill_7Day: False
IsLagDay: False
LagDays: 0
```

### Burglary - Auto (lag day 1)
```
Incident_Date_Date: 12/29/25 (example - before cycle)
Report_Date: 1/06/26 (example - during cycle)
Period: "Prior Year" or "Historical"
Backfill_7Day: True ✅
IsLagDay: True ✅
LagDays: 1 ✅
```

## Quick Fix: Check Incident Dates

The most likely issue is that the **Burglary - Residence incident date is outside the 7-Day window**.

**If the incident occurred on 1/06/26 or later:**
- It will NOT be "7-Day" (cycle ended 1/05/26)
- It will be "YTD" (if 2026) or next cycle's "7-Day"

**If the incident occurred before 12/30/25:**
- It will be "Prior Year" or "Historical"
- It might be a backfill case if reported during the cycle

## Action Items

1. ✅ Check the actual `Incident_Date_Date` for Burglary - Residence
2. ✅ Verify it's between 12/30/25 and 1/05/26
3. ✅ If not, that's why it's not showing as "7-Day"
4. ✅ Verify Burglary - Auto has correct lag day calculation
