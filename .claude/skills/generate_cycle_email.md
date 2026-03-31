Preview or regenerate the EMAIL_TEMPLATE.txt for a given SCRPA cycle with all placeholders filled from cycle info and report summary data.

## When to Use

- After a pipeline run, when the user wants to review or adjust the email before sending.
- When the user says "generate email", "preview email", or invokes `/generate-cycle-email`.
- When the email template needs regeneration after a data correction.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. The cycle folder's `Documentation/SCRPA_Report_Summary.md` — for counts
2. The cycle folder's `Documentation/EMAIL_TEMPLATE.txt` — current version (if exists)
3. `scripts/run_scrpa_pipeline.py` — `create_email_template()` function for the canonical format

## Steps

1. **Identify the cycle.** If the user provides a cycle folder path, use it. Otherwise, find the most recently modified folder under `Time_Based/YYYY/`.

2. **Extract cycle info.** From the cycle folder name and `SCRPA_Report_Summary.md`, extract:
   - Cycle Name (e.g., `26C03W10`)
   - Bi-Weekly Cycle (e.g., `26BW05`)
   - Report Due Date
   - 7-Day Window (start - end)
   - Bi-Weekly Period (start - end)

3. **Build the email template** using the same format as `create_email_template()` in `run_scrpa_pipeline.py`:
   ```
   Subject: SCRPA Bi-Weekly Report - Cycle [BIWEEKLY] | 7-Day: [START] - [END]

   Sir,

   Please find attached the SCRPA Combined Executive Summary for Bi-Weekly Cycle [BIWEEKLY] ([CYCLE_NAME]).

   7-Day Report Period: [START_7] - [END_7]
   Bi-Weekly Period: [START_BW] - [END_BW]
   Date Generated: [TODAY]

   The report includes:
   - 7-Day Executive Summary with detailed incident summaries
   - ArcGIS Map visuals showing incidents occurring in the last 7 days
   - Statistical charts and visualizations by crime type
   - 28-Day Executive Summary (operational planning)
   - YTD Executive Summary (strategic analysis)

   Please let me know if you have any questions or require additional information.
   ```

4. **Show preview** to the user with all placeholders filled.

5. **If the user confirms**, write the email to `Documentation/EMAIL_TEMPLATE.txt` in the cycle folder.

## Guardrails

- **Show a preview and ask for confirmation before writing any file.**
- Never send the email — only generate the template text.
- Never modify data files (CSV, JSON).
- Never change the email format without user approval.
- The salutation "Sir," is intentional (standard HPD format). Do not change it unless the user explicitly requests a different salutation.

## Output Format

Show the full email text with a header:

```
## Email Preview — Cycle [CYCLE_NAME]

[Full email text with all placeholders filled]

---
Write to: [path to EMAIL_TEMPLATE.txt]
Confirm? (y/n)
```
