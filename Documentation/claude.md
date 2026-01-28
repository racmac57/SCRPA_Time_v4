# SCRPA Crime Reporting System - Claude AI Specification

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
