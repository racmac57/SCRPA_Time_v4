# Skill: generate_cycle_report

## Purpose
Generate the full SCRPA Combined Executive Summary HTML report directly from cycle data files. This skill replaces the ChatGPT report generation workflow entirely.

---

## Tone & Detail Rules (Read Before Starting)

- Write synopses in **plain law enforcement language** — factual, direct, past tense
- Include **specific times, addresses, and actions** — do not generalize or sanitize
- **Do not redact** — this report is for command staff (Patrol Commander), not public release
- Tactical notes must be **operationally specific**: include time-of-day patterns, grid/zone references if present in data, suspect status, and recommended patrol actions
- Match the **detail level of a detective briefing**, not a press release
- If an incident has no tactical implication, say so briefly — do not pad

---

## Prerequisites

All 4 validation skills must pass before this skill runs:
- `check_cycle_calendar.md` ✅
- `check_period_logic.md` ✅
- `validate_cycle_output.md` ✅
- `check_lag_logic.md` ✅

---

## Input Files

Resolve `{CYCLE_FOLDER}` to the current cycle path before reading:

```
{CYCLE_FOLDER}\Documentation\CHATGPT_BRIEFING_PROMPT.md → role and context
{CYCLE_FOLDER}\Documentation\CHATGPT_SESSION_PROMPT.md → task instructions
{CYCLE_FOLDER}\Documentation\HPD_REPORT_STYLE_BLOCK.md → HTML styling
{CYCLE_FOLDER}\Documentation\SCRPA_Report_Summary.md → summary data
{CYCLE_FOLDER}\Data\SCRPA_All_Crimes_Enhanced.csv → incident-level data
```

---

## Execution Steps

### Step 1 — Load and confirm input files
Read all 5 files. Confirm each loaded successfully.

**HPD style block fallback:** If `{CYCLE_FOLDER}\Documentation\HPD_REPORT_STYLE_BLOCK.md` does not exist, fall back to:
`C:\Users\carucci_r\OneDrive - City of Hackensack\08_Templates\Report_Styles\html\HPD_Report_Style_Prompt.md`

If neither file exists, STOP and report:
"HPD_REPORT_STYLE_BLOCK.md not found in cycle folder or template directory. Run the pipeline to regenerate, or verify 08_Templates path."

For all other files, if any is missing, STOP and report which file is absent.

### Step 2 — Parse role and task instructions
- Read `CHATGPT_BRIEFING_PROMPT.md` as your assigned role and operational context
- Read `CHATGPT_SESSION_PROMPT.md` as your task instructions
- Follow both exactly — do not skip or reinterpret sections

### Step 3 — Extract cycle metadata from SCRPA_Report_Summary.md
Confirm and record:
- Cycle name (e.g., 26BW06)
- 7-Day window start and end
- Bi-Weekly window start and end
- Report due date
- Total incidents, period breakdown, lag count, backfill count

### Step 4 — Build 7-Day Incident Highlights table

Filter `SCRPA_All_Crimes_Enhanced.csv` for `Period == '7-Day'` rows only.

For each incident write:
- **Category** — use the crime category field
- **Incident Date** — formatted MM/DD/YYYY
- **Synopsis** — 3-5 sentences, factual, specific, past tense. Include time, location, victim actions, suspect actions, officer response, and case disposition. Do not redact. Do not generalize.
- **Tactical Note** — 2-3 sentences. Include: time-of-day pattern, location/grid if available, suspect status, recommended patrol focus. If no tactical implication exists, state: "No immediate patrol implication — investigation ongoing."

If 0 rows exist for `Period == '7-Day'`:
- Insert one row: "No incidents reported in the 7-day window for this cycle."
- Add a note: "Early-cycle run — window opens [7_Day_Start]. Re-run on report due date for complete data."

### Step 5 — Apply HPD styling
- Embed the full contents of `HPD_REPORT_STYLE_BLOCK.md` into the HTML `<head>` as a `<style>` block
- Do not link to external stylesheets
- Apply HPD class names exactly as defined in the style block

### Step 6 — Assemble full HTML report
Follow the structure defined in `CHATGPT_SESSION_PROMPT.md` exactly.
Include all sections the session prompt requires (executive summary, stats tables, incident highlights, footer).
Footer must include:
```
Hackensack Police Department - Safe Streets Operations Control Center | Cycle: {cycle} | Range: 7-Day: {start} - {end} | Bi-Weekly: {bw_start} - {bw_end} | Version: 1.0
```

### Step 7 — Save output
Write the final HTML to:
```
{CYCLE_FOLDER}\Reports\SCRPA_Claude_Report.html
```
Confirm file written. Report file size in KB.

---

## Output Format

```
generate_cycle_report — RESULT
Cycle: [cycle name]
7-Day Window: [start] - [end]
7-Day Incidents in report: [count]
Output file: [full path]
File size: [KB]
Status: COMPLETE ✅
```

If any step fails, output:
```
Status: FAILED ❌
Step: [step number]
Reason: [specific error]
```
