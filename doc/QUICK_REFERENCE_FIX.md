# QUICK REFERENCE: SCRPA HTML Data Mismatch Fix

**Issue:** HTML shows wrong cycle data  
**Status:** Root cause found, fix ready  
**Urgency:** Fix needed for current cycle (02/10/2026)

---

## 🚨 IMMEDIATE FIX (15 minutes)

### Step 1: Generate Fresh HTML
```powershell
# Open PowerShell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator"

# Set report date
$env:REPORT_DATE = "02/10/2026"

# Run SCRPA_ArcPy
python RMS_Statistical_Export_FINAL_COMPLETE.py
```

**Expected Output:**
```
=== SCRPA RMS STATISTICAL EXPORT SYSTEM ===
✅ Report saved: SCRPA_Combined_Executive_Summary_YYYYMMDD_HHMMSS.html
```

---

### Step 2: Verify HTML Generated
```powershell
# Check newest HTML file
dir "..\06_Output\SCRPA_Combined_Executive_Summary_*.html" | 
  Sort-Object LastWriteTime -Descending | 
  Select-Object -First 1 | 
  Format-List FullName, LastWriteTime
```

**Expected:** File created within last few minutes

---

### Step 3: Re-run Python Pipeline
```powershell
# Go to SCRPA folder
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA"

# Run pipeline
.\Run_SCRPA_Pipeline.bat
```

**Expected Output:**
```
[6/6] Generating and copying reports...
  ✅ HTML report generated successfully
  Copied report: SCRPA_Combined_Executive_Summary.html
```

---

### Step 4: Validate Output
```powershell
# Check cycle folder
cd "Time_Based\2026\26C02W06_26_02_10"

# Compare CSV and HTML
Write-Host "CSV 7-Day count:"
(Import-Csv "Data\SCRPA_All_Crimes_Enhanced.csv" | 
  Where-Object Period -eq "7-Day").Count

Write-Host "HTML file date:"
(Get-Item "Reports\SCRPA_Combined_Executive_Summary.html").LastWriteTime
```

**Expected:** CSV count = 2, HTML modified today

---

## 🐛 WHAT WAS WRONG?

```
┌─────────────────────────────────────────┐
│ Python Pipeline (02/10) runs           │
│   ↓                                     │
│ ✅ Generates CSV (correct)              │
│   ↓                                     │
│ ❌ Tries to generate HTML → FAILS       │
│   ↓                                     │
│ ❌ Copies old HTML from 01/27           │
│   ↓                                     │
│ ⚠️  Only patches headers                │
│   ↓                                     │
│ Result: 02/10 headers + 01/27 data ❌   │
└─────────────────────────────────────────┘
```

**Root Cause:**
- SCRPA_ArcPy is a **separate system** that must be run independently
- Python pipeline **assumes** fresh HTML exists but doesn't verify
- When HTML generation fails, pipeline **silently continues**
- Only **headers** are patched, **data tables** remain from old cycle

---

## 📋 QUICK CHECKLIST

**Before Each Cycle Report:**

- [ ] Run SCRPA_ArcPy manually with correct date
- [ ] Verify HTML file created in `06_Output/`
- [ ] Run Python pipeline
- [ ] Check HTML file modified date in cycle folder
- [ ] Spot-check incident counts in HTML vs CSV

**Files to Check:**
```
Time_Based/2026/26C02W06_26_02_10/
├─ Data/SCRPA_All_Crimes_Enhanced.csv
│  └─ Count rows where Period = "7-Day"
└─ Reports/SCRPA_Combined_Executive_Summary.html
   └─ Look for "7-Day Incidents" count in HTML
```

**Counts Should Match:**
- CSV: Filter `Period = "7-Day"` → Count rows
- HTML: Find "7-Day Executive Summary" → Check incident count

---

## 🔧 FILE LOCATIONS

### Input
```
05_EXPORTS\_RMS\scrpa\
└─ [Latest RMS Excel file]
```

### SCRPA_ArcPy
```
02_ETL_Scripts\SCRPA_ArcPy\
├─ 05_orchestrator\RMS_Statistical_Export_FINAL_COMPLETE.py
└─ 06_Output\SCRPA_Combined_Executive_Summary_*.html
```

### Python Pipeline
```
16_Reports\SCRPA\
├─ scripts\run_scrpa_pipeline.py
└─ Time_Based\2026\26C02W06_26_02_10\
    ├─ Data\*.csv
    └─ Reports\*.html
```

---

## ⚠️ COMMON ISSUES

### Issue 1: "SCRPA_ArcPy script not found"
**Solution:** Check path in `run_scrpa_pipeline.py` line 140:
```python
SCRPA_ARCPY_SCRIPT = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator\RMS_Statistical_Export_FINAL_COMPLETE.py")
```

### Issue 2: HTML file not generated
**Check:**
1. RMS Excel file exists in `05_EXPORTS\_RMS\scrpa\`
2. Python environment has required packages
3. Check SCRPA_ArcPy output for errors

### Issue 3: HTML copied but data still wrong
**Reason:** Old HTML file still newest in `06_Output/`  
**Solution:** Delete old HTML files or check timestamps carefully

---

## 📞 HELP

### Full Documentation
- **Executive Summary:** `doc/EXECUTIVE_SUMMARY_HTML_MISMATCH.md`
- **Technical Analysis:** `doc/CODE_REVIEW_ANALYSIS_HTML_MISMATCH.md`
- **Data Flow Diagrams:** `doc/DATA_FLOW_DIAGRAMS.md`
- **Deliverables:** `doc/CODE_REVIEW_DELIVERABLES.md`

### Quick Tests
```python
# Verify CSV data
import pandas as pd
df = pd.read_csv('Data/SCRPA_All_Crimes_Enhanced.csv')
print(f"7-Day incidents: {len(df[df['Period'] == '7-Day'])}")

# Check HTML dates
with open('Reports/SCRPA_Combined_Executive_Summary.html') as f:
    content = f.read()
    if '02/03/2026' in content and '02/09/2026' in content:
        print("✅ HTML has correct cycle dates")
    else:
        print("❌ HTML has wrong cycle dates")
```

---

## 🎯 PERMANENT FIX OPTIONS

### Option A: Add Validation (Quick)
Add check before copying HTML:
```python
if not validate_html_matches_cycle(html_file, cycle_info):
    raise ValueError("HTML doesn't match current cycle!")
```

### Option B: Use CSV for HTML (Recommended)
Make SCRPA_ArcPy read Python CSV instead of raw RMS:
```python
# SCRPA_ArcPy reads SCRPA_All_Crimes_Enhanced.csv
# Period, Crime_Category already calculated
# Guaranteed consistency
```

### Option C: Integrated HTML (Best)
Move HTML generation into Python pipeline:
```python
# Generate HTML natively from CSV
# No separate SCRPA_ArcPy needed
# Single pipeline run
```

**See full documentation for implementation details.**

---

## ✅ SUCCESS CRITERIA

**Immediate Fix Working:**
- [ ] HTML file modified today
- [ ] HTML contains 02/03-02/09 date range
- [ ] 7-Day incident count matches CSV
- [ ] No error messages in pipeline output

**Long-term Fix Working:**
- [ ] Single command generates all outputs
- [ ] No manual SCRPA_ArcPy run needed
- [ ] CSV and HTML always consistent
- [ ] Pipeline fails fast if HTML wrong

---

**Last Updated:** 2026-02-10  
**Next Review:** After implementing permanent fix
