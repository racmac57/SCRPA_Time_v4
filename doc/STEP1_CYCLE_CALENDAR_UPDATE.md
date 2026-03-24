# Step 1: Cycle Calendar Update - COMPLETED ✅

**Date**: 2026-01-26  
**Status**: ✅ Complete

---

## What Was Done

### 1. Backups Created ✅
- **CSV Backup**: `7Day_28Day_Cycle_20260106_backup_weekly.csv`
  - Location: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\`
  - Contains original weekly cycle data for 2025 and 2026
  
- **TXT Backup**: `26_scrpa_cycle_backup_weekly.txt`
  - Location: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\`
  - Contains original weekly cycle data for 2026

### 2. Files Updated ✅

#### A. Main CSV File (Power BI uses this)
**File**: `7Day_28Day_Cycle_20260106.csv`
- **Location**: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\`
- **Changes**:
  - ✅ Kept all 2025 weekly data (historical reference)
  - ✅ Filtered 2026 to bi-weekly entries only (26 reports)
  - ✅ Added `BiWeekly_Report_Name` column
  - ✅ Bi-weekly naming: `26BW01` through `26BW26`

#### B. TXT File (Reference copy)
**File**: `26_scrpa_cycle.txt`
- **Location**: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\`
- **Changes**:
  - ✅ Updated to match CSV file structure
  - ✅ Contains only 2026 bi-weekly entries
  - ✅ Added `BiWeekly_Report_Name` column

---

## File Format Decision: CSV ✅

### Why CSV (Not JSON)?

**✅ CSV is the correct choice because:**

1. **Power BI Compatibility**
   - Power BI M code uses `Csv.Document()` function
   - The query in `q_CycleCalendar.m` is already configured for CSV
   - No code changes needed for format

2. **Simplicity**
   - CSV is human-readable and easy to edit in Excel
   - No special parsing required
   - Standard format for tabular data

3. **Existing Infrastructure**
   - All scripts already expect CSV format
   - Python scripts use `pd.read_csv()` which works with CSV
   - No need to update multiple scripts

4. **JSON Would Require:**
   - ❌ Changing Power BI M code to use `Json.Document()`
   - ❌ Updating all Python scripts to parse JSON
   - ❌ More complex structure for simple tabular data
   - ❌ Harder to edit manually

**Conclusion**: CSV format is perfect for this use case. No conversion needed.

---

## Bi-Weekly Cycle Structure

### 2026 Bi-Weekly Report Dates (26 total)

| Report # | Report_Due_Date | BiWeekly_Report_Name | 7-Day Window | 28-Day Window |
|----------|----------------|---------------------|--------------|---------------|
| 1 | 01/13/26 | 26BW01 | 01/06-01/12 | 12/16-01/12 |
| 2 | 01/27/26 | 26BW02 | 01/20-01/26 | 12/30-01/26 |
| 3 | 02/10/26 | 26BW03 | 02/03-02/09 | 01/13-02/09 |
| 4 | 02/24/26 | 26BW04 | 02/17-02/23 | 01/27-02/23 |
| ... | ... | ... | ... | ... |
| 26 | 12/29/26 | 26BW26 | 12/22-12/28 | 12/01-12/28 |

**Pattern**: Every 2 weeks starting from 01/13/26

---

## Column Structure

### Updated Header Row:
```
Report_Due_Date,7_Day_Start,7_Day_End,28_Day_Start,28_Day_End,Report_Name,BiWeekly_Report_Name
```

### Column Descriptions:
- **Report_Due_Date**: When the report is submitted (bi-weekly)
- **7_Day_Start**: Start of 7-day analysis window
- **7_Day_End**: End of 7-day analysis window
- **28_Day_Start**: Start of 28-day analysis window
- **28_Day_End**: End of 28-day analysis window
- **Report_Name**: Original weekly name (e.g., `26C01W02`) - kept for reference
- **BiWeekly_Report_Name**: New bi-weekly name (e.g., `26BW01`)

---

## Important Notes

### ✅ Date Ranges Stay the Same
- The `7_Day_Start`, `7_Day_End`, `28_Day_Start`, `28_Day_End` columns represent **analysis periods**, not reporting frequency
- These windows continue to roll forward every 7 days regardless of bi-weekly reporting
- **No changes needed** to date range logic

### ✅ Historical Data Preserved
- All 2025 weekly data is kept in the CSV file
- Useful for historical reference and comparisons
- Power BI will only use 2026 entries for current cycle detection

### ✅ Bi-Weekly Naming Convention
- Format: `YYBW##` (Year + Bi-Weekly + Number)
- Example: `26BW01` = 2026 Bi-Weekly Report 01
- Total: 26 bi-weekly reports per year

---

## Next Steps

### Step 2: Update M Code Query
- [ ] Update `q_CycleCalendar.m` to include `BiWeekly_Report_Name` column in type definitions
- [ ] Test cycle calendar loads correctly in Power BI
- [ ] Verify current cycle detection works for bi-weekly dates

### Step 3: Update Scripts
- [ ] Locate `generate_weekly_report.py`
- [ ] Update folder naming logic for bi-weekly format
- [ ] Test folder creation

### Step 4: Update Power BI Template
- [ ] Review visuals for "weekly" terminology
- [ ] Update to "bi-weekly" or "reporting period"
- [ ] Save updated template

---

## Verification

To verify the update worked:

1. **Check CSV File**:
   - Open `7Day_28Day_Cycle_20260106.csv` in Excel
   - Verify `BiWeekly_Report_Name` column exists
   - Verify only bi-weekly dates for 2026 (26 entries)
   - Verify 01/27/26 shows `26BW02`

2. **Test Power BI**:
   - Open Power BI template
   - Refresh `q_CycleCalendar` query
   - Verify new column appears
   - Verify cycle lookup for 01/27/26 works

---

## Files Modified

1. ✅ `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv`
2. ✅ `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\26_scrpa_cycle.txt`

## Files Created (Backups)

1. ✅ `7Day_28Day_Cycle_20260106_backup_weekly.csv`
2. ✅ `26_scrpa_cycle_backup_weekly.txt`

---

**Status**: ✅ Step 1 Complete  
**Ready for**: Step 2 - M Code Updates
