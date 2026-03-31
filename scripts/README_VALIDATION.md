# SCRPA 7-Day JSON Validation Script

## Overview

`validate_7day_json.py` is an automated validation script that catches JSON/CSV mismatches in SCRPA reporting cycles. It validates all critical fields in `SCRPA_7Day_Summary.json` against the source `SCRPA_All_Crimes_Enhanced.csv` data.

## Purpose

This script was created to prevent data mismatches like those documented in `JSON_VALIDATION_FINDINGS_26C02W06.md`, specifically:

- **Error #1**: `lag_incidents` counting backfill incidents instead of reporting delays
- **Error #2**: `lag_by_category` missing categories due to wrong data source
- **Error #3**: `incident_date_range` showing backfill dates instead of 7-Day period dates

## What It Validates

The script validates 9 critical fields:

| Field | Description | Common Issues |
|-------|-------------|---------------|
| `total_all_crimes` | Total records in CSV | Should match CSV row count |
| `incidents_in_7day_period` | Count where Period='7-Day' | Should exclude backfill |
| `lag_incidents` | Incidents with IncidentToReportDays > 0 | Often confused with backfill count |
| `backfill_7day` | Count where Backfill_7Day=True | Incidents before cycle, reported during |
| `total_7day_window` | Sum of 7-Day + backfill | Should equal incidents_in_7day_period + backfill_7day |
| `lag_by_category` | Reporting delays by crime type | Should only count 7-Day period with delay |
| `lagdays_distribution` | Min, max, mean, median of delays | Statistics for IncidentToReportDays > 0 |
| `7day_by_crime_category` | Full breakdown with lag counts | LagDayCount + TotalCount per category |
| `incident_date_range` | Earliest/latest incident dates | Should be 7-Day period only, not backfill |

## Key Distinctions

The script understands two types of "lag":

### Reporting Lag (What Should Be Counted)
- **Definition**: Delay between incident date and report date
- **Calculation**: `IncidentToReportDays > 0`
- **Scope**: 7-Day period incidents only (`Period='7-Day'`)
- **Example**: Incident on 02/03, reported on 02/08 = 5 days lag

### Backfill Lag (What Should NOT Be Counted)
- **Definition**: Incidents from before the cycle, reported during the cycle
- **Calculation**: `Backfill_7Day=True`
- **Scope**: Incidents from 28-Day or earlier periods
- **Example**: Incident on 01/20 (28-Day period), reported in 7-Day window

**The bug**: The original code counted backfill lag instead of reporting lag.

## Usage

### Basic Usage

```bash
# Validate latest cycle automatically
python validate_7day_json.py --latest

# Validate specific cycle by name
python validate_7day_json.py --cycle 26C02W06_26_02_10

# Validate with custom file paths
python validate_7day_json.py --csv path/to/SCRPA_All_Crimes_Enhanced.csv --json path/to/SCRPA_7Day_Summary.json

# Verbose output (shows load details)
python validate_7day_json.py --latest -v
```

### Integration with Pipeline

Add to the end of `run_scrpa_pipeline.py`:

```python
# After Step 6 (reports generation)
print(f"\n[7/7] Validating JSON outputs...")
validation_result = subprocess.run(
    [sys.executable, SCRIPT_DIR / 'validate_7day_json.py', 
     '--csv', str(enhanced_csv),
     '--json', str(json_summary)],
    capture_output=True,
    text=True
)

if validation_result.returncode != 0:
    print("  ⚠️  JSON validation failed - check output for details")
    print(validation_result.stdout)
else:
    print("  ✅ JSON validation passed")
```

### CI/CD Integration

```yaml
# .github/workflows/validate-cycle.yml
- name: Validate SCRPA JSON
  run: |
    python scripts/validate_7day_json.py --latest
  continue-on-error: false  # Fail build if validation fails
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All validations passed |
| `1` | One or more validations failed |
| `2` | File not found or other error |

## Output Format

### Success Output
```
Auto-detected cycle: 26C02W06_26_02_10
Running validation...

======================================================================
SCRPA 7-Day JSON Validation Report
======================================================================

Files:
  CSV: .../Data/SCRPA_All_Crimes_Enhanced.csv
  JSON: .../Data/SCRPA_7Day_Summary.json
  Timestamp: 2026-02-10T13:45:23.688006

Validation Results:
  ✓ [PASS] total_all_crimes
      total_all_crimes: 252 ✓
  ✓ [PASS] incidents_in_7day_period
      incidents_in_7day_period: 2 ✓
  ✓ [PASS] lag_incidents
      lag_incidents: 2 ✓
  ✓ [PASS] backfill_7day
      backfill_7day: 1 ✓
  ✓ [PASS] total_7day_window
      total_7day_window: 3 ✓
  ✓ [PASS] lag_by_category
      lag_by_category: 2 categories ✓
  ✓ [PASS] lagdays_distribution
      lagdays_distribution: min=1, max=5, mean=3.0, median=3 ✓
  ✓ [PASS] 7day_by_crime_category
      7day_by_crime_category: 2 categories + TOTAL ✓
  ✓ [PASS] incident_date_range
      incident_date_range: 2026-02-03 to 2026-02-05 ✓

======================================================================
✓ ALL VALIDATIONS PASSED (9/9)
======================================================================
```

### Failure Output
```
Validation Results:
  ✗ [FAIL] lag_incidents
      lag_incidents: Expected 2, got 1 (JSON shows backfill count 1, not reporting lag count 2)
  ✗ [FAIL] lag_by_category
      lag_by_category: Missing categories: {'Burglary - Comm & Res'}
  ✗ [FAIL] incident_date_range
      incident_date_range: earliest: expected 2026-02-03 (7-Day period), got 2026-01-20 (includes backfill)

======================================================================
✗ VALIDATIONS FAILED (3/9 failures)
======================================================================
```

## When to Use

### Manual Validation
- After running the pipeline for a new cycle
- Before finalizing reports for distribution
- When debugging data discrepancies
- After fixing bugs in `prepare_7day_outputs.py`

### Automated Validation
- As final step in `run_scrpa_pipeline.py`
- In CI/CD pipeline for pull requests
- In scheduled data quality checks
- Before archiving cycle data

## Testing the Fixes

To verify that the bug fixes in `prepare_7day_outputs.py` are working:

### Before Fixes (Expected to FAIL)
```bash
# Check out code before fixes
git checkout <commit-before-fixes>

# Run pipeline
python run_scrpa_pipeline.py input.csv --report-date 02/10/2026

# Run validation (should FAIL)
python validate_7day_json.py --latest
# Expected failures:
# - lag_incidents: Expected 2, got 1
# - lag_by_category: Missing categories
# - incident_date_range: showing backfill date
```

### After Fixes (Expected to PASS)
```bash
# Check out code with fixes
git checkout <commit-with-fixes>

# Run pipeline
python run_scrpa_pipeline.py input.csv --report-date 02/10/2026

# Run validation (should PASS)
python validate_7day_json.py --latest
# Expected: ✓ ALL VALIDATIONS PASSED (9/9)
```

## Technical Details

### Data Sources
- **CSV**: `SCRPA_All_Crimes_Enhanced.csv` - Full enriched data with all periods
- **JSON**: `SCRPA_7Day_Summary.json` - Summary metadata for 7-Day reporting

### Key Columns Used
- `Period` - Which reporting period ('7-Day', '28-Day', 'YTD', 'Prior Year')
- `Backfill_7Day` - Boolean flag for backfill incidents
- `IncidentToReportDays` - Delay between incident and report (reporting lag)
- `Crime_Category` - Crime type for category breakdowns
- `Incident_Date_Date` - Date of incident occurrence

### Validation Logic
Each validator function:
1. Filters CSV data appropriately (7-Day period only, not backfill)
2. Calculates expected value from CSV
3. Extracts actual value from JSON
4. Compares and returns (passed: bool, message: str)

### Color Output
Terminal output uses ANSI color codes:
- 🟢 Green: PASS
- 🔴 Red: FAIL
- 🔵 Blue: Info
- 🟡 Yellow: Warning

Colors are automatically disabled when not running in a TTY (e.g., in CI logs).

## Maintenance

### Adding New Validations
To add a new validation check:

1. Create a new validator function:
```python
def validate_new_field(csv_df: pd.DataFrame, json_data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate new_field."""
    # Calculate expected from CSV
    expected = ...
    
    # Get actual from JSON
    actual = json_data.get('new_field')
    
    # Compare and return
    if expected == actual:
        return True, f"new_field: {actual} ✓"
    else:
        return False, f"new_field: Expected {expected}, got {actual}"
```

2. Add to validations list in `validate_cycle()`:
```python
validations = [
    # ... existing validations ...
    ('new_field', validate_new_field),
]
```

### Updating for Schema Changes
If JSON schema changes:
1. Update validator functions to match new structure
2. Update documentation in this README
3. Test with both old and new data formats if needed

## Troubleshooting

### "Cycle folder not found"
- Check cycle name format: `26C02W06_26_02_10`
- Verify folder exists in `Time_Based/YYYY/`
- Ensure `Data/` subdirectory exists

### "CSV/JSON file not found"
- Check that pipeline completed successfully
- Verify files exist: `SCRPA_All_Crimes_Enhanced.csv`, `SCRPA_7Day_Summary.json`
- Check file permissions

### "Missing required columns"
- Verify CSV has all enrichment columns from `scrpa_transform.py`
- Check for column name changes in pipeline
- Ensure CSV isn't corrupted or truncated

### All Validations Failing
- Check if you're using old JSON format (before bug fixes)
- Verify CSV and JSON are from same cycle
- Re-run pipeline to regenerate files

## Related Documentation

- `JSON_VALIDATION_FINDINGS_26C02W06.md` - Original bug report that prompted this script
- `prepare_7day_outputs.py` - Script that generates the JSON being validated
- `run_scrpa_pipeline.py` - Main pipeline that can integrate this validator

## Version History

- **v1.0.0** (2026-02-10): Initial release
  - Validates 9 critical fields
  - Catches lag_incidents bug (Error #1)
  - Catches lag_by_category bug (Error #2)
  - Catches incident_date_range bug (Error #3)
  - Colorized terminal output
  - Supports --latest, --cycle, and custom paths

## Author

R. A. Carucci (with AI assistance)  
Created: 2026-02-10  
Purpose: Automated validation to prevent JSON/CSV mismatches in future cycles
