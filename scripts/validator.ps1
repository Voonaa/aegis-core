# Aegis Core Platform — Release Validator Script
# Validates that all required release artifacts exist and pass integrity checks.
# Usage: .\scripts\validator.ps1
# Called by: release.ps1 (local), release.yml (CI)

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "     AEGIS CORE — RELEASE ARTIFACT VALIDATOR" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$env:PYTHONPATH = "."
python scripts/release_validator.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nRelease validation FAILED." -ForegroundColor Red
    exit 1
}

Write-Host "`nAll release artifacts validated successfully." -ForegroundColor Green
