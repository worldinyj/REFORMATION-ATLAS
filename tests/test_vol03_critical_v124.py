#!/usr/bin/env python3
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def get(s):
    return json.loads((ROOT/("data/deep/vol03_v124_"+s+".json")).read_text(encoding="utf8"))
class CriticalResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=get("source_and_manuscript_catalog")
        cls.b=get("passage_witness_matrix")
        cls.c=get("hus_proceedings_crosswalk")
        cls.d=get("claim_decision_register")
    def test_closed_gates(self):
        for d in (self.a,self.b,self.c,self.d):
            self.assertFalse(d["publication_gate"]["approved"])
            self.assertFalse(d["publication_gate"]["can_ship"])
    def test_genesis_is_not_in_egerton(self):
        for r in self.a["records"][:2]:
            self.assertFalse(r["genesis_present"])
    def test_exodus_is_not_in_egerton(self):
        for r in self.a["records"][:2]:
            self.assertFalse(r["exodus_present"])
    def test_mixed_manuscript(self):
        self.assertIn("MIXED_EV_LV",[x["version"] for x in self.a["records"]])
    def test_unverified_folios(self):
        self.assertTrue(all(x["verified_folio"] is None for x in self.b["passages"]))
    def test_hearing_not_sentence(self):
        self.assertNotEqual(self.c["events"][0]["genre"],self.c["events"][1]["genre"])
    def test_rel_date_is_edition_date(self):
        self.assertEqual(self.c["events"][2]["date_label"],"1869 printed edition")
    def test_reference_integrity(self):
        ids={s["id"] for s in self.a["sources"]}
        self.assertTrue(all(set(e["source_ids"])<=ids for e in self.c["events"]))
        self.assertTrue(all(set(x["sources"])<=ids for x in self.d["items"]))
    def test_rejected_claims(self):
        rejected=[x for x in self.d["items"] if x["claim_status"]=="rejected"]
        self.assertEqual(len(rejected),2)
    def test_unapproved_media(self):
        self.assertEqual(self.a["rights"]["images"],"do_not_rehost")
if __name__=="__main__":
    unittest.main()
