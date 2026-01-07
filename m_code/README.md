# M Code - Active Queries

This directory contains the **current, active Power BI M code queries** used in the SCRPA reporting workflow.

## Active Queries

### Staging Queries (Disable Load: Yes)
- **`q_RMS_Source.m`** - Loads latest Excel file from RMS export folder
- **`q_CycleCalendar.m`** - Loads cycle calendar CSV (7-Day/28-Day cycles)
- **`q_CallTypeCategories.m`** - Loads call type category mapping CSV

### Main Query
- **`all_crimes.m`** - Main transformation query that processes RMS data with all enhancements

## Usage

These files are reference copies of the M code used in Power BI Desktop. When making changes:
1. Update the query in Power BI Desktop Advanced Editor
2. Copy the updated M code to the corresponding `.m` file here
3. Commit changes to version control

## File Paths

All file paths in these queries use absolute paths. Ensure paths are:
- Single continuous strings (no line breaks)
- Updated if source file locations change
