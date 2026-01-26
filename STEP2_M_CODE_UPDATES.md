# Step 2: M Code Updates - COMPLETED ✅

**Date**: 2026-01-26  
**Status**: ✅ Complete

---

## Files Updated

### 1. ✅ `q_CycleCalendar.m` - UPDATED

**Change**: Added `BiWeekly_Report_Name` column to type definitions

**What Changed**:
- Added `{"BiWeekly_Report_Name", type nullable text}` to `Table.TransformColumnTypes`
- Updated header comment with new timestamp and bi-weekly note

**Location in Power BI**: 
- Query Name: `q_CycleCalendar`
- **Action Required**: ✅ **MUST UPDATE IN POWER BI ADVANCED EDITOR**

---

### 2. ✅ `Export_Formatting.m` - UPDATED

**Change**: Updated cycle name validation to accept both weekly and bi-weekly formats

**What Changed**:
- Validation now accepts:
  - Weekly format: `C##W##` (e.g., `26C01W02`)
  - Bi-weekly format: `##BW##` (e.g., `26BW01`)

**Location in Power BI**:
- This is a function/module, not a direct query
- **Action Required**: ⚠️ **CHECK IF USED** - If this module is referenced, update it in Advanced Editor

---

### 3. ✅ `all_crimes.m` - NO CHANGES NEEDED

**Status**: Works as-is with bi-weekly calendar

**Why No Changes**:
- Uses `Report_Name` column which still exists in CSV
- Cycle detection logic works with bi-weekly dates
- Period classification logic unchanged
- All date range calculations remain the same

**Location in Power BI**:
- Query Name: `all_crimes` (or `Updated_All_Crimes`)
- **Action Required**: ❌ **NO UPDATE NEEDED**

---

### 4. ✅ `q_CallTypeCategories.m` - NO CHANGES NEEDED

**Status**: Unrelated to cycle calendar

**Why No Changes**:
- Handles call type mappings only
- Not affected by bi-weekly reporting

**Location in Power BI**:
- Query Name: `q_CallTypeCategories`
- **Action Required**: ❌ **NO UPDATE NEEDED**

---

### 5. ✅ `q_RMS_Source.m` - NO CHANGES NEEDED

**Status**: Unrelated to cycle calendar

**Why No Changes**:
- Loads RMS Excel source data only
- Not affected by bi-weekly reporting

**Location in Power BI**:
- Query Name: `q_RMS_Source`
- **Action Required**: ❌ **NO UPDATE NEEDED**

---

## Power BI Advanced Editor Updates Required

### ⚠️ CRITICAL: Must Update in Power BI

#### 1. Query: `q_CycleCalendar`

**Steps**:
1. Open Power BI Desktop
2. Go to **Home** → **Transform Data** (or **Edit Queries**)
3. Find query: **`q_CycleCalendar`**
4. Right-click → **Advanced Editor**
5. Replace the entire query code with the updated version from:
   - `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\m_code\q_CycleCalendar.m`
6. Click **Done**
7. Verify the query loads without errors
8. Check that `BiWeekly_Report_Name` column appears in the preview

**What to Look For**:
- Line 22 should include: `{"BiWeekly_Report_Name", type nullable text}`
- Query should refresh successfully
- Preview should show the new column

---

#### 2. Optional: Check `Export_Formatting` Module

**If Used**:
- This is typically a custom function/module
- If your Power BI file uses export formatting functions, update the validation logic
- File: `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\m_code\Export_Formatting.m`

**How to Check**:
1. In Power BI, go to **Home** → **Transform Data**
2. Look for any queries or functions related to "Export" or "Formatting"
3. If found, update the cycle name validation logic

---

## Verification Steps

### After Updating `q_CycleCalendar`:

1. **Refresh the Query**:
   - Right-click `q_CycleCalendar` → **Refresh Preview**
   - Should complete without errors

2. **Check Column Exists**:
   - In query preview, verify `BiWeekly_Report_Name` column appears
   - Should show values like `26BW01`, `26BW02`, etc. for 2026 rows
   - 2025 rows will have empty/null values (expected)

3. **Test Cycle Detection**:
   - Refresh `all_crimes` query
   - Verify it still works correctly
   - Check that current cycle detection works for bi-weekly dates

4. **Verify Date Ranges**:
   - Check that `7_Day_Start`, `7_Day_End`, `28_Day_Start`, `28_Day_End` are correct
   - These should match the CSV file values

---

## Summary of Changes

| File | Status | Power BI Update Required? |
|------|--------|---------------------------|
| `q_CycleCalendar.m` | ✅ Updated | ✅ **YES - MUST UPDATE** |
| `Export_Formatting.m` | ✅ Updated | ⚠️ Check if used |
| `all_crimes.m` | ✅ No changes | ❌ No |
| `q_CallTypeCategories.m` | ✅ No changes | ❌ No |
| `q_RMS_Source.m` | ✅ No changes | ❌ No |

---

## Next Steps

After updating Power BI:

1. ✅ **Test Cycle Calendar Load**
   - Verify `q_CycleCalendar` loads correctly
   - Check `BiWeekly_Report_Name` column appears

2. ✅ **Test Current Cycle Detection**
   - Set Today to 01/27/26 (or use actual date)
   - Verify current cycle is detected correctly
   - Check that `CurrentCycleName` works

3. ✅ **Test Period Classification**
   - Verify 7-Day, 28-Day, YTD, Prior Year classifications still work
   - Check that date ranges are correct

4. ✅ **Save Template**
   - Save updated Power BI template
   - Location: `C:\Users\carucci_r\OneDrive - City of Hackensack\15_Templates\Base_Report.pbix`

---

## Important Notes

### ✅ Backward Compatibility
- `Report_Name` column still exists and is used by `all_crimes.m`
- System will work with both weekly and bi-weekly cycles
- Historical data (2025) continues to use weekly names

### ✅ Bi-Weekly Column Usage
- `BiWeekly_Report_Name` is available for display/reporting purposes
- Can be used in Power BI visuals if desired
- Not required for core functionality (cycle detection, period classification)

### ✅ Date Ranges Unchanged
- All date range calculations remain the same
- 7-Day and 28-Day windows continue to work as before
- Only reporting frequency changed, not analysis periods

---

**Status**: ✅ Step 2 Complete  
**Ready for**: Step 3 - Script Updates
