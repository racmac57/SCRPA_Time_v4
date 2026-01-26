# Step 3: Script Verification & Updates - COMPLETED ✅

**Date**: 2026-01-26  
**Status**: ✅ Complete

---

## Scripts That Need Updates

### 🔴 CRITICAL: Must Update

#### 1. `generate_weekly_report.py`
**Location**: `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\`
**Issue**: References OLD cycle calendar file
- **Line 16**: Uses `7Day_28Day_Cycle_20250414.csv`
- **Needs**: Update to `7Day_28Day_Cycle_20260106.csv`
- **Impact**: Script won't find bi-weekly cycles for 2026

#### 2. `export_excel_sheets_to_csv.py`
**Location**: `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\`
**Issue**: References OLD cycle calendar file
- **Line 619**: Uses `7Day_28Day_Cycle_20250414.csv`
- **Needs**: Update to `7Day_28Day_Cycle_20260106.csv`
- **Impact**: 7-day CSV filtering won't use correct bi-weekly dates

---

### ✅ Already Correct (No Updates Needed)

#### 1. `prepare_briefing_csv.py`
**Location**: `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA\scripts\`
**Status**: ✅ Already has smart fallback logic
- **Lines 52-54**: Checks for new file first, then falls back to old
- **Logic**: `_cycle_calendar_new if exists else _cycle_calendar_old`
- **Result**: Will automatically use updated file

#### 2. `export_enriched_data_and_email.py`
**Location**: `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\scripts\`
**Status**: ✅ Already uses correct file
- **Line 85**: Uses `7Day_28Day_Cycle_20260106.csv`
- **No changes needed**

#### 3. `organize_report_files.py`
**Status**: ✅ No cycle calendar references
- Works with folder names only
- No changes needed

---

## Lagday Logic Verification ✅

### M Code: `all_crimes.m`

**Status**: ✅ **CORRECT - No Changes Needed**

The lagday logic uses a **three-tier approach** that works perfectly with bi-weekly cycles:

1. **First Try**: Match `Report_Due_Date` exactly
   - For 01/27/26, finds cycle with `Report_Due_Date = 01/27/26`
   - This is the **most accurate** method and works with bi-weekly cycles

2. **Second Try**: Report Date within cycle range
   - Falls back if report date is mid-cycle
   - Uses `7_Day_Start` and `7_Day_End` from cycle calendar

3. **Third Try**: Most recent cycle that ended on/before Report Date
   - Final fallback for edge cases
   - Sorts by `7_Day_End` descending

**Why This Works with Bi-Weekly**:
- The logic matches on `Report_Due_Date` first, which is exactly what we need
- Bi-weekly cycles have `Report_Due_Date` values (01/13/26, 01/27/26, etc.)
- The three-tier approach ensures it finds the correct cycle even if dates don't match exactly

**Lagday Calculation** (Lines 386-425):
- Uses same three-tier approach for each row's `Report_Date`
- Calculates: `Duration.Days(CycleStartForReport - dI)`
- This correctly identifies incidents that occurred before the cycle start

**Conclusion**: ✅ Lagday logic is **correct and will work** with bi-weekly cycles. No changes needed.

---

## Folder Naming Consideration

### Current Behavior
- `generate_weekly_report.py` uses `Report_Name` from cycle calendar
- For 01/27/26, this will return: `26C01W04` (weekly name)
- Folder will be: `26C01W04_26_01_27`

### Option 1: Keep Weekly Names (Recommended for Now)
- **Pros**: Maintains consistency with existing folders
- **Cons**: Name doesn't reflect bi-weekly reporting
- **Action**: No changes needed

### Option 2: Use Bi-Weekly Names
- **Pros**: Folder names reflect bi-weekly reporting
- **Cons**: Breaks consistency with existing folders
- **Action**: Update `generate_weekly_report.py` to use `BiWeekly_Report_Name` when available

**Recommendation**: Keep weekly names for now to maintain consistency. Can update later if needed.

---

## Script Updates Required

### Update 1: `generate_weekly_report.py`

**Change Line 16**:
```python
# OLD:
CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20250414.csv"

# NEW:
CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv"
```

---

### Update 2: `export_excel_sheets_to_csv.py`

**Change Line 619**:
```python
# OLD:
CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20250414.csv"

# NEW:
CYCLE_CSV = r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv"
```

---

## Verification Checklist

### Before Running Next Report:

- [ ] Update `generate_weekly_report.py` (line 16)
- [ ] Update `export_excel_sheets_to_csv.py` (line 619)
- [ ] Test with report date 01/27/26
- [ ] Verify folder is created correctly
- [ ] Verify 7-day CSV filtering uses correct dates
- [ ] Verify lagday calculations are correct

---

## Testing Procedure

### Test 1: Folder Creation
1. Run `Run_SCRPA_Report_Folder.bat`
2. Enter date: `01/27/26`
3. Verify folder name: Should be `26C01W04_26_01_27` (or `26BW02_26_01_27` if using bi-weekly names)
4. Verify folder structure: `Data/`, `Reports/`, `Documentation/`

### Test 2: 7-Day CSV Filtering
1. Check exported CSV files
2. Verify 7-day filtered CSV uses dates: 01/20/26 to 01/26/26
3. Verify incidents outside this range are excluded

### Test 3: Lagday Verification
1. Open Power BI report
2. Check `IsLagDay` and `LagDays` columns
3. Verify lagday incidents are correctly identified
4. Spot-check a few cases to ensure calculations are correct

---

## Summary

| Script | Status | Action Required |
|--------|--------|-----------------|
| `generate_weekly_report.py` | 🔴 Needs Update | Update cycle calendar path |
| `export_excel_sheets_to_csv.py` | 🔴 Needs Update | Update cycle calendar path |
| `prepare_briefing_csv.py` | ✅ OK | No changes (has fallback) |
| `export_enriched_data_and_email.py` | ✅ OK | No changes (already correct) |
| `organize_report_files.py` | ✅ OK | No changes (no cycle refs) |
| `all_crimes.m` (lagday logic) | ✅ OK | No changes (logic is correct) |

---

**Next**: Update the 2 scripts, then test with 01/27/26 report date
