Verify that LagDays, IsLagDay, Backfill_7Day, and Report_Date_ForLagday calculations in the SCRPA transform scripts conform to the five critical logic rules.

## When to Use

- After any edit to `scripts/scrpa_transform.py` or `scripts/prepare_7day_outputs.py`.
- When the user says "check lag logic", "verify lag", or invokes `/check-lag-logic`.
- During code review of any PR that touches lag-related fields.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. `scripts/scrpa_transform.py` — contains `build_all_crimes_enhanced()`, `resolve_cycle()`, lag calculation logic
2. `scripts/prepare_7day_outputs.py` — contains `save_7day_outputs()`, lag statistics, crime category breakdown

## Steps

### Step 0: Execute Source Code Search (Required — TEST 4)

Before any analysis, run these grep searches and capture the exact output (file:line + code). These constitute the evidence for every rule check.

**Target files (absolute paths):**
- `scripts/scrpa_transform.py`
- `scripts/prepare_7day_outputs.py`

**Required grep patterns (run ALL of these):**

| Pattern | Purpose | Target |
|---------|---------|--------|
| `Report_Date_ForLagday` | Rule 1: find all assignments | `scrpa_transform.py` |
| `Incident_Date.*Report_Date_ForLagday\|Report_Date_ForLagday.*Incident_Date` | Rule 1: detect forbidden fallback | `scrpa_transform.py` |
| `LagDays` | Rule 2: find formula | `scrpa_transform.py` |
| `Report_Date.*Incident_Date\|Incident_Date.*Report_Date` near `LagDays` | Rule 2: detect wrong formula | `scrpa_transform.py` |
| `IsLagDay` | Rule 3: find derivation | `scrpa_transform.py` |
| `Backfill_7Day` | Rule 4: find condition | `scrpa_transform.py` |
| `IncidentToReportDays` | Rule 5/7: find computation | `scrpa_transform.py` |
| `Period.*7-Day` | Rule 5: verify category filter | `prepare_7day_outputs.py` |
| `IncidentToReportDays` | Rule 5: verify lag stats metric | `prepare_7day_outputs.py` |
| `IsCurrent7DayCycle` | Rule 5/7: detect backfill leak | `prepare_7day_outputs.py` |

Save all grep output as evidence. If a pattern returns no matches, record "0 matches" as evidence.

### Step 1: Read Source Files

Read `scripts/scrpa_transform.py` and `scripts/prepare_7day_outputs.py`. Locate all code that computes or references these exact column names:
- `Report_Date_ForLagday`
- `LagDays`
- `IsLagDay`
- `Backfill_7Day`
- `IncidentToReportDays`
- `IsCurrent7DayCycle`
- `Period`
- `Crime_Category`

### Step 2: Rule 1 — Report_Date_ForLagday fallback chain

Verify that:
```python
Report_Date_ForLagday = Coalesce(Report_Date, EntryDate)
```
There must be **NO** `Incident_Date` fallback. When both `Report_Date` and `EntryDate` are null, `Report_Date_ForLagday` must remain null/NaT, which correctly yields `IsLagDay=False` and `LagDays=0`.

**Grep evidence required:**
- `coalesce_any(d_rd, d_ed)` at line ~943 confirms correct chain
- No match for `Incident_Date` assigned to `Report_Date_ForLagday`

Flag any line that assigns `Incident_Date`, `Incident_Date_Date`, or `Incident Date` to `Report_Date_ForLagday` as **CRITICAL VIOLATION**.

### Step 3: Rule 2 — LagDays formula

Verify that:
```python
LagDays = CycleStart_7Day - Incident_Date
```
where `CycleStart_7Day` is the `7_Day_Start` of the cycle resolved from `Report_Date_ForLagday` (not from `Report_Date` or `Incident_Date`).

**Grep evidence required:**
- `lag_days = (cycle_start_for_report - incident_date).days` at line ~1107
- `cycle_start_for_report = report_cycle['7_Day_Start']` at line ~1097
- `report_cycle = resolve_cycle(calendar_df, report_date_for_lagday)` at line ~1092

Flag any code that computes `LagDays = Report_Date - Incident_Date` as **CRITICAL VIOLATION** (this is `IncidentToReportDays`, a different metric).

### Step 4: Rule 3 — IsLagDay derivation

Verify that `IsLagDay` is derived by:
- Resolving the cycle that contains `Report_Date_ForLagday` (using 3-tier cycle resolution via `resolve_cycle()`)
- Checking `Incident_Date < CycleStart_7Day` for that resolved cycle

**Grep evidence required:**
- `is_lag_day = incident_date < cycle_start_for_report` at line ~1102
- `report_date_for_lagday = row.get('Report_Date_ForLagday')` at line ~1086

Flag any code that uses `Report_Date` (without the `_ForLagday` suffix) for cycle resolution in this context.

### Step 5: Rule 4 — Backfill_7Day condition

Verify the exact condition:
```python
Backfill_7Day = (
    Incident_Date < CycleStart_7Day AND
    Report_Date_ForLagday >= CycleStart_7Day AND
    Report_Date_ForLagday <= CycleEnd_7Day
)
```

**Grep evidence required:**
- `incident_date < current_cycle_start` at line ~1042
- `current_cycle_start <= report_date_for_lagday <= current_cycle_end` at line ~1043

`CycleStart_7Day` and `CycleEnd_7Day` refer to the **current** reporting cycle (the one being processed), not the cycle resolved from `Report_Date_ForLagday`.

Flag any variation that uses different date fields or different cycle boundaries.

### Step 6: Rule 5 — LagDays vs IncidentToReportDays separation

In `prepare_7day_outputs.py`, verify that:

**6a. Crime category breakdown uses `Period == '7-Day'` (NOT `IsCurrent7DayCycle == True`):**
- Grep for `Period.*7-Day` in category groupby logic
- Verify `df_7day_period_only = df_7day[df_7day['Period'] == '7-Day']` at lines ~185, ~195, ~222
- Confirm no category count uses `IsCurrent7DayCycle == True` as filter

**6b. Lag statistics use `IncidentToReportDays` (NOT `LagDays`):**
- Grep for `IncidentToReportDays` in lag distribution logic
- Verify `lag_values = df_7day_period_only['IncidentToReportDays']` at line ~225
- Confirm `lag_incidents` count uses `IncidentToReportDays > 0` at line ~273

**6c. IncidentToReportDays computation in `scrpa_transform.py`:**
- Verify `(rd - idd).days` where `rd = Report_Date` and `idd = Incident_Date_Date` at lines ~957-960
- This is `Report_Date - Incident_Date`, NOT `CycleStart - Incident_Date`

### Step 7: Regression Checks (TEST 7)

Check for known regressions from CHANGELOG v2.0.0:

**7a. LagDays/IncidentToReportDays confusion (v2.0.0 bug):**
- In `prepare_7day_outputs.py`, verify lag statistics do NOT reference `LagDays` column
- Grep `prepare_7day_outputs.py` for `\['LagDays'\]` — should return 0 matches in summary/distribution logic
- Verify all lag metric computations use `IncidentToReportDays`
- Verify `LagDays` does NOT appear in the summary/distribution section of `prepare_7day_outputs.py` (grep: `lagdays_distribution.*LagDays` or `LagDays.*mean|median|max`). The distribution must use `IncidentToReportDays` values, not `LagDays`.

**7b. Backfill leak into 7-Day category counts (v2.0.0 bug):**
- In `prepare_7day_outputs.py`, verify crime category breakdown filters on `Period == '7-Day'`
- NOT on `IsCurrent7DayCycle == True` (which would include backfill rows)
- Grep for `IsCurrent7DayCycle` in category groupby — should appear only in row filtering, not in category counts

### Step 8: Report Findings

Produce output in the format specified below.

## Guardrails

- **This skill is READ-ONLY. Do not modify any file. Report findings only.**
- Never change lag calculation logic, even to "fix" a suspected issue — report it and let the user decide.
- Never simplify or reinterpret the five critical logic rules listed in Steps 2-6.
- If `scrpa_transform.py` uses helper functions for lag calculation that are not directly visible (e.g., imported from another module), note them as "inspect before confirming" rather than asserting correctness.
- Do not confuse `LagDays` (cycle-relative) with `IncidentToReportDays` (reporting delay) in your analysis.
- The five critical logic rules from CLAUDE.md (verbatim):
  1. **Report_Date_ForLagday** = `Coalesce(Report_Date, EntryDate)` — NO `Incident_Date` fallback
  2. **LagDays** = `CycleStart_7Day - Incident_Date` (NOT `Report_Date - Incident_Date`)
  3. **IsLagDay** derived from `Report_Date_ForLagday` cycle resolution (3-tier)
  4. **Backfill_7Day**: `Incident_Date < CycleStart AND Report_Date_ForLagday IN [CycleStart, CycleEnd]`
  5. **Period priority**: `7-Day > Prior Year > 28-Day > YTD > Historical` (based on `Incident_Date`, NOT `Report_Date`)

## Output Format

```
## Lag Logic Audit — SCRPA Transform Scripts

### Rule 1: Report_Date_ForLagday (NO Incident_Date fallback)
Status: PASS=1 | FAIL=0
Location: scrpa_transform.py:NN
Evidence: [exact grep output]

### Rule 2: LagDays = CycleStart_7Day - Incident_Date
Status: PASS=1 | FAIL=0
Location: scrpa_transform.py:NN
Evidence: [exact grep output]

### Rule 3: IsLagDay from Report_Date_ForLagday cycle resolution
Status: PASS=1 | FAIL=0
Location: scrpa_transform.py:NN
Evidence: [exact grep output]

### Rule 4: Backfill_7Day condition
Status: PASS=1 | FAIL=0
Location: scrpa_transform.py:NN
Evidence: [exact grep output]

### Rule 5: LagDays vs IncidentToReportDays separation
Status: PASS=1 | FAIL=0
Location: prepare_7day_outputs.py:NN
Evidence: [exact grep output]

### Regression: LagDays/IncidentToReportDays confusion (v2.0.0)
Status: PASS=1 | FAIL=0
Evidence: [grep for LagDays column usage in prepare_7day_outputs.py]

### Regression: Backfill leak into 7-Day counts (v2.0.0)
Status: PASS=1 | FAIL=0
Evidence: [grep for IsCurrent7DayCycle in category breakdown]

Result: [N/5 rules PASSED, N/2 regressions PASSED] — [CLEAN | ACTION REQUIRED]
```
