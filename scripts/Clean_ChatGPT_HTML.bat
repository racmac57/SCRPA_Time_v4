@echo off
title Clean ChatGPT HTML Artifacts
setlocal EnableDelayedExpansion

set "SCRPA_ROOT=C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA"
set "PYTHON_SCRIPT=%SCRPA_ROOT%\scripts\clean_chatgpt_html.py"

echo.
echo Clean ChatGPT HTML Artifacts
echo ─────────────────────────────────────────────
echo Removes: ``` code fences, ChatGPT citation comments
echo.

REM ── If a file was dragged onto the .bat, clean just that file
if not "%~1"=="" (
    echo Target: %~1
    echo.
    python "%PYTHON_SCRIPT%" "%~1"
    goto :done
)

REM ── Otherwise prompt for a path (file or folder)
set /p TARGET="Drag a .html file here, or type a folder path (Enter for Reports folder): "

if "!TARGET!"=="" (
    set "TARGET=%SCRPA_ROOT%\Time_Based"
    echo Using default: !TARGET!
)

REM ── Strip surrounding quotes if user dragged a file
set "TARGET=!TARGET:"=!"

if not exist "!TARGET!" (
    echo ERROR: Path not found: !TARGET!
    goto :done
)

echo.
python "%PYTHON_SCRIPT%" "!TARGET!"

:done
echo.
pause
