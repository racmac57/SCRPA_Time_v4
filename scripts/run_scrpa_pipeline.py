# 2026_01_28
# Project: scripts/run_scrpa_pipeline.py
# Author: R. A. Carucci
# Purpose: Main orchestration script for SCRPA Python-first processing pipeline.

"""
SCRPA Pipeline Orchestrator

This script is the main entry point that runs the entire SCRPA data processing pipeline:
1. Load RMS export and cycle calendar
2. Run scrpa_transform.py -> SCRPA_All_Crimes_Enhanced.csv
3. Run prepare_7day_outputs.py -> 7-day filtered CSVs + metadata
4. Run generate_documentation.py -> Documentation folder contents
5. Optionally validate outputs against reference CSV
6. Generate summary report

Usage:
    python run_scrpa_pipeline.py input.csv --report-date 01/27/2026 -o Time_Based/2026/26C01W04_26_01_27

Output Structure:
    {output_dir}/
    ├── Data/
    │   ├── SCRPA_All_Crimes_Enhanced.csv
    │   ├── SCRPA_7Day_With_LagFlags.csv
    │   └── SCRPA_7Day_Summary.yaml
    ├── Documentation/   (cycle-specific only)
    │   ├── SCRPA_Report_Summary.md   (populated from pipeline data)
    │   ├── CHATGPT_BRIEFING_PROMPT.md
    │   └── EMAIL_TEMPLATE.txt
    └── Reports/
        └── (HTML/PDF from SCRPA_ArcPy)

Canonical docs (data_dictionary, PROJECT_SUMMARY, claude.md) live in
16_Reports/SCRPA/Documentation. Update with: python scripts/generate_documentation.py -o <path>
"""

from __future__ import annotations

import sys
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, Mapping
import argparse
import yaml
import pandas as pd

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import our modules
from scrpa_transform import (
    read_rms_export,
    load_cycle_calendar,
    build_all_crimes_enhanced,
    resolve_cycle,
    CYCLE_CALENDAR_PATH
)
from prepare_7day_outputs import save_7day_outputs
from generate_documentation import (
    write_report_summary_with_data,
    write_chatgpt_briefing_prompt,
)


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA")
TIME_BASED_DIR = BASE_DIR / "Time_Based"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_output_structure(base_dir: Path, cycle_name: str, report_date: date) -> Dict[str, Path]:
    """
    Create the output folder structure for a reporting cycle.

    Args:
        base_dir: Base output directory (e.g., Time_Based/2026)
        cycle_name: Cycle name (e.g., 26C01W04)
        report_date: Report due date

    Returns:
        Dictionary with paths to Data, Documentation, Reports folders
    """
    # Format: CYCLE_YY_MM_DD
    date_suffix = report_date.strftime('%y_%m_%d')
    folder_name = f"{cycle_name}_{date_suffix}"

    root = base_dir / folder_name
    paths = {
        'root': root,
        'data': root / 'Data',
        'documentation': root / 'Documentation',
        'reports': root / 'Reports'
    }

    # Create directories
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)

    return paths


def _clean_data_folder(data_dir: Path) -> None:
    """Remove timestamped SCRPA files so Data folder keeps only 2–3 stable files."""
    if not data_dir.exists():
        return
    import re
    pattern = re.compile(r'^SCRPA_.*_\d{8}_\d{6}\.(csv|yaml|json)$')
    removed = 0
    for f in data_dir.iterdir():
        if f.is_file() and pattern.match(f.name):
            try:
                f.unlink()
                removed += 1
            except OSError:
                pass
    if removed:
        print(f"  Cleaned {removed} old timestamped file(s) from Data/")


# Default location where SCRPA_ArcPy / briefing generates HTML reports
SCRPA_ARCPY_OUTPUT = Path(
    r"C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\06_Output"
)


# =============================================================================
# Executive Summary HTML patcher (cycle / range / version / footer)
# Tailored to the SCRPA Combined Executive Summary HTML template.
# =============================================================================


def _write_backup_and_atomic_replace(target: Path, new_text: str) -> None:
    """
    Write backup to {target}.bak (e.g. foo.html.bak) and atomically replace target content.
    Prevents partial writes if the process is interrupted.
    """
    original = target.read_text(encoding="utf-8", errors="ignore")
    backup_path = target.with_suffix(target.suffix + ".bak")
    backup_path.write_text(original, encoding="utf-8")
    tmp_dir = target.parent
    fd = None
    try:
        fd = tempfile.NamedTemporaryFile(
            mode="w", delete=False, dir=tmp_dir, encoding="utf-8", suffix=".tmp"
        )
        fd.write(new_text)
        fd.close()
        Path(fd.name).replace(target)
    finally:
        if fd is not None and not fd.closed:
            fd.close()


@dataclass(frozen=True)
class _ExecSummaryPatch:
    cycle_id: str
    range_start: str
    range_end: str
    version: str


def _first_present(d: Mapping[str, Any], keys: list[str], default: str = "") -> str:
    for k in keys:
        v = d.get(k)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return default


def _discover_scrpa_arcpy_root(start: Path) -> Optional[Path]:
    """
    Prefer env var SCRPA_ARCPY_ROOT. Otherwise, search upward for a folder named
    'SCRPA_ArcPy' that contains '05_orchestrator/patch_executive_summary_html.py'.
    """
    env = os.getenv("SCRPA_ARCPY_ROOT")
    if env:
        p = Path(env)
        if (p / "05_orchestrator" / "patch_executive_summary_html.py").exists():
            return p
    cur = start.resolve()
    for _ in range(8):
        candidate = cur / "SCRPA_ArcPy"
        if (candidate / "05_orchestrator" / "patch_executive_summary_html.py").exists():
            return candidate
        cur = cur.parent
    return None


def _read_version_file(arcpy_root: Path, default: str = "") -> str:
    p = arcpy_root / "VERSION"
    if p.exists():
        return p.read_text(encoding="utf-8", errors="ignore").strip()
    return default


def _resolve_version_for_fallback(cycle_info: Mapping[str, Any], arcpy_root: Optional[Path]) -> str:
    """Resolve version: cycle_info['version'], else SCRPA_ArcPy/VERSION, else 16_Reports/SCRPA/VERSION."""
    v = _first_present(cycle_info, ["version"], "")
    if v:
        return v
    if arcpy_root:
        v = _read_version_file(arcpy_root, "")
        if v:
            return v
    pipeline_version = BASE_DIR / "VERSION"
    if pipeline_version.exists():
        return pipeline_version.read_text(encoding="utf-8", errors="ignore").strip()
    return ""


def _try_import_arcpy_patcher(arcpy_root: Path):
    """
    Import patcher without permanently mutating sys.path.
    Returns (CycleInfo, patch_func) or (None, None).
    """
    patcher_dir = arcpy_root / "05_orchestrator"
    if not (patcher_dir / "patch_executive_summary_html.py").exists():
        return None, None
    added = str(patcher_dir)
    sys.path.insert(0, added)
    try:
        from patch_executive_summary_html import (  # type: ignore
            CycleInfo,
            patch_combined_executive_summary_html,
        )
        return CycleInfo, patch_combined_executive_summary_html
    except Exception:
        return None, None
    finally:
        try:
            sys.path.remove(added)
        except ValueError:
            pass


def _normalize_cycle_info(cycle_info: Mapping[str, Any], arcpy_root: Path) -> _ExecSummaryPatch:
    cycle_id = _first_present(
        cycle_info,
        ["cycle_id", "biweekly", "biweekly_name", "cycle", "cycle_name", "name"],
        "Auto-Detected",
    )
    range_start = _first_present(cycle_info, ["range_start", "start_bw", "start_7", "start_date"], "Auto-Detected")
    range_end = _first_present(cycle_info, ["range_end", "end_bw", "end_7", "end_date"], "Current")
    version = _first_present(cycle_info, ["version"], _read_version_file(arcpy_root, default=""))
    return _ExecSummaryPatch(cycle_id=cycle_id, range_start=range_start, range_end=range_end, version=version)


def _inline_patch_exec_summary_html(
    html_path: Path,
    patch: _ExecSummaryPatch,
    *,
    include_version_in_footer: bool = True,
    remove_auto_detection_pill: bool = True,
    footer_template: Optional[str] = None,
) -> bool:
    """
    Inline fallback patcher (ArcPy-free). Patches header pills and footer.
    Tailored to the SCRPA Combined Executive Summary HTML template; regex may need
    updates if the template structure changes.
    Returns True if file was changed.
    """
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    original = text

    pill_cycle = re.compile(r'(<div\s+class="pill">\s*Cycle:\s*)(.*?)(\s*</div>)', re.IGNORECASE | re.DOTALL)
    pill_range = re.compile(r'(<div\s+class="pill">\s*Range:\s*)(.*?)(\s*</div>)', re.IGNORECASE | re.DOTALL)
    pill_version = re.compile(r'(<div\s+class="pill">\s*Version:\s*)(.*?)(\s*</div>)', re.IGNORECASE | re.DOTALL)
    auto_pill = re.compile(r'\s*<div\s+class="pill">\s*Auto-Detection:.*?</div>\s*', re.IGNORECASE | re.DOTALL)
    footer_first_div = re.compile(r'(<footer\b[^>]*>\s*<div>)(.*?)(</div>)', re.IGNORECASE | re.DOTALL)

    # Use \g<1>/\g<3> to avoid \1 + digits (e.g. "26") being interpreted as octal escape
    text = pill_cycle.sub(r"\g<1>" + patch.cycle_id + r"\g<3>", text, count=1)
    text = pill_range.sub(
        r"\g<1>" + f"{patch.range_start} - {patch.range_end}" + r"\g<3>", text, count=1
    )
    if patch.version:
        text = pill_version.sub(r"\g<1>" + patch.version + r"\g<3>", text, count=1)
    if remove_auto_detection_pill:
        text = auto_pill.sub("\n", text, count=1)

    tpl = footer_template or (
        "Hackensack Police Department - Safe Streets Operations Control Center | "
        "Cycle: {cycle_id} | Range: {range_en}"
        + (" | Version: {version}" if include_version_in_footer and patch.version else "")
    )
    footer_text = tpl.format(
        cycle_id=patch.cycle_id,
        range_start=patch.range_start,
        range_end=patch.range_end,
        range_hy=f"{patch.range_start} - {patch.range_end}",
        range_en=f"{patch.range_start} – {patch.range_end}",
        version=patch.version,
    )
    text = footer_first_div.sub(r"\g<1>" + footer_text + r"\g<3>", text, count=1)

    if text == original:
        return False
    _write_backup_and_atomic_replace(html_path, text)
    return True


def patch_scrpa_combined_exec_summary_after_copy(
    copied_html_path: Path,
    cycle_info: Mapping[str, Any],
    *,
    include_version_in_footer: bool = True,
    remove_auto_detection_pill: bool = True,
    footer_template: Optional[str] = None,
) -> None:
    """
    Call after copying SCRPA_Combined_Executive_Summary.html into the cycle Reports folder.
    Prefers importing SCRPA_ArcPy patcher (sys.path hygiene: no permanent pollution);
    falls back to inline patch if import fails.
    """
    copied_html_path = Path(copied_html_path)
    if not copied_html_path.exists():
        return

    script_dir = Path(__file__).resolve().parent
    arcpy_root = _discover_scrpa_arcpy_root(script_dir)
    version = _resolve_version_for_fallback(cycle_info, arcpy_root)
    patch = _ExecSummaryPatch(
        cycle_id=_first_present(cycle_info, ["biweekly", "cycle_id", "cycle", "name"], "Auto-Detected"),
        range_start=_first_present(cycle_info, ["start_bw", "start_7", "range_start"], "Auto-Detected"),
        range_end=_first_present(cycle_info, ["end_bw", "end_7", "range_end"], "Current"),
        version=version or _first_present(cycle_info, ["version"], ""),
    )

    if arcpy_root:
        CycleInfo_cls, patch_func = _try_import_arcpy_patcher(arcpy_root)
        if CycleInfo_cls is not None and patch_func is not None:
            try:
                patch_for_arcpy = _normalize_cycle_info(cycle_info, arcpy_root)
                changed = patch_func(
                    copied_html_path,
                    CycleInfo_cls(
                        cycle_id=patch_for_arcpy.cycle_id,
                        range_start=patch_for_arcpy.range_start,
                        range_end=patch_for_arcpy.range_end,
                        version=patch_for_arcpy.version,
                        footer_template=footer_template or "",
                    ),
                    include_version_in_footer=include_version_in_footer,
                    remove_auto_detection_pill=remove_auto_detection_pill,
                    footer_template=footer_template,
                    backup=True,
                )
                print(
                    f"  Patch: ArcPy patcher, changed={changed} | {copied_html_path.name}"
                )
                return
            except Exception:
                pass

    changed = _inline_patch_exec_summary_html(
        copied_html_path,
        patch,
        include_version_in_footer=include_version_in_footer,
        remove_auto_detection_pill=remove_auto_detection_pill,
        footer_template=footer_template,
    )
    print(
        f"  Patch: inline fallback, changed={changed} | {copied_html_path.name}"
    )


def _copy_scrpa_reports_to_cycle(reports_dir: Path, cycle_info: Optional[Dict[str, Any]] = None) -> list:
    """
    Copy latest SCRPA_Combined_Executive_Summary.html from SCRPA_ArcPy/06_Output to cycle Reports folder.
    Optionally patch the copied HTML with cycle/range/version/footer from cycle_info.
    Does not copy rms_summary.html (user provides ChatGPT prompt for that separately).
    Returns list of destination paths copied.
    """
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    if not SCRPA_ARCPY_OUTPUT.exists():
        print(f"  Reports source not found: {SCRPA_ARCPY_OUTPUT} (skipping copy)")
        return []

    copied = []
    combined = list(SCRPA_ARCPY_OUTPUT.glob("SCRPA_Combined_Executive_Summary_*.html"))
    if combined:
        latest = max(combined, key=lambda p: p.stat().st_mtime)
        dest = reports_dir / "SCRPA_Combined_Executive_Summary.html"
        try:
            shutil.copy2(latest, dest)
            copied.append(str(dest))
            print(f"  Copied report: {dest.name}")
            if cycle_info:
                patch_scrpa_combined_exec_summary_after_copy(dest, cycle_info)
        except OSError as e:
            print(f"  Could not copy {latest.name}: {e}")
    else:
        print("  No SCRPA_Combined_Executive_Summary_*.html found in 06_Output")

    return copied


def get_biweekly_info(calendar_df: pd.DataFrame, cycle: pd.Series) -> Dict[str, Any]:
    """
    Extract bi-weekly information from cycle data.

    Args:
        calendar_df: Cycle calendar DataFrame
        cycle: Series with current cycle info

    Returns:
        Dictionary with bi-weekly details
    """
    info = {
        'name': cycle['Report_Name'],
        'report_due': cycle['Report_Due_Date'].strftime('%m/%d/%Y') if isinstance(cycle['Report_Due_Date'], date) else str(cycle['Report_Due_Date']),
        'start_7': cycle['7_Day_Start'].strftime('%m/%d/%Y') if isinstance(cycle['7_Day_Start'], date) else str(cycle['7_Day_Start']),
        'end_7': cycle['7_Day_End'].strftime('%m/%d/%Y') if isinstance(cycle['7_Day_End'], date) else str(cycle['7_Day_End']),
        'start_28': cycle['28_Day_Start'].strftime('%m/%d/%Y') if isinstance(cycle['28_Day_Start'], date) else str(cycle['28_Day_Start']),
        'end_28': cycle['28_Day_End'].strftime('%m/%d/%Y') if isinstance(cycle['28_Day_End'], date) else str(cycle['28_Day_End']),
        'biweekly': None,
        'start_bw': None,
        'end_bw': None
    }

    # Check for bi-weekly name
    if 'BiWeekly_Report_Name' in cycle.index:
        bw_name = cycle['BiWeekly_Report_Name']
        if pd.notna(bw_name) and str(bw_name).strip():
            info['biweekly'] = str(bw_name).strip()

            # Calculate bi-weekly period
            start_7_date = cycle['7_Day_Start']
            if isinstance(start_7_date, date):
                start_bw_date = start_7_date - timedelta(days=7)
                info['start_bw'] = start_bw_date.strftime('%m/%d/%Y')
                info['end_bw'] = info['end_7']

    return info


def create_email_template(
    output_dir: Path,
    cycle_info: Dict[str, Any],
    generation_date: str
) -> Path:
    """
    Create email template for bi-weekly report distribution.

    Args:
        output_dir: Documentation folder path
        cycle_info: Cycle information dictionary
        generation_date: Date string for email

    Returns:
        Path to created email template
    """
    cycle_name = cycle_info['name']
    biweekly = cycle_info.get('biweekly')

    # Determine date range for email
    if biweekly and cycle_info.get('start_bw') and cycle_info.get('end_bw'):
        date_range = f"{cycle_info['start_bw']} - {cycle_info['end_bw']}"
        cycle_display = biweekly
        body_cycle = f"Bi-Weekly Cycle {biweekly} ({cycle_name})"
    else:
        date_range = f"{cycle_info['start_7']} - {cycle_info['end_7']}"
        cycle_display = cycle_name
        body_cycle = f"Cycle {cycle_name}"

    email_template = f"""Subject: SCRPA Bi-Weekly Report - Cycle {cycle_display} | {date_range}

Sir,

Please find attached the Strategic Crime Reduction Plan Analysis Combined Executive Summary for {body_cycle}.

Report Period: {date_range}
Date Generated: {generation_date}

The report includes:
- 7-Day Executive Summary with detailed incident summaries
- ArcGIS Map visuals showing incidents occurring in the last 7 days
- Statistical charts and visualizations by crime type
- 28-Day Executive Summary (operational planning)
- YTD Executive Summary (strategic analysis)

Please let me know if you have any questions or require additional information.
"""

    email_path = output_dir / 'EMAIL_TEMPLATE.txt'
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(email_template)

    return email_path


def print_summary(
    df_enhanced: pd.DataFrame,
    cycle_info: Dict[str, Any],
    paths: Dict[str, Path]
) -> None:
    """Print pipeline execution summary."""
    print("\n" + "=" * 70)
    print("SCRPA PIPELINE EXECUTION SUMMARY")
    print("=" * 70)

    print(f"\nCycle: {cycle_info['name']}")
    if cycle_info.get('biweekly'):
        print(f"Bi-Weekly: {cycle_info['biweekly']}")
    print(f"Report Due: {cycle_info['report_due']}")
    print(f"7-Day Window: {cycle_info['start_7']} - {cycle_info['end_7']}")
    if cycle_info.get('start_bw'):
        print(f"Bi-Weekly Period: {cycle_info['start_bw']} - {cycle_info['end_bw']}")

    print(f"\nOutput Directory: {paths['root']}")

    print(f"\nData Summary:")
    print(f"  Total incidents: {len(df_enhanced)}")
    if 'Period' in df_enhanced.columns:
        print(f"  Period breakdown:")
        for period, count in df_enhanced['Period'].value_counts().items():
            print(f"    {period}: {count}")

    if 'IsLagDay' in df_enhanced.columns:
        lag_count = df_enhanced['IsLagDay'].sum()
        print(f"  Lag incidents: {lag_count}")

    if 'Backfill_7Day' in df_enhanced.columns:
        backfill_count = df_enhanced['Backfill_7Day'].sum()
        print(f"  Backfill 7-Day: {backfill_count}")

    print("\nGenerated Files:")
    print(f"  Data/")
    for f in sorted(paths['data'].iterdir(), key=lambda p: p.name):
        print(f"    - {f.name}")
    print(f"  Documentation/")
    for f in sorted(paths['documentation'].iterdir(), key=lambda p: p.name):
        print(f"    - {f.name}")
    if paths['reports'].exists():
        report_files = list(paths['reports'].iterdir())
        if report_files:
            print(f"  Reports/")
            for f in sorted(report_files, key=lambda p: p.name):
                print(f"    - {f.name}")

    print("=" * 70)


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_pipeline(
    rms_path: Path,
    output_dir: Optional[Path] = None,
    report_due_date: Optional[date] = None,
    calendar_path: Path = CYCLE_CALENDAR_PATH,
    validate_reference: Optional[Path] = None,
    today_override: Optional[date] = None
) -> Dict[str, Any]:
    """
    Run the complete SCRPA data processing pipeline.

    Args:
        rms_path: Path to RMS export file
        output_dir: Optional output directory (auto-generated if not provided)
        report_due_date: Optional report due date (defaults to today)
        calendar_path: Path to cycle calendar CSV
        validate_reference: Optional path to reference CSV for validation
        today_override: Optional override for "today" (for testing)

    Returns:
        Dictionary with pipeline results
    """
    start_time = datetime.now()
    results = {
        'success': False,
        'start_time': start_time.isoformat(),
        'end_time': None,
        'files_created': []
    }

    try:
        # =================================================================
        # STEP 1: Load data
        # =================================================================
        print("=" * 70)
        print("SCRPA PIPELINE - Python-First Crime Data Processing")
        print("=" * 70)

        print(f"\n[1/6] Loading data...")
        print(f"  RMS Export: {rms_path}")
        rms_df = read_rms_export(rms_path)
        print(f"  Loaded {len(rms_df)} rows from RMS export")

        print(f"  Cycle Calendar: {calendar_path}")
        calendar_df = load_cycle_calendar(calendar_path)
        print(f"  Loaded {len(calendar_df)} cycles")

        # Set today
        today = today_override or date.today()

        # Resolve cycle
        if report_due_date:
            cycle = resolve_cycle(calendar_df, report_due_date)
        else:
            cycle = resolve_cycle(calendar_df, today)
            report_due_date = today

        if cycle is None:
            raise ValueError(f"Could not resolve cycle for date: {report_due_date}")

        cycle_info = get_biweekly_info(calendar_df, cycle)
        print(f"  Resolved cycle: {cycle_info['name']}")
        if cycle_info.get('biweekly'):
            print(f"  Bi-Weekly cycle: {cycle_info['biweekly']}")

        # =================================================================
        # STEP 2: Create output structure
        # =================================================================
        print(f"\n[2/6] Creating output structure...")

        if output_dir:
            paths = {
                'root': Path(output_dir),
                'data': Path(output_dir) / 'Data',
                'documentation': Path(output_dir) / 'Documentation',
                'reports': Path(output_dir) / 'Reports'
            }
            for path in paths.values():
                path.mkdir(parents=True, exist_ok=True)
        else:
            year = report_due_date.year
            year_dir = TIME_BASED_DIR / str(year)
            paths = create_output_structure(year_dir, cycle_info['name'], report_due_date)

        print(f"  Output directory: {paths['root']}")

        # =================================================================
        # STEP 3: Transform data
        # =================================================================
        print(f"\n[3/6] Transforming data (scrpa_transform)...")
        df_enhanced = build_all_crimes_enhanced(
            rms_df,
            calendar_df,
            report_due_date=cycle['Report_Due_Date'] if isinstance(cycle['Report_Due_Date'], date) else report_due_date,
            today=today
        )
        print(f"  Generated {len(df_enhanced)} enriched rows")

        # Filter to incident date range: 12/31/2024 through report date
        incident_start = date(2024, 12, 31)
        incident_end = report_due_date
        if hasattr(incident_end, 'date') and callable(getattr(incident_end, 'date')):
            incident_end = incident_end.date()
        if 'Incident_Date_Date' in df_enhanced.columns:
            col = pd.to_datetime(df_enhanced['Incident_Date_Date'], errors='coerce')
            mask = (col >= pd.Timestamp(incident_start)) & (col <= pd.Timestamp(incident_end))
            df_enhanced = df_enhanced.loc[mask].copy()
            print(f"  Filtered to incident date {incident_start}–{incident_end}: {len(df_enhanced)} rows")

        # Clean Data folder: remove old timestamped files (keep only stable names)
        _clean_data_folder(paths['data'])

        # Save single enriched CSV (preview-table style) – no timestamped copies
        enhanced_csv = paths['data'] / 'SCRPA_All_Crimes_Enhanced.csv'
        df_enhanced.to_csv(enhanced_csv, index=False)
        results['files_created'].append(str(enhanced_csv))
        print(f"  Saved: {enhanced_csv.name}")

        # =================================================================
        # STEP 4: Generate 7-day outputs (one CSV + one YAML only)
        # =================================================================
        print(f"\n[4/6] Generating 7-day outputs (prepare_7day_outputs)...")
        csv_7day, yaml_summary = save_7day_outputs(
            df_enhanced,
            paths['data'],
            cycle_info=cycle_info,
            timestamp=False
        )
        results['files_created'].extend([str(csv_7day), str(yaml_summary)])

        # =================================================================
        # STEP 5: Cycle documentation only (no canonical docs copied here)
        # Canonical docs: 16_Reports/SCRPA/Documentation; update via generate_documentation.py -o <path>
        # =================================================================
        print(f"\n[5/6] Writing cycle documentation...")
        yaml_data = {}
        if yaml_summary.exists():
            try:
                with open(yaml_summary, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f) or {}
            except Exception:
                pass
        period_counts = df_enhanced['Period'].value_counts() if 'Period' in df_enhanced.columns else {}
        lag_analysis = yaml_data.get('lag_analysis') or {}
        lag_dist = lag_analysis.get('lagdays_distribution') or {}
        summary_data = {
            'total': len(df_enhanced),
            'period_7': int(period_counts.get('7-Day', 0)),
            'period_28': int(period_counts.get('28-Day', 0)),
            'ytd': int(period_counts.get('YTD', 0)),
            'prior_year': int(period_counts.get('Prior Year', 0)),
            'lag_count': int(df_enhanced['IsLagDay'].sum()) if 'IsLagDay' in df_enhanced.columns else 0,
            'backfill_count': int(df_enhanced['Backfill_7Day'].sum()) if 'Backfill_7Day' in df_enhanced.columns else 0,
            'lag_mean': lag_dist.get('mean', '-'),
            'lag_median': lag_dist.get('median', '-'),
            'lag_max': lag_dist.get('max', '-'),
            '7day_by_crime_category': yaml_data.get('7day_by_crime_category') or [],
        }
        report_summary_path = write_report_summary_with_data(
            paths['documentation'], cycle_info, summary_data
        )
        results['files_created'].append(str(report_summary_path))
        briefing_path = write_chatgpt_briefing_prompt(paths['documentation'], cycle_info)
        results['files_created'].append(str(briefing_path))
        generation_date = datetime.now().strftime('%m/%d/%Y')
        email_path = create_email_template(paths['documentation'], cycle_info, generation_date)
        results['files_created'].append(str(email_path))
        print(f"  Created: {email_path.name}")

        # =================================================================
        # STEP 6: Copy reports from SCRPA_ArcPy/06_Output to cycle Reports folder
        # =================================================================
        print(f"\n[6/6] Copying reports to {paths['reports'].name}/...")
        reports_copied = _copy_scrpa_reports_to_cycle(paths['reports'], cycle_info)
        results['files_created'].extend(reports_copied)

        # =================================================================
        # OPTIONAL: Validate against reference
        # =================================================================
        if validate_reference:
            print(f"\n[VALIDATION] Comparing against: {validate_reference}")
            try:
                from validate_parity import validate_parity
                validation_result = validate_parity(enhanced_csv, validate_reference)
                results['validation'] = validation_result
                if validation_result.get('passed'):
                    print("  Validation PASSED")
                else:
                    print("  Validation FAILED - see validation report")
            except ImportError:
                print("  Validation script not available - skipping")

        # =================================================================
        # Summary
        # =================================================================
        print_summary(df_enhanced, cycle_info, paths)

        results['success'] = True
        results['cycle_info'] = cycle_info
        results['output_dir'] = str(paths['root'])
        results['row_count'] = len(df_enhanced)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        results['error'] = str(e)

    finally:
        end_time = datetime.now()
        results['end_time'] = end_time.isoformat()
        results['duration_seconds'] = (end_time - start_time).total_seconds()

    return results


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """Command-line interface for run_scrpa_pipeline."""
    parser = argparse.ArgumentParser(
        description='SCRPA Pipeline - Python-First Crime Data Processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process with auto-detected cycle (based on today)
  python run_scrpa_pipeline.py rms_export.csv

  # Process for specific report date
  python run_scrpa_pipeline.py rms_export.csv --report-date 01/27/2026

  # Process with custom output directory
  python run_scrpa_pipeline.py rms_export.csv -o Time_Based/2026/26C01W04_26_01_27

  # Process and validate against reference
  python run_scrpa_pipeline.py rms_export.csv --validate reference.csv
"""
    )
    parser.add_argument(
        'input',
        help='Path to RMS export CSV or Excel file'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output directory (auto-generated if not provided)',
        default=None
    )
    parser.add_argument(
        '--report-date',
        help='Report due date (MM/DD/YYYY format)',
        default=None
    )
    parser.add_argument(
        '--calendar',
        help='Path to cycle calendar CSV',
        default=str(CYCLE_CALENDAR_PATH)
    )
    parser.add_argument(
        '--validate',
        help='Path to reference CSV for validation',
        default=None
    )
    parser.add_argument(
        '--today',
        help='Override today date (MM/DD/YYYY format) for testing',
        default=None
    )

    args = parser.parse_args()

    # Parse dates
    report_due_date = None
    if args.report_date:
        report_due_date = datetime.strptime(args.report_date, '%m/%d/%Y').date()

    today_override = None
    if args.today:
        today_override = datetime.strptime(args.today, '%m/%d/%Y').date()

    # Run pipeline
    results = run_pipeline(
        rms_path=Path(args.input),
        output_dir=Path(args.output) if args.output else None,
        report_due_date=report_due_date,
        calendar_path=Path(args.calendar),
        validate_reference=Path(args.validate) if args.validate else None,
        today_override=today_override
    )

    # Exit code
    return 0 if results['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
