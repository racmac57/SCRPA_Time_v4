# Bi-Weekly SCRPA Report Workflow

**Effective Date:** 2026-02-10  
**Purpose:** Step-by-step guide for generating bi-weekly SCRPA reports

---

## Overview

This workflow runs **every other week** (bi-weekly) to generate crime analysis reports. The entire process is mostly automated, requiring only a few simple steps.

---

## Prerequisites

✅ RMS data exported to: `C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa\`  
✅ Export filename format: `YYYY_MM_DD_HH_MM_SS_SCRPA_RMS.xlsx`

---

## Step-by-Step Workflow

### Step 1: Run the Pipeline (2 minutes)

1. Double-click: `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\scripts\Run_SCRPA_Pipeline.bat`

2. When prompted, enter the **report date** (format: `MM/DD/YYYY`)
   - Example: `02/10/2026`

3. Wait for completion message (creates cycle folder with all data)

**What this does:**
- ✅ Finds latest RMS export automatically
- ✅ Transforms data (Python processing)
- ✅ Generates CSV files in `Data/` folder
- ✅ Creates documentation in `Documentation/` folder
- ✅ Copies Power BI template to cycle folder
- ✅ **Generates fresh HTML report via SCRPA_ArcPy** ⭐ NEW
- ✅ Copies HTML report to `Reports/` folder

**Output location:**
```
Time_Based\2026\26C02W06_26_02_10\
├── 26C02W06_26_02_10.pbix          ← Power BI template
├── Data\
│   ├── SCRPA_All_Crimes_Enhanced.csv
│   ├── SCRPA_7Day_With_LagFlags.csv
│   └── SCRPA_7Day_Summary.yaml
├── Documentation\
│   ├── SCRPA_Report_Summary.md
│   ├── CHATGPT_BRIEFING_PROMPT.md
│   └── EMAIL_TEMPLATE.txt
└── Reports\
    └── SCRPA_Combined_Executive_Summary.html
```

---

### Step 2: Refresh Power BI (1 minute)

1. Navigate to the new cycle folder:
   ```
   Time_Based\2026\26C02W06_26_02_10\
   ```

2. Open: `26C02W06_26_02_10.pbix`

3. Click **Refresh** button (or press `Ctrl+R`)
   - ⚠️ **Important:** The M code now automatically finds the correct data file - **no path editing needed!**

4. Wait for refresh to complete

5. **Verify the data loaded correctly:**
   - Check total record count (bottom right)
   - Expected for cycle `26C02W06_26_02_10`: **252 records**
   - Period breakdown:
     - 7-Day: **2**
     - 28-Day: **11**
     - YTD: **7**
     - Prior Year: **232**

6. Save the PBIX file

**What's New (2026-02-10):**
✨ **No more manual path editing!** The M code automatically detects and loads data from the most recent cycle folder.

---

### Step 3: Review Charts (2 minutes)

Verify all charts display correctly:

✅ **Burglary Auto** - Check for correct 7-Day (RED) and 28-Day (GREEN) bars  
✅ **Burglary - Commercial | Residence**  
✅ **Motor Vehicle Theft**  
✅ **Robbery**  
✅ **Sexual Offenses**  

**Expected color scheme:**
- 🔴 **RED** = 7-Day period incidents (current reporting window)
- 🟢 **GREEN** = 28-Day period incidents (broader context)
- 🔵 **BLUE** = YTD (year-to-date)
- ⚫ **GRAY** = Prior Year (historical comparison)

---

### Step 4: Generate Briefing (Optional - 5 minutes)

If you need the tactical briefing:

1. Open: `Documentation\CHATGPT_BRIEFING_PROMPT.md`
2. Copy entire file contents (`Ctrl+A`, `Ctrl+C`)
3. Paste into ChatGPT
4. Review generated briefing
5. Save/export as needed

---

### Step 5: Send Report (2 minutes)

1. Open: `Documentation\EMAIL_TEMPLATE.txt`
2. Copy email template
3. Attach: `Reports\SCRPA_Combined_Executive_Summary.html`
4. Review and send

---

## Troubleshooting

### Issue: Power BI shows wrong data after refresh

**Symptoms:**
- Chart counts don't match expected values
- Period shows incidents from previous cycles

**Solution:**
The M code should auto-detect the correct path, but if it doesn't:
1. In Power BI, go to **Home** > **Transform Data**
2. Check if the query loaded from the correct cycle folder
3. Look at the "FilePath" step to verify it points to your current cycle

---

### Issue: "File not found" error when refreshing

**Cause:** M code can't find the Data folder

**Solution:**
1. Verify the cycle folder structure is correct:
   ```
   26C02W06_26_02_10/
   ├── 26C02W06_26_02_10.pbix
   └── Data/
       └── SCRPA_All_Crimes_Enhanced.csv
   ```

2. If structure is correct, the PBIX might need to be in the cycle root folder (not a subfolder)

---

### Issue: Map visuals don't show street addresses

**Cause:** Map labels not configured

**Solution:**
1. Click on the map visual
2. In "Visualizations" pane, expand "Data labels"
3. Drag `Clean_Address` field to the labels section

---

### Issue: HTML report shows wrong data

**Symptoms:**
- HTML report incident counts don't match the CSV data
- Report shows data from previous cycle

**Solution:**
This should no longer happen as the pipeline now generates fresh HTML automatically. If you still see this:

1. Check if SCRPA_ArcPy script exists:
   ```
   C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator\RMS_Statistical_Export_FINAL_COMPLETE.py
   ```

2. Look at the pipeline output - you should see:
   ```
   [6a] Generating HTML report via SCRPA_ArcPy...
   ✅ HTML report generated successfully
   ```

3. If generation failed, manually run SCRPA_ArcPy:
   ```bat
   cd C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\SCRPA_ArcPy\05_orchestrator
   set REPORT_DATE=02/10/2026
   python RMS_Statistical_Export_FINAL_COMPLETE.py
   ```

---

## Quick Reference

| Task | Time | Tool/File |
|------|------|-----------|
| Run pipeline | 2 min | `scripts/Run_SCRPA_Pipeline.bat` |
| Refresh Power BI | 1 min | Open PBIX → Click Refresh |
| Verify data | 2 min | Check record count = 252 |
| Review charts | 2 min | Visual inspection |
| Generate briefing | 5 min | ChatGPT + briefing prompt |
| Send report | 2 min | Email template + HTML report |
| **Total** | **~15 min** | |

---

## Changes from Previous Workflow

### What's New (2026-02-10):
✅ **Automatic path detection** - M code now auto-finds the correct data file  
✅ **No manual editing** - Just refresh Power BI, no path changes needed  
✅ **Power BI template auto-copied** - Pipeline now copies template to cycle folder  
✅ **HTML report auto-generated** - Pipeline calls SCRPA_ArcPy to generate fresh HTML with correct data ⭐ NEW  
✅ **Simplified workflow** - Reduced from 7 steps to 5 steps  

### What's Removed:
❌ Manual path editing in Power Query Editor  
❌ Manual template copying  
❌ Path verification step  

---

## Support

**Documentation Location:**
```
Time_Based\2026\26C02W06_26_02_10\Documentation\
```

**Key Files:**
- `SCRPA_Report_Summary.md` - Cycle summary with statistics
- `CHART_VERIFICATION_RESULTS.md` - Data verification results
- `EMAIL_TEMPLATE.txt` - Pre-filled email template

**For issues:** Check the pipeline log or documentation files in the cycle folder.

---

## Version

**Workflow Version:** 2.0  
**Last Updated:** 2026-02-10  
**Breaking Changes:** Automatic path detection (no manual editing needed)
