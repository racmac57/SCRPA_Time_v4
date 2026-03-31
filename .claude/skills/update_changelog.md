Append a properly formatted entry to CHANGELOG.md following the project's Keep-a-Changelog and SemVer conventions.

## When to Use

- After completing a feature, fix, or documentation update.
- When the user says "update changelog", "add changelog entry", or invokes `/update-changelog`.
- Before creating a release or version bump.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. `CHANGELOG.md` — current changelog (full file)
2. Recent git log: `git log --oneline -20`
3. `git diff` or `git diff --staged` for the current changes

## Steps

1. **Read `CHANGELOG.md`** to understand the current format, latest version, and section structure.

2. **Analyze the changes.** From git log/diff, determine:
   - What changed (Added / Changed / Fixed / Removed / Breaking Changes / Documentation / Technical)
   - Which files were affected
   - The nature of the change (new feature, enhancement, bug fix, refactor, docs)

3. **Check [Unreleased] section.** Before drafting a new entry, check if `[Unreleased]` already has content. If it does, the new entry should either be appended to `[Unreleased]` or the existing `[Unreleased]` items should be rolled into the new version — ask the user which approach they prefer.

4. **Determine the version.** Based on the change type:
   - Bug fix or minor docs update: patch bump (e.g., 2.0.2 -> 2.0.3)
   - New feature or significant enhancement: minor bump (e.g., 2.0.x -> 2.1.0)
   - Breaking change: major bump (e.g., 2.x.x -> 3.0.0)
   - If unsure, add to `[Unreleased]` and let the user decide the version.

5. **Draft the changelog entry** following the project's format:
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD

   ### Added
   - **Feature name** — description

   ### Changed
   - **What changed** — description

   ### Fixed
   - **Bug name** — description
     - Root cause / impact details

   ### Documentation
   - What docs were updated
   ```

6. **Show the draft** to the user for review.

7. **If confirmed**, insert the new entry after the `[Unreleased]` section and before the previous version entry. Add the comparison link at the bottom of the file following the existing pattern:
   ```markdown
   [X.Y.Z]: https://github.com/racmac57/SCRPA_Time_v4/compare/vPREVIOUS...vX.Y.Z
   ```

## Guardrails

- **Show a diff before writing. Create a `.bak` backup before overwriting.**
- Never remove existing changelog entries.
- Never change version numbers of existing entries.
- Preserve the comparison link references at the bottom of the file.
- Follow the exact heading structure used in the existing changelog (### Added, ### Changed, ### Fixed, etc.).
- Do not add entries for changes that are already documented in the latest version.
- If `[Unreleased]` has items and the user wants a version bump, move those items into the new version section.

## Output Format

```
## Changelog Update Preview

Version: [X.Y.Z] (or [Unreleased])
Date: [YYYY-MM-DD]

[Draft entry in markdown]

---
Insert after: [Unreleased] section
Backup: CHANGELOG.md.bak
Confirm? (y/n)
```
