# Workflow Script Location Analysis

## Current Structure

### Script Locations
- **Main Workflow**: `02_ETL_Scripts\Run_SCRPA_Report_Folder.bat`
- **Enriched Data Export**: `16_Reports\SCRPA\export_enriched_data.bat`
- **Other ETL Scripts**: `02_ETL_Scripts\SCRPA\` (generate_weekly_report.py, organize_report_files.py, etc.)

### Considerations

#### Option 1: Keep Current Structure (Recommended)
**Keep `Run_SCRPA_Report_Folder.bat` in `02_ETL_Scripts\`**

**Pros**:
- ✅ Logical separation: ETL/processing scripts in `02_ETL_Scripts\`, report outputs in `16_Reports\SCRPA\`
- ✅ Matches existing structure where other workflow scripts are
- ✅ `02_ETL_Scripts\` is the standard location for automation scripts
- ✅ No need to update path references in the batch file
- ✅ Clear separation between "processing" and "output" directories

**Cons**:
- ⚠️ Two different locations for related scripts (but this is actually good organization)

#### Option 2: Move to `16_Reports\SCRPA\`
**Move `Run_SCRPA_Report_Folder.bat` to `16_Reports\SCRPA\`**

**Pros**:
- ✅ All SCRPA-related scripts in one place
- ✅ Easier to find everything SCRPA-related

**Cons**:
- ❌ Breaks logical separation (ETL scripts vs. report outputs)
- ❌ Would need to update all path references in the batch file
- ❌ `02_ETL_Scripts\` is the standard location for automation/workflow scripts
- ❌ Other ETL scripts it calls are still in `02_ETL_Scripts\SCRPA\`

---

## Recommendation

**Keep `Run_SCRPA_Report_Folder.bat` in `02_ETL_Scripts\`**

### Reasoning:
1. **Logical Organization**: 
   - `02_ETL_Scripts\` = Processing/Automation scripts
   - `16_Reports\SCRPA\` = Report outputs and report-specific utilities

2. **Path References**: 
   - The batch file likely references scripts in `02_ETL_Scripts\SCRPA\`
   - Moving it would require updating all relative paths

3. **Standard Practice**: 
   - ETL/automation scripts typically live in a dedicated scripts directory
   - Report outputs live in a reports directory

4. **Separation of Concerns**:
   - Workflow orchestration (ETL) ≠ Report utilities (output processing)
   - `export_enriched_data.bat` is a post-processing utility for reports
   - `Run_SCRPA_Report_Folder.bat` is the main workflow orchestrator

---

## Alternative: Create a Shortcut

If you want easier access, create a shortcut in `16_Reports\SCRPA\` that points to the batch file:

```batch
REM Create shortcut script in 16_Reports\SCRPA\
@echo off
call "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\Run_SCRPA_Report_Folder.bat"
```

This gives you:
- ✅ Easy access from report directory
- ✅ Maintains logical file organization
- ✅ No path updates needed

---

## Final Structure (Recommended)

```
02_ETL_Scripts\
├── Run_SCRPA_Report_Folder.bat          ← Main workflow (stays here)
└── SCRPA\
    ├── generate_weekly_report.py
    ├── organize_report_files.py
    └── ...

16_Reports\SCRPA\
├── export_enriched_data.bat             ← Report utility (stays here)
├── export_enriched_data_and_email.py
└── Time_Based\
    └── ...
```

---

**Date**: 2026-01-06  
**Recommendation**: Keep current structure, maintain logical separation
