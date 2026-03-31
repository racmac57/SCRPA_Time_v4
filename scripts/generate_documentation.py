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
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
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
                '1. RMS Export (.xlsx) -> Raw crime incident data',
                '2. scrpa_transform.py -> SCRPA_All_Crimes_Enhanced.csv (cycle, lag days, period, etc.)',
                '3. prepare_7day_outputs.py -> SCRPA_7Day_With_LagFlags.csv + SCRPA_7Day_Summary.json',
                '4. generate_documentation.py -> SCRPA_Report_Summary.md, CHATGPT_BRIEFING_PROMPT.md, CHATGPT_SESSION_PROMPT.md, HPD_REPORT_STYLE_BLOCK.md, EMAIL_TEMPLATE.txt',
                '5. SCRPA_ArcPy HTML generator -> SCRPA_Combined_Executive_Summary.html',
                '6. Power BI (All_Crimes_Simple.m) -> Simple CSV import, no transformations',
                '7. [Manual] ChatGPT: paste CHATGPT_SESSION_PROMPT.md, attach briefing + summary + HPD_REPORT_STYLE_BLOCK.md -> 7Day tactical briefing HTML',
                '8. [Optional] clean_chatgpt_html.py -> strip ChatGPT code-fence artifacts from HTML output'
            ],
            'diagram': '''
RMS Export (.xlsx)
    |
    v
[scrpa_transform.py] -----> SCRPA_All_Crimes_Enhanced.csv
    |
    v
[prepare_7day_outputs.py] --> SCRPA_7Day_With_LagFlags.csv
    |                         SCRPA_7Day_Summary.json
    v
[generate_documentation.py] -> SCRPA_Report_Summary.md
    |                          CHATGPT_BRIEFING_PROMPT.md
    |                          CHATGPT_SESSION_PROMPT.md  <- paste into ChatGPT
    |                          HPD_REPORT_STYLE_BLOCK.md  <- attach (START–END CSS)
    |                          EMAIL_TEMPLATE.txt
    |                          PROJECT_SUMMARY.yaml/json
    v
[SCRPA_ArcPy HTML generator] -> SCRPA_Combined_Executive_Summary.html
    |
    v
[Power BI - All_Crimes_Simple.m] --> Import CSVs (no transforms)

ChatGPT 7-Day Briefing workflow (manual, each cycle):
  1. Paste CHATGPT_SESSION_PROMPT.md into ChatGPT project chat (or attach it)
  2. Attach CHATGPT_BRIEFING_PROMPT.md + SCRPA_Report_Summary.md + HPD_REPORT_STYLE_BLOCK.md
  3. Save HTML output to Reports/
  4. Run Clean_ChatGPT_HTML.bat to strip any code-fence artifacts

Canonical docs (Documentation/ folder):
  data_dictionary.yaml/json, PROJECT_SUMMARY.yaml/json, claude.md
  -> Regenerate with: python scripts/generate_documentation.py -o Documentation/
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
                    'SCRPA_7Day_Summary.json'
                ],
                'notes': [
                    'SCRPA_7Day_Lag_Only.csv no longer generated (backfill rows in With_LagFlags)',
                    'SCRPA_7Day_Summary.yaml no longer generated (JSON only)'
                ],
                'key_functions': [
                    'filter_7day_by_report_date() - IsCurrent7DayCycle filter',
                    'extract_backfill_lag() - Backfill_7Day filter (internal, not saved separately)',
                    'generate_lagday_summary() - Metadata generation'
                ],
                'dependencies': ['pandas']
            },
            'generate_documentation.py': {
                'purpose': 'Generate structured documentation (canonical and per-cycle)',
                'inputs': ['Cycle info', 'System constants'],
                'outputs': [
                    'data_dictionary.yaml/json (canonical only)',
                    'PROJECT_SUMMARY.yaml/json (canonical only)',
                    'claude.md (canonical only)',
                    'SCRPA_Report_Summary.md (per-cycle, populated with real counts)',
                    'CHATGPT_BRIEFING_PROMPT.md (per-cycle, with 7-day narratives)',
                    'CHATGPT_SESSION_PROMPT.md (per-cycle, paste-and-go ChatGPT prompt)',
                    'HPD_REPORT_STYLE_BLOCK.md (per-cycle, START–END excerpt for ChatGPT)',
                    'EMAIL_TEMPLATE.txt (per-cycle, ready-to-send email)'
                ],
                'dependencies': ['pyyaml']
            },
            'run_scrpa_pipeline.py': {
                'purpose': 'Main orchestration script',
                'inputs': ['RMS Export path (.xlsx)', 'Report due date (MM/DD/YYYY)'],
                'outputs': ['All generated files in structured folders'],
                'workflow': [
                    '1. Load RMS export + cycle calendar; resolve cycle',
                    '2. Create output directory; copy Power BI template',
                    '3. Run scrpa_transform -> SCRPA_All_Crimes_Enhanced.csv',
                    '4. Run prepare_7day_outputs -> SCRPA_7Day_With_LagFlags.csv + SCRPA_7Day_Summary.json',
                    '5. Write cycle docs (SCRPA_Report_Summary.md, HPD_REPORT_STYLE_BLOCK.md, CHATGPT_BRIEFING_PROMPT.md, CHATGPT_SESSION_PROMPT.md, EMAIL_TEMPLATE.txt)',
                    '6. Generate HTML report via SCRPA_ArcPy; copy to Reports/'
                ],
                'entry_point': 'Run_SCRPA_Pipeline.bat (auto-selects latest RMS .xlsx)'
            },
            'clean_chatgpt_html.py': {
                'purpose': 'Remove ChatGPT formatting artifacts from HTML output files',
                'inputs': ['HTML file or folder path'],
                'outputs': ['Cleaned HTML file(s) in place'],
                'artifacts_removed': [
                    'Leading ```html or ``` code fences',
                    'Trailing ``` code fences (wherever they appear in the body)',
                    'Inline ``` occurrences inside HTML',
                    'ChatGPT citation comments (<!-- :contentReference[...] -->)'
                ],
                'entry_point': 'Clean_ChatGPT_HTML.bat (drag-and-drop or double-click)'
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
├── {CYCLE_NAME}_{YY_MM_DD}.pbix           # Power BI template (copied)
├── Data/
│   ├── SCRPA_All_Crimes_Enhanced.csv      # Full enriched dataset
│   ├── SCRPA_7Day_With_LagFlags.csv       # IsCurrent7DayCycle=TRUE (includes backfill)
│   └── SCRPA_7Day_Summary.json            # Lag day statistics + period counts
├── Documentation/
│   ├── SCRPA_Report_Summary.md            # Cycle summary with real counts
│   ├── CHATGPT_BRIEFING_PROMPT.md         # Attach to ChatGPT (narratives + params)
│   ├── CHATGPT_SESSION_PROMPT.md          # Paste into ChatGPT chat (the prompt)
│   ├── HPD_REPORT_STYLE_BLOCK.md          # Attach — START–END HPD CSS/skeleton
│   ├── EMAIL_TEMPLATE.txt                 # Ready-to-send email
│   ├── PROJECT_SUMMARY.json               # Project overview (canonical copy)
│   └── PROJECT_SUMMARY.yaml
└── Reports/
    ├── SCRPA_Combined_Executive_Summary.html  # Auto-generated by ArcPy
    ├── SCRPA_Combined_Executive_Summary.html.bak
    └── [CYCLE]_scrpa_tac.html             # ChatGPT 7-day tactical briefing

Canonical docs (16_Reports/SCRPA/Documentation/):
    data_dictionary.yaml/json, PROJECT_SUMMARY.yaml/json, claude.md
    -> These are NOT copied per-cycle; regenerate with generate_documentation.py
'''
        },
        'critical_logic': {
            'cycle_resolution': {
                'description': '3-tier lookup to find the current reporting cycle',
                'tiers': [
                    'Tier 1: Exact Report_Due_Date match (for report day)',
                    'Tier 2: Date falls within a 7-Day window',
                    'Tier 3: Most recent cycle where 7_Day_End <= date'
                ],
                'python_function': 'scrpa_transform.resolve_cycle()'
            },
            'lagdays_calculation': {
                'description': 'Days between incident and cycle start',
                'formula': 'LagDays = CycleStart_7Day - Incident_Date',
                'critical_note': 'Uses CycleStart from Report_Date_ForLagday resolution, NOT Report_Date - Incident_Date',
                'python_function': 'scrpa_transform.calculate_lag_days()'
            },
            'report_date_for_lagday': {
                'description': 'Date used for lag day cycle resolution',
                'formula': 'Coalesce(Report Date, EntryDate)',
                'critical_note': 'NO Incident_Date fallback - ensures correct lag day detection',
                'python_function': 'scrpa_transform.build_all_crimes_enhanced()'
            },
            'period_classification': {
                'description': 'Classify incident into reporting period',
                'based_on': 'Incident_Date (NOT Report_Date)',
                'priority': '7-Day > Prior Year > 28-Day > YTD > Historical',
                'critical_note': 'Prior Year checked before 28-Day to prevent 2025 incidents appearing in 28-Day',
                'python_function': 'scrpa_transform.classify_period()'
            },
            'backfill_7day': {
                'description': 'Flag for late-reported incidents (incident before cycle, report during cycle)',
                'condition': 'Incident_Date < CycleStart AND Report_Date_ForLagday IN [CycleStart, CycleEnd]',
                'python_function': 'scrpa_transform.build_all_crimes_enhanced()'
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
                },
                '26BW03': {
                    'report_due': '02/10/2026',
                    '7_day_window': '02/03/2026 - 02/09/2026',
                    'bi_weekly_period': '01/27/2026 - 02/09/2026'
                },
                '26BW04': {
                    'report_due': '02/24/2026',
                    '7_day_window': '02/17/2026 - 02/23/2026',
                    'bi_weekly_period': '02/10/2026 - 02/23/2026'
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

**HTML:** ArcPy combined reports use `08_Templates/Themes/HTML/scrpa_html.md`. ChatGPT tactical briefings use per-cycle **`HPD_REPORT_STYLE_BLOCK.md`** (START–END excerpt) or the full **`08_Templates/Report_Styles/html/HPD_Report_Style_Prompt.md`** as attachment **#4**.

**PDF / print (tactical HTML):** After Lag Day, **close** `<div class="content">`. Wrap **7-Day Incident Highlights** (`h2` + **`table.incident-highlights`**) and the **`.footer`** in `<div class="report-tail">` (optional **`report-tail-landscape`** for landscape). The **`.footer` must stay inside** that same `div` so browser PDF does not place the footer alone on the next portrait page. Full CSS (`@page`, `.report-tail`, `table.incident-highlights`) comes from the style file above.

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
| `SCRPA_7Day_With_LagFlags.csv` | IsCurrent7DayCycle=TRUE filter (includes backfill rows) |
| `SCRPA_7Day_Summary.json` | Lag day statistics and period counts |
| `EMAIL_TEMPLATE.txt` | Bi-weekly report email (ready to send) |
| `CHATGPT_BRIEFING_PROMPT.md` | **Attach** to ChatGPT — cycle params + 7-day narratives |
| `CHATGPT_SESSION_PROMPT.md` | **Paste** into ChatGPT chat — the per-cycle prompt |
| `SCRPA_Report_Summary.md` | **Attach** to ChatGPT — authoritative counts + category table |
| `HPD_REPORT_STYLE_BLOCK.md` | **Attach** — START–END excerpt from `HPD_Report_Style_Prompt.md` |

> Note: `SCRPA_7Day_Lag_Only.csv` and `SCRPA_7Day_Summary.yaml` are no longer generated.
> Backfill rows are included in `SCRPA_7Day_With_LagFlags.csv` (Backfill_7Day=TRUE).

## ChatGPT 7-Day Tactical Briefing Workflow

Each cycle, after the pipeline runs:
1. Open a new chat in the SCRPA ChatGPT project
2. Copy all text from `CHATGPT_SESSION_PROMPT.md` → paste into the chat (or attach it)
3. Attach `CHATGPT_BRIEFING_PROMPT.md`, `SCRPA_Report_Summary.md`, and **one** style file: `HPD_REPORT_STYLE_BLOCK.md` (recommended) **or** full `HPD_Report_Style_Prompt.md` — whichever is attachment **#4**, per `CHATGPT_SESSION_PROMPT.md`
4. Send — ChatGPT generates the HTML tactical briefing
5. Save output as `[CYCLE]_scrpa_tac.html` in `Reports/`
6. Run `Clean_ChatGPT_HTML.bat` on the file to remove any ``` artifacts

## clean_chatgpt_html.py / Clean_ChatGPT_HTML.bat

Removes ChatGPT formatting artifacts from saved HTML files:
- Leading/trailing ` ``` ` or ` ```html ` code fences
- Inline ` ``` ` occurrences inside the HTML body
- ChatGPT citation comments (`<!-- :contentReference[...] -->`)

Usage: drag any `.html` file onto `Clean_ChatGPT_HTML.bat`, or double-click
to scan all HTML files in the `Time_Based/` folder.

## Lag Incident Counts — Two Scopes

The pipeline reports lag counts in two scopes; both are correct:

| Scope | Location | Meaning |
|-------|----------|---------|
| Pipeline console "Lag incidents: N" | Run summary | All IsLagDay=TRUE rows across the full dataset |
| SCRPA_Report_Summary.md "Lag Incidents: N" | Cycle docs | Lag rows within the 7-day window only |

## Bi-Weekly Reporting

For bi-weekly cycles, the reporting period spans two 7-day windows:

| Cycle | Report Due | 7-Day Window | Bi-Weekly Period |
|-------|------------|--------------|------------------|
| 26BW01 | 01/13/2026 | 01/06 - 01/12 | 12/30/2025 - 01/12/2026 |
| 26BW02 | 01/27/2026 | 01/20 - 01/26 | 01/13/2026 - 01/26/2026 |
| 26BW03 | 02/10/2026 | 02/03 - 02/09 | 01/27/2026 - 02/09/2026 |
| 26BW04 | 02/24/2026 | 02/17 - 02/23 | 02/10/2026 - 02/23/2026 |

Formula: `Bi-Weekly Period = (7_Day_Start - 7 days) to 7_Day_End`

## Script Execution Order

```bash
# Run entire pipeline (recommended):
python scripts/run_scrpa_pipeline.py input.xlsx --report-date 02/24/2026

# Or run steps individually:
# 1. Transform raw data
python scripts/scrpa_transform.py input.xlsx -o Data/SCRPA_All_Crimes_Enhanced.csv

# 2. Generate 7-day outputs
python scripts/prepare_7day_outputs.py Data/SCRPA_All_Crimes_Enhanced.csv -o Data/

# 3. Generate cycle documentation (per-cycle, called by pipeline)
python scripts/generate_documentation.py -o Documentation/

# 4. Regenerate canonical docs (run from SCRPA root when docs change)
python scripts/generate_documentation.py -o Documentation/
```

## Validation Checks

When validating Python output:
1. Row count must match expected (check SCRPA_Report_Summary.md Data Summary)
2. Period sum (7-Day + 28-Day + YTD + Prior Year) must equal Total Incidents
3. LagDays: Verify `(CycleStart_7Day - Incident_Date).days == LagDays`
4. Backfill_7Day=TRUE rows must also have IsLagDay=TRUE
5. All IsCurrent7DayCycle=TRUE rows appear in SCRPA_7Day_With_LagFlags.csv
'''


# =============================================================================
# HPD HTML REPORT STYLE (AI outputs — aligns with 08_Templates/Report_Styles)
# =============================================================================

HPD_REPORT_STYLE_PROMPT_PATH = (
    r"C:\Users\carucci_r\OneDrive - City of Hackensack\08_Templates\Report_Styles"
    r"\html\HPD_Report_Style_Prompt.md"
)

# Inserted into CHATGPT_* prompts; no brace characters (avoids str.format conflicts).
MARKDOWN_HPD_HTML_STYLE_FOR_AI = f"""## HPD HTML design system (mandatory when generating HTML)

**Full design system — paste the START–END block from this file into the AI (or follow it verbatim):**  
`{HPD_REPORT_STYLE_PROMPT_PATH}`

**Context:** `08_Templates\\Report_Styles\\README.md`, `Report_Styles\\CLAUDE.md`, `Report_Styles\\html\\README.md`

**Rules**
- **Self-contained HTML only** — all CSS in a `<style>` block in `<head>`; no external stylesheets, fonts, or scripts.
- **Palette:** Navy `#1a2744`, Gold `#c8a84b`, Dark green `#2e7d32`, Dark red `#b71c1c`; page background `#f5f5f0`, card `#ffffff`, meta bar `#eef0f5`, body text `#2c2c3e`.
- **Structure:** `.page` → `.header` → `.meta-bar` → `.content` (through Lag Day) → **close `.content`** → `.report-tail` with **7-Day Incident Highlights** + **`table.incident-highlights`** + **`.footer`** (see SCRPA closing note in the style prompt). Do not place `.footer` alone outside the same wrapper as a landscape highlights block.
- **Typography:** Segoe UI / Arial, 13.5px body; `h2` uppercase with gold underline.
- **Executive callouts:** **Key Findings** (not “Bottom Line”) — use `.alert` with `<span class="alert-icon">&#9654;</span> <strong>Key Findings:</strong>` per the prompt.
- **Prepared by:** R. A. Carucci #261, Principal Analyst | Safe Streets Operations Control Center | Hackensack Police Department.
- **Tables:** Navy header row, alternating rows; add `primary-crimes` / `table-notes` classes when needed; **incident highlights:** `class="incident-highlights"` (and `table-notes` if synopsis column is wide).
- **Print / PDF:** Include the full CSS from the style block (`@page`, `@page landscape`, `.report-tail`, `.report-tail-landscape`, `table.incident-highlights` split rules). Prefer keeping footer inside `.report-tail` with the highlights table.
"""


def _report_summary_hpd_note() -> str:
    """Single line for SCRPA_Report_Summary Notes (data-only file; points AI to HTML style)."""
    return (
        f"- **HTML tactical briefings:** Use the Hackensack PD design system in "
        f"`{HPD_REPORT_STYLE_PROMPT_PATH}` (self-contained HTML, Key Findings callout, "
        f"navy/gold palette, meta bar + footer pattern, `@media print`). "
        f"Same folder: `HPD_REPORT_STYLE_BLOCK.md` (START–END excerpt for ChatGPT)."
    )


# Per-cycle file: excerpt between markers in HPD_Report_Style_Prompt.md
HPD_REPORT_STYLE_BLOCK_FILENAME = "HPD_REPORT_STYLE_BLOCK.md"


def extract_hpd_style_block_markdown(source_path: Optional[Path] = None) -> Tuple[str, str]:
    """
    Extract markdown between START OF STYLE BLOCK and END OF STYLE BLOCK markers.

    Returns:
        (body, error_message). body is empty if error_message is non-empty.
    """
    src = Path(source_path or HPD_REPORT_STYLE_PROMPT_PATH)
    if not src.is_file():
        return "", f"Style source not found: {src}"
    lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
    start_idx: Optional[int] = None
    end_idx: Optional[int] = None
    for i, line in enumerate(lines):
        if start_idx is None and "START OF STYLE BLOCK" in line:
            start_idx = i + 1
            continue
        if "END OF STYLE BLOCK" in line:
            end_idx = i
            break
    if start_idx is None or end_idx is None or end_idx <= start_idx:
        return "", "Could not find START/END OF STYLE BLOCK markers in style prompt file."
    body = "\n".join(lines[start_idx:end_idx]).strip()
    return body, ""


def write_hpd_report_style_block(
    output_dir: Path, source_path: Optional[Path] = None
) -> Path:
    """
    Write HPD_REPORT_STYLE_BLOCK.md — START–END excerpt from HPD_Report_Style_Prompt.md
    for attaching to ChatGPT alongside session/briefing/summary.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    body, err = extract_hpd_style_block_markdown(source_path)
    header = f"""# HPD HTML style — START–END block

Pipeline copy for this cycle. Excerpt is between the markers in:

`{HPD_REPORT_STYLE_PROMPT_PATH}`

Attach with **CHATGPT_SESSION_PROMPT.md**, **CHATGPT_BRIEFING_PROMPT.md**, and **SCRPA_Report_Summary.md**.

---

"""
    if err:
        body = (
            f"**Could not extract style block:** {err}\n\n"
            f"Copy the START–END section manually from `{HPD_REPORT_STYLE_PROMPT_PATH}` "
            "or fix `HPD_REPORT_STYLE_PROMPT_PATH` in `scripts/generate_documentation.py`."
        )
    out_path = output_dir / HPD_REPORT_STYLE_BLOCK_FILENAME
    out_path.write_text(header + body + "\n", encoding="utf-8")
    print(f"  Created: {out_path.name}")
    return out_path


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
{_report_summary_hpd_note()}
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

    # Crime Category Breakdown table (7-Day | 28-Day | YTD) - matches 26C01W04 style
    category_rows = []
    if summary_data and summary_data.get('category_breakdown'):
        for row in summary_data['category_breakdown']:
            cat = row.get('Category', row.get('Crime_Category', ''))
            p7 = row.get('7-Day', row.get('period_7', '-'))
            p28 = row.get('28-Day', row.get('period_28', '-'))
            y = row.get('YTD', row.get('ytd', '-'))
            category_rows.append(f"| {cat} | {p7} | {p28} | {y} |")
    if not category_rows:
        # Fallback: use 7day_by_crime_category for 7-Day column only
        default_cats = ['Motor Vehicle Theft', 'Burglary Auto', 'Burglary - Comm & Res', 'Robbery', 'Sexual Offenses', 'Other']
        for cat in default_cats:
            category_rows.append(f"| {cat} | - | - | - |")
    table_category = "\n".join(category_rows)

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

## Crime Category Breakdown

| Category | 7-Day | 28-Day | YTD |
|----------|-------|--------|-----|
{table_category}

## Lag Day Analysis

- Mean Lag Days: {lag_mean}
- Median Lag Days: {lag_median}
- Max Lag Days: {lag_max}

## Notes

- Generated by: `scripts/generate_documentation.py`
- Data Source: SCRPA_All_Crimes_Enhanced.csv
- Report Period: Bi-weekly ({start_bw} - {end_bw})
{_report_summary_hpd_note()}
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

{hpd_html_style}

## Instructions

1. Use the attached/pasted SCRPA 7-day data for this cycle.
2. Summarize key incidents by category (Burglary - Auto, Motor Vehicle Theft, Robbery, Sexual Offenses, Burglary - Commercial, Burglary - Residence).
3. Insert the date range from the Reporting Parameters in any generated output (MM/DD/YYYY - MM/DD/YYYY).
4. For **HTML** output: follow **HPD HTML design system** above (`HPD_REPORT_STYLE_BLOCK.md` or full `HPD_Report_Style_Prompt.md`). For tactical PDF: close **.content** after Lag Day; wrap **7-Day Incident Highlights** + **`table.incident-highlights`** + **`.footer`** in **`.report-tail`** (optional **`.report-tail-landscape`**). For plain-text or email snippets, footer line: **HPD | SSOCC | SCRPA Report | Cycle: {cycle_id}**

---
Generated by SCRPA pipeline for cycle {cycle_id}. Report due: {report_due}.
"""


def write_chatgpt_briefing_prompt(
    output_dir: Path,
    cycle_info: Optional[Dict],
    seven_day_incidents: Optional[list] = None
) -> Path:
    """
    Write CHATGPT_BRIEFING_PROMPT.md with cycle placeholders filled.
    Optionally include 7-day incident narratives when seven_day_incidents is provided.

    Args:
        output_dir: Documentation folder path
        cycle_info: Cycle information dict (name, biweekly, start_7, end_7, start_bw, end_bw, report_due)
        seven_day_incidents: Optional list of dicts with Crime_Category, Incident_Date, Narrative

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
        date_range_bw=date_range_bw,
        hpd_html_style=MARKDOWN_HPD_HTML_STYLE_FOR_AI,
    )
    # Insert 7-day incident narratives section if provided
    if seven_day_incidents:
        narrative_section = "\n## 7-Day Incidents (this cycle)\n\nIncidents occurring in the 7-Day window with narrative for briefing use.\n\n"
        for i, inc in enumerate(seven_day_incidents, 1):
            cat = inc.get('Crime_Category', '')
            inc_date = inc.get('Incident_Date', '')
            narr = (inc.get('Narrative') or '').strip()[:2500]
            narrative_section += f"### {i}. {cat} | Incident Date: {inc_date}\n\n{narr}\n\n"
        # Insert after Reporting Parameters table, before Instructions
        content = content.replace(
            "## Instructions\n",
            narrative_section + "## Instructions\n"
        )
    md_path = output_dir / 'CHATGPT_BRIEFING_PROMPT.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created: {md_path.name}")
    return md_path


CHATGPT_SESSION_PROMPT_TEMPLATE = """\
SCRPA TACTICAL BRIEFING — CYCLE {cycle_id}

--- PASTE THIS USER MESSAGE FIRST (then attach the files listed under ATTACHED FILES) ---
SCRPA tactical briefing — Cycle **{cycle_id}**. I am attaching:
1. CHATGPT_SESSION_PROMPT.md — full task spec (same as this paste; attach if easier)
2. CHATGPT_BRIEFING_PROMPT.md — cycle parameters and 7-day incident narratives
3. SCRPA_Report_Summary.md — Data Summary counts and category table
4. **One** style file — either **HPD_REPORT_STYLE_BLOCK.md** (same Documentation folder; recommended) **or** the full **`HPD_Report_Style_Prompt.md`** from Templates (`{hpd_style_path}`). Whichever file is attachment **#4**, use it as the complete CSS + print rules source.

Deliverable: one self-contained HTML tactical briefing per TASK below. Copy the **FULL CSS BLOCK** from attachment (4) into `<style>` (including `@page` / `@page landscape` / `.report-tail` rules if present).
---

ATTACHED FILES (4 — same cycle Documentation folder for 1–3; for #4 use BLOCK **or** full prompt, not both unless you clarify)
  1. CHATGPT_SESSION_PROMPT.md — this file (paste or attach)
  2. CHATGPT_BRIEFING_PROMPT.md
  3. SCRPA_Report_Summary.md
  4. HPD_REPORT_STYLE_BLOCK.md **or** HPD_Report_Style_Prompt.md — must include updated print/PDF rules (incident-highlights + report-tail)

TASK
Generate a standalone HTML tactical briefing for the 7-day window defined in
CHATGPT_BRIEFING_PROMPT.md. This report is submitted to a police captain —
keep it concise, professional, and operationally focused.

HACKENSACK PD HTML DESIGN SYSTEM (mandatory)
  Primary source: attachment **#4** (HPD_REPORT_STYLE_BLOCK.md **or** full `{hpd_style_path}`) — copy the **entire** FULL CSS BLOCK and follow the SCRPA closing structure in that file.
  Non-negotiable:
    • Self-contained HTML only — all CSS in <style> in <head>; no external stylesheets, fonts, or scripts.
    • DOM order: .page → .header → .meta-bar → .content (Executive Summary through Lag Day only) → **close .content** → **.report-tail** (required) containing: h2 "7-Day Incident Highlights" + **table.incident-highlights** (add **table-notes** if synopsis column is wide) + **.footer** with the exact footer line from section 8 below.
    • **PDF / print:** The **.footer must not** sit outside the same wrapper as the incident highlights when using **landscape** for that section. Use **<div class="report-tail report-tail-landscape">** only if you use landscape; otherwise **<div class="report-tail">** (portrait). Footer stays **inside** .report-tail in both cases.
    • Palette and typography per that file (body #2c2c3e, page #f5f5f0, tables with navy headers, alternating rows).
    • Executive callout label: Key Findings (not "Bottom Line") — .alert with alert-icon pattern from the prompt.
    • Meta bar — Prepared by: R. A. Carucci #261, Principal Analyst | Safe Streets Operations Control Center | Hackensack Police Department.
    • Include **all** print rules from the CSS block: default **@page** portrait, **@page landscape**, @media print, **table.incident-highlights** (allows multi-page table), **.report-tail** / **.report-tail-landscape**.
  CHATGPT_BRIEFING_PROMPT.md repeats a short checklist; attachment #4 is authoritative for CSS/layout.

BEFORE WRITING, EXTRACT:
  From CHATGPT_BRIEFING_PROMPT.md:
    → Cycle ({cycle_id}), Bi-Weekly ({biweekly}), Report Due ({report_due})
    → 7-Day Window ({date_range_7})
    → Bi-Weekly Period ({date_range_bw})
    → All "7-Day Incidents" narratives (use these verbatim, redacted, for incident highlights)

  From SCRPA_Report_Summary.md:
    → All Data Summary counts
    → Category Breakdown table (7-Day | 28-Day | YTD)
    → Lag Day Analysis (mean / median / max)

CRIME CATEGORIES (only these five — never include "Other")
  Motor Vehicle Theft | Burglary Auto | Burglary - Comm & Res | Robbery | Sexual Offenses

HTML SECTIONS (this order; use class names from HPD_REPORT_STYLE_BLOCK.md)

1. HEADER (.header)
   .dept: City of Hackensack | Police Department | Safe Streets Operations Control Center
   h1: SCRPA Tactical Briefing
   .subtitle: Cycle {cycle_id} | Bi-Weekly {biweekly} | 7-Day: {date_range_7} | Bi-Weekly period: {date_range_bw} | Report Due: {report_due}

2. META BAR (.meta-bar)
   Prepared by (author line above); Date; Subject: SCRPA Tactical Briefing; Status (.status-final or .status-review)

3. EXECUTIVE SUMMARY (.content, h2)
   2–4 bullets: only what occurred in the 7-day window; omit zero-count categories.
   Optional: .alert Key Findings for the main takeaway.
   Note backfill only if Backfill 7-Day > 0 in Data Summary.

4. KEY METRICS TABLE (h2 + table from SCRPA_Report_Summary.md Data Summary)
   Rows: Total Incidents | 7-Day | 28-Day | YTD | Prior Year | Lag Incidents | Backfill 7-Day

5. CATEGORY BREAKDOWN TABLE (h2 + table)
   Columns: Category | 7-Day | 28-Day | YTD — five categories only.

6. LAG DAY SUMMARY (h2)
   Mean / Median / Max + one plain-language operational sentence.
   Then close the **.content** div (Lag Day is the last block inside .content).

7–8. After .content, still inside .page, open **.report-tail** (optional class **report-tail-landscape** for landscape PDF — footer must stay inside this same div):
   • h2: 7-Day Incident Highlights
   • table with **class="incident-highlights"** (add **table-notes** if synopsis column is wide). Rows from CHATGPT_BRIEFING_PROMPT.md; columns: Category | Incident Date | Redacted synopsis | Tactical note. If none: one row or short note.
   • **.footer** with exact line: Hackensack Police Department - Safe Streets Operations Control Center | Cycle: {biweekly} | Range: 7-Day: {date_range_7} | Bi-Weekly: {date_range_bw} | Version: 1.0
   • Close .report-tail

OUTPUT RULES (CRITICAL)
  • Raw HTML only; first line <!DOCTYPE html>; last line </html>; no code fences or extra commentary.
  • Apply full HPD CSS from attachment #4 (.page max-width ~900px; include @page / landscape / .report-tail rules).
  • Never display "Other" as a crime category; never invent data — use "—" if absent.
  • **Print-to-PDF:** Do not place **.footer** as a direct child of **.page** after a landscape-only inner wrapper — that orphans the footer. **.footer** must be the last child inside **.report-tail** alongside the incident table.

Now generate the HTML tactical briefing.
"""


def write_chatgpt_session_prompt(
    output_dir: Path,
    cycle_info: Optional[Dict]
) -> Path:
    """
    Write CHATGPT_SESSION_PROMPT.md — the per-cycle paste-and-go prompt for
    ChatGPT. Paste this text into the chat (or attach it) and attach
    CHATGPT_BRIEFING_PROMPT.md, SCRPA_Report_Summary.md, and
    HPD_REPORT_STYLE_BLOCK.md from the same Documentation folder.

    Args:
        output_dir: Documentation folder path
        cycle_info: Cycle information dict (name, biweekly, start_7, end_7,
                    start_bw, end_bw, report_due)

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

    content = CHATGPT_SESSION_PROMPT_TEMPLATE.format(
        cycle_id=cycle_id,
        biweekly=biweekly,
        report_due=report_due,
        date_range_7=date_range_7,
        date_range_bw=date_range_bw,
        hpd_style_path=HPD_REPORT_STYLE_PROMPT_PATH,
    )

    md_path = output_dir / 'CHATGPT_SESSION_PROMPT.md'
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
