#!/usr/bin/env python3
"""Reject misleading source, edition, person and publication edits."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol04_prayerbook_research_v01 import load, validate

def reject(baseline,name,mutator):
    data=copy.deepcopy(baseline)
    mutator(data)
    try:
        validate(data)
    except (ValueError,KeyError,TypeError,IndexError):
        return
    raise AssertionError("research guard accepted an unsafe alteration: "+name)

def main():
    d=load("data/deep/vol04_prayerbook_editions_research_v01.json")
    assert validate(d)["public"]==0
    cases=[
      ("publish",lambda x:x["release_gate"].__setitem__("publication_approved",True)),
      ("rights",lambda x:x["release_gate"].__setitem__("rights_approved",True)),
      ("collated",lambda x:x.__setitem__("source_text_fully_collated",True)),
      ("wrong work",lambda x:x.__setitem__("canonical_work_id","OV-D-011")),
      ("wrong person",lambda x:x.__setitem__("canonical_person_id","OV-P-013")),
      ("fake witness rights",lambda x:x["sources"][0].__setitem__("reuse_rights_approved",True)),
      ("fake source authority",lambda x:x["sources"][0].__setitem__("canonical_source_id","SRC-O-999")),
      ("unverified text",lambda x:x["sources"][0].__setitem__("full_text_collated",True)),
      ("bad source",lambda x:x["sources"][0].__setitem__("url","http://invalid.example")),
      ("missing source",lambda x:x["sources"].pop()),
      ("wrong ed year",lambda x:x["edition_families"][0].__setitem__("year",1559)),
      ("cranmer compiling 1559",lambda x:x["edition_families"][2].__setitem__("compiled_by_cranmer",True)),
      ("1559 during life",lambda x:x["edition_families"][2].__setitem__("posthumous_to_cranmer",False)),
      ("new public id",lambda x:x["edition_families"][2].__setitem__("research_edition_key","EDN-V04-9999")),
      ("missing witness",lambda x:x["edition_families"][1]["print_witnesses"].clear()),
      ("witness source",lambda x:x["edition_families"][0]["print_witnesses"][0]["source_keys"].append("UNKNOWN")),
      ("duplicate witness",lambda x:x["edition_families"][2]["print_witnesses"][0].__setitem__("witness_key","PRB-WIT-PROP-1549-CHE")),
      ("wrong comparison",lambda x:x["comparisons"][0].__setitem__("comparison_type","OTHER")),
      ("collation fabricated",lambda x:x["comparisons"][0].__setitem__("original_edition_text_collated",True)),
      ("missing 1559",lambda x:x["comparisons"][0]["edition_keys"].pop()),
      ("rubric variation erased",lambda x:x["comparisons"][1].__setitem__("printing_variation_hold",False)),
      ("act conflation",lambda x:x.__setitem__("witness_warning","")),
      ("missing scholarly holds",lambda x:x["editorial_holds"].clear()),
    ]
    for name,mutator in cases:
        reject(d,name,mutator)
    print(f"PASS: {len(cases)} unsafe edition/provenance mutations rejected; public=0")

if __name__=="__main__":
    main()
