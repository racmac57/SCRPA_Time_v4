# CODE REVIEW DELIVERABLES - SCRPA HTML Data Mismatch

**Review Date:** 2026-02-10  
**Reviewer:** AI Code Review Agent  
**Issue:** HTML report data mismatch (cycle 26C02W06 showing 26BW03 data)  
**Status:** ✅ Complete - Root cause identified, solutions proposed

---

## 📋 DOCUMENTS CREATED

### 1. **Executive Summary** (THIS DOCUMENT)
**File:** `doc/EXECUTIVE_SUMMARY_HTML_MISMATCH.md`  
**Purpose:** High-level overview for decision-makers  
**Contents:**
- Problem statement
- Root cause explanation
- 4 solution options with pros/cons
- Comparison matrix
- Recommended path forward

**Target Audience:** Project owner, management

---

### 2. **Detailed Technical Analysis**
**File:** `doc/CODE_REVIEW_ANALYSIS_HTML_MISMATCH.md`  
**Purpose:** In-depth code review for developers  
**Contents:**
- System architecture analysis
- Data flow examination
- 4 critical bugs identified with exact code locations
- Function-by-function analysis
- Proposed code fixes with examples
- Testing strategy

**Target Audience:** Developers, technical reviewers

**Key Findings:**
- Bug #1: Silent HTML generation failure (lines 843-853)
- Bug #2: No data validation before copying (lines 496-509)
- Bug #3: Header-only patching (lines 392-454)
- Bug #4: Divergent period calculation logic

---

### 3. **Data Flow Diagrams**
**File:** `doc/DATA_FLOW_DIAGRAMS.md`  
**Purpose:** Visual representation of system architecture  
**Contents:**
- Current broken architecture (ASCII diagram)
- Proposed fix Option 3 (Single source of truth)
- Proposed fix Option 4 (Integrated HTML)
- Timeline comparison
- Validation flow diagrams
- Error scenario flows

**Target Audience:** All stakeholders (visual reference)

---

### 4. **Root Cause Document** (Pre-existing, Referenced)
**File:** `doc/ROOT_CAUSE_HTML_MISMATCH.md`  
**Purpose:** Original investigation findings  
**Contents:**
- Initial problem discovery
- System comparison
- Manual fix instructions

**Status:** Referenced but not modified by this review

---

## 🔍 KEY FINDINGS SUMMARY

### Root Cause
The Python pipeline **copies stale HTML** from `SCRPA_ArcPy/06_Output/` without validating it matches the current cycle. HTML generation is a **separate system** that must be manually run.

### Critical Issues
1. **Silent failure:** HTML generation errors don't stop pipeline
2. **No validation:** Pipeline copies "latest" file by timestamp without checking cycle
3. **Dual transformation:** Two systems calculate periods differently
4. **Header-only patch:** Only cycle name/dates updated, not data tables

### Impact
- ❌ Executive reports contain **incorrect incident data**
- ✅ CSV/JSON outputs are correct
- ⚠️ **Inconsistent reporting** across formats

---

## 💡 SOLUTION OPTIONS

### Option 1: Manual Run (IMMEDIATE)
- **Effort:** Low
- **When:** This cycle (today)
- **How:** Run SCRPA_ArcPy manually before pipeline
- **Pros:** Immediate fix
- **Cons:** Manual process, doesn't prevent recurrence

### Option 2: Add Validation (SHORT-TERM)
- **Effort:** Low
- **When:** Next cycle
- **How:** Validate HTML cycle dates before copying
- **Pros:** Prevents wrong data, alerts user
- **Cons:** Still requires manual SCRPA_ArcPy run

### Option 3: Single Source of Truth (RECOMMENDED)
- **Effort:** Medium
- **When:** 1-2 cycles
- **How:** Make SCRPA_ArcPy read Python CSV instead of RMS
- **Pros:** Guaranteed consistency, automated
- **Cons:** Requires SCRPA_ArcPy refactoring

### Option 4: Integrated HTML (OPTIMAL)
- **Effort:** High
- **When:** 2-3 cycles
- **How:** Move HTML generation into Python pipeline
- **Pros:** Single codebase, simplest architecture
- **Cons:** Most development work

---

## 📊 CODE LOCATIONS

### Files Requiring Changes (Option 3)

**Primary:**
1. `scripts/run_scrpa_pipeline.py`
   - Lines 150-210: `_generate_html_report_via_arcpy()` - Improve error handling
   - Lines 482-511: `_copy_scrpa_reports_to_cycle()` - Add validation
   - Lines 843-853: Pipeline flow - Fail fast on HTML error

2. `02_ETL_Scripts/SCRPA_ArcPy/05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py`
   - Add CSV input mode
   - Accept `--enhanced-csv` parameter
   - Use Python's Period/Crime_Category directly

**Supporting:**
3. `scripts/scrpa_transform.py` (No changes - already correct)
4. `scripts/prepare_7day_outputs.py` (No changes - already correct)

### Files Requiring Changes (Option 4)

**New File:**
1. `scripts/generate_html_report.py` (NEW)
   - Function: `generate_html_from_csv()`
   - Reads enhanced CSV
   - Generates HTML with embedded data
   - Uses Python CSS template

**Modified:**
2. `scripts/run_scrpa_pipeline.py`
   - Remove SCRPA_ArcPy subprocess call
   - Add native HTML generation step
   - Remove HTML copying logic

---

## 🎯 RECOMMENDED IMPLEMENTATION PLAN

### Phase 1: Immediate (Today)
**Goal:** Fix current cycle 26C02W06

1. ✅ Run SCRPA_ArcPy manually:
   ```powershell
   cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator"
   $env:REPORT_DATE = "02/10/2026"
   python RMS_Statistical_Export_FINAL_COMPLETE.py
   ```

2. ✅ Verify HTML generation:
   ```powershell
   dir "..\06_Output\SCRPA_Combined_Executive_Summary_*.html" | 
     Sort-Object LastWriteTime -Descending | 
     Select-Object -First 1
   ```

3. ✅ Re-run Python pipeline:
   ```powershell
   cd "C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA"
   .\Run_SCRPA_Pipeline.bat
   ```

4. ✅ Validate results:
   - Check CSV: `Data/SCRPA_All_Crimes_Enhanced.csv` (2 rows for 7-Day)
   - Check HTML: `Reports/SCRPA_Combined_Executive_Summary.html` (2 incidents for 7-Day)
   - Verify counts match

---

### Phase 2: Short-term (Next Cycle)
**Goal:** Prevent recurrence with validation

1. Implement validation function:
   ```python
   def _validate_html_for_cycle(html_path, cycle_info):
       """Check if HTML contains correct cycle dates."""
       content = html_path.read_text(encoding='utf-8')
       return (cycle_info['start_7'] in content and 
               cycle_info['end_7'] in content)
   ```

2. Add validation before copying:
   ```python
   if not _validate_html_for_cycle(latest, cycle_info):
       raise ValueError("HTML does not match current cycle")
   ```

3. Test with next cycle (26C02W07 on 02/17/2026)

---

### Phase 3: Long-term (1-2 Cycles)
**Goal:** Architectural fix for guaranteed consistency

**Decision Point:** Choose Option 3 or Option 4

**If Option 3 (CSV Input):**

1. Add CSV input mode to SCRPA_ArcPy:
   ```python
   parser.add_argument('--enhanced-csv', 
                       help='Path to SCRPA_All_Crimes_Enhanced.csv')
   
   if args.enhanced_csv:
       df = pd.read_csv(args.enhanced_csv)
       # Period, Crime_Category already calculated!
   else:
       # Legacy RMS Excel mode
   ```

2. Update pipeline to pass CSV:
   ```python
   result = subprocess.run([
       sys.executable, 
       str(SCRPA_ARCPY_SCRIPT),
       '--enhanced-csv', str(enhanced_csv)
   ])
   ```

3. Test with non-production cycle first
4. Deploy to production

**If Option 4 (Integrated HTML):**

1. Create `scripts/generate_html_report.py`
2. Port HTML generation logic from SCRPA_ArcPy
3. Integrate into pipeline (replace step 6)
4. Test with non-production cycle
5. Deprecate SCRPA_ArcPy for HTML generation

---

## 🧪 TESTING CHECKLIST

### Unit Tests
- [ ] Test `_validate_html_for_cycle()` with matching/non-matching HTML
- [ ] Test HTML generation with various cycle dates
- [ ] Test period classification consistency (CSV vs HTML)

### Integration Tests
- [ ] Run full pipeline with test RMS data
- [ ] Verify CSV/JSON/HTML all contain same incident counts
- [ ] Test with edge cases (lag incidents, backfill, etc.)

### Regression Tests
- [ ] Compare new HTML output against known-good output
- [ ] Verify all existing features still work
- [ ] Test with historical cycle dates

### Validation Tests
- [ ] Test with current cycle (02/10/2026)
- [ ] Test with future cycle (02/17/2026)
- [ ] Test with past cycle (01/27/2026)

---

## 📈 SUCCESS METRICS

### Immediate (Phase 1)
- ✅ HTML report contains correct 02/10 data
- ✅ Incident counts match CSV
- ✅ No manual corrections needed

### Short-term (Phase 2)
- ✅ Pipeline fails fast if HTML wrong
- ✅ Clear error messages guide manual fix
- ✅ No silent data mismatches

### Long-term (Phase 3)
- ✅ Single pipeline run generates all outputs
- ✅ Automated consistency validation
- ✅ Zero manual intervention required
- ✅ CSV/JSON/HTML always match

---

## 🔗 DEPENDENCIES

### Python Packages (Current)
- pandas
- openpyxl (Excel reading)
- datetime (stdlib)
- pathlib (stdlib)

### Python Packages (If Option 4)
- Add: jinja2 (for HTML templating - recommended)
- Or: Use f-strings (current approach - no new dependencies)

### External Systems
- **SCRPA_ArcPy:** Currently required, may be deprecated in Option 4
- **Cycle Calendar:** `09_Reference/Temporal/SCRPA_Cycle/7Day_28Day_Cycle_*.csv`
- **RMS Exports:** `05_EXPORTS\_RMS\scrpa\*.xlsx`

---

## 📞 NEXT STEPS

### For Project Owner
1. **Review** this document and technical analysis
2. **Choose** preferred solution approach (Option 3 or 4)
3. **Approve** Phase 1 immediate fix
4. **Schedule** Phase 2/3 implementation

### For Development Team
1. **Execute** Phase 1 manual fix (today)
2. **Implement** Phase 2 validation (next sprint)
3. **Design** Phase 3 architecture (chosen option)
4. **Test** thoroughly before production deployment

---

## 📚 ADDITIONAL RESOURCES

### Documentation Files
- `doc/CODE_REVIEW_ANALYSIS_HTML_MISMATCH.md` - Full technical analysis
- `doc/DATA_FLOW_DIAGRAMS.md` - Visual architecture diagrams
- `doc/ROOT_CAUSE_HTML_MISMATCH.md` - Original investigation
- `doc/HTML_DATA_MISMATCH_ANALYSIS_v2.md` - Earlier analysis

### Code Files
- `scripts/run_scrpa_pipeline.py` - Main orchestrator
- `scripts/scrpa_transform.py` - Data transformation
- `scripts/prepare_7day_outputs.py` - 7-day filtering
- `02_ETL_Scripts/SCRPA_ArcPy/05_orchestrator/RMS_Statistical_Export_FINAL_COMPLETE.py` - HTML generator

### Test Data
- `verify_fix.py` - Validation script (exists in workspace)
- Sample RMS exports in `05_EXPORTS\_RMS\scrpa\`

---

## ✅ DELIVERABLES CHECKLIST

### Documentation
- [x] Executive summary created
- [x] Technical analysis completed
- [x] Data flow diagrams created
- [x] Implementation plan drafted
- [x] Testing checklist provided

### Code Analysis
- [x] Root cause identified
- [x] Bugs located and documented
- [x] Solution options proposed
- [x] Code examples provided

### Recommendations
- [x] Immediate fix steps
- [x] Short-term validation approach
- [x] Long-term architecture options
- [x] Testing strategy

---

## 🎉 CONCLUSION

**Root Cause:** Identified and documented  
**Solutions:** 4 options proposed with clear trade-offs  
**Risk:** Mitigated with validation and testing plan  
**Recommendation:** Implement Phase 1 immediately, Phase 2 next cycle, Phase 3 (Option 3 or 4) within 1-2 cycles

**Estimated Effort:**
- Phase 1 (Manual fix): 30 minutes
- Phase 2 (Validation): 4-8 hours development + testing
- Phase 3 Option 3 (CSV input): 16-24 hours development + testing
- Phase 3 Option 4 (Integrated): 24-40 hours development + testing

**Questions?** Refer to the detailed technical analysis or contact the review team.

---

**End of Code Review Deliverables**
