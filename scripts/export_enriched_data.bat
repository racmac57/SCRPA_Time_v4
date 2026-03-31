@echo off
REM Export Enriched Data and Create Email Template
REM Run this after exporting Power BI preview table

cd /d "%~dp0"
python "%~dp0export_enriched_data_and_email.py"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Script completed successfully!
    pause
) else (
    echo.
    echo ❌ Script encountered an error.
    pause
)
