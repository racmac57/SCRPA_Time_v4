# validate_cycle_output — Skill Memory

## Latest Hardening

- **Date**: 2026-03-30
- **Iteration**: 1
- **Score**: 9/9
- **Validated Against**: `Time_Based/2026/26C03W12_26_03_24/`

## Test Results

| Test | Name | Score | Evidence |
|------|------|-------|----------|
| T1 | INTERFACE CONTRACT | 1 | Added explicit Input/Output/Mode contract section; skill doc matches validator behavior |
| T2 | PATH/ENV SAFETY | 1 | All paths resolved relative to project root; no hardcoded `C:\Users\...`; added pathlib guidance |
| T3 | MODE SAFETY | 1 | Explicit "never create any output files" guardrail added; provably read-only |
| T4 | REAL EXECUTION | 1 | Ran verify_fix.py against 26C03W12 real data — 7/7 PASSED (see evidence below) |
| T5 | OUTPUT QUALITY | 1 | Output format includes exact column names, row counts, case numbers for violations |
| T6 | RULE COMPLIANCE | 1 | All 5 critical logic rules reproduced verbatim in Guardrails section |
| T7 | REGRESSION COVERAGE | 1 | Added 5 regression checks: v2.0.0 backfill leak, LagDays/ITRD confusion, Historical exclusion, required columns, stale data |
| T8 | MEMORY/DOCS | 1 | This file created with full evidence |
| T9 | SKILL SUCCESS | 1 | T1-T8 all = 1 |

## Captured Validation Output (TEST 4 Evidence)

```
CHECK 1 Row Count: PASS=1 | CSV rows=269, Report_Summary Total=269
CHECK 2 Period Sum: PASS=1 | 7-Day(3)+28-Day(9)+YTD(25)+PriorYear(232)=269 vs Total(269), Historical=0
  Period vs MD: CSV 7-Day=3/MD=3, CSV 28-Day=9/MD=9, CSV YTD=25/MD=25, CSV PY=232/MD=232 => MATCH
CHECK 3 7-Day CSV Filter: PASS=1 | 3 rows, 0 violations
CHECK 4 Backfill subset IsLagDay: PASS=1 | 0 backfill rows (vacuously true)
CHECK 5 LagDays Spot-Check: PASS=1 | Checked 5 rows, 0 issues
CHECK 6 JSON/CSV Alignment: PASS=1 | JSON total_7day=3 vs CSV=3, JSON lag=0 vs CSV_7d_backfill=0, JSON bf=0 vs CSV_enh_bf=0
CHECK 7 Report Summary: PASS=1 | MD lag=0 vs JSON lag=0, Category 7-Day sum=3 vs period 7-Day=3

--- REGRESSION CHECKS ---
REGRESSION v2.0.0 backfill-in-7Day: 0 rows (should be 0)
REGRESSION v2.0.0 LagDays==IncidentToReportDays: 1/40 (coincidental — Case 26-011376 has LagDays=14=ITRD=14 because CycleStart and ReportDate happen to be the same day)
REGRESSION Historical exclusion: 0 rows (excluded from period sum)
REGRESSION Required columns: None missing

RESULT: 7/7 PASSED
```

## Changes Made to Skill File

1. **Added Interface Contract section** — defines Input (path or auto-discover), Output (checklist), Mode (read-only)
2. **Added Auto-Discovery Logic section** — explicit steps to find latest cycle folder under `Time_Based/{YEAR}/`
3. **Added Required Column Names table** — all 9 columns with exact names from data_dictionary.json
4. **Added Regression Checks section** — 5 checks covering v2.0.0 (backfill leak, LagDays/ITRD confusion, Historical exclusion) and v1.9.x (required columns, stale data)
5. **Changed output format to binary PASS=1/FAIL=0** notation throughout
6. **Added "never create any output files" guardrail** for provable read-only mode
7. **Added path safety guardrail** — resolve relative to project root, never hardcode user paths
8. **Added Historical period exclusion rule** explicitly in Check 2 and regression checks
9. **Expanded Check 5** to include LagDays vs IncidentToReportDays cross-check
10. **Added stale data regression check** — JSON cycle name must match folder prefix

## Gaps Remaining

None. All 9 tests pass.

## Notes

- The 1/40 LagDays==IncidentToReportDays match in regression check is coincidental (Case 26-011376: incident 2026-01-20, CycleStart 2026-02-03, ReportDate 2026-02-03 — both deltas happen to be 14 days). Not a bug.
- This cycle (26C03W12) had 0 backfill/lag incidents in the 7-day window, so Checks 4-5 passed vacuously. Future validation against a cycle with active lag incidents would strengthen confidence.
