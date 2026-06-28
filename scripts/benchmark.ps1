# Aegis Core Platform — Benchmark Script (Local Developer Tool)
# Runs performance benchmarks against local hardware.
# DO NOT call this from GitHub Actions — WMI/GPU metrics require physical hardware.
# Usage: .\scripts\benchmark.ps1

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "     AEGIS CORE — PERFORMANCE BENCHMARK" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$IsCI = ($env:GITHUB_ACTIONS -eq "true") -or ($env:CI -eq "true")
if ($IsCI) {
    Write-Host "ERROR: benchmark.ps1 must not run in CI/CD environments." -ForegroundColor Red
    Write-Host "       Benchmarks require physical hardware access (WMI, GPU, CPU metrics)." -ForegroundColor Red
    exit 1
}

Write-Host "Running performance benchmark suite..." -ForegroundColor Yellow
$env:PYTHONPATH = "."
python scripts/benchmark.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Benchmark run failed." -ForegroundColor Red
    exit 1
}

Write-Host "`nBenchmark complete. Reports saved to reports/benchmark/" -ForegroundColor Green
