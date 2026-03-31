# SCRPA_7Day_Summary.json Validation Report
## Cycle 26C02W06_26_02_10 | Generated: 2026-02-10

---

## Executive Summary

The `SCRPA_7Day_Summary.json` file was validated against the source CSV (`SCRPA_All_Crimes_Enhanced.csv`) and **THREE ERRORS** were found:

| Field | Status | Severity |
|-------|--------|----------|
| Total counts | ✅ CORRECT | - |
| 7-Day period incidents | ✅ CORRECT | - |
| **Lag incidents count** | ❌ **INCORRECT** | **HIGH** |
| **Lag analysis by category** | ❌ **INCOMPLETE** | **HIGH** |
| Backfill_7Day | ✅ CORRECT | - |
| Total 7-Day window | ✅ CORRECT | - |
| Lag days distribution | ✅ CORRECT | - |
| 7-Day by crime category | ✅ CORRECT | - |
| Period breakdown | ⚠️ PARTIAL | Low |
| **Incident date range** | ❌ **MISLEADING** | **MEDIUM** |

---

## Error #1: Lag Incidents Count

### The Problem

**JSON says:** `"lag_incidents": 1`

**CSV shows:** `2` incidents in 7-Day period have reporting lag (`IncidentToReportDays > 0`)

### The Data

Both 7-Day period incidents have reporting lag:

| Incident | Crime Category | Incident Date | Report Date | Lag Days |
|----------|----------------|---------------|-------------|----------|
| 26-012829 | Burglary Auto | 02/03/2026 | 02/08/2026 | **5 days** |
| 26-012181 | Burglary - Comm & Res | 02/05/2026 | 02/06/2026 | **1 day** |

### Root Cause

**File:** `scripts/prepare_7day_outputs.py`, Line 224

```python
'lag_incidents': len(df_lag_only),  # ❌ WRONG
```

**Problem:** This counts `df_lag_only`, which contains **backfill incidents** (`Backfill_7Day=True`), NOT incidents with reporting lag.

**What it's counting:**
- `Backfill_7Day=True` — incidents that occurred **before the cycle** but were reported **during the cycle**
- These are "cycle-based lag" incidents (1 in this cycle: Burglary Auto from 01/20/2026)

**What it should count:**
- Incidents with `IncidentToReportDays > 0` in the 7-Day period
- These are "reporting delay lag" incidents (2 in this cycle)

### The Fix

```python
# OLD (Line 224):
'lag_incidents': len(df_lag_only),

# NEW (should be):
'lag_incidents': len(df_7day_period_only[df_7day_period_only['IncidentToReportDays'] > 0]) if 'IncidentToReportDays' in df_7day_period_only.columns else 0,
```

---

## Error #2: Lag Analysis By Crime Category

### The Problem

**JSON says:**
```json
"by_crime_category": {
  "Burglary Auto": 1
}
```

**CSV shows:**
```
Burglary Auto: 1 lag incident
Burglary - Comm & Res: 1 lag incident
```

The JSON is **missing** `"Burglary - Comm & Res": 1`.

### Root Cause

**File:** `scripts/prepare_7day_outputs.py`, Lines 148-150

```python
lag_by_category = {}
if 'Crime_Category' in df_lag_only.columns and len(df_lag_only) > 0:
    lag_by_category = df_lag_only['Crime_Category'].value_counts().to_dict()
```

**Problem:** Same as Error #1 — uses `df_lag_only` (backfill incidents) instead of actual reporting lag incidents.

The `df_lag_only` DataFrame contains only 1 incident:
- Burglary Auto from 01/20/2026 (backfill)

It doesn't contain the 7-Day period incidents with reporting lag.

### The Fix

```python
# OLD (Lines 148-150):
lag_by_category = {}
if 'Crime_Category' in df_lag_only.columns and len(df_lag_only) > 0:
    lag_by_category = df_lag_only['Crime_Category'].value_counts().to_dict()

# NEW (should be):
lag_by_category = {}
if 'Period' in df_7day.columns and 'Crime_Category' in df_7day.columns and 'IncidentToReportDays' in df_7day.columns:
    df_7day_period_only = df_7day[df_7day['Period'] == '7-Day'].copy()
    lag_incidents_only = df_7day_period_only[df_7day_period_only['IncidentToReportDays'] > 0]
    if len(lag_incidents_only) > 0:
        lag_by_category = lag_incidents_only['Crime_Category'].value_counts().to_dict()
```

---

## Error #3: Incident Date Range

### The Problem

**JSON says:** `"earliest": "2026-01-20"`

**CSV shows:** Earliest 7-Day period incident is `02/03/2026`

### The Data

The 7-Day window (Period='7-Day' OR Backfill_7Day=True) contains 3 incidents:

| Incident Date | Crime Category | Period | Backfill |
|---------------|----------------|--------|----------|
| **01/20/2026** | Burglary Auto | 28-Day | **True** |
| 02/03/2026 | Burglary Auto | 7-Day | False |
| 02/05/2026 | Burglary - Comm & Res | 7-Day | False |

### Root Cause

**File:** `scripts/prepare_7day_outputs.py`, Lines 110-121

The code calculates `min_incident` from `df_7day`, which includes backfill incidents. The earliest incident in `df_7day` is the backfill incident from 01/20/2026.

### The Issue

**Is this a bug or intentional?**

The JSON field is called `"incident_date_range"` which suggests it should show:
- **Option A:** Date range of 7-Day **period** incidents only (02/03 to 02/05)
- **Option B:** Date range of the entire 7-Day **window** including backfill (01/20 to 02/05)

Currently it shows Option B, but this is misleading because:
1. The earliest date (01/20) is NOT in the 7-Day period
2. It's a backfill incident from the 28-Day period
3. Users might think the 7-Day period started on 01/20 (it actually started 02/03)

### Recommended Fix

**Rename the field to clarify what it represents:**

```json
"incident_date_range_7day_period": {
  "earliest": "2026-02-03",
  "latest": "2026-02-05"
},
"incident_date_range_full_window": {
  "earliest": "2026-01-20",
  "latest": "2026-02-05"
}
```

**OR** change the calculation to only use 7-Day period incidents:

```python
# Filter to only Period='7-Day' before calculating date range
df_7day_period_only = df_7day[df_7day['Period'] == '7-Day']
if 'Incident_Date_Date' in df_7day_period_only.columns and len(df_7day_period_only) > 0:
    incident_dates = df_7day_period_only['Incident_Date_Date'].dropna()
    # ...
```

---

## Validation Results Summary

### ✅ Correct Fields

1. **total_all_crimes**: `252` ✅
   - Matches CSV total records

2. **incidents_in_7day_period**: `2` ✅
   - Correctly counts incidents where `Period='7-Day'`

3. **backfill_7day**: `1` ✅
   - Correctly counts incidents where `Backfill_7Day=True`

4. **total_7day_window**: `3` ✅
   - Correctly calculated as `incidents_in_7day_period + backfill_7day`

5. **lagdays_distribution**: ✅
   - Min: 1, Max: 5, Mean: 3.0, Median: 3
   - All values correct for the 2 incidents with reporting lag

6. **7day_by_crime_category**: ✅
   - Correctly shows both crime categories with their lag counts:
     - Burglary Auto: LagDayCount=1, TotalCount=1
     - Burglary - Comm & Res: LagDayCount=1, TotalCount=1
     - TOTAL: LagDayCount=2, TotalCount=2

### ❌ Incorrect Fields

1. **lag_incidents**: Should be `2`, shows `1` ❌

2. **lag_analysis.by_crime_category**: Missing "Burglary - Comm & Res" ❌

3. **incident_date_range.earliest**: Shows `2026-01-20` instead of `2026-02-03` ⚠️

### ⚠️ Partial/Context-Dependent Fields

**period_breakdown**: Shows `{"7-Day": 2, "28-Day": 1}`

This is intentionally limited to relevant periods for 7-Day analysis. The CSV contains all periods:
- Prior Year: 232
- 28-Day: 11
- YTD: 7
- 7-Day: 2

The JSON only shows the periods present in the `df_7day` window (7-Day + backfill). This is **acceptable** since the JSON is specifically for 7-Day reporting.

---

## Impact Assessment

### High Priority Issues

**Error #1 & #2** directly affect:
- `SCRPA_Report_Summary.md` — May undercount lag incidents
- `EMAIL_TEMPLATE.txt` — May have incorrect lag statistics
- `CHATGPT_BRIEFING_PROMPT.md` — May provide wrong lag analysis

### Medium Priority Issues

**Error #3** may confuse users about:
- When the 7-Day period actually started
- Which incidents are "current" vs "backfill"

---

## Recommended Actions

### Immediate (Before Next Cycle)

1. **Fix `lag_incidents` count** in `prepare_7day_outputs.py` line 224
2. **Fix `lag_by_category`** in `prepare_7day_outputs.py` lines 148-150
3. **Clarify or fix `incident_date_range`** in `prepare_7day_outputs.py` lines 110-121
4. **Re-run pipeline** for cycle 26C02W06 to regenerate correct JSON
5. **Verify documentation** files have correct lag counts

### Long-Term (Next Sprint)

1. **Add unit tests** for `generate_lagday_summary()` function
2. **Add validation script** to automatically check JSON against CSV
3. **Document the difference** between:
   - "Backfill lag" (cycle-based, `Backfill_7Day=True`)
   - "Reporting lag" (delay-based, `IncidentToReportDays > 0`)

---

## Test Case for Verification

After fixes are applied, the JSON should show:

```json
{
  "counts": {
    "lag_incidents": 2,  // NOT 1
  },
  "lag_analysis": {
    "by_crime_category": {
      "Burglary Auto": 1,
      "Burglary - Comm & Res": 1  // NOT missing
    }
  },
  "incident_date_range": {
    "earliest": "2026-02-03",  // NOT 2026-01-20 (if we choose to show 7-Day period only)
    "latest": "2026-02-05"
  }
}
```

---

## Conclusion

The JSON contains **3 errors**:
1. Undercounts lag incidents (shows 1, should be 2)
2. Missing lag category (shows only Burglary Auto, missing Burglary - Comm & Res)
3. Misleading earliest incident date (shows backfill date, not 7-Day period start)

**Root cause**: Confusion between two types of "lag":
- **Backfill lag** (cycle-based) — incident before cycle start
- **Reporting lag** (delay-based) — delay between incident and report

The code uses `df_lag_only` (backfill) where it should use `IncidentToReportDays > 0` (reporting delay).

**Priority**: Fix before next cycle to ensure accurate documentation and reporting.

---

**Validated by:** Automated analysis comparing JSON against CSV  
**Date:** 2026-02-10  
**Files checked:**
- `SCRPA_7Day_Summary.json`
- `SCRPA_All_Crimes_Enhanced.csv`
- `prepare_7day_outputs.py`

---

## Fix Applied (2026-02-10)

- **Code:** All three fixes were implemented in `scripts/prepare_7day_outputs.py` (lag_incidents, lag_by_category, incident_date_range).
- **Regeneration:** `SCRPA_7Day_Summary.json` was regenerated for cycle 26C02W06; it now shows:
  - `lag_incidents`: 2
  - `lag_analysis.by_crime_category`: `{"Burglary Auto": 1, "Burglary - Comm & Res": 1}`
  - `incident_date_range.earliest`: `"2026-02-03"`
- **Validation:** Use `python scripts/validate_7day_json.py <data_dir>` to verify JSON vs CSV for any cycle.
