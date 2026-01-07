# How to Access VS Code Settings (When Ctrl+Shift+P is Blocked)

## Problem
`Ctrl+Shift+P` opens Perplexity AI instead of VS Code Command Palette (keyboard shortcut conflict).

## Solutions

### Method 1: File Explorer (Easiest)
1. Open File Explorer
2. Navigate to: `C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\.vscode\`
3. Open `settings.json` with VS Code (right-click → Open with → VS Code)

### Method 2: VS Code Menu Bar
1. Click **File** → **Preferences** → **Settings**
2. Click the **{}** icon (top-right) to open JSON view
3. Or: **File** → **Preferences** → **Settings (JSON)**

### Method 3: Direct File Path
1. In VS Code, press `Ctrl+P` (Quick Open)
2. Type: `.vscode/settings.json`
3. Press Enter

### Method 4: Change Perplexity AI Shortcut
If you want to free up `Ctrl+Shift+P`:

1. **Windows Settings**:
   - Press `Win+I`
   - Go to **Apps** → **Advanced app settings** → **App execution aliases**
   - Or search for "Keyboard shortcuts" in Windows Settings

2. **Perplexity AI Settings**:
   - Open Perplexity AI
   - Go to Settings/Preferences
   - Change the keyboard shortcut to something else (e.g., `Ctrl+Shift+Alt+P`)

3. **VS Code Settings**:
   - After freeing up the shortcut, `Ctrl+Shift+P` will work in VS Code

### Method 5: Use VS Code's Settings UI
1. In VS Code: **File** → **Preferences** → **Settings**
2. Search for: `format on save`
3. Uncheck the boxes for:
   - Editor: Format On Save
   - Editor: Format On Paste
   - Editor: Format On Type

### Method 6: Edit Settings via Terminal
1. In VS Code, open terminal: `Ctrl+` ` (backtick)
2. Type: `code .vscode/settings.json`
3. Press Enter

## Quick Reference: Current Settings File

**Location**: 
```
C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA\.vscode\settings.json
```

**Current Content** (should look like this):
```json
{
    "editor.formatOnPaste": false,
    "editor.formatOnSave": false,
    "editor.formatOnType": false,
    "[m]": {
        "editor.formatOnPaste": false,
        "editor.formatOnSave": false,
        "editor.formatOnType": false,
        "editor.defaultFormatter": null
    }
}
```

## Verify Settings Are Working

1. Open any `.m` file
2. Make a small change (add a space)
3. Press `Ctrl+S` to save
4. If the file **does NOT** auto-format, settings are working ✅
5. If it **does** auto-format, you need to:
   - Check for conflicting extensions
   - Reload VS Code window
   - Check file association (bottom-right should say "M")
