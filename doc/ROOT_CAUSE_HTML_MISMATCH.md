# ROOT CAUSE ANALYSIS: HTML Report Data Mismatch

**Date:** 2026-02-10  
**Cycle:** 26C02W06_26_02_10  
**Issue:** HTML report contains wrong data from previous cycle (01/27)

---

## 🔴 Problem Summary

### The Mismatch:

| File | Cycle Info | Data Correct? |
|------|-----------|---------------|
| `Data/SCRPA_All_Crimes_Enhanced.csv` | 26C02W06, 02/03-02/09 | ✅ YES (252 records, 2 for 7-Day) |
| `Documentation/SCRPA_Report_Summary.md` | 26C02W06, 02/03-02/09 | ✅ YES (correct counts) |
| `Documentation/CHATGPT_BRIEFING_PROMPT.md` | 26C02W06, 02/03-02/09 | ✅ YES (correct dates) |
| `Reports/SCRPA_Combined_Executive_Summary.html` | 26BW03, 02/03-02/09 (header) | ❌ NO (contains 01/27 data) |

**The HTML headers were patched but the actual incident data is from the old cycle!**

---

## 🔍 Root Cause

### The Two-System Problem:

You have **TWO separate processing systems** that must run in sequence:

**System 1: SCRPA_ArcPy** (`02_ETL_Scripts/SCRPA_ArcPy/`)
- **Purpose:** Generate HTML reports from RMS Excel exports
- **Input:** `05_EXPORTS\_RMS\scrpa\*.xlsx`
- **Output:** `02_ETL_Scripts\SCRPA_ArcPy\06_Output\SCRPA_Combined_Executive_Summary_*.html`
- **Script:** `05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py`

**System 2: Python Pipeline** (`16_Reports/SCRPA/`)
- **Purpose:** Transform RMS data to enhanced CSV, generate documentation
- **Input:** `05_EXPORTS\_RMS\scrpa\*.xlsx`
- **Output:** `Time_Based/2026/CYCLE/` with Data/, Documentation/, Reports/
- **Script:** `scripts/run_scrpa_pipeline.py`

### The Workflow Break:

The Python pipeline **copies** HTML from `SCRPA_ArcPy/06_Output/` but **SCRPA_ArcPy hasn't run** for the current cycle (02/10).

**Last run of SCRPA_ArcPy:** 2026-01-27 (for cycle 26BW03/01/27)  
**Current run of Python Pipeline:** 2026-02-10 (for cycle 26C02W06/02/10)  
**Result:** Pipeline copies **stale HTML** from 01/27

---

## ✅ LASTING SOLUTION (3 Options)

### Option 1: Integrate SCRPA_ArcPy into Pipeline (RECOMMENDED)

Modify `run_scrpa_pipeline.py` to call SCRPA_ArcPy **before** copying HTML:

**Workflow:**
```python
1. Load RMS data → Transform to CSV
2. Generate 7-day outputs
3. ➕ Call SCRPA_ArcPy script to generate HTML ← NEW STEP
4. Copy fresh HTML from 06_Output to Reports/
5. Patch HTML headers
6. Generate documentation
```

**Implementation:**
```python
# In run_scrpa_pipeline.py, before _copy_scrpa_reports_to_cycle():

def _generate_html_report_via_arcpy(rms_path: Path, cycle_info: Dict[str, Any]) -> bool:
    """
    Call SCRPA_ArcPy to generate HTML report before copying.
    """
    arcpy_script = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator\RMS_Statistical_Export_FINAL_COMPLETE.py")
    
    if not arcpy_script.exists():
        print("  SCRPA_ArcPy script not found - skipping HTML generation")
        return False
    
    # Set environment variables for cycle info
    env = os.environ.copy()
    env['REPORT_DATE'] = cycle_info['report_due']
    
    # Run SCRPA_ArcPy script
    result = subprocess.run(
        ['python', str(arcpy_script)],
        env=env,
        capture_output=True,
        text=True
    )
    
    return result.returncode == 0
```

Then call it before copying:
```python
# Step 6: Generate and copy reports
print(f"\n[6/6] Generating HTML report...")
_generate_html_report_via_arcpy(rms_path, cycle_info)
reports_copied = _copy_scrpa_reports_to_cycle(paths['reports'], cycle_info)
```

---

### Option 2: Update SCRPA_ArcPy to Use Python CSV (ALTERNATIVE)

Modify `RMS_Statistical_Export_FINAL_COMPLETE.py` to read from the **Python-generated CSV** instead of the raw RMS export:

**Benefits:**
- Single source of truth (Python transformations)
- No duplicate processing logic
- Guaranteed data consistency

**Changes needed:**
1. Add command-line argument for CSV input path
2. Skip RMS Excel reading, load from `SCRPA_All_Crimes_Enhanced.csv` instead
3. Use Python's `Period`, `Crime_Category`, `TimeOfDay` columns directly

---

### Option 3: Manual Two-Step Workflow (CURRENT STATE)

Document that users must run **both systems** separately:

**Step 1:** Run SCRPA_ArcPy
```bat
cd C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator
set REPORT_DATE=02/10/2026
python RMS_Statistical_Export_FINAL_COMPLETE.py
```

**Step 2:** Run Python Pipeline
```bat
cd C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\scripts
Run_SCRPA_Pipeline.bat
```

---

## 🎯 Recommended Approach

**Option 1 (Integrate into Pipeline)** is the best because:
- ✅ Single command to run everything
- ✅ Correct execution order guaranteed
- ✅ No manual steps needed
- ✅ HTML always has correct data

---

## 🔧 Implementation Steps

### For This Cycle (Immediate Fix):

1. **Run SCRPA_ArcPy manually** to generate fresh HTML:
   ```bat
   cd C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator
   set REPORT_DATE=02/10/2026
   python RMS_Statistical_Export_FINAL_COMPLETE.py
   ```

2. **Copy the new HTML** to your cycle folder:
   ```
   From: 02_ETL_Scripts\SCRPA_ArcPy\06_Output\SCRPA_Combined_Executive_Summary_*.html
   To: 16_Reports\SCRPA\Time_Based\2026\26C02W06_26_02_10\Reports\
   ```

### For Future Cycles (Permanent Fix):

Would you like me to:
1. **Implement Option 1** - Integrate SCRPA_ArcPy call into `run_scrpa_pipeline.py`?
2. **Implement Option 2** - Update SCRPA_ArcPy to read Python CSV?
3. **Document Option 3** - Create clear two-step workflow documentation?

Which approach would you prefer?

---

## Summary

**What happened:**
- Python pipeline ran correctly ✅
- SCRPA_ArcPy didn't run for current cycle ❌
- Pipeline copied old HTML from 01/27 ❌

**Why:**
- The two systems are independent
- Pipeline assumes fresh HTML exists
- No automatic triggering of SCRPA_ArcPy

**Fix:**
- Either integrate the systems (automatic)
- Or document two-step manual process (manual but clear)
