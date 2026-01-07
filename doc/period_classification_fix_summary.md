// 2025-12-29-19-40-00
# SCRPA_Time_v3/period_classification_fix_summary.md
# Author: R. A. Carucci
# Purpose: Executive summary and action plan for correcting 7-Day period classification in SCRPA reporting

# 7-Day Period Classification Fix - Executive Summary

## 🔴 **Critical Issue Identified**

**Report:** C13W51 (12/23/25 - 12/29/25, Due 12/30/25)  
**Chart:** Burglary - Commercial | Residence  
**Problem:** Chart shows **2 incidents** in 7-Day period when it should show **0 incidents**

---

## 📊 **Root Cause Analysis**

### What We Found:

| Case Number | Incident Date | Report Date | Lag Days | Category | Current Chart | Should Be |
|------------|--------------|-------------|----------|----------|---------------|-----------|
| 25-111319 | 12/21/25 | 12/23/25 | 2 | Burglary-Auto | ✅ Shows in 7-Day | ❌ Lagday ONLY |
| 25-113076 | 12/20/25 | 12/28/25 | 8 | Burglary-Residence | ✅ Shows in 7-Day | ❌ Lagday ONLY |

### The Logic Flaw:

**Current M Code:**
```
Period = based on Report_Date proximity to "Today"
    if Report_Date within last 7 days → "7-Day"
```

**Problem:**
- Includes BACKFILL cases (incident before cycle, reported during cycle)
- Conflates **reporting delays** with **actual crime occurrence**
- Distorts tactical analysis (charts should show when crimes occurred, not when they were reported)

**Correct Logic:**
```
Period = based on Incident_Date within cycle boundaries
    if Incident_Date within (12/23/25 - 12/29/25) → "7-Day"
```

---

## ✅ **Solution Provided**

### 1. **M Code Fix** (`m_code_period_fix.txt`)
   - Replaces Report_Date-based period calculation with Incident_Date-based logic
   - Uses actual cycle boundaries from cycle calendar
   - Preserves existing Backfill_7Day flag (already correct)
   - Adds optional validation column for QA

### 2. **Python Validation Script** (`validate_7day_backfill.py`)
   - Analyzes RMS export to categorize incidents as:
     * **IN_CYCLE**: Occurred during cycle (should appear in charts)
     * **BACKFILL**: Occurred before cycle, reported during (lagday table only)
     * **OUTSIDE_CYCLE**: Not relevant to current report
   - Generates detailed reports by crime category
   - Exports validation CSV for further analysis

### 3. **Verification Process:**
   ```bash
   python validate_7day_backfill.py 2025_12_29_18_46_24_SCRPA_RMS.csv 2025-12-23 2025-12-29
   ```

---

## 📋 **Implementation Steps**

### **Immediate Actions (Before 12/30/25 Report):**

1. **Backup Current Power BI File**
   - Save copy of current .pbix file
   - Document current chart values for comparison

2. **Apply M Code Fix**
   - Open Power BI Desktop
   - Navigate to Power Query Editor
   - Locate "Period_Added" step in your main query
   - Replace with corrected logic from `m_code_period_fix.txt`
   - Verify no syntax errors

3. **Run Validation Script**
   ```bash
   cd C:\Users\carucci_r\OneDrive - City of Hackensack\01_DataSources\SCRPA_Time_v2
   python validate_7day_backfill.py 2025_12_29_18_46_24_SCRPA_RMS.csv 2025-12-23 2025-12-29
   ```

4. **Verify Power BI Results Match Validation**
   - Refresh Power BI data
   - Check Burglary chart: should show **0** in 7-Day period (not 2)
   - Check lagday table: should show **2** burglary cases
   - Verify counts for all crime categories match validation script

5. **Document Changes**
   - Note discrepancies between old/new counts
   - Add footnote to report explaining correction methodology
   - Archive validation output for audit trail

### **Ongoing Actions:**

6. **Add Pre-Report Validation to Workflow**
   - Run validation script before each weekly report
   - Compare Power BI counts with validation output
   - Flag any discrepancies for investigation

7. **Update Documentation**
   - Add validation step to SCRPA_quickstart_guide.md
   - Document Period vs Backfill logic in system documentation
   - Create troubleshooting guide for count discrepancies

---

## 🎯 **Expected Results After Fix**

### C13W51 Burglary Counts:

| Metric | Before Fix | After Fix | Explanation |
|--------|-----------|-----------|-------------|
| 7-Day Chart | 2 incidents | **0 incidents** | Removed backfill cases |
| Lagday Table | ? | **2 incidents** | Both cases are backfill |
| YTD Total | Same | Same | No change (all incidents still counted) |

### Chart Interpretation Changes:

**Before Fix:**
- 7-Day chart mixed occurrence timing with reporting delays
- Unable to identify true crime patterns vs administrative lag
- Potentially inflated current period counts

**After Fix:**
- 7-Day chart shows only crimes that **occurred** during cycle
- Clear separation between tactical analysis (charts) and reporting metrics (lagday table)
- Accurate trend identification for crime prevention strategies

---

## 🔍 **Impact Assessment**

### **Reports Affected:**
- ✅ 7-Day charts (all crime categories)
- ✅ 28-Day charts (if using same logic)
- ❌ Lagday tables (no change - already correct)
- ❌ YTD totals (no change - all incidents still counted)

### **Historical Data:**
- Previous reports may have inflated 7-Day counts due to backfill inclusion
- Recommend re-running validation for last 4-6 weeks to quantify impact
- Consider footnote in next report acknowledging methodology improvement

### **Stakeholder Communication:**

**For Command Staff:**
> "We identified and corrected a period classification issue in the SCRPA system. 
> The 7-Day charts now accurately show crimes that occurred during the reporting 
> period, with delayed reports tracked separately in the lagday table. This 
> provides clearer tactical intelligence for crime reduction strategies."

**Technical Details (If Requested):**
> "Period assignment was previously based on Report_Date proximity to 'Today', 
> which incorrectly included backfilled cases. We've implemented cycle-boundary 
> logic using Incident_Date to ensure charts reflect actual crime occurrence 
> patterns rather than reporting delays."

---

## 🛡️ **Quality Assurance Checklist**

Before finalizing each weekly report:

- [ ] Run validation script on RMS export
- [ ] Verify Power BI Period counts match validation IN_CYCLE counts
- [ ] Verify Power BI Backfill_7Day counts match validation BACKFILL counts
- [ ] Check for any "⚠️ ERROR" entries in Period_Validation column
- [ ] Confirm lagday table shows all backfill cases
- [ ] Review any discrepancies > 10% from validation output

---

## 📁 **Deliverables Provided**

1. **validate_7day_backfill.py** - Validation script for data consistency checking
2. **m_code_period_fix.txt** - Corrected M Code for Period classification
3. **period_classification_fix_summary.md** - This document (implementation guide)

---

## 🔄 **Next Steps (Post-Implementation)**

1. **Monitor for 2-3 Cycles:**
   - Track validation results
   - Document any edge cases
   - Refine logic if needed

2. **Expand Validation Coverage:**
   - Add checks for other data quality metrics
   - Integrate with automated workflow
   - Create dashboard for ongoing monitoring

3. **System Improvements:**
   - Consider adding Period_Validation column permanently for QA
   - Implement automated alerts for count discrepancies
   - Develop comprehensive test suite for M Code changes

4. **Training Update:**
   - Brief command staff on new methodology
   - Update analyst documentation
   - Create reference guide for interpreting lagday data

---

## 📞 **Support & Questions**

For questions or issues during implementation:
- Review detailed comments in `m_code_period_fix.txt`
- Run validation script with sample data to verify expected behavior
- Check Power BI Advanced Editor for syntax errors after applying fix
- Compare validation output with Power BI visual counts to identify discrepancies

---

**Last Updated:** 2025-12-29 19:40:00 EST  
**Next Review:** After C13W52 implementation (2025-01-06)
