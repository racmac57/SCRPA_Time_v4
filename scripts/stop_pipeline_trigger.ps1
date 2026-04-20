# 🕒 2026-04-20-12-35-11
# Project: 16_Reports/SCRPA/scripts/stop_pipeline_trigger.ps1
# Author: R. A. Carucci
# Purpose: Stop the SCRPA Pipeline Trigger service by reading its PID file and
#          terminating the matching Python process. Mirrors the convention of
#          Export_File_Watchdog launchers.

$ErrorActionPreference = 'SilentlyContinue'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidFile   = Join-Path $ScriptDir 'scrpa_pipeline_trigger.pid'

if (-not (Test-Path $PidFile)) {
    Write-Host "No PID file found; trigger service does not appear to be running."
    exit 0
}

try {
    $ExistingPid = [int](Get-Content $PidFile -ErrorAction Stop | Select-Object -First 1)
} catch {
    Write-Host "PID file unreadable. Removing it."
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
    exit 1
}

$Proc = Get-Process -Id $ExistingPid -ErrorAction SilentlyContinue
if (-not $Proc) {
    Write-Host "PID $ExistingPid not running. Cleaning up stale PID file."
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
    exit 0
}

try {
    Stop-Process -Id $ExistingPid -Force -ErrorAction Stop
    Write-Host "Stopped SCRPA Pipeline Trigger (PID $ExistingPid)."
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
} catch {
    Write-Host "Failed to stop PID $ExistingPid: $_"
    exit 1
}
