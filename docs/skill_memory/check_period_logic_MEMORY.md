# check_period_logic Skill Memory

## Latest Iteration

- **Date**: 2026-03-30
- **Iteration**: 1
- **Score**: 9/9

## Per-Test Binary Scores

| Test | Description | Score |
|------|-------------|-------|
| T1 | Skill doc specifies both code checks and data checks | 1 |
| T2 | Paths resolved safely (Path(), raw strings, carucci_r only) | 1 |
| T3 | Provably read-only (guardrails section explicit, no write ops) | 1 |
| T4 | Both code search and data validation ran with captured output | 1 |
| T5 | Output includes file:line for code checks and row counts for data | 1 |
| T6 | Enforces all 5 critical logic rules (especially Period priority) | 1 |
| T7 | Catches v2.0.0 backfill-leaking-into-7-Day bug | 1 |
| T8 | Memory file updated | 1 |
| T9 | All tests = 1 | 1 |

## Evidence

### Code Checks (scrpa_transform.py)

- **Priority Order**: `classify_period()` at line 410-457. Returns in order: 7-Day (line 441), Prior Year (line 445), 28-Day (line 450), YTD (line 454), Historical (line 457). Prior Year checked BEFORE 28-Day. PASS.
- **Based on Incident_Date**: Function signature `classify_period(incident_date, ...)` at line 410-411. No reference to Report_Date in the function body. PASS.
- **7-Day Window Boundaries**: Uses `cycle_start_7 <= incident_date <= cycle_end_7` at line 440. No relative date math. PASS.

### Code Checks (prepare_7day_outputs.py)

- **Backfill Exclusion**: Crime category breakdown at line 193-209 filters `df_7day[df_7day['Period'] == '7-Day']` (line 195), NOT `IsCurrent7DayCycle`. PASS.
- **Lag category breakdown**: Also filters on `Period == '7-Day'` at line 185. PASS.

### Data Checks (26C03W12_26_03_24 fixture)

```
Period Distribution:
  28-Day: 9
  7-Day: 3
  Prior Year: 232
  YTD: 25
  TOTAL: 269

Backfill Leak: 0 rows (Backfill_7Day=True AND Period=7-Day) — PASS
Prior Year Validation: All years = [2025] — PASS
28-Day Year Check: All years = [2026], no prior-year rows — PASS
_Period_Debug: PRESENT, sample: "dI=2026/02/11 | HasCycle=true | ReportDue=2026/03/24 | CycleStart=2026/03/17 | CycleEnd=2026/03/23 | in7Day=false | in28..."
```

## Changes Made

Hardened `.claude/skills/check_period_logic.md`:
- Added "Key Column Names" section listing Period, Incident_Date_Date, Backfill_7Day, IsCurrent7DayCycle, Crime_Category, _Period_Debug, IncidentToReportDays
- Added explicit grep patterns for finding Period classification (`def classify_period`, `cycle_start_7 <= incident_date <= cycle_end_7`, `Period.*==.*7-Day`)
- Split steps into Part A (Code Checks), Part B (Data Checks), Part C (Report)
- Added v2.0.0 regression check #4: crime category breakdown MUST filter on `Period=='7-Day'`, NOT `IsCurrent7DayCycle==True`
- Added v2.0.0 regression check #5: `Backfill_7Day=True` rows MUST NOT have `Period='7-Day'`
- Added note about `_Period_Debug` column (may not be present in all outputs)
- Changed output format to binary PASS=1/FAIL=0 with file:line references
- Added path safety note in Guardrails
- Expanded data checks to 5 numbered items (6-10) with explicit criteria

## Remaining Gaps

None. All 9 tests pass.
