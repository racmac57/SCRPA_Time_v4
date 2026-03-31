"""Cycle Calendar Validator — binary PASS=1/FAIL=0 for each check."""
import csv
from datetime import datetime, timedelta
import re
import os

CSV_PATH = os.path.join(
    "C:/Users/carucci_r/OneDrive - City of Hackensack",
    "09_Reference/Temporal/SCRPA_Cycle/7Day_28Day_Cycle_20260106.csv"
)

# Load CSV
rows = []
with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    actual_columns = list(reader.fieldnames)
    for r in reader:
        rows.append(r)

print(f"Total rows: {len(rows)}")
print(f"Columns found: {actual_columns}")


def parse_date(s):
    if not s or not s.strip():
        return None
    return datetime.strptime(s.strip(), "%m/%d/%Y")


REQUIRED_COLS = [
    'Report_Due_Date', '7_Day_Start', '7_Day_End',
    '28_Day_Start', '28_Day_End', 'Report_Name', 'BiWeekly_Report_Name'
]

# ============ CHECK 1: Required columns ============
missing_cols = [c for c in REQUIRED_COLS if c not in actual_columns]
c1_pass = len(missing_cols) == 0
print(f"\nCheck 1 - Required Columns: {'PASS=1' if c1_pass else 'FAIL=0'}")
if missing_cols:
    print(f"  Missing: {missing_cols}")
else:
    print(f"  All 7 required columns present")

# Parse all rows with dates
parsed = []
for i, r in enumerate(rows):
    try:
        p = {
            'row': i + 2,
            'Report_Due_Date': parse_date(r['Report_Due_Date']),
            '7_Day_Start': parse_date(r['7_Day_Start']),
            '7_Day_End': parse_date(r['7_Day_End']),
            '28_Day_Start': parse_date(r['28_Day_Start']),
            '28_Day_End': parse_date(r['28_Day_End']),
            'Report_Name': r.get('Report_Name', ''),
            'BiWeekly_Report_Name': r.get('BiWeekly_Report_Name', '').strip(),
        }
        parsed.append(p)
    except Exception as e:
        print(f"  Parse error row {i+2}: {e}")

# Filter 2026 rows: 7_Day_End year is 2026
rows_2026 = [p for p in parsed if p['7_Day_End'] and p['7_Day_End'].year == 2026]
print(f"\n2026 rows (7_Day_End in 2026): {len(rows_2026)}")

# Sort by 7_Day_Start
rows_2026.sort(key=lambda x: x['7_Day_Start'])

# ============ CHECK 2: 7-Day coverage (no gaps) ============
gaps = []
for i in range(len(rows_2026) - 1):
    end_cur = rows_2026[i]['7_Day_End']
    start_next = rows_2026[i + 1]['7_Day_Start']
    expected_next = end_cur + timedelta(days=1)
    if start_next != expected_next:
        gap_start = end_cur + timedelta(days=1)
        gap_end = start_next - timedelta(days=1)
        gaps.append((
            gap_start.strftime("%m/%d/%Y"),
            gap_end.strftime("%m/%d/%Y"),
            rows_2026[i]['Report_Name'],
            rows_2026[i + 1]['Report_Name']
        ))

c2_pass = len(gaps) == 0
print(f"\nCheck 2 - 7-Day Coverage (no gaps): {'PASS=1' if c2_pass else 'FAIL=0'}")
if gaps:
    print(f"  {len(gaps)} gap(s) found:")
    for g in gaps:
        print(f"    Gap: {g[0]} to {g[1]} (between {g[2]} and {g[3]})")
else:
    print(f"  No gaps - continuous coverage for {len(rows_2026)} rows")

# ============ CHECK 3: No overlapping 7-Day windows ============
overlaps = []
for i in range(len(rows_2026)):
    for j in range(i + 1, len(rows_2026)):
        s1, e1 = rows_2026[i]['7_Day_Start'], rows_2026[i]['7_Day_End']
        s2, e2 = rows_2026[j]['7_Day_Start'], rows_2026[j]['7_Day_End']
        if s1 <= e2 and s2 <= e1:
            overlaps.append((
                rows_2026[i]['Report_Name'],
                rows_2026[j]['Report_Name']
            ))

c3_pass = len(overlaps) == 0
print(f"\nCheck 3 - No Overlapping 7-Day Windows: {'PASS=1' if c3_pass else 'FAIL=0'}")
if overlaps:
    print(f"  {len(overlaps)} overlap(s): {overlaps}")
else:
    print(f"  No overlaps found")

# ============ CHECK 4: 28-Day consistency ============
inconsistent_28 = []
for p in rows_2026:
    if p['28_Day_End'] != p['7_Day_End']:
        inconsistent_28.append((
            p['Report_Name'], '28_Day_End mismatch',
            p['28_Day_End'].strftime("%m/%d/%Y"),
            p['7_Day_End'].strftime("%m/%d/%Y")
        ))
    expected_28_start = p['7_Day_Start'] - timedelta(days=21)
    if p['28_Day_Start'] != expected_28_start:
        inconsistent_28.append((
            p['Report_Name'], '28_Day_Start mismatch',
            p['28_Day_Start'].strftime("%m/%d/%Y"),
            expected_28_start.strftime("%m/%d/%Y")
        ))

c4_pass = len(inconsistent_28) == 0
print(f"\nCheck 4 - 28-Day Consistency: {'PASS=1' if c4_pass else 'FAIL=0'}")
if inconsistent_28:
    print(f"  {len(inconsistent_28)} inconsistency(ies):")
    for inc in inconsistent_28:
        print(f"    {inc[0]}: {inc[1]} (got {inc[2]}, expected {inc[3]})")
else:
    print(f"  All 28-day windows consistent with 7-day windows")

# ============ CHECK 5: BiWeekly_Report_Name completeness ============
bw_names = [p['BiWeekly_Report_Name'] for p in rows_2026
            if p['BiWeekly_Report_Name']]
bw_format_ok = all(re.match(r'^\d{2}BW\d{2}$', n) for n in bw_names)
bw_bad = [n for n in bw_names if not re.match(r'^\d{2}BW\d{2}$', n)]

c5_pass = len(bw_names) == 26 and bw_format_ok
print(f"\nCheck 5 - BiWeekly_Report_Name Completeness: {'PASS=1' if c5_pass else 'FAIL=0'}")
print(f"  {len(bw_names)}/26 bi-weekly names present")
print(f"  Format: {'All match YYBW## pattern' if bw_format_ok else f'Bad formats: {bw_bad}'}")
if bw_names:
    print(f"  Range: {bw_names[0]} to {bw_names[-1]}")

# ============ CHECK 6: Report_Due_Date sequencing ============
rdd_issues = []
for i in range(len(rows_2026) - 1):
    d1 = rows_2026[i]['Report_Due_Date']
    d2 = rows_2026[i + 1]['Report_Due_Date']
    if d2 <= d1:
        rdd_issues.append(
            f"Not monotonic: {d1.strftime('%m/%d')} >= {d2.strftime('%m/%d')}"
        )
    diff = (d2 - d1).days
    if diff != 14:
        rdd_issues.append(
            f"Spacing {diff}d (expected 14) between "
            f"{rows_2026[i]['Report_Name']} and {rows_2026[i+1]['Report_Name']}"
        )

is_monotonic = all(
    rows_2026[i + 1]['Report_Due_Date'] > rows_2026[i]['Report_Due_Date']
    for i in range(len(rows_2026) - 1)
)
spacings = [
    (rows_2026[i + 1]['Report_Due_Date'] - rows_2026[i]['Report_Due_Date']).days
    for i in range(len(rows_2026) - 1)
]
unique_spacings = set(spacings)

c6_pass = is_monotonic and len(rdd_issues) == 0
print(f"\nCheck 6 - Report_Due_Date Sequencing: {'PASS=1' if c6_pass else 'FAIL=0'}")
print(f"  Monotonic: {is_monotonic}")
print(f"  Spacings: {unique_spacings} days")
if rdd_issues:
    for issue in rdd_issues[:5]:
        print(f"    {issue}")

# ============ CHECK 7: Cycle count ============
weekly_count_2026 = len(rows_2026)
bw_count_2026 = len(bw_names)

c7_pass = bw_count_2026 == 26
print(f"\nCheck 7 - Cycle Count: {'PASS=1' if c7_pass else 'FAIL=0'}")
print(f"  Total 2026 rows: {weekly_count_2026}")
print(f"  Bi-weekly entries: {bw_count_2026}/26")

# ============ REGRESSION: v1.9.1 gap check ============
test_date = datetime(2026, 1, 6)
covered = any(
    p['7_Day_Start'] <= test_date <= p['7_Day_End'] for p in parsed
)
print(f"\nRegression - v1.9.1 (01/06/2026 coverage): {'PASS=1' if covered else 'FAIL=0'}")
if covered:
    covering = [
        p for p in parsed
        if p['7_Day_Start'] <= test_date <= p['7_Day_End']
    ]
    print(
        f"  01/06/2026 covered by: {covering[0]['Report_Name']} "
        f"({covering[0]['7_Day_Start'].strftime('%m/%d/%Y')} - "
        f"{covering[0]['7_Day_End'].strftime('%m/%d/%Y')})"
    )
else:
    print(
        "  WARNING: 01/06/2026 falls outside all 7-day windows "
        "- Tier 2 resolution would fail!"
    )

# ============ SUMMARY ============
all_checks = [c1_pass, c2_pass, c3_pass, c4_pass, c5_pass, c6_pass, c7_pass]
passed = sum(all_checks)
print(f"\n{'='*60}")
print(f"SUMMARY: {passed}/7 checks passed")
print(f"Check 1 (Required Columns):    {'PASS=1' if c1_pass else 'FAIL=0'}")
print(f"Check 2 (7-Day Coverage):       {'PASS=1' if c2_pass else 'FAIL=0'}")
print(f"Check 3 (No Overlaps):          {'PASS=1' if c3_pass else 'FAIL=0'}")
print(f"Check 4 (28-Day Consistency):   {'PASS=1' if c4_pass else 'FAIL=0'}")
print(f"Check 5 (BiWeekly Names):       {'PASS=1' if c5_pass else 'FAIL=0'}")
print(f"Check 6 (Report_Due Sequence):  {'PASS=1' if c6_pass else 'FAIL=0'}")
print(f"Check 7 (Cycle Count):          {'PASS=1' if c7_pass else 'FAIL=0'}")
print(f"Regression (v1.9.1):            {'PASS=1' if covered else 'FAIL=0'}")
print(f"{'='*60}")
