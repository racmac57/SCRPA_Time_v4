# Period Classification Fix - Prior Year Priority

## Problem Identified

**Case 25-113412** (12/29/2025) was still showing **"28-Day"** instead of **"Prior Year"** after the cycle detection fix.

### Root Cause

The Period classification logic was checking 28-Day BEFORE checking Prior Year:
1. 7-Day (highest priority)
2. 28-Day ← This was catching 2025 incidents
3. YTD
4. Prior Year ← Never reached for 2025 incidents in 28-Day window

Since the 28-Day window (12/09/2025 to 1/5/2026) includes dates from 2025, a 2025 incident (12/29/2025) was being classified as "28-Day" before the Prior Year check could run.

## Solution Applied

Reordered the Period classification logic to check **Prior Year BEFORE 28-Day**:

1. **7-Day** (highest priority - current cycle incidents)
2. **Prior Year** (check before 28-Day to prevent prior year incidents from being misclassified)
3. **28-Day** (only applies to current year incidents now)
4. **YTD** (current year incidents outside 7-Day/28-Day windows)
5. **Historical** (older years)

### Updated Logic

```m
if dI = null then "Historical"
// 7-Day period: Check first (highest priority)
else if in7Day then "7-Day"
// Prior year (2025): Check before 28-Day to prevent prior year incidents from being classified as 28-Day
// Prior year incidents should be "Prior Year" even if they fall within 28-Day window
else if incidentYear = currentYear - 1 then "Prior Year"
// 28-Day period: Check third (only for current year incidents, not prior year)
else if in28Day then "28-Day"
// YTD: incident occurred in current year (2026) but outside 7-Day/28-Day windows
else if incidentYear = currentYear then "YTD"
// Older years (2024 and earlier): Generic "Historical"
else "Historical"
```

## Expected Results After Fix

### Case 25-113412 (12/29/2025):
- **Period**: "Prior Year" ✅
- **Reason**: Incident year is 2025 (prior year), so it's classified as "Prior Year" regardless of 28-Day window

### Case 26-001094 (01/04/2026):
- **Period**: "7-Day" ✅ (already working correctly)
- **Reason**: Incident date is within 7-Day cycle range (12/30/2025 - 1/5/2026)

## Verification Steps

1. **Update Power BI template** with fixed M code
2. **Refresh query** in Power BI
3. **Verify Period values**:
   - Case 25-113412: Period = "Prior Year" ✅
   - Case 26-001094: Period = "7-Day" ✅

## Technical Details

The 28-Day window spans across year boundaries:
- **28-Day Range**: 12/09/2025 to 1/5/2026
- This includes both 2025 and 2026 dates

**Rule**: Prior year incidents should always be classified as "Prior Year", even if they fall within the 28-Day window. The 28-Day classification should only apply to current year incidents.

---

**Date**: 2026-01-06  
**Status**: ✅ Fixed  
**File Modified**: `m_code/all_crimes.m`
