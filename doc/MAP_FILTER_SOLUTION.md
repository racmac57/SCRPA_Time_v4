# Dynamic Map Filter Solution

## Problem
You need to filter the map to show only incidents from the current 7-day cycle (12/23/25 - 12/29/25), but don't want to manually update the date filter every week.

## Solution
Added a new calculated column `IsCurrent7DayCycle` to the `Updated_All_Crimes` query that automatically identifies rows belonging to the current 7-day cycle based on `Report_Date`.

## New Column: `IsCurrent7DayCycle`

**Type:** Boolean (true/false)

**Logic:**
- `true` when `Report_Date` falls within the current cycle's start and end dates
- `false` otherwise
- Automatically updates based on "Today" - no manual date changes needed

**Calculation:**
```m
IsCurrent7DayCycle = 
    if HasCurrentCycle and Report_Date <> null then
        Report_Date >= CurrentCycleStart and Report_Date <= CurrentCycleEnd
    else false
```

## How to Use in Power BI

### For the Map Visual:

1. **Add Filter to Map:**
   - Select the map visual
   - Go to Visualizations pane → Filters on this visual
   - Add filter: `IsCurrent7DayCycle`
   - Set to: `IsCurrent7DayCycle = true`

2. **That's it!** The filter will automatically work for the current week without any manual updates.

### Alternative: Exclude Backfill Incidents

If you want to exclude backfill incidents (incidents that occurred before the cycle but were reported during it):

**Filter:**
- `IsCurrent7DayCycle = true`
- `Backfill_7Day = false`

This shows only incidents that:
- Were reported during the current 7-day cycle
- AND occurred during the current 7-day cycle (not backfill)

## Benefits

✅ **No manual updates** - Automatically uses the current cycle based on "Today"
✅ **Consistent with cycle logic** - Uses the same cycle calendar that defines your 7-day periods
✅ **Matches chart/table** - Uses `Report_Date` like your other visuals
✅ **Simple filter** - Just one boolean column to filter on

## Column Location

The `IsCurrent7DayCycle` column is added right after `cycle_name_adjusted` in the query, so it's available for all subsequent transformations and in your Power BI model.

## Testing

After refreshing the query:
1. Check that `IsCurrent7DayCycle` column appears in your table
2. Verify it's `true` for incidents with `Report_Date` between 12/23/25 and 12/29/25
3. Apply the filter to your map visual
4. The map should now match your chart and table

