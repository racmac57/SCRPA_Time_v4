Preview or regenerate SCRPA_Report_Summary.md with data from a cycle folder when counts need correction or the template has changed.

## When to Use

- After a pipeline run when the report summary counts look wrong.
- When the user says "regenerate summary", "fix report summary", or invokes `/generate-report-summary`.
- After correcting data in the enhanced CSV and needing to refresh the summary.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. `scripts/generate_documentation.py` — `get_report_summary_with_data()` function and template
2. The cycle folder's data files

## Steps

1. **Identify the cycle folder.** If the user provides a path, use it. Otherwise, find the most recently modified folder under `Time_Based/YYYY/`.

2. **Read the data files:**
   - `Data/SCRPA_All_Crimes_Enhanced.csv` — for period counts and category breakdown
   - `Data/SCRPA_7Day_Summary.json` — for lag analysis and 7-day crime category counts
   - `Documentation/SCRPA_Report_Summary.md` — current version

3. **Extract cycle info** from the folder name and existing report summary:
   - Cycle Name, Bi-Weekly Cycle, Report Due Date
   - 7-Day Window, Bi-Weekly Period

4. **Compute summary data** from the CSV and JSON:
   - `total`: row count of enhanced CSV
   - `period_7`: count of `Period == '7-Day'`
   - `period_28`: count of `Period == '28-Day'`
   - `ytd`: count of `Period == 'YTD'`
   - `prior_year`: count of `Period == 'Prior Year'`
   - `lag_count`: `counts.lag_incidents` from JSON (7-day scope)
   - `backfill_count`: count of `Backfill_7Day == True` in enhanced CSV
   - `lag_mean`, `lag_median`, `lag_max`: from `lag_analysis.lagdays_distribution` in JSON
   - `category_breakdown`: cross-tab of `Crime_Category` x `Period` for 7-Day/28-Day/YTD columns, ordered: Motor Vehicle Theft, Burglary Auto, Burglary - Comm & Res, Robbery, Sexual Offenses, Other

5. **Build the markdown** following the exact format in `get_report_summary_with_data()`:
   - Cycle Information table
   - Data Summary table
   - Crime Category Breakdown table
   - Lag Day Analysis
   - Notes section

6. **Show a preview** comparing the new content against the existing file. Highlight any count differences.

7. **If the user confirms**, write to `Documentation/SCRPA_Report_Summary.md` in the cycle folder.

## Guardrails

- **Show a preview and ask for confirmation before writing any file.**
- Never modify data files (CSV, JSON).
- Never change the template format without user approval — use the exact format from `get_report_summary_with_data()`.
- The crime category breakdown must exclude backfill rows from the 7-Day column (filter on `Period == '7-Day'`, not `IsCurrent7DayCycle == True`).
- Preserve the Notes section including the HPD HTML style reference.

## Output Format

```
## Report Summary Preview — [CYCLE_NAME]

### Changes from current version:
- Total Incidents: [old] -> [new]
- 7-Day Period: [old] -> [new]
- [etc.]

### Full Preview:
[Complete markdown content]

---
Write to: [path to SCRPA_Report_Summary.md]
Confirm? (y/n)
```
