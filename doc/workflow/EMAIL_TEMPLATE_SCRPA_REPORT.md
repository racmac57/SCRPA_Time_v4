# Email Template for SCRPA Weekly Report

## TextExpander Snippet Setup

**Snippet Name**: `scrpa-report-email`  
**Abbreviation**: `scrpaemail` (or your preferred shortcut)

---

## Email Subject Line

```
SCRPA Weekly Report - Cycle [CYCLE] | [DATE_RANGE]
```

**Example**: `SCRPA Weekly Report - Cycle 26C01W01 | 12/30/2025 - 01/05/2026`

**Alternative (shorter)**: `SCRPA Report - [CYCLE] | [DATE_RANGE]`

---

## Email Body

```
Captain [LAST_NAME],

Please find attached the Strategic Crime Reduction Plan Analysis (SCRPA) Combined Executive Summary for Cycle [CYCLE].

Report Period: [DATE_RANGE]
Date Generated: [GENERATION_DATE]

The report includes:
• 7-Day Executive Summary with detailed incident summaries
• ArcGIS Map visuals showing incidents occurring in the last 7 days
• Statistical charts and visualizations by crime type
• 28-Day Executive Summary (operational planning)
• YTD Executive Summary (strategic analysis)

Please let me know if you have any questions or require additional information.

Respectfully,

P.O. R. A. Carucci
Hackensack Police Department
```

---

## TextExpander Variables

For dynamic content, use TextExpander's built-in date variables or create custom fields:

### Option 1: Manual Placeholders (Replace each week)
- `[CYCLE]` → e.g., `26C01W01`
- `[DATE_RANGE]` → e.g., `12/30/2025 - 01/05/2026`
- `[GENERATION_DATE]` → e.g., `January 6, 2026`
- `[LAST_NAME]` → e.g., `Smith`

### Option 2: TextExpander Date Variables
- `%date%` - Current date
- `%date+1w%` - Date one week from now
- `%time%` - Current time

### Option 3: Custom Fields (Recommended)
Create TextExpander fields that prompt for:
- Cycle (e.g., `26C01W01`)
- Date Range (e.g., `12/30/2025 - 01/05/2026`)
- Generation Date (e.g., `January 6, 2026`)

---

## Shorter Version (Alternative)

If you prefer a more concise email:

```
Captain [LAST_NAME],

Attached is the SCRPA Combined Executive Summary for Cycle [CYCLE] (Report Period: [DATE_RANGE]).

The report includes 7-Day detailed summaries, ArcGIS map visuals, statistical charts, and 28-Day/YTD analysis.

Generated: [GENERATION_DATE]

Please let me know if you have any questions.

Respectfully,

P.O. R. A. Carucci
Hackensack Police Department
```

---

## Usage Instructions

1. **Create the snippet in TextExpander**:
   - Name: `scrpa-report-email`
   - Abbreviation: `scrpaemail` (or your preference)
   - Content: Copy the email body above

2. **Each week when sending**:
   - Type your abbreviation (e.g., `scrpaemail`)
   - TextExpander will expand the template
   - Replace the placeholders `[CYCLE]`, `[DATE_RANGE]`, `[GENERATION_DATE]`, `[LAST_NAME]` with current values
   - Attach the PDF file
   - Send

3. **Optional**: Set up TextExpander fields to prompt for these values automatically

---

## Example (Filled In)

**Subject**: `SCRPA Weekly Report - Cycle 26C01W01 | 12/30/2025 - 01/05/2026`

**Body**:
```
Captain Smith,

Please find attached the Strategic Crime Reduction Plan Analysis (SCRPA) Combined Executive Summary for Cycle 26C01W01.

Report Period: 12/30/2025 - 01/05/2026
Date Generated: January 6, 2026

The report includes:
• 7-Day Executive Summary with detailed incident summaries
• ArcGIS Map visuals showing incidents occurring in the last 7 days
• Statistical charts and visualizations by crime type
• 28-Day Executive Summary (operational planning)
• YTD Executive Summary (strategic analysis)

Please let me know if you have any questions or require additional information.

Respectfully,

P.O. R. A. Carucci
Hackensack Police Department
```

---

**Last Updated**: 2026-01-06  
**Created For**: Weekly SCRPA Report Distribution
