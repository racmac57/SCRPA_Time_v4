Verify Period classification priority and ensure backfill rows do not leak into 7-Day crime category totals.

## When to Use

- After any edit to `scripts/scrpa_transform.py` or `scripts/prepare_7day_outputs.py` that touches Period assignment.
- When validating a cycle's data and period counts look wrong.
- When the user says "check period logic", "verify periods", or invokes `/check-period-logic`.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. `scripts/scrpa_transform.py` — Period classification logic
2. `scripts/prepare_7day_outputs.py` — 7-Day crime category breakdown
3. The cycle folder's `Data/SCRPA_All_Crimes_Enhanced.csv` (if validating data)

## Key Column Names

- `Period` — classification result: `7-Day`, `Prior Year`, `28-Day`, `YTD`, `Historical`
- `Incident_Date_Date` — parsed incident date (used for Period classification)
- `Backfill_7Day` — boolean, True when incident occurred before cycle but was reported during cycle
- `IsCurrent7DayCycle` — boolean, True when Report_Date_ForLagday falls in current 7-day window
- `Crime_Category` — crime type grouping used in 7-Day breakdown
- `_Period_Debug` — diagnostic string (may not be present in all outputs)
- `IncidentToReportDays` — days between incident and report (for reporting lag tracking)

## Steps

### Part A: Code Checks

Use grep/search to locate and verify the following. Report `file:line` for each finding.

**1. Priority Order** — Search `scrpa_transform.py` for function `classify_period` (grep pattern: `def classify_period`). Verify the if/elif chain follows this exact priority:
   ```
   7-Day > Prior Year > 28-Day > YTD > Historical
   ```
   Specifically verify that `Prior Year` is checked BEFORE `28-Day` (grep: `Prior Year.*before.*28-Day` or inspect the ordering of return statements). This prevents previous-year incidents from being misclassified as `28-Day`.

**2. Based on Incident_Date** — In `classify_period`, verify the first parameter is `incident_date` (grep: `def classify_period.*incident_date`). Confirm the function does NOT reference `Report_Date` or `Report_Date_ForLagday` for period assignment.

**3. 7-Day Window Boundaries** — Verify that 7-Day classification uses `cycle_start_7` and `cycle_end_7` parameters from the cycle calendar (grep: `cycle_start_7 <= incident_date <= cycle_end_7`). Must NOT use relative date math like `today - timedelta(days=7)`.

**4. v2.0.0 Regression: Backfill exclusion from crime category breakdown** — In `prepare_7day_outputs.py`, search for the crime category breakdown (grep: `by_crime_category` or `Crime_Category.*groupby`). Verify it filters on `Period == '7-Day'` (grep: `Period.*==.*7-Day`), NOT on `IsCurrent7DayCycle == True`. The `IsCurrent7DayCycle` filter includes backfill rows, which would inflate 7-Day totals. This was the v2.0.0 critical fix.

**5. v2.0.0 Regression: Backfill_7Day=True rows MUST NOT have Period='7-Day'** — This is enforced by the classify_period logic: since backfill incidents have Incident_Date before cycle_start_7, they cannot satisfy `cycle_start_7 <= incident_date <= cycle_end_7`. Verify this invariant holds in the code.

### Part B: Data Checks

If a cycle folder or `SCRPA_All_Crimes_Enhanced.csv` is available, run a Python script (read-only, no file writes) to validate:

**6. Period Distribution** — Count rows per `Period` value and report totals.

**7. Backfill Leak Check** — Count rows where `Backfill_7Day == True AND Period == '7-Day'`. Must be 0. If non-zero, the backfill leak bug has regressed.

**8. Prior Year Validation** — Verify all `Period == 'Prior Year'` rows have `Incident_Date_Date.year` in the previous calendar year (e.g., 2025 when current year is 2026).

**9. 28-Day Year Check** — Verify no `Period == '28-Day'` rows have `Incident_Date_Date.year` in the previous calendar year. If any exist, Prior Year priority is broken.

**10. _Period_Debug Inspection** — Check if `_Period_Debug` column exists. If present, report 2-3 sample values. This column is diagnostic and may not be in all outputs.

### Part C: Report

Report all findings with `file:line` references for code checks and row counts for data checks. Use the binary output format below.

## Guardrails

- **READ-ONLY. Do not modify any source file, script, or data file. Report findings only.**
- Never change Period classification logic.
- Never reinterpret the priority order — it is intentional that Prior Year is checked before 28-Day.
- Path resolution: use `Path()` or raw strings for OneDrive paths. Never hardcode user profile names other than `carucci_r`.
- The five critical logic rules apply here:
  1. `Report_Date_ForLagday = Coalesce(Report_Date, EntryDate)` — NO `Incident_Date` fallback
  2. `LagDays = CycleStart_7Day - Incident_Date` (NOT `Report_Date - Incident_Date`)
  3. `IsLagDay` derived from `Report_Date_ForLagday` cycle resolution
  4. `Backfill_7Day`: `Incident_Date < CycleStart AND Report_Date_ForLagday IN [CycleStart, CycleEnd]`
  5. Period priority: `7-Day > Prior Year > 28-Day > YTD > Historical` (based on `Incident_Date`, NOT `Report_Date`)

## Output Format

Use PASS=1, FAIL=0. No partial credit.

```
## Period Logic Audit

### Code Checks
1. Priority Order:              [1|0] — [details with file:line]
2. Based on Incident_Date:      [1|0] — [details with file:line]
3. 7-Day Window Boundaries:     [1|0] — [details with file:line]
4. Backfill Exclusion (v2.0.0): [1|0] — [details with file:line]
5. Backfill!=7-Day Invariant:   [1|0] — [details with file:line]

### Data Checks (if CSV provided)
6. Period Distribution:         [counts per period]
7. Backfill Leak Check:         [1|0] — [N rows with Backfill_7Day=True AND Period=7-Day]
8. Prior Year Validation:       [1|0] — [all in previous year?]
9. 28-Day Year Check:           [1|0] — [any previous-year rows in 28-Day?]
10. _Period_Debug Column:       [present|absent] — [sample values if present]

Result: [N/N checks PASSED] — [CLEAN | ACTION REQUIRED]
```
