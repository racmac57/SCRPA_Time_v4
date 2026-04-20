# 🕒 2026-04-20-12-35-11
# Project: 16_Reports/SCRPA/scripts/scrpa_pipeline_trigger.py
# Author: R. A. Carucci
# Purpose: Standalone watchdog that observes _RMS/scrpa/raw/YYYY/ for new raw
#          RMS exports and auto-invokes scrpa_transform.py with the full
#          historical multi-file roll-up. Runs as a separate process from the
#          main Export_File_Watchdog to preserve single responsibility -- file
#          movement and pipeline orchestration are different failure domains.
"""
SCRPA Pipeline Trigger
======================

⚠️  Conventions: This service follows 02_ETL_Scripts/WATCHDOG_CONVENTIONS.md.
   PID-locking pattern: Convention 4 Pattern A (Python-side, see acquire_lock).
   Run the drift-detection checklist there when editing this file.

Trigger flow:
    1. Main Export_File_Watchdog moves a SCRPA_RMS_Export.xlsx drop to
       _RMS\\scrpa\\raw\\YYYY\\YYYY_MM_DD_HH_MM_SS_RMS.xlsx
    2. This service detects the new file in raw/YYYY/
    3. Debounces for 10 s and waits 5 s for OneDrive sync to settle
    4. Spawns: python scrpa_transform.py <yearly + monthly + raw glob>
    5. Pipeline writes its enriched CSV; downstream consumers pick it up

Design notes:
    * Subprocess is fire-and-forget (Popen, no wait) so a long pipeline run
      doesn't block subsequent file detections.
    * Lockfile prevents duplicate instances.
    * Rotating log mirrors the main watchdog's pattern (5 MB x 5 backups).
    * No per-file dedupe state -- the underlying scrpa_transform.py already
      dedupes by Case Number, so re-runs are idempotent.

Stop with: stop_pipeline_trigger.ps1  (or kill the python process by PID file).
"""

import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import List

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


# =============================================================================
# CONFIG
# =============================================================================

ONEDRIVE = Path.home() / "OneDrive - City of Hackensack"
RMS_ROOT = ONEDRIVE / "05_EXPORTS" / "_RMS"

# Folder to watch (recursive — picks up new YYYY/ subfolders too)
WATCH_DIR = RMS_ROOT / "scrpa" / "raw"

# Inputs to pass to scrpa_transform.py (globs are evaluated each trigger)
INPUT_GLOBS: List[Path] = [
    RMS_ROOT / "yearly" / "2025",       # 2025_ALL_RMS.xlsx
    RMS_ROOT / "monthly" / "2026",      # 2026_*_RMS.xlsx
    WATCH_DIR,                           # all raw partials, every year subfolder
]
# (2024_ALL_RMS.xlsx contributes 0 SCRPA rows under the current filter; excluded.
#  Add ONEDRIVE / "05_EXPORTS" / "_RMS" / "yearly" / "2024" if that ever changes.)

TRANSFORM_SCRIPT = (
    ONEDRIVE / "16_Reports" / "SCRPA" / "scripts" / "scrpa_transform.py"
)

# Where the pipeline writes its enriched output (cwd of the spawned subprocess)
PIPELINE_CWD = ONEDRIVE / "16_Reports" / "SCRPA"

# Local working dir for logs + lockfile
SERVICE_DIR = ONEDRIVE / "16_Reports" / "SCRPA" / "scripts"
LOG_DIR     = SERVICE_DIR / "logs"
LOG_FILE    = LOG_DIR / "scrpa_pipeline_trigger.log"
PID_FILE    = SERVICE_DIR / "scrpa_pipeline_trigger.pid"

# Debounce: don't re-trigger inside this window (handles copy + modify event burst)
DEBOUNCE_SECONDS = 10

# Wait for OneDrive sync / file write to stabilize before reading inputs
SETTLE_SECONDS = 5


# =============================================================================
# LOGGING
# =============================================================================

def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("scrpa_pipeline_trigger")
    logger.setLevel(logging.INFO)
    if logger.handlers:  # idempotent under re-entry
        return logger
    handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger


# =============================================================================
# LOCKFILE (prevent duplicate instances)
# =============================================================================

def acquire_lock(logger: logging.Logger) -> bool:
    """Return True if we got the lock; False if another instance is running."""
    if PID_FILE.exists():
        try:
            existing_pid = int(PID_FILE.read_text().strip())
            # Best-effort: check if pid is still alive on Windows
            if _pid_alive(existing_pid):
                logger.error(
                    f"Another trigger instance (PID {existing_pid}) is already "
                    f"running. Exiting."
                )
                return False
            else:
                logger.warning(
                    f"Stale PID file from PID {existing_pid}; replacing."
                )
        except (ValueError, OSError):
            logger.warning("PID file unreadable; replacing.")
    PID_FILE.write_text(str(os.getpid()))
    return True


def release_lock() -> None:
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
    except OSError:
        pass


def _pid_alive(pid: int) -> bool:
    """Cross-platform pid liveness check."""
    if pid <= 0:
        return False
    try:
        if os.name == "nt":
            # Windows: tasklist returns the row if the PID exists
            out = subprocess.check_output(
                ["tasklist", "/FI", f"PID eq {pid}"],
                stderr=subprocess.DEVNULL, timeout=5,
            )
            return str(pid).encode() in out
        else:
            os.kill(pid, 0)
            return True
    except Exception:
        return False


# =============================================================================
# INPUT COLLECTION + PIPELINE SPAWN
# =============================================================================

def collect_inputs(logger: logging.Logger) -> List[str]:
    """
    Build the file list passed to scrpa_transform.py.

    Order matters because read_rms_exports() dedupes with keep='last'.
    Sorted lexicographically per glob root so newer files (later names) win.
    """
    files: List[str] = []
    for root in INPUT_GLOBS:
        if not root.exists():
            logger.warning(f"  glob root missing: {root}")
            continue
        for fp in sorted(root.rglob("*.xlsx")):
            if fp.is_file() and fp.stat().st_size > 0:
                files.append(str(fp))
    return files


def run_pipeline(trigger_path: Path, logger: logging.Logger) -> None:
    """Spawn scrpa_transform.py in fire-and-forget mode."""
    inputs = collect_inputs(logger)
    if not inputs:
        logger.error("No input files collected; skipping pipeline run.")
        return
    cmd = [sys.executable, str(TRANSFORM_SCRIPT), *inputs]
    logger.info(
        f"Trigger fired by '{trigger_path.name}'. Spawning pipeline with "
        f"{len(inputs)} input file(s). cwd={PIPELINE_CWD}"
    )
    try:
        # Detached subprocess so trigger service doesn't block on long runs.
        # On Windows, CREATE_NEW_PROCESS_GROUP allows independent lifecycle.
        creationflags = 0
        if os.name == "nt":
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]
        proc = subprocess.Popen(
            cmd,
            cwd=str(PIPELINE_CWD),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
        )
        logger.info(f"  pipeline PID: {proc.pid}")
    except Exception as e:
        logger.error(f"  pipeline spawn FAILED: {e}")


# =============================================================================
# EVENT HANDLER
# =============================================================================

class TriggerHandler(FileSystemEventHandler):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__()
        self.logger = logger
        self._last_run = 0.0

    def on_created(self, event: FileSystemEvent) -> None:
        self._maybe_trigger(event)

    def on_moved(self, event: FileSystemEvent) -> None:
        # The main watchdog's move into raw/ shows up here as on_moved
        self._maybe_trigger(event)

    def _maybe_trigger(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        # `dest_path` exists on moved events; fall back to src_path otherwise
        path_str = getattr(event, "dest_path", None) or event.src_path
        fp = Path(path_str)
        if fp.suffix.lower() != ".xlsx":
            return
        # Only trigger on files that actually live under raw/
        try:
            fp.relative_to(WATCH_DIR)
        except ValueError:
            return  # event outside our watch root

        now = time.time()
        if (now - self._last_run) < DEBOUNCE_SECONDS:
            self.logger.info(
                f"Debounced (within {DEBOUNCE_SECONDS}s of last trigger): {fp.name}"
            )
            return
        self._last_run = now

        self.logger.info(
            f"New raw file detected: {fp.name} -- waiting {SETTLE_SECONDS}s "
            f"for write/sync to settle"
        )
        time.sleep(SETTLE_SECONDS)
        run_pipeline(fp, self.logger)


# =============================================================================
# MAIN
# =============================================================================

def main() -> int:
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info(
        f"SCRPA Pipeline Trigger starting "
        f"({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
    )
    logger.info(f"  watching   : {WATCH_DIR}")
    logger.info(f"  transform  : {TRANSFORM_SCRIPT}")
    logger.info(f"  log file   : {LOG_FILE}")
    logger.info("=" * 70)

    if not acquire_lock(logger):
        return 1

    if not WATCH_DIR.exists():
        WATCH_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created missing watch dir: {WATCH_DIR}")

    if not TRANSFORM_SCRIPT.exists():
        logger.error(f"Transform script not found: {TRANSFORM_SCRIPT}")
        release_lock()
        return 2

    handler = TriggerHandler(logger)
    observer = Observer()
    observer.schedule(handler, str(WATCH_DIR), recursive=True)
    observer.start()
    logger.info("Trigger service is now running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Stop requested (KeyboardInterrupt).")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
    finally:
        observer.stop()
        observer.join(timeout=5)
        release_lock()
        logger.info("Trigger service stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
