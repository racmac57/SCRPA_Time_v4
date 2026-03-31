"""
clean_chatgpt_html.py
─────────────────────
Removes ChatGPT formatting artifacts from HTML files saved from chat output:

  • Leading  ```html  or  ```  code-fence lines
  • Trailing ```  code-fence lines (wherever they appear in the HTML)
  • ChatGPT citation comments: <!-- :contentReference[...]{...} ... -->

Usage (run on a single file):
    python scripts/clean_chatgpt_html.py path/to/file.html

Usage (run on a folder — cleans all .html files in place):
    python scripts/clean_chatgpt_html.py path/to/folder/

Called automatically by: Clean_ChatGPT_HTML.bat
"""

from __future__ import annotations
import re
import sys
from pathlib import Path


# ── Patterns ────────────────────────────────────────────────────────────────

# Matches ```html or ``` optionally followed by whitespace, at start or end
_FENCE_START = re.compile(r'^\s*```(?:html)?\s*\n?', re.IGNORECASE)
_FENCE_END   = re.compile(r'\n?\s*```\s*$', re.IGNORECASE)

# Matches any inline ``` that survived inside the HTML body
_FENCE_INLINE = re.compile(r'```(?:html)?', re.IGNORECASE)

# ChatGPT citation comments injected into the document
_CITATION = re.compile(
    r'<!--\s*:contentReference\[.*?\]\{.*?\}.*?-->\s*\n?',
    re.DOTALL
)


def clean(html: str) -> tuple[str, list[str]]:
    """
    Remove ChatGPT artifacts from an HTML string.

    Returns:
        (cleaned_html, list_of_changes_made)
    """
    changes: list[str] = []
    original = html

    # 1. Strip leading code fence (```html or ```)
    cleaned = _FENCE_START.sub('', html, count=1)
    if cleaned != html:
        changes.append('Removed leading code fence (```html or ```)')
    html = cleaned

    # 2. Strip trailing code fence
    cleaned = _FENCE_END.sub('', html, count=1)
    if cleaned != html:
        changes.append('Removed trailing code fence (```)')
    html = cleaned

    # 3. Remove any remaining inline ``` inside the HTML body
    cleaned, n = _FENCE_INLINE.subn('', html)
    if n:
        changes.append(f'Removed {n} inline code fence(s) from HTML body')
    html = cleaned

    # 4. Remove ChatGPT citation comments
    cleaned, n = _CITATION.subn('', html)
    if n:
        changes.append(f'Removed {n} ChatGPT citation comment(s)')
    html = cleaned

    # 5. Ensure file starts with <!DOCTYPE
    stripped = html.lstrip()
    if not stripped.lower().startswith('<!doctype'):
        changes.append('WARNING: file does not start with <!DOCTYPE — check manually')

    return html.strip() + '\n', changes


def clean_file(path: Path) -> bool:
    """Clean a single HTML file in place. Returns True if changes were made."""
    try:
        original = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        original = path.read_text(encoding='latin-1')

    cleaned, changes = clean(original)

    if not changes:
        print(f'  [no changes] {path.name}')
        return False

    path.write_text(cleaned, encoding='utf-8')
    print(f'  [cleaned]    {path.name}')
    for c in changes:
        print(f'               -> {c}')
    return True


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python clean_chatgpt_html.py <file.html | folder>')
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        paths = [target]
    elif target.is_dir():
        paths = sorted(target.glob('*.html'))
        if not paths:
            print(f'No .html files found in {target}')
            sys.exit(0)
    else:
        print(f'Error: {target} is not a file or directory')
        sys.exit(1)

    print(f'Cleaning {len(paths)} file(s)...')
    changed = sum(clean_file(p) for p in paths)
    print(f'\nDone. {changed} file(s) modified.')


if __name__ == '__main__':
    main()
