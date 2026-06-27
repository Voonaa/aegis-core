import os
import tempfile
import shutil
import unittest
from scripts.release_validator import ReleaseValidator

class TestReleaseValidator(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for project files
        self.test_dir = tempfile.mkdtemp()
        self.validator = ReleaseValidator(project_root=self.test_dir)

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

    def write_file(self, filename, content):
        path = os.path.join(self.test_dir, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def test_get_version(self):
        self.write_file("version.txt", "1.2.3\n")
        self.assertEqual(self.validator.get_version(), "1.2.3")

    def test_validate_version_consistency_success(self):
        self.write_file("version.txt", "1.0.0")
        self.write_file("CHANGELOG.md", "## [1.0.0] - 2026-06-27\n- Init release")
        self.write_file("README.md", "Aegis Core **Current Stable Version:** `1.0.0`")
        
        ok, msg = self.validator.validate_version_consistency()
        self.assertTrue(ok, msg)
        self.assertIn("validated successfully", msg)

    def test_validate_version_consistency_fail_changelog(self):
        self.write_file("version.txt", "1.0.0")
        self.write_file("CHANGELOG.md", "## [0.9.0] - 2026-06-27\n- Init release")
        self.write_file("README.md", "Aegis Core **Current Stable Version:** `1.0.0`")
        
        ok, msg = self.validator.validate_version_consistency()
        self.assertFalse(ok)
        self.assertIn("does not match version.txt", msg)

    def test_validate_version_consistency_fail_readme(self):
        self.write_file("version.txt", "1.0.0")
        self.write_file("CHANGELOG.md", "## [1.0.0] - 2026-06-27\n- Init release")
        self.write_file("README.md", "Aegis Core **Current Stable Version:** `0.9.0`")
        
        ok, msg = self.validator.validate_version_consistency()
        self.assertFalse(ok)
        self.assertIn("does not match version.txt", msg)

    def test_validate_release_notes(self):
        notes_content = """
        # Version 1.0.0
        ## Release Date
        2026-06-27
        ## Highlights
        Great performance boost
        ## Bug Fixes
        None
        ## Performance
        Fast startup
        ## Checksums
        SHA-256 available
        ## Installation
        Run installer
        ## Known Issues
        None
        """
        notes_path = os.path.join(self.test_dir, "release_notes.md")
        self.write_file("release_notes.md", notes_content)
        
        ok, msg = self.validator.validate_release_notes(notes_path)
        self.assertTrue(ok)

        # Test incomplete notes
        incomplete_content = "# Version 1.0.0\n## Highlights\nGood"
        self.write_file("release_notes.md", incomplete_content)
        ok, msg = self.validator.validate_release_notes(notes_path)
        self.assertFalse(ok)
        self.assertIn("missing in release notes", msg)

    def test_validate_release_artifacts(self):
        release_dir = os.path.join(self.test_dir, "reports", "release")
        os.makedirs(release_dir, exist_ok=True)
        
        self.write_file("version.txt", "1.0.0")
        
        # Write dummy files
        setup_content = b"setup_exe_data"
        portable_content = b"portable_zip_data"
        
        with open(os.path.join(release_dir, "AegisSetup.exe"), "wb") as f:
            f.write(setup_content)
        with open(os.path.join(release_dir, "AegisPortable.zip"), "wb") as f:
            f.write(portable_content)
            
        import hashlib
        setup_hash = hashlib.sha256(setup_content).hexdigest()
        portable_hash = hashlib.sha256(portable_content).hexdigest()
        
        checksum_data = f"{setup_hash}  AegisSetup.exe\n{portable_hash}  AegisPortable.zip"
        
        self.write_file("reports/release/checksums.sha256", checksum_data)
        self.write_file("reports/release/build_metadata.json", "{}")
        self.write_file("reports/release/manifest.json", "{}")
        self.write_file("reports/release/release_notes.md", "## Version\n## Release Date\n## Highlights\n## Bug Fixes\n## Performance\n## Checksums\n## Installation\n## Known Issues")
        
        # Write mock coverage and benchmark reports
        self.write_file("reports/coverage/coverage.xml", "<coverage></coverage>")
        self.write_file("reports/benchmark/benchmark.md", "# Benchmarks")
        self.write_file("reports/benchmark/benchmark.json", "{}")

        ok, msg = self.validator.validate_release_artifacts(release_dir)
        self.assertTrue(ok, msg)

if __name__ == "__main__":
    unittest.main()
