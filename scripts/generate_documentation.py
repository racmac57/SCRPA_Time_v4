# 2026_01_28
# Project: scripts/generate_documentation.py
# Author: R. A. Carucci
# Purpose: Generate structured documentation outputs for SCRPA system.

"""
SCRPA Documentation Generator

This module creates structured documentation outputs:
1. data_dictionary.yaml + .json - Field definitions and schema
2. PROJECT_SUMMARY.yaml + .json - Project overview (data sources, script flow, dependencies)
3. claude.md - System specification for Claude AI
4. SCRPA_Report_Summary.md - Report-specific summary template

All outputs are placed in the Documentation folder of the report cycle directory.
"""

import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import argparse


# =============================================================================
# DATA DICTIONARY DEFINITION
# =============================================================================

DATA_DICTIONARY = {
    'metadata': {
        'title': 'SCRPA All_Crimes Data Dictionary',
        'version': '1.0.0',
        'last_updated': None,  # Set at generation time
        'description': 'Field definitions for the SCRPA enriched crime data output'
    },
    'source_fields': {
        'Case Number': {
            'type': 'string',
            'description': 'Unique case identifier from RMS',
            'example': '25-009438',
            'source': 'RMS Export'
        },
        'Incident Date': {
            'type': 'date',
            'description': 'Date the incident occurred (raw from RMS)',
            'format': 'MM/DD/YYYY or null',
            'source': 'RMS Export'
        },
        'Incident Time': {
            'type': 'time',
            'description': 'Time the incident occurred',
            'format': 'HH:MM:SS or HH:MM AM/PM',
            'source': 'RMS Export'
        },
        'Incident Date_Between': {
            'type': 'date',
            'description': 'Alternative incident date (for range incidents)',
            'source': 'RMS Export'
        },
        'Incident Time_Between': {
            'type': 'time',
            'description': 'Alternative incident time (for range incidents)',
            'source': 'RMS Export'
        },
        'Report Date': {
            'type': 'date',
            'description': 'Date the incident was reported/entered in RMS',
            'source': 'RMS Export'
        },
        'Report Time': {
            'type': 'time',
            'description': 'Time the incident was reported',
            'source': 'RMS Export'
        },
        'Incident Type_1': {
            'type': 'string',
            'description': 'Primary incident/offense type',
            'example': 'Robbery',
            'source': 'RMS Export'
        },
        'Incident Type_2': {
            'type': 'string',
            'description': 'Secondary incident/offense type',
            'nullable': True,
            'source': 'RMS Export'
        },
        'Incident Type_3': {
            'type': 'string',
            'description': 'Tertiary incident/offense type',
            'nullable': True,
            'source': 'RMS Export'
        },
        'FullAddress': {
            'type': 'string',
            'description': 'Full address of incident location',
            'example': '400 Hackensack Avenue, Hackensack, NJ, 07601',
            'source': 'RMS Export'
        },
        'Grid': {
            'type': 'string',
            'description': 'Grid reference for location',
            'example': 'I6',
            'source': 'RMS Export'
        },
        'Zone': {
            'type': 'integer',
            'description': 'Police zone number (whole number, observed range 5-9)',
            'example': '9',
            'format': 'Integer (no decimals)',
            'source': 'RMS Export'
        },
        'Narrative': {
            'type': 'text',
            'description': 'Detailed incident narrative (cleaned of special characters)',
            'source': 'RMS Export'
        },
        'NIBRS Classification': {
            'type': 'string',
            'description': 'NIBRS offense code and description',
            'example': '120 = Robbery',
            'source': 'RMS Export'
        }
    },
    'computed_fields': {
        'BestTimeValue': {
            'type': 'time',
            'description': 'Best available time of incident. Used for time-of-day analysis.',
            'format': 'HH:mm:ss',
            'calculation': 'Cascade: Incident Time → if null, Incident Time_Between → if null, Report Time',
            'usage': 'Derives Incident_Time (HH:MM:SS), StartOfHour, TimeOfDay, and TimeOfDay_SortKey',
            'source': 'Computed'
        },
        'TimeSource': {
            'type': 'string',
            'description': 'Source of BestTimeValue',
            'values': ['Incident Time', 'Incident Time_Between', 'Report Time', 'None'],
            'source': 'Computed'
        },
        'Incident_Time': {
            'type': 'string',
            'description': 'Formatted incident time (HH:MM:SS)',
            'format': 'HH:MM:SS',
            'default': '00:00:00',
            'source': 'Computed'
        },
        'Incident_Date': {
            'type': 'string',
            'description': 'Formatted incident date text',
            'format': 'MM/DD/YY',
            'calculation': 'Coalesce(Incident Date, Incident Date_Between, Report Date)',
            'source': 'Computed'
        },
        'Incident_Date_Date': {
            'type': 'date',
            'description': 'Best incident date as date type (for calculations)',
            'calculation': 'Coalesce(Incident Date, Incident Date_Between, Report Date)',
            'source': 'Computed'
        },
        'Report_Date': {
            'type': 'date',
            'description': 'Resolved report date',
            'calculation': 'Coalesce(Report Date, EntryDate, Incident_Date_Date)',
            'source': 'Computed'
        },
        'Report_Date_ForLagday': {
            'type': 'date',
            'description': 'Report date for lag day calculation - CRITICAL: NO Incident_Date fallback',
            'calculation': 'Coalesce(Report Date, EntryDate)',
            'note': 'Used for IsLagDay and LagDays. When null, lag logic yields false/0.',
            'source': 'Computed'
        },
        'Report_Date_Text': {
            'type': 'string',
            'description': 'Formatted report date text',
            'format': 'MM/DD/YY',
            'source': 'Computed'
        },
        'IncidentToReportDays': {
            'type': 'integer',
            'description': 'Days between incident and report',
            'calculation': 'Report_Date - Incident_Date_Date',
            'source': 'Computed'
        },
        'Period': {
            'type': 'string',
            'description': 'Reporting period classification based on Incident_Date',
            'values': ['7-Day', '28-Day', 'YTD', 'Prior Year', 'Historical'],
            'priority_order': '7-Day > Prior Year > 28-Day > YTD > Historical',
            'note': 'Based on Incident_Date, NOT Report_Date. 7-Day uses calendar 7_Day_Start/7_Day_End for the resolved cycle (fixed window), not "today minus 7 days".',
            'source': 'Computed'
        },
        '_Period_Debug': {
            'type': 'string',
            'description': 'Debug info for period calculation (for validation)',
            'source': 'Computed'
        },
        'Period_SortKey': {
            'type': 'integer',
            'description': 'Sort key for Period field',
            'mapping': {'7-Day': 1, '28-Day': 2, 'YTD': 3, 'Prior Year': 4, 'Historical': 5},
            'source': 'Computed'
        },
        'cycle_name': {
            'type': 'string',
            'description': 'Weekly cycle name (Report_Name) that contains Incident_Date',
            'example': '26C01W04',
            'note': 'Set to "Historical" if Incident_Date falls outside all calendar 7-day windows (e.g., day after cycle end)',
            'source': 'Computed'
        },
        'Backfill_7Day': {
            'type': 'boolean',
            'description': 'True if incident occurred before cycle but reported during current 7-day window',
            'calculation': 'Incident_Date < CycleStart AND Report_Date_ForLagday IN [CycleStart, CycleEnd]',
            'source': 'Computed'
        },
        'cycle_name_adjusted': {
            'type': 'string',
            'description': 'Cycle name adjusted for backfill cases. For backfill lag incidents, attributes them to current report cycle.',
            'calculation': 'If Backfill_7Day=True then CurrentCycleName (current report cycle) else cycle_name',
            'note': 'Allows lag incidents reported during current 7-day window to be attributed to the current cycle for reporting',
            'source': 'Computed'
        },
        'BiWeekly_Report_Name': {
            'type': 'string',
            'description': 'Bi-weekly report name from cycle calendar (e.g., 26BW02)',
            'example': '26BW02',
            'note': 'Populated from cycle calendar BiWeekly_Report_Name column when present. Format: YYBW## (YY=year, BW=bi-weekly, ##=period number)',
            'source': 'Computed from cycle calendar'
        },
        'IsCurrent7DayCycle': {
            'type': 'boolean',
            'description': 'True if Report_Date_ForLagday falls within current 7-day cycle window',
            'calculation': 'Report_Date_ForLagday >= CycleStart AND Report_Date_ForLagday <= CycleEnd',
            'source': 'Computed'
        },
        'IsLagDay': {
            'type': 'boolean',
            'description': 'True if incident occurred before the cycle that contains Report_Date_ForLagday',
            'calculation': 'Incident_Date < CycleStartForReport (using 3-tier cycle resolution)',
            'source': 'Computed'
        },
        'LagDays': {
            'type': 'integer',
            'description': 'Days between incident and cycle start (NOT Report_Date)',
            'calculation': 'CycleStartForReport - Incident_Date (in days)',
            'note': 'CRITICAL: This is cycle-relative, not report-date-relative',
            'source': 'Computed'
        },
        'StartOfHour': {
            'type': 'string',
            'description': 'Start of hour for time grouping',
            'format': 'HH:00:00',
            'source': 'Computed'
        },
        'TimeOfDay': {
            'type': 'string',
            'description': 'Time of day classification',
            'values': [
                'Late Night (00:00-03:59)',
                'Early Morning (04:00-07:59)',
                'Morning (08:00-11:59)',
                'Afternoon (12:00-15:59)',
                'Evening Peak (16:00-19:59)',
                'Night (20:00-23:59)',
                'Unknown Time'
            ],
            'source': 'Computed'
        },
        'TimeOfDay_SortKey': {
            'type': 'integer',
            'description': 'Sort key for TimeOfDay field',
            'mapping': {
                'Late Night (00:00-03:59)': 1,
                'Early Morning (04:00-07:59)': 2,
                'Morning (08:00-11:59)': 3,
                'Afternoon (12:00-15:59)': 4,
                'Evening Peak (16:00-19:59)': 5,
                'Night (20:00-23:59)': 6,
                'Unknown Time': 99
            },
            'source': 'Computed'
        },
        'ALL_INCIDENTS': {
            'type': 'string',
            'description': 'Concatenation of all incident types',
            'calculation': 'Incident Type_1 + ", " + Incident Type_2 + ", " + Incident Type_3',
            'source': 'Computed'
        },
        'Crime_Category': {
            'type': 'string',
            'description': 'High-level crime category for reporting',
            'values': [
                'Motor Vehicle Theft',
                'Burglary Auto',
                'Burglary - Comm & Res',
                'Robbery',
                'Sexual Offenses',
                'Other'
            ],
            'source': 'Computed'
        },
        'Incident_Type_1_Norm': {
            'type': 'string',
            'description': 'Normalized incident type (Attempted Burglary -> Burglary)',
            'source': 'Computed'
        },
        'Vehicle_1': {
            'type': 'string',
            'description': 'Formatted vehicle 1 info (STATE - REG, MAKE/MODEL)',
            'nullable': True,
            'source': 'Computed'
        },
        'Vehicle_2': {
            'type': 'string',
            'description': 'Formatted vehicle 2 info',
            'nullable': True,
            'source': 'Computed'
        },
        'Vehicle_1_and_Vehicle_2': {
            'type': 'string',
            'description': 'Combined vehicle info with pipe separator',
            'nullable': True,
            'source': 'Computed'
        },
        'Clean_Address': {
            'type': 'string',
            'description': 'Address with city/state suffix removed',
            'example': '400 Hackensack Avenue',
            'source': 'Computed'
        },
        'IncidentKey': {
            'type': 'string',
            'description': 'Key for category lookup (ALL_INCIDENTS or Incident Type_1)',
            'source': 'Computed'
        },
        'Category_Type': {
            'type': 'string',
            'description': 'Incident category classification (e.g., Criminal Incidents, Public Safety and Welfare)',
            'lookup': '09_Reference/Classifications/CallTypes/CallType_Categories.csv',
            'lookup_method': 'Exact match on Incident column, then Incident_Norm column',
            'default': 'Unknown (when no match found)',
            'source': 'Computed via CallType lookup'
        },
        'Response_Type': {
            'type': 'string',
            'description': 'Response priority classification',
            'values': ['Emergency', 'Urgent', 'Routine', 'Unknown'],
            'lookup': '09_Reference/Classifications/CallTypes/CallType_Categories.csv',
            'lookup_method': 'Exact match on Incident column, then Incident_Norm column',
            'default': 'Unknown (when no match found)',
            'source': 'Computed via CallType lookup'
        },
        'Time_Validation': {
            'type': 'string',
            'description': 'Debug string showing time cascade resolution',
            'source': 'Computed'
        }
    }
}


# =============================================================================
# PROJECT SUMMARY DEFINITION
# =============================================================================

def get_project_summary(cycle_info: Optional[Dict] = None) -> Dict[str, Any]:
    """Generate PROJECT_SUMMARY content."""
    return {
        'metadata': {
            'title': 'SCRPA Crime Reporting System - Project Summary',
            'version': '2.0.0 (Python-First)',
            'last_updated': None,  # Set at generation time
            'description': 'Python-first crime data transformation system for bi-weekly SCRPA reporting'
        },
        'architecture': {
            'overview': 'Python-first processing where all data transformations occur in Python scripts. Power BI consumes pre-processed CSV files with minimal M code (simple imports only).',
            'data_flow': [
                '1. RMS Export (Excel/CSV) -> Raw crime incident data',
                '2. scrpa_transform.py -> Enriched All_Crimes data (cycle, lag days, period, etc.)',
                '3. prepare_7day_outputs.py -> Filtered 7-day data + lag day metadata',
                '4. generate_documentation.py -> Documentation files',
                '5. Power BI (All_Crimes_Simple.m) -> Simple CSV import, no transformations',
                '6. export_enriched_data_and_email.py -> Email template + organized outputs'
            ],
            'diagram': '''
RMS Export
    |
    v
[scrpa_transform.py] -----> SCRPA_All_Crimes_Enhanced.csv
    |
    v
[prepare_7day_outputs.py] --> SCRPA_7Day_With_LagFlags.csv
    |                         SCRPA_7Day_Lag_Only.csv
    |                         SCRPA_7Day_Summary.yaml/json
    v
[generate_documentation.py] -> data_dictionary.yaml/json
    |                          PROJECT_SUMMARY.yaml/json
    |                          claude.md
    |                          SCRPA_Report_Summary.md
    v
[Power BI - All_Crimes_Simple.m] --> Import CSVs (no transforms)
    |
    v
[export_enriched_data_and_email.py] -> EMAIL_TEMPLATE.txt
                                       Organized folder structure
'''
        },
        'data_sources': {
            'rms_export': {
                'description': 'Raw crime incident export from Records Management System',
                'location': 'Varies per export (typically Time_Based/YYYY/CYCLE_NAME/)',
                'format': 'CSV or Excel (.xlsx)',
                'refresh': 'Weekly/Bi-weekly before report generation'
            },
            'cycle_calendar': {
                'description': 'SCRPA 7-Day and 28-Day cycle definitions',
                'location': r'C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv',
                'format': 'CSV',
                'columns': ['Report_Due_Date', '7_Day_Start', '7_Day_End', '28_Day_Start', '28_Day_End', 'Report_Name', 'BiWeekly_Report_Name'],
                'refresh': 'Annually (at year start)'
            }
        },
        'scripts': {
            'scrpa_transform.py': {
                'purpose': 'Core data transformation engine',
                'inputs': ['RMS Export', 'Cycle Calendar'],
                'outputs': ['SCRPA_All_Crimes_Enhanced.csv'],
                'key_functions': [
                    'read_rms_export() - Load raw data',
                    'resolve_cycle() - 3-tier cycle lookup',
                    'calculate_lag_days() - LagDays = CycleStart - Incident_Date',
                    'classify_period() - Incident_Date-based period classification',
                    'build_all_crimes_enhanced() - Main transform pipeline'
                ],
                'dependencies': ['pandas', 'numpy']
            },
            'prepare_7day_outputs.py': {
                'purpose': 'Filter 7-day data and generate lag metadata',
                'inputs': ['SCRPA_All_Crimes_Enhanced.csv'],
                'outputs': [
                    'SCRPA_7Day_With_LagFlags.csv',
                    'SCRPA_7Day_Lag_Only.csv',
                    'SCRPA_7Day_Summary.yaml',
                    'SCRPA_7Day_Summary.json'
                ],
                'key_functions': [
                    'filter_7day_by_report_date() - IsCurrent7DayCycle filter',
                    'extract_backfill_lag() - Backfill_7Day filter',
                    'generate_lagday_summary() - Metadata generation'
                ],
                'dependencies': ['pandas', 'pyyaml']
            },
            'generate_documentation.py': {
                'purpose': 'Generate structured documentation',
                'inputs': ['Cycle info', 'System constants'],
                'outputs': [
                    'data_dictionary.yaml',
                    'data_dictionary.json',
                    'PROJECT_SUMMARY.yaml',
                    'PROJECT_SUMMARY.json',
                    'claude.md',
                    'SCRPA_Report_Summary.md'
                ],
                'dependencies': ['pyyaml']
            },
            'export_enriched_data_and_email.py': {
                'purpose': 'Export data and generate email template',
                'inputs': ['Power BI preview CSV', 'Cycle Calendar'],
                'outputs': [
                    'SCRPA_All_Incidents_Enriched_*.csv',
                    'SCRPA_7Day_LagDay_Enriched_*.csv',
                    'EMAIL_TEMPLATE.txt'
                ],
                'key_functions': [
                    'get_date_range_and_biweekly_from_calendar() - Bi-weekly date calculation',
                    'create_email_template() - Email generation with bi-weekly support'
                ]
            },
            'run_scrpa_pipeline.py': {
                'purpose': 'Main orchestration script',
                'inputs': ['RMS Export path', 'Report due date', 'Output directory'],
                'outputs': ['All generated files in structured folders'],
                'workflow': [
                    '1. Load RMS export and cycle calendar',
                    '2. Run scrpa_transform.py',
                    '3. Run prepare_7day_outputs.py',
                    '4. Run generate_documentation.py',
                    '5. Validate outputs',
                    '6. Generate summary report'
                ]
            },
            'validate_parity.py': {
                'purpose': 'Validate Python outputs against M code reference',
                'inputs': ['Python output CSV', 'Reference CSV (from M code)'],
                'outputs': ['Validation report'],
                'checks': [
                    'Row count match',
                    'Column match',
                    'LagDays calculation',
                    'Period classification',
                    'Backfill_7Day logic'
                ]
            }
        },
        'output_structure': {
            'description': 'Folder structure for each reporting cycle',
            'template': '''
Time_Based/YYYY/{CYCLE_NAME}_{YY_MM_DD}/
├── Data/
│   ├── SCRPA_All_Crimes_Enhanced.csv      # Full enriched dataset
│   ├── SCRPA_7Day_With_LagFlags.csv       # Filtered: IsCurrent7DayCycle=TRUE
│   ├── SCRPA_7Day_Lag_Only.csv            # Filtered: Backfill_7Day=TRUE
│   ├── SCRPA_7Day_Summary.yaml            # Lag day metadata
│   └── SCRPA_7Day_Summary.json
├── Documentation/
│   ├── data_dictionary.yaml               # Field definitions
│   ├── data_dictionary.json
│   ├── PROJECT_SUMMARY.yaml               # This file
│   ├── PROJECT_SUMMARY.json
│   ├── claude.md                          # System specification
│   ├── SCRPA_Report_Summary.md            # Report summary template
│   └── EMAIL_TEMPLATE.txt                 # Email for report distribution
└── Reports/
    └── (Power BI exports, PDFs, etc.)
'''
        },
        'critical_logic': {
            'cycle_resolution': {
                'description': '3-tier lookup to find the current reporting cycle',
                'tiers': [
                    'Tier 1: Exact Report_Due_Date match (for report day)',
                    'Tier 2: Date within 7-Day window (for mid-cycle)',
                    'Tier 3: Most recent cycle where 7_Day_End <= date'
                ],
                'm_code_lines': '191-224'
            },
            'lagdays_calculation': {
                'description': 'Days between incident and cycle start',
                'formula': 'LagDays = CycleStart_7Day - Incident_Date',
                'critical_note': 'Uses CycleStart from Report_Date_ForLagday resolution, NOT Report_Date - Incident_Date',
                'm_code_lines': '400-439'
            },
            'report_date_for_lagday': {
                'description': 'Date used for lag day cycle resolution',
                'formula': 'Coalesce(Report Date, EntryDate)',
                'critical_note': 'NO Incident_Date fallback - ensures correct lag day detection',
                'm_code_lines': '156-168'
            },
            'period_classification': {
                'description': 'Classify incident into reporting period',
                'based_on': 'Incident_Date (NOT Report_Date)',
                'priority': '7-Day > Prior Year > 28-Day > YTD > Historical',
                'critical_note': 'Prior Year checked before 28-Day to prevent misclassification',
                'm_code_lines': '242-273'
            },
            'backfill_7day': {
                'description': 'Flag for late-reported incidents',
                'condition': 'Incident_Date < CycleStart AND Report_Date_ForLagday IN [CycleStart, CycleEnd]',
                'm_code_lines': '328-336'
            }
        },
        'bi_weekly_reporting': {
            'description': 'Bi-weekly email and report period calculation',
            'examples': {
                '26BW01': {
                    'report_due': '01/13/2026',
                    '7_day_window': '01/06/2026 - 01/12/2026',
                    'bi_weekly_period': '12/30/2025 - 01/12/2026'
                },
                '26BW02': {
                    'report_due': '01/27/2026',
                    '7_day_window': '01/20/2026 - 01/26/2026',
                    'bi_weekly_period': '01/13/2026 - 01/26/2026'
                }
            },
            'formula': 'Bi-weekly period = (7_Day_Start - 7 days) to 7_Day_End'
        }
    }


# =============================================================================
# CLAUDE.MD SYSTEM SPECIFICATION
# =============================================================================

CLAUDE_MD_CONTENT = '''# SCRPA Crime Reporting System - Claude AI Specification

## System Overview

The Strategic Crime Reduction Plan Analysis (SCRPA) system processes crime incident data from the Hackensack Police Department Records Management System (RMS) into structured reports for bi-weekly executive briefings.

**Architecture**: Python-First Processing
- All data transformations occur in Python (`scripts/scrpa_transform.py`)
- Power BI imports pre-processed CSV files (no complex M code)
- Bi-weekly reporting cycles with 7-day and 28-day analysis windows

## Critical Logic Rules

### 1. Cycle Resolution (3-Tier Lookup)

When determining the current reporting cycle:
1. **Tier 1**: Exact match on Report_Due_Date (most accurate)
2. **Tier 2**: Date falls within a 7-Day cycle window
3. **Tier 3**: Most recent cycle where 7_Day_End <= date

```python
def resolve_cycle(calendar_df, report_due_date):
    # Tier 1: Exact Report_Due_Date match
    match1 = calendar_df[calendar_df['Report_Due_Date'] == report_due_date]
    if len(match1) > 0:
        return match1.iloc[0]

    # Tier 2: Date within 7-Day window
    match2 = calendar_df[
        (calendar_df['7_Day_Start'] <= report_due_date) &
        (report_due_date <= calendar_df['7_Day_End'])
    ]
    if len(match2) > 0:
        return match2.iloc[0]

    # Tier 3: Most recent cycle
    eligible = calendar_df[calendar_df['7_Day_End'] <= report_due_date]
    return eligible.sort_values('7_Day_End').iloc[-1]
```

### 2. LagDays Calculation

**CRITICAL**: LagDays = CycleStart_7Day - Incident_Date

This is NOT `Report_Date - Incident_Date`. The LagDays represents how many days before the cycle start the incident occurred.

For each incident:
1. Find the cycle containing `Report_Date_ForLagday` (using 3-tier lookup)
2. Get that cycle's `7_Day_Start`
3. Calculate: `LagDays = 7_Day_Start - Incident_Date`

### 3. Report_Date_ForLagday

**CRITICAL**: Only uses Report_Date or EntryDate (NO Incident_Date fallback)

```python
Report_Date_ForLagday = Coalesce(Report_Date, EntryDate)
```

When both are null, lag logic correctly yields `IsLagDay=False` and `LagDays=0`.

### 4. Period Classification

Based on **Incident_Date** (not Report_Date), with this priority:
1. **7-Day**: Incident within current 7-day cycle window
2. **Prior Year**: Incident in previous calendar year (e.g., 2025 when current year is 2026)
3. **28-Day**: Incident within current 28-day window (current year only)
4. **YTD**: Incident in current year, outside 7/28-Day windows
5. **Historical**: Older incidents (2024 and earlier)

**Important**: Prior Year is checked BEFORE 28-Day to prevent 2025 incidents from appearing in 28-Day period.

### 5. Backfill_7Day Flag

Identifies late-reported incidents:
```python
Backfill_7Day = (
    Incident_Date < CycleStart_7Day AND
    Report_Date_ForLagday >= CycleStart_7Day AND
    Report_Date_ForLagday <= CycleEnd_7Day
)
```

## Key Data Files

| File | Purpose |
|------|---------|
| `SCRPA_All_Crimes_Enhanced.csv` | Full enriched dataset |
| `SCRPA_7Day_With_LagFlags.csv` | IsCurrent7DayCycle=TRUE filter |
| `SCRPA_7Day_Lag_Only.csv` | Backfill_7Day=TRUE only |
| `SCRPA_7Day_Summary.yaml/json` | Lag day statistics |
| `EMAIL_TEMPLATE.txt` | Bi-weekly report email |

## Bi-Weekly Reporting

For bi-weekly cycles, the reporting period spans two 7-day windows:

| Cycle | Report Due | 7-Day Window | Bi-Weekly Period |
|-------|------------|--------------|------------------|
| 26BW01 | 01/13/2026 | 01/06 - 01/12 | 12/30/2025 - 01/12/2026 |
| 26BW02 | 01/27/2026 | 01/20 - 01/26 | 01/13/2026 - 01/26/2026 |

Formula: `Bi-Weekly Period = (7_Day_Start - 7 days) to 7_Day_End`

## Script Execution Order

```bash
# 1. Transform raw data
python scripts/scrpa_transform.py input.csv -o Data/SCRPA_All_Crimes_Enhanced.csv

# 2. Generate 7-day outputs
python scripts/prepare_7day_outputs.py Data/SCRPA_All_Crimes_Enhanced.csv -o Data/

# 3. Generate documentation
python scripts/generate_documentation.py -o Documentation/

# 4. Validate against reference
python scripts/validate_parity.py Data/SCRPA_All_Crimes_Enhanced.csv reference.csv

# Or run entire pipeline:
python scripts/run_scrpa_pipeline.py input.csv --report-date 01/27/2026
```

## Validation Checks

When validating Python output against M code reference:
1. Row count must match
2. All columns must be present
3. LagDays: Verify `(CycleStart_7Day - Incident_Date).days == LagDays`
4. Period: Compare values row-by-row
5. Backfill_7Day: All TRUE values must have IsLagDay=TRUE
'''


# =============================================================================
# REPORT SUMMARY TEMPLATE
# =============================================================================

def get_report_summary_template(cycle_info: Optional[Dict] = None) -> str:
    """Generate SCRPA_Report_Summary.md template."""
    cycle_name = cycle_info.get('name', '[CYCLE_NAME]') if cycle_info else '[CYCLE_NAME]'
    biweekly = cycle_info.get('biweekly', '') if cycle_info else ''
    start_7 = cycle_info.get('start_7', '[START_DATE]') if cycle_info else '[START_DATE]'
    end_7 = cycle_info.get('end_7', '[END_DATE]') if cycle_info else '[END_DATE]'
    start_bw = cycle_info.get('start_bw', start_7) if cycle_info else '[START_DATE]'
    end_bw = cycle_info.get('end_bw', end_7) if cycle_info else '[END_DATE]'
    report_due = cycle_info.get('report_due', '[REPORT_DUE]') if cycle_info else '[REPORT_DUE]'

    return f'''# SCRPA Report Summary - {cycle_name}

## Cycle Information

| Field | Value |
|-------|-------|
| Cycle Name | {cycle_name} |
| Bi-Weekly Cycle | {biweekly or 'N/A'} |
| Report Due Date | {report_due} |
| 7-Day Window | {start_7} - {end_7} |
| Bi-Weekly Period | {start_bw} - {end_bw} |

## Data Summary

*To be populated after data processing*

| Metric | Count |
|--------|-------|
| Total Incidents | - |
| 7-Day Period | - |
| 28-Day Period | - |
| YTD | - |
| Prior Year | - |
| Lag Incidents | - |
| Backfill 7-Day | - |

## Crime Category Breakdown

*To be populated after data processing*

| Category | 7-Day | 28-Day | YTD |
|----------|-------|--------|-----|
| Motor Vehicle Theft | - | - | - |
| Burglary Auto | - | - | - |
| Burglary - Comm & Res | - | - | - |
| Robbery | - | - | - |
| Sexual Offenses | - | - | - |
| Other | - | - | - |

## Lag Day Analysis

*To be populated after data processing*

- Mean Lag Days: -
- Median Lag Days: -
- Max Lag Days: -

## Notes

- Generated by: `scripts/generate_documentation.py`
- Data Source: SCRPA_All_Crimes_Enhanced.csv
- Report Period: Bi-weekly ({start_bw} - {end_bw})
'''


# =============================================================================
# MAIN GENERATION FUNCTIONS
# =============================================================================

def create_data_dictionary(output_dir: Path, format_types: List[str] = ['yaml', 'json']) -> List[Path]:
    """
    Generate data_dictionary files.

    Args:
        output_dir: Output directory path
        format_types: List of formats to generate ('yaml', 'json')

    Returns:
        List of created file paths
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    data_dict = DATA_DICTIONARY.copy()
    data_dict['metadata']['last_updated'] = datetime.now().isoformat()

    created = []

    if 'yaml' in format_types:
        yaml_path = output_dir / 'data_dictionary.yaml'
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data_dict, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        created.append(yaml_path)
        print(f"  Created: {yaml_path.name}")

    if 'json' in format_types:
        json_path = output_dir / 'data_dictionary.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
        created.append(json_path)
        print(f"  Created: {json_path.name}")

    return created


def create_project_summary(
    output_dir: Path,
    cycle_info: Optional[Dict] = None,
    format_types: List[str] = ['yaml', 'json']
) -> List[Path]:
    """
    Generate PROJECT_SUMMARY files.

    Args:
        output_dir: Output directory path
        cycle_info: Optional cycle information dict
        format_types: List of formats to generate ('yaml', 'json')

    Returns:
        List of created file paths
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = get_project_summary(cycle_info)
    summary['metadata']['last_updated'] = datetime.now().isoformat()

    created = []

    if 'yaml' in format_types:
        yaml_path = output_dir / 'PROJECT_SUMMARY.yaml'
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(summary, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        created.append(yaml_path)
        print(f"  Created: {yaml_path.name}")

    if 'json' in format_types:
        json_path = output_dir / 'PROJECT_SUMMARY.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        created.append(json_path)
        print(f"  Created: {json_path.name}")

    return created


def create_system_spec(output_dir: Path) -> Path:
    """
    Generate claude.md system specification.

    Args:
        output_dir: Output directory path

    Returns:
        Created file path
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / 'claude.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(CLAUDE_MD_CONTENT)

    print(f"  Created: {md_path.name}")
    return md_path


def create_report_summary(output_dir: Path, cycle_info: Optional[Dict] = None) -> Path:
    """
    Generate SCRPA_Report_Summary.md template.

    Args:
        output_dir: Output directory path
        cycle_info: Optional cycle information dict

    Returns:
        Created file path
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    content = get_report_summary_template(cycle_info)

    md_path = output_dir / 'SCRPA_Report_Summary.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Created: {md_path.name}")
    return md_path


def get_report_summary_with_data(
    cycle_info: Optional[Dict],
    summary_data: Optional[Dict[str, Any]] = None
) -> str:
    """
    Build SCRPA_Report_Summary.md content with real counts when summary_data is provided.

    Args:
        cycle_info: Cycle information dict (name, biweekly, start_7, end_7, etc.)
        summary_data: Optional dict with total, period_7, period_28, ytd, prior_year,
            lag_count, backfill_count, lag_mean, lag_median, lag_max, 7day_by_crime_category (list of dicts)

    Returns:
        Markdown string for SCRPA_Report_Summary.md
    """
    cycle_name = cycle_info.get('name', '[CYCLE_NAME]') if cycle_info else '[CYCLE_NAME]'
    biweekly = cycle_info.get('biweekly', '') if cycle_info else ''
    start_7 = cycle_info.get('start_7', '[START_DATE]') if cycle_info else '[START_DATE]'
    end_7 = cycle_info.get('end_7', '[END_DATE]') if cycle_info else '[END_DATE]'
    start_bw = cycle_info.get('start_bw', start_7) if cycle_info else '[START_DATE]'
    end_bw = cycle_info.get('end_bw', end_7) if cycle_info else '[END_DATE]'
    report_due = cycle_info.get('report_due', '[REPORT_DUE]') if cycle_info else '[REPORT_DUE]'

    total = summary_data.get('total', '-') if summary_data else '-'
    period_7 = summary_data.get('period_7', '-') if summary_data else '-'
    period_28 = summary_data.get('period_28', '-') if summary_data else '-'
    ytd = summary_data.get('ytd', '-') if summary_data else '-'
    prior_year = summary_data.get('prior_year', '-') if summary_data else '-'
    lag_count = summary_data.get('lag_count', '-') if summary_data else '-'
    backfill_count = summary_data.get('backfill_count', '-') if summary_data else '-'
    lag_mean = summary_data.get('lag_mean', '-') if summary_data else '-'
    lag_median = summary_data.get('lag_median', '-') if summary_data else '-'
    lag_max = summary_data.get('lag_max', '-') if summary_data else '-'

    rows_7day = []
    if summary_data and summary_data.get('7day_by_crime_category'):
        for row in summary_data['7day_by_crime_category']:
            cat = row.get('Crime_Category', '')
            lag = row.get('LagDayCount', 0)
            tot = row.get('TotalCount', 0)
            rows_7day.append(f"| {cat} | {lag} | {tot} |")
    if not rows_7day:
        rows_7day = ["| (no 7-day breakdown) | - | - |"]

    table_7day = "\n".join(rows_7day)

    return f'''# SCRPA Report Summary - {cycle_name}

## Cycle Information

| Field | Value |
|-------|-------|
| Cycle Name | {cycle_name} |
| Bi-Weekly Cycle | {biweekly or 'N/A'} |
| Report Due Date | {report_due} |
| 7-Day Window | {start_7} - {end_7} |
| Bi-Weekly Period | {start_bw} - {end_bw} |

## Data Summary

| Metric | Count |
|--------|-------|
| Total Incidents | {total} |
| 7-Day Period | {period_7} |
| 28-Day Period | {period_28} |
| YTD | {ytd} |
| Prior Year | {prior_year} |
| Lag Incidents | {lag_count} |
| Backfill 7-Day | {backfill_count} |

## 7-Day by Crime Category

| Category | LagDayCount | TotalCount |
|----------|-------------|------------|
{table_7day}

## Lag Day Analysis

- Mean Lag Days: {lag_mean}
- Median Lag Days: {lag_median}
- Max Lag Days: {lag_max}

## Notes

- Generated by: `scripts/run_scrpa_pipeline.py` (cycle documentation)
- Data Source: SCRPA_All_Crimes_Enhanced.csv
- Report Period: Bi-weekly ({start_bw} - {end_bw})
'''


def write_report_summary_with_data(
    output_dir: Path,
    cycle_info: Optional[Dict],
    summary_data: Optional[Dict[str, Any]] = None
) -> Path:
    """
    Write SCRPA_Report_Summary.md with real data when summary_data is provided.

    Args:
        output_dir: Documentation folder path
        cycle_info: Cycle information dict
        summary_data: Optional dict from pipeline (total, period_7, 7day_by_crime_category, etc.)

    Returns:
        Path to created file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    content = get_report_summary_with_data(cycle_info, summary_data)
    md_path = output_dir / 'SCRPA_Report_Summary.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created: {md_path.name}")
    return md_path


# Placeholders for CHATGPT_BRIEFING_PROMPT.md: CYCLE_ID, DATE_RANGE, REPORT_DUE, BIWEEKLY, 7_DAY_WINDOW
CHATGPT_BRIEFING_TEMPLATE = """# SCRPA ChatGPT Briefing Prompt - {cycle_id}

Use this prompt with ChatGPT (or similar) for the Strategic Crime Reduction briefing. Copy the entire content below and paste into the chat; attach or paste the 7-day CSV from this cycle's Data folder if needed.

## Reporting Parameters

| Field | Value |
|-------|-------|
| Cycle | {cycle_id} |
| Bi-Weekly | {biweekly} |
| Report Due | {report_due} |
| 7-Day Window | {date_range_7} |
| Bi-Weekly Period | {date_range_bw} |

## Instructions

1. Use the attached/pasted SCRPA 7-day data for this cycle.
2. Summarize key incidents by category (Burglary - Auto, Motor Vehicle Theft, Robbery, Sexual Offenses, Burglary - Commercial, Burglary - Residence).
3. Insert the date range from the Reporting Parameters in any generated output (MM/DD/YYYY - MM/DD/YYYY).
4. Footer for generated content: **HPD | SSOCC | SCRPA Report | Cycle: {cycle_id}**

---
Generated by SCRPA pipeline for cycle {cycle_id}. Report due: {report_due}.
"""


def write_chatgpt_briefing_prompt(output_dir: Path, cycle_info: Optional[Dict]) -> Path:
    """
    Write CHATGPT_BRIEFING_PROMPT.md with cycle placeholders filled.

    Args:
        output_dir: Documentation folder path
        cycle_info: Cycle information dict (name, biweekly, start_7, end_7, start_bw, end_bw, report_due)

    Returns:
        Path to created file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if not cycle_info:
        cycle_id = "[CYCLE_ID]"
        biweekly = "[BIWEEKLY]"
        report_due = "[REPORT_DUE]"
        date_range_7 = "[START] - [END]"
        date_range_bw = "[START] - [END]"
    else:
        cycle_id = cycle_info.get('name', '[CYCLE_ID]')
        biweekly = cycle_info.get('biweekly', 'N/A')
        report_due = cycle_info.get('report_due', '[REPORT_DUE]')
        start_7 = cycle_info.get('start_7', '[START]')
        end_7 = cycle_info.get('end_7', '[END]')
        date_range_7 = f"{start_7} - {end_7}"
        start_bw = cycle_info.get('start_bw', start_7)
        end_bw = cycle_info.get('end_bw', end_7)
        date_range_bw = f"{start_bw} - {end_bw}"
    content = CHATGPT_BRIEFING_TEMPLATE.format(
        cycle_id=cycle_id,
        biweekly=biweekly,
        report_due=report_due,
        date_range_7=date_range_7,
        date_range_bw=date_range_bw
    )
    md_path = output_dir / 'CHATGPT_BRIEFING_PROMPT.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created: {md_path.name}")
    return md_path


def generate_all_documentation(
    output_dir: Path,
    cycle_info: Optional[Dict] = None
) -> Dict[str, List[Path]]:
    """
    Generate all documentation files (canonical: data_dictionary, PROJECT_SUMMARY, claude.md).
    Use for the single canonical Documentation folder (e.g. 16_Reports/SCRPA/Documentation), not per cycle.

    Args:
        output_dir: Output directory path
        cycle_info: Optional cycle information dict

    Returns:
        Dictionary mapping doc type to list of created paths
    """
    output_dir = Path(output_dir)
    print(f"Generating documentation to: {output_dir}")

    results = {
        'data_dictionary': create_data_dictionary(output_dir),
        'project_summary': create_project_summary(output_dir, cycle_info),
        'claude_md': [create_system_spec(output_dir)],
        'report_summary': [create_report_summary(output_dir, cycle_info)]
    }

    total = sum(len(v) for v in results.values())
    print(f"\nGenerated {total} documentation files")

    return results


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """Command-line interface for generate_documentation."""
    parser = argparse.ArgumentParser(
        description='SCRPA Documentation Generator'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='Output directory (default: ./Documentation)',
        default='./Documentation'
    )
    parser.add_argument(
        '--cycle-name',
        help='Cycle name (e.g., 26C01W04)',
        default=None
    )
    parser.add_argument(
        '--biweekly',
        help='Bi-weekly cycle name (e.g., 26BW02)',
        default=None
    )
    parser.add_argument(
        '--start-7',
        help='7-Day start date (MM/DD/YYYY)',
        default=None
    )
    parser.add_argument(
        '--end-7',
        help='7-Day end date (MM/DD/YYYY)',
        default=None
    )
    parser.add_argument(
        '--report-due',
        help='Report due date (MM/DD/YYYY)',
        default=None
    )

    args = parser.parse_args()

    # Build cycle info if provided
    cycle_info = None
    if any([args.cycle_name, args.biweekly, args.start_7, args.end_7, args.report_due]):
        cycle_info = {
            'name': args.cycle_name,
            'biweekly': args.biweekly,
            'start_7': args.start_7,
            'end_7': args.end_7,
            'report_due': args.report_due
        }

        # Calculate bi-weekly period if we have 7-day dates
        if args.start_7 and args.end_7:
            try:
                start_dt = datetime.strptime(args.start_7, '%m/%d/%Y')
                end_dt = datetime.strptime(args.end_7, '%m/%d/%Y')
                start_bw = (start_dt - timedelta(days=7)).strftime('%m/%d/%Y')
                cycle_info['start_bw'] = start_bw
                cycle_info['end_bw'] = args.end_7
            except:
                pass

    generate_all_documentation(Path(args.output_dir), cycle_info)


if __name__ == '__main__':
    main()
