Regenerate canonical `Documentation/` files from `generate_documentation.py` and show what changed before writing.

## When to Use

- After updating template strings in `scripts/generate_documentation.py`.
- When `Documentation/` files are stale and need a refresh.
- When the user says "sync docs", "regenerate docs", or invokes `/sync-canonical-docs`.
- After a version bump or significant pipeline change.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. `scripts/generate_documentation.py` — template definitions
2. All files in `Documentation/` — current canonical versions

## Steps

1. **Snapshot the current state.** Read and store the content of:
   - `Documentation/data_dictionary.json`
   - `Documentation/data_dictionary.yaml`
   - `Documentation/PROJECT_SUMMARY.json`
   - `Documentation/PROJECT_SUMMARY.yaml`
   - `Documentation/claude.md`
   - `Documentation/SCRPA_Report_Summary.md` (template version)

2. **Run the documentation generator.** Verify the working directory is the SCRPA project root (contains `scripts/` and `Documentation/` folders) before executing:
   ```
   python scripts/generate_documentation.py -o Documentation/
   ```
   This regenerates all canonical docs from the template definitions in the script. If the working directory is wrong, the script will fail or write to the wrong location.

3. **Diff the results.** For each file, compare the new content against the snapshot from Step 1. Show a summary diff:
   - Files unchanged
   - Files with content changes (show key differences, not full diff)
   - Files that are new

4. **Show the diff to the user** and ask for confirmation before keeping the changes.

5. **If the user rejects**, restore the original files from the snapshot.

## Guardrails

- **Show a diff before writing. Create a `.bak` backup before overwriting.**
- Before running the generator, back up each existing file as `filename.bak`.
- Never touch per-cycle Documentation folders — only the canonical `Documentation/` at the repo root.
- Never modify `generate_documentation.py` itself.
- If the generator script fails, restore backups and report the error.
- The generator requires `pyyaml` — if import fails, report the dependency issue.

## Output Format

```
## Canonical Documentation Sync

Backed up N files to .bak

### Changes
- data_dictionary.json:      [unchanged | updated — N fields changed]
- data_dictionary.yaml:      [unchanged | updated]
- PROJECT_SUMMARY.json:      [unchanged | updated — sections changed: ...]
- PROJECT_SUMMARY.yaml:      [unchanged | updated]
- claude.md:                 [unchanged | updated — sections changed: ...]
- SCRPA_Report_Summary.md:   [unchanged | updated]

[Key diffs shown here]

Keep changes? (y/n)
```
