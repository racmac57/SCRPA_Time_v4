Remove ChatGPT formatting artifacts from HTML tactical briefing files saved from ChatGPT output — wraps the existing `scripts/clean_chatgpt_html.py`.

## When to Use

- After saving a ChatGPT tactical briefing HTML file to a cycle's `Reports/` folder.
- When the user says "clean HTML", "strip code fences", or invokes `/clean-chatgpt-html`.
- When an HTML file starts with ` ```html ` or contains `<!-- :contentReference -->` comments.

## Shared Context

Read the files listed in `.claude/skills/_shared_context.md` before acting. Additionally read:

1. `scripts/clean_chatgpt_html.py` — the existing cleaner script (do NOT rewrite this logic)

## Steps

1. **Identify the target.** The user provides either:
   - A specific HTML file path (e.g., `Reports/26BW05_scrpa_tac.html`)
   - A folder path (scans all `.html` files in it)
   - Nothing — default to the latest cycle's `Reports/` folder

2. **Run the existing script.** Execute:
   ```
   python scripts/clean_chatgpt_html.py <target>
   ```
   This script removes:
   - Leading ```` ```html ```` or ```` ``` ```` code-fence lines
   - Trailing ```` ``` ```` code-fence lines
   - Any remaining inline ```` ``` ```` occurrences inside the HTML body
   - ChatGPT citation comments (`<!-- :contentReference[...]{...} ... -->`)

3. **Report the results.** The script prints which files were cleaned and what changes were made. Relay this output to the user.

4. **Post-clean check.** After cleaning, verify the file starts with `<!DOCTYPE` (the script warns if it doesn't). If it doesn't, alert the user that manual inspection may be needed.

## Guardrails

- **Show a diff before writing. Create a `.bak` backup before overwriting.** (The script itself writes in-place; recommend the user keep a backup or use the `.bak` the script does not create.)
- Do NOT rewrite or duplicate the logic in `clean_chatgpt_html.py` — always delegate to the existing script.
- Never modify the HTML structure, content, CSS, or data — only strip ChatGPT artifacts.
- Never clean files that are not HTML (skip `.csv`, `.json`, `.md` even if in the same folder).
- If the script is not found at `scripts/clean_chatgpt_html.py`, report the error and suggest the user verify the script location.

## Output Format

```
## ChatGPT HTML Cleanup

Target: [file or folder path]
Files scanned: N
Files modified: N

[Per-file details from script output]

Post-clean: [All files start with <!DOCTYPE | WARNING: file.html does not start with <!DOCTYPE]
```
