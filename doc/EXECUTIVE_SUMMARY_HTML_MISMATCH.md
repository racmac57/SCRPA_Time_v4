# SCRPA HTML Data Mismatch - Executive Summary

**Date:** 2026-02-10  
**Issue:** HTML report contains data from previous cycle (01/27) despite headers showing current cycle (02/10)  
**Status:** Root cause identified, fix options proposed  

---

## 🔴 THE PROBLEM

**What Happened:**
- CSV files: ✅ Correct (252 records, 2 for 7-Day period 02/03-02/09)
- Documentation: ✅ Correct (cycle 26C02W06 metadata)
- HTML Report: ❌ **Contains 01/27 data with 02/10 headers**

**Why It Matters:**
Executive leadership receives **incorrect incident data** in the HTML report while all other outputs are accurate.

---

## 🔍 ROOT CAUSE

### The Architecture Problem

You have **TWO SEPARATE SYSTEMS** processing the same RMS data:

```
System 1: Python Pipeline (16_Reports/SCRPA/)
├─ Reads: RMS Excel
├─ Outputs: Enhanced CSV + JSON + Documentation
└─ Status: ✅ WORKING CORRECTLY

System 2: SCRPA_ArcPy (02_ETL_Scripts/SCRPA_ArcPy/)
├─ Reads: RMS Excel
├─ Outputs: HTML Executive Summary
└─ Status: ❌ NOT RUNNING FOR CURRENT CYCLE
```

### The Workflow Break

**Current Broken Flow:**
1. Python pipeline runs (02/10) → Generates correct CSV/JSON ✅
2. Pipeline tries to call SCRPA_ArcPy → **Fails silently** ❌
3. Pipeline copies HTML from `06_Output/` → **Gets stale file from 01/27** ❌
4. Pipeline patches HTML headers → **Only updates cycle name, NOT data** ❌
5. Result: 02/10 headers + 01/27 data ❌

**What Should Happen:**
1. Python pipeline runs (02/10) → Generates correct CSV/JSON ✅
2. SCRPA_ArcPy generates fresh HTML (02/10) → Creates new HTML with current data ✅
3. Pipeline copies **fresh** HTML → Gets correct 02/10 file ✅
4. Result: 02/10 headers + 02/10 data ✅

---

## 🐛 CRITICAL BUGS IDENTIFIED

### Bug #1: Silent HTML Generation Failure
**File:** `run_scrpa_pipeline.py`, lines 843-853  
**Issue:** When HTML generation fails, pipeline prints warning but **continues anyway**

```python
html_generated = _generate_html_report_via_arcpy(rms_path, cycle_info)
if not html_generated:
    print(f"  ⚠️  HTML generation failed/skipped - will copy existing file if available")
    # ❌ BUG: Still copies old HTML even when generation failed!

reports_copied = _copy_scrpa_reports_to_cycle(paths['reports'], cycle_info)
```

**Impact:** Stale HTML always gets copied, no matter what.

---

### Bug #2: No Data Validation
**File:** `run_scrpa_pipeline.py`, lines 496-509  
**Issue:** Copies "latest" HTML by timestamp, doesn't check if it matches current cycle

```python
combined = list(SCRPA_ARCPY_OUTPUT.glob("SCRPA_Combined_Executive_Summary_*.html"))
if combined:
    latest = max(combined, key=lambda p: p.stat().st_mtime)  # ❌ Gets newest file
    dest = reports_dir / "SCRPA_Combined_Executive_Summary.html"
    shutil.copy2(latest, dest)  # ❌ No validation of content
```

**Impact:** Wrong cycle's HTML gets copied if SCRPA_ArcPy hasn't run recently.

---

### Bug #3: Header-Only Patching
**File:** `run_scrpa_pipeline.py`, lines 392-454  
**Issue:** `patch_scrpa_combined_exec_summary_after_copy()` only changes header pills

```python
# ✅ Patches: Cycle name, date range, version
text = pill_cycle.sub(r"\g<1>" + patch.cycle_id + r"\g<3>", text, count=1)
text = pill_range.sub(r"\g<1>" + f"{range_start} - {range_end}" + r"\g<3>", text, count=1)

# ❌ Does NOT patch: Incident counts, crime types, tables, charts
```

**Impact:** Headers look correct but data tables remain from old cycle.

---

### Bug #4: Divergent Period Logic
**Issue:** Python and SCRPA_ArcPy calculate `Period` differently

**Python (`scrpa_transform.py`):**
```python
# Uses cycle calendar: fixed 7-day window (02/03-02/09)
if 7_Day_Start <= Incident_Date <= 7_Day_End:
    Period = "7-Day"
```

**SCRPA_ArcPy (`RMS_Statistical_Export_FINAL_COMPLETE.py`):**
```python
# Uses rolling window: "today minus N days"
delta = (date.today() - Incident_Date).days
if delta <= 7:
    return "7-Day"
```

**Impact:** Same incident can be classified as "7-Day" in CSV but "28-Day" in HTML!

---

## 💡 SOLUTION OPTIONS

### Option 1: Quick Fix (THIS CYCLE)
**Run SCRPA_ArcPy manually before pipeline:**

```powershell
# Step 1: Generate fresh HTML
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator"
$env:REPORT_DATE = "02/10/2026"
python RMS_Statistical_Export_FINAL_COMPLETE.py

# Step 2: Verify generation
dir "..\06_Output\SCRPA_Combined_Executive_Summary_*.html" | Sort-Object LastWriteTime -Descending | Select -First 1

# Step 3: Re-run Python pipeline
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA"
.\Run_SCRPA_Pipeline.bat
```

**Pros:** Immediate fix for current cycle  
**Cons:** Manual, doesn't prevent future issues

---

### Option 2: Validation Fix (NEXT CYCLE)
**Add HTML validation before copying:**

```python
def _validate_html_for_cycle(html_path: Path, cycle_info: Dict[str, Any]) -> bool:
    """Check if HTML contains correct cycle dates."""
    content = html_path.read_text(encoding='utf-8', errors='ignore')
    start_7 = cycle_info.get('start_7', '')
    end_7 = cycle_info.get('end_7', '')
    return (start_7 in content and end_7 in content)

# In _copy_scrpa_reports_to_cycle():
if not _validate_html_for_cycle(latest, cycle_info):
    print(f"  ⚠️  WARNING: HTML does not match current cycle - SKIPPING COPY")
    return []  # Don't copy wrong data!
```

**Pros:** Prevents copying wrong data, alerts user to problem  
**Cons:** Requires manual SCRPA_ArcPy run, pipeline produces incomplete output

---

### Option 3: Single Source of Truth (BEST LONG-TERM)
**Make SCRPA_ArcPy read Python CSV instead of RMS Excel:**

```python
# In RMS_Statistical_Export_FINAL_COMPLETE.py:
def load_enhanced_csv(csv_path: str) -> pd.DataFrame:
    """Load pre-enriched data from Python pipeline."""
    df = pd.read_csv(csv_path)
    # Period, Crime_Category, LagDays already calculated correctly!
    return df

# Accept CSV path as argument:
parser.add_argument('--enhanced-csv', help='Path to SCRPA_All_Crimes_Enhanced.csv')
```

**Pros:** 
- ✅ Guaranteed data consistency (one transformation)
- ✅ No duplicate period calculation logic
- ✅ CSV and HTML always match

**Cons:** Requires refactoring SCRPA_ArcPy script

---

### Option 4: Integrated HTML Generation (OPTIMAL)
**Move HTML generation into Python pipeline:**

```python
# NEW: scripts/generate_html_report.py
def generate_html_from_csv(csv_path: Path, cycle_info: Dict, output_path: Path):
    """Generate HTML directly from enhanced CSV."""
    df = pd.read_csv(csv_path)
    df_7day = df[df['Period'] == '7-Day']  # Already calculated!
    df_28day = df[df['Period'] == '28-Day']
    df_ytd = df[df['Period'] == 'YTD']
    
    # Calculate stats, generate HTML...
    html_content = generate_html_template(...)
    output_path.write_text(html_content)

# In run_scrpa_pipeline.py:
html_path = paths['reports'] / 'SCRPA_Combined_Executive_Summary.html'
generate_html_from_csv(enhanced_csv, cycle_info, html_path)
```

**Pros:**
- ✅ No subprocess calls, no external dependencies
- ✅ No file copying, no validation needed
- ✅ Single codebase, easier maintenance
- ✅ HTML generated at same time as CSV

**Cons:** Requires porting HTML generation logic to Python pipeline

---

## 📊 COMPARISON MATRIX

| Option | Effort | Reliability | Data Consistency | Maintenance |
|--------|--------|-------------|------------------|-------------|
| **1. Manual Run** | Low | ⚠️ Depends on user | ⚠️ If remembered | ⚠️ High risk |
| **2. Validation** | Low | ⚠️ Alerts only | ⚠️ Catches errors | ⚠️ Still manual |
| **3. CSV Input** | Medium | ✅ Automated | ✅ Guaranteed | ✅ Single logic |
| **4. Integrated** | High | ✅ Automated | ✅ Guaranteed | ✅ Simplest |

---

## 🎯 RECOMMENDED PATH FORWARD

### Phase 1: Immediate (Today)
1. ✅ Run SCRPA_ArcPy manually for 02/10 cycle
2. ✅ Verify HTML generation succeeded
3. ✅ Re-run Python pipeline to copy fresh HTML
4. ✅ Validate HTML data matches CSV data

### Phase 2: Short-term (Next Cycle)
1. ✅ Implement validation checks (Option 2)
2. ✅ Add error handling to fail fast if HTML wrong
3. ✅ Document two-step workflow clearly

### Phase 3: Long-term (1-2 Cycles Out)
1. ✅ Implement Option 3 (CSV input) or Option 4 (Integrated)
2. ✅ Migrate HTML generation to use Python enriched data
3. ✅ Deprecate dual-system architecture
4. ✅ Add integration tests for data consistency

---

## 📋 ACTION ITEMS

**Owner: User**
- [ ] Review proposed solutions
- [ ] Select preferred long-term approach (Option 3 or 4)
- [ ] Approve immediate manual fix for current cycle

**Owner: AI/Developer**
- [ ] Implement immediate fix (manual SCRPA_ArcPy run)
- [ ] Create validation patches (Option 2)
- [ ] Prepare refactoring plan for selected option
- [ ] Write integration tests

---

## 📂 RELATED DOCUMENTS

- **Full Technical Analysis:** `doc/CODE_REVIEW_ANALYSIS_HTML_MISMATCH.md`
- **Root Cause Document:** `doc/ROOT_CAUSE_HTML_MISMATCH.md`
- **Previous Analysis:** `doc/HTML_DATA_MISMATCH_ANALYSIS_v2.md`

---

**End of Executive Summary**  
For detailed code analysis, bug locations, and implementation code, see the full technical review.
