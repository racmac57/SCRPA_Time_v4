# check_paths Skill Memory

## Latest Run

- **Date**: 2026-03-30
- **Iteration**: 1
- **Score**: 9/9

## Per-Test Binary Scores

| Test | Description | Score |
|------|-------------|-------|
| T1 | Skill doc specifies all 7 path checks | 1 |
| T2 | Safe path resolution, no forbidden hardcoding patterns | 1 |
| T3 | Provably read-only (guardrails section, no file writes) | 1 |
| T4 | Path scan ran with captured output | 1 |
| T5 | Output includes file:line for every finding | 1 |
| T6 | Enforces CLAUDE.md path rules (carucci_r, scrpa lowercase, canonical OneDrive root) | 1 |
| T7 | Catches v1.2.0 path case sensitivity bug (SCRPA vs scrpa) | 1 |
| T8 | Memory file updated | 1 |
| T9 | All tests = 1 | 1 |

## Evidence: Path Scan Results (2026-03-30)

### Files Scanned
- **11 Python files** in `scripts/`
- **3 batch files**: `scripts/export_enriched_data.bat`, `scripts/Run_SCRPA_Pipeline.bat`, `scripts/Clean_ChatGPT_HTML.bat`

### Check 1 -- Username (RobertCarucci): PASS=1
- 0 occurrences found. All paths use `carucci_r`.

### Check 2 -- PowerBI_Date typo: PASS=1
- 0 occurrences found. No typo present.

### Check 3 -- OneDrive root canonical: PASS=1
- 16 OneDrive path references found across scripts and batch files.
- All use canonical form: `C:\Users\carucci_r\OneDrive - City of Hackensack`
- No variations (no numbered suffixes, no wrong usernames).

### Check 4 -- Case sensitivity (scrpa vs SCRPA): PASS=1
- Regex `_RMS[/\\]SCRPA[^_]` returned 0 matches (no uppercase SCRPA in exports path).
- Regex `_RMS[/\\]scrpa` returned 3 matches, all correct lowercase:
  - `scripts/move_place_export_once.py:2` (comment)
  - `scripts/move_place_export_once.py:11` (`05_EXPORTS\_RMS\scrpa\place`)
  - `scripts/Run_SCRPA_Pipeline.bat:9` (`05_EXPORTS\_RMS\scrpa`)
- `SCRPA_ArcPy` references: 20+ occurrences in `run_scrpa_pipeline.py` and `generate_documentation.py`, all correctly capitalized.

### Check 5 -- Hardcoded inline paths: INFO
- **Module-level constants (intentional, not flagged)**:
  - `scripts/crime_breakdown_and_lagdays.py:22` -- `BASE`
  - `scripts/export_enriched_data_and_email.py:30` -- `BASE_DIR`
  - `scripts/run_scrpa_pipeline.py:78` -- `BASE_DIR`
  - `scripts/run_scrpa_pipeline.py:80` -- `TEMPLATE_DIR`
  - `scripts/run_scrpa_pipeline.py:138-139` -- `SCRPA_ARCPY_OUTPUT`
  - `scripts/run_scrpa_pipeline.py:143-144` -- `SCRPA_ARCPY_SCRIPT`
  - `scripts/scrpa_transform.py:43` -- `CYCLE_CALENDAR_PATH`
  - `scripts/scrpa_transform.py:48` -- `CALLTYPE_CATEGORIES_PATH`
  - `scripts/move_place_export_once.py:10-11` -- `DESKTOP`, `DEST_DIR`
  - `scripts/generate_documentation.py:797-799` -- `HPD_REPORT_STYLE_PROMPT_PATH`
- **Inline paths in function bodies**:
  - `scripts/export_enriched_data_and_email.py:101` -- cycle calendar path hardcoded inside `get_cycle_info()` function
  - `scripts/generate_documentation.py:430` -- cycle calendar path hardcoded inside dict literal within function

### Check 6 -- Path separators: PASS=1
- 0 doubled-backslash issues found in source code.

### Check 7 -- File existence guards: INFO
- Most `open()` calls are for writing output (no guard needed).
- `pd.read_csv()` in `scripts/export_enriched_data_and_email.py:108` has preceding `.exists()` check at line 104.
- `scripts/verify_fix.py:5,35` -- uses relative paths with no existence check (utility script).
- `scripts/scrpa_transform.py:786,794` -- reads input file; guarded by argparse required argument.

### get_onedrive_root() Usage
- **0 scripts** import or call `get_onedrive_root()`. All paths are hardcoded module-level constants. This is informational -- the function exists in `path_config.py` but is not used by any SCRPA pipeline script.

## Changes Made to Skill File

1. Added explicit regex patterns for Check 1 (`RobertCarucci`), Check 4 (`_RMS[/\\]SCRPA[^_]`), and Check 6 (`\\\\\\\\`)
2. Added v1.2.0 regression note in new "Regression Notes" section explaining the SCRPA vs scrpa case sensitivity bug
3. Added binary PASS=1/FAIL=0 output format in the output template table
4. Added note that `SCRPA_ArcPy` is correctly capitalized (not a false positive) in both Shared Context and Guardrails
5. Added list of known intentional module-level constants to skip in Check 5
6. Added Check 9 for `get_onedrive_root()` usage detection
7. Strengthened READ-ONLY guardrail language in header and Guardrails section
8. Changed em-dashes to `--` for compatibility

## Gaps Remaining

None. All 9 tests pass.
