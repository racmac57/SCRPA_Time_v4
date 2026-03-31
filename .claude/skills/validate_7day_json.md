Cross-check SCRPA_7Day_Summary.json counts against the 7-day CSV and report summary markdown for a given cycle.

## When to Use

- After every pipeline run, as part of output validation.
- When JSON counts look suspicious or don't match the report summary.
- When the user says "validate JSON", "check 7-day summary", or invokes `/validate-7day-json`.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting.

## Steps

1. **Identify the cycle folder.** If the user provides a path, use it. Otherwise, find the most recently modified folder under `Time_Based/YYYY/`.

2. **Read the three files:**
   - `Data/SCRPA_7Day_Summary.json`
   - `Data/SCRPA_7Day_With_LagFlags.csv`
   - `Documentation/SCRPA_Report_Summary.md`

3. **Check 1 — JSON structure.** Verify the JSON contains the expected top-level keys: `counts`, `lag_analysis`, `7day_by_crime_category`. Report any missing keys.

4. **Check 2 — Total 7-Day count.** Compare `counts.total_7day` in JSON against the actual row count in `SCRPA_7Day_With_LagFlags.csv`. They must match exactly.

5. **Check 3 — Lag incidents count.** Compare `counts.lag_incidents` in JSON against the count of rows where `Backfill_7Day == True` in the 7-day CSV. These represent lag incidents within the 7-day window specifically (not the full-dataset `IsLagDay` count).

6. **Check 4 — Lag distribution plausibility.** Check `lag_analysis.lagdays_distribution`:
   - `mean` should be >= 0
   - `median` should be >= 0
   - `max` should be >= `median` >= 0
   - If all values are 0 or "-", verify there are actually no lag incidents (consistent with `counts.lag_incidents == 0`)

7. **Check 5 — Crime category breakdown.** Compare `7day_by_crime_category` in JSON:
   - Sum of all category counts should equal the 7-Day period count (rows with `Period == '7-Day'`, NOT total 7-day CSV rows which include backfill)
   - Expected categories: `Motor Vehicle Theft`, `Burglary Auto`, `Burglary - Comm & Res`, `Robbery`, `Sexual Offenses`, `Other`
   - Report any unexpected category names

8. **Check 6 — Report Summary alignment.** Parse the `SCRPA_Report_Summary.md` tables and verify:
   - "Lag Incidents" count matches `counts.lag_incidents` from JSON
   - "7-Day Period" count matches the sum of crime category 7-Day column
   - Lag Day Analysis (mean/median/max) matches JSON distribution values

9. **Report results** as a numbered checklist.

## Guardrails

- **Do not modify any file. Report findings only.**
- Never edit the JSON, CSV, or markdown files.
- Distinguish between two scopes of lag counts:
  - Pipeline console "Lag incidents: N" = all `IsLagDay=True` across the full dataset
  - Report Summary "Lag Incidents: N" = lag rows within the 7-day window only (`Backfill_7Day=True` in 7-day CSV)
  Both are correct but measure different things. Do not flag this difference as an error.

## Output Format

```
## 7-Day JSON Validation — [CYCLE_NAME]

1. JSON Structure:      [PASS|FAIL] — [keys present/missing]
2. Total 7-Day Count:   [PASS|FAIL] — JSON: N, CSV rows: N
3. Lag Incidents:        [PASS|FAIL] — JSON: N, CSV Backfill_7Day=True: N
4. Lag Distribution:     [PASS|FAIL] — mean=X, median=X, max=X [plausible|implausible]
5. Category Breakdown:   [PASS|FAIL] — sum=N, 7-Day period count=N [match|mismatch]
6. Report Summary:       [PASS|FAIL] — [alignment details]

Result: [N/6 PASSED] — [CLEAN | ACTION REQUIRED]
```
