# Save Current .pbix as New Template - Instructions

## Overview

Since your current report `.pbix` file already contains all the updated M code fixes, you can save it directly as the new template instead of manually updating the template file.

---

## Steps to Save Current .pbix as New Template

### 1. Open Current Report in Power BI
- Navigate to: `Time_Based\2026\26C01W01_26_01_06\26C01W01_26_01_06.pbix`
- Open in Power BI Desktop

### 2. Verify M Code is Updated
- Go to **Transform Data** (Power Query Editor)
- Check that queries have the latest fixes:
  - `q_CycleCalendar` - Should load `Report_Due_Date` column
  - `all_crimes` - Should have updated Period calculation logic
  - All file paths should be single continuous strings

### 3. Remove Report-Specific Data (Optional but Recommended)
- **Option A**: Keep data (template will have sample data)
  - Pro: Can preview visuals immediately
  - Con: Template file will be larger
  
- **Option B**: Clear data (template will be empty)
  - In Power Query Editor, for each query that loads data:
    - Right-click query → **Delete**
    - Or: Keep queries but remove data source connections
  - Pro: Cleaner template, smaller file size
  - Con: Need to reconnect data sources when using template

**Recommendation**: Keep the queries but they'll reconnect to latest data when used, so keeping sample data is fine.

### 4. Save As New Template
- **File** → **Save As**
- Navigate to: `C:\Users\carucci_r\OneDrive - City of Hackensack\08_Templates\`
- **File name**: `Base_Report.pbix`
- Click **Save**
- **Confirm overwrite** if prompted (backup old template first if needed)

### 5. Backup Old Template (Recommended)
Before overwriting, backup the old template:
- Rename: `Base_Report.pbix` → `Base_Report_backup_20260106.pbix`
- Or move to archive folder

---

## What Gets Saved in the Template

✅ **All M Code Queries** - Including all fixes:
- Updated `q_CycleCalendar.m` with `Report_Due_Date`
- Updated `all_crimes.m` with fixed Period calculation
- Updated `q_RMS_Source.m` with correct file paths
- Updated `q_CallTypeCategories.m` with correct file paths

✅ **All Visuals and Pages** - All Power BI visuals and layouts

✅ **All Measures and Calculated Columns** - Any DAX measures you've created

✅ **Data Model Relationships** - Table relationships

✅ **Theme and Formatting** - Colors, fonts, visual styles

✅ **Filters and Slicers** - Filter configurations

---

## After Saving Template

### Next Report Generation
When you run `Run_SCRPA_Report_Folder.bat`:
1. Script will copy `Base_Report.pbix` to new report folder
2. Power BI will automatically refresh queries
3. Queries will load latest data from:
   - `05_EXPORTS\_RMS\scrpa\` (latest Excel file)
   - `09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv`
   - `09_Reference\Classifications\CallTypes\CallType_Categories.csv`

### Verify Template Works
1. Create a test report folder
2. Copy the new `Base_Report.pbix` to it
3. Open in Power BI
4. Click **Refresh** on all queries
5. Verify:
   - Period values are correct
   - Cycle detection works
   - All visuals display correctly

---

## Quick Checklist

- [ ] Current `.pbix` has all updated M code
- [ ] All queries refresh successfully
- [ ] Period values are calculating correctly
- [ ] Visuals display correctly
- [ ] Old template backed up (if desired)
- [ ] Save As to `08_Templates\Base_Report.pbix`
- [ ] Test template with next report generation

---

## Alternative: Update Template Manually

If you prefer to update the existing template manually:
1. Open `08_Templates\Base_Report.pbix`
2. Copy M code from current report to template
3. Update each query one by one
4. Save template

**Note**: Saving current `.pbix` as template is faster and less error-prone.

---

**Date**: 2026-01-06  
**Status**: ✅ Recommended Approach  
**Template Location**: `08_Templates\Base_Report.pbix`
