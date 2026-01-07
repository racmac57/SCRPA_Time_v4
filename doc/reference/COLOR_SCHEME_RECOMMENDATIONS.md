# Period Color Scheme - Final Implementation

**Date**: 2026-01-06  
**Status**: ✅ Implemented

## Final Color Assignments

- **7-Day**: (existing color - unchanged)
- **28-Day**: `#77C99A` ✅ (green - unchanged)
- **Prior Year**: `#7F92A2` ✅ (gray-blue - chosen)
- **YTD**: `#118DFF` ✅ (blue - moved from Prior Year)

**Note**: Prior Year color changed from `#118DFF` to `#7F92A2` (gray-blue). YTD now uses `#118DFF` (blue) that Prior Year previously used.

---

## Implementation Details

### Color Rationale
- **Prior Year** (`#7F92A2`): Gray-blue provides subtle distinction for prior year data
- **YTD** (`#118DFF`): Blue emphasizes current year data
- **28-Day** (`#77C99A`): Green remains consistent for 28-day period
- **7-Day**: Existing color maintained

### Where to Apply
Update these colors in all Power BI visuals that use the `Period` column:
- Bar charts (Burglary, Motor Vehicle Theft, etc.)
- Column charts
- Any visual with Period as legend/category
- Conditional formatting (if used)

---

## Historical Options (Reference Only)

**Rationale**: Prior Year already has a color that works (`#118DFF`). Give YTD a distinct, professional color.

### Color Assignments:
- **7-Day**: (keep existing)
- **28-Day**: `#77C99A` ✅ (keep - green)
- **Prior Year**: `#118DFF` ✅ (keep - blue)
- **YTD**: `#FF6B35` (orange/coral) or `#F7931E` (orange)

**Pros**:
- Minimal changes (only YTD color changes)
- Blue for "past" (Prior Year) is intuitive
- Orange/Yellow for "current" (YTD) is attention-grabbing

**Cons**:
- Orange might clash with green depending on chart type

---

## Option 2: Swap Colors - Prior Year Gets New Color, YTD Gets Blue

**Rationale**: YTD is more important, so it should get the more prominent blue color.

### Color Assignments:
- **7-Day**: (keep existing)
- **28-Day**: `#77C99A` ✅ (keep - green)
- **Prior Year**: `#9B9B9B` (gray) or `#A0A0A0` (light gray)
- **YTD**: `#118DFF` ✅ (blue - move from Prior Year)

**Pros**:
- Blue for current year (YTD) is more prominent
- Gray for prior year is subtle/background

**Cons**:
- Requires changing Prior Year color in all visuals
- Gray might be too subtle

---

## Option 3: Professional Color Palette

**Rationale**: Use a cohesive color scheme that works well together.

### Color Assignments:
- **7-Day**: (keep existing)
- **28-Day**: `#77C99A` ✅ (keep - green)
- **Prior Year**: `#6C757D` (gray-blue) or `#95A5A6` (blue-gray)
- **YTD**: `#3498DB` (bright blue) or `#2E86AB` (blue)

**Pros**:
- Cohesive palette
- Good contrast between all periods

**Cons**:
- Requires changing both Prior Year and YTD colors

---

---

## Quick Reference

**Copy-paste hex codes for Power BI**:
```
7-Day:     (existing - unchanged)
28-Day:    #77C99A
Prior Year: #7F92A2
YTD:       #118DFF
```

**Power BI Formatting Steps**:
1. Select visual → Format pane
2. Find "Data colors" or "Legend" section
3. Click color next to each Period value
4. Enter hex code (with or without #)
5. Repeat for all visuals using Period column
