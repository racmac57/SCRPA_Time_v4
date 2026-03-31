# SCRPA Scripts Directory

Python-first data transformation scripts for SCRPA crime reporting.

## Architecture

**Python-First Processing**: All data transformations occur in Python. Power BI imports pre-processed CSVs (no complex M code).

```
RMS Export → Python Scripts → Enriched CSVs → Power BI (simple import)
```

## Quick Start

### Full Pipeline
```powershell
# Run entire pipeline with automatic cycle detection
python scripts/run_scrpa_pipeline.py "path/to/rms_export.csv" --report-date 01/27/2026

# Or with custom output directory
python scripts/run_scrpa_pipeline.py "path/to/rms_export.csv" -o "Time_Based/2026/26C01W04_26_01_27"
```

### Individual Scripts
```powershell
# 1. Transform raw RMS data
python scripts/scrpa_transform.py input.csv -o Data/SCRPA_All_Crimes_Enhanced.csv --report-date 01/27/2026

# 2. Generate 7-day filtered outputs
python scripts/prepare_7day_outputs.py Data/SCRPA_All_Crimes_Enhanced.csv -o Data/

# 3. Generate documentation
python scripts/generate_documentation.py -o Documentation/ --cycle-name 26C01W04 --biweekly 26BW02

# 4. Validate against M code reference
python scripts/validate_parity.py python_output.csv reference.csv
```

## Scripts

### `scrpa_transform.py` - Core Transformation
Main data transformation engine matching `All_Crimes.m` logic exactly.

**Features**:
- 3-tier cycle resolution (Report_Due_Date → In-cycle → Most recent)
- LagDays = CycleStart_7Day - Incident_Date (not Report_Date - Incident_Date)
- Period classification: 7-Day → Prior Year → 28-Day → YTD → Historical
- Crime category, TimeOfDay, vehicle formatting, etc.

**Usage**:
```powershell
python scripts/scrpa_transform.py input.csv -o output.csv --report-date MM/DD/YYYY
```

### `prepare_7day_outputs.py` - 7-Day Filtering
Generates filtered datasets and lag day metadata.

**Outputs**:
- `SCRPA_7Day_With_LagFlags.csv` - IsCurrent7DayCycle=TRUE
- `SCRPA_7Day_Lag_Only.csv` - Backfill_7Day=TRUE
- `SCRPA_7Day_Summary.yaml/json` - Lag statistics

### `generate_documentation.py` - Documentation Generator
Creates structured documentation.

**Outputs**:
- `data_dictionary.yaml/json` - Field definitions
- `PROJECT_SUMMARY.yaml/json` - System overview
- `claude.md` - AI specification
- `SCRPA_Report_Summary.md` - Report template

### `run_scrpa_pipeline.py` - Orchestration
Main entry point running entire pipeline.

**Output Structure**:
```
Time_Based/2026/26C01W04_26_01_27/
├── Data/
│   ├── SCRPA_All_Crimes_Enhanced.csv
│   ├── SCRPA_7Day_With_LagFlags.csv
│   ├── SCRPA_7Day_Lag_Only.csv
│   └── SCRPA_7Day_Summary.yaml/json
├── Documentation/
│   ├── data_dictionary.yaml/json
│   ├── PROJECT_SUMMARY.yaml/json
│   ├── claude.md
│   └── EMAIL_TEMPLATE.txt
└── Reports/
```

### `validate_parity.py` - Validation
Validates Python output against M code reference.

**Checks**:
- Row count match
- Period classification
- LagDays calculation
- IsLagDay/Backfill_7Day logic
- Crime_Category, TimeOfDay

### `export_enriched_data_and_email.py` - Email Template
Generates bi-weekly email templates with correct date ranges.

**Bi-Weekly Periods**:
- 26BW01 (01/13/2026): 12/30/2025 - 01/12/2026
- 26BW02 (01/27/2026): 01/13/2026 - 01/26/2026

## Requirements

```bash
pip install pandas pyyaml openpyxl
```

## Validation Results (01/27/2026)

```
Python vs M Code (200 common cases):
✓ Row Count: PASSED
✓ Period Classification: PASSED
✓ LagDays Calculation: PASSED
✓ IsLagDay Values: PASSED
✓ Backfill_7Day Logic: PASSED
✓ TimeOfDay: PASSED
✓ Crime_Category: PASSED
Overall: 10/10 checks PASSED
```

---
**Last Updated**: 2026-01-28
