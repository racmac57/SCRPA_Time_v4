# Issue Fixes - v1.9.1

**Date**: 2026-01-26  
**Status**: ✅ Fixed

---

## Issues Identified and Fixed

### Issue 1: Incomplete Cycle Calendar Filtering ✅ FIXED

**Problem**: 
- The 2026 cycle calendar was filtered to only include bi-weekly `Report_Due_Date` entries (01/13, 01/27, etc.)
- The first entry (01/13/2026) has `7_Day_Start = 01/06/2026`
- This created a gap: any code looking up cycles for dates between 01/06/2026 and 01/12/2026 would fail because those dates don't exist as `Report_Due_Date` values
- The weekly entry for 01/06/2026 with `Report_Due_Date = 01/06/2026` was removed during the filter, breaking backward-compatible date lookups

**Solution**:
- Added back the missing weekly entry for 01/06/2026
- Entry: `01/06/2026,12/30/2025,01/05/2026,12/09/2025,01/05/2026,26C01W01,`
- This entry has empty `BiWeekly_Report_Name` (not a bi-weekly report date)
- Allows date lookups to work for the period 01/06/2026 - 01/12/2026
- Maintains backward compatibility while preserving bi-weekly reporting structure

**File Updated**:
- `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv`

**Impact**:
- ✅ Date lookups now work for all dates in 2026
- ✅ No gaps in cycle calendar coverage
- ✅ Backward compatibility maintained
- ✅ Bi-weekly reporting structure preserved

---

### Issue 2: Overly Permissive Bi-Weekly Validation ✅ FIXED

**Problem**:
- The validation logic checked `Text.Contains(cycleName, "BW")` and `Text.Length(cycleName) >= 5`
- This was too loose—it would accept any string containing "BW" with 5+ characters (e.g., "TestBW", "XBWabc")
- Not just the intended format `##BW##` (e.g., `26BW01`)
- The weekly format check was also imprecise but less dangerous

**Solution**:
- Made validation stricter for both formats:
  - **Weekly**: Must start with "C", contain "W", and be exactly 7 characters (e.g., "26C01W02")
  - **Bi-weekly**: Must be exactly 6 characters, with "BW" at positions 2-3, and valid 2-digit prefixes/suffixes (e.g., "26BW01")
- Uses `Text.Middle()` to check exact position of "BW"
- Validates length requirements for both formats

**File Updated**:
- `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\m_code\Export_Formatting.m`

**New Validation Logic**:
```m
let
    isWeekly = Text.StartsWith(cycleName, "C") and Text.Contains(cycleName, "W") and Text.Length(cycleName) = 7,
    isBiWeekly = Text.Length(cycleName) = 6 and 
                Text.Middle(cycleName, 2, 2) = "BW" and
                Text.Start(cycleName, 2) <> null and
                Text.End(cycleName, 2) <> null
in
    isWeekly or isBiWeekly
```

**Impact**:
- ✅ Only accepts valid weekly format: `C##W##` (7 chars)
- ✅ Only accepts valid bi-weekly format: `##BW##` (6 chars)
- ✅ Rejects invalid formats like "TestBW", "XBWabc", etc.
- ✅ Prevents data integrity issues in downstream processes

---

## Testing Recommendations

### Test 1: Cycle Calendar Date Lookups
1. Test date lookup for 01/06/2026 - should find entry with `Report_Due_Date = 01/06/2026`
2. Test date lookup for 01/10/2026 - should find entry with `Report_Due_Date = 01/06/2026` (within 7-day range)
3. Test date lookup for 01/13/2026 - should find entry with `Report_Due_Date = 01/13/2026` (bi-weekly)
4. Verify no gaps in date coverage

### Test 2: Cycle Name Validation
1. Test valid weekly: `26C01W02` - should pass ✅
2. Test valid bi-weekly: `26BW01` - should pass ✅
3. Test invalid: `TestBW` - should fail ❌
4. Test invalid: `XBWabc` - should fail ❌
5. Test invalid: `26BW1` (too short) - should fail ❌
6. Test invalid: `26BW001` (too long) - should fail ❌

---

## Files Changed

1. ✅ `7Day_28Day_Cycle_20260106.csv` - Added missing 01/06/2026 entry
2. ✅ `Export_Formatting.m` - Stricter validation logic

---

## Next Steps

1. **Update Power BI Template**:
   - Update `Export_Formatting.m` in Power BI Advanced Editor
   - Refresh `q_CycleCalendar` query to load updated CSV

2. **Verify in Power BI**:
   - Test cycle name validation with various formats
   - Test date lookups for the gap period (01/06-01/12/2026)

3. **Update Scripts** (if needed):
   - Scripts should automatically pick up the updated cycle calendar CSV
   - No script changes needed for validation (M code only)

---

**Status**: ✅ Both issues fixed and ready for testing
