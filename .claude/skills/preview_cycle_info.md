Resolve a date to its SCRPA cycle and display cycle name, 7-day window, bi-weekly period, and report due date without running the full pipeline.

## When to Use

- When planning a pipeline run and needing to know which cycle a date falls in.
- When the user asks "what cycle is [date]?", "show cycle info", or invokes `/preview-cycle-info`.
- When verifying that cycle resolution returns the expected result for a specific date.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. The cycle calendar CSV (default: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv`)

## Steps

1. **Get the target date.** If the user provides a date (MM/DD/YYYY), use it. Otherwise, use today's date.

2. **Load the cycle calendar CSV.** Parse date columns: `Report_Due_Date`, `7_Day_Start`, `7_Day_End`, `28_Day_Start`, `28_Day_End`.

3. **Apply 3-tier cycle resolution** (exactly as defined in `scrpa_transform.py`):

   **Tier 1 — Exact Report_Due_Date match:**
   ```
   match = calendar[calendar.Report_Due_Date == target_date]
   ```
   If found, use this row. Note: "Matched via Tier 1 (exact Report_Due_Date)."

   **Tier 2 — Date within 7-Day window:**
   ```
   match = calendar[(calendar.7_Day_Start <= target_date) & (target_date <= calendar.7_Day_End)]
   ```
   If found, use this row. Note: "Matched via Tier 2 (within 7-Day window)."

   **Tier 3 — Most recent cycle:**
   ```
   eligible = calendar[calendar.7_Day_End <= target_date]
   match = eligible.sort_values('7_Day_End').iloc[-1]
   ```
   Note: "Matched via Tier 3 (most recent completed cycle)." For bi-weekly cadence (2026+), Tier 3 fires on off-weeks (the 7-day gap between active cycles) — label this as "Off-week gap — date falls between active cycles" in the output.

4. **Extract bi-weekly info.** If the matched row has a non-empty `BiWeekly_Report_Name`:
   - Bi-Weekly name = `BiWeekly_Report_Name` value
   - Bi-Weekly period start = `7_Day_Start - 7 days`
   - Bi-Weekly period end = `7_Day_End`

5. **Display the result** in a structured table.

## Guardrails

- **Do not modify any file. Report findings only.**
- Never run the pipeline or any transform scripts.
- Never modify the cycle calendar.
- If the target date falls outside all calendar rows (e.g., a future year not yet added), report this clearly rather than guessing.

## Output Format

```
## Cycle Info — [TARGET_DATE]

Resolution: Tier [1|2|3] — [explanation]

| Field               | Value            |
|---------------------|------------------|
| Cycle Name          | [Report_Name]    |
| Bi-Weekly Cycle     | [YYBW##] or N/A  |
| Report Due Date     | [MM/DD/YYYY]     |
| 7-Day Window        | [start] - [end]  |
| 28-Day Window       | [start] - [end]  |
| Bi-Weekly Period    | [start] - [end]  |

Expected output folder: Time_Based/[YYYY]/[CYCLE_NAME]_[YY_MM_DD]/
```
