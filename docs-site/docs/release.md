# Release Process

Aegis Core Platform utilizes an automated build pipeline to compile portable directories, compile Windows Setup installers, verify checksums, and publish release assets to GitHub.

---

## Release Artifacts

A successful build produces the following outputs inside the `reports/release/` workspace:

| Asset Name | Format | Description |
|:---|:---:|:---|
| **`AegisPortable.zip`** | ZIP Archive | Compressed archive containing the application folders, scripts, and runtime launchers, ready to run without installation. |
| **`AegisSetup.exe`** | Setup Binary | Dynamic installer built using Inno Setup Compiler. Registers directories, configurations, and shortcut links on the host OS. |
| **`checksums.sha256`** | SHA-256 Manifest | Text manifest file mapping all compiled binaries to their computed SHA-256 hashes for integrity verification. |
| **`manifest.json`** | JSON Metadata | File detailing the release version string, commit hash, build timestamp, and author signatures. |
| **`release_notes.md`** | Markdown Document | Generated release notes highlighting features, fixes, performance metrics, and checksum maps. |

---

## 1. Local Build Pipeline

To build and compile a release locally, follow the process below.

### Prerequisites
-   A fully configured Python virtual environment.
-   **Inno Setup Compiler (`ISCC.exe`)** installed and registered in your system's PATH. If `ISCC.exe` is missing, the script will show a warning and skip the installer step, generating only the portable assets.

### Execute Release Pipeline
Run the PowerShell compilation script:
```powershell
.\scripts\release.ps1
```

The script automates the following steps:
1.  **Compliance Checks**: Runs static checkers (`ruff` and `mypy`).
2.  **Unit Tests Validation**: Runs the entire pytest suite. The build fails if any tests fail.
3.  **Performance Metrics**: Triggers benchmark runs to record cold-start, warm-start, and database latencies.
4.  **Metadata Compilation**: Writes versioning and build variables (extracted from `version.txt` as the Single Source of Truth) to `build_metadata.json`.
5.  **Packaging**: Compiles the source files, UI elements, theme files, default configuration overrides, and launchers into `reports/release/aegis_v{VERSION}_portable/`.
6.  **Compression**: Packs the portable folder into `AegisPortable.zip`.
7.  **Inno Setup Compiler**: Invokes `ISCC.exe` on `installer/aegis_setup.iss` to compile `AegisSetup.exe`.
8.  **Checksum Calculations**: Computes SHA-256 hashes of `AegisSetup.exe` and `AegisPortable.zip` to generate `checksums.sha256`.
9.  **Release Verification**: Runs the `ReleaseValidator` script to confirm the integrity of all compiled assets.

---

## 2. GitHub Actions Automated Release

The GitHub CD pipeline (`.github/workflows/release.yml`) automates packaging and uploads compiled artifacts to GitHub Releases on tag pushes.

```text
Developer pushes git tag (v*)
             │
             ▼
    GitHub CD Triggered
             │
             ▼
1. Checkout repository
             │
             ▼
2. Configure Python 3.12 environment
             │
             ▼
3. Install dependencies (requirements.txt & requirements-dev.txt)
             │
             ▼
4. Install Inno Setup Compiler (ISCC) via setup-iscc action
             │
             ▼
5. Execute release runner script: .\scripts\release.ps1
             │
             ▼
6. Run ReleaseValidator checks (fails if assets are incomplete or dummy)
             │
             ▼
7. Create Draft GitHub Release and upload deliverables:
   ├── AegisPortable.zip
   ├── AegisSetup.exe
   ├── checksums.sha256
   ├── manifest.json
   ├── coverage.xml
   ├── benchmark.md
   └── benchmark.json
```

### Triggering Automated Release
To trigger the automated release pipeline, tag a commit and push it to GitHub:
```powershell
# Create an annotated release tag
git tag -a v1.0.0 -m "Release version 1.0.0 stable"

# Push tag to upstream origin
git push origin v1.0.0
```
This triggers the runner, compiles the artifacts, runs validation checks, and publishes a new release draft on GitHub.
