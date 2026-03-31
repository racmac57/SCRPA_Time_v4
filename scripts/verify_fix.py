"""Validate SCRPA cycle output - all 7 checks + regression."""
import pandas as pd
import json
import re
import sys

CYCLE_DIR = 'Time_Based/2026/26C03W12_26_03_24'
ENHANCED = f'{CYCLE_DIR}/Data/SCRPA_All_Crimes_Enhanced.csv'
SEVENDAY = f'{CYCLE_DIR}/Data/SCRPA_7Day_With_LagFlags.csv'
SUMMARY_JSON = f'{CYCLE_DIR}/Data/SCRPA_7Day_Summary.json'
REPORT_MD = f'{CYCLE_DIR}/Documentation/SCRPA_Report_Summary.md'

results = {}

# Load data
df_enh = pd.read_csv(ENHANCED, low_memory=False)
df_7d = pd.read_csv(SEVENDAY, low_memory=False)
with open(SUMMARY_JSON) as f:
    js = json.load(f)
with open(REPORT_MD) as f:
    md_text = f.read()

# CHECK 1: Row count
total_md = int(re.search(r'Total Incidents\s*\|\s*(\d+)', md_text).group(1))
row_count = len(df_enh)
c1 = row_count == total_md
tag1 = "PASS=1" if c1 else "FAIL=0"
results[1] = (c1, 'CSV={}, MD={}'.format(row_count, total_md))
print('CHECK 1 Row Count: {} | CSV rows={}, Report_Summary Total={}'.format(tag1, row_count, total_md))

# CHECK 2: Period sum
period_counts = df_enh['Period'].value_counts().to_dict()
s7 = period_counts.get('7-Day', 0)
s28 = period_counts.get('28-Day', 0)
sytd = period_counts.get('YTD', 0)
spy = period_counts.get('Prior Year', 0)
shist = period_counts.get('Historical', 0)
period_sum = s7 + s28 + sytd + spy
c2 = period_sum == row_count
tag2 = "PASS=1" if c2 else "FAIL=0"
detail2 = '7-Day({})+28-Day({})+YTD({})+PriorYear({})={} vs Total({}), Historical={}'.format(s7, s28, sytd, spy, period_sum, row_count, shist)
results[2] = (c2, detail2)
print('CHECK 2 Period Sum: {} | {}'.format(tag2, detail2))

# Check MD period values match CSV
md_7d_val = int(re.search(r'7-Day Period\s*\|\s*(\d+)', md_text).group(1))
md_28d_val = int(re.search(r'28-Day Period\s*\|\s*(\d+)', md_text).group(1))
md_ytd_m = re.search(r'YTD\s*\|\s*(\d+)', md_text)
md_ytd_val = int(md_ytd_m.group(1)) if md_ytd_m else -1
md_py_m = re.search(r'Prior Year\s*\|\s*(\d+)', md_text)
md_py_val = int(md_py_m.group(1)) if md_py_m else -1
md_match = (s7 == md_7d_val and s28 == md_28d_val and sytd == md_ytd_val and spy == md_py_val)
print('  Period vs MD: CSV 7-Day={}/MD={}, CSV 28-Day={}/MD={}, CSV YTD={}/MD={}, CSV PY={}/MD={} => {}'.format(
    s7, md_7d_val, s28, md_28d_val, sytd, md_ytd_val, spy, md_py_val, "MATCH" if md_match else "MISMATCH"))

# CHECK 3: 7-Day CSV integrity
if 'IsCurrent7DayCycle' in df_7d.columns:
    violations = df_7d[df_7d['IsCurrent7DayCycle'] != True]
    c3 = len(violations) == 0
    tag3 = "PASS=1" if c3 else "FAIL=0"
    results[3] = (c3, '{} rows, {} violations'.format(len(df_7d), len(violations)))
    print('CHECK 3 7-Day CSV Filter: {} | {} rows, {} violations'.format(tag3, len(df_7d), len(violations)))
else:
    print('CHECK 3 7-Day CSV Filter: FAIL=0 | IsCurrent7DayCycle column missing')
    results[3] = (False, 'column missing')

# CHECK 4: Backfill subset of IsLagDay
bf_rows = df_enh[df_enh['Backfill_7Day'] == True]
if len(bf_rows) > 0:
    violations4 = bf_rows[bf_rows['IsLagDay'] != True]
    c4 = len(violations4) == 0
    detail4 = '{} backfill rows, {} violations'.format(len(bf_rows), len(violations4))
else:
    c4 = True
    detail4 = '0 backfill rows (vacuously true)'
tag4 = "PASS=1" if c4 else "FAIL=0"
results[4] = (c4, detail4)
print('CHECK 4 Backfill subset IsLagDay: {} | {}'.format(tag4, detail4))

# CHECK 5: LagDays spot-check
lag_rows = df_enh[df_enh['IsLagDay'] == True].head(5)
if len(lag_rows) == 0:
    print('CHECK 5 LagDays Spot-Check: PASS=1 | No IsLagDay=True rows to check')
    results[5] = (True, 'No lag rows')
else:
    mismatches = []
    for idx, row in lag_rows.iterrows():
        ld = row.get('LagDays', None)
        case_num = row.get('Case Number', 'unknown')
        if pd.notna(ld) and ld <= 0:
            mismatches.append('{}: LagDays={} (should be >0)'.format(case_num, ld))
    c5 = len(mismatches) == 0
    detail5 = 'Checked {} rows, {} issues'.format(len(lag_rows), len(mismatches))
    if mismatches:
        detail5 += ': ' + '; '.join(mismatches)
    tag5 = "PASS=1" if c5 else "FAIL=0"
    results[5] = (c5, detail5)
    print('CHECK 5 LagDays Spot-Check: {} | {}'.format(tag5, detail5))

# CHECK 6: JSON/CSV alignment
json_total_7d = js['counts'].get('total_7day_window', js['counts'].get('total_7day', 0))
csv_7d_rows = len(df_7d)
json_lag = js['counts'].get('lag_incidents', 0)
csv_lag_in_7d = len(df_7d[df_7d['Backfill_7Day'] == True]) if 'Backfill_7Day' in df_7d.columns else -1
json_bf = js['counts'].get('backfill_7day', js['counts'].get('backfill_count', 0))
csv_bf_enh = len(df_enh[df_enh['Backfill_7Day'] == True])

c6a = json_total_7d == csv_7d_rows
c6b = json_lag == csv_lag_in_7d
c6c = json_bf == csv_bf_enh
lag_dist = js.get('lag_analysis', {}).get('lagdays_distribution', {})
c6d = True
if lag_dist:
    mn = lag_dist.get('mean', 0)
    md_v = lag_dist.get('median', 0)
    mx = lag_dist.get('max', 0)
    c6d = mn >= 0 and md_v >= 0 and mx >= md_v
c6 = c6a and c6b and c6c and c6d
detail6 = 'JSON total_7day={} vs CSV={}, JSON lag={} vs CSV_7d_backfill={}, JSON bf={} vs CSV_enh_bf={}'.format(
    json_total_7d, csv_7d_rows, json_lag, csv_lag_in_7d, json_bf, csv_bf_enh)
tag6 = "PASS=1" if c6 else "FAIL=0"
results[6] = (c6, detail6)
print('CHECK 6 JSON/CSV Alignment: {} | {}'.format(tag6, detail6))

# CHECK 7: Report Summary alignment
md_lag_m2 = re.search(r'Lag Incidents\s*\|\s*(\d+)', md_text)
md_lag_val2 = int(md_lag_m2.group(1)) if md_lag_m2 else -1
c7a = md_lag_val2 == json_lag

# 7-Day column sum in crime category breakdown
cat_lines = re.findall(r'\|\s*([^|]+)\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', md_text)
cat_7d_sum = sum(int(m[1]) for m in cat_lines if m[0].strip() not in ('Category', 'Metric', 'Field'))
c7b = cat_7d_sum == s7

c7 = c7a and c7b
detail7 = 'MD lag={} vs JSON lag={}, Category 7-Day sum={} vs period 7-Day={}'.format(md_lag_val2, json_lag, cat_7d_sum, s7)
tag7 = "PASS=1" if c7 else "FAIL=0"
results[7] = (c7, detail7)
print('CHECK 7 Report Summary: {} | {}'.format(tag7, detail7))

# REGRESSION CHECKS
print()
print('--- REGRESSION CHECKS ---')
bf_in_7day = df_enh[(df_enh['Backfill_7Day'] == True) & (df_enh['Period'] == '7-Day')]
print('REGRESSION v2.0.0 backfill-in-7Day: {} rows (should be 0)'.format(len(bf_in_7day)))

if 'LagDays' in df_enh.columns and 'IncidentToReportDays' in df_enh.columns:
    lag_pos = df_enh[(df_enh['IsLagDay'] == True) & (df_enh['LagDays'] > 0)]
    if len(lag_pos) > 0:
        confused = lag_pos[lag_pos['LagDays'] == lag_pos['IncidentToReportDays']]
        print('REGRESSION v2.0.0 LagDays==IncidentToReportDays: {}/{} (suspicious if >0)'.format(len(confused), len(lag_pos)))
    else:
        print('REGRESSION v2.0.0 LagDays==ITRD: No lag rows with LagDays>0 to check')

hist_rows = df_enh[df_enh['Period'] == 'Historical']
print('REGRESSION Historical exclusion: {} rows (excluded from period sum)'.format(len(hist_rows)))

required_cols = ['Report_Date_ForLagday', 'IsCurrent7DayCycle', 'Backfill_7Day', 'IsLagDay',
                 'LagDays', 'Period', 'IncidentToReportDays', 'Crime_Category', 'Incident_Date_Date']
missing = [c for c in required_cols if c not in df_enh.columns]
print('REGRESSION Required columns: {}'.format("None missing" if not missing else missing))

print()
total_pass = sum(1 for k, v in results.items() if v[0])
print('RESULT: {}/7 PASSED'.format(total_pass))
for k in sorted(results.keys()):
    v = results[k]
    tag = "PASS=1" if v[0] else "FAIL=0"
    print('  Check {}: {} | {}'.format(k, tag, v[1]))
