# HTML Report Data Mismatch - Root Cause Analysis v2
## 2026-02-10 - CRITICAL ISSUE

## Problem Statement

The HTML report (`SCRPA_Combined_Executive_Summary.html`) shows:
- ✅ **Correct dates**: Cycle 26BW03, Range 01/27/2026 - 02/09/2026 (patched by pipeline)
- ❌ **Wrong incident count**: Shows 1 incident for 7-Day period
- ✅ **Actual count**: Python pipeline CSV shows 2 incidents for 7-Day period

## Root Cause: Dual Processing Systems

The SCRPA system has **TWO INDEPENDENT data processing pipelines** that produce **DIFFERENT results**:

### System 1: Python Pipeline (scripts/run_scrpa_pipeline.py)
**Input:** RMS Export → `scrpa_transform.py`  
**Logic:** Uses cycle calendar, proper period classification, LagDays calculation  
**Output:** `SCRPA_All_Crimes_Enhanced.csv` (252 rows, 2 7-Day incidents)  
**Result:** ✅ CORRECT DATA

### System 2: SCRPA_ArcPy (02_ETL_Scripts/SCRPA_ArcPy)
**Input:** Same RMS Export → Independent processing  
**Logic:** Own cycle detection, own period classification  
**Output:** `SCRPA_Combined_Executive_Summary.html` (1 7-Day incident)  
**Result:** ❌ INCORRECT DATA

## Evidence

### Python Pipeline CSV (CORRECT)
```
26C02W06_26_02_10/Data/SCRPA_All_Crimes_Enhanced.csv:
- Total rows: 252
- Period='7-Day' incidents: 2
  1. Case 26-012829 (Burglary Auto) - Incident: 02/03, Report: 02/08
  2. Case 26-012181 (Burglary - Comm) - Incident: 02/05, Report: 02/06
```

### SCRPA_ArcPy HTML (INCORRECT)
```
SCRPA_Combined_Executive_Summary_20260210_130727.html:
- 7-Day Incidents: 1
- Shows only: Burglary - Commercial (100%)
- Missing: Case 26-012829 (Burglary Auto)
```

### Patched HTML (CORRECT DATES, WRONG DATA)
```
26C02W06_26_02_10/SCRPA_Combined_Executive_Summary.html:
- Header patched by pipeline: ✅ Cycle 26BW03, Range 01/27/2026-02/09/2026
- Data from SCRPA_ArcPy: ❌ Still shows 1 incident (not 2)
```

## Why the Mismatch Occurs

SCRPA_ArcPy likely has DIFFERENT LOGIC for:
1. **Period Classification** - May use different date ranges or rules
2. **Cycle Detection** - Even with REPORT_DATE, may not match Python pipeline's 3-tier lookup
3. **Data Filtering** - May filter incidents differently
4. **Date Handling** - May parse/classify dates differently

## Current Workflow (BROKEN)

```
RMS Export (256 incidents)
    |
    ├──> Python Pipeline (scrpa_transform.py)
    |    └──> CSV: 252 incidents, 2 7-Day ✅ CORRECT
    |
    └──> SCRPA_ArcPy (RMS_Statistical_Export_FINAL_COMPLETE.py)
         └──> HTML: ??? incidents, 1 7-Day ❌ WRONG
                 |
                 └──> Pipeline patches HTML header (dates) ✅
                      but data content is still wrong ❌
```

## Solution Options

### Option 1: Make SCRPA_ArcPy Read Python CSV (RECOMMENDED)

**Approach:** Modify SCRPA_ArcPy to use `SCRPA_All_Crimes_Enhanced.csv` as input instead of raw RMS export.

**Pros:**
- ✅ Single source of truth (Python pipeline)
- ✅ Guaranteed data consistency
- ✅ HTML will always match CSV data
- ✅ No need to sync two different processing logics

**Cons:**
- Requires modifying SCRPA_ArcPy to accept CSV input
- Need to map Python CSV columns to SCRPA_ArcPy's expected schema

### Option 2: Fix SCRPA_ArcPy Logic to Match Python Pipeline

**Approach:** Debug and fix SCRPA_ArcPy's period classification logic to match Python pipeline.

**Pros:**
- Both systems remain independent
- Can validate one against the other

**Cons:**
- ❌ Maintaining two identical logics in two codebases
- ❌ High risk of future divergence
- ❌ Double the testing effort
- ❌ Complex debugging

### Option 3: Generate HTML from Python Pipeline

**Approach:** Remove SCRPA_ArcPy dependency, generate HTML directly from Python using the CSV data.

**Pros:**
- ✅ Single codebase
- ✅ Complete control over HTML generation
- ✅ Guaranteed accuracy

**Cons:**
- Major refactoring effort
- Lose ArcGIS Pro integration (if used for maps)
- Need to reimplement all HTML generation logic

### Option 4: Don't Use SCRPA_ArcPy HTML (QUICK FIX)

**Approach:** Stop copying the HTML from SCRPA_ArcPy. Use only the Python CSV data and manually create summaries or generate HTML from Python.

**Pros:**
- ✅ Immediate fix
- ✅ No code changes needed

**Cons:**
- ❌ Lose HTML report functionality
- ❌ Doesn't solve the underlying issue

## Recommended Path Forward

**OPTION 1** is the best solution because:

1. **Single Source of Truth**
   - Python pipeline becomes the authoritative data processor
   - All reports (CSV, JSON, HTML) use the same data

2. **Maintainability**
   - Only one place to fix bugs
   - Only one place to add features
   - No sync issues

3. **Implementation**
   ```python
   # In SCRPA_ArcPy: Instead of processing RMS export
   # Read the Python-generated CSV:
   df = pd.read_csv('SCRPA_All_Crimes_Enhanced.csv')
   
   # Then generate HTML from this pre-processed data
   ```

## Immediate Workaround

Until Option 1 is implemented, you have two choices:

**A. Use CSV data only**
- Ignore the HTML report
- Use `SCRPA_Report_Summary.md` and Power BI for reporting
- CSV data is correct

**B. Manually verify HTML**
- Check HTML incident counts against CSV
- If mismatched, note the discrepancy in your report
- Use CSV data as authoritative source

## Next Steps

1. **Decide** which option to pursue (recommend Option 1)
2. **Modify** SCRPA_ArcPy to read Python CSV instead of RMS
3. **Test** HTML generation with Python CSV input
4. **Verify** HTML incident counts match CSV counts
5. **Document** the change in both repositories

## Technical Details

**Files Involved:**
- `scripts/run_scrpa_pipeline.py` (lines 168-210) - Calls SCRPA_ArcPy
- `02_ETL_Scripts/SCRPA_ArcPy/05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py` - HTML generator
- Line ~1500-1600: Cycle detection logic
- Need to modify to accept CSV input instead of RMS

**Key Question:** What input does SCRPA_ArcPy expect, and can it handle the Python CSV format?

---

**Status:** UNRESOLVED  
**Severity:** HIGH - HTML data incorrect  
**Impact:** Cannot trust HTML report for distribution  
**Date:** 2026-02-10
