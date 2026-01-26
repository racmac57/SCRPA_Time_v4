# Bi-Weekly Reporting Cycle Setup Guide

**Date Created**: 2026-01-26  
**Last Report Submitted**: 2026-01-13  
**Next Report Due**: 2026-01-27  
**Change**: Weekly → Bi-Weekly Reporting

---

## Executive Summary

The reporting frequency is changing from **weekly** to **bi-weekly** (every 2 weeks). The analysis periods (7-day and 28-day windows) remain the same - only the submission frequency changes.

---

## What Stays the Same ✅

### 7_Day_Start, 7_Day_End, 28_Day_Start, 28_Day_End Columns

**These columns DO NOT need to change.** They represent:
- **7-Day Window**: The rolling 7-day analysis period (e.g., 01/20/26 to 01/26/26)
- **28-Day Window**: The rolling 28-day analysis period (e.g., 12/30/25 to 01/26/26)

These are **analysis periods**, not reporting frequency. The system will continue to analyze data in 7-day and 28-day windows regardless of how often reports are submitted.

**Example for 01/27/2026 report:**
- `7_Day_Start`: 01/20/26
- `7_Day_End`: 01/26/26
- `28_Day_Start`: 12/30/25
- `28_Day_End`: 01/26/26

These date ranges are correct and should remain as-is.

---

## What Needs to Change 🔄

### 1. Cycle Calendar CSV File

**File**: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\26_scrpa_cycle.txt`

**Current Structure:**
```
Report_Due_Date,7_Day_Start,7_Day_End,28_Day_Start,28_Day_End,Report_Name
01/06/26,12/30/25,01/05/26,12/09/25,01/05/26,C01W01
01/13/26,01/06/26,01/12/26,12/16/25,01/12/26,C01W02
01/20/26,01/13/26,01/19/26,12/23/25,01/19/26,C01W03
01/27/26,01/20/26,01/26/26,12/30/25,01/26/26,C01W04
```

**Changes Needed:**

#### A. Add Bi-Weekly Report Name Column (Optional but Recommended)

You can add a new column for bi-weekly naming, or modify the existing `Report_Name` column:

**Option 1: Add New Column**
```
Report_Due_Date,7_Day_Start,7_Day_End,28_Day_Start,28_Day_End,Report_Name,BiWeekly_Report_Name
01/13/26,01/06/26,01/12/26,12/16/25,01/12/26,C01W02,26BW01
01/27/26,01/20/26,01/26/26,12/30/25,01/26/26,C01W04,26BW02
```

**Option 2: Update Report_Name Column**
Change `Report_Name` to reflect bi-weekly cycles:
- `26BW01` = 2026 Bi-Weekly Report 01
- `26BW02` = 2026 Bi-Weekly Report 02
- etc.

**Recommended Naming Convention:**
- Format: `YYBW##` (Year + Bi-Weekly + Number)
- Example: `26BW01`, `26BW02`, `26BW03`...`26BW26` (26 bi-weekly reports per year)

#### B. Filter to Bi-Weekly Report Dates Only

Keep only the rows where reports will be submitted (every 2 weeks):

**Keep these dates:**
- 01/13/26 ✅ (last submitted)
- 01/27/26 ✅ (next due)
- 02/10/26
- 02/24/26
- 03/10/26
- etc.

**Remove these dates:**
- 01/06/26 ❌ (skip - between 01/13 and 01/27)
- 01/20/26 ❌ (skip - between 01/13 and 01/27)
- 02/03/26 ❌ (skip - between 01/27 and 02/10)
- etc.

**Note**: You can keep all rows in the file for reference, but ensure scripts only use bi-weekly dates when looking up cycles.

---

### 2. M Code Query Updates

**File**: `m_code/q_CycleCalendar.m`

**Current Code:**
```m
CycleCalendarTyped = Table.TransformColumnTypes(
    CycleCalendarTable0, {{"Report_Due_Date", type date},
                          {"7_Day_Start", type date},
                          {"7_Day_End", type date},
                          {"28_Day_Start", type date},
                          {"28_Day_End", type date},
                          {"Report_Name", type text}}),
```

**If you add BiWeekly_Report_Name column:**
```m
CycleCalendarTyped = Table.TransformColumnTypes(
    CycleCalendarTable0, {{"Report_Due_Date", type date},
                          {"7_Day_Start", type date},
                          {"7_Day_End", type date},
                          {"28_Day_Start", type date},
                          {"28_Day_End", type date},
                          {"Report_Name", type text},
                          {"BiWeekly_Report_Name", type text}}),
```

**No other changes needed** - the date range columns work the same way.

---

### 3. Folder Naming Script Updates

**Script**: `generate_weekly_report.py` (may need renaming to `generate_report.py`)

**Current Naming Pattern**: `YYCMMWww_YY_MM_DD`
- Example: `26C01W02_26_01_13`

**For Bi-Weekly, Suggested Pattern**: `YYBW##_YY_MM_DD`
- Example: `26BW01_26_01_13` (2026 Bi-Weekly 01, submitted 01/13/26)
- Example: `26BW02_26_01_27` (2026 Bi-Weekly 02, submitted 01/27/26)

**Alternative Pattern**: `YYCMMBW##_YY_MM_DD`
- Example: `26C01BW01_26_01_13` (2026 Calendar Month 01, Bi-Weekly 01)

**Action Required:**
1. Locate `generate_weekly_report.py` script
2. Update folder naming logic to use bi-weekly cycle numbers
3. Consider renaming script to `generate_report.py` or `generate_biweekly_report.py`

---

### 4. Power BI Visual Updates

**Check for these items in Power BI:**

#### A. Visual Titles and Labels
- Look for any visuals that say "Weekly Report" or "Week"
- Update to "Bi-Weekly Report" or "Bi-Week" as appropriate
- Examples:
  - "Weekly Crime Summary" → "Bi-Weekly Crime Summary"
  - "This Week" → "This Bi-Week" or "Current Period"

#### B. Cycle Name Display
- If visuals display `Report_Name` from the cycle calendar, they will automatically show the new bi-weekly names once the CSV is updated
- No code changes needed if using the `Report_Name` column directly

#### C. Date Range Labels
- Check if any visuals have hardcoded text like "Week of..." or "Weekly Period"
- Update to "Bi-Weekly Period" or "Reporting Period"

#### D. Measures and Calculations
- **No changes needed** - all date range calculations use `7_Day_Start`, `7_Day_End`, `28_Day_Start`, `28_Day_End` which remain the same
- Period classification logic (7-Day, 28-Day, YTD, Prior Year) remains unchanged

**Action Required:**
1. Open Power BI template: `C:\Users\carucci_r\OneDrive - City of Hackensack\15_Templates\Base_Report.pbix`
2. Review all page titles, visual titles, and text boxes
3. Update any "weekly" terminology to "bi-weekly" or "reporting period"
4. Save updated template

---

### 5. Documentation Updates

**Files to Update:**

1. **README.md**
   - Change "weekly" to "bi-weekly" in descriptions
   - Update naming convention examples

2. **CHANGELOG.md**
   - Add entry for bi-weekly transition
   - Document date of change (2026-01-27)

3. **SUMMARY.md**
   - Update system description from "weekly" to "bi-weekly"

4. **Script Comments**
   - Update `generate_weekly_report.py` comments if script is not renamed

---

## Implementation Checklist

### Phase 1: Cycle Calendar Update
- [ ] Update cycle calendar CSV with bi-weekly report dates only
- [ ] Add or update `Report_Name` column with bi-weekly naming (e.g., `26BW01`, `26BW02`)
- [ ] Verify date ranges (7_Day_Start, 7_Day_End, 28_Day_Start, 28_Day_End) are correct for each bi-weekly cycle
- [ ] Test cycle lookup with report date 01/27/26

### Phase 2: M Code Updates
- [ ] Update `q_CycleCalendar.m` if new column added (BiWeekly_Report_Name)
- [ ] Test cycle calendar loads correctly in Power BI
- [ ] Verify current cycle detection works for bi-weekly dates

### Phase 3: Script Updates
- [ ] Locate and review `generate_weekly_report.py`
- [ ] Update folder naming logic for bi-weekly format
- [ ] Test folder creation with bi-weekly naming
- [ ] Consider renaming script file

### Phase 4: Power BI Template Updates
- [ ] Open `Base_Report.pbix` template
- [ ] Review all page titles and visual titles
- [ ] Update "weekly" terminology to "bi-weekly" or "reporting period"
- [ ] Verify cycle name displays correctly
- [ ] Save updated template

### Phase 5: Documentation
- [ ] Update README.md
- [ ] Update CHANGELOG.md
- [ ] Update SUMMARY.md
- [ ] Update any workflow documentation

### Phase 6: Testing
- [ ] Test complete workflow with 01/27/26 report date
- [ ] Verify folder naming is correct
- [ ] Verify Power BI loads correct cycle
- [ ] Verify all visuals display correctly
- [ ] Verify email template generation works

---

## Example: Updated Cycle Calendar Entry

For the 01/27/2026 report:

```
Report_Due_Date,7_Day_Start,7_Day_End,28_Day_Start,28_Day_End,Report_Name,BiWeekly_Report_Name
01/27/26,01/20/26,01/26/26,12/30/25,01/26/26,C01W04,26BW02
```

**Explanation:**
- `Report_Due_Date`: 01/27/26 (when report is submitted)
- `7_Day_Start`: 01/20/26 (7-day analysis window start)
- `7_Day_End`: 01/26/26 (7-day analysis window end)
- `28_Day_Start`: 12/30/25 (28-day analysis window start)
- `28_Day_End`: 01/26/26 (28-day analysis window end)
- `Report_Name`: C01W04 (original weekly name - kept for reference)
- `BiWeekly_Report_Name`: 26BW02 (new bi-weekly name)

---

## Key Points to Remember

1. **7-Day and 28-Day windows stay the same** - these are analysis periods, not reporting frequency
2. **Only Report_Due_Date frequency changes** - from weekly to bi-weekly
3. **Report_Name needs new format** - to reflect bi-weekly cycles
4. **Folder naming needs update** - to match bi-weekly naming convention
5. **Power BI visuals may need terminology updates** - change "weekly" to "bi-weekly"
6. **All date calculations remain the same** - no logic changes needed

---

## Questions to Clarify

1. **Naming Convention Preference**: Do you prefer `26BW01` or `26C01BW01` format?
2. **Keep Weekly Rows**: Should weekly cycle rows remain in CSV for reference, or be removed?
3. **Script Renaming**: Should `generate_weekly_report.py` be renamed to `generate_biweekly_report.py`?
4. **Backward Compatibility**: Do you need to maintain compatibility with existing weekly report folders?

---

## Support

For questions or issues during the transition:
1. Check this document first
2. Review cycle calendar CSV structure
3. Test with a single report date before full rollout
4. Verify Power BI template updates before next report

---

**Last Updated**: 2026-01-26  
**Prepared By**: AI Assistant  
**Next Review**: After 01/27/2026 report submission
