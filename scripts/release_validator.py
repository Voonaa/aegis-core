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
        version = self.get_version()
        
        # Validate CHANGELOG.md
        changelog_path = os.path.join(self.project_root, "CHANGELOG.md")
        if not os.path.exists(changelog_path):
            raise FileNotFoundError("CHANGELOG.md is missing")
        with open(changelog_path, "r", encoding="utf-8") as f:
            changelog_content = f.read()
        
        # Get the first version header in CHANGELOG.md (must be identical)
        changelog_match = re.search(r"##\s+\[([0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.]+)?)]", changelog_content)
        if not changelog_match:
            return False, "Could not parse any version header in CHANGELOG.md"
        changelog_version = changelog_match.group(1)
        if changelog_version != version:
            return False, f"Version in CHANGELOG.md ({changelog_version}) does not match version.txt ({version})"

        # Validate README.md
        readme_path = os.path.join(self.project_root, "README.md")
        if not os.path.exists(readme_path):
            raise FileNotFoundError("README.md is missing")
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        
        # Get the version from README.md dynamic/static declaration
        readme_match = re.search(r"\*\*Current Stable Version:\*\*\s+`([0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.]+)??)`", readme_content)
        if not readme_match:
            return False, "Could not find '**Current Stable Version:** `version`' pattern in README.md"
        readme_version = readme_match.group(1)
        if readme_version != version:
            return False, f"Version in README.md ({readme_version}) does not match version.txt ({version})"

        return True, "Version consistency validated successfully"

    def validate_release_artifacts(self, release_dir):
        version = self.get_version()
        
        required_files = [
            "AegisSetup.exe",
            "AegisPortable.zip",
            "checksums.sha256",
            "build_metadata.json",
            "manifest.json",
            "release_notes.md"
        ]
        
        for file in required_files:
            file_path = os.path.join(release_dir, file)
            if not os.path.exists(file_path):
                return False, f"Required release file is missing: {file}"

        # Verify quality assurance reports existence (CR-7)
        reports_dir = os.path.dirname(release_dir)
        cov_xml = os.path.join(reports_dir, "coverage", "coverage.xml")
        bench_md = os.path.join(reports_dir, "benchmark", "benchmark.md")
        bench_json = os.path.join(reports_dir, "benchmark", "benchmark.json")

        if not os.path.exists(cov_xml):
            return False, "Quality report is missing: reports/coverage/coverage.xml"
        if not os.path.exists(bench_md):
            return False, "Quality report is missing: reports/benchmark/benchmark.md"
        if not os.path.exists(bench_json):
            return False, "Quality report is missing: reports/benchmark/benchmark.json"

        # Verify dummy installer block in CI environment (CR-2)
        is_ci = os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true"
        if is_ci:
            setup_path = os.path.join(release_dir, "AegisSetup.exe")
            with open(setup_path, "r", encoding="utf-8", errors="ignore") as f:
                first_line = f.readline()
                if "Dummy Setup Content" in first_line:
                    return False, "Validation failed: Dummy setup installer detected in CI/CD environment"

        # Validate SHA256 checksums file content
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

        # Check if files in checksum match their actual hash
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
                return False, f"Hash mismatch for {file_name}: expected {hash_map[file_name]}, got {actual_hash}"

        return True, "Release artifacts and checksums verified successfully"

    def validate_release_notes(self, release_notes_path):
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
            "Known Issues"
        ]

        for section in required_sections:
            # Match section headers (either markdown header or bold text or plain lines)
            # Standard markdown header format preferred: e.g. # Version, ## Version, ### Version, or **Version**
            pattern = rf"(#+\s+{section}|\*\*{section}\*\*|{section}:)"
            if not re.search(pattern, content, re.IGNORECASE):
                return False, f"Required section is missing in release notes: {section}"

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
    print("Running release validation checks...")
    success, message = validator.run_all_checks(rel_dir)
    print(message)
    if not success:
        sys.exit(1)
    sys.exit(0)
