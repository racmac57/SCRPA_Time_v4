# 🕒 2026-04-20-11-50-27
# Project: scripts/scrpa_transform.py
# Author: R. A. Carucci
# Purpose: Core Python transformation engine matching All_Crimes.m logic exactly.
#          Converts RMS export data to enriched SCRPA format with cycle detection,
#          lag days calculation, period classification, and crime categorization.
#          Now ingests RAW RMS exports and applies the SCRPA-specific LawSoft IR
#          filter natively (replaces the legacy pre-filtered extract workflow).
#          Supports multi-file ingestion: filter per-file, concat, dedupe by
#          Case Number -- spans yearly + monthly + partial exports in one run.

"""
SCRPA Transform - Python-First Data Transformation Engine

This module provides the core transformation logic that exactly matches the Power BI
M code in All_Crimes.m. All data enrichment is done here, enabling Power BI to become
a simple CSV consumer.

Critical Logic Rules (must match M code exactly):
1. Cycle Resolution: 3-tier lookup (Report_Due_Date match -> In-cycle -> Most recent)
2. LagDays = CycleStart_7Day - Incident_Date (NOT Report_Date - Incident_Date)
3. Report_Date_ForLagday: Only Report_Date or EntryDate (no Incident_Date fallback)
4. Period Classification: Incident_Date-driven, precedence: 7-Day -> Prior Year -> 28-Day -> YTD -> Historical
5. Backfill_7Day: Incident before cycle start AND Report_Date_ForLagday in current 7-day window
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, date, time, timedelta
from typing import Optional, Tuple, Dict, Any, Union, Iterable, List
import warnings
import re

# Suppress pandas warnings for cleaner output
try:
    warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)
except AttributeError:
    pass  # pandas 3.0+ moved or removed this warning


# =============================================================================
# CONFIGURATION
# =============================================================================

CYCLE_CALENDAR_PATH = Path(
    r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Temporal\SCRPA_Cycle\7Day_28Day_Cycle_20260106.csv"
)

# CallType Categories reference for Category_Type and Response_Type lookup
CALLTYPE_CATEGORIES_PATH = Path(
    r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Classifications\CallTypes\CallType_Categories.csv"
)

# =============================================================================
# SCRPA RMS FILTER CONFIG
# Native port of "SCRPA RMS Filter.txt" (LawSoft IR Find/Omit Records criteria).
# Applied in apply_scrpa_filter() before any cycle / LagDays / Period logic so
# that 7-day and 28-day window counts only see SCRPA-eligible incidents.
# Matching is case-insensitive and whitespace-trimmed across Incident Type 1/2/3.
# =============================================================================

# Common gating criteria (must match for both Find and Omit rules)
SCRPA_CASE_NUMBER_PATTERN = r'^\d{2}-\d{6}$'   # LawSoft "## - ######"
SCRPA_REPORT_DATE_FLOOR   = '2024-12-31'        # LawSoft "12/31/2024 ..." (inclusive)

# All three Incident Type slots are scanned with OR semantics
SCRPA_INCIDENT_TYPE_COLS = ['Incident Type_1', 'Incident Type_2', 'Incident Type_3']

# Find Records — keep if ANY type slot matches an exact value or a prefix
SCRPA_INCLUDE_TYPES_EXACT = frozenset({
    'Motor Vehicle Theft - 2C:20-3',
    'Robbery - 2C:15-1',
    'Sexual Assault - 2C:14-2b',
    'Criminal Sexual Contact - 2C:14-3a',
    'Aggravated Sexual Assault - 2C:14-2a',
})
SCRPA_INCLUDE_TYPES_PREFIX = ('Burglary - ',)   # legacy "Burglary - *" wildcard

# Omit Records — drop if ANY type slot matches one of these
SCRPA_OMIT_TYPES_EXACT = frozenset({
    'Domestic Violence - 2C:25-21',
    'Violation of Court Order',
    'Violation: TRO/ FRO - 2C:29-9b',
    'Assist Other Agency',
})

# Omit Records — drop if Case Number is one of these regardless of type
SCRPA_OMIT_CASE_NUMBERS = frozenset({
    '25-070454',
    '25-012110',
})


# Column mappings from RMS export to expected names
RMS_COLUMN_MAP = {
    'Case Number': 'Case Number',
    'Incident Date': 'Incident Date',
    'Incident Time': 'Incident Time',
    'Incident Date_Between': 'Incident Date_Between',
    'Incident Time_Between': 'Incident Time_Between',
    'Report Date': 'Report Date',
    'Report Time': 'Report Time',
    'Incident Type_1': 'Incident Type_1',
    'Incident Type_2': 'Incident Type_2',
    'Incident Type_3': 'Incident Type_3',
    'FullAddress': 'FullAddress',
    'Grid': 'Grid',
    'Zone': 'Zone',
    'Narrative': 'Narrative',
    'Total Value Stolen': 'Total Value Stolen',
    'Total Value Recover': 'Total Value Recover',
    'Registration 1': 'Registration 1',
    'Make1': 'Make1',
    'Model1': 'Model1',
    'Reg State 1': 'Reg State 1',
    'Registration 2': 'Registration 2',
    'Reg State 2': 'Reg State 2',
    'Make2': 'Make2',
    'Model2': 'Model2',
    'Reviewed By': 'Reviewed By',
    'CompleteCalc': 'CompleteCalc',
    'Officer of Record': 'Officer of Record',
    'Squad': 'Squad',
    'Det_Assigned': 'Det_Assigned',
    'Case_Status': 'Case_Status',
    'NIBRS Classification': 'NIBRS Classification',
    'EntryDate': 'EntryDate',  # May not be in all exports
}


# =============================================================================
# HELPER FUNCTIONS (Matching M code CoalesceText, CoalesceAny, AsTime, AsDate)
# =============================================================================

def coalesce_text(a: Any, b: Any) -> Optional[str]:
    """Return first non-null, non-empty text value. Matches M code CoalesceText."""
    if a is None or (isinstance(a, str) and a.strip() == '') or pd.isna(a):
        return b if not pd.isna(b) else None
    return str(a) if not pd.isna(a) else None


def coalesce_any(a: Any, b: Any) -> Any:
    """Return first non-null value. Matches M code CoalesceAny."""
    return a if not pd.isna(a) and a is not None else b


def parse_time(v: Any) -> Optional[time]:
    """
    Parse various time formats to Python time object.
    Matches M code AsTime function behavior.
    """
    if v is None or pd.isna(v):
        return None

    # Already a time
    if isinstance(v, time):
        return v

    # datetime -> extract time
    if isinstance(v, datetime):
        return v.time()

    # pd.Timestamp -> extract time
    if isinstance(v, pd.Timestamp):
        return v.time() if not pd.isna(v) else None

    # timedelta -> convert to time
    if isinstance(v, (timedelta, pd.Timedelta)):
        try:
            total_seconds = v.total_seconds()
            hours = int(total_seconds // 3600) % 24
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            return time(hours, minutes, seconds)
        except:
            return None

    # Number (Excel serial time)
    if isinstance(v, (int, float)):
        try:
            # Excel time fraction
            if 0 <= v < 1:
                total_seconds = int(v * 86400)
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                return time(hours, minutes, seconds)
            return None
        except:
            return None

    # Text parsing
    if isinstance(v, str):
        v_str = v.strip()
        if not v_str:
            return None

        # Try various formats
        time_formats = [
            '%H:%M:%S',
            '%I:%M:%S %p',
            '%I:%M %p',
            '%H:%M',
            '%I:%M:%S%p',
            '%I:%M%p',
        ]

        for fmt in time_formats:
            try:
                dt = datetime.strptime(v_str, fmt)
                return dt.time()
            except ValueError:
                continue

        # Try adding :00 for formats like "16:40"
        if ':' in v_str and v_str.count(':') == 1:
            try:
                dt = datetime.strptime(v_str + ':00', '%H:%M:%S')
                return dt.time()
            except ValueError:
                pass

        return None

    return None


def parse_date(v: Any) -> Optional[date]:
    """
    Parse various date formats to Python date object.
    Matches M code AsDate function behavior.
    """
    if v is None or pd.isna(v):
        return None

    # Already a date
    if isinstance(v, date) and not isinstance(v, datetime):
        return v

    # datetime -> extract date
    if isinstance(v, datetime):
        return v.date()

    # pd.Timestamp -> extract date
    if isinstance(v, pd.Timestamp):
        return v.date() if not pd.isna(v) else None

    # Number (Excel serial date)
    if isinstance(v, (int, float)) and not pd.isna(v):
        try:
            # Excel date serial number (days since 1899-12-30)
            return (datetime(1899, 12, 30) + timedelta(days=int(v))).date()
        except:
            return None

    # Text parsing
    if isinstance(v, str):
        v_str = v.strip()
        if not v_str or v_str.lower() in ('null', 'none', ''):
            return None

        date_formats = [
            '%m/%d/%Y',
            '%Y-%m-%d',
            '%m/%d/%y',
            '%Y/%m/%d',
            '%d/%m/%Y',
            '%m-%d-%Y',
        ]

        for fmt in date_formats:
            try:
                dt = datetime.strptime(v_str, fmt)
                return dt.date()
            except ValueError:
                continue

        # Try pandas parsing as fallback
        try:
            return pd.to_datetime(v_str).date()
        except:
            return None

    return None


def format_time_str(t: Optional[time]) -> str:
    """Format time as HH:MM:SS string, default to 00:00:00."""
    if t is None:
        return "00:00:00"
    return t.strftime('%H:%M:%S')


def format_date_str(d: Optional[date]) -> str:
    """Format date as MM/DD/YYYY string (matches M code output)."""
    if d is None:
        return "Unknown"
    return d.strftime('%m/%d/%Y')


# =============================================================================
# CYCLE CALENDAR FUNCTIONS
# =============================================================================

def load_cycle_calendar(path: Path = CYCLE_CALENDAR_PATH) -> pd.DataFrame:
    """Load and parse the cycle calendar CSV."""
    df = pd.read_csv(path)

    # Parse date columns
    date_cols = ['Report_Due_Date', '7_Day_Start', '7_Day_End', '28_Day_Start', '28_Day_End']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y').dt.date

    return df


def resolve_cycle(calendar_df: pd.DataFrame, report_due_date: date) -> Optional[pd.Series]:
    """
    3-tier cycle resolution matching M code lines 191-224.

    Tier 1: Exact Report_Due_Date match (most accurate - report day lookup)
    Tier 2: Today/report_due within a 7-day cycle (for mid-cycle refreshes)
    Tier 3: Most recent cycle that ended on/before the date

    Args:
        calendar_df: Cycle calendar DataFrame
        report_due_date: The date to resolve cycle for

    Returns:
        Series with cycle info or None if no match
    """
    # Tier 1: Exact Report_Due_Date match
    match1 = calendar_df[calendar_df['Report_Due_Date'] == report_due_date]
    if len(match1) > 0:
        return match1.iloc[0]

    # Tier 2: Date within a 7-day cycle window
    match2 = calendar_df[
        (calendar_df['7_Day_Start'] <= report_due_date) &
        (report_due_date <= calendar_df['7_Day_End'])
    ]
    if len(match2) > 0:
        return match2.iloc[0]

    # Tier 3: Most recent cycle (7_Day_End <= report_due_date)
    eligible = calendar_df[calendar_df['7_Day_End'] <= report_due_date]
    if len(eligible) > 0:
        sorted_df = eligible.sort_values('7_Day_End', ascending=False)
        return sorted_df.iloc[0]

    return None


def resolve_cycle_for_date(calendar_df: pd.DataFrame, d: date) -> Optional[pd.Series]:
    """
    Find the cycle that a given date falls within.
    Used for cycle_name assignment based on Incident_Date.
    """
    if d is None:
        return None

    match = calendar_df[
        (calendar_df['7_Day_Start'] <= d) &
        (d <= calendar_df['7_Day_End'])
    ]
    if len(match) > 0:
        return match.iloc[0]

    return None


# =============================================================================
# TIME OF DAY CLASSIFICATION
# =============================================================================

def classify_time_of_day(t: Optional[time]) -> Tuple[str, int]:
    """
    Classify time into period of day.
    Matches M code lines 453-484.

    Returns:
        Tuple of (TimeOfDay label, TimeOfDay_SortKey)
    """
    if t is None:
        return ("Unknown Time", 99)

    hr = t.hour

    if 4 <= hr < 8:
        return ("Early Morning (04:00-07:59)", 2)
    elif 8 <= hr < 12:
        return ("Morning (08:00-11:59)", 3)
    elif 12 <= hr < 16:
        return ("Afternoon (12:00-15:59)", 4)
    elif 16 <= hr < 20:
        return ("Evening Peak (16:00-19:59)", 5)
    elif 20 <= hr < 24:
        return ("Night (20:00-23:59)", 6)
    else:  # 0 <= hr < 4
        return ("Late Night (00:00-03:59)", 1)


def get_start_of_hour(t: Optional[time]) -> str:
    """Return start of hour as HH:00:00 string."""
    if t is None:
        return "00:00:00"
    return f"{t.hour:02d}:00:00"


# =============================================================================
# CRIME CATEGORY CLASSIFICATION
# =============================================================================

def classify_crime_category(all_incidents: str, narrative: Optional[str]) -> str:
    """
    Classify crime into category.
    Matches M code lines 504-521.
    """
    L = (all_incidents or '').upper()
    N = (narrative or '').upper()

    # Motor Vehicle Theft with theft-from narrative -> Burglary Auto
    if 'MOTOR VEHICLE THEFT' in L:
        if 'THEFT OF HIS PROPERTY' in N or 'THEFT FROM MOTOR VEHICLE' in N:
            return "Burglary Auto"
        return "Motor Vehicle Theft"

    # Direct Burglary Auto matches
    if any(x in L for x in ['BURGLARY - AUTO', 'ATTEMPTED BURGLARY - AUTO', 'THEFT FROM MOTOR VEHICLE']):
        return "Burglary Auto"

    # Commercial/Residence Burglary
    if any(x in L for x in ['BURGLARY - COMMERCIAL', 'ATTEMPTED BURGLARY - COMMERCIAL',
                             'BURGLARY - RESIDENCE', 'ATTEMPTED BURGLARY - RESIDENCE']):
        return "Burglary - Comm & Res"

    # Robbery
    if 'ROBBERY' in L:
        return "Robbery"

    # Sexual Offenses
    if any(x in L for x in ['SEXUAL', 'RAPE']):
        return "Sexual Offenses"

    return "Other"


# =============================================================================
# PERIOD CLASSIFICATION
# =============================================================================

def classify_period(
    incident_date: Optional[date],
    current_year: int,
    cycle_start_7: Optional[date],
    cycle_end_7: Optional[date],
    cycle_start_28: Optional[date],
    cycle_end_28: Optional[date]
) -> Tuple[str, int]:
    """
    Classify incident into reporting period.
    Matches M code lines 242-273.

    IMPORTANT: The 7-Day window uses the CALENDAR's fixed 7_Day_Start and 7_Day_End
    for the resolved cycle (e.g., 01/20/2026 - 01/26/2026 for 26C01W04), NOT
    "today minus 7 days". This means an incident on 01/27/2026 when running the
    01/27/2026 report would be classified as YTD (not 7-Day) because it falls
    outside the cycle's 7-Day window which ended on 01/26/2026.

    Priority order: 7-Day -> Prior Year (currentYear-1) -> 28-Day -> YTD -> Historical

    Returns:
        Tuple of (Period label, Period_SortKey)
    """
    if incident_date is None:
        return ("Historical", 5)

    incident_year = incident_date.year

    # Check 7-Day first (highest priority)
    if cycle_start_7 and cycle_end_7:
        if cycle_start_7 <= incident_date <= cycle_end_7:
            return ("7-Day", 1)

    # Check Prior Year before 28-Day (to prevent prior year from being classified as 28-Day)
    if incident_year == current_year - 1:
        return ("Prior Year", 4)

    # Check 28-Day (only for current year incidents, not prior year)
    if cycle_start_28 and cycle_end_28:
        if cycle_start_28 <= incident_date <= cycle_end_28:
            return ("28-Day", 2)

    # YTD: incident occurred in current year but outside 7-Day/28-Day windows
    if incident_year == current_year:
        return ("YTD", 3)

    # Historical: older years (2024 and earlier)
    return ("Historical", 5)


def build_period_debug(
    incident_date: Optional[date],
    has_cycle: bool,
    report_due_date: Optional[date],
    cycle_start: Optional[date],
    cycle_end: Optional[date],
    in_7day: bool,
    in_28day: bool
) -> str:
    """Build debug string for period calculation. Matches M code lines 278-298."""
    d_str = "NULL" if incident_date is None else str(incident_date)
    year_str = "NULL" if incident_date is None else str(incident_date.year)

    return (
        f"dI={d_str.replace('-', '/')} | "
        f"HasCycle={str(has_cycle).lower()} | "
        f"ReportDue={str(report_due_date).replace('-', '/') if report_due_date else 'NULL'} | "
        f"CycleStart={str(cycle_start).replace('-', '/') if cycle_start else 'NULL'} | "
        f"CycleEnd={str(cycle_end).replace('-', '/') if cycle_end else 'NULL'} | "
        f"in7Day={str(in_7day).lower()} | "
        f"in28Day={str(in_28day).lower()} | "
        f"Year={year_str}"
    )


# =============================================================================
# VEHICLE AND ADDRESS FORMATTING
# =============================================================================

def format_vehicle(
    reg_state: Any,
    registration: Any,
    make: Any,
    model: Any
) -> Optional[str]:
    """
    Format vehicle info as "STATE - REG, MAKE/MODEL".
    Matches M code lines 574-598 (Vehicle_1) and 600-624 (Vehicle_2).
    """
    reg_state_str = str(reg_state).strip() if reg_state and not pd.isna(reg_state) else ""
    registration_str = str(registration).strip() if registration and not pd.isna(registration) else ""
    make_str = str(make).strip() if make and not pd.isna(make) else ""
    model_str = str(model).strip() if model and not pd.isna(model) else ""

    # Build state/registration part
    if reg_state_str and registration_str:
        state_reg = f"{reg_state_str} - {registration_str}"
    elif registration_str:
        state_reg = registration_str
    else:
        state_reg = reg_state_str

    # Build make/model part
    if make_str and model_str:
        make_model = f"{make_str}/{model_str}"
    elif make_str:
        make_model = make_str
    else:
        make_model = model_str

    # Combine
    if state_reg and make_model:
        result = f"{state_reg}, {make_model}"
    elif state_reg:
        result = state_reg
    else:
        result = make_model

    if not result:
        return None

    return result.upper()


def clean_address(full_address: Any) -> Optional[str]:
    """
    Clean address by removing ", Hackensack, NJ, XXXXX" suffix.
    Matches M code lines 633-644.
    """
    if full_address is None or pd.isna(full_address):
        return None

    addr = str(full_address).strip()
    if not addr:
        return None

    # Remove ", Hackensack, NJ" and everything after
    idx = addr.find(', Hackensack, NJ')
    if idx > 0:
        return addr[:idx]

    return addr


# =============================================================================
# CALLTYPE CATEGORIES LOOKUP
# =============================================================================

def load_calltype_categories(path: Path = CALLTYPE_CATEGORIES_PATH) -> Optional[pd.DataFrame]:
    """Load CallType_Categories.csv for Category_Type and Response_Type lookup."""
    if not path.exists():
        print(f"Warning: CallType_Categories not found at {path}")
        return None

    try:
        df = pd.read_csv(path)
        # Normalize column names
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Warning: Could not load CallType_Categories: {e}")
        return None


def lookup_category_response(
    incident_key: str,
    calltype_df: Optional[pd.DataFrame]
) -> Tuple[str, str]:
    """
    Look up Category_Type and Response_Type for an incident key.

    Matching strategy (matches M code):
    1. Exact match on 'Incident' column
    2. Exact match on 'Incident_Norm' column
    3. Default to "Unknown"

    Args:
        incident_key: The incident type string to look up (e.g., IncidentKey or ALL_INCIDENTS)
        calltype_df: DataFrame from CallType_Categories.csv

    Returns:
        Tuple of (Category_Type, Response_Type)
    """
    if calltype_df is None or incident_key is None or pd.isna(incident_key):
        return ("Unknown", "Unknown")

    incident_key_str = str(incident_key).strip()
    if not incident_key_str:
        return ("Unknown", "Unknown")

    # Try exact match on Incident column
    if 'Incident' in calltype_df.columns:
        match = calltype_df[calltype_df['Incident'] == incident_key_str]
        if len(match) > 0:
            row = match.iloc[0]
            cat = row.get('Category_Type', 'Unknown')
            resp = row.get('Response_Type', 'Unknown')
            return (cat if pd.notna(cat) else 'Unknown', resp if pd.notna(resp) else 'Unknown')

    # Try exact match on Incident_Norm column
    if 'Incident_Norm' in calltype_df.columns:
        match = calltype_df[calltype_df['Incident_Norm'] == incident_key_str]
        if len(match) > 0:
            row = match.iloc[0]
            cat = row.get('Category_Type', 'Unknown')
            resp = row.get('Response_Type', 'Unknown')
            return (cat if pd.notna(cat) else 'Unknown', resp if pd.notna(resp) else 'Unknown')

    # Try partial/contains match on Incident column (for compound incident types)
    if 'Incident' in calltype_df.columns:
        # Check if any part of the incident_key matches
        for _, row in calltype_df.iterrows():
            incident_val = str(row.get('Incident', '')).strip()
            if incident_val and incident_val in incident_key_str:
                cat = row.get('Category_Type', 'Unknown')
                resp = row.get('Response_Type', 'Unknown')
                return (cat if pd.notna(cat) else 'Unknown', resp if pd.notna(resp) else 'Unknown')

    return ("Unknown", "Unknown")


# =============================================================================
# CSV OUTPUT FORMATTING
# =============================================================================

def format_time_for_csv(t: Any) -> Optional[str]:
    """
    Format time value as HH:mm:ss string for CSV output.
    Handles various input types: time, datetime, Timestamp, timedelta, string.
    Returns None for null values, HH:mm:ss string otherwise.
    """
    if t is None or pd.isna(t):
        return None

    # Already a time object
    if isinstance(t, time):
        return t.strftime('%H:%M:%S')

    # datetime or Timestamp
    if isinstance(t, (datetime, pd.Timestamp)):
        return t.strftime('%H:%M:%S')

    # timedelta (e.g., "0 days 16:40:35")
    if isinstance(t, (timedelta, pd.Timedelta)):
        total_seconds = int(t.total_seconds())
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # String - check if it already looks like HH:mm:ss
    if isinstance(t, str):
        t_str = t.strip()
        # Remove "0 days " prefix if present
        if t_str.startswith('0 days '):
            t_str = t_str[7:]
        # Check if it's already in time format
        if re.match(r'^\d{1,2}:\d{2}(:\d{2})?$', t_str):
            return t_str if ':' in t_str else t_str + ':00'
        # Try to parse
        try:
            parsed = parse_time(t_str)
            if parsed:
                return parsed.strftime('%H:%M:%S')
        except:
            pass
        return t_str  # Return as-is if can't parse

    return str(t) if t else None


def coerce_zone_to_int(zone: Any) -> Optional[int]:
    """
    Coerce Zone value to integer.
    Zone should be a whole number (observed range 5-9).
    """
    if zone is None or pd.isna(zone):
        return None

    try:
        # Handle string
        if isinstance(zone, str):
            zone = zone.strip()
            if not zone:
                return None
            # Remove any decimal part
            if '.' in zone:
                zone = zone.split('.')[0]
            return int(zone)

        # Handle float
        if isinstance(zone, float):
            return int(zone)

        # Handle int
        if isinstance(zone, int):
            return zone

        return int(zone)
    except (ValueError, TypeError):
        return None


def clean_narrative(narrative: Any) -> Optional[str]:
    """
    Clean narrative text: remove line breaks, collapse whitespace.
    Matches M code lines 551-572.
    """
    if narrative is None or pd.isna(narrative):
        return None

    text = str(narrative)
    if not text.strip():
        return None

    # Replace various line breaks with space
    text = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')

    # Collapse multiple spaces
    while '    ' in text:
        text = text.replace('    ', ' ')
    while '   ' in text:
        text = text.replace('   ', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')

    # Remove control characters
    text = ''.join(c for c in text if c.isprintable() or c == ' ')

    return text.strip() if text.strip() else None


def clean_incident_type(incident_type: Any) -> Optional[str]:
    """
    Clean incident type by removing " - 2C" suffix.
    Matches M code lines 523-530.
    """
    if incident_type is None or pd.isna(incident_type):
        return None

    text = str(incident_type)
    idx = text.find(' - 2C')
    if idx > 0:
        return text[:idx]

    return text


def normalize_incident_type(incident_type: Any) -> Optional[str]:
    """
    Normalize incident type by replacing "Attempted Burglary" with "Burglary".
    Matches M code lines 532-549.
    """
    if incident_type is None or pd.isna(incident_type):
        return None

    return str(incident_type).replace('Attempted Burglary', 'Burglary')


# =============================================================================
# MAIN TRANSFORM FUNCTION
# =============================================================================

def _scrpa_type_mask(
    df: pd.DataFrame,
    exact_set: frozenset,
    prefixes: Tuple[str, ...] = (),
) -> pd.Series:
    """
    Build an OR mask across all three Incident Type slots.

    Matching is case-insensitive and whitespace-trimmed so dirty source data
    (e.g. trailing spaces, mixed casing) does not silently drop SCRPA-eligible
    incidents. Returns a boolean Series aligned to df.index.
    """
    mask = pd.Series(False, index=df.index)
    exact_norm = {s.casefold() for s in exact_set}
    pref_norm  = tuple(p.casefold() for p in prefixes)
    for col in SCRPA_INCIDENT_TYPE_COLS:
        if col not in df.columns:
            continue  # tolerate exports missing Type_2/3 slots
        vals = df[col].astype(str).str.strip().str.casefold()
        mask |= vals.isin(exact_norm)
        for p in pref_norm:
            mask |= vals.str.startswith(p, na=False)
    return mask


def apply_scrpa_filter(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Apply the SCRPA RMS filter to a raw RMS export DataFrame.

    Native port of "SCRPA RMS Filter.txt" (legacy LawSoft IR Find/Omit
    criteria). MUST be called BEFORE resolve_cycle / LagDays / Period
    classification so 7-day and 28-day window counts are computed only
    over SCRPA-eligible incidents.

    Logic (mirrors LawSoft IR semantics):
        KEEP if  case_number matches '##-######'
             AND report_date >= 2024-12-31
             AND ANY incident-type slot ∈ INCLUDE_EXACT
                 OR  ANY incident-type slot startswith INCLUDE_PREFIX
        AND NOT (
                 ANY incident-type slot ∈ OMIT_EXACT
              OR case_number ∈ OMIT_CASE_NUMBERS
        )
    """
    required = ['Case Number', 'Report Date'] + SCRPA_INCIDENT_TYPE_COLS[:1]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(
            f"RMS export missing columns required by SCRPA filter: {missing}"
        )

    # ---- Common gating criteria ----------------------------------------
    case_str = df['Case Number'].astype(str).str.strip()
    case_ok  = case_str.str.match(SCRPA_CASE_NUMBER_PATTERN)

    report_dt = pd.to_datetime(df['Report Date'], errors='coerce')
    date_ok   = report_dt >= pd.Timestamp(SCRPA_REPORT_DATE_FLOOR)

    # ---- Find Records (KEEP) -------------------------------------------
    include_mask = _scrpa_type_mask(
        df, SCRPA_INCLUDE_TYPES_EXACT, SCRPA_INCLUDE_TYPES_PREFIX
    )

    # ---- Omit Records (DROP) -------------------------------------------
    omit_by_type = _scrpa_type_mask(df, SCRPA_OMIT_TYPES_EXACT, ())
    omit_by_case = case_str.isin(SCRPA_OMIT_CASE_NUMBERS)
    omit_mask    = omit_by_type | omit_by_case

    keep = case_ok & date_ok & include_mask & ~omit_mask
    out  = df.loc[keep].copy().reset_index(drop=True)

    if verbose:
        print(f"  SCRPA filter: {len(df)} raw -> {len(out)} kept "
              f"(dropped {len(df) - len(out)})")
        # Diagnostic: SCRPA-eligible rows lost only to the case-pattern gate
        lost_to_case = (include_mask & ~omit_mask & ~case_ok).sum()
        if lost_to_case:
            print(f"  SCRPA filter: {lost_to_case} eligible incident(s) "
                  f"dropped by case-number pattern '{SCRPA_CASE_NUMBER_PATTERN}' "
                  f"-- review for non-conforming Case Numbers")

    return out


def read_rms_export(
    path: Union[str, Path],
    apply_filter: bool = True,
) -> pd.DataFrame:
    """
    Load a raw RMS export (CSV/Excel) and optionally apply the SCRPA filter.

    Args:
        path:         Path to RMS export file
        apply_filter: If True (default), the SCRPA filter is applied natively
                      so downstream stages see only SCRPA-eligible incidents.
                      Pass False for diagnostic / raw-data inspection.

    Returns:
        DataFrame with RMS data (filtered by default).
    """
    path = Path(path)

    if path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(path)
    else:
        # Try multiple encodings - RMS exports may use Windows encoding
        encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
        df = None
        last_error = None
        for encoding in encodings:
            try:
                df = pd.read_csv(path, low_memory=False, encoding=encoding)
                break
            except UnicodeDecodeError as e:
                last_error = e
                continue
        if df is None:
            raise last_error or ValueError(f"Could not read CSV with any supported encoding: {encodings}")

    if apply_filter:
        df = apply_scrpa_filter(df)

    return df


def read_rms_exports(
    paths: Iterable[Union[str, Path]],
    apply_filter: bool = True,
    dedupe_by_case: bool = True,
) -> pd.DataFrame:
    """
    Load and concatenate multiple RMS exports, applying the SCRPA filter per file.

    Per-file filtering keeps diagnostics clean (you see "raw -> kept" for each
    export individually). Concat is column-tolerant (sort=False) so an older
    export missing a newer field won't crash ingestion. Optional dedupe by
    'Case Number' keeps the LAST occurrence across files -- designed for the
    case where a case appears in both a yearly rollup and a monthly export.

    Args:
        paths:          Iterable of file paths (order determines dedupe "winner")
        apply_filter:   Apply SCRPA filter per file (default True)
        dedupe_by_case: Drop duplicate Case Numbers across files (default True)

    Returns:
        Single combined, filtered, deduped DataFrame ready for
        build_all_crimes_enhanced().
    """
    paths_list: List[Path] = [Path(p) for p in paths]
    if not paths_list:
        raise ValueError("read_rms_exports: no input paths provided")

    frames: List[pd.DataFrame] = []
    for p in paths_list:
        if not p.exists():
            print(f"  WARNING: {p} does not exist -- skipping")
            continue
        if p.stat().st_size == 0:
            print(f"  WARNING: {p} is empty (0 bytes) -- skipping")
            continue
        print(f"  Loading: {p.name}")
        df = read_rms_export(p, apply_filter=apply_filter)
        print(f"    -> {len(df)} rows kept from {p.name}")
        frames.append(df)

    if not frames:
        raise ValueError("read_rms_exports: no readable input files")

    # Column-tolerant concat (sort=False preserves first-seen column order)
    combined = pd.concat(frames, ignore_index=True, sort=False)
    print(f"  Combined: {len(combined)} rows from {len(frames)} file(s)")

    if dedupe_by_case and 'Case Number' in combined.columns:
        before = len(combined)
        # keep='last' so a later-listed file (e.g. a partial with fresher data)
        # wins over an earlier yearly rollup for the same Case Number
        combined = combined.drop_duplicates(subset='Case Number', keep='last')
        dropped = before - len(combined)
        if dropped:
            print(f"  Deduped: dropped {dropped} duplicate Case Number(s) "
                  f"(kept last occurrence across files)")
        combined = combined.reset_index(drop=True)

    return combined


def build_all_crimes_enhanced(
    rms_df: pd.DataFrame,
    calendar_df: pd.DataFrame,
    report_due_date: Optional[date] = None,
    today: Optional[date] = None
) -> pd.DataFrame:
    """
    Main transformation pipeline matching All_Crimes.m logic.

    Args:
        rms_df: Raw RMS export DataFrame
        calendar_df: Cycle calendar DataFrame
        report_due_date: Optional specific report due date (defaults to today)
        today: Optional override for "today" (defaults to actual today)

    Returns:
        Enriched DataFrame matching preview table structure
    """
    # Work on a copy
    df = rms_df.copy()

    # Set today
    if today is None:
        today = date.today()
    current_year = today.year

    # =========================================================================
    # STEP 1: Resolve Current Cycle (matches M code lines 191-232)
    # =========================================================================
    if report_due_date:
        cycle = resolve_cycle(calendar_df, report_due_date)
    else:
        cycle = resolve_cycle(calendar_df, today)

    has_current_cycle = cycle is not None

    def _to_date(v):
        """Normalize to Python date for reliable comparisons (handles pandas Timestamp/NaT)."""
        if v is None or pd.isna(v):
            return None
        if isinstance(v, date) and not hasattr(v, 'date'):
            return v
        if hasattr(v, 'date') and callable(getattr(v, 'date')):
            try:
                return v.date()
            except Exception:
                return None
        return None

    if has_current_cycle:
        current_cycle_report_due = _to_date(cycle.get('Report_Due_Date'))
        current_cycle_start = _to_date(cycle.get('7_Day_Start'))
        current_cycle_end = _to_date(cycle.get('7_Day_End'))
        current_cycle_28_start = _to_date(cycle.get('28_Day_Start'))
        current_cycle_28_end = _to_date(cycle.get('28_Day_End'))
        # Fallback: if 28-day window missing or same as 7-day (calendar error), use 28 days ending on 7_Day_End
        if current_cycle_end:
            if current_cycle_28_start is None or current_cycle_28_end is None:
                current_cycle_28_end = current_cycle_end
                current_cycle_28_start = current_cycle_end - timedelta(days=27)
            elif current_cycle_28_start == current_cycle_start and current_cycle_28_end == current_cycle_end:
                # Calendar has 28-day same as 7-day; use proper 28-day window (27 days before 7_Day_End through 7_Day_End)
                current_cycle_28_start = current_cycle_end - timedelta(days=27)
                current_cycle_28_end = current_cycle_end
        current_cycle_name = cycle.get('Report_Name')
        # Extract BiWeekly_Report_Name if available (e.g., 26BW01, 26BW02)
        current_biweekly_name = None
        if 'BiWeekly_Report_Name' in cycle.index:
            bw_name = cycle['BiWeekly_Report_Name']
            if pd.notna(bw_name) and str(bw_name).strip():
                current_biweekly_name = str(bw_name).strip()
    else:
        current_cycle_report_due = None
        current_cycle_start = None
        current_cycle_end = None
        current_cycle_28_start = None
        current_cycle_28_end = None
        current_cycle_name = None
        current_biweekly_name = None

    # =========================================================================
    # STEP 2: Time Processing with Cascading Logic (matches M code lines 64-109)
    # =========================================================================
    def process_time_row(row):
        """Process time columns with cascading: Incident Time -> Incident Time_Between -> Report Time"""
        it = parse_time(row.get('Incident Time'))
        itb = parse_time(row.get('Incident Time_Between'))
        rt = parse_time(row.get('Report Time'))

        # Best time value (cascade)
        best = it if it else (itb if itb else rt)

        # Time source
        if it:
            source = "Incident Time"
        elif itb:
            source = "Incident Time_Between"
        elif rt:
            source = "Report Time"
        else:
            source = "None"

        return best, source

    time_results = df.apply(process_time_row, axis=1)
    df['BestTimeValue'] = [r[0] for r in time_results]
    df['TimeSource'] = [r[1] for r in time_results]
    df['Incident_Time'] = df['BestTimeValue'].apply(format_time_str)

    # =========================================================================
    # STEP 3: Incident Date Processing (matches M code lines 114-139)
    # =========================================================================
    def process_incident_date_row(row):
        """Process incident date with cascading: Incident Date -> Incident Date_Between -> Report Date"""
        d_it = parse_date(row.get('Incident Date'))
        d_itb = parse_date(row.get('Incident Date_Between'))
        d_rt = parse_date(row.get('Report Date'))

        best = d_it if d_it else (d_itb if d_itb else d_rt)
        return best

    df['Incident_Date_Date'] = df.apply(process_incident_date_row, axis=1)
    df['Incident_Date'] = df['Incident_Date_Date'].apply(format_date_str)

    # =========================================================================
    # STEP 4: Report Date Processing (matches M code lines 144-182)
    # =========================================================================
    def process_report_date_row(row):
        """Process report date with cascade to Incident_Date_Date as fallback."""
        d_rd = parse_date(row.get('Report Date'))
        d_ed = parse_date(row.get('EntryDate'))
        incident_date_date = row.get('Incident_Date_Date')

        # Report_Date: Report Date -> EntryDate -> Incident_Date_Date
        report_date = coalesce_any(d_rd, coalesce_any(d_ed, incident_date_date))

        # Report_Date_ForLagday: ONLY Report Date or EntryDate (NO Incident_Date fallback)
        # This is critical for correct LagDay calculation
        report_date_for_lagday = coalesce_any(d_rd, d_ed)

        return report_date, report_date_for_lagday

    report_results = df.apply(process_report_date_row, axis=1)
    df['Report_Date'] = [r[0] for r in report_results]
    df['Report_Date_ForLagday'] = [r[1] for r in report_results]

    df['Report_Date_Text'] = df['Report_Date'].apply(
        lambda d: d.strftime('%m/%d/%Y') if d else None
    )

    # IncidentToReportDays
    def calc_incident_to_report_days(row):
        rd = row.get('Report_Date')
        idd = row.get('Incident_Date_Date')
        if rd and idd:
            return (rd - idd).days
        return None

    df['IncidentToReportDays'] = df.apply(calc_incident_to_report_days, axis=1)

    # =========================================================================
    # STEP 5: Period Classification (matches M code lines 242-313)
    # =========================================================================
    def classify_period_row(row):
        incident_date = row.get('Incident_Date_Date')
        period, sort_key = classify_period(
            incident_date,
            current_year,
            current_cycle_start,
            current_cycle_end,
            current_cycle_28_start,
            current_cycle_28_end
        )

        # Build debug info
        in_7day = (
            incident_date is not None and
            current_cycle_start is not None and
            current_cycle_end is not None and
            current_cycle_start <= incident_date <= current_cycle_end
        )
        in_28day = (
            incident_date is not None and
            current_cycle_28_start is not None and
            current_cycle_28_end is not None and
            current_cycle_28_start <= incident_date <= current_cycle_28_end
        )

        debug = build_period_debug(
            incident_date,
            has_current_cycle,
            current_cycle_report_due,
            current_cycle_start,
            current_cycle_end,
            in_7day,
            in_28day
        )

        return period, sort_key, debug

    period_results = df.apply(classify_period_row, axis=1)
    df['Period'] = [r[0] for r in period_results]
    df['Period_SortKey'] = [r[1] for r in period_results]
    df['_Period_Debug'] = [r[2] for r in period_results]

    # =========================================================================
    # STEP 6: Cycle Name Assignment (matches M code lines 315-326)
    # =========================================================================
    def get_cycle_name(incident_date):
        if incident_date is None:
            return "Unknown"

        cycle = resolve_cycle_for_date(calendar_df, incident_date)
        if cycle is not None:
            return cycle['Report_Name']
        return "Historical"

    df['cycle_name'] = df['Incident_Date_Date'].apply(get_cycle_name)

    # =========================================================================
    # STEP 7: Backfill_7Day Flag (matches M code lines 328-336)
    # =========================================================================
    def calc_backfill_7day(row):
        """
        Backfill_7Day: Incident occurred BEFORE cycle start
        AND Report_Date_ForLagday is WITHIN current 7-day window.
        """
        if not has_current_cycle:
            return False

        incident_date = row.get('Incident_Date_Date')
        report_date_for_lagday = row.get('Report_Date_ForLagday')

        if incident_date is None or report_date_for_lagday is None:
            return False

        return (
            incident_date < current_cycle_start and
            current_cycle_start <= report_date_for_lagday <= current_cycle_end
        )

    df['Backfill_7Day'] = df.apply(calc_backfill_7day, axis=1)

    # cycle_name_adjusted (matches M code lines 338-343)
    df['cycle_name_adjusted'] = df.apply(
        lambda row: coalesce_text(current_cycle_name, row['cycle_name']) if row['Backfill_7Day'] else row['cycle_name'],
        axis=1
    )

    # BiWeekly_Report_Name: Add bi-weekly cycle name from calendar (e.g., 26BW02)
    # This is the bi-weekly label for the current reporting cycle (when available)
    df['BiWeekly_Report_Name'] = current_biweekly_name

    # =========================================================================
    # STEP 8: IsCurrent7DayCycle (matches M code lines 348-358)
    # =========================================================================
    def calc_is_current_7day_cycle(row):
        """Check if Report_Date_ForLagday falls within current 7-day cycle."""
        if not has_current_cycle:
            return False

        report_date_for_lagday = row.get('Report_Date_ForLagday')
        if report_date_for_lagday is None:
            return False

        return current_cycle_start <= report_date_for_lagday <= current_cycle_end

    df['IsCurrent7DayCycle'] = df.apply(calc_is_current_7day_cycle, axis=1)

    # =========================================================================
    # STEP 9: IsLagDay and LagDays (matches M code lines 360-439)
    # =========================================================================
    def calc_is_lagday_and_lagdays(row):
        """
        Calculate IsLagDay and LagDays using 3-tier cycle resolution.

        For each row, find cycle based on Report_Date_ForLagday using same 3-tier approach.
        IsLagDay = True if Incident_Date < CycleStartForReport
        LagDays = CycleStartForReport - Incident_Date (in days)
        """
        incident_date = row.get('Incident_Date_Date')
        report_date_for_lagday = row.get('Report_Date_ForLagday')

        if incident_date is None or report_date_for_lagday is None:
            return False, 0 if incident_date is None or report_date_for_lagday is None else None

        # Find cycle for this row's Report_Date_ForLagday using 3-tier approach
        report_cycle = resolve_cycle(calendar_df, report_date_for_lagday)

        if report_cycle is None:
            return False, 0

        cycle_start_for_report = report_cycle['7_Day_Start']

        if cycle_start_for_report is None:
            return False, 0

        is_lag_day = incident_date < cycle_start_for_report

        if not is_lag_day:
            return False, 0

        lag_days = (cycle_start_for_report - incident_date).days
        return True, lag_days

    lag_results = df.apply(calc_is_lagday_and_lagdays, axis=1)
    df['IsLagDay'] = [r[0] for r in lag_results]
    df['LagDays'] = [r[1] for r in lag_results]

    # =========================================================================
    # STEP 10: Time of Day (matches M code lines 444-484)
    # =========================================================================
    df['StartOfHour'] = df['BestTimeValue'].apply(get_start_of_hour)

    tod_results = df['BestTimeValue'].apply(classify_time_of_day)
    df['TimeOfDay'] = [r[0] for r in tod_results]
    df['TimeOfDay_SortKey'] = [r[1] for r in tod_results]

    # =========================================================================
    # STEP 11: Incident Consolidation & Category (matches M code lines 489-521)
    # =========================================================================
    def build_all_incidents(row):
        i1 = row.get('Incident Type_1') or ''
        i2 = row.get('Incident Type_2') or ''
        i3 = row.get('Incident Type_3') or ''

        parts = [str(i1) if i1 and not pd.isna(i1) else '']
        if i2 and not pd.isna(i2) and str(i2).strip():
            parts.append(str(i2))
        if i3 and not pd.isna(i3) and str(i3).strip():
            parts.append(str(i3))

        return ', '.join(p for p in parts if p)

    df['ALL_INCIDENTS'] = df.apply(build_all_incidents, axis=1)

    # Clean incident types (remove " - 2C" suffix)
    for col in ['Incident Type_1', 'Incident Type_2', 'Incident Type_3']:
        if col in df.columns:
            df[col] = df[col].apply(clean_incident_type)

    # Normalize incident types
    df['Incident_Type_1_Norm'] = df['Incident Type_1'].apply(normalize_incident_type)
    df['Incident_Type_2_Norm'] = df['Incident Type_2'].apply(normalize_incident_type)
    df['Incident_Type_3_Norm'] = df['Incident Type_3'].apply(normalize_incident_type)

    # Crime Category
    df['Crime_Category'] = df.apply(
        lambda row: classify_crime_category(row.get('ALL_INCIDENTS', ''), row.get('Narrative')),
        axis=1
    )

    # Clean narrative
    if 'Narrative' in df.columns:
        df['Narrative'] = df['Narrative'].apply(clean_narrative)

    # =========================================================================
    # STEP 12: Vehicle Formatting (matches M code lines 574-631)
    # =========================================================================
    df['Vehicle_1'] = df.apply(
        lambda row: format_vehicle(
            row.get('Reg State 1'),
            row.get('Registration 1'),
            row.get('Make1'),
            row.get('Model1')
        ),
        axis=1
    )

    df['Vehicle_2'] = df.apply(
        lambda row: format_vehicle(
            row.get('Reg State 2'),
            row.get('Registration 2'),
            row.get('Make2'),
            row.get('Model2')
        ),
        axis=1
    )

    # Vehicle_1_and_Vehicle_2 (combined)
    df['Vehicle_1_and_Vehicle_2'] = df.apply(
        lambda row: f"{row['Vehicle_1']} | {row['Vehicle_2']}"
            if row['Vehicle_1'] and row['Vehicle_2'] else None,
        axis=1
    )

    # =========================================================================
    # STEP 13: Clean Address (matches M code lines 633-644)
    # =========================================================================
    df['Clean_Address'] = df['FullAddress'].apply(clean_address)

    # =========================================================================
    # STEP 14: IncidentKey for Category Lookup (matches M code lines 649-654)
    # =========================================================================
    df['IncidentKey'] = df.apply(
        lambda row: coalesce_text(row.get('ALL_INCIDENTS'), row.get('Incident Type_1')),
        axis=1
    )

    # =========================================================================
    # STEP 15: Category_Type and Response_Type (lookup from CallType_Categories.csv)
    # =========================================================================
    # Load CallType_Categories reference table
    calltype_df = load_calltype_categories()

    def get_category_response(row):
        """Look up Category_Type and Response_Type using IncidentKey."""
        incident_key = row.get('IncidentKey')
        return lookup_category_response(incident_key, calltype_df)

    cat_resp_results = df.apply(get_category_response, axis=1)
    df['Category_Type'] = [r[0] for r in cat_resp_results]
    df['Response_Type'] = [r[1] for r in cat_resp_results]

    # =========================================================================
    # STEP 16: Time Validation (matches M code lines 719-729)
    # =========================================================================
    def build_time_validation(row):
        source = row.get('TimeSource', 'None')
        it_orig = row.get('Incident Time')
        itb_orig = row.get('Incident Time_Between')
        rt_orig = row.get('Report Time')
        best = row.get('BestTimeValue')

        it_str = "null" if it_orig is None or pd.isna(it_orig) else str(it_orig)
        itb_str = "null" if itb_orig is None or pd.isna(itb_orig) else str(itb_orig)
        rt_str = "null" if rt_orig is None or pd.isna(rt_orig) else str(rt_orig)
        best_str = "null" if best is None else best.strftime('%I:%M %p')

        return (
            f"Source: {source} | "
            f"Original IT: {it_str} | "
            f"Original ITB: {itb_str} | "
            f"Original RT: {rt_str} | "
            f"Cascaded: {best_str}"
        )

    df['Time_Validation'] = df.apply(build_time_validation, axis=1)

    # =========================================================================
    # STEP 17: Sort and finalize (matches M code lines 733-741)
    # =========================================================================
    # Sort by Incident Date ascending, Period descending, Report Date ascending
    df = df.sort_values(
        by=['Incident Date', 'Period', 'Report Date', 'Report_Date'],
        ascending=[True, False, True, True],
        na_position='first'
    )

    # =========================================================================
    # STEP 18: Format columns for CSV output
    # =========================================================================
    # Zone: Coerce to integer (whole number, range 5-9)
    # Convert to string representation without decimals for CSV output
    if 'Zone' in df.columns:
        def zone_to_str(z):
            if z is None or pd.isna(z):
                return ''
            try:
                return str(int(float(z)))
            except (ValueError, TypeError):
                return ''
        df['Zone'] = df['Zone'].apply(zone_to_str)

    # Time columns: Format as HH:mm:ss (not "0 days HH:mm:ss")
    time_columns_to_format = ['Incident Time', 'Incident Time_Between', 'Report Time', 'BestTimeValue']
    for col in time_columns_to_format:
        if col in df.columns:
            df[col] = df[col].apply(format_time_for_csv)

    # =========================================================================
    # STEP 19: Select and order columns to match preview table
    # =========================================================================
    output_columns = [
        # Original RMS columns
        'Case Number', 'Incident Date', 'Incident Time', 'Incident Date_Between',
        'Incident Time_Between', 'Report Date', 'Report Time', 'Incident Type_1',
        'Incident Type_2', 'Incident Type_3', 'FullAddress', 'Grid', 'Zone',
        'Narrative', 'Total Value Stolen', 'Total Value Recover', 'Registration 1',
        'Make1', 'Model1', 'Reg State 1', 'Registration 2', 'Reg State 2', 'Make2',
        'Model2', 'Reviewed By', 'CompleteCalc', 'Officer of Record', 'Squad',
        'Det_Assigned', 'Case_Status', 'NIBRS Classification',
        # Computed columns
        'BestTimeValue', 'TimeSource', 'Incident_Time', 'Incident_Date',
        'Incident_Date_Date', 'Report_Date', 'Report_Date_Text',
        'IncidentToReportDays', 'Period', '_Period_Debug', 'Period_SortKey',
        'cycle_name', 'Backfill_7Day', 'cycle_name_adjusted', 'BiWeekly_Report_Name',
        'IsCurrent7DayCycle', 'IsLagDay', 'LagDays', 'StartOfHour', 'TimeOfDay',
        'TimeOfDay_SortKey', 'ALL_INCIDENTS', 'Crime_Category', 'Incident_Type_1_Norm',
        'Incident_Type_2_Norm', 'Incident_Type_3_Norm', 'Vehicle_1', 'Vehicle_2',
        'Vehicle_1_and_Vehicle_2', 'Clean_Address', 'IncidentKey', 'Category_Type',
        'Response_Type', 'Time_Validation'
    ]

    # Add Report_Date_ForLagday (used internally but may be useful for debugging)
    output_columns.append('Report_Date_ForLagday')

    # Only include columns that exist
    final_columns = [c for c in output_columns if c in df.columns]

    # Add any remaining original columns not in the list
    for col in df.columns:
        if col not in final_columns:
            final_columns.append(col)

    return df[final_columns].reset_index(drop=True)


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """Command-line interface for scrpa_transform."""
    import argparse

    parser = argparse.ArgumentParser(
        description='SCRPA Transform - Convert RMS export to enriched crime data'
    )
    parser.add_argument(
        'input',
        nargs='+',
        help='Path(s) to RMS export CSV or Excel file(s). Accepts one or many '
             '(shell globs work, e.g. monthly/2026/*.xlsx). Multiple files are '
             'filtered per-file, concatenated, then deduped by Case Number.'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output CSV path (default: input_enhanced.csv)',
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
        '--today',
        help='Override today date (MM/DD/YYYY format) for testing',
        default=None
    )
    parser.add_argument(
        '--no-filter',
        action='store_true',
        help='Skip the native SCRPA RMS filter (load raw data as-is). '
             'Use only for diagnostics; production runs should keep the filter on.'
    )

    args = parser.parse_args()

    # Load data (SCRPA filter applied natively by default)
    print(f"Loading RMS export(s): {len(args.input)} file(s)")
    rms_df = read_rms_exports(args.input, apply_filter=not args.no_filter)
    print(f"  {len(rms_df)} rows loaded after filter + dedupe")

    print(f"Loading cycle calendar: {args.calendar}")
    calendar_df = load_cycle_calendar(Path(args.calendar))
    print(f"  {len(calendar_df)} cycles loaded")

    # Parse dates
    report_due_date = None
    if args.report_date:
        report_due_date = datetime.strptime(args.report_date, '%m/%d/%Y').date()
        print(f"Using report due date: {report_due_date}")

    today = None
    if args.today:
        today = datetime.strptime(args.today, '%m/%d/%Y').date()
        print(f"Using today override: {today}")

    # Transform
    print("Transforming data...")
    enhanced_df = build_all_crimes_enhanced(
        rms_df,
        calendar_df,
        report_due_date=report_due_date,
        today=today
    )

    # Output: single-file run preserves legacy "<stem>_enhanced.csv" naming;
    # multi-file run uses a date-stamped combined name to avoid ambiguity.
    if args.output:
        output_path = args.output
    elif len(args.input) == 1:
        output_path = Path(args.input[0]).stem + '_enhanced.csv'
    else:
        output_path = f"scrpa_combined_{date.today().strftime('%Y_%m_%d')}_enhanced.csv"
    print(f"Saving to: {output_path}")
    enhanced_df.to_csv(output_path, index=False)

    print(f"Done! {len(enhanced_df)} rows written.")

    # Summary
    print("\nPeriod breakdown:")
    print(enhanced_df['Period'].value_counts().to_string())

    print(f"\nLag days: {enhanced_df['IsLagDay'].sum()} incidents")
    print(f"Backfill 7-Day: {enhanced_df['Backfill_7Day'].sum()} incidents")


if __name__ == '__main__':
    main()
