Scan SCRPA pipeline scripts for hardcoded path issues -- case mismatches, wrong username, broken OneDrive references, and missing fallbacks. **READ-ONLY: never auto-correct paths.**

## When to Use

- After any path-related change in `scripts/`.
- When the user says "check paths", "verify paths", or invokes `/check-paths`.
- After encountering a `FileNotFoundError` or `OSError` related to path resolution.
- Periodically as a maintenance check (path bugs have caused multiple production issues).

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally reference these path rules from `CLAUDE.md`:

- Canonical OneDrive root: `C:\Users\carucci_r\OneDrive - City of Hackensack`
- Always use `carucci_r` in Windows user paths -- never `RobertCarucci`
- Never change `PowerBI_Data` to `PowerBI_Date` (the latter is the typo)
- The exports folder uses lowercase `scrpa` (not `SCRPA`) in `05_EXPORTS\_RMS\scrpa\`
- `SCRPA_ArcPy` IS correctly capitalized -- do not flag as false positive
- Module-level constants (`BASE_DIR`, `SCRPA_ARCPY_OUTPUT`, `SCRPA_ARCPY_SCRIPT`, `HPD_REPORT_STYLE_PROMPT_PATH`, etc.) are intentional -- only flag inline hardcoded paths inside function bodies
- `path_config.py` resolves the correct root at runtime via `get_onedrive_root()` -- note if no scripts import it

## Regression Notes

### v1.2.0 Path Case Sensitivity Bug (2026-01)
The exports path `05_EXPORTS\_RMS\SCRPA\` (uppercase) was used in early versions, causing `FileNotFoundError` on case-sensitive filesystems and OneDrive sync issues. The fix changed it to lowercase `scrpa`. This check must always verify no uppercase `SCRPA` appears in the exports path (i.e., `_RMS\SCRPA\` or `_RMS/SCRPA/` where the next segment is NOT `_ArcPy`).

## Steps

1. **Identify all files to scan.** Glob all `.py` files in `scripts/` and all `.bat` files in the repo. Record counts.

2. **Check 1 -- Username in paths.** Grep for regex pattern (case-insensitive):
   ```
   RobertCarucci
   ```
   This is always wrong -- the correct username is `carucci_r`. Report each occurrence with file:line. PASS=1 if 0 occurrences, FAIL=0 otherwise.

3. **Check 2 -- PowerBI_Data vs PowerBI_Date.** Grep for literal string:
   ```
   PowerBI_Date
   ```
   The correct name is `PowerBI_Data`. PASS=1 if 0 occurrences, FAIL=0 otherwise.

4. **Check 3 -- OneDrive root consistency.** Grep for paths containing `OneDrive` and verify each uses the canonical form:
   ```
   C:\Users\carucci_r\OneDrive - City of Hackensack
   ```
   Flag any variations (different username, different folder name, numbered suffix like `(1)`). Forward slashes in `Path()` constructors are OK but note them. PASS=1 if all match canonical, FAIL=0 otherwise.

5. **Check 4 -- Case sensitivity in exports path (v1.2.0 regression).** Grep for regex:
   ```
   _RMS[/\\]SCRPA[^_]
   ```
   This catches uppercase `SCRPA` in the exports path while excluding `SCRPA_ArcPy` (which IS correctly capitalized). Also verify lowercase `scrpa` is used via:
   ```
   _RMS[/\\]scrpa
   ```
   PASS=1 if 0 uppercase matches, FAIL=0 otherwise.

6. **Check 5 -- Hardcoded paths in function bodies.** Search for `OneDrive` path strings that appear inside function bodies (not at module-level as constants). Inline paths in functions should use existing constants or `get_onedrive_root()`. Known intentional module-level constants to skip:
   - `BASE_DIR`, `BASE` (module-level)
   - `SCRPA_ARCPY_OUTPUT`, `SCRPA_ARCPY_SCRIPT` (module-level)
   - `HPD_REPORT_STYLE_PROMPT_PATH` (module-level)
   - `CYCLE_CALENDAR_PATH` (module-level)
   - `CALLTYPE_CATEGORIES_PATH` (module-level)
   - `TEMPLATE_DIR` (module-level)
   Report as INFO with file:line for each inline occurrence.

7. **Check 6 -- Path separators.** Grep for doubled backslash patterns in path construction (regex: `\\\\\\\\` in source). Flag any `\\\\` (literal doubled) or missing separators between path segments. PASS=1 if 0 issues, FAIL=0 otherwise.

8. **Check 7 -- File existence guards (PASS=1 / FAIL=0).** Search for `pd.read_csv(`, `pd.read_excel(`, `pd.read_json(`, and `open(` calls in read mode. For each, check whether the path argument has a preceding `.exists()` check or surrounding `try/except`. PASS=1 if all input-file reads have at least one guard; FAIL=0 if any `pd.read_csv`/`pd.read_excel`/`pd.read_json`/`open(…, 'r')` call lacks both `.exists()` and `try/except`. Report file:line for each unguarded read. Note: output files (write mode) do not need existence checks.

9. **Check for `get_onedrive_root()` usage.** Grep for `get_onedrive_root` across all scanned files. Note if zero scripts import or call it -- this is informational (not a failure), but indicates all paths are currently hardcoded constants.

10. **Report results** using the binary output format below.

## Guardrails

- **Do not modify any file. Report findings only.** This skill is READ-ONLY.
- Never auto-correct paths -- report the issue and let the user decide.
- Do not flag paths inside comments or docstrings unless they appear to be copy-paste targets.
- Do not flag `Path()` objects that correctly handle forward slashes on Windows.
- Do not flag `SCRPA_ArcPy` as a case-sensitivity violation -- it is correctly capitalized.
- Recognize that module-level hardcoded paths are intentional constants -- only flag inline hardcoded paths in function bodies.

## Output Format

```
## SCRPA Path Audit

Date: YYYY-MM-DD
Files scanned: [N Python files, N batch files]

### Binary Test Results

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Username (RobertCarucci) | PASS=1 / FAIL=0 | [N occurrences, file:line list] |
| 2 | PowerBI_Date typo | PASS=1 / FAIL=0 | [N occurrences, file:line list] |
| 3 | OneDrive root canonical | PASS=1 / FAIL=0 | [N paths checked, N non-canonical] |
| 4 | Case sensitivity (scrpa vs SCRPA) | PASS=1 / FAIL=0 | [N uppercase exports matches] |
| 5 | Hardcoded inline paths | INFO | [N inline paths in function bodies] |
| 6 | Path separators | PASS=1 / FAIL=0 | [N doubled-backslash issues] |
| 7 | File existence guards | PASS=1 / FAIL=0 | [N unguarded input-file reads] |

### Additional Notes
- get_onedrive_root() usage: [found in N files / not used]
- SCRPA_ArcPy references: [N occurrences, all correctly capitalized]
- Module-level constants: [list of intentional constants found]

### Details
[For each FAIL or INFO item, list file:line and the problematic string]

Score: [N/7 checks passed] -- [CLEAN | ACTION REQUIRED]
```
