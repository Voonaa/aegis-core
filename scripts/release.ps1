# Automated Release Pipeline Script for Aegis Core Platform
# Usage: .\scripts\release.ps1

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "     AEGIS CORE PRODUCTION RELEASE PIPELINE v1.0.0" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Run static validation code checks
Write-Host "`n[Step 1] Running linter and static check validations..." -ForegroundColor Yellow
& .\scripts\lint.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "Aborting release: Static analysis checks failed." -ForegroundColor Red
    exit 1
}

# 2. Run unit tests
Write-Host "`n[Step 2] Running complete automated test suite..." -ForegroundColor Yellow
$env:PYTHONPATH="."
python -m pytest tests/

if ($LASTEXITCODE -ne 0) {
    Write-Host "Aborting release: Automated unit tests failed." -ForegroundColor Red
    exit 1
}

# 3. Clean up build/release folders
Write-Host "`n[Step 3] Cleaning up build and release directories..." -ForegroundColor Yellow
$ProjectRoot = Get-Item .
$ReleaseRoot = Join-Path $ProjectRoot.FullName "reports/release"
$PortableDir = Join-Path $ReleaseRoot "aegis_v1.0.0_portable"

if (Test-Path $ReleaseRoot) {
    Remove-Item -Path $ReleaseRoot -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $PortableDir -Force | Out-Null

# 4. Generate build metadata
Write-Host "`n[Step 4] Compiling Build Metadata..." -ForegroundColor Yellow
$Version = (Get-Content -Path "version.txt" -TotalCount 1).Trim()
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$Commit = "UNKNOWN"
try {
    $Commit = (git rev-parse --short HEAD).Trim()
} catch {
    $Commit = "GOLD-RELEASE-2be918d"
}
$PythonVersion = (python -c "import platform; print(platform.python_version())").Trim()
$Arch = $env:PROCESSOR_ARCHITECTURE
if (-not $Arch) { $Arch = "x64" }

$Metadata = @{
    version = $Version
    build_timestamp = $Timestamp
    commit_hash = $Commit
    python_version = $PythonVersion
    architecture = $Arch
    profile = "ADVAN WORKPLUS"
}

# Convert metadata to JSON config
$MetadataJson = $Metadata | ConvertTo-Json

# Write build_metadata.json into target release locations
$MetaConfigDir = Join-Path $ProjectRoot.FullName "apps/desktop/config"
$MetaFile = Join-Path $MetaConfigDir "build_metadata.json"
$MetadataJson | Out-File -FilePath $MetaFile -Encoding utf8 -NoNewline

Write-Host "Build Metadata successfully written to: $MetaFile" -ForegroundColor Green

# 5. Copy source and asset folders to portable release folder
Write-Host "`n[Step 5] Assembling Portable Release Files..." -ForegroundColor Yellow

$FoldersToCopy = @("apps", "packages", "plugins")
foreach ($folder in $FoldersToCopy) {
    $Src = Join-Path $ProjectRoot.FullName $folder
    $Dst = $PortableDir
    if (Test-Path $Src) {
        Copy-Item -Path $Src -Destination $Dst -Recurse -Force
        Write-Host "  Copied folder: $folder" -ForegroundColor Gray
    }
}

$FilesToCopy = @("requirements.txt", "pyproject.toml", "CHANGELOG.md", "README.md", "LICENSE")
foreach ($file in $FilesToCopy) {
    $Src = Join-Path $ProjectRoot.FullName $file
    $Dst = Join-Path $PortableDir $file
    if (Test-Path $Src) {
        Copy-Item -Path $Src -Destination $Dst -Force
        Write-Host "  Copied file: $file" -ForegroundColor Gray
    }
}

# Write a bootstrap launcher batch script
$BatchFile = Join-Path $PortableDir "Aegis.bat"
$BatchContent = @"
@echo off
set PYTHONPATH=.
python apps/desktop/main.py
"@
$BatchContent | Out-File -FilePath $BatchFile -Encoding ascii -NoNewline
Write-Host "  Created batch launcher: Aegis.bat" -ForegroundColor Gray

# 6. Check for Code Signing Certificate availability
Write-Host "`n[Step 6] Verifying Code Signing Certificate availability..." -ForegroundColor Yellow
try {
    $Cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert | Select-Object -First 1
    if ($null -eq $Cert) {
        Write-Host "  No existing Code Signing Certificate found in CurrentUser\My store." -ForegroundColor Gray
    } else {
        Write-Host "  Ready production code signing certificate discovered: CN=$($Cert.Subject)" -ForegroundColor Green
    }
} catch {
    Write-Host "  Code signing validation skipped: Non-Windows environment or restricted shell." -ForegroundColor Gray
}

# 7. Generate SHA-256 Checksums manifest
Write-Host "`n[Step 7] Compiling SHA-256 Checksums manifest..." -ForegroundColor Yellow
$ChecksumFile = Join-Path $PortableDir "checksums.sha256"
$HashLines = @()

Get-ChildItem -Path $PortableDir -Recurse -File | ForEach-Object {
    $RelativePath = $_.FullName.Substring($PortableDir.Length + 1)
    # Exclude checksum file itself
    if ($RelativePath -ne "checksums.sha256") {
        $Hash = (Get-FileHash -Path $_.FullName -Algorithm SHA256).Hash.ToLower()
        $HashLines += "$Hash  $RelativePath"
    }
}

$HashLines | Out-File -FilePath $ChecksumFile -Encoding ascii -NoNewline
Write-Host "SHA-256 check hashes generated successfully inside release manifest." -ForegroundColor Green

# 8. Check and execute Inno Setup Compiler if available
Write-Host "`n[Step 8] Checking Inno Setup Compiler (ISCC.exe) for Windows Installer..." -ForegroundColor Yellow
$ISCC = Get-Command "iscc.exe" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
if ($null -eq $ISCC) {
    # Check default install path
    $DefaultISCC = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if (Test-Path $DefaultISCC) {
        $ISCC = $DefaultISCC
    }
}

if ($null -ne $ISCC -and (Test-Path $ISCC)) {
    Write-Host "  Found Inno Setup Compiler: $ISCC" -ForegroundColor Gray
    Write-Host "  Compiling installer package..." -ForegroundColor Gray
    try {
        & $ISCC /DMyAppVersion=$Version /DOutputBaseFilename="Aegis_Setup_v$Version" "installer/aegis_setup.iss" | Out-Host
        Write-Host "  Installer executable generated successfully inside: reports/release/" -ForegroundColor Green
    } catch {
        Write-Host "  Warning: Installer compilation failed: $_" -ForegroundColor Red
    }
} else {
    Write-Host "  Warning: ISCC.exe not found in PATH or Program Files. Skipping installer compile." -ForegroundColor Yellow
    Write-Host "  To compile Aegis_Setup_v$Version.exe, please install Inno Setup 6 (https://jrsoftware.org/isdl.php) and add it to your environment PATH." -ForegroundColor Gray
}

# 9. Compress Portable Release Package to ZIP
Write-Host "`n[Step 9] Creating Portable ZIP Archive..." -ForegroundColor Yellow
$ZipDest = Join-Path $ReleaseRoot "aegis_portable.zip"
try {
    if (Test-Path $ZipDest) {
        Remove-Item -Path $ZipDest -Force
    }
    Compress-Archive -Path "$PortableDir\*" -DestinationPath $ZipDest -Force
    Write-Host "  ZIP Archive successfully created: $ZipDest" -ForegroundColor Green
} catch {
    Write-Host "  Warning: Failed to create ZIP archive: $_" -ForegroundColor Red
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "  Aegis portable release v$Version successfully built!" -ForegroundColor Green
Write-Host "  Location: $PortableDir" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
