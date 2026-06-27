# Contributing to Aegis Core Platform

We love contributions! Here is a simple guide to help you build, test, and submit your pull requests to Aegis Core.

## Getting Started

1. Fork this repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/Voonaa/aegis-core.git
   ```
3. Set up the development dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Development Workflow

1. Always branch off the `develop` branch:
   ```bash
   git checkout develop
   git checkout -b feature/your-awesome-feature
   ```
2. Write clean code adhering to **SOLID principles** and Clean Architecture.
3. Keep the launcher `apps/desktop/main.py` thin. Register new services in [bootstrap.py](packages/core/bootstrap.py).

## Testing and Linting

Before pushing your changes, you must ensure that all checks pass:

1. **Static Analysis & Formatting**:
   Run the static linter script:
   ```powershell
   .\scripts\lint.ps1
   ```
2. **Automated Unit Tests**:
   Run all pytest test cases:
   ```powershell
   $env:PYTHONPATH="."
   python -m pytest tests/ -v
   ```
3. **Performance Regressions**:
   Ensure no bootstrap latency is introduced:
   ```powershell
   python scripts/benchmark.py
   ```

## Submitting Pull Requests

- Keep your PR descriptions detailed using our PR Template.
- Link relevant issues.
- Once reviewed and approved by the Technical Lead, your changes will be merged into `develop` and eventually packaged into the next production release.
