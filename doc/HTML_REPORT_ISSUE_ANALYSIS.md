# HTML Report Generation Issue - Analysis and Solution

**Date:** 2026-02-10  
**Cycle:** 26C02W06  
**Issue:** HTML report contains wrong data from previous cycle

---

## Problem Summary

### Current State:
- ✅ **CSV Data**: Correct (252 records, 2 incidents in 7-Day period)
- ✅ **Documentation Files**: Correct (Report Summary, Briefing Prompt)
- ❌ **HTML Report**: WRONG - Shows 3 incidents in 7-Day (data from 01/27 cycle)

### Root Cause:

The `run_scrpa_pipeline.py` script **copies** an existing HTML file from:
```
SCRPA_ArcPy\06_Output\SCRPA_Combined_Executive_Summary_*.html
```

This file was generated on **2026-01-27** for the previous cycle and hasn't been regenerated for the current cycle (02/10).

---

## Why Header Patching Isn't Enough

The pipeline has logic to **patch the HTML headers** (cycle name, date range) but does NOT regenerate the actual incident data inside the report.

**What gets patched:**
- ✅ Cycle name (26BW03)
- ✅ Date range in header
- ✅ Footer

**What does NOT get updated:**
- ❌ Incident counts
- ❌ Crime type distribution
- ❌ Incident details
- ❌ All the actual data

---

## The Missing Step

According to the README, the workflow should be:

```
Step 1: Run Python pipeline → Generate CSV data
Step 2: Run SCRPA_ArcPy → Generate HTML reports from CSV  ← THIS IS MISSING!
Step 3: Pipeline copies HTML → Latest HTML to cycle folder
```

**Currently happening:**
```
Step 1: Run Python pipeline → Generate CSV data ✓
Step 2: SKIPPED - No HTML regeneration  ← PROBLEM!
Step 3: Pipeline copies OLD HTML → Stale data copied ✗
```

---

## Solutions

### Immediate Fix (Manual):

Since the HTML contains complex formatting and analysis, you need to regenerate it using SCRPA_ArcPy or similar tooling that reads the current CSV and produces the HTML.

**Steps:**
1. Delete the wrong HTML:
   ```
   Time_Based\2026\26C02W06_26_02_10\Reports\SCRPA_Combined_Executive_Summary.html
   ```

2. Run SCRPA_ArcPy report generation with:
   - Input: `Time_Based\2026\26C02W06_26_02_10\Data\SCRPA_All_Crimes_Enhanced.csv`
   - Output: Fresh HTML in `SCRPA_ArcPy\06_Output\`

3. Copy the new HTML to the Reports folder

---

### Permanent Solution: Update Pipeline

The `run_scrpa_pipeline.py` should either:

**Option A: Generate HTML Directly (Best)**
- Add HTML generation logic to the pipeline
- Read from `SCRPA_All_Crimes_Enhanced.csv`
- Generate HTML report with correct data
- No dependency on external SCRPA_ArcPy files

**Option B: Call SCRPA_ArcPy First (If You Must)**
- Before copying HTML, call SCRPA_ArcPy to regenerate it
- Add subprocess call to run the HTML generation script
- Then copy the fresh HTML

**Option C: Don't Copy HTML at All**
- Remove the HTML copy step from pipeline
- Require manual HTML generation after pipeline completes
- Document this as a required step

---

## Workflow Fix

### Updated Bi-Weekly Workflow:

```
1. Export RMS data
2. Run pipeline: Run_SCRPA_Pipeline.bat
   → Creates cycle folder
   → Generates CSV files  
   → Creates documentation (correct)
   → Copies HTML (WRONG - stale data)
   
3. [NEW STEP] Regenerate HTML:
   → Run SCRPA_ArcPy with current cycle CSV
   → Or use Python script to generate HTML
   → Replace the HTML in Reports folder

4. Open Power BI and refresh
5. Verify all files correct
6. Send report
```

---

## Recommendation

**Short-term (This Cycle):**
- Manually regenerate the HTML using SCRPA_ArcPy or equivalent
- Replace the stale HTML in the Reports folder

**Long-term (Next Release):**
- Add HTML generation to `run_scrpa_pipeline.py`
- Or call SCRPA_ArcPy automatically as part of the pipeline
- Or remove HTML copy and document manual step requirement

The current pipeline design assumes SCRPA_ArcPy runs separately and produces fresh HTML files. If this isn't happening automatically, you need to either:
1. Make it automatic (integrate into pipeline), or
2. Make it a required manual step (update documentation)

---

## Files to Check

**Does SCRPA_ArcPy Exist?**
```
C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\
```

**If yes:**
- Find the HTML generation script
- Run it with current cycle CSV
- Copy output to Reports folder

**If no:**
- Need to create HTML generation logic
- Or use ChatGPT to generate briefing instead
- Or accept that HTML will always be stale until regenerated

---

## Questions to Answer

1. **Do you have SCRPA_ArcPy scripts?** If yes, where and how to run them?
2. **Should HTML generation be automated?** Should the pipeline generate HTML or just copy it?
3. **Is the HTML report critical?** Or can you use ChatGPT briefing + Power BI instead?

The answers will determine which permanent solution to implement.
