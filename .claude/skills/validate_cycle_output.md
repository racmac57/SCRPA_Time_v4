Validate a completed SCRPA cycle folder for data integrity — row counts, period sums, lag correctness, JSON/CSV alignment, and report summary accuracy.

## When to Use

- After every pipeline run (`run_scrpa_pipeline.py`), before distributing the cycle folder.
- When the user says "validate", "check output", "verify cycle", or invokes `/validate-cycle-output`.
- Before starting the ChatGPT tactical briefing workflow.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. At minimum:

1. `CLAUDE.md` (repo root) — critical logic rules
2. `Documentation/data_dictionary.json` — field definitions and column names
3. The cycle folder's `Data/` and `Documentation/` contents (identified below)

## Interface Contract

**Input**: One of:
- A user-supplied cycle folder path (e.g., `Time_Based/2026/26C03W12_26_03_24/`)
- Nothing — the skill auto-discovers the latest cycle folder

**Output**: A numbered checklist of 7 checks, each scored PASS=1 or FAIL=0, plus regression checks. Total score as N/7. No files are created or modified.

**Mode**: READ-ONLY. This skill never writes, modifies, or deletes any file.

## Auto-Discovery Logic

When no cycle folder is provided:

1. Get the current year (e.g., `2026`).
2. List directories under `Time_Based/{YEAR}/`.
3. Sort by directory name descending (cycle names encode dates: `26C03W12_26_03_24`).
4. Use the first (most recent) folder.
5. Verify these four files exist inside it before proceeding:
   - `Data/SCRPA_All_Crimes_Enhanced.csv`
   - `Data/SCRPA_7Day_With_LagFlags.csv`
   - `Data/SCRPA_7Day_Summary.json`
   - `Documentation/SCRPA_Report_Summary.md`

If any file is missing, report it as FAIL (file not found) for the relevant check — do not skip silently.

## Required Column Names

From `Documentation/data_dictionary.json` — use these exact names in all checks:

| Column | Type | Key Rule |
|--------|------|----------|
| `Report_Date_ForLagday` | date | `Coalesce(Report_Date, EntryDate)` — NO Incident_Date fallback |
| `LagDays` | integer | `CycleStart_7Day - Incident_Date` (NOT Report_Date - Incident_Date) |
| `IsLagDay` | boolean | Incident before cycle containing Report_Date_ForLagday |
| `Backfill_7Day` | boolean | Incident before cycle, reported during current 7-day window |
| `IsCurrent7DayCycle` | boolean | Report_Date_ForLagday in current 7-day window |
| `Period` | string | `7-Day` / `28-Day` / `YTD` / `Prior Year` / `Historical` |
| `IncidentToReportDays` | integer | `Report_Date - Incident_Date` (reporting delay, NOT LagDays) |
| `Crime_Category` | string | MVT / Burglary Auto / Burglary - Comm & Res / Robbery / Sexual Offenses / Other |
| `Incident_Date_Date` | date | Best incident date: `Coalesce(Incident Date, Incident Date_Between, Report Date)` |

## Steps

1. **Identify the cycle folder.** If the user provides a path, use it. Otherwise, use the auto-discovery logic above.

2. **Read the four core files** from the cycle folder:
   - `Data/SCRPA_All_Crimes_Enhanced.csv`
   - `Data/SCRPA_7Day_With_LagFlags.csv`
   - `Data/SCRPA_7Day_Summary.json`
   - `Documentation/SCRPA_Report_Summary.md`

3. **Check 1 — Row count (PASS=1 / FAIL=0).** Count rows in `SCRPA_All_Crimes_Enhanced.csv`. Parse "Total Incidents" from `SCRPA_Report_Summary.md` Data Summary table. Report both numbers.

4. **Check 2 — Period sum (PASS=1 / FAIL=0).** From `SCRPA_All_Crimes_Enhanced.csv`, count rows per `Period` value. Verify:
   - `7-Day + 28-Day + YTD + Prior Year` = Total Incidents
   - **Historical rows are excluded** from this sum — they represent pre-current-year-minus-one data
   - Each period count matches the corresponding row in `SCRPA_Report_Summary.md`

5. **Check 3 — 7-Day CSV integrity (PASS=1 / FAIL=0).** Verify every row in `SCRPA_7Day_With_LagFlags.csv` has `IsCurrent7DayCycle == True`. Report count and any violating rows with `Case Number`.

6. **Check 4 — Backfill ⊆ IsLagDay (PASS=1 / FAIL=0).** In `SCRPA_All_Crimes_Enhanced.csv`, verify that every row with `Backfill_7Day == True` also has `IsLagDay == True`. Report any violations with `Case Number` and `Incident_Date_Date`.

7. **Check 5 — LagDays formula spot-check (PASS=1 / FAIL=0).** For up to 5 rows where `IsLagDay == True`:
   - Verify `LagDays > 0` (must be positive for lag rows)
   - Verify `LagDays != IncidentToReportDays` unless coincidental (flag but don't fail if only 1-2 matches out of 5)
   - If the cycle calendar is available, verify: `LagDays == (CycleStart_7Day - Incident_Date_Date).days`
   - If no `IsLagDay == True` rows exist, report PASS=1 with note "0 lag incidents"

8. **Check 6 — JSON/CSV alignment (PASS=1 / FAIL=0).** Compare `SCRPA_7Day_Summary.json` counts against the CSV:
   - `counts.total_7day_window` == number of rows in `SCRPA_7Day_With_LagFlags.csv`
   - `counts.lag_incidents` == count of rows where `Backfill_7Day == True` in the 7-day CSV
   - `counts.backfill_7day` == count of `Backfill_7Day == True` in enhanced CSV
   - `lag_analysis.lagdays_distribution.mean/median/max` are plausible (non-negative, max >= median >= 0)

9. **Check 7 — Report Summary alignment (PASS=1 / FAIL=0).** Verify that `SCRPA_Report_Summary.md`:
   - "Lag Incidents" matches `counts.lag_incidents` from JSON
   - Crime Category Breakdown 7-Day column sums to the 7-Day period count
   - Lag Day Analysis mean/median/max match JSON (or both show "-" when no lag incidents)

10. **Report results** using the binary output format below.

## Regression Checks

After the 7 main checks, run these additional regression checks and report them in the output. These do NOT affect the main score but are reported as warnings.

### v2.0.0 Regressions

1. **Backfill leaking into 7-Day period**: Count rows where `Backfill_7Day == True AND Period == '7-Day'`. This should be 0 — backfill rows have `Incident_Date` before the cycle window, so their Period should NOT be `7-Day`. Report count.

2. **LagDays vs IncidentToReportDays confusion**: For all rows where `IsLagDay == True AND LagDays > 0`, check how many have `LagDays == IncidentToReportDays`. A high ratio (>50%) suggests the pipeline is incorrectly using `Report_Date - Incident_Date` instead of `CycleStart_7Day - Incident_Date`. Report ratio.

3. **Historical period exclusion**: Count `Period == 'Historical'` rows. These must be excluded from the period sum in Check 2. Report count.

### v1.9.x Regressions

4. **Required columns present**: Verify all 9 required columns exist in the enhanced CSV: `Report_Date_ForLagday`, `IsCurrent7DayCycle`, `Backfill_7Day`, `IsLagDay`, `LagDays`, `Period`, `IncidentToReportDays`, `Crime_Category`, `Incident_Date_Date`. Report any missing.

5. **No stale data**: Verify the JSON `cycle.name` matches the cycle folder name prefix (e.g., folder `26C03W12_26_03_24` should have `cycle.name == "26C03W12"`).

## Guardrails

- **Do not modify any file. Report findings only.**
- Never change data in CSVs, JSON, or markdown files.
- Never re-run the pipeline or any transform scripts.
- Never create any output files (no logs, no reports, no temp files).
- Never simplify or reinterpret the five critical logic rules:
  1. `Report_Date_ForLagday = Coalesce(Report_Date, EntryDate)` — NO `Incident_Date` fallback
  2. `LagDays = CycleStart_7Day - Incident_Date` (NOT `Report_Date - Incident_Date`)
  3. `IsLagDay` derived from `Report_Date_ForLagday` cycle resolution (3-tier)
  4. `Backfill_7Day`: `Incident_Date < CycleStart AND Report_Date_ForLagday IN [CycleStart, CycleEnd]`
  5. Period priority: `7-Day > Prior Year > 28-Day > YTD > Historical` (based on `Incident_Date`, NOT `Report_Date`)
- If a file is missing, report it as FAIL=0 (file not found) — do not skip the check silently.
- All paths must be resolved relative to the SCRPA project root or use `pathlib` — never hardcode `C:\Users\...` paths.

## Output Format

Use binary scoring: PASS=1, FAIL=0. No partial credit.

```
## SCRPA Cycle Validation — [CYCLE_NAME]
Folder: [path]

1. Row Count:          PASS=1|FAIL=0 — Enhanced CSV: N rows, Report Summary: N
2. Period Sum:         PASS=1|FAIL=0 — 7-Day(N) + 28-Day(N) + YTD(N) + Prior Year(N) = N [== | !=] Total(N), Historical(N excluded)
3. 7-Day CSV Filter:   PASS=1|FAIL=0 — All N rows have IsCurrent7DayCycle=True [or: N violations: Case X, Case Y]
4. Backfill ⊆ IsLagDay: PASS=1|FAIL=0 — N backfill rows, all have IsLagDay=True [or: N violations: Case X]
5. LagDays Spot-Check: PASS=1|FAIL=0 — Checked N rows, N issues [details per row if FAIL]
6. JSON/CSV Alignment: PASS=1|FAIL=0 — total_7day: JSON=N/CSV=N, lag: JSON=N/CSV=N, backfill: JSON=N/CSV=N
7. Report Summary:     PASS=1|FAIL=0 — lag: MD=N/JSON=N, cat_7day_sum=N/period_7day=N

--- Regression Checks ---
- v2.0.0 Backfill in 7-Day: N rows (expect 0)
- v2.0.0 LagDays==ITRD: N/M lag rows (suspicious if ratio > 50%)
- v2.0.0 Historical excluded: N rows
- v1.9.x Required columns: [None missing | list]
- v1.9.x Stale data: JSON cycle=[name] vs folder=[name] [MATCH|MISMATCH]

Result: N/7 PASSED — [CLEAN | ACTION REQUIRED]
```
