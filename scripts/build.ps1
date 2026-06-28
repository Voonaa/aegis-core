# Aegis Core Platform — Build Script (Packaging Only)
# Responsibility: Produce all release artifacts from source.
# Does NOT run lint, tests, coverage, or benchmarks.
# Usage: .\scripts\build.ps1

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "     AEGIS CORE — BUILD & PACKAGING PIPELINE" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 0. Read version from SSOT
$Version = (Get-Content -Path "version.txt" -TotalCount 1).Trim()
Write-Host "Target Version: $Version" -ForegroundColor Green

# 1. Prepare output directories
Write-Host "`n[Step 1] Preparing release directories..." -ForegroundColor Yellow
$ProjectRoot = Get-Item .
$ReportsDir  = Join-Path $ProjectRoot.FullName "reports"
$ReleaseRoot = Join-Path $ReportsDir "release"
$PortableDir = Join-Path $ReleaseRoot "aegis_v$($Version)_portable"

foreach ($path in @($ReleaseRoot, $PortableDir)) {
    if (Test-Path $path) { Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue }
    New-Item -ItemType Directory -Path $path -Force | Out-Null
}
Write-Host "  Release directory ready: $ReleaseRoot" -ForegroundColor Gray

# 2. Assemble portable release
Write-Host "`n[Step 2] Assembling portable release package..." -ForegroundColor Yellow
foreach ($folder in @("apps", "packages", "plugins", "assets")) {
    $Src = Join-Path $ProjectRoot.FullName $folder
    if (Test-Path $Src) {
        Copy-Item -Path $Src -Destination $PortableDir -Recurse -Force
        Write-Host "  Copied: $folder" -ForegroundColor Gray
    }
}
foreach ($file in @("requirements.txt", "pyproject.toml", "CHANGELOG.md", "README.md", "LICENSE")) {
    $Src = Join-Path $ProjectRoot.FullName $file
    if (Test-Path $Src) {
        Copy-Item -Path $Src -Destination (Join-Path $PortableDir $file) -Force
        Write-Host "  Copied: $file" -ForegroundColor Gray
    }
}
"@echo off`r`nset PYTHONPATH=.`r`npython apps/desktop/main.py" | Out-File -FilePath (Join-Path $PortableDir "Aegis.bat") -Encoding ascii -NoNewline
Write-Host "  Created: Aegis.bat" -ForegroundColor Gray

# 3. Build metadata
Write-Host "`n[Step 3] Generating build metadata..." -ForegroundColor Yellow
$Commit = "UNKNOWN"
try { $Commit = (git rev-parse --short HEAD).Trim() } catch {}
$Metadata = @{
    version         = $Version
    build_timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    commit_hash     = $Commit
    python_version  = (python -c "import platform; print(platform.python_version())").Trim()
    architecture    = if ($env:PROCESSOR_ARCHITECTURE) { $env:PROCESSOR_ARCHITECTURE } else { "x64" }
} | ConvertTo-Json
$MetaPath = Join-Path $ReleaseRoot "build_metadata.json"
$Metadata | Out-File -FilePath $MetaPath -Encoding utf8 -NoNewline
Copy-Item -Path $MetaPath -Destination (Join-Path $PortableDir "build_metadata.json") -Force
Write-Host "  build_metadata.json written." -ForegroundColor Gray

# 4. Release notes
Write-Host "`n[Step 4] Generating release_notes.md..." -ForegroundColor Yellow
$ReleaseNotesPath = Join-Path $ReleaseRoot "release_notes.md"
@"
# Version $Version
## Release Date
$(Get-Date -Format "yyyy-MM-dd")

# Highlights
Production-grade packaging release for Aegis Core Platform.

# New Features
- Automated installer and release artifact integrity validation.
- Standardized monorepo layout and package structure.

# Improvements
- Modular release pipeline with separated build, benchmark, and validation stages.

# Bug Fixes
- Safe profile application warnings resolved.
- EventBus threading overhead minimized.

# Performance
- Startup execution speed optimized (Health engine < 10ms check).
- Memory footprints reduced inside CustomTkinter page transitions.

# Compatibility
- Supported on Windows 10 and Windows 11 architectures.
- Requires Python 3.12+.

# Checksums
SHA-256 validation checksums compiled for release binaries.

# Installation
1. Run AegisSetup.exe for full system integration.
2. Alternatively, extract AegisPortable.zip and run Aegis.bat.

# Known Issues
- Elevated permissions required for full WMI hardware diagnostic metrics.
"@ | Out-File -FilePath $ReleaseNotesPath -Encoding utf8 -NoNewline
Write-Host "  release_notes.md generated." -ForegroundColor Gray

# 5. Manifest
Write-Host "`n[Step 5] Generating manifest.json..." -ForegroundColor Yellow
$ManifestPath = Join-Path $ReleaseRoot "manifest.json"
@{
    name         = "Aegis Core Platform"
    version      = $Version
    release_date = (Get-Date -Format "yyyy-MM-dd")
    components   = @("AegisSetup.exe","AegisPortable.zip","checksums.sha256","release_notes.md","manifest.json")
} | ConvertTo-Json | Out-File -FilePath $ManifestPath -Encoding utf8 -NoNewline
Write-Host "  manifest.json generated." -ForegroundColor Gray

# 6. AegisPortable.zip
Write-Host "`n[Step 6] Creating AegisPortable.zip..." -ForegroundColor Yellow
$ZipDest = Join-Path $ReleaseRoot "AegisPortable.zip"
if (Test-Path $ZipDest) { Remove-Item -Path $ZipDest -Force }
Compress-Archive -Path "$PortableDir\*" -DestinationPath $ZipDest -Force
Write-Host "  AegisPortable.zip created." -ForegroundColor Green

# 7. Inno Setup Installer
Write-Host "`n[Step 7] Compiling Inno Setup installer..." -ForegroundColor Yellow
$ISCC = Get-Command "iscc.exe" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
if ($null -eq $ISCC) {
    $DefaultISCC = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if (Test-Path $DefaultISCC) { $ISCC = $DefaultISCC }
}
$IsCI = ($env:GITHUB_ACTIONS -eq "true") -or ($env:CI -eq "true")
if ($null -ne $ISCC -and (Test-Path $ISCC)) {
    Write-Host "  Found ISCC: $ISCC" -ForegroundColor Gray
    & $ISCC /DMyAppVersion=$Version /DSourceDir="$PortableDir" /DOutputDir="$ReleaseRoot" /DOutputBaseFilename="AegisSetup" "installer/aegis_setup.iss" | Out-Host
    Write-Host "  AegisSetup.exe compiled." -ForegroundColor Green
} elseif ($IsCI) {
    throw "ISCC.exe not found in CI environment. Ensure Inno Setup is installed via Chocolatey before running build.ps1."
} else {
    Write-Host "  Warning: ISCC not found locally. Creating placeholder AegisSetup.exe." -ForegroundColor Yellow
    "Placeholder — compile with Inno Setup locally" | Out-File -FilePath (Join-Path $ReleaseRoot "AegisSetup.exe") -Encoding ascii
}

# 8. SHA-256 Checksums
Write-Host "`n[Step 8] Generating SHA-256 checksums..." -ForegroundColor Yellow
$ChecksumFile = Join-Path $ReleaseRoot "checksums.sha256"
$HashLines = @()
foreach ($binary in @("AegisSetup.exe", "AegisPortable.zip")) {
    $BinPath = Join-Path $ReleaseRoot $binary
    if (Test-Path $BinPath) {
        $Hash = (Get-FileHash -Path $BinPath -Algorithm SHA256).Hash.ToLower()
        $HashLines += "$Hash  $binary"
    }
}
$HashLines -join "`r`n" | Out-File -FilePath $ChecksumFile -Encoding ascii
Write-Host "  checksums.sha256 generated." -ForegroundColor Gray

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "  BUILD COMPLETE: $ReleaseRoot" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Get-ChildItem -Path $ReleaseRoot | Select-Object Name, Length | Format-Table -AutoSize
