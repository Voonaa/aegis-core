"""Aegis Core Platform — Release Artifact Validator.

Validates only release artifacts. Does NOT check coverage or benchmark reports.
Those belong to the CI pipeline (ci.yml).

Required artifacts:
    - AegisSetup.exe
    - AegisPortable.zip
    - manifest.json
    - checksums.sha256
    - release_notes.md
"""
import os
import re
import hashlib


class ReleaseValidator:
    def __init__(self, project_root="."):
        self.project_root = os.path.abspath(project_root)

    def get_version(self):
        version_path = os.path.join(self.project_root, "version.txt")
        if not os.path.exists(version_path):
            raise FileNotFoundError("version.txt is missing")
        with open(version_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def validate_version_consistency(self):
        """Verify version.txt matches CHANGELOG.md and README.md."""
        version = self.get_version()

        # Validate CHANGELOG.md
        changelog_path = os.path.join(self.project_root, "CHANGELOG.md")
        if not os.path.exists(changelog_path):
            raise FileNotFoundError("CHANGELOG.md is missing")
        with open(changelog_path, "r", encoding="utf-8") as f:
            changelog_content = f.read()
        changelog_match = re.search(
            r"##\s+\[([0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.]+)?)]",
            changelog_content,
        )
        if not changelog_match:
            return False, "Could not parse any version header in CHANGELOG.md"
        changelog_version = changelog_match.group(1)
        if changelog_version != version:
            return (
                False,
                f"Version in CHANGELOG.md ({changelog_version}) does not match version.txt ({version})",
            )

        # Validate README.md
        readme_path = os.path.join(self.project_root, "README.md")
        if not os.path.exists(readme_path):
            raise FileNotFoundError("README.md is missing")
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        readme_match = re.search(
            r"\*\*Current Stable Version:\*\*\s+`([0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.]+)??)`",
            readme_content,
        )
        if not readme_match:
            return (
                False,
                "Could not find '**Current Stable Version:** `version`' pattern in README.md",
            )
        readme_version = readme_match.group(1)
        if readme_version != version:
            return (
                False,
                f"Version in README.md ({readme_version}) does not match version.txt ({version})",
            )

        return True, "Version consistency validated successfully"

    def validate_release_artifacts(self, release_dir):
        """Verify required release artifact files exist and checksums are valid."""
        required_files = [
            "AegisSetup.exe",
            "AegisPortable.zip",
            "checksums.sha256",
            "manifest.json",
            "release_notes.md",
        ]
        for file in required_files:
            file_path = os.path.join(release_dir, file)
            if not os.path.exists(file_path):
                return False, f"Required release artifact is missing: {file}"

        # Validate SHA256 checksums
        checksums_path = os.path.join(release_dir, "checksums.sha256")
        with open(checksums_path, "r", encoding="utf-8") as f:
            checksums_content = f.read().strip().split("\n")

        hash_map = {}
        for line in checksums_content:
            if not line.strip():
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_map[parts[1].strip()] = parts[0].strip().lower()

        for file_name in ["AegisSetup.exe", "AegisPortable.zip"]:
            if file_name not in hash_map:
                return False, f"{file_name} is not registered in checksums.sha256"
            file_path = os.path.join(release_dir, file_name)
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            actual_hash = sha256.hexdigest().lower()
            if actual_hash != hash_map[file_name]:
                return (
                    False,
                    f"Hash mismatch for {file_name}: expected {hash_map[file_name]}, got {actual_hash}",
                )

        return True, "Release artifacts and checksums verified successfully"

    def validate_release_notes(self, release_notes_path):
        """Verify release_notes.md contains all required sections."""
        if not os.path.exists(release_notes_path):
            return False, "release_notes.md is missing"
        with open(release_notes_path, "r", encoding="utf-8") as f:
            content = f.read()
        required_sections = [
            "Version",
            "Release Date",
            "Highlights",
            "Bug Fixes",
            "Performance",
            "Checksums",
            "Installation",
            "Known Issues",
        ]
        for section in required_sections:
            pattern = rf"(#+\s+{section}|\*\*{section}\*\*|{section}:)"
            if not re.search(pattern, content, re.IGNORECASE):
                return False, f"Required section missing in release_notes.md: {section}"
        return True, "Release notes format validated successfully"

    def run_all_checks(self, release_dir):
        ok, msg = self.validate_version_consistency()
        if not ok:
            return False, msg

        notes_path = os.path.join(release_dir, "release_notes.md")
        ok, msg = self.validate_release_notes(notes_path)
        if not ok:
            return False, msg

        ok, msg = self.validate_release_artifacts(release_dir)
        if not ok:
            return False, msg

        return True, "All release validation checks passed."


if __name__ == "__main__":
    import sys

    rel_dir = os.path.abspath("reports/release")
    validator = ReleaseValidator()
    print("Running release artifact validation...")
    success, message = validator.run_all_checks(rel_dir)
    print(message)
    sys.exit(0 if success else 1)
