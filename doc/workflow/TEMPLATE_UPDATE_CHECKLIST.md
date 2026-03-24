# Template Update Checklist

**Template Location**: `C:\Users\carucci_r\OneDrive - City of Hackensack\08_Templates\Base_Report.pbix`  
**Date**: 2026-01-06

## ✅ Pre-Update Checklist

Before updating the template, ensure you have:
- [ ] Backed up current `Base_Report.pbix` (optional but recommended)
- [ ] Updated M code files in `m_code/` directory are ready
- [ ] Color scheme decisions finalized

---

## 📝 Items to Update in Base_Report.pbix

### 1. M Code Queries
Update these queries in Power BI Desktop Advanced Editor:

- [ ] **`q_RMS_Source`** - Copy from `m_code/q_RMS_Source.m`
- [ ] **`q_CycleCalendar`** - Copy from `m_code/q_CycleCalendar.m`
- [ ] **`q_CallTypeCategories`** - Copy from `m_code/q_CallTypeCategories.m`
- [ ] **`All_Crimes`** (or `Updated_All_Crimes`) - Copy from `m_code/all_crimes.m`

**Key Changes in all_crimes.m**:
- Period label changed from "2025 Historical" to "Prior Year"
- Period classification logic updated for year transitions

### 2. Visual Formatting - Period Colors

Update color formatting in all visuals that use the `Period` column:

- [ ] **7-Day**: (keep existing color)
- [ ] **28-Day**: `#77C99A` ✅ (green - verify it's set)
- [ ] **Prior Year**: `#7F92A2` ✅ (gray-blue - **NEW COLOR**)
- [ ] **YTD**: `#118DFF` ✅ (blue - verify it's set)

**Where to Update**:
- Bar charts (Burglary, Motor Vehicle Theft, etc.)
- Column charts
- Any visual with Period as legend/category
- Conditional formatting (if used)

### 3. Data Source Verification

- [ ] Verify `q_CycleCalendar` points to: `7Day_28Day_Cycle_20260106.csv`
- [ ] Verify `q_RMS_Source` points to correct folder path
- [ ] Verify `q_CallTypeCategories` points to correct CSV path

---

## 🔄 After Template Update

### 1. Test the Template
- [ ] Open updated `Base_Report.pbix` in Power BI Desktop
- [ ] Refresh all queries
- [ ] Verify Period column shows "Prior Year" (not "2025 Historical")
- [ ] Check that colors match the scheme above
- [ ] Verify visuals display correctly

### 2. Save Template
- [ ] Save `Base_Report.pbix` with all updates
- [ ] Close Power BI Desktop

### 3. Run Automation
- [ ] Run `Run_SCRPA_Report_Folder.bat`
- [ ] When prompted to overwrite existing `.pbix`, type `y`
- [ ] Verify new report folder has updated template

---

## ⚠️ What Gets Overwritten

When you run the `.bat` file and confirm overwrite:

✅ **Will be overwritten**:
- The `.pbix` file in the report folder (e.g., `26C01W01_26_01_06.pbix`)

❌ **Will NOT be overwritten**:
- `Data/` folder contents (CSV files)
- `Reports/` folder contents (HTML/PDF files)
- `Documentation/` folder contents (MD files)
- Any other files in the report folder

**Note**: Only the Power BI file gets replaced. All your data exports and reports remain intact.

---

## 📋 Quick Reference

**Color Hex Codes**:
```
7-Day:     (existing - unchanged)
28-Day:    #77C99A (green)
Prior Year: #7F92A2 (gray-blue)
YTD:       #118DFF (blue)
```

**M Code Files Location**:
```
m_code/q_RMS_Source.m
m_code/q_CycleCalendar.m
m_code/q_CallTypeCategories.m
m_code/all_crimes.m
```

---

## ✅ Verification Steps

After running the automation:
1. Open the new `.pbix` file in Power BI Desktop
2. Refresh queries
3. Check a visual with Period legend - should show "Prior Year" (not "2025 Historical")
4. Verify colors match the scheme
5. Export a preview table to confirm Period values are correct
