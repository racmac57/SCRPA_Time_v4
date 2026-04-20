# 🕒 2026-04-20-12-35-11
# Project: 16_Reports/SCRPA/scripts/start_pipeline_trigger_silent.ps1
# Author: R. A. Carucci
# Purpose: Silent PowerShell launcher for scrpa_pipeline_trigger.py. Starts the
#          trigger service hidden in the background with duplicate-instance
#          detection. Mirrors the convention of Export_File_Watchdog launchers.

$ErrorActionPreference = 'SilentlyContinue'

$ScriptDir    = Split-Path -Parent $MyInvocation.MyCommand.Path
$TriggerPy    = Join-Path $ScriptDir 'scrpa_pipeline_trigger.py'
$PidFile      = Join-Path $ScriptDir 'scrpa_pipeline_trigger.pid'

# --- Duplicate-instance detection (best-effort) -----------------------------
if (Test-Path $PidFile) {
    try {
        $ExistingPid = [int](Get-Content $PidFile -ErrorAction Stop | Select-Object -First 1)
        $Proc = Get-Process -Id $ExistingPid -ErrorAction SilentlyContinue
        if ($Proc) {
            Write-Host "SCRPA Pipeline Trigger already running (PID $ExistingPid). Exiting."
            exit 0
        }
    } catch {
        # stale PID file; let the script overwrite it
    }
}

# --- Launch hidden ----------------------------------------------------------
$PythonCmd = 'python'
$StartInfo = New-Object System.Diagnostics.ProcessStartInfo
$StartInfo.FileName               = $PythonCmd
$StartInfo.Arguments              = "`"$TriggerPy`""
$StartInfo.WorkingDirectory       = $ScriptDir
$StartInfo.WindowStyle            = 'Hidden'
$StartInfo.CreateNoWindow         = $true
$StartInfo.UseShellExecute        = $false
$StartInfo.RedirectStandardOutput = $false
$StartInfo.RedirectStandardError  = $false

$Started = [System.Diagnostics.Process]::Start($StartInfo)
if ($Started) {
    Write-Host "SCRPA Pipeline Trigger started (PID $($Started.Id))."
} else {
    Write-Host "Failed to start SCRPA Pipeline Trigger."
    exit 1
}
