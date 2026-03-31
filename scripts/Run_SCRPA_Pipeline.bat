@echo off
title SCRPA Pipeline - Enter Report Date
setlocal EnableDelayedExpansion

REM Script and project paths (run from any location)
set "SCRPA_ROOT=C:\Users\carucci_r\OneDrive - City of Hackensack\16_Reports\SCRPA"
set "PYTHON_SCRIPT=%SCRPA_ROOT%\scripts\run_scrpa_pipeline.py"
REM Folder where watchdog drops timestamped RMS exports
set "RMS_DIR=C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS\_RMS\scrpa"

if not exist "%PYTHON_SCRIPT%" (
    echo ERROR: Pipeline script not found.
    echo   %PYTHON_SCRIPT%
    pause
    exit /b 1
)

if not exist "%RMS_DIR%" (
    echo ERROR: RMS export folder not found.
    echo   %RMS_DIR%
    pause
    exit /b 1
)

REM Use latest .xlsx in RMS folder (by date)
set "LATEST_XLSX="
for /f "delims=" %%F in ('dir /b /o-d "%RMS_DIR%\*.xlsx" 2^>nul') do (
    set "LATEST_XLSX=%RMS_DIR%\%%F"
    goto :found
)
:found
if not defined LATEST_XLSX (
    echo ERROR: No .xlsx file found in %RMS_DIR%
    pause
    exit /b 1
)

echo.
echo SCRPA Pipeline
echo --------------
echo RMS file: !LATEST_XLSX!
echo.
set /p REPORT_DATE="Enter report date (MM/DD/YYYY): "
if "!REPORT_DATE!"=="" (
    echo No date entered. Exiting.
    pause
    exit /b 1
)

echo.
echo Running pipeline for report date !REPORT_DATE!...
echo.
cd /d "%SCRPA_ROOT%"
python "%PYTHON_SCRIPT%" "!LATEST_XLSX!" --report-date "!REPORT_DATE!"
set EXIT_CODE=!errorlevel!
echo.
if !EXIT_CODE! equ 0 (
    echo Pipeline completed successfully.
    echo.
    echo Running quick validation...
    echo.
    REM Discover the most recent cycle folder for this year
    set "CYCLE_DIR="
    for /f "delims=" %%D in ('dir /b /o-d /ad "Time_Based\2026\" 2^>nul') do (
        set "CYCLE_DIR=%SCRPA_ROOT%\Time_Based\2026\%%D"
        goto :found_cycle
    )
    :found_cycle
    if defined CYCLE_DIR (
        python "%SCRPA_ROOT%\scripts\validate_cycle_quick.py" "!CYCLE_DIR!"
        set VAL_CODE=!errorlevel!
        echo.
        if !VAL_CODE! equ 0 (
            echo Quick validation: PASSED — safe to open report
        ) else (
            echo Quick validation: FAILED — check output before submitting report
            pause
        )
    ) else (
        echo WARNING: Could not find cycle folder to validate.
    )
) else (
    echo Pipeline exited with error code !EXIT_CODE!.
)
pause
exit /b !EXIT_CODE!
