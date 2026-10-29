#!/usr/bin/env python3
"""Regression tests for V1.16 read-only projections; mutate only in-memory copies."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from atlas_readonly_adapter_v116 import adapt

class AdapterRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = adapt()
        cls.records = cls.data["records"]

    def test_record_count(self):
        self.assertEqual(len(self.records), 39)

    def test_unique_ids(self):
        self.assertEqual(len({r["id"] for r in self.records}), len(self.records))

    def test_provenance(self):
        self.assertTrue(all(r["source_ids"] for r in self.records))

    def test_all_private(self):
        self.assertFalse(self.data["publication_gate"]["can_ship"])
        self.assertTrue(all(r["public_visible"] is False and r["publication_approved"] is False for r in self.records))

    def test_volume_counts(self):
        self.assertEqual(sum(r["source_file"].endswith("events_documents_v01.json") for r in self.records),34)
        self.assertEqual(sum(r["source_file"].endswith("vol04_luther_v01.json") for r in self.records),1)
        self.assertEqual(sum(r["source_file"].endswith("vol05_education_map_timeline_v114.json") for r in self.records),4)

    def test_distinct_approval_and_arrival(self):
        items = {r["id"]:r for r in self.records}
        self.assertEqual(items["EV-PAD-PERMIT-1652"]["date_label"],"1652-10-21")
        self.assertEqual(items["EV-PAD-ARRIVAL-1658"]["date_label"],"1658-03-28")

    def test_non_mutating_copy(self):
        original = copy.deepcopy(self.data)
        _ = [dict(r, public_visible=True) for r in self.records]
        self.assertEqual(self.data,original)

if __name__ == "__main__":
    unittest.main()
