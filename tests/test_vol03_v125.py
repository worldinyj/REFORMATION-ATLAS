import json
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(name):
 return json.loads((R/("data/deep/vol03_v125_"+name+".json")).read_text(encoding="utf8"))
class MegabatchTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=load("source_registry");cls.c=load("claim_registry");cls.w=load("witness_registry");cls.p=load("passage_plan");cls.h=load("constance_textual_audit");cls.g=load("publication_gate_matrix")
 def test_source_count(self):self.assertEqual(len(self.s["sources"]),14)
 def test_claim_count(self):self.assertEqual(len(self.c["claims"]),20)
 def test_claim_ids_unique(self):self.assertEqual(len({x["id"] for x in self.c["claims"]}),20)
 def test_manuscript_not_collated(self):self.assertTrue(all(x["direct_folio_verified"] is False for x in self.w["witnesses"]))
 def test_genesis_absence(self):self.assertTrue(all("Genesis" in x["excludes"] for x in self.w["witnesses"][:2]))
 def test_exodus_absence(self):self.assertTrue(all("Exodus" in x["excludes"] for x in self.w["witnesses"][:2]))
 def test_passages_unverified(self):self.assertTrue(all(x["collated"] is False for x in self.p["passages"]))
 def test_source_resolution(self):
  ids={x["id"] for x in self.s["sources"]}
  self.assertTrue(all(set(x["source_ids"])<=ids for x in self.c["claims"]))
 def test_hus_three_genres(self):self.assertEqual(len({x["genre"] for x in self.h["panels"]}),3)
 def test_hus_1869_non_autograph(self):self.assertFalse(self.h["printed_edition"]["edition_is_autograph"])
 def test_gates(self):
  for x in (self.s,self.c,self.w,self.p,self.h,self.g):
   self.assertFalse(x["publication_gate"]["can_ship"])
 def test_merge_blocked(self):self.assertEqual(self.g["gates"]["main_merge"],"blocked")
 def test_rejections(self):self.assertGreaterEqual(sum("rejected" in x["verdict"] for x in self.c["claims"]),4)
 def test_rights(self):self.assertTrue(all(x["rights"]=="metadata_link_and_paraphrase_only" for x in self.s["sources"]))
 def test_vol03_data_immutability(self):self.assertEqual(self.p["status"],"DRAFT_RESEARCH_NOT_PUBLIC")
if __name__=="__main__":unittest.main()
