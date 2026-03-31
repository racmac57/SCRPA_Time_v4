# LagDays vs IncidentToReportDays Fix - 2026-02-10

## Issue

**Critical Bug:** Crime category breakdown and lag statistics were using the wrong "lag" field, resulting in always-zero lag counts for 7-Day period incidents.

## Root Cause

The system has **two different "lag" concepts** that were being confused:

### 1. `LagDays` (Cycle-Based Backfill Metric)

**Formula:** `LagDays = CycleStart_7Day - Incident_Date`

**Purpose:** Identifies incidents that occurred BEFORE the cycle start but were reported DURING the cycle (backfill incidents).

**Behavior:**
- **Positive** when `Incident_Date < CycleStart_7Day` (backfill)
- **Zero or negative** when `Incident_Date >= CycleStart_7Day` (current cycle incidents)

**Example:**
```
Cycle: 02/03/2026 - 02/09/2026
Incident: 02/05/2026
Report: 02/08/2026

LagDays = 02/03 - 02/05 = -2 days (negative because incident is AFTER cycle start)
```

**Used for:**
- `IsLagDay` flag (True when LagDays > 0)
- `Backfill_7Day` identification
- NOT for reporting delay statistics

### 2. `IncidentToReportDays` (Reporting Delay Metric)

**Formula:** `IncidentToReportDays = Report_Date - Incident_Date`

**Purpose:** Measures the actual delay between when an incident occurred and when it was reported to RMS.

**Behavior:**
- **Always positive** when report date is after incident date
- Measures reporting performance/delay
- Applies to ANY period (7-Day, 28-Day, YTD, etc.)

**Example:**
```
Cycle: 02/03/2026 - 02/09/2026
Incident: 02/05/2026
Report: 02/08/2026

IncidentToReportDays = 02/08 - 02/05 = 3 days
```

**Used for:**
- Crime category lag counts
- Lag statistics (mean, median, max)
- Reporting delay analysis

## The Bug

In `scripts/prepare_7day_outputs.py`, the code was using `LagDays` to count reporting delays:

```python
# WRONG - Line 163 (old)
lag_count = int((grp['LagDays'] > 0).sum())

# WRONG - Line 184-185 (old)
lag_values = df_7day_period_only['LagDays'].dropna()
lag_values = lag_values[lag_values > 0]
```

**Why this is wrong:**

For incidents with `Period='7-Day'`:
1. Incident date is WITHIN the 7-day cycle window
2. By definition: `Incident_Date >= CycleStart_7Day`
3. Therefore: `LagDays = CycleStart - Incident_Date ≤ 0`
4. Condition `LagDays > 0` is ALWAYS FALSE
5. Result: **Lag count is always 0**, even when incidents had significant reporting delays

**Example of the broken logic:**

```
Case: 26-012829
Incident: 02/03/2026
Report: 02/08/2026
Period: 7-Day
CycleStart: 02/03/2026

OLD LOGIC:
  LagDays = 02/03 - 02/03 = 0
  LagDays > 0? FALSE
  Counted as lag? NO ❌

REALITY:
  Reporting delay = 02/08 - 02/03 = 5 days
  Should count as lag? YES ✅
```

## The Fix

Changed to use `IncidentToReportDays` for all reporting delay calculations:

### 1. Crime Category Breakdown (Lines 153-177)

```python
# NEW - Correct field for reporting delay
has_reporting_lag = 'IncidentToReportDays' in df_7day_period_only.columns
lag_count = int((grp['IncidentToReportDays'] > 0).sum()) if has_reporting_lag else 0
```

### 2. Lag Statistics (Lines 179-199)

```python
# NEW - Use reporting delay field
if 'Period' in df_7day.columns and 'IncidentToReportDays' in df_7day.columns and len(df_7day) > 0:
    df_7day_period_only = df_7day[df_7day['Period'] == '7-Day'].copy()
    if len(df_7day_period_only) > 0:
        # Use IncidentToReportDays for reporting delay
        lag_values = df_7day_period_only['IncidentToReportDays'].dropna()
        lag_values = lag_values[lag_values > 0]
```

## Impact

### Before Fix
- **Crime category lag counts:** Always 0 for 7-Day incidents
- **Lag statistics:** Empty (no data)
- **Reporting analysis:** Impossible

### After Fix
- **Crime category lag counts:** Correctly shows incidents with reporting delays
- **Lag statistics:** Accurate mean, median, max, and range distribution
- **Reporting analysis:** Enables detection of reporting delays

## Example Output Comparison

### Cycle 26C02W06 (02/03-02/09):

**Before Fix:**
```json
{
  "by_crime_category": [
    {"Crime_Category": "Burglary - Auto", "LagDayCount": 0, "TotalCount": 2}
  ],
  "lagdays_distribution": {}  // Empty - no data
}
```

**After Fix:**
```json
{
  "by_crime_category": [
    {"Crime_Category": "Burglary - Auto", "LagDayCount": 2, "TotalCount": 2}
  ],
  "lagdays_distribution": {
    "min": 1,
    "max": 5,
    "mean": 3.0,
    "median": 3,
    "ranges": {
      "1-7_days": 2,
      "8-14_days": 0
    }
  }
}
```

## Files Changed

- `scripts/prepare_7day_outputs.py` (Lines 153-199)

## Related Documentation

- `SCRPA_7Day_Summary.json` - Now contains accurate lag statistics
- `SCRPA_Report_Summary.md` - Lag statistics now populated correctly

## Validation

To verify the fix works correctly:

1. Run the pipeline: `scripts\Run_SCRPA_Pipeline.bat`
2. Check `SCRPA_7Day_Summary.json` for non-zero lag counts
3. Verify lag statistics match actual reporting delays in the CSV

## Breaking Changes

None - this is a bug fix that corrects incorrect output. The output format remains the same.

---

**Date:** 2026-02-10  
**Author:** R. A. Carucci (via Claude)  
**Impact:** Critical - Fixes always-zero lag counts and empty lag statistics
