# Power BI Query Fix Summary - LagDays Calculation

## Issue Identified

**Case 25-113076** showed a discrepancy:
- **SCRPA_7Day_Detailed.csv**: `LagDays = 3` ✅ (Correct)
- **Power BI Queries**: `LagDays = 8` ❌ (Incorrect - was calculating reporting delay)

## Root Cause

Both Power BI queries (`all_crimes.m` and `Updated_All_Crimes.m`) were calculating `LagDays` incorrectly:
- **Wrong**: `LagDays = Report Date - Incident Date` (this is actually reporting delay)
- **Correct**: `LagDays = CycleStartDate - Incident Date` (only for lagday incidents, 0 otherwise)

## Fixes Applied

### 1. Updated `Updated_All_Crimes.m`
- ✅ Renamed incorrect `LagDays` calculation to `IncidentToReportDays` (QA metric)
- ✅ Added `IsLagDay` column (boolean: true if Incident Date < CycleStartDate)
- ✅ Added correct `LagDays` calculation (cycle-aware, days incident precedes cycle start)
- ✅ Fixed cycle calendar date typing

### 2. Updated `all_crimes.m`
- ✅ Renamed incorrect `LagDays` calculation to `IncidentToReportDays` (QA metric)
- ✅ Added `IsLagDay` column (boolean: true if Incident Date < CycleStartDate)
- ✅ Added correct `LagDays` calculation (cycle-aware, days incident precedes cycle start)
- ✅ Fixed cycle calendar date typing (removed Date.FromText calls)

## Column Definitions (Now Correct)

### LagDays
- **Type**: Integer
- **Definition**: Days incident precedes `CycleStartDate` (0 if not lagday)
- **Calculation**: `CycleStartDate - Incident Date` (only when `IsLagDay = true`)

### IsLagDay
- **Type**: Boolean
- **Definition**: `true` when `Incident Date < CycleStartDate` (for the cycle that Report Date falls into)

### IncidentToReportDays
- **Type**: Integer
- **Definition**: Days between `Report Date` and `Incident Date` (QA metric for reporting delays)
- **Calculation**: `Report Date - Incident Date` (always calculated)

## Which Query to Use?

**Recommendation**: Use `Updated_All_Crimes.m` as it is:
- More optimized (uses Table.Buffer for performance)
- Has cleaner code structure
- Already has cycle calendar properly typed

**Action Required**:
1. Open Power BI template: `15_Templates\Base_Report.pbix`
2. Check which query is referenced (likely "All_Crimes" or "Updated_All_Crimes")
3. If using `all_crimes.m`, consider switching to `Updated_All_Crimes.m` for better performance
4. If keeping `all_crimes.m`, ensure it's updated with the fixes above

## Testing

To verify the fix works:
1. Open Power BI Desktop
2. Load the updated query
3. Filter for case 25-113076
4. Verify:
   - `IsLagDay` = `true`
   - `LagDays` = `3` (not 8)
   - `IncidentToReportDays` = `8` (reporting delay)

## Next Steps

1. ✅ Both queries fixed
2. ⏳ **Update Power BI template** (`15_Templates\Base_Report.pbix`) to use the corrected query
3. ⏳ **Test** with case 25-113076 to verify fix
4. ⏳ **Consider deleting** unused query if only one is needed

## Files Modified

- `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\Updated_All_Crimes.m`
- `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\all_crimes.m`

## Files Created

- `LAGDAYS_DISCREPANCY_ANALYSIS.md` - Detailed analysis of the issue
- `POWER_BI_QUERY_FIX_SUMMARY.md` - This summary document

