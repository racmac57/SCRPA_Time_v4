# 🕒 2026_01_13_11_32_58
# Project: scripts/export_enriched_data_and_email.py
# Author: R. A. Carucci
# Purpose: Export enriched All_Crimes data from Power BI preview table to CSV, create filtered 7-Day + LagDay CSV, remove rms_summary files, and generate email template with cycle name and date range

"""
SCRPA Enriched Data Export and Email Template Generator

This script:
1. Exports enriched All_Crimes data from Power BI preview table to CSV
2. Creates filtered 7-Day + LagDay CSV
3. Removes rms_summary.html files from Reports folder
4. Creates email template as .txt file

Run this after Power BI refresh and CSV export.
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import re

# Configuration
BASE_DIR = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA")
REPORT_DATE_ENV = os.environ.get('REPORT_DATE', None)

def find_latest_report_folder():
    """Find the most recently created report folder."""
    time_based_dir = BASE_DIR / "Time_Based"
    if not time_based_dir.exists():
        raise FileNotFoundError(f"Time_Based directory not found: {time_based_dir}")
    
    # Get all year folders
    year_folders = [d for d in time_based_dir.iterdir() if d.is_dir() and d.name.isdigit()]
    if not year_folders:
        raise FileNotFoundError("No year folders found in Time_Based")
    
    # Get all report folders
    report_folders = []
    for year_folder in year_folders:
        report_folders.extend([d for d in year_folder.iterdir() if d.is_dir()])
    
    if not report_folders:
        raise FileNotFoundError("No report folders found")
    
    # Sort by modification time, get most recent
    latest_folder = max(report_folders, key=lambda x: x.stat().st_mtime)
    return latest_folder

def find_preview_table_csv(report_folder):
    """Find the All_Crime preview table CSV in the report folder."""
    # Look for All_Crime_*.csv in the report folder root
    pattern = "All_Crime_*.csv"
    matches = list(report_folder.glob(pattern))
    
    if not matches:
        # Try in Data subfolder
        data_folder = report_folder / "Data"
        if data_folder.exists():
            matches = list(data_folder.glob(pattern))
    
    if not matches:
        raise FileNotFoundError(f"All_Crime preview CSV not found in {report_folder}")
    
    # Return most recent if multiple
    return max(matches, key=lambda x: x.stat().st_mtime)

def extract_cycle_info(report_folder_name):
    """Extract cycle and date range from folder name or Power BI."""
    # Folder name format: YYCMMWww_YY_MM_DD
    # Example: 26C01W01_26_01_06
    match = re.match(r'(\d{2})C(\d{2})W(\d{2})_(\d{2})_(\d{2})_(\d{2})', report_folder_name)
    if match:
        year, month, week, y, m, d = match.groups()
        cycle = f"{year}C{month}W{week}"
        # Date will be extracted from cycle calendar or Power BI
        return cycle, None
    
    return None, None

def get_date_range_from_cycle_calendar(cycle_name, report_date_str):
    """Get date range from cycle calendar CSV."""
    cycle_calendar_path = Path(
        r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv"
    )
    
    if not cycle_calendar_path.exists():
        return None, None
    
    try:
        df = pd.read_csv(cycle_calendar_path)
        # Find row matching cycle
        if 'Report_Name' in df.columns:
            match = df[df['Report_Name'] == cycle_name]
            if not match.empty:
                row = match.iloc[0]
                start_date = pd.to_datetime(row['7_Day_Start']).strftime('%m/%d/%Y')
                end_date = pd.to_datetime(row['7_Day_End']).strftime('%m/%d/%Y')
                return start_date, end_date
    except Exception as e:
        print(f"Warning: Could not read cycle calendar: {e}")
    
    return None, None

def export_enriched_data(preview_csv_path, report_folder):
    """Export enriched data to CSV files."""
    print(f"Reading preview table: {preview_csv_path}")
    df = pd.read_csv(preview_csv_path)
    
    data_folder = report_folder / "Data"
    data_folder.mkdir(exist_ok=True)
    
    # Get cycle and date info
    cycle_name, _ = extract_cycle_info(report_folder.name)
    report_date_str = REPORT_DATE_ENV or datetime.now().strftime('%m/%d/%Y')
    start_date, end_date = get_date_range_from_cycle_calendar(cycle_name, report_date_str)
    
    if not start_date or not end_date:
        # Fallback: try to get from folder name
        print("Warning: Could not get date range from cycle calendar, using defaults")
        start_date = "12/30/2025"
        end_date = "01/05/2026"
    
    date_range = f"{start_date} - {end_date}"
    
    # 1. Export ALL enriched incidents
    all_incidents_file = data_folder / f"SCRPA_All_Incidents_Enriched_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(all_incidents_file, index=False)
    print(f"✅ Exported all enriched incidents: {all_incidents_file.name}")
    
    # 2. Filter for 7-Day + LagDay incidents
    # 7-Day: Period = "7-Day"
    # LagDay: IsLagDay = TRUE (or LagDays > 0 and Period might be different)
    seven_day_mask = df['Period'] == '7-Day'
    lagday_mask = df.get('IsLagDay', pd.Series([False] * len(df))) == True
    
    # Also check if LagDays column exists and > 0
    if 'LagDays' in df.columns:
        lagday_mask = lagday_mask | (df['LagDays'] > 0)
    
    # Combined filter: 7-Day OR LagDay
    filtered_mask = seven_day_mask | lagday_mask
    df_filtered = df[filtered_mask].copy()
    
    filtered_file = data_folder / f"SCRPA_7Day_LagDay_Enriched_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_filtered.to_csv(filtered_file, index=False)
    print(f"✅ Exported 7-Day + LagDay incidents ({len(df_filtered)} rows): {filtered_file.name}")
    
    # Get folder creation date for "Date Generated"
    folder_creation_time = datetime.fromtimestamp(report_folder.stat().st_ctime)
    generation_date = folder_creation_time.strftime('%B %d, %Y')
    
    return cycle_name, date_range, generation_date

def remove_rms_summary_files(report_folder):
    """Remove rms_summary.html and .pdf files from Reports folder."""
    reports_folder = report_folder / "Reports"
    if not reports_folder.exists():
        print("⚠️  Reports folder not found, skipping removal")
        return
    
    removed_count = 0
    for pattern in ["*_rms_summary.html", "*_rms_summary.pdf"]:
        for file in reports_folder.glob(pattern):
            try:
                file.unlink()
                print(f"✅ Removed: {file.name}")
                removed_count += 1
            except Exception as e:
                print(f"⚠️  Could not remove {file.name}: {e}")
    
    if removed_count == 0:
        print("ℹ️  No rms_summary files found to remove")

def create_email_template(report_folder, cycle_name, date_range, generation_date):
    """Create email template as .txt file with exact format specified."""
    # Format date generated as MM/DD/YYYY
    try:
        # Try to parse generation_date if it's in "Month Day, Year" format
        gen_date_obj = datetime.strptime(generation_date, '%B %d, %Y')
        date_generated = gen_date_obj.strftime('%m/%d/%Y')
    except:
        # If parsing fails, use current date
        date_generated = datetime.now().strftime('%m/%d/%Y')
    
    email_template = f"""Subject: SCRPA Bi-Weekly Report - Cycle {cycle_name} | {date_range}

Sir,

Please find attached the Strategic Crime Reduction Plan Analysis Combined Executive Summary for Cycle {cycle_name}.

Report Period: {date_range}
Date Generated: {date_generated}

The report includes:
• 7-Day Executive Summary with detailed incident summaries
• ArcGIS Map visuals showing incidents occurring in the last 7 days
• Statistical charts and visualizations by crime type
• 28-Day Executive Summary (operational planning)
• YTD Executive Summary (strategic analysis)

Please let me know if you have any questions or require additional information.
"""
    
    # Save to Documentation folder
    doc_folder = report_folder / "Documentation"
    doc_folder.mkdir(exist_ok=True)
    
    email_file = doc_folder / "EMAIL_TEMPLATE.txt"
    with open(email_file, 'w', encoding='utf-8') as f:
        f.write(email_template)
    
    print(f"✅ Created email template: {email_file.name}")

def main():
    """Main execution."""
    print("=" * 60)
    print("SCRPA Enriched Data Export and Email Template Generator")
    print("=" * 60)
    
    try:
        # Find latest report folder
        report_folder = find_latest_report_folder()
        print(f"\n📁 Report folder: {report_folder.name}")
        
        # Find preview table CSV
        preview_csv = find_preview_table_csv(report_folder)
        print(f"📄 Preview table: {preview_csv.name}")
        
        # Export enriched data
        cycle_name, date_range, generation_date = export_enriched_data(preview_csv, report_folder)
        
        # Remove rms_summary files
        print("\n🗑️  Removing rms_summary files...")
        remove_rms_summary_files(report_folder)
        
        # Create email template
        print("\n📧 Creating email template...")
        create_email_template(report_folder, cycle_name or "26C01W01", date_range or "12/30/2025 - 01/05/2026", generation_date)
        
        print("\n" + "=" * 60)
        print("✅ All tasks completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
