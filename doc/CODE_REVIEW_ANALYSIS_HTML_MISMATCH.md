# CODE REVIEW: SCRPA HTML Data Mismatch - Technical Analysis

**Review Date:** 2026-02-10  
**Reviewer:** AI Code Review Agent  
**Issue:** HTML report contains wrong data from previous cycle  
**Cycles Affected:** 26C02W06 (02/10/2026) showing 26BW03 (01/27/2026) data  

---

## 🔍 EXECUTIVE SUMMARY

**Root Cause Confirmed:** The Python pipeline (`run_scrpa_pipeline.py`) **copies stale HTML** from `SCRPA_ArcPy/06_Output/` without regenerating it. The HTML generation system (`SCRPA_ArcPy`) is a **completely separate codebase** that must be run independently.

**Critical Finding:** There are **TWO INDEPENDENT DATA TRANSFORMATION SYSTEMS** processing the same RMS source data with **DIFFERENT LOGIC**, creating a **dual-source-of-truth problem**.

---

## 📊 SYSTEM ARCHITECTURE ANALYSIS

### System 1: Python Pipeline (`16_Reports/SCRPA/`)

**Location:** `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\`

**Purpose:** Transform RMS data to enhanced CSV with cycle-based enrichment

**Key Scripts:**
- `scripts/run_scrpa_pipeline.py` - Main orchestrator
- `scripts/scrpa_transform.py` - Core transformation engine
- `scripts/prepare_7day_outputs.py` - 7-day filtering and lag analysis
- `scripts/generate_documentation.py` - Documentation generator

**Data Flow:**
```
RMS Export (xlsx)
    ↓
scrpa_transform.py
    ↓ [Cycle resolution, Period classification, Lag calculation]
SCRPA_All_Crimes_Enhanced.csv
    ↓
prepare_7day_outputs.py
    ↓ [7-day filtering, JSON summary generation]
SCRPA_7Day_With_LagFlags.csv + SCRPA_7Day_Summary.json
    ↓
generate_documentation.py
    ↓
SCRPA_Report_Summary.md + EMAIL_TEMPLATE.txt
```

**Output:** CSV files, JSON metadata, Markdown documentation

---

### System 2: SCRPA_ArcPy (`02_ETL_Scripts/SCRPA_ArcPy/`)

**Location:** `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\`

**Purpose:** Generate HTML executive summary reports with embedded charts

**Key Script:**
- `05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py`

**Data Flow:**
```
RMS Export (xlsx)
    ↓
RMS_Statistical_Export_FINAL_COMPLETE.py
    ↓ [Period bucketing, Stats calculation, HTML generation]
SCRPA_Combined_Executive_Summary_TIMESTAMP.html
    ↓ [Stored in 06_Output/]
HTML Report with inline CSS and data tables
```

**Output:** Self-contained HTML reports with embedded data

---

## 🔴 CRITICAL CODE ANALYSIS

### Issue 1: Stale HTML Copy Mechanism

**File:** `scripts/run_scrpa_pipeline.py`  
**Function:** `_copy_scrpa_reports_to_cycle()` (lines 482-511)

```python
def _copy_scrpa_reports_to_cycle(reports_dir: Path, cycle_info: Optional[Dict[str, Any]] = None) -> list:
    """
    Copy latest SCRPA_Combined_Executive_Summary.html from SCRPA_ArcPy/06_Output to cycle Reports folder.
    """
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    if not SCRPA_ARCPY_OUTPUT.exists():
        print(f"  Reports source not found: {SCRPA_ARCPY_OUTPUT} (skipping copy)")
        return []

    copied = []
    combined = list(SCRPA_ARCPY_OUTPUT.glob("SCRPA_Combined_Executive_Summary_*.html"))
    if combined:
        latest = max(combined, key=lambda p: p.stat().st_mtime)  # ⚠️ GETS LATEST BY TIMESTAMP
        dest = reports_dir / "SCRPA_Combined_Executive_Summary.html"
        try:
            shutil.copy2(latest, dest)
            copied.append(str(dest))
            print(f"  Copied report: {dest.name}")
            if cycle_info:
                patch_scrpa_combined_exec_summary_after_copy(dest, cycle_info)  # Only patches headers!
        except OSError as e:
            print(f"  Could not copy {latest.name}: {e}")
    else:
        print("  No SCRPA_Combined_Executive_Summary_*.html found in 06_Output")

    return copied
```

**Problems:**
1. ❌ **Assumes fresh HTML exists** - No check if HTML matches current cycle
2. ❌ **Copies by modification time** - Gets "latest" file, not "correct cycle" file
3. ❌ **Only patches headers** - Does not regenerate data tables/charts
4. ❌ **No validation** - No verification that HTML data matches CSV data

**Evidence from ROOT_CAUSE_HTML_MISMATCH.md:**
> "Last run of SCRPA_ArcPy: 2026-01-27 (for cycle 26BW03/01/27)  
> Current run of Python Pipeline: 2026-02-10 (for cycle 26C02W06/02/10)  
> Result: Pipeline copies **stale HTML** from 01/27"

---

### Issue 2: HTML Generation Stub (Non-Functional)

**File:** `scripts/run_scrpa_pipeline.py`  
**Function:** `_generate_html_report_via_arcpy()` (lines 150-210)

```python
def _generate_html_report_via_arcpy(
    rms_path: Path,
    cycle_info: Dict[str, Any]
) -> bool:
    """
    Call SCRPA_ArcPy to generate fresh HTML report from RMS export.
    
    This ensures the HTML report in 06_Output is current before copying.
    """
    import subprocess
    
    if not SCRPA_ARCPY_SCRIPT.exists():
        print(f"  ⚠️  SCRPA_ArcPy script not found: {SCRPA_ARCPY_SCRIPT}")
        print(f"  HTML report will not be generated - copy will use existing file")
        return False  # ⚠️ SILENTLY FAILS AND CONTINUES
    
    # Prepare environment with REPORT_DATE for cycle lookup
    env = os.environ.copy()
    report_date = cycle_info.get('report_due', '')
    if report_date:
        env['REPORT_DATE'] = report_date
        print(f"  Generating HTML report for {report_date}...")
    else:
        print(f"  Generating HTML report (auto-detect date)...")
    
    # Run SCRPA_ArcPy script
    try:
        result = subprocess.run(
            [sys.executable, str(SCRPA_ARCPY_SCRIPT)],
            env=env,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"  ✅ HTML report generated successfully")
            return True
        else:
            print(f"  ❌ HTML generation failed (exit code {result.returncode})")
            if result.stderr:
                print(f"  Error output: {result.stderr[:500]}")
            return False  # ⚠️ CONTINUES TO COPY STALE HTML
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  HTML generation timed out after 5 minutes")
        return False  # ⚠️ CONTINUES TO COPY STALE HTML
    except Exception as e:
        print(f"  ❌ Error running SCRPA_ArcPy: {e}")
        return False  # ⚠️ CONTINUES TO COPY STALE HTML
```

**Problems:**
1. ❌ **No error handling** - Returns `False` but pipeline continues anyway
2. ❌ **Silent degradation** - Failure to generate HTML doesn't stop the pipeline
3. ❌ **No validation** - No check if generated HTML contains correct cycle data
4. ❌ **Weak integration** - Subprocess call without proper error propagation

**Evidence from code execution flow (lines 842-853):**
```python
# 6a. Generate HTML report from RMS export
print(f"  [6a] Generating HTML report via SCRPA_ArcPy...")
html_generated = _generate_html_report_via_arcpy(rms_path, cycle_info)
if not html_generated:
    print(f"  ⚠️  HTML generation failed/skipped - will copy existing file if available")

# 6b. Copy reports from SCRPA_ArcPy/06_Output to cycle Reports folder
print(f"  [6b] Copying reports to {paths['reports'].name}/...")
reports_copied = _copy_scrpa_reports_to_cycle(paths['reports'], cycle_info)
```

**The pipeline ALWAYS copies HTML even if generation fails!**

---

### Issue 3: Dual Data Transformation Logic (Inconsistency Risk)

Both systems independently transform the same RMS data with **different logic**:

#### Python Pipeline Transformation Logic

**File:** `scripts/scrpa_transform.py`  
**Function:** `build_all_crimes_enhanced()` (lines 600+)

**Key Logic:**
- **Cycle Resolution:** 3-tier lookup (Report_Due_Date match → In-cycle → Most recent)
- **Period Classification:** `7-Day`, `28-Day`, `YTD`, `Prior Year`, `Historical`
  - Based on **Incident_Date** vs **7_Day_Start/7_Day_End from cycle calendar**
  - Uses **fixed window** from calendar, NOT rolling "today minus 7 days"
- **Lag Calculation:** `LagDays = CycleStart_7Day - Incident_Date`
- **Backfill Detection:** `Backfill_7Day = (Incident before cycle) AND (Report in 7-day window)`
- **Reporting Delay:** `IncidentToReportDays = Report_Date - Incident_Date`

**Evidence from scrpa_transform.py docstring (lines 15-20):**
```python
Critical Logic Rules (must match M code exactly):
1. Cycle Resolution: 3-tier lookup (Report_Due_Date match -> In-cycle -> Most recent)
2. LagDays = CycleStart_7Day - Incident_Date (NOT Report_Date - Incident_Date)
3. Report_Date_ForLagday: Only Report_Date or EntryDate (no Incident_Date fallback)
4. Period Classification: Incident_Date-driven, precedence: 7-Day -> Prior Year -> 28-Day -> YTD -> Historical
5. Backfill_7Day: Incident before cycle start AND Report_Date_ForLagday in current 7-day window
```

#### SCRPA_ArcPy Transformation Logic

**File:** `02_ETL_Scripts/SCRPA_ArcPy/05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py`  
**Function:** `_period_bucket()` (lines 76-84)

```python
def _period_bucket(d: date, today: date | None = None) -> str:
    today = today or date.today()
    if d is None: 
        return "Historical"
    delta = (today - d).days
    if delta <= 7: return "7-Day"
    if delta <= 28: return "28-Day"
    if d.year == today.year: return "YTD"
    return "Historical"
```

**Key Differences:**
- ❌ **Rolling window:** Uses `date.today()` for period calculation
- ❌ **No cycle calendar:** No awareness of `7_Day_Start/7_Day_End`
- ❌ **Simple delta logic:** `delta <= 7` instead of calendar-based window
- ❌ **Different bucketing:** No `Prior Year` period (goes straight to `Historical`)
- ❌ **No backfill tracking:** No `Backfill_7Day` concept

**Evidence from RMS_Statistical_Export_FINAL_COMPLETE.py (lines 86-110):**
```python
def _compute_period_series(incident_date_str: pd.Series, range_end_str: str) -> pd.Series:
    """
    Compute period bucket for each date in the series.
    Uses range_end_str as the reference date if provided, otherwise uses today.
    """
    try:
        if range_end_str:
            today = pd.to_datetime(range_end_str).date()
        else:
            today = date.today()  # ⚠️ Fallback to current date
    except Exception:
        today = date.today()
    
    def _to_date(x):
        if x is None or pd.isna(x): 
            return None
        if hasattr(x, "date"): 
            return x.date()
        try:
            return pd.to_datetime(x).date()
        except Exception:
            return None
    
    return incident_date_str.map(lambda x: _period_bucket(_to_date(x), today))
```

---

### Issue 4: HTML Report Data Embedding

**File:** `02_ETL_Scripts/SCRPA_ArcPy/05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py`  
**Function:** `generate_combined_executive_summary_html()` (lines 1600+)

The HTML report embeds data **directly in the HTML structure** during generation:

```python
html_content = f"""
<div class="report-card">
  <h2>{period} Executive Summary</h2>
  <p class="summary"><strong>{stats.get('total_incidents', 0)} incidents</strong> 
     across <strong>{stats.get('zones_affected', 0)} zones</strong>. 
     Primary incident: <strong>{stats.get('top_crime', 'N/A')} - 
     {stats.get('top_crime_count', 0)} occurrences</strong>.</p>
  
  <table>
    <thead><tr><th>Item</th><th>Count</th><th>%</th></tr></thead>
    <tbody>"""

# Add incident type distribution
for incident_type, count in stats.get('crime_distribution', {}).items():
    percentage = (count / stats.get('total_incidents', 1)) * 100
    html_content += f"""
        <tr><td>{incident_type}</td><td>{count}</td><td>{percentage:.1f}%</td></tr>"""
```

**Problem:** HTML is **not a template** - it's a **frozen snapshot** of the data at generation time.

**The `patch_scrpa_combined_exec_summary_after_copy()` function ONLY patches:**
- Header pills (Cycle name, date range, version)
- Footer text

**It CANNOT patch:**
- ❌ Incident counts
- ❌ Crime type distributions
- ❌ Zone activity tables
- ❌ Hourly/daily distributions
- ❌ Recent incident lists
- ❌ Statistical summaries

**Evidence from run_scrpa_pipeline.py (lines 355-368):**
```python
text = pill_cycle.sub(r"\g<1>" + patch.cycle_id + r"\g<3>", text, count=1)
text = pill_range.sub(
    r"\g<1>" + f"{patch.range_start} - {patch.range_end}" + r"\g<3>", text, count=1
)
if patch.version:
    text = pill_version.sub(r"\g<1>" + patch.version + r"\g<3>", text, count=1)
```

**Only regex-replaces pill content, NOT data tables!**

---

## 🎯 DATA FLOW ANALYSIS

### Current Pipeline Flow (BROKEN)

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Python Pipeline Runs (02/10/2026)                  │
├─────────────────────────────────────────────────────────────┤
│ RMS Export (02/10/2026 data)                               │
│   ↓                                                          │
│ scrpa_transform.py                                           │
│   ↓ [Processes with cycle calendar: 26C02W06, 02/03-02/09] │
│ SCRPA_All_Crimes_Enhanced.csv ✅ (252 rows, 2 for 7-Day)   │
│   ↓                                                          │
│ prepare_7day_outputs.py                                      │
│   ↓ [Filters IsCurrent7DayCycle = TRUE]                    │
│ SCRPA_7Day_Summary.json ✅ (Correct counts for 02/03-02/09)│
│   ↓                                                          │
│ generate_documentation.py                                    │
│   ↓                                                          │
│ SCRPA_Report_Summary.md ✅ (Correct metadata)              │
└─────────────────────────────────────────────────────────────┘
                          ↓
                          ↓ [Step 6: HTML Copy]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: _generate_html_report_via_arcpy() FAILS            │
├─────────────────────────────────────────────────────────────┤
│ Subprocess call to SCRPA_ArcPy script                       │
│   ↓                                                          │
│ ⚠️ Script not found OR execution error OR timeout          │
│   ↓                                                          │
│ Returns False                                                │
│   ↓                                                          │
│ Pipeline prints warning but CONTINUES                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
                          ↓ [Step 6b: Copy anyway!]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: _copy_scrpa_reports_to_cycle() Copies Stale HTML   │
├─────────────────────────────────────────────────────────────┤
│ Searches: SCRPA_ArcPy/06_Output/*.html                      │
│   ↓                                                          │
│ Finds: SCRPA_Combined_Executive_Summary_20260127_*.html     │
│        (Last generated on 01/27/2026 for cycle 26BW03)     │
│   ↓                                                          │
│ Copies to: Time_Based/2026/26C02W06_26_02_10/Reports/       │
│   ↓                                                          │
│ patch_scrpa_combined_exec_summary_after_copy()              │
│   ↓ [Only patches header pills with 26C02W06 info]         │
│                                                              │
│ Result: HTML with 26C02W06 header but 01/27 data ❌        │
└─────────────────────────────────────────────────────────────┘
```

### What SHOULD Happen

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Python Pipeline Runs (02/10/2026)                  │
├─────────────────────────────────────────────────────────────┤
│ [Same as above - CSV/JSON generation]                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
                          ↓ [Step 6a: Generate HTML]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: SCRPA_ArcPy Generates FRESH HTML                   │
├─────────────────────────────────────────────────────────────┤
│ _generate_html_report_via_arcpy() calls subprocess          │
│   ↓                                                          │
│ RMS_Statistical_Export_FINAL_COMPLETE.py runs               │
│   ↓ [Reads RMS export for 02/10/2026]                      │
│   ↓ [Calculates stats for 7-Day, 28-Day, YTD]              │
│   ↓ [Generates HTML with embedded data tables]             │
│   ↓                                                          │
│ SCRPA_Combined_Executive_Summary_20260210_*.html ✅         │
│ (Stored in SCRPA_ArcPy/06_Output/)                          │
└─────────────────────────────────────────────────────────────┘
                          ↓
                          ↓ [Step 6b: Copy FRESH HTML]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: _copy_scrpa_reports_to_cycle() Copies Fresh HTML   │
├─────────────────────────────────────────────────────────────┤
│ Searches: SCRPA_ArcPy/06_Output/*.html                      │
│   ↓                                                          │
│ Finds: SCRPA_Combined_Executive_Summary_20260210_*.html     │
│        (JUST generated for 02/10/2026 cycle)               │
│   ↓                                                          │
│ Copies to: Time_Based/2026/26C02W06_26_02_10/Reports/       │
│   ↓                                                          │
│ patch_scrpa_combined_exec_summary_after_copy()              │
│   ↓ [Patches header pills with 26C02W06 info]              │
│                                                              │
│ Result: HTML with 26C02W06 header AND 02/10 data ✅        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🐛 IDENTIFIED BUGS

### Bug #1: Silent HTML Generation Failure

**Location:** `run_scrpa_pipeline.py`, lines 843-848

**Current Code:**
```python
html_generated = _generate_html_report_via_arcpy(rms_path, cycle_info)
if not html_generated:
    print(f"  ⚠️  HTML generation failed/skipped - will copy existing file if available")

# 6b. Copy reports from SCRPA_ArcPy/06_Output to cycle Reports folder
reports_copied = _copy_scrpa_reports_to_cycle(paths['reports'], cycle_info)
```

**Bug:** Pipeline continues to copy HTML even when generation fails

**Fix:**
```python
html_generated = _generate_html_report_via_arcpy(rms_path, cycle_info)
if not html_generated:
    print(f"  ⚠️  HTML generation failed/skipped")
    print(f"  ⚠️  WARNING: Reports/ will contain stale HTML or no HTML")
    # Option 1: Fail fast
    # raise RuntimeError("HTML generation required but failed")
    # Option 2: Skip copy
    # return results
    # Option 3: Continue but mark results as degraded
    results['html_stale'] = True

# Only copy if generation succeeded
if html_generated:
    reports_copied = _copy_scrpa_reports_to_cycle(paths['reports'], cycle_info)
else:
    print(f"  ⚠️  Skipping HTML copy - no fresh report available")
    reports_copied = []
```

---

### Bug #2: No HTML Data Validation

**Location:** `run_scrpa_pipeline.py`, lines 482-511

**Current Code:**
```python
combined = list(SCRPA_ARCPY_OUTPUT.glob("SCRPA_Combined_Executive_Summary_*.html"))
if combined:
    latest = max(combined, key=lambda p: p.stat().st_mtime)  # Gets latest by time
    dest = reports_dir / "SCRPA_Combined_Executive_Summary.html"
    shutil.copy2(latest, dest)
```

**Bug:** No validation that HTML contains data for correct cycle

**Fix:**
```python
def _find_html_for_cycle(output_dir: Path, cycle_info: Dict[str, Any]) -> Optional[Path]:
    """
    Find HTML file matching the current cycle by parsing content.
    Returns path to matching HTML or None.
    """
    import re
    from datetime import datetime, timedelta
    
    cycle_start = cycle_info.get('start_7')  # e.g., "02/03/2026"
    cycle_end = cycle_info.get('end_7')      # e.g., "02/09/2026"
    
    if not cycle_start or not cycle_end:
        return None
    
    # Parse dates
    try:
        start_date = datetime.strptime(cycle_start, '%m/%d/%Y')
        end_date = datetime.strptime(cycle_end, '%m/%d/%Y')
    except ValueError:
        return None
    
    # Look for HTML files generated within cycle window or shortly after
    tolerance_days = 7
    html_files = list(output_dir.glob("SCRPA_Combined_Executive_Summary_*.html"))
    
    for html_path in sorted(html_files, key=lambda p: p.stat().st_mtime, reverse=True):
        # Check file modification time
        mtime = datetime.fromtimestamp(html_path.stat().st_mtime)
        if start_date - timedelta(days=1) <= mtime <= end_date + timedelta(days=tolerance_days):
            # Quick content check: look for cycle dates in HTML
            try:
                content = html_path.read_text(encoding='utf-8', errors='ignore')
                if cycle_start in content and cycle_end in content:
                    return html_path
            except Exception:
                continue
    
    return None

# Then in _copy_scrpa_reports_to_cycle():
html_file = _find_html_for_cycle(SCRPA_ARCPY_OUTPUT, cycle_info)
if html_file:
    dest = reports_dir / "SCRPA_Combined_Executive_Summary.html"
    shutil.copy2(html_file, dest)
    print(f"  Copied report: {html_file.name} (validated for cycle)")
else:
    print(f"  ⚠️  No HTML report found matching cycle {cycle_info['name']}")
    print(f"  ⚠️  Expected date range: {cycle_info['start_7']} - {cycle_info['end_7']}")
```

---

### Bug #3: Divergent Transformation Logic

**Location:** 
- Python: `scrpa_transform.py`, `build_all_crimes_enhanced()`
- ArcPy: `RMS_Statistical_Export_FINAL_COMPLETE.py`, `_period_bucket()`

**Bug:** Two systems calculate periods differently

**Example Scenario:**
- **Incident Date:** 02/01/2026
- **Report Date:** 02/08/2026
- **Current Cycle:** 26C02W06 (02/03-02/09)

**Python Pipeline Logic:**
```python
# Cycle calendar lookup
7_Day_Start = 02/03/2026
7_Day_End = 02/09/2026

# Period classification
if 7_Day_Start <= Incident_Date <= 7_Day_End:
    Period = "7-Day"
else:
    # Fallback to other periods
```
**Result:** `Period = "Historical"` (incident before cycle start)

**SCRPA_ArcPy Logic:**
```python
# Rolling window
today = date.today()  # 02/10/2026
delta = (today - Incident_Date).days  # 9 days

if delta <= 7:
    return "7-Day"
elif delta <= 28:
    return "28-Day"
```
**Result:** `Period = "28-Day"` (within 28 days of today)

**Impact:** Same incident classified differently in CSV vs HTML!

**Fix:** Unify the logic by making SCRPA_ArcPy use the Python CSV as input:

```python
# Option A: Read Python CSV instead of RMS Excel
def load_enhanced_csv_for_html(csv_path: Path) -> pd.DataFrame:
    """Load pre-enriched CSV from Python pipeline"""
    df = pd.read_csv(csv_path)
    # Period, Crime_Category, etc. already computed
    return df

# Option B: Import Python transformation logic
from scrpa_transform import build_all_crimes_enhanced, load_cycle_calendar
```

---

### Bug #4: Missing Cycle Date Context in SCRPA_ArcPy

**Location:** `RMS_Statistical_Export_FINAL_COMPLETE.py`, lines 86-110

**Current Code:**
```python
def _compute_period_series(incident_date_str: pd.Series, range_end_str: str) -> pd.Series:
    try:
        if range_end_str:
            today = pd.to_datetime(range_end_str).date()
        else:
            today = date.today()  # ⚠️ Fallback to current date
    except Exception:
        today = date.today()
```

**Bug:** `range_end_str` parameter exists but isn't used consistently

**Evidence:**
- Function accepts `range_end_str` parameter
- Falls back to `date.today()` on parse error
- No cycle calendar integration

**Fix:**
```python
def _compute_period_series(incident_date_str: pd.Series, cycle_calendar_path: Path, report_date: str) -> pd.Series:
    """
    Compute period bucket using cycle calendar (consistent with Python pipeline).
    """
    from scrpa_transform import load_cycle_calendar, resolve_cycle
    
    calendar_df = load_cycle_calendar(cycle_calendar_path)
    report_date_obj = datetime.strptime(report_date, '%m/%d/%Y').date()
    cycle = resolve_cycle(calendar_df, report_date_obj)
    
    if cycle is None:
        raise ValueError(f"No cycle found for {report_date}")
    
    start_7 = cycle['7_Day_Start']
    end_7 = cycle['7_Day_End']
    
    def classify_period(incident_date):
        if pd.isna(incident_date):
            return "Historical"
        if start_7 <= incident_date <= end_7:
            return "7-Day"
        # ... rest of period logic
    
    return incident_date_str.map(classify_period)
```

---

## 💡 RECOMMENDATIONS

### 1. **IMMEDIATE FIX (This Cycle):**

**Action:** Manually run SCRPA_ArcPy before re-running pipeline

```powershell
# Step 1: Generate fresh HTML
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator"
$env:REPORT_DATE = "02/10/2026"
python RMS_Statistical_Export_FINAL_COMPLETE.py

# Step 2: Verify HTML was generated
dir "..\06_Output\SCRPA_Combined_Executive_Summary_*.html" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# Step 3: Re-run Python pipeline (will copy fresh HTML)
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA"
.\Run_SCRPA_Pipeline.bat
```

---

### 2. **SHORT-TERM FIX (Next Cycle):**

**Action:** Improve error handling and validation

**Changes to `run_scrpa_pipeline.py`:**

```python
# Add validation function
def _validate_html_for_cycle(html_path: Path, cycle_info: Dict[str, Any]) -> bool:
    """Check if HTML contains correct cycle data."""
    try:
        content = html_path.read_text(encoding='utf-8', errors='ignore')
        start_7 = cycle_info.get('start_7', '')
        end_7 = cycle_info.get('end_7', '')
        return (start_7 in content and end_7 in content)
    except Exception:
        return False

# Modify copy function
def _copy_scrpa_reports_to_cycle(reports_dir: Path, cycle_info: Dict[str, Any]) -> list:
    # ... existing code ...
    if combined:
        latest = max(combined, key=lambda p: p.stat().st_mtime)
        
        # VALIDATE before copying
        if not _validate_html_for_cycle(latest, cycle_info):
            print(f"  ⚠️  WARNING: Latest HTML ({latest.name}) does not match current cycle!")
            print(f"  ⚠️  Expected dates: {cycle_info['start_7']} - {cycle_info['end_7']}")
            print(f"  ⚠️  Skipping HTML copy - manual intervention required")
            return []
        
        dest = reports_dir / "SCRPA_Combined_Executive_Summary.html"
        shutil.copy2(latest, dest)
        # ... rest of code ...
```

---

### 3. **LONG-TERM FIX (Architecture Refactor):**

**Option A: Single Source of Truth - Python-First**

**Changes:**
1. Make SCRPA_ArcPy read `SCRPA_All_Crimes_Enhanced.csv` instead of RMS Excel
2. Remove duplicate transformation logic from SCRPA_ArcPy
3. Use Python's `Period`, `Crime_Category`, `LagDays` directly in HTML generation

**File:** `RMS_Statistical_Export_FINAL_COMPLETE.py`

```python
# NEW: Load from Python CSV instead of RMS Excel
def load_enhanced_csv(csv_path: str) -> pd.DataFrame:
    """Load pre-enriched data from Python pipeline."""
    df = pd.read_csv(csv_path)
    
    # Rename columns to match existing HTML generation logic
    column_map = {
        'Case Number': 'ReportNumber',
        'Incident_Date': 'IncidentDate',
        'Crime_Category': 'CrimeType',
        'Zone': 'Zone',
        'FullAddress': 'Address',
        # ... etc
    }
    df = df.rename(columns=column_map)
    
    # Period already calculated correctly!
    # No need for _period_bucket() or _compute_period_series()
    
    return df

# Modify main() to accept CSV path
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--enhanced-csv', help='Path to SCRPA_All_Crimes_Enhanced.csv')
    parser.add_argument('--rms-xlsx', help='Path to RMS Excel (legacy mode)')
    args = parser.parse_args()
    
    if args.enhanced_csv:
        df = load_enhanced_csv(args.enhanced_csv)
        print(f"✅ Loaded enhanced CSV: {args.enhanced_csv}")
    elif args.rms_xlsx:
        df = load_dataframe_from_xlsx(args.rms_xlsx)
        # ... legacy transformation logic ...
    else:
        # Auto-detect latest CSV from Python pipeline output
        csv_path = find_latest_enhanced_csv()
        df = load_enhanced_csv(csv_path)
```

**Benefits:**
- ✅ Single transformation logic
- ✅ Guaranteed data consistency between CSV and HTML
- ✅ No duplicate period calculation
- ✅ Python pipeline controls all enrichment

---

**Option B: Integrated Pipeline**

**Changes:**
1. Move HTML generation INTO Python pipeline as a native module
2. Deprecate SCRPA_ArcPy as standalone system
3. Generate HTML directly from `SCRPA_All_Crimes_Enhanced.csv`

**New File:** `scripts/generate_html_report.py`

```python
"""
Generate HTML executive summary from enhanced CSV.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, Any

def generate_html_from_csv(
    csv_path: Path,
    cycle_info: Dict[str, Any],
    output_path: Path
) -> Path:
    """
    Generate HTML report directly from enhanced CSV.
    
    Args:
        csv_path: Path to SCRPA_All_Crimes_Enhanced.csv
        cycle_info: Cycle metadata dict
        output_path: Where to save HTML
    
    Returns:
        Path to generated HTML file
    """
    df = pd.read_csv(csv_path)
    
    # Filter by period (Period column already computed!)
    df_7day = df[df['Period'] == '7-Day']
    df_28day = df[df['Period'] == '28-Day']
    df_ytd = df[df['Period'] == 'YTD']
    
    # Calculate stats
    stats_7day = calculate_stats(df_7day)
    stats_28day = calculate_stats(df_28day)
    stats_ytd = calculate_stats(df_ytd)
    
    # Generate HTML using existing CSS/template
    html_content = generate_html_template(
        cycle_info=cycle_info,
        stats_7day=stats_7day,
        stats_28day=stats_28day,
        stats_ytd=stats_ytd
    )
    
    output_path.write_text(html_content, encoding='utf-8')
    print(f"✅ Generated HTML: {output_path}")
    
    return output_path
```

**Integration in `run_scrpa_pipeline.py`:**

```python
# Replace step 6a and 6b:
print(f"\n[6/6] Generating HTML report from CSV...")
from generate_html_report import generate_html_from_csv

html_path = paths['reports'] / 'SCRPA_Combined_Executive_Summary.html'
generate_html_from_csv(
    csv_path=enhanced_csv,
    cycle_info=cycle_info,
    output_path=html_path
)
results['files_created'].append(str(html_path))
```

**Benefits:**
- ✅ No subprocess calls
- ✅ No stale HTML copying
- ✅ Guaranteed data consistency
- ✅ Single codebase to maintain
- ✅ Simpler debugging

---

### 4. **TESTING STRATEGY:**

**Test Case 1: Data Consistency Validation**

```python
"""
Test: Verify CSV data matches HTML data.
"""
def test_csv_html_consistency(cycle_dir: Path):
    csv_path = cycle_dir / 'Data' / 'SCRPA_All_Crimes_Enhanced.csv'
    html_path = cycle_dir / 'Reports' / 'SCRPA_Combined_Executive_Summary.html'
    
    # Load CSV
    df = pd.read_csv(csv_path)
    df_7day = df[df['Period'] == '7-Day']
    
    # Parse HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract counts from HTML
    import re
    match = re.search(r'7-Day.*?<strong>(\d+) incidents</strong>', html_content, re.DOTALL)
    html_7day_count = int(match.group(1)) if match else None
    
    # Compare
    csv_7day_count = len(df_7day)
    
    assert html_7day_count == csv_7day_count, (
        f"7-Day count mismatch: CSV={csv_7day_count}, HTML={html_7day_count}"
    )
    print(f"✅ Data consistency validated: 7-Day count = {csv_7day_count}")
```

**Test Case 2: HTML Generation Integration Test**

```python
"""
Test: Full pipeline run with HTML validation.
"""
def test_full_pipeline_with_html(rms_path: Path, report_date: str):
    # Run pipeline
    results = run_pipeline(
        rms_path=rms_path,
        report_due_date=datetime.strptime(report_date, '%m/%d/%Y').date(),
        output_dir=None  # Auto-generate
    )
    
    assert results['success'], f"Pipeline failed: {results.get('error')}"
    
    # Verify HTML exists
    html_path = Path(results['output_dir']) / 'Reports' / 'SCRPA_Combined_Executive_Summary.html'
    assert html_path.exists(), f"HTML not generated: {html_path}"
    
    # Verify HTML contains correct cycle
    html_content = html_path.read_text(encoding='utf-8')
    assert results['cycle_info']['start_7'] in html_content
    assert results['cycle_info']['end_7'] in html_content
    
    print(f"✅ Full pipeline test passed for {report_date}")
```

---

## 📋 SUMMARY

### Root Cause
The Python pipeline **assumes fresh HTML exists** but doesn't reliably generate it, leading to stale HTML being copied with only headers patched.

### Contributing Factors
1. **Silent failure** - HTML generation errors don't stop the pipeline
2. **No validation** - No check that HTML matches current cycle
3. **Dual transformation** - Two systems calculate periods differently
4. **Weak integration** - Subprocess call without error handling

### Immediate Impact
- ❌ HTML reports show **wrong data** (previous cycle's incidents)
- ✅ CSV/JSON outputs are **correct** (current cycle)
- ⚠️ **Inconsistent reporting** across formats

### Recommended Solution
**Option A (Quick):** Improve validation and error handling  
**Option B (Robust):** Make SCRPA_ArcPy read Python CSV (single source of truth)  
**Option C (Optimal):** Integrate HTML generation into Python pipeline

### Files Requiring Changes
1. `scripts/run_scrpa_pipeline.py` - Error handling, validation
2. `05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py` - Accept CSV input
3. `scripts/generate_html_report.py` - NEW module for HTML generation (Option C)

---

## 🔧 PROPOSED CODE FIXES

See attached patch files:
- `PATCH_001_error_handling.py` - Improve HTML generation error handling
- `PATCH_002_validation.py` - Add HTML/CSV data validation
- `PATCH_003_unified_transform.py` - Use Python CSV in SCRPA_ArcPy
- `PATCH_004_integrated_html.py` - Native HTML generation in Python pipeline

---

**End of Code Review Analysis**  
**Next Steps:** Review recommendations with project owner and select implementation approach.
