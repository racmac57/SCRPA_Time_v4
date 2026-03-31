# SCRPA Skill Regression Test Catalog

Generated: 2026-03-30
Cross-skill regression agent run against 6 hardened skills.

## Known Historical Bugs

### Bug 1: v2.0.0 -- LagDays vs IncidentToReportDays confusion

**Description**: Pipeline used `LagDays` (CycleStart - Incident_Date) where `IncidentToReportDays` (Report_Date - Incident_Date) was correct for reporting delay stats and crime category lag averages.

**Guarding skills**:
- `check_lag_logic.md` -- Step 6 (Rule 5: LagDays vs IncidentToReportDays separation) + Step 7a regression check
- `validate_cycle_output.md` -- Regression check "LagDays vs IncidentToReportDays confusion" (ratio >50% detection)
- `review_pipeline_change.md` -- Category A (Lag/Backfill Logic) + F1 regression pattern

**Verification**: Grep `prepare_7day_outputs.py` for `['LagDays']` in summary/distribution logic -- must return 0 matches. All lag metric computations must use `IncidentToReportDays`. In output data, check ratio of `LagDays == IncidentToReportDays` among IsLagDay=True rows; ratio >50% indicates regression.

**Status**: COVERED

---

### Bug 2: v2.0.0 -- Backfill leaking into 7-Day crime category counts

**Description**: Crime category breakdown filtered on `IsCurrent7DayCycle == True` instead of `Period == '7-Day'`, which included backfill rows and inflated 7-Day totals.

**Guarding skills**:
- `check_lag_logic.md` -- Step 6a + Step 7b regression check
- `check_period_logic.md` -- Part A check 4 (v2.0.0 Regression: Backfill exclusion) + Part B check 7 (Backfill Leak Check)
- `validate_cycle_output.md` -- Regression check "Backfill leaking into 7-Day period" (count rows where Backfill_7Day=True AND Period='7-Day')
- `review_pipeline_change.md` -- Category B (Period Classification) + F2 regression pattern

**Verification**: In `prepare_7day_outputs.py`, verify crime category breakdown filters on `Period == '7-Day'`, NOT `IsCurrent7DayCycle == True`. In output data, count rows where `Backfill_7Day == True AND Period == '7-Day'` -- must be 0.

**Status**: COVERED

---

### Bug 3: v2.0.0 -- Stale HTML data (pipeline ordering)

**Description**: Pipeline Step 6b copied HTML before Step 6a generated it via SCRPA_ArcPy, resulting in stale data in the cycle folder.

**Guarding skills**:
- `review_pipeline_change.md` -- F3 regression pattern

**Verification**: In any pipeline change review, verify Step 6a (generate HTML via SCRPA_ArcPy) occurs BEFORE Step 6b (copy HTML). Any reordering is flagged CRITICAL.

**Status**: COVERED

---

### Bug 4: v1.9.2 -- Scripts blocking on stdin in batch mode

**Description**: `input()`, `safe_input()`, or stdin reads without `<nul` redirection or TTY guard caused scripts to hang when run in batch/automated mode.

**Guarding skills**:
- `review_pipeline_change.md` -- Category E (Subprocess & Error Handling) + F4 regression pattern

**Verification**: Grep diff for `input(`, `safe_input(`, `sys.stdin` without batch-mode guards. Any occurrence without TTY check or `<nul` redirection is flagged WARNING.

**Status**: COVERED

---

### Bug 5: v1.9.1 -- Cycle calendar date gap (missing 01/06/2026)

**Description**: Missing row for 01/06/2026 in the cycle calendar CSV created a Tier 2 cycle resolution lookup hole. Dates not covered by any `7_Day_Start..7_Day_End` range cause `resolve_cycle()` to fall through to Tier 3 (wrong cycle).

**Guarding skills**:
- `check_cycle_calendar.md` -- Check 2 (7-Day window coverage) + explicit v1.9.1 regression check for 01/06/2026
- `review_pipeline_change.md` -- F5 regression pattern

**Verification**: In cycle calendar validation, verify 01/06/2026 is covered by at least one 7-day window. Check 2 detects unexpected gaps between consecutive 7-day windows.

**Status**: COVERED

---

### Bug 6: v1.9.2 -- WinError 5 from deleting in-use folders

**Description**: `shutil.rmtree()` on in-use folders caused `WinError 5` (Access Denied). Fix was to use reuse-or-skip pattern instead of delete-and-recreate.

**Guarding skills**:
- `review_pipeline_change.md` -- F6 regression pattern

**Verification**: Grep diff for `shutil.rmtree()` or folder deletion. Any new occurrence is flagged with recommendation to use reuse-or-skip pattern.

**Status**: COVERED

---

### Bug 7: v1.2.0 -- Path case sensitivity (exports folder)

**Description**: Exports path used uppercase `SCRPA` (`05_EXPORTS\_RMS\SCRPA\`) instead of lowercase `scrpa`, causing `FileNotFoundError` on case-sensitive filesystems and OneDrive sync issues.

**Guarding skills**:
- `check_paths.md` -- Check 4 (Case sensitivity in exports path, v1.2.0 regression)
- `review_pipeline_change.md` -- Category C (Path Correctness)

**Verification**: Grep for `_RMS[/\\]SCRPA[^_]` (uppercase in exports path, excluding `SCRPA_ArcPy`). Must return 0 matches.

**Status**: COVERED

---

## Cross-Skill Coverage Matrix

| Bug | validate_cycle_output | check_lag_logic | check_cycle_calendar | review_pipeline_change | check_paths | check_period_logic |
|-----|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| v2.0.0 LagDays/ITRD | X | X | | X | | |
| v2.0.0 Backfill leak | X | X | | X | | X |
| v2.0.0 Stale HTML | | | | X | | |
| v1.9.2 stdin block | | | | X | | |
| v1.9.1 calendar gap | | | X | X | | |
| v1.9.2 WinError 5 | | | | X | | |
| v1.2.0 path case | | | | X | X | |

## Summary

- **7 known historical bugs** cataloged
- **All 7** are COVERED by at least one hardened skill
- `review_pipeline_change.md` provides broadest coverage (all 6 CHANGELOG bugs)
- `validate_cycle_output.md` and `check_lag_logic.md` provide deep coverage for the v2.0.0 data integrity bugs
- No coverage gaps detected
