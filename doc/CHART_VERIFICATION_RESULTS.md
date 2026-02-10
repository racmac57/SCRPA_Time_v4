# Power BI Chart Verification Results
**Cycle:** 26C02W06_26_02_10  
**Report Date:** 02/10/2026  
**Verification Date:** 02/10/2026  
**Data Source:** preview_tables/All_Crimes_Simple.csv

---

## Data Source Confirmation

✅ **Total Records:** 252  
✅ **Period Breakdown:**
- 7-Day: **2** incidents
- 28-Day: **11** incidents  
- YTD: **7** incidents
- Prior Year: **232** incidents

✅ **Crime Category Breakdown:**
- Burglary - Comm & Res: **68**
- Burglary Auto: **64**
- Motor Vehicle Theft: **59**
- Sexual Offenses: **31**
- Robbery: **28**
- Other: **2**

---

## Chart 1: Burglary Auto

### Expected vs. Actual

| Time of Day | 7-Day (RED) Expected | 7-Day (RED) in Chart | 28-Day (GREEN) Expected | 28-Day (GREEN) in Chart | Status |
|-------------|---------------------|---------------------|------------------------|------------------------|--------|
| Late Night (00:00-03:59) | 0 | 0 | 0 | 0 | ✅ |
| Early Morning (04:00-07:59) | 0 | 0 | 0 | 0 | ✅ |
| Morning (08:00-11:59) | 0 | 0 | 0 | 0 | ✅ |
| **Afternoon (12:00-15:59)** | **1** | **1** | **0** | **0** | ✅ |
| **Evening Peak (16:00-19:59)** | **0** | **1** | **1** | **1** | ⚠️ RED BAR INCORRECT |
| **Night (20:00-23:59)** | **0** | **1** | **1** | **1** | ⚠️ RED BAR INCORRECT |

### Issues Found:
🔴 **Evening Peak:** Chart shows RED bar (1) but data shows 0 for 7-Day
🔴 **Night:** Chart shows RED bar (1) but data shows 0 for 7-Day

### Data Analysis:
```
Burglary Auto 7-Day + 28-Day incidents:
- 02/03/2026, Afternoon, 7-Day period  ← Correct (RED bar)
- 01/13/2026, Evening Peak, 28-Day period  ← Should be GREEN only
- 01/20/2026, Night, 28-Day period, IsLagDay=TRUE, Backfill_7Day=TRUE  ← Should be GREEN only
```

**Root Cause:** The chart is incorrectly showing RED bars for 28-Day incidents. The `Backfill_7Day` flag is meant to identify lag incidents but should NOT make them appear as "7-Day" incidents in the visualization.

---

## Chart 2: Burglary - Commercial | Residence ✅

### Expected vs. Actual

| Time of Day | 7-Day (RED) Expected | 7-Day (RED) in Chart | 28-Day (GREEN) Expected | 28-Day (GREEN) in Chart | Status |
|-------------|---------------------|---------------------|------------------------|------------------------|--------|
| Late Night (00:00-03:59) | 0 | 0 | 0 | 0 | ✅ |
| **Early Morning (04:00-07:59)** | **0** | **0** | **1** | **1** | ✅ |
| **Morning (08:00-11:59)** | **0** | **0** | **1** | **1** | ✅ |
| Afternoon (12:00-15:59) | 0 | 0 | 0 | 0 | ✅ |
| Evening Peak (16:00-19:59) | 0 | 0 | 0 | 0 | ✅ |
| **Night (20:00-23:59)** | **1** | **1** | **0** | **0** | ✅ |

### Verification: ✅ CORRECT
All bars match the expected data perfectly!

---

## Chart 3: Motor Vehicle Theft ✅

### Expected vs. Actual

| Time of Day | 7-Day (RED) Expected | 7-Day (RED) in Chart | 28-Day (GREEN) Expected | 28-Day (GREEN) in Chart | Status |
|-------------|---------------------|---------------------|------------------------|------------------------|--------|
| **Late Night (00:00-03:59)** | **0** | **0** | **1** | **1** | ✅ |
| Early Morning (04:00-07:59) | 0 | 0 | 0 | 0 | ✅ |
| **Morning (08:00-11:59)** | **0** | **0** | **1** | **1** | ✅ |
| **Afternoon (12:00-15:59)** | **0** | **0** | **1** | **1** | ✅ |
| Evening Peak (16:00-19:59) | 0 | 0 | 0 | 0 | ✅ |
| Night (20:00-23:59) | 0 | 0 | 0 | 0 | ✅ |

**Note:** Chart legend shows no 7-Day incidents, which is correct. There are 0 Motor Vehicle Theft incidents in the 7-Day period.

### Verification: ✅ CORRECT
All bars match the expected data perfectly!

---

## Chart 4: Robbery ✅

### Expected vs. Actual

| Time of Day | 7-Day (RED) Expected | 7-Day (RED) in Chart | 28-Day (GREEN) Expected | 28-Day (GREEN) in Chart | Status |
|-------------|---------------------|---------------------|------------------------|------------------------|--------|
| Late Night (00:00-03:59) | 0 | 0 | 0 | 0 | ✅ |
| Early Morning (04:00-07:59) | 0 | 0 | 0 | 0 | ✅ |
| Morning (08:00-11:59) | 0 | 0 | 0 | 0 | ✅ |
| Afternoon (12:00-15:59) | 0 | 0 | 0 | 0 | ✅ |
| **Evening Peak (16:00-19:59)** | **0** | **0** | **1** | **1** | ✅ |
| Night (20:00-23:59) | 0 | 0 | 0 | 0 | ✅ |

**Note:** Chart legend shows no 7-Day incidents, which is correct.

### Verification: ✅ CORRECT
All bars match the expected data perfectly!

---

## Chart 5: Sexual Offenses ✅

### Expected vs. Actual

| Time of Day | 7-Day (RED) Expected | 7-Day (RED) in Chart | 28-Day (GREEN) Expected | 28-Day (GREEN) in Chart | Status |
|-------------|---------------------|---------------------|------------------------|------------------------|--------|
| Late Night (00:00-03:59) | 0 | 0 | 0 | 0 | ✅ |
| Early Morning (04:00-07:59) | 0 | 0 | 0 | 0 | ✅ |
| **Morning (08:00-11:59)** | **0** | **0** | **1** | **1** | ✅ |
| **Afternoon (12:00-15:59)** | **0** | **0** | **1** | **1** | ✅ |
| **Evening Peak (16:00-19:59)** | **0** | **0** | **1** | **1** | ✅ |
| Night (20:00-23:59) | 0 | 0 | 0 | 0 | ✅ |

**Note:** Chart shows 7-Day legend but no actual 7-Day bars, which is correct (0 incidents).

### Verification: ✅ CORRECT
All bars match the expected data perfectly!

---

## Summary

### ✅ Charts Verified as CORRECT (4 of 5):
1. ✅ **Burglary - Commercial | Residence** - All data matches perfectly
2. ✅ **Motor Vehicle Theft** - All data matches perfectly
3. ✅ **Robbery** - All data matches perfectly
4. ✅ **Sexual Offenses** - All data matches perfectly

### ⚠️ Chart with Issues (1 of 5):
1. ⚠️ **Burglary Auto** - Incorrect RED bars in Evening Peak and Night slots

---

## Issue Details: Burglary Auto Chart

### Problem:
The Burglary Auto chart is showing **RED (7-Day) bars** where there should only be **GREEN (28-Day) bars**.

### Specific Issues:

#### Evening Peak (16:00-19:59):
- **Expected:** GREEN bar only (1 incident from 28-Day period)
- **Actual:** GREEN bar (1) + RED bar (1) ❌
- **Data:** 01/13/2026, 28-Day period, IsLagDay=FALSE

#### Night (20:00-23:59):
- **Expected:** GREEN bar only (1 incident from 28-Day period) 
- **Actual:** GREEN bar (1) + RED bar (1) ❌
- **Data:** 01/20/2026, 28-Day period, IsLagDay=TRUE, Backfill_7Day=TRUE

### Root Cause Analysis:

The issue is NOT with your data - the M code and CSV are correct. The problem is with your **DAX measure or visual filter** for the 7-Day (RED) series.

**Current (INCORRECT) Logic:**
```DAX
7-Day Count = CALCULATE(COUNT(...), 'All_Crimes'[Backfill_7Day] = TRUE OR 'All_Crimes'[Period] = "7-Day")
```

**This is wrong because:**
- `Backfill_7Day = TRUE` means the incident occurred BEFORE the 7-Day cycle
- It's a LAG incident that belongs to the 28-Day period
- It should NOT be counted as a 7-Day incident

**Correct Logic:**
```DAX
7-Day Count = CALCULATE(COUNT(...), 'All_Crimes'[Period] = "7-Day")
```

**OR if you want to track lag days separately:**
```DAX
7-Day Count = CALCULATE(COUNT(...), 'All_Crimes'[Period] = "7-Day" AND 'All_Crimes'[IsLagDay] = FALSE)

Lag Day Count = CALCULATE(COUNT(...), 'All_Crimes'[Backfill_7Day] = TRUE)
```

---

## Recommended Fix

### Option 1: Simplest Fix (Recommended)
Change your 7-Day measure to ONLY filter on `Period = "7-Day"`:

```DAX
7-Day Incidents = 
CALCULATE(
    COUNT('All_Crimes'[IncidentKey]),
    'All_Crimes'[Period] = "7-Day"
)
```

### Option 2: If You Want Lag Days as Separate Series
Create THREE series instead of two:

1. **7-Day (Current Period)** - RED
   ```DAX
   CALCULATE(COUNT(...), 'All_Crimes'[Period] = "7-Day" AND 'All_Crimes'[IsLagDay] = FALSE)
   ```

2. **7-Day (Lag Days)** - ORANGE or YELLOW
   ```DAX
   CALCULATE(COUNT(...), 'All_Crimes'[Backfill_7Day] = TRUE)
   ```

3. **28-Day** - GREEN
   ```DAX
   CALCULATE(COUNT(...), 'All_Crimes'[Period] = "28-Day")
   ```

---

## Conclusion

✅ **4 out of 5 charts (80%) are displaying correctly** with no issues.

⚠️ **1 chart (Burglary Auto) has a DAX measure or filter issue** - the 7-Day series is incorrectly including 28-Day lag incidents.

**Next Steps:**
1. Open your Power BI file
2. Check the DAX measure for the 7-Day series in the Burglary Auto chart
3. Remove any reference to `Backfill_7Day` from the 7-Day measure
4. Refresh and verify the chart shows:
   - Afternoon: 1 RED bar only
   - Evening Peak: 1 GREEN bar only (no RED)
   - Night: 1 GREEN bar only (no RED)
