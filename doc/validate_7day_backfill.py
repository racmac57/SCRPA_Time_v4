// 2025-12-29-19-30-00
# SCRPA_Time_v3/validate_7day_backfill.py
# Author: R. A. Carucci
# Purpose: Validate 7-Day period incidents vs backfill cases for SCRPA reporting accuracy

"""
SCRPA 7-Day vs Backfill Validation Script

This script validates that incidents are correctly categorized as either:
- IN_CYCLE: Incident occurred within current 7-day cycle boundaries
- BACKFILL: Incident occurred before cycle but reported during cycle
- OUTSIDE_CYCLE: Not relevant to current reporting period

Usage:
    python validate_7day_backfill.py <rms_csv_file> <cycle_start> <cycle_end>
    
Example:
    python validate_7day_backfill.py 2025_12_29_18_46_24_SCRPA_RMS.csv 2025-12-23 2025-12-29
"""

import pandas as pd
import sys
from datetime import datetime
from pathlib import Path

class SCRPA7DayValidator:
    
    def __init__(self, rms_file, cycle_start, cycle_end):
        """Initialize validator with RMS data and cycle dates."""
        self.rms_file = Path(rms_file)
        self.cycle_start = pd.to_datetime(cycle_start).date()
        self.cycle_end = pd.to_datetime(cycle_end).date()
        self.df = None
        self.results = {}
        
    def load_data(self):
        """Load and prepare RMS export data."""
        print(f"\n📂 Loading: {self.rms_file.name}")
        self.df = pd.read_csv(self.rms_file)
        
        # Convert dates
        self.df['Incident Date'] = pd.to_datetime(self.df['Incident Date'], errors='coerce')
        self.df['Report Date'] = pd.to_datetime(self.df['Report Date'], errors='coerce')
        
        print(f"✅ Loaded {len(self.df):,} total records")
        
    def categorize_incidents(self, crime_filter=None):
        """
        Categorize incidents as IN_CYCLE, BACKFILL, or OUTSIDE_CYCLE.
        
        Args:
            crime_filter: Optional list of crime types to filter (case-insensitive partial match)
        """
        # Apply crime filter if specified
        if crime_filter:
            filter_mask = pd.Series([False] * len(self.df))
            for crime_type in crime_filter:
                filter_mask |= (
                    self.df['Incident Type_1'].str.contains(crime_type, case=False, na=False) |
                    self.df['Incident Type_2'].str.contains(crime_type, case=False, na=False) |
                    self.df['Incident Type_3'].str.contains(crime_type, case=False, na=False)
                )
            filtered_df = self.df[filter_mask].copy()
            filter_label = ", ".join(crime_filter)
        else:
            filtered_df = self.df.copy()
            filter_label = "ALL CRIMES"
        
        # Categorize
        filtered_df['Category'] = filtered_df.apply(
            lambda row: self._categorize_row(row), axis=1
        )
        
        return filtered_df, filter_label
    
    def _categorize_row(self, row):
        """Categorize individual incident row."""
        incident_date = row['Incident Date']
        report_date = row['Report Date']
        
        # Handle missing dates
        if pd.isna(incident_date):
            return 'MISSING_INCIDENT_DATE'
        if pd.isna(report_date):
            return 'MISSING_REPORT_DATE'
        
        # Convert to date objects
        incident_date = incident_date.date()
        report_date = report_date.date()
        
        # Categorization logic
        if self.cycle_start <= incident_date <= self.cycle_end:
            return 'IN_CYCLE'
        elif (incident_date < self.cycle_start and 
              self.cycle_start <= report_date <= self.cycle_end):
            return 'BACKFILL'
        else:
            return 'OUTSIDE_CYCLE'
    
    def generate_report(self, crime_types=None):
        """Generate validation report for specified crime types."""
        
        print("\n" + "="*80)
        print(f"SCRPA 7-DAY VALIDATION REPORT")
        print(f"Cycle: {self.cycle_start} to {self.cycle_end}")
        print("="*80)
        
        # Process each crime type
        crime_configs = [
            {'name': 'Burglary', 'filters': ['Burglary']},
            {'name': 'Motor Vehicle Theft', 'filters': ['Motor Vehicle Theft']},
            {'name': 'Robbery', 'filters': ['Robbery']},
            {'name': 'Sexual Offenses', 'filters': ['Sexual']},
            {'name': 'ALL CRIMES', 'filters': None}
        ]
        
        if crime_types:
            crime_configs = [c for c in crime_configs if c['name'] in crime_types]
        
        for config in crime_configs:
            self._print_crime_report(config['name'], config['filters'])
    
    def _print_crime_report(self, crime_name, crime_filter):
        """Print detailed report for specific crime type."""
        
        filtered_df, filter_label = self.categorize_incidents(crime_filter)
        
        print(f"\n{'─'*80}")
        print(f"📊 {crime_name.upper()}")
        print(f"{'─'*80}")
        
        # Count by category
        category_counts = filtered_df['Category'].value_counts()
        
        in_cycle = category_counts.get('IN_CYCLE', 0)
        backfill = category_counts.get('BACKFILL', 0)
        outside = category_counts.get('OUTSIDE_CYCLE', 0)
        
        print(f"✅ IN_CYCLE (should appear in 7-Day chart):      {in_cycle:3d}")
        print(f"⚠️  BACKFILL (lagday table ONLY):                {backfill:3d}")
        print(f"❌ OUTSIDE_CYCLE (not in current report):       {outside:3d}")
        
        # Show details for IN_CYCLE and BACKFILL cases
        for category in ['IN_CYCLE', 'BACKFILL']:
            cat_df = filtered_df[filtered_df['Category'] == category]
            if len(cat_df) > 0:
                print(f"\n{category} DETAILS:")
                for idx, row in cat_df.iterrows():
                    case_num = row['Case Number']
                    inc_date = row['Incident Date'].strftime('%m/%d/%y')
                    rep_date = row['Report Date'].strftime('%m/%d/%y')
                    lag_days = (row['Report Date'] - row['Incident Date']).days
                    inc_type = (row['Incident Type_1'] or 
                               row['Incident Type_2'] or 
                               row['Incident Type_3'] or 'Unknown')
                    
                    print(f"  • {case_num:12s} | Inc: {inc_date} | Rep: {rep_date} | "
                          f"Lag: {lag_days:3d} | {inc_type[:40]}")
        
        # Validation message
        if in_cycle == 0 and backfill > 0:
            print(f"\n🔴 CRITICAL: 7-Day chart should show 0 incidents, NOT {backfill}!")
            print(f"   All {backfill} case(s) are BACKFILL (lagdays only)")
        elif in_cycle > 0:
            print(f"\n✅ 7-Day chart should show exactly {in_cycle} incident(s)")
            if backfill > 0:
                print(f"✅ Lagday table should show {backfill} additional incident(s)")
    
    def export_validation_csv(self, output_dir='.'):
        """Export categorized data to CSV for further analysis."""
        output_path = Path(output_dir) / f"validation_{self.cycle_start}_{self.cycle_end}.csv"
        
        all_categorized, _ = self.categorize_incidents()
        all_categorized.to_csv(output_path, index=False)
        
        print(f"\n💾 Validation data exported: {output_path}")
        return output_path

def main():
    """Main execution function."""
    
    if len(sys.argv) < 4:
        print("Usage: python validate_7day_backfill.py <rms_csv> <cycle_start> <cycle_end>")
        print("\nExample:")
        print("  python validate_7day_backfill.py 2025_12_29_18_46_24_SCRPA_RMS.csv 2025-12-23 2025-12-29")
        sys.exit(1)
    
    rms_file = sys.argv[1]
    cycle_start = sys.argv[2]
    cycle_end = sys.argv[3]
    
    # Initialize validator
    validator = SCRPA7DayValidator(rms_file, cycle_start, cycle_end)
    
    # Load data
    validator.load_data()
    
    # Generate full report
    validator.generate_report()
    
    # Export validation CSV
    validator.export_validation_csv()
    
    print("\n" + "="*80)
    print("✅ Validation complete!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
