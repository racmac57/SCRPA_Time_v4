SCRPA-aware code review for changes to pipeline scripts — catches domain-specific bugs that a generic reviewer would miss: lag/backfill logic, path correctness, cycle calendar assumptions, and known regression patterns.

## When to Use

- Before committing any change to files in `scripts/`.
- When the user says "review changes", "review pipeline", or invokes `/review-pipeline-change`.
- After modifying `scrpa_transform.py`, `prepare_7day_outputs.py`, `run_scrpa_pipeline.py`, or `generate_documentation.py`.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. The git diff of changed files (`git diff` or `git diff --staged` for `scripts/`)
2. `CHANGELOG.md` — to check for known regression patterns from previous fixes

## Steps

1. **Get the diff.** Run `git diff scripts/` and `git diff --staged scripts/` to see all pending changes. If both commands return empty output, report:
   ```
   ## SCRPA Pipeline Change Review
   No changes detected in scripts/. Nothing to review.
   ```
   and stop. Do NOT ask the user for files or proceed with empty analysis.

2. **Category A — Lag/Backfill Logic.** Scan the diff for any changes to these columns or their computation:
   - `Report_Date_ForLagday` — must remain `Coalesce(Report_Date, EntryDate)` with NO `Incident_Date` fallback
   - `LagDays` — must remain `CycleStart_7Day - Incident_Date` (NOT `Report_Date - Incident_Date`)
   - `IsLagDay` — must use `Report_Date_ForLagday` for cycle resolution
   - `Backfill_7Day` — must check `Incident_Date < CycleStart AND Report_Date_ForLagday IN [CycleStart, CycleEnd]`
   - `IncidentToReportDays` — must remain `Report_Date - Incident_Date` (reporting delay, separate from `LagDays`)
   - Flag any change that confuses `LagDays` (cycle-relative) with `IncidentToReportDays` (reporting delay) — this was the v2.0.0 critical fix.

3. **Category B — Period Classification.** Check for changes to `Period` assignment:
   - Priority must remain: `7-Day > Prior Year > 28-Day > YTD > Historical`
   - `Prior Year` must be checked BEFORE `28-Day` to prevent previous-year incidents from appearing in 28-Day
   - Period must be based on `Incident_Date` (NOT `Report_Date`)
   - 7-Day crime category breakdown must filter on `Period == '7-Day'` (excludes backfill), NOT `IsCurrent7DayCycle == True`

4. **Category C — Path Correctness.** Scan for:
   - `RobertCarucci` instead of `carucci_r` in any path string
   - `PowerBI_Date` instead of `PowerBI_Data`
   - Case mismatches: `SCRPA` vs `scrpa` in cross-project paths (the exports folder uses lowercase `scrpa`)
   - Hardcoded paths that should use `Path()` or config constants
   - New paths that don't use the canonical OneDrive root (`C:\Users\carucci_r\OneDrive - City of Hackensack`)

5. **Category D — Cycle Calendar Assumptions.** Check for:
   - New column name assumptions (the calendar has: `Report_Due_Date`, `7_Day_Start`, `7_Day_End`, `28_Day_Start`, `28_Day_End`, `Report_Name`, `BiWeekly_Report_Name`)
   - Changes to `resolve_cycle()` 3-tier logic
   - Hard-coded cycle names or dates that should come from the calendar

6. **Category E — Subprocess and Error Handling.** Check for:
   - New `subprocess.run()` calls MUST include all three: `encoding='utf-8'`, `errors='replace'`, AND `timeout=<seconds>`. Missing any one is a WARNING.
   - Missing `try/except` around file I/O or subprocess calls
   - `sys.path` modifications that don't clean up after themselves
   - Any `input()` or `sys.stdin` reads without batch-mode guards (see v1.9.2 stdin regression)

7. **Category F — Known Regression Patterns.** Cross-reference against `CHANGELOG.md` fixes. Each pattern below was a real production bug — flag ANY diff that could reintroduce it:

   | # | Version | Bug | What to flag |
   |---|---------|-----|--------------|
   | F1 | v2.0.0 (2026-02-10) | `LagDays` vs `IncidentToReportDays` confusion | Any code that uses `LagDays` where `IncidentToReportDays` is correct (reporting delay stats, crime category lag averages) or vice versa. `LagDays = CycleStart - Incident_Date`; `IncidentToReportDays = Report_Date - Incident_Date`. |
   | F2 | v2.0.0 (2026-02-10) | Backfill leaking into 7-Day crime category counts | Crime category breakdown must filter `Period == '7-Day'`, NOT `IsCurrent7DayCycle == True` (the latter includes backfill rows). |
   | F3 | v2.0.0 (2026-02-10) | Stale HTML data (pipeline must generate before copying) | Pipeline Step 6a must generate HTML via SCRPA_ArcPy BEFORE Step 6b copies it. Any reordering is CRITICAL. |
   | F4 | v1.9.2 (2026-01-27) | Scripts blocking on stdin in batch mode | Any `input()`, `safe_input()`, or stdin read without `<nul` redirection or TTY guard. |
   | F5 | v1.9.1 (2026-01-26) | Cycle calendar date gap (01/06/2026 lookup hole) | Any hard-coded cycle dates or calendar edits that could create a lookup gap. |
   | F6 | v1.9.2 (2026-01-27) | WinError 5 from deleting in-use folders | Any `shutil.rmtree()` or folder deletion that should be a reuse-or-skip pattern instead. |

8. **IncidentToReportDays / LagDays verification.** Grep the diff for both terms. If `LagDays` appears in a context where reporting delay is meant (e.g., average lag in summary stats, crime category delay), flag as CRITICAL regression risk (see F1 above). If `IncidentToReportDays` appears in a context where cycle-relative lag is meant, flag the same.

9. **Report findings** organized by category, with risk level (CRITICAL / WARNING / INFO) and file:line references. Each category gets a binary score: PASS=1 (no CRITICAL findings) or FAIL=0 (any CRITICAL finding).

## Guardrails

- **Do not modify any file. Report findings only.**
- Never auto-apply fixes — report the issue and let the user decide.
- Never approve changes that violate the five critical logic rules, even if they "look simpler."
- Do not flag stylistic issues (formatting, naming conventions) unless they create a functional risk.
- If the diff is large (>500 lines), focus on Categories A–D first and note that E–F were not fully reviewed.

## Output Format

```
## SCRPA Pipeline Change Review

Files changed: [list]
Diff source: [git diff scripts/ | git diff --staged scripts/ | both]

### Category A — Lag/Backfill Logic  [PASS=1 | FAIL=0]
[CLEAR | findings with risk level and file:line]

### Category B — Period Classification  [PASS=1 | FAIL=0]
[CLEAR | findings with risk level and file:line]

### Category C — Path Correctness  [PASS=1 | FAIL=0]
[CLEAR | findings with risk level and file:line]

### Category D — Cycle Calendar Assumptions  [PASS=1 | FAIL=0]
[CLEAR | findings with risk level and file:line]

### Category E — Subprocess & Error Handling  [PASS=1 | FAIL=0]
[CLEAR | findings with risk level and file:line]

### Category F — Known Regression Patterns  [PASS=1 | FAIL=0]
[F1-F6 each checked. CLEAR | findings with version reference and file:line]

### Summary
- Critical: N | Warning: N | Info: N
- Category scores: A=X B=X C=X D=X E=X F=X
- Recommendation: [APPROVE | REVIEW REQUIRED | DO NOT MERGE]
```
