# Aegis Core Platform — Local Release Script (Developer Convenience Tool)
# Runs the full local release pipeline: build -> validate.
# Does NOT run lint, tests, coverage, or benchmarks.
# Those belong in: ci.yml (lint+tests), benchmark.ps1 (benchmarks).
# Usage: .\scripts\release.ps1

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   AEGIS CORE — LOCAL RELEASE PIPELINE" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$Version = (Get-Content -Path "version.txt" -TotalCount 1).Trim()
Write-Host "Version: $Version" -ForegroundColor Green

# Step 1: Build artifacts (packaging)
Write-Host "`n[1/2] Running build pipeline..." -ForegroundColor Yellow
.\scripts\build.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Aborting release." -ForegroundColor Red
    exit 1
}

# Step 2: Validate release artifacts
Write-Host "`n[2/2] Validating release artifacts..." -ForegroundColor Yellow
.\scripts\validator.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Validation failed. Aborting release." -ForegroundColor Red
    exit 1
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "  Local release v$Version completed successfully!" -ForegroundColor Green
Write-Host "  Artifacts: reports\release\" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
