# SCRPA Data Flow Diagrams

## Current Architecture (BROKEN)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RMS EXPORT (Excel)                               │
│                  Single Source of Raw Data                          │
│                                                                     │
│  Content: Incident records from RMS database                        │
│  Format: .xlsx                                                      │
│  Location: 05_EXPORTS\_RMS\scrpa\                                  │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           │ (Read by TWO separate systems)
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│  SYSTEM 1: Python Pipeline│   │  SYSTEM 2: SCRPA_ArcPy    │
│  (16_Reports/SCRPA/)      │   │  (02_ETL_Scripts/)        │
├───────────────────────────┤   ├───────────────────────────┤
│                           │   │                           │
│ ┌─────────────────────┐   │   │ ┌─────────────────────┐   │
│ │ scrpa_transform.py  │   │   │ │ RMS_Statistical_    │   │
│ │                     │   │   │ │ Export_FINAL.py     │   │
│ │ Logic:              │   │   │ │                     │   │
│ │ - Cycle calendar    │   │   │ │ Logic:              │   │
│ │ - Fixed 7-day window│   │   │ │ - Rolling window    │   │
│ │ - Period = 7-Day if │   │   │ │ - Period = 7-Day if │   │
│ │   incident in       │   │   │ │   today - date <= 7 │   │
│ │   02/03-02/09       │   │   │ │                     │   │
│ └─────────────────────┘   │   │ └─────────────────────┘   │
│            ↓              │   │            ↓              │
│ ┌─────────────────────┐   │   │ ┌─────────────────────┐   │
│ │ Enhanced CSV        │   │   │ │ HTML Report         │   │
│ │ - Period            │   │   │ │ (Embedded data)     │   │
│ │ - Crime_Category    │   │   │ │                     │   │
│ │ - LagDays           │   │   │ │ Stored in:          │   │
│ │ - IsLagDay          │   │   │ │ 06_Output/          │   │
│ │                     │   │   │ │                     │   │
│ │ ✅ CORRECT DATA     │   │   │ │ ⚠️ MAY BE STALE     │   │
│ └─────────────────────┘   │   │ └─────────────────────┘   │
│            ↓              │   │            │              │
│ ┌─────────────────────┐   │   │            │              │
│ │ prepare_7day_       │   │   │            │              │
│ │ outputs.py          │   │   │            │              │
│ │                     │   │   │            │              │
│ │ Filters to          │   │   │            │              │
│ │ IsCurrent7DayCycle  │   │   │            │              │
│ └─────────────────────┘   │   │            │              │
│            ↓              │   │            │              │
│ ┌─────────────────────┐   │   │            │              │
│ │ JSON Summary        │   │   │            │              │
│ │ - 7-Day stats       │   │   │            │              │
│ │ - Lag analysis      │   │   │            │              │
│ │ ✅ CORRECT DATA     │   │   │            │              │
│ └─────────────────────┘   │   │            │              │
└───────────────────────────┘   └────────────┼──────────────┘
                │                            │
                │                            │
                │ ┌──────────────────────────┘
                │ │ (Pipeline tries to call System 2)
                │ │ (Often fails or doesn't run)
                │ │
                ▼ ▼
        ┌────────────────────────────────────────┐
        │  _copy_scrpa_reports_to_cycle()        │
        │                                        │
        │  Searches: 06_Output/*.html            │
        │  Finds: Latest by timestamp            │
        │  ❌ NO VALIDATION OF CYCLE             │
        │  ❌ COPIES STALE HTML                  │
        └────────────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────┐
        │  patch_scrpa_combined_exec_summary_    │
        │  after_copy()                          │
        │                                        │
        │  ✅ Patches: Header pills              │
        │  ❌ Does NOT patch: Data tables        │
        └────────────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────────┐
        │  FINAL OUTPUT                          │
        ├────────────────────────────────────────┤
        │  Data/                                 │
        │  ├─ CSV ✅ (Correct: 02/10 data)       │
        │  └─ JSON ✅ (Correct: 02/10 data)      │
        │                                        │
        │  Documentation/                        │
        │  └─ MD ✅ (Correct: 02/10 metadata)    │
        │                                        │
        │  Reports/                              │
        │  └─ HTML ❌ (Wrong: 01/27 data,        │
        │             02/10 headers)             │
        └────────────────────────────────────────┘

KEY PROBLEMS:
❌ TWO separate transformation systems (inconsistent logic)
❌ HTML generation NOT integrated into pipeline
❌ No validation that HTML matches current cycle
❌ Silent failure when HTML generation doesn't work
❌ Only header patching (data tables unchanged)
```

---

## Proposed Architecture (FIXED - Option 3)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RMS EXPORT (Excel)                               │
│                  Single Source of Raw Data                          │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           │ (Read by ONE system only)
                           ▼
┌───────────────────────────────────────────────────────────────────┐
│  SYSTEM 1: Python Pipeline (SINGLE SOURCE OF TRUTH)               │
│  (16_Reports/SCRPA/)                                              │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │ scrpa_transform.py (Master Transformation Engine)       │     │
│  │                                                         │     │
│  │ Logic:                                                  │     │
│  │ - Cycle calendar-based                                  │     │
│  │ - Fixed 7-day window from calendar                      │     │
│  │ - Period classification (7-Day, 28-Day, YTD, etc.)     │     │
│  │ - Lag calculation (cycle-based)                         │     │
│  │ - Backfill detection                                    │     │
│  └─────────────────────────────────────────────────────────┘     │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ SCRPA_All_Crimes_Enhanced.csv                            │    │
│  │ (CANONICAL DATA SOURCE)                                  │    │
│  │                                                          │    │
│  │ Contains:                                                │    │
│  │ - All raw RMS fields                                     │    │
│  │ - Enriched: Period, Crime_Category, LagDays, etc.      │    │
│  │ - Single transformation, guaranteed consistency         │    │
│  └──────────────────────────────────────────────────────────┘    │
│                    ↓            ↓            ↓                    │
│         ┌──────────┴────────┐   │   ┌────────┴──────────┐        │
│         ▼                   │   │   │                   ▼        │
│  ┌─────────────────┐        │   │   │        ┌─────────────────┐│
│  │ prepare_7day_   │        │   │   │        │ SCRPA_ArcPy     ││
│  │ outputs.py      │        │   │   │        │ (Modified)      ││
│  │                 │        │   │   │        │                 ││
│  │ Reads CSV       │        │   │   │        │ NEW: Reads CSV  ││
│  │ (not RMS!)      │        │   │   │        │ (not RMS!)      ││
│  └─────────────────┘        │   │   │        └─────────────────┘│
│         ↓                   │   │   │                ↓           │
│  ┌─────────────────┐        │   │   │        ┌─────────────────┐│
│  │ JSON Summary    │        │   │   │        │ HTML Report     ││
│  │ ✅ Correct      │        │   │   │        │ ✅ Correct      ││
│  └─────────────────┘        │   │   │        │ (Uses CSV data) ││
│                             │   │   │        └─────────────────┘│
│                             │   │   │                ↓           │
│                             │   │   │        ┌─────────────────┐│
│                             │   │   │        │ Saves to        ││
│                             │   │   │        │ 06_Output/      ││
│                             │   │   │        └─────────────────┘│
│                             │   │   │                │           │
│                             │   │   └────────────────┘           │
│                             │   │   (Automatically invoked)       │
│                             │   │                                │
│                             ▼   ▼                                │
│                  ┌──────────────────────┐                        │
│                  │ Copy HTML to         │                        │
│                  │ cycle Reports/       │                        │
│                  │                      │                        │
│                  │ ✅ Always fresh      │                        │
│                  │ ✅ Data matches CSV  │                        │
│                  └──────────────────────┘                        │
│                             ↓                                    │
│                  ┌──────────────────────┐                        │
│                  │ Patch headers        │                        │
│                  │ (cycle info)         │                        │
│                  └──────────────────────┘                        │
└───────────────────────────────────────────────────────────────────┘
                             ↓
        ┌────────────────────────────────────────┐
        │  FINAL OUTPUT (ALL CORRECT)            │
        ├────────────────────────────────────────┤
        │  Data/                                 │
        │  ├─ CSV ✅ (Master source)             │
        │  └─ JSON ✅ (Derived from CSV)         │
        │                                        │
        │  Documentation/                        │
        │  └─ MD ✅ (Derived from CSV)           │
        │                                        │
        │  Reports/                              │
        │  └─ HTML ✅ (Derived from CSV)         │
        │                                        │
        │  ALL FILES GUARANTEED CONSISTENT       │
        └────────────────────────────────────────┘

KEY IMPROVEMENTS:
✅ SINGLE transformation engine (consistent logic)
✅ CSV is canonical source for ALL outputs
✅ SCRPA_ArcPy reads CSV instead of raw RMS
✅ HTML automatically generated with correct data
✅ No validation needed (guaranteed consistency)
✅ No silent failures (integrated pipeline)
```

---

## Proposed Architecture (OPTIMAL - Option 4)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RMS EXPORT (Excel)                               │
│                  Single Source of Raw Data                          │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           │ (Read by unified pipeline)
                           ▼
┌───────────────────────────────────────────────────────────────────┐
│  UNIFIED PYTHON PIPELINE (COMPLETE SOLUTION)                      │
│  (16_Reports/SCRPA/)                                              │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │ Step 1: scrpa_transform.py                              │     │
│  │ Master transformation: RMS → Enhanced CSV               │     │
│  └─────────────────────────────────────────────────────────┘     │
│                              ↓                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ SCRPA_All_Crimes_Enhanced.csv (CANONICAL)               │    │
│  └──────────────────────────────────────────────────────────┘    │
│                    ↓            ↓            ↓                    │
│         ┌──────────┴────────┐   │   ┌────────┴──────────┐        │
│         ▼                   ▼   ▼   ▼                   ▼        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐       │
│  │ Step 2:      │  │ Step 3:      │  │ Step 4: NEW      │       │
│  │ prepare_7day │  │ generate_    │  │ generate_html_   │       │
│  │ _outputs.py  │  │ documenta-   │  │ report.py        │       │
│  │              │  │ tion.py      │  │                  │       │
│  │ CSV → JSON   │  │ CSV → MD     │  │ CSV → HTML       │       │
│  └──────────────┘  └──────────────┘  └──────────────────┘       │
│         ↓                   ↓                   ↓                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐       │
│  │ JSON Summary │  │ Report       │  │ HTML Executive   │       │
│  │              │  │ Summary MD   │  │ Summary          │       │
│  │ ✅ Correct   │  │              │  │                  │       │
│  │              │  │ ✅ Correct   │  │ ✅ Correct       │       │
│  └──────────────┘  └──────────────┘  └──────────────────┘       │
│                                                                   │
│  ALL OUTPUTS GENERATED IN SINGLE PIPELINE RUN                    │
│  ALL OUTPUTS DERIVED FROM SAME CSV → GUARANTEED CONSISTENCY      │
│  NO EXTERNAL DEPENDENCIES (no SCRPA_ArcPy subprocess)            │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                             ↓
        ┌────────────────────────────────────────┐
        │  FINAL OUTPUT (PERFECT CONSISTENCY)    │
        ├────────────────────────────────────────┤
        │  Time_Based/2026/26C02W06_26_02_10/    │
        │                                        │
        │  Data/                                 │
        │  ├─ SCRPA_All_Crimes_Enhanced.csv ✅   │
        │  └─ SCRPA_7Day_Summary.json ✅         │
        │                                        │
        │  Documentation/                        │
        │  ├─ SCRPA_Report_Summary.md ✅         │
        │  └─ EMAIL_TEMPLATE.txt ✅              │
        │                                        │
        │  Reports/                              │
        │  └─ SCRPA_Combined_Executive_          │
        │     Summary.html ✅                    │
        │                                        │
        │  ✅ Single pipeline run                │
        │  ✅ All files consistent               │
        │  ✅ No external dependencies           │
        │  ✅ No subprocess calls                │
        │  ✅ No file copying                    │
        │  ✅ Automatic error detection          │
        └────────────────────────────────────────┘

KEY ADVANTAGES:
✅ SINGLE codebase (easiest maintenance)
✅ Native HTML generation (no subprocess)
✅ Atomic operation (all outputs or none)
✅ Impossible for outputs to be inconsistent
✅ Simplest debugging (single call stack)
✅ Fastest execution (no external process overhead)
```

---

## Timeline Comparison

### Current (Broken) System

```
Day 1 (01/27/2026):
  - SCRPA_ArcPy runs manually → Generates HTML for 26BW03
  - HTML saved to 06_Output/

Day 14 (02/10/2026):
  - Python pipeline runs → CSV/JSON for 26C02W06 ✅
  - Pipeline tries to call SCRPA_ArcPy → FAILS ❌
  - Pipeline copies HTML from 06_Output → Gets 01/27 file ❌
  - Result: Mismatched data!
```

### Fixed System (Option 3 or 4)

```
Day 14 (02/10/2026):
  - Python pipeline runs
  - Generates CSV ✅
  - Generates JSON ✅
  - Generates HTML (from CSV) ✅
  - All files consistent!

Every cycle:
  - Single pipeline run
  - All outputs always match
  - No manual steps
```

---

## Data Flow Validation Points

### Where Validation Happens (Option 3)

```
┌─────────────────┐
│ RMS Export      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ scrpa_transform.py      │
│ ✅ VALIDATION:          │
│ - Date parsing          │
│ - Cycle resolution      │
│ - Period classification │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Enhanced CSV (Master)   │
│ ✅ CANONICAL DATA       │
└────────┬───────┬────────┘
         │       │
         ▼       ▼
┌──────────┐ ┌─────────────┐
│ JSON     │ │ SCRPA_ArcPy │
│          │ │ (reads CSV) │
└──────────┘ └──────┬──────┘
                    │
                    ▼
              ┌──────────────┐
              │ HTML         │
              │ ✅ MATCH     │
              │ (from CSV)   │
              └──────────────┘

Validation: CSV = JSON = HTML (all from same source)
```

---

## Error Scenarios

### Current System: Silent Failure

```
SCRPA_ArcPy generation fails
         ↓
Pipeline prints warning
         ↓
Pipeline continues anyway
         ↓
Copies stale HTML
         ↓
❌ Wrong data in reports
```

### Fixed System: Fail-Fast

```
HTML generation fails
         ↓
Pipeline detects failure
         ↓
Pipeline STOPS with error
         ↓
User alerted immediately
         ↓
✅ No wrong data distributed
```

Or with Option 4:

```
HTML generation fails
         ↓
Same process as CSV generation
         ↓
Exception raised
         ↓
Transaction rolled back
         ↓
✅ Atomic: all outputs or none
```
