Verify the SCRPA cycle calendar CSV has no date gaps, overlapping 7-day windows, or missing bi-weekly entries for a target year.

## When to Use

- Before the first pipeline run of a new calendar year.
- After any edit to the cycle calendar CSV.
- When the user says "check calendar", "verify cycle calendar", or invokes `/check-cycle-calendar`.
- After the kind of bug seen in v1.9.1 (missing 01/06/2026 entry that created a date lookup gap).

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. The cycle calendar CSV (default: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv`)

## Required CSV Columns

The calendar CSV **must** contain all 7 of these columns (exact names):

| Column | Type | Purpose |
|--------|------|---------|
| `Report_Due_Date` | date (MM/DD/YYYY) | When the report is due |
| `7_Day_Start` | date | Start of the 7-day analysis window |
| `7_Day_End` | date | End of the 7-day analysis window |
| `28_Day_Start` | date | Start of the 28-day analysis window |
| `28_Day_End` | date | End of the 28-day analysis window |
| `Report_Name` | string | Cycle identifier (e.g., `26C01W02`) |
| `BiWeekly_Report_Name` | string | Bi-weekly label (e.g., `26BW01`), empty on off-weeks |

## Calendar Structure: Weekly vs. Bi-Weekly

The calendar supports two cadences:

- **2025 and earlier**: Weekly rows (52-53 per year, 7-day spacing between Report_Due_Dates)
- **2026 and later**: Bi-weekly rows with only the reporting weeks present. The "off" weeks between bi-weekly entries are **intentional gaps** in the CSV. Each bi-weekly row still covers a 7-day window; the 28-day window provides lookback coverage.

**Cross-year boundary**: The first 2026 cycle (26C01W01, 7_Day_Start=12/30/2025) may have weekly spacing to the next row (26C01W02) because it bridges the calendar year. This is expected.

## Steps

1. **Locate the calendar file.** If the user provides a path, use it. Otherwise, use the default path above. If the file is not found, check `scripts/scrpa_transform.py` for the `CYCLE_CALENDAR_PATH` constant.

2. **Load the CSV** and parse date columns: `Report_Due_Date`, `7_Day_Start`, `7_Day_End`, `28_Day_Start`, `28_Day_End`. Verify all parse successfully. Report any rows with unparseable dates.

3. **Check 1 — Required columns exist.** Verify the CSV has all 7 required columns listed above.

4. **Check 2 — 7-Day window coverage (no gaps).** For the target year (default: current year):
   - Sort all rows by `7_Day_Start`.
   - **Weekly cadence** (2025 and earlier): consecutive rows must have `row[n+1].7_Day_Start == row[n].7_Day_End + 1 day`. Any gap means a date falls outside all 7-day windows, which will cause Tier 2 cycle resolution to fail.
   - **Bi-weekly cadence** (2026+): gaps of exactly 7 days between consecutive rows are **expected** (the off-week). Flag only gaps that are NOT exactly 7 days, as those indicate missing or malformed entries.
   - Report each unexpected gap with the missing date range.

5. **Check 3 — No overlapping 7-Day windows.** For each pair of rows in the target year, verify that no date belongs to more than one 7-day window (`7_Day_Start` to `7_Day_End`). Report overlaps.

6. **Check 4 — 28-Day window consistency.** Verify that each row's `28_Day_End` == `7_Day_End` and `28_Day_Start` == `7_Day_Start - 21 days` (i.e., 28-day window = 7-day window + 21 preceding days). **Note:** For bi-weekly cadence (2026+), the 28-day window still anchors to each row's own `7_Day_Start`, even though the off-week has no row — so the 28-day formula is the same for both weekly and bi-weekly calendars. Report any rows that don't follow this pattern.

7. **Check 5 — BiWeekly_Report_Name completeness.** For the target year:
   - Count non-empty `BiWeekly_Report_Name` values. Expect 26 for a full year.
   - The bi-weekly names must follow the pattern `YYBW##` (e.g., `26BW01`, `26BW02`, ..., `26BW26`).
   - Report any missing or malformed bi-weekly names.

8. **Check 6 — Report_Due_Date sequencing.** Verify `Report_Due_Date` values are monotonically increasing.
   - **Weekly cadence**: each is exactly 7 days after the previous.
   - **Bi-weekly cadence**: each is exactly 14 days after the previous, **except** the cross-year transition (first two rows of the year may have 7-day spacing).
   - Report any breaks.

9. **Check 7 — Cycle count.** For the target year, verify:
   - **Weekly cadence**: 52 or 53 rows (depending on ISO week count)
   - **Bi-weekly cadence**: 26 or 27 rows, with 26 non-empty `BiWeekly_Report_Name` entries

10. **Report results** using the binary output format below.

## Regression Checks

### v1.9.1 — Single-Entry Calendar Gap

The v1.9.1 bug was caused by a missing row for 01/06/2026 that created a Tier 2 cycle resolution lookup hole. Any date not covered by a `7_Day_Start`..`7_Day_End` range will cause `resolve_cycle()` Tier 2 to fail silently, falling through to Tier 3 (wrong cycle).

**Always verify**: Test that specific known dates (especially cross-year boundary dates like 01/06/2026) are covered by at least one 7-day window in the full dataset (not just the target-year filter). A single missing entry can create a lookup hole that silently misclassifies incidents.

### Bi-Weekly Gap Awareness

For bi-weekly calendars, the "off" weeks (dates between consecutive 7-day windows) are **not** covered by any 7-day window. This is by design. Tier 2 resolution will correctly fall through to Tier 3 for incidents on those dates. The validator should NOT flag these 7-day off-week gaps as errors.

## Guardrails

- **READ-ONLY — Do not modify any file. Report findings only.**
- Never edit the cycle calendar CSV.
- Never add or remove rows from the calendar.
- If the calendar uses a different column naming convention than expected, report the actual column names found and map them to the expected names before checking.

## Output Format

All checks use binary scoring: `PASS=1` or `FAIL=0`. No partial credit.

```
## Cycle Calendar Validation — [YEAR]
File: [path]
Rows: [N total, N for target year]
Cadence: [Weekly | Bi-Weekly]

1. Required Columns:     PASS=1|FAIL=0 — [details]
2. 7-Day Coverage:       PASS=1|FAIL=0 — [N unexpected gaps found: date ranges]
3. No Overlaps:          PASS=1|FAIL=0 — [N overlaps found]
4. 28-Day Consistency:   PASS=1|FAIL=0 — [N inconsistent rows]
5. BiWeekly Names:       PASS=1|FAIL=0 — [N/26 present, format OK/issues]
6. Report_Due Sequence:  PASS=1|FAIL=0 — [monotonic, spacing details]
7. Cycle Count:          PASS=1|FAIL=0 — [N rows, N bi-weekly]

Regression v1.9.1:      PASS=1|FAIL=0 — [01/06/2026 covered by: Report_Name]

Result: [N/7 PASSED] — [CLEAN | ACTION REQUIRED]
```
