# Incident Classification Analysis

## Case Data

### Case 25-113412 (Burglary - Auto)
- **Incident Date**: 12/29/2025
- **Report Date**: 12/30/2025
- **Lag Days**: 1 day (12/30/25 - 12/29/25)

### Case 26-001094 (Burglary - Residence)
- **Incident Date**: 01/04/2026
- **Report Date**: 01/04/2026
- **Lag Days**: 0 days (same day)

## Current Cycle (26C01W01)
- **7-Day Window**: 12/30/25 - 1/05/26
- **28-Day Window**: 12/09/25 - 1/05/26

## Expected Classification

### Case 25-113412 (Burglary - Auto)

**Period Classification:**
- Incident Date (12/29/25) is **BEFORE** cycle start (12/30/25)
- Therefore: `Period` = **"Prior Year"** (not "7-Day")
- ✅ Correct - incident occurred in 2025, outside current cycle

**Backfill_7Day:**
- Incident Date (12/29/25) < Cycle Start (12/30/25) ✅
- Report Date (12/30/25) >= Cycle Start (12/30/25) ✅
- Report Date (12/30/25) <= Cycle End (1/05/26) ✅
- Therefore: `Backfill_7Day` = **True** ✅
- ✅ Should appear in lagday table

**LagDays:**
- Report Date cycle: 12/30/25 - 1/05/26
- Cycle Start for Report: 12/30/25
- Incident Date: 12/29/25
- LagDays = 12/30/25 - 12/29/25 = **1 day** ✅
- ✅ Correct

### Case 26-001094 (Burglary - Residence)

**Period Classification:**
- Incident Date (01/04/26) is **WITHIN** 7-Day window (12/30/25 - 1/05/26) ✅
- Therefore: `Period` = **"7-Day"** ✅
- ✅ Should appear in 7-Day charts

**Backfill_7Day:**
- Incident Date (01/04/26) is NOT < Cycle Start (12/30/25)
- Incident Date (01/04/26) >= Cycle Start ✅
- Therefore: `Backfill_7Day` = **False** ✅
- ✅ Should NOT appear in lagday table

**LagDays:**
- Incident Date (01/04/26) = Report Date (01/04/26)
- Incident Date is within cycle where reported
- Therefore: `IsLagDay` = **False**
- `LagDays` = **0** ✅
- ✅ Correct - no lag

## Verification Checklist

### In Power BI, check these values:

**Case 25-113412:**
- [ ] `Period` = "Prior Year" (not "7-Day")
- [ ] `Backfill_7Day` = True
- [ ] `IsLagDay` = True
- [ ] `LagDays` = 1
- [ ] Appears in lagday table ✅

**Case 26-001094:**
- [ ] `Period` = "7-Day" ✅
- [ ] `Backfill_7Day` = False
- [ ] `IsLagDay` = False
- [ ] `LagDays` = 0
- [ ] Appears in 7-Day charts ✅
- [ ] Does NOT appear in lagday table ✅

## If Case 26-001094 is NOT showing as "7-Day"

**Possible Issues:**

1. **Date Parsing Problem**
   - Check if `Incident_Date_Date` is correctly parsed as 01/04/2026
   - Verify it's a date type, not text

2. **Current Cycle Detection**
   - Verify `HasCurrentCycle` = True
   - Verify `CurrentCycleStart` = 12/30/25
   - Verify `CurrentCycleEnd` = 1/05/26

3. **Date Comparison**
   - The logic checks: `dI >= CurrentCycleStart and dI <= CurrentCycleEnd`
   - For 01/04/26: `01/04/26 >= 12/30/25` = True ✅
   - For 01/04/26: `01/04/26 <= 1/05/26` = True ✅
   - Should match "7-Day" condition

4. **Year Boundary Issue**
   - Check if there's a year comparison issue (2025 vs 2026)
   - The dates span year boundary (12/30/25 to 1/05/26)

## Debug Steps

1. **Create diagnostic table** in Power BI with:
   - Case Number
   - Incident_Date_Date
   - Report_Date
   - Period
   - Backfill_7Day
   - IsLagDay
   - LagDays
   - CurrentCycleStart (if available)
   - CurrentCycleEnd (if available)

2. **Filter to these two cases** and verify all values

3. **Check date types** - ensure dates are date type, not text

4. **Verify cycle calendar** - ensure 26C01W01 exists with correct dates
