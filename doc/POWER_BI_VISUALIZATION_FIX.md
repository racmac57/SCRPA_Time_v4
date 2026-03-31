# Power BI Visualization Fix for Cycle 26C02W06_26_02_10

**Date:** 2026-02-10  
**Issue:** Burglary Auto chart not showing lag day (backfill) incident correctly

---

## Issue Summary

The Burglary Auto chart is showing 28-Day (gray) data but missing the 7-Day backfill incident that should appear as a green bar in the Night time slot.

---

## Data Analysis

### Current Cycle: 26C02W06
- **7-Day Period:** 02/03/2026 - 02/09/2026
- **28-Day Period:** 01/13/2026 - 02/09/2026
- **Report Date:** 02/10/2026

### Burglary Auto Incidents

#### 7-Day Period (Green Bars)
| Incident Date | Time of Day | Period | IsLagDay | Backfill_7Day | LagDays |
|---------------|-------------|--------|----------|---------------|---------|
| 02/03/2026 | Afternoon (12:00-15:59) | 7-Day | FALSE | FALSE | 0 |

#### 28-Day Period with Backfill (Should show as Green in "7-Day" context)
| Incident Date | Time of Day | Period | IsLagDay | Backfill_7Day | LagDays |
|---------------|-------------|--------|----------|---------------|---------|
| 01/20/2026 | Night (20:00-23:59) | 28-Day | **TRUE** | **TRUE** | 14 |

#### 28-Day Period (Gray Bars)
| Incident Date | Time of Day | Period | IsLagDay | Backfill_7Day |
|---------------|-------------|--------|----------|---------------|
| 01/13/2026 | Evening Peak (16:00-19:59) | 28-Day | FALSE | FALSE |

---

## Expected Chart Display

### For "7-Day" View (Green Bars):
Should filter on: `Backfill_7Day = TRUE` OR `Period = "7-Day"`

- **Afternoon (12:00-15:59)**: **1** incident (02/03/2026)
- **Night (20:00-23:59)**: **1** incident (01/20/2026 - the lag day backfill)

### For "28-Day" View (Gray Bars):
Should filter on: `Period = "28-Day"`

- **Evening Peak (16:00-19:59)**: **1** incident (01/13/2026)
- **Night (20:00-23:59)**: **1** incident (01/20/2026)

---

## Power BI Fix Instructions

### Step 1: Update M Code File Path

The M code in your Power BI file is pointing to the **wrong cycle folder**.

**Current (WRONG):**
```
FilePath = "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C01W04_26_01_28\Data\SCRPA_All_Crimes_Enhanced.csv"
```

**Corrected (RIGHT):**
```
FilePath = "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C02W06_26_02_10\Data\SCRPA_All_Crimes_Enhanced.csv"
```

**How to Update:**
1. Open your Power BI file: `26C02W06_26_02_10.pbix`
2. Go to **Home** > **Transform Data** > **Power Query Editor**
3. Find the `All_Crimes` query (or `All_Crimes_Simple`)
4. Click on **Advanced Editor**
5. Change line 36 to the corrected path above
6. Click **Done** > **Close & Apply**

### Step 2: Check Visual Filters

Your chart should have TWO series/measures:

#### Measure 1: 7-Day Count (Green Bars)
Should use this filter logic:
```DAX
7-Day Count = 
CALCULATE(
    COUNT('All_Crimes'[IncidentKey]),
    OR(
        'All_Crimes'[Period] = "7-Day",
        'All_Crimes'[Backfill_7Day] = TRUE
    )
)
```

OR use a simple filter:
- Filter: `Backfill_7Day = TRUE` OR `Period = "7-Day"`

#### Measure 2: 28-Day Count (Gray Bars)
```DAX
28-Day Count = 
CALCULATE(
    COUNT('All_Crimes'[IncidentKey]),
    'All_Crimes'[Period] = "28-Day"
)
```

### Step 3: Verify Data Load

After updating the path:
1. Click **Refresh** in Power BI
2. Check the data loaded correctly:
   - Total records should be **252** (see SCRPA_7Day_Summary.yaml)
   - Period breakdown:
     - 7-Day: **2** 
     - 28-Day: **11**
     - YTD: **7**
     - Prior Year: **232**

---

## Alternative: Use SCRPA_7Day_With_LagFlags.csv

If you want a simpler approach, use the pre-filtered 7-Day CSV instead:

**File:** `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Time_Based\2026\26C02W06_26_02_10\Data\SCRPA_7Day_With_LagFlags.csv`

This CSV contains only the 3 incidents relevant to the 7-Day window:
- 2 incidents with `Period = "7-Day"`
- 1 incident with `Backfill_7Day = TRUE` (the lag day incident)

---

## Verification

After fixing, you should see:

**Burglary Auto - 7-Day Period (Green Bars):**
- Afternoon: **1** 
- Night: **1** ← This should now appear!

**Burglary Auto - 28-Day Period (Gray Bars):**
- Evening Peak: **1**
- Night: **1**

The lag incident (01/20) appears in BOTH views because:
- It's in the 28-Day period (gray bar)
- It's a backfill for the 7-Day window (green bar)

---

## Questions?

If the chart still doesn't look right after these fixes, check:
1. Is the correct PBIX file open? (`26C02W06_26_02_10.pbix`)
2. Did the data refresh successfully? (Check record count = 252)
3. Are you filtering by Crime_Category = "Burglary Auto"?
4. Is the Period slicer set correctly?
