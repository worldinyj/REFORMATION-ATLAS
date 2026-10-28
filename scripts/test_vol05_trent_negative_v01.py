#!/usr/bin/env python3
"""Regression checks: prevent historically false promotion or date conflation."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_trent_research_v01 import read,validate

def rejected(baseline,label,mutate):
    changed=copy.deepcopy(baseline)
    mutate(changed)
    try: validate(changed)
    except (ValueError,KeyError,TypeError,StopIteration):return
    raise AssertionError("unsafe revision accepted: "+label)

def main():
    baseline=read("data/deep/vol05_trent_catholic_reform_registry_v01.json")
    assert validate(baseline)["public"]==0
    attacks=[
      ("release",lambda d:d["release_gate"].__setitem__("publication_approved",True)),
      ("human approval",lambda d:d["release_gate"].__setitem__("human_approved",True)),
      ("original collation",lambda d:d["release_gate"].__setitem__("original_text_collated",True)),
      ("rights",lambda d:d["release_gate"].__setitem__("media_rights_approved",True)),
      ("overview changed",lambda d:d.__setitem__("overview_modified",True)),
      ("canonical IDs minted",lambda d:d.__setitem__("created_canonical_ids",1)),
      ("wrong event ID",lambda d:d.__setitem__("canonical_event_id","OV-E-022")),
      ("wrong document ID",lambda d:d.__setitem__("canonical_document_id","OV-D-013")),
      ("wrong volume",lambda d:d.__setitem__("volume_id","VOL-04")),
      ("wrong phase dates",lambda d:d["phase_records"][2].__setitem__("year_start",1551)),
      ("false continuous phase",lambda d:d["phase_records"][1].__setitem__("opening","1547-01-01")),
      ("missing session",lambda d:d["sessions"].pop()),
      ("wrong justification date",lambda d:d["sessions"][1].__setitem__("date","1546-01-13")),
      ("Eucharist/Mass conflation",lambda d:d["sessions"][4].__setitem__("phase",2)),
      ("seminary ignored",lambda d:d["sessions"][5].__setitem__("subject","Holy Orders only")),
      ("source released",lambda d:d["source_records"][0].__setitem__("public_approved",True)),
      ("unregistered source",lambda d:d["sessions"][0]["source_keys"].append("TR-SRC-NOTFOUND")),
      ("unsecure evidence",lambda d:d["source_records"][0].__setitem__("url","http://not-secure.org")),
      ("false original edition",lambda d:d["sessions"][0].__setitem__("full_original_collation",True)),
      ("theological ambiguity erased",lambda d:d["interpretive_comparisons"][0].__setitem__("scholarly_debate_open",False)),
      ("one sided interpretation",lambda d:d["interpretive_comparisons"][0].__setitem__("participants",["CATHOLIC_TRENT_1547"])),
      ("ignatius created by Trent",lambda d:d["catholic_reform_context"][0].__setitem__("relation_to_trent","CREATED_BY_COUNCIL")),
      ("teresa wrong year",lambda d:d["catholic_reform_context"][1].__setitem__("year",1545)),
      ("scholarly holds erased",lambda d:d["editorial_holds"].clear())
    ]
    for label,mutate in attacks:rejected(baseline,label,mutate)
    print(f"PASS: {len(attacks)} unapproved/publication/chronology regressions rejected; PUBLIC 0")

if __name__=="__main__":main()
