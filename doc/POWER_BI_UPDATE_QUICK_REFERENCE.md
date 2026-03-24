# Power BI Template Update - Quick Reference

**Date**: 2026-01-26  
**Purpose**: Bi-Weekly Reporting Transition

---

## ⚠️ REQUIRED: Update This Query in Power BI Advanced Editor

### Query: `q_CycleCalendar`

**Location in Power BI**:
- Power Query Editor → Queries pane → `q_CycleCalendar`

**Steps**:
1. Open Power BI Desktop
2. Click **Transform Data** (or **Edit Queries**)
3. In left pane, find **`q_CycleCalendar`**
4. Right-click → **Advanced Editor**
5. **Copy the entire code** from:
   ```
   C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\m_code\q_CycleCalendar.m
   ```
6. **Paste** into Advanced Editor (replace all existing code)
7. Click **Done**
8. Verify no errors appear

**What Changed**:
- Added `BiWeekly_Report_Name` column to type definitions (line 22)
- Updated timestamp in header comment

**Verification**:
- ✅ Query should refresh without errors
- ✅ Preview should show `BiWeekly_Report_Name` column
- ✅ 2026 rows should show values like `26BW01`, `26BW02`, etc.
- ✅ 2025 rows will have empty/null values (expected)

---

## ❌ NO UPDATE NEEDED: These Queries Work As-Is

### ✅ `all_crimes` (or `Updated_All_Crimes`)
- **Status**: No changes needed
- **Reason**: Uses `Report_Name` which still exists, all logic works with bi-weekly dates

### ✅ `q_RMS_Source`
- **Status**: No changes needed
- **Reason**: Only loads source data, unrelated to cycles

### ✅ `q_CallTypeCategories`
- **Status**: No changes needed
- **Reason**: Only handles call type mappings, unrelated to cycles

---

## ⚠️ OPTIONAL: Check If This Module Exists

### `Export_Formatting` (if used)
- **Status**: Updated for bi-weekly format support
- **Action**: Only update if your Power BI file uses export formatting functions
- **How to Check**: Look for queries/functions with "Export" or "Formatting" in name

---

## Testing After Update

1. **Refresh `q_CycleCalendar`**
   - Should complete without errors
   - Check `BiWeekly_Report_Name` column appears

2. **Refresh `all_crimes`**
   - Should complete without errors
   - Verify cycle detection still works

3. **Check Current Cycle**
   - Verify current cycle is detected correctly for bi-weekly dates
   - Check date ranges are correct

4. **Save Template**
   - Save updated `.pbix` file
   - Location: `08_Templates\Base_Report.pbix`

---

## Summary

| Query/Module | Update Required? | Priority |
|-------------|------------------|----------|
| `q_CycleCalendar` | ✅ **YES** | 🔴 **CRITICAL** |
| `all_crimes` | ❌ No | - |
| `q_RMS_Source` | ❌ No | - |
| `q_CallTypeCategories` | ❌ No | - |
| `Export_Formatting` | ⚠️ Check if used | 🟡 Optional |

---

**Next**: After updating Power BI, proceed to Step 3 (Script Updates)
