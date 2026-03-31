Verify that the HPD_REPORT_STYLE_BLOCK.md extraction matches the current START/END markers in the source HPD_Report_Style_Prompt.md.

## When to Use

- After updating `08_Templates/Report_Styles/html/HPD_Report_Style_Prompt.md`.
- When a ChatGPT tactical briefing looks wrong (missing CSS, broken layout).
- When the user says "check style sync", "verify style block", or invokes `/check-html-template-sync`.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. `scripts/generate_documentation.py` — `extract_hpd_style_block_markdown()` function and `HPD_REPORT_STYLE_PROMPT_PATH` constant
2. The source style file (default: `C:\Users\carucci_r\OneDrive - City of Hackensack\08_Templates\Report_Styles\html\HPD_Report_Style_Prompt.md`)
3. The latest cycle's `Documentation/HPD_REPORT_STYLE_BLOCK.md`

## Steps

1. **Locate the source file.** Check `HPD_REPORT_STYLE_PROMPT_PATH` in `generate_documentation.py` for the canonical path. If the file doesn't exist at that path, report the error.

2. **Extract the START/END block.** Read the source file and find the content between `START OF STYLE BLOCK` and `END OF STYLE BLOCK` markers. This is the same logic as `extract_hpd_style_block_markdown()` in `generate_documentation.py`.

3. **Read the per-cycle block.** Find the latest cycle folder's `Documentation/HPD_REPORT_STYLE_BLOCK.md` and read its content (after the header/preamble).

4. **Compare.** Diff the extracted block against the per-cycle file content:
   - Are they identical (aside from the header preamble)?
   - Are there CSS rules in the source not present in the per-cycle file?
   - Are there extra rules in the per-cycle file not in the source?

5. **Check marker presence.** Verify the source file contains both markers:
   - `START OF STYLE BLOCK`
   - `END OF STYLE BLOCK`
   If either is missing, the extraction will fail silently — report as CRITICAL.

6. **Check key CSS rules.** Verify the extracted block contains these critical rules (which are required for PDF print):
   - `@page` (default portrait)
   - `@page landscape`
   - `.report-tail`
   - `.report-tail-landscape`
   - `table.incident-highlights`
   - `.footer`
   Report any missing rules.

7. **v2.0.0 Regression anchor.** Verify the per-cycle HTML report uses data from the current cycle's JSON/CSV, not stale or cached data. Check that `SCRPA_7Day_Summary.json` `cycle.name` matches the cycle folder name prefix. This catches the v2.0.0 stale HTML data mismatch regression.

8. **Report findings.**

## Guardrails

- **Do not modify any file. Report findings only.**
- Never edit the source style file or the per-cycle style block.
- Never modify CSS rules.
- If the source file is outside this repo (in `08_Templates/`), note that changes there require re-running the pipeline to propagate.

## Output Format

```
## HPD Style Block Sync Check

Source: [path to HPD_Report_Style_Prompt.md]
Per-cycle: [path to HPD_REPORT_STYLE_BLOCK.md]

1. Source markers:    [PRESENT|MISSING] — START: [found|missing], END: [found|missing]
2. Block extraction:  [SUCCESS|FAILED] — [N lines extracted]
3. Content match:     [IDENTICAL|DIFFERS] — [summary of differences]
4. Critical CSS rules:
   - @page:                    [PRESENT|MISSING]
   - @page landscape:          [PRESENT|MISSING]
   - .report-tail:             [PRESENT|MISSING]
   - .report-tail-landscape:   [PRESENT|MISSING]
   - table.incident-highlights: [PRESENT|MISSING]
   - .footer:                  [PRESENT|MISSING]

Result: [IN SYNC | OUT OF SYNC — re-run pipeline to propagate changes]
```
