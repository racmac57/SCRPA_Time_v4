# Claude Code Follow-Up: SCRPA Python Transform Edits

**Date:** 2026-01-28  
**Purpose:** Edits to `scripts/scrpa_transform.py` and related outputs based on user review of `m_code/preview_tables/all_crimes/2026_01_28_all_crimes.csv` and reference standards.

---

## 1. Time Column Formatting (Incident Time, Incident Time_Between, Report Time)

**Issue:** Values appear as `0 days 16:40:35` (pandas timedelta/time string) instead of standard time format.

**Reference:**  
- `09_Reference/Standards/RMS/DataDictionary/current/schema/rms_export_field_definitions.md`: IncidentTime type = time; accepted formats = Excel time, HH:mm, H:mm, HH:mm:ss.  
- `09_Reference/Standards/unified_data_dictionary/schemas/rms_fields_schema_latest.json`: Incident Time output_type = time, accepted_formats = excel_time, HH:mm, H:mm.

**Required:**  
- When writing the enriched CSV, **export time columns as HH:mm or HH:mm:ss** (e.g. `16:40:35`), not `0 days 16:40:35`.  
- In `scrpa_transform.py`, before returning the final DataFrame (or in `run_scrpa_pipeline.py` before `to_csv`), convert any time-type columns (e.g. `Incident Time`, `Incident Time_Between`, `Report Time`, `BestTimeValue`) to string in HH:mm:ss (or HH:mm) so CSV output matches RMS/unified_data_dictionary expectations.  
- Keep internal logic using Python `time`/`datetime`; only the serialization to CSV should change.

---

## 2. Zone as Whole Number

**Issue:** Zone should be a whole number (integer).

**Reference:**  
- RMS field definitions: Zone = "integer or text (stored as string in current schema; observed as integer in analysis). Observed range 5–9. If present: must be an integer."

**Required:**  
- In `scrpa_transform.py`, ensure `Zone` is output as integer where possible (coerce numeric, drop decimals). If the source is text (e.g. "7"), convert to int before write.  
- In the final CSV/DataFrame, `Zone` column should be integer type (or string representation of integer with no decimals). Document in data_dictionary that Zone is integer (whole number).

---

## 3. Period Classification: Case 26-009173 (YTD) vs 7-Day

**Context:**  
- User ran pipeline with report date **01/28/2026**.  
- Resolved cycle is **26C01W04** (Report_Due_Date 01/27/2026) with **7-Day window 01/20/2026 – 01/26/2026**.  
- Case **26-009173** has Period = **YTD**.  
- Case **26-008441** has Period = **7-Day**.

**Clarification:**  
- Period is driven by **Incident_Date** and the **current cycle’s fixed 7-Day window** (01/20–01/26 for 26C01W04), not “7 days before the run date.”  
- If 26-009173 has **Incident_Date = 01/27/2026**, then 01/27 is **after** 01/26, so it correctly falls **outside** the 7-Day window and is classified **YTD**.  
- If 26-008441 has Incident_Date within 01/20–01/26, it correctly gets 7-Day.

**Required:**  
- **No change to period logic** if the above is the intended rule (cycle 7-Day window is fixed by calendar).  
- **Optional:** Add a short comment in `scrpa_transform.py` near `classify_period` explaining that 7-Day uses the calendar’s 7_Day_Start/7_Day_End for the resolved cycle, not “today minus 7 days.”  
- If the user instead wants “current 7 days” relative to run date (e.g. 01/21–01/28 when run on 01/28), that would be a **product decision** and would require a different cycle or window definition; document that as an optional enhancement and do not implement unless user confirms.

---

## 4. BestTimeValue Column – Explanation

**User ask:** Explain the values in BestTimeValue.

**Answer to document:**  
- **BestTimeValue** is the single time used for time-of-day analysis.  
- It is the **cascade**: Incident Time → if null, Incident Time_Between → if null, Report Time.  
- So it is “best available time of the incident” (or report time as fallback).  
- It is used to derive `Incident_Time` (HH:MM:SS), `StartOfHour`, `TimeOfDay`, and `TimeOfDay_SortKey`.  
- In CSV output, format BestTimeValue as **HH:mm:ss** (see item 1).

**Required:**  
- Add a brief description of BestTimeValue (and this cascade) to `Documentation/data_dictionary.yaml` and `data_dictionary.json` so it’s clear to readers.

---

## 5. cycle_name and cycle_name_adjusted

**User ask:**  
- Is cycle_name the older version before bi-weekly?  
- What is cycle_name_adjusted? They look like copies of cycle_name.  
- Case 26-009173 has "Historical" for cycle_name and cycle_name_adjusted.

**Clarification:**  
- **cycle_name** = the **weekly** cycle label (e.g. 26C01W02, 26C01W04) from the cycle calendar, based on **Incident_Date**: i.e. the 7-day window that contains the incident date. It is the “Report_Name” from the calendar (weekly style), not the bi-weekly name.  
- **cycle_name_adjusted** = for rows where **Backfill_7Day** is True, use the **current** cycle’s Report_Name (the cycle we’re reporting for); otherwise same as cycle_name. So backfill lag incidents are “attributed” to the current report cycle.  
- If Incident_Date does not fall inside any calendar 7-day window (e.g. 01/27/2026 for 26C01W04, since 7_Day_End is 01/26), `resolve_cycle_for_date` returns None, so cycle_name becomes **"Historical"**. That’s why 26-009173 can show Historical: incident 01/27 is outside the 26C01W04 7-Day window.

**Required:**  
- In `Documentation/data_dictionary.yaml` (and .json), add clear definitions:  
  - **cycle_name:** Weekly cycle (Report_Name) that contains Incident_Date; "Historical" if no such cycle.  
  - **cycle_name_adjusted:** Same as cycle_name except when Backfill_7Day is True, then current cycle’s Report_Name.  
- Optionally add a **BiWeekly_Report_Name** (or similar) column so bi-weekly label (e.g. 26BW02) is visible in the output (see item 7).

---

## 6. Category_Type and Response_Type Not Correct

**Issue:** Category_Type and Response_Type are currently hardcoded to "Unknown" in `scrpa_transform.py` (around lines 995–996).

**Reference:**  
- M code uses a join to **CallTypeCategories** (exact + normalized + fuzzy).  
- Call type reference: `09_Reference/Classifications/CallTypes/CallType_Categories.csv` — columns: Incident, Incident_Norm, Category_Type, Response_Type.

**Required:**  
- Implement **Category_Type** and **Response_Type** lookup in `scrpa_transform.py`:  
  1. Load `CallType_Categories.csv` from `09_Reference/Classifications/CallTypes/` (or a path provided by config).  
  2. Join/lookup on **Incident** (and optionally **Incident_Norm**) against the transform’s incident key (e.g. ALL_INCIDENTS or Incident_Type_1 / IncidentKey).  
  3. Match M code behavior: try exact match on Incident, then Incident_Norm, then optional fuzzy match; populate Category_Type and Response_Type from the lookup table.  
- If the reference file path is configurable, document it (e.g. in PROJECT_SUMMARY or claude.md).

---

## 7. Bi-Weekly Report Name (e.g. 26BW02) in Output

**Issue:** User does not see the bi-weekly report name (e.g. 26BW02) in the output.

**Reference:**  
- Cycle calendar has **BiWeekly_Report_Name** (e.g. 26BW01, 26BW02) for 2026 rows.  
- Path: `09_Reference/Temporal/SCRPA_Cycle/7Day_28Day_Cycle_20260106.csv`.

**Required:**  
- In `scrpa_transform.py`, when resolving the **current** cycle, if the calendar has **BiWeekly_Report_Name**, expose it:  
  - Add a column (e.g. **BiWeekly_Report_Name** or **Cycle_BiWeekly**) to the enriched output, populated with the current cycle’s BiWeekly_Report_Name when available (e.g. 26BW02 for 26C01W04).  
- For rows that use “current cycle” (e.g. for display or reporting), this gives a single bi-weekly label per run.  
- Document the new column in data_dictionary.

---

## 8. cycle_name = "Historical" for 26-009173

**Explanation (for user and docs):**  
- 26-009173 has Incident_Date = **01/27/2026**.  
- Current cycle 26C01W04 has 7-Day window **01/20/2026 – 01/26/2026**.  
- 01/27 is **after** 01/26, so it does not fall in any 7-day window in the calendar for that cycle; the next cycle (26C02W05) starts later.  
- So `resolve_cycle_for_date(01/27/2026)` returns no row → cycle_name = **"Historical"**.  
- This is consistent with the current design: cycle_name is “which 7-day window contains this incident date,” not “which report we’re generating today.”

**Required:**  
- No code change needed; add a note in data_dictionary or claude.md that cycle_name can be "Historical" when Incident_Date falls outside all calendar 7-day windows (e.g. the day after the cycle end).

---

## 9. Reference Paths for Data Types and Classifications

**Reference locations (for implementation and docs):**  
- **RMS field definitions / data types:**  
  `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\RMS\DataDictionary\current\schema\rms_export_field_definitions.md`  
- **Unified data dictionary (schemas, types):**  
  `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary\`  
  - e.g. `schemas/rms_fields_schema_latest.json`  
- **Call type classifications (Category_Type, Response_Type):**  
  `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Classifications\CallTypes\CallType_Categories.csv`

**Required:**  
- Use these paths (or configurable equivalents) when loading CallType_Categories and when documenting types.  
- In PROJECT_SUMMARY or claude.md, add a short “Reference data” section listing these paths and how they are used (RMS types, unified schema, CallTypes).

---

## 10. Summary Checklist for Claude Code

- [ ] **Time formatting:** Export Incident Time, Incident Time_Between, Report Time, and BestTimeValue as HH:mm or HH:mm:ss in CSV (no "0 days" prefix).  
- [ ] **Zone:** Coerce Zone to integer (whole number) in output and document.  
- [ ] **Period:** Leave logic as-is; add comment that 7-Day uses calendar 7_Day_Start/7_Day_End; optionally document “run-date-relative” as future option.  
- [ ] **BestTimeValue:** Document in data_dictionary (cascade + usage).  
- [ ] **cycle_name / cycle_name_adjusted:** Document in data_dictionary; optionally add BiWeekly_Report_Name column (see next).  
- [ ] **BiWeekly_Report_Name:** Add column from cycle calendar to enriched output when present; document.  
- [ ] **Category_Type / Response_Type:** Implement lookup using `09_Reference/Classifications/CallTypes/CallType_Categories.csv` (exact, Incident_Norm, optional fuzzy).  
- [ ] **Historical for 26-009173:** Document why cycle_name can be "Historical" when incident date is outside all 7-day windows.  
- [ ] **Reference paths:** Use RMS and unified_data_dictionary for types; use CallTypes for Category/Response; document in PROJECT_SUMMARY or claude.md.

---

**End of follow-up.**
