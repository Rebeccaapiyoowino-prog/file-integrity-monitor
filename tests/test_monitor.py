import tempfile
import unittest
from pathlib import Path

from monitor import (
    calculate_hash,
    build_snapshot,
    compare_snapshots,
)


class TestFileIntegrityMonitor(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.file_a = self.root / "server.conf"
        self.file_a.write_text(
            "ssh_port=22\nlogging=enabled\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_calculate_hash_returns_sha256(self):
        file_hash = calculate_hash(self.file_a)

        self.assertEqual(len(file_hash), 64)

    def test_build_snapshot_detects_file(self):
        snapshot = build_snapshot(self.root)

        self.assertIn("server.conf", snapshot)

    def test_detects_modified_file(self):
        baseline = build_snapshot(self.root)

        self.file_a.write_text(
            "ssh_port=2222\nlogging=enabled\n",
            encoding="utf-8",
        )

        current = build_snapshot(self.root)
        changes = compare_snapshots(baseline, current)

        self.assertIn("server.conf", changes["modified"])

    def test_detects_added_file(self):
        baseline = build_snapshot(self.root)

        new_file = self.root / "new.conf"
        new_file.write_text(
            "enabled=true\n",
            encoding="utf-8",
        )

        current = build_snapshot(self.root)
        changes = compare_snapshots(baseline, current)

        self.assertIn("new.conf", changes["added"])

    def test_detects_deleted_file(self):
        baseline = build_snapshot(self.root)

        self.file_a.unlink()

        current = build_snapshot(self.root)
        changes = compare_snapshots(baseline, current)

        self.assertIn("server.conf", changes["deleted"])


if __name__ == "__main__":
    unittest.main()
