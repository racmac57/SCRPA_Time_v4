# SCRPA Lag Types: Quick Reference Card

---

## Two Types of "Lag" in SCRPA Reporting

### 🔴 Type 1: REPORTING LAG (Delay-Based)
**Definition**: Time delay between when incident occurred and when it was reported

**Measured By**: `IncidentToReportDays > 0`

**Example**:
```
Incident Date: 02/03/2026
Report Date:   02/08/2026
Reporting Lag: 5 days
```

**Used In JSON Fields**:
- `counts.lag_incidents`
- `lag_analysis.by_crime_category`
- `lag_analysis.lagdays_distribution`
- `7day_by_crime_category[].LagDayCount`

**What It Tells Us**: How quickly incidents are being reported after they occur

---

### 🔵 Type 2: BACKFILL LAG (Cycle-Based)
**Definition**: Incidents that occurred BEFORE the current cycle but were reported DURING the cycle

**Marked By**: `Backfill_7Day = True`

**Example**:
```
Incident Date:  01/20/2026  (before cycle start)
Report Date:    02/08/2026  (during current cycle)
Cycle Dates:    02/03 - 02/09
Backfill Lag:   TRUE
```

**Used In JSON Fields**:
- `counts.backfill_7day`

**What It Tells Us**: How many "late-reported" incidents from prior periods are appearing in the current cycle

---

## Side-by-Side Comparison

| Aspect | Reporting Lag | Backfill Lag |
|--------|---------------|--------------|
| **Definition** | Delay between incident & report | Incident before cycle, reported in cycle |
| **Filter** | `IncidentToReportDays > 0` | `Backfill_7Day = True` |
| **Period** | Period = '7-Day' | Period ≠ '7-Day' (usually '28-Day') |
| **When Incident Occurred** | During current cycle | Before current cycle |
| **When Report Filed** | During current cycle | During current cycle |
| **DataFrame** | `df_7day_period_only` | `df_lag_only` |

---

## Example Dataset: Cycle 26C02W06 (02/03-02/09)

| Case | Incident Date | Report Date | Days | Period | Backfill | Reporting Lag? | Backfill Lag? |
|------|---------------|-------------|------|--------|----------|----------------|---------------|
| 26-012829 | 02/03/2026 | 02/08/2026 | 5 | 7-Day | False | ✅ YES (5 days) | ❌ NO |
| 26-012181 | 02/05/2026 | 02/06/2026 | 1 | 7-Day | False | ✅ YES (1 day) | ❌ NO |
| (backfill) | 01/20/2026 | 02/08/2026 | 19 | 28-Day | True | ❌ NO (not in period) | ✅ YES |

**Result**:
- Reporting Lag Count: **2** (both 7-Day incidents have delays)
- Backfill Lag Count: **1** (one incident from prior cycle)

---

## Common Pitfalls ⚠️

### ❌ DON'T: Use `df_lag_only` for reporting lag analysis
```python
# WRONG:
lag_by_category = df_lag_only['Crime_Category'].value_counts()
```
This counts **backfill** incidents, not reporting delays!

### ✅ DO: Filter 7-Day period and check IncidentToReportDays
```python
# CORRECT:
df_7day_period_only = df_7day[df_7day['Period'] == '7-Day']
lag_incidents = df_7day_period_only[df_7day_period_only['IncidentToReportDays'] > 0]
lag_by_category = lag_incidents['Crime_Category'].value_counts()
```

---

### ❌ DON'T: Mix the two types
```python
# WRONG:
'lag_incidents': len(df_lag_only),  # Counts backfill
```

### ✅ DO: Use the correct filter for each
```python
# CORRECT:
'lag_incidents': len(df_7day[(df_7day['Period'] == '7-Day') & 
                             (df_7day['IncidentToReportDays'] > 0)]),  # Counts reporting delay
'backfill_7day': len(df_lag_only),  # Counts backfill
```

---

## When to Use Each

### Use REPORTING LAG when analyzing:
- ✅ How quickly incidents are being reported
- ✅ Average time delay between incident and report
- ✅ Crime categories with longest reporting delays
- ✅ Trends in reporting speed over time

### Use BACKFILL LAG when analyzing:
- ✅ How many "old" incidents are appearing in current reports
- ✅ Data completeness and historical adjustments
- ✅ Cross-cycle incident tracking
- ✅ Understanding total workload (current + backfill)

---

## Key Takeaway

**Both are important, but they measure different things:**

- **Reporting Lag** = "How fast are incidents reported?" (process efficiency)
- **Backfill Lag** = "How many old incidents are showing up now?" (data completeness)

Don't confuse them! 🎯

---

**Reference**: `doc/BUG_FIX_SUMMARY_PREPARE_7DAY_OUTPUTS.md`  
**Related**: `doc/JSON_VALIDATION_FINDINGS_26C02W06.md`
