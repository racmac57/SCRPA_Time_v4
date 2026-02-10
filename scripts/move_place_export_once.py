"""
One-time move: Desktop SCRPA_Place_RMS_Export.xlsx -> 05_EXPORTS/_RMS/scrpa/place
Uses same naming as watchdog: YYYY_MM_DD_HH_MM_SS_SCRPA_Place_RMS.xlsx
Run this if the watchdog hasn't picked up the file (e.g. before restarting watchdog).
"""
from pathlib import Path
from datetime import datetime
import shutil

DESKTOP = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\Desktop")
DEST_DIR = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa\place")
SOURCE_NAME = "SCRPA_Place_RMS_Export.xlsx"

def main():
    src = DESKTOP / SOURCE_NAME
    if not src.exists():
        print(f"File not found: {src}")
        return 1
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    dest_name = f"{ts}_SCRPA_Place_RMS.xlsx"
    dest = DEST_DIR / dest_name
    try:
        shutil.move(str(src), str(dest))
        print(f"Moved: {SOURCE_NAME} -> {dest}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
