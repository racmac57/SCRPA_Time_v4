# Pre-Save Checklist - Power BI Template

**Date**: 2026-01-26  
**Before Saving**: `15_Templates\Base_Report.pbix`

---

## ✅ Critical: Must Verify Before Saving

### 1. Query Refresh Test
- [ ] **Refresh `q_CycleCalendar`**
  - Right-click → **Refresh Preview**
  - Should complete without errors
  - Verify `BiWeekly_Report_Name` column appears
  - Check that 2026 rows show values (26BW01, 26BW02, etc.)
  - 2025 rows showing null is **expected and correct**

- [ ] **Refresh `all_crimes` query**
  - Should complete without errors
  - Verify no errors in query dependencies

### 2. Cycle Detection Test
- [ ] **Verify Current Cycle Detection**
  - Check that current cycle is detected correctly
  - For today (01/26/26), it should find cycle ending 01/26/26
  - For tomorrow (01/27/26), it should find cycle with Report_Due_Date = 01/27/26 (26BW02)

### 3. Data Preview Check
- [ ] **Check Period Classification**
  - Verify 7-Day, 28-Day, YTD, Prior Year classifications still work
  - Spot-check a few rows to ensure Period values are correct

---

## ⚠️ Recommended: Visual Terminology Check

### Quick Visual Review (5-10 minutes)

**Check these areas in Power BI:**

1. **Page Titles**
   - [ ] Look for "Weekly Report" → Change to "Bi-Weekly Report" or "Reporting Period"
   - [ ] Look for "Week" → Change to "Bi-Week" or "Period" as appropriate

2. **Visual Titles**
   - [ ] Check chart/table titles for "Weekly" terminology
   - [ ] Update to "Bi-Weekly" or "Reporting Period"

3. **Text Boxes**
   - [ ] Look for hardcoded text like "Week of..." or "Weekly Period"
   - [ ] Update to "Bi-Weekly Period" or "Reporting Period"

4. **Tooltips/Descriptions**
   - [ ] Check any tooltips or descriptions that mention "weekly"
   - [ ] Update as needed

**Note**: This is **optional but recommended**. You can do this now or later - the template will work either way, but updating terminology makes it clearer for users.

---

## ❌ Not Required Before Saving

These can be done later:

- [ ] Script updates (folder naming) - Can wait until next report
- [ ] Documentation updates (README, CHANGELOG) - Can do anytime
- [ ] Template file renaming - Not critical

---

## Quick Test Procedure

### Test 1: Query Load
1. Open Power Query Editor
2. Refresh `q_CycleCalendar` → Should work ✅
3. Refresh `all_crimes` → Should work ✅

### Test 2: Cycle Detection
1. In Power Query Editor, check `all_crimes` query
2. Look at the `CurrentCycleName` variable (if visible in preview)
3. Or create a quick test: Filter to today's date and verify cycle is detected

### Test 3: Period Classification
1. In Power BI, create a quick table visual
2. Add columns: `Case Number`, `Incident_Date_Date`, `Period`
3. Verify Period values look correct (7-Day, 28-Day, YTD, Prior Year)

---

## If Everything Works ✅

**You're ready to save!**

1. **Save the template**:
   - File → Save As
   - Location: `C:\Users\carucci_r\OneDrive - City of Hackensack\15_Templates\Base_Report.pbix`
   - Overwrite existing file (or create backup first)

2. **Optional**: Create a backup before overwriting:
   - Save as: `Base_Report_backup_weekly.pbix`
   - Then save as: `Base_Report.pbix`

---

## If Something Doesn't Work ❌

**Don't save yet!** Let me know what error you're seeing and we'll fix it first.

Common issues:
- Query refresh errors → Check file paths
- Missing columns → Verify CSV file structure
- Cycle detection not working → Check date formats

---

## Summary

| Item | Required? | Time |
|------|-----------|------|
| Query refresh test | ✅ **YES** | 2 min |
| Cycle detection test | ✅ **YES** | 2 min |
| Period classification check | ✅ **YES** | 2 min |
| Visual terminology review | ⚠️ Optional | 5-10 min |

**Minimum before save**: First 3 items (6 minutes)  
**Recommended**: All 4 items (15 minutes)

---

**Ready to save?** If all tests pass, go ahead and save the template!
