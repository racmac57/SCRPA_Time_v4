# SCRPA Documentation Files - What's Needed vs Historical Notes

## Summary

**Only ONE file is needed for ChatGPT:**
- `CHATGPT_BRIEFING_PROMPT.md` - Complete prompt with embedded CSV data

**Data Dictionary is now stored once in reference location:**
- `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\RMS\SCRPA\SCRPA_7Day_Data_Dictionary.md`
- Generated only once, then referenced for all future reports

---

## Files in Documentation Folder

### ✅ **NEEDED - Active Use**

1. **`CHATGPT_BRIEFING_PROMPT.md`**
   - **Purpose**: Complete prompt file for ChatGPT with embedded CSV data
   - **Usage**: Copy entire file and paste into ChatGPT with message: "I need you to generate an HTML tactical briefing report from the crime data below. Please read the complete prompt and CSV data in this file, then generate the HTML output as specified."
   - **Contains**: CSV data summary, complete prompt text, HTML template, column mapping guide
   - **Status**: ✅ **KEEP** - This is the only file you need for ChatGPT

2. **`SCRPA_Report_Summary.md`**
   - **Purpose**: Consolidated summary of the report with CSV file listings and prompt content
   - **Usage**: Quick reference for what files are in this report
   - **Status**: ✅ **KEEP** - Useful for documentation

3. **`SCRPA_7Day_Data_Dictionary.md`** (if copied to Documentation/)
   - **Purpose**: Data dictionary for 7-Day outputs
   - **Usage**: Reference documentation (now stored in `09_Reference\Standards\RMS\SCRPA`)
   - **Status**: ⚠️ **OPTIONAL** - Can be removed from Documentation/ since it's in reference location
   - **Note**: This file is now generated once and stored in the reference location. Future reports will copy from there instead of regenerating.

4. **`README_7day_outputs.md`** (if copied to Documentation/)
   - **Purpose**: Migration notes for 7-Day output changes
   - **Usage**: Reference documentation
   - **Status**: ⚠️ **OPTIONAL** - Can be removed from Documentation/ if not needed

### ❌ **NOT NEEDED - Historical/Development Notes**

These files are historical development notes and can be removed from Documentation/ folder:

1. **`CHATGPT_PROMPT_UPDATE_REVIEW.md`**
   - **Purpose**: Review of ChatGPT prompt updates (December 9, 2025)
   - **Status**: ❌ **REMOVE** - Historical development note

2. **`CYCLE_FIX_PROMPT.md`**
   - **Purpose**: Documentation of cycle fix implementation
   - **Status**: ❌ **REMOVE** - Historical development note

3. **`FIX_PROMPT_AND_REPORTS_FOLDER.md`**
   - **Purpose**: Documentation of fixes to prompt and reports folder issues
   - **Status**: ❌ **REMOVE** - Historical development note

4. **`CSV_RETENTION_AND_PROMPT_FIX.md`**
   - **Purpose**: Documentation of CSV retention and prompt fixes
   - **Status**: ❌ **REMOVE** - Historical development note

5. **`SCRPA_WORKFLOW_USER_GUIDE.md`**
   - **Purpose**: User guide for SCRPA workflow
   - **Status**: ⚠️ **OPTIONAL** - Can be kept if useful, but not needed for report generation
   - **Note**: This is general documentation, not report-specific

6. **`CHATGPT_PROMPT_GUIDE.md`**
   - **Purpose**: Guide for using ChatGPT prompts
   - **Status**: ⚠️ **OPTIONAL** - Can be kept if useful, but not needed for report generation
   - **Note**: This is general documentation, not report-specific

---

## Recommended Documentation Folder Contents

**Minimum (Essential):**
- `CHATGPT_BRIEFING_PROMPT.md` ✅
- `SCRPA_Report_Summary.md` ✅

**Optional (Reference):**
- `SCRPA_7Day_Data_Dictionary.md` (or reference from `09_Reference\Standards\RMS\SCRPA`)
- `README_7day_outputs.md`

**Remove (Historical):**
- `CHATGPT_PROMPT_UPDATE_REVIEW.md`
- `CYCLE_FIX_PROMPT.md`
- `FIX_PROMPT_AND_REPORTS_FOLDER.md`
- `CSV_RETENTION_AND_PROMPT_FIX.md`
- `SCRPA_WORKFLOW_USER_GUIDE.md` (unless you want to keep it)
- `CHATGPT_PROMPT_GUIDE.md` (unless you want to keep it)

---

## Data Dictionary Location

The Data Dictionary is now stored in a reference location and only generated once:

**Reference Location:**
```
C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\RMS\SCRPA\SCRPA_7Day_Data_Dictionary.md
```

**How It Works:**
1. First time: Script generates the dictionary and saves it to the reference location
2. Future runs: Script copies from reference location instead of regenerating
3. Report folder: Dictionary is copied to Documentation/ folder for reference (optional)

This ensures the dictionary is consistent across all reports and doesn't need to be regenerated each time.

---

## ChatGPT Usage

**Simple Workflow:**
1. Open `CHATGPT_BRIEFING_PROMPT.md` from the Documentation/ folder
2. Copy the entire file content
3. Paste into ChatGPT with this message:
   ```
   I need you to generate an HTML tactical briefing report from the crime data below. 
   Please read the complete prompt and CSV data in this file, then generate the HTML output as specified.
   ```
4. ChatGPT will generate the HTML briefing

**That's it!** No need for other files.

