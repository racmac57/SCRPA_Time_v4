"""
Minimal pytest suite for SCRPA Executive Summary HTML patcher.
Asserts Cycle/Range/Version/Footer changes and .bak backup writing.

Note: Markdown executive summary (SCRPA_Combined_Executive_Summary_*.md) is not
patched yet; add tests and patching when the pipeline starts copying it into the cycle folder.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts so we can import from run_scrpa_pipeline
SCRPA_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = SCRPA_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from run_scrpa_pipeline import (
    _ExecSummaryPatch,
    _inline_patch_exec_summary_html,
    _write_backup_and_atomic_replace,
)


SAMPLE_HTML = """<!DOCTYPE html>
<html>
<head><title>SCRPA Combined Executive Summary</title></head>
<body>
  <div class="header">
    <div class="pill">Cycle: Auto-Detected</div>
    <div class="pill">Range: Auto-Detected - Current</div>
    <div class="pill">Version: v1.1</div>
    <div class="pill">Auto-Detection: SCRPA Statistical Export System</div>
  </div>
  <main>Content</main>
  <footer><div>Hackensack Police Department - Safe Streets Operations Control Center | Cycle: Auto-Detected</div></footer>
</body>
</html>
"""


@pytest.fixture
def sample_html_file(tmp_path):
    """Write sample HTML to a temp file and return path."""
    html_path = tmp_path / "SCRPA_Combined_Executive_Summary.html"
    html_path.write_text(SAMPLE_HTML, encoding="utf-8")
    return html_path


def test_exec_summary_patch_range_pill_biweekly():
    """When bi-weekly bounds exist, range pill shows both 7-day and bi-weekly windows."""
    patch = _ExecSummaryPatch(
        cycle_id="26BW06",
        range_start="03/17/2026",
        range_end="03/23/2026",
        version="v1.9.4",
        biweekly_start="03/10/2026",
        biweekly_end="03/23/2026",
    )
    inner = patch.range_pill_inner()
    assert "7-Day: 03/17/2026 - 03/23/2026" in inner
    assert "Bi-Weekly: 03/10/2026 - 03/23/2026" in inner
    assert "7-Day:" in patch.footer_range_en()
    assert "Bi-Weekly:" in patch.footer_range_en()


def test_inline_patch_updates_cycle_range_version_footer(sample_html_file):
    """Patch updates Cycle, Range, Version pills and footer; leaves .bak."""
    patch = _ExecSummaryPatch(
        cycle_id="26BW02",
        range_start="01/13/2026",
        range_end="01/26/2026",
        version="v1.2",
    )
    changed = _inline_patch_exec_summary_html(
        sample_html_file,
        patch,
        include_version_in_footer=True,
        remove_auto_detection_pill=True,
    )
    assert changed is True

    text = sample_html_file.read_text(encoding="utf-8")
    assert "Cycle: 26BW02" in text
    assert "Range: 01/13/2026 - 01/26/2026" in text
    assert "Version: v1.2" in text
    assert "Auto-Detection:" not in text
    assert "Cycle: 26BW02 | Range: 01/13/2026 – 01/26/2026 | Version: v1.2" in text

    bak = sample_html_file.with_suffix(sample_html_file.suffix + ".bak")
    assert bak.exists()
    assert "Cycle: Auto-Detected" in bak.read_text(encoding="utf-8")


def test_inline_patch_idempotent_no_change(sample_html_file):
    """Patching twice with same values does not change content second time (no new .bak overwrite)."""
    patch = _ExecSummaryPatch(
        cycle_id="26BW02",
        range_start="01/13/2026",
        range_end="01/26/2026",
        version="v1.2",
    )
    _inline_patch_exec_summary_html(sample_html_file, patch)
    first_text = sample_html_file.read_text(encoding="utf-8")
    changed2 = _inline_patch_exec_summary_html(sample_html_file, patch)
    assert changed2 is False
    assert sample_html_file.read_text(encoding="utf-8") == first_text


def test_write_backup_and_atomic_replace(tmp_path):
    """Atomic replace writes .bak and replaces file content."""
    target = tmp_path / "foo.html"
    target.write_text("original", encoding="utf-8")
    _write_backup_and_atomic_replace(target, "new content")
    assert target.read_text(encoding="utf-8") == "new content"
    bak = target.with_suffix(".html.bak")
    assert bak.exists()
    assert bak.read_text(encoding="utf-8") == "original"
