#!/usr/bin/env python3
"""Fail closed tests: §3 parity ≠ §35 individual enforcement, pre-1648 ≠ postwar."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_ipo_regional_reception_v06 import load,validate,REG

def assert_rejected(original,title,mutate):
    x=copy.deepcopy(original)
    mutate(x)
    try: validate(x)
    except (ValueError,KeyError,IndexError,TypeError,StopIteration):return
    raise AssertionError("unsafe local history change accepted: "+title)

def main():
    d=load(REG)
    assert validate(d)["public"]==0
    tests=[
      ("public approved",lambda x:x["release_gate"].__setitem__("can_ship",True)),
      ("published",lambda x:x["release_gate"].__setitem__("publication_approved",True)),
      ("primary records fabricated",lambda x:x["release_gate"].__setitem__("regional_archival_primary_records_collated",True)),
      ("V35 enforcement fabricated",lambda x:x["release_gate"].__setitem__("v35_post_treaty_enforcement_proven",True)),
      ("media rights fabricated",lambda x:x["release_gate"].__setitem__("media_rights_approved",True)),
      ("scholar approval fabricated",lambda x:x["release_gate"].__setitem__("scholar_review",True)),
      ("overview changed",lambda x:x.__setitem__("overview_modified",True)),
      ("AI Studio changed",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("canonical ID created",lambda x:x.__setitem__("created_canonical_ids",1)),
      ("wrong work",lambda x:x.__setitem__("existing_document_id","OV-D-014")),
      ("source not https",lambda x:x["source_records"][0].__setitem__("url","http://invalid.example")),
      ("false city council original",lambda x:x["source_records"][1].__setitem__("original_city_council_minutes_examined",True)),
      ("unauthorized image rights",lambda x:x["source_records"][2].__setitem__("reproduced_image_rights_approved",True)),
      ("missing source",lambda x:x["source_records"].pop()),
      ("missing city case",lambda x:x["region_cases"].pop()),
      ("Augsburg falsely V35",lambda x:x["region_cases"][0].__setitem__("legal_anchor","IPO_ART_V_PAR_35")),
      ("Biberach 1548 lost",lambda x:x["region_cases"][1].__setitem__("time_focus","1648–1649")),
      ("Dinkelsbuehl fiction becomes archive",lambda x:x["region_cases"][2].__setitem__("evidence_level","DIRECT_CITY_ARCHIVE_CONFIRMED")),
      ("Ravensburg V35 suit invented",lambda x:x["region_cases"][3].__setitem__("direct_application_of_v35_proved",True)),
      ("Muenster 1587 becomes treaty outcome",lambda x:x["region_cases"][4].__setitem__("legal_anchor","IPO_ART_V_PAR_3")),
      ("Muenster false dating",lambda x:x["region_cases"][4].__setitem__("time_focus","1648–1649")),
      ("region source lost",lambda x:x["region_cases"][0]["source_keys"].clear()),
      ("local original falsely read",lambda x:x["region_cases"][1].__setitem__("post_treaty_local_original_records_read",True)),
      ("V35 estate court case made up",lambda x:x["article_35_implementation_topics"][1].__setitem__("regional_application_evidence_found",True)),
      ("V35 hospital admission made up",lambda x:x["article_35_implementation_topics"][2].__setitem__("regional_application_evidence_found",True)),
      ("V35 burial verdict made up",lambda x:x["article_35_implementation_topics"][3].__setitem__("regional_application_evidence_found",True)),
      ("methodical separation erased",lambda x:x.__setitem__("core_method","V3 and V35 are the same provision")),
      ("uncertainties erased",lambda x:x["editorial_holds"].clear()),
    ]
    for label,m in tests:assert_rejected(d,label,m)
    print(f"PASS: {len(tests)} false regional enforcement/canon/publication changes rejected; PUBLIC 0")

if __name__=="__main__":main()
