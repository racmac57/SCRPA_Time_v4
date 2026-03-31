Detect drift between canonical documentation in `Documentation/` and the template strings in `generate_documentation.py`, and between canonical and per-cycle docs.

## When to Use

- After updating template strings in `scripts/generate_documentation.py`.
- When canonical docs feel stale or out of sync with the pipeline.
- When the user says "audit docs", "check doc drift", or invokes `/audit-doc-drift`.
- Periodically as a maintenance check.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. `scripts/generate_documentation.py` — template constants: `DATA_DICTIONARY`, `get_project_summary()`, `CLAUDE_MD_CONTENT`, `get_report_summary_template()`, `CHATGPT_BRIEFING_TEMPLATE`, `CHATGPT_SESSION_PROMPT_TEMPLATE`
2. `Documentation/data_dictionary.json` or `.yaml`
3. `Documentation/PROJECT_SUMMARY.json` or `.yaml`
4. `Documentation/claude.md`
5. Latest cycle folder's `Documentation/` contents (if available)

## Steps

1. **Check 1 — data_dictionary drift.** Compare the `DATA_DICTIONARY` dict in `generate_documentation.py` against `Documentation/data_dictionary.json`:
   - Are there fields in the Python dict not in the JSON (or vice versa)?
   - Do field descriptions, types, or calculations match?
   - Is the `last_updated` timestamp recent (within the last version release)?

2. **Check 2 — PROJECT_SUMMARY drift.** Compare `get_project_summary()` output against `Documentation/PROJECT_SUMMARY.json`:
   - Does the `data_flow` list match the current pipeline steps?
   - Does the `scripts` section list all current scripts with correct purposes?
   - Does the `output_structure` template match the actual folder layout?
   - Are `critical_logic` entries consistent with `CLAUDE.md`?

3. **Check 3 — claude.md drift.** Compare `CLAUDE_MD_CONTENT` string in `generate_documentation.py` against both:
   - `Documentation/claude.md` (canonical)
   - `CLAUDE.md` (repo root)
   All three should be consistent. Note any differences in critical logic rules, file tables, or workflow descriptions.

4. **Check 4 — Per-cycle doc freshness.** If a latest cycle folder exists:
   - Check `SCRPA_Report_Summary.md` — are counts populated (not "-" placeholders)?
   - Check `CHATGPT_BRIEFING_PROMPT.md` — are cycle placeholders filled (not `[CYCLE_ID]`)?
   - Check `CHATGPT_SESSION_PROMPT.md` — are date ranges filled?
   - Check `HPD_REPORT_STYLE_BLOCK.md` — is it non-empty and does it contain the START-END block content?
   - Check `EMAIL_TEMPLATE.txt` — are dates and cycle names populated?

5. **Check 5 — Script list completeness.** Verify that `PROJECT_SUMMARY` lists all scripts currently in `scripts/`:
   - Compare script names in `get_project_summary()['scripts']` against actual files in `scripts/`
   - Report any scripts in the folder but not in the summary, or vice versa

6. **Check 6 — Version consistency.** Check that version numbers mentioned in docs match:
   - `SUMMARY.md` version
   - `CHANGELOG.md` latest version
   - `generate_documentation.py` metadata version
   - `Documentation/PROJECT_SUMMARY.json` version

7. **Report findings** organized by check, with specific field/section references.

## Guardrails

- **Do not modify any file. Report findings only.**
- Never overwrite canonical docs without explicit user confirmation.
- Never touch per-cycle Documentation folders.
- Distinguish between intentional differences (e.g., repo root `CLAUDE.md` may have extra project-level context) and unintentional drift.

## Output Format

```
## Documentation Drift Audit

1. Data Dictionary:     [IN SYNC | DRIFT] — [N fields differ, N missing]
2. PROJECT_SUMMARY:     [IN SYNC | DRIFT] — [sections with differences]
3. claude.md:           [IN SYNC | DRIFT] — [which copies differ]
4. Per-Cycle Docs:      [POPULATED | STALE] — [N files with placeholders]
5. Script List:         [COMPLETE | INCOMPLETE] — [missing scripts]
6. Version Numbers:     [CONSISTENT | INCONSISTENT] — [which disagree]

### Details
[For each DRIFT item, list the specific differences]

Recommendation: [No action needed | Run `python scripts/generate_documentation.py -o Documentation/` to resync]
```
