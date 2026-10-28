#!/usr/bin/env python3
"""Reject unreviewed war narrative and 1648 treaty misattributions."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_war_westphalia_v01 import read,validate,REGISTRY

def reject(original,label,mutate):
    test=copy.deepcopy(original)
    mutate(test)
    try:
        validate(test)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):
        return
    raise AssertionError("unsafe historical revision accepted: "+label)

def main():
    base=read(REGISTRY)
    assert validate(base)["public"]==0
    attacks=[
        ("release permission",lambda d:d["release_gate"].__setitem__("can_ship",True)),
        ("historical editor bypass",lambda d:d["release_gate"].__setitem__("historical_editorial_approval",True)),
        ("treaty text collated",lambda d:d["release_gate"].__setitem__("original_treaty_text_collated",True)),
        ("image rights fabricated",lambda d:d["release_gate"].__setitem__("rights_approval",True)),
        ("new canonical ID",lambda d:d.__setitem__("canonical_ids_minted",1)),
        ("AI Studio changed",lambda d:d.__setitem__("ai_studio_modified",True)),
        ("wrong top-level work",lambda d:d.__setitem__("existing_document_id","OV-D-014")),
        ("missing event",lambda d:d["existing_event_ids"].remove("OV-E-024")),
        ("duplicate source key",lambda d:d["source_records"][1].__setitem__("source_key","WAR-SRC-01")),
        ("insecure source",lambda d:d["source_records"][0].__setitem__("url","http://invalid.example")),
        ("source public",lambda d:d["source_records"][0].__setitem__("public_visible",True)),
        ("source original falsely checked",lambda d:d["source_records"][0].__setitem__("complete_original_text_collated",True)),
        ("remove war phase",lambda d:d["conflict_periods"].pop()),
        ("wrong Swedish phase",lambda d:d["conflict_periods"][2].__setitem__("year_start",1629)),
        ("fake hiatus",lambda d:d["conflict_periods"][1].__setitem__("no_claim_of_armistice_between_phases",False)),
        ("IPO attributed to France",lambda d:d["treaty_instruments"][0].__setitem__("document_kind","IPM")),
        ("IPM signed in Osnabruck",lambda d:d["treaty_instruments"][1].__setitem__("site","Osnabrück")),
        ("Dutch signing falsely May",lambda d:d["treaty_instruments"][2].__setitem__("signing_date","1648-05-15")),
        ("Dutch ratification falsely October",lambda d:d["treaty_instruments"][2].__setitem__("ratification_oath_date","1648-10-24")),
        ("French Spanish treated same treaty",lambda d:d["treaty_instruments"][2]["not_same_as"].pop()),
        ("Reformed Article II mistake",lambda d:next(c for c in d["article_anchors"] if c["clause_key"]=="WAR-CL-IPO-VII-1").__setitem__("article","II")),
        ("1624 date confused with 1618",lambda d:next(c for c in d["article_anchors"] if c["clause_key"]=="WAR-CL-IPO-V-2").__setitem__("interpretation_label","NORMAL_YEAR_1618_01_01")),
        ("IPO clause linked to IPM",lambda d:d["article_anchors"][0].__setitem__("treaty_key","WAR-TREATY-IPM-1648")),
        ("incorrect claim of original collation",lambda d:d["article_anchors"][0].__setitem__("direct_original_language_collated",True)),
        ("clause source lost",lambda d:d["article_anchors"][0]["source_keys"].clear()),
        ("painting claims Oct IPO",lambda d:d["media_research_only"][0].__setitem__("actual_event_treaty_key","WAR-TREATY-IPO-1648")),
        ("painting date shifted October",lambda d:d["media_research_only"][0].__setitem__("event_date","1648-10-24")),
        ("National Gallery object forged",lambda d:d["media_research_only"][0].__setitem__("national_gallery_inventory","NG000")),
        ("art image downloaded",lambda d:d["media_research_only"][0].__setitem__("image_downloaded",True)),
        ("art rights fabricated",lambda d:d["media_research_only"][0].__setitem__("reproduction_rights_approved",True)),
        ("uncertainty hidden",lambda d:d["historical_holds"].clear()),
        ("counterparty no longer separate",lambda d:d["treaty_instruments"][0].__setitem__("not_same_as",[])),
    ]
    for label,mutate in attacks:
        reject(base,label,mutate)
    print(f"PASS: {len(attacks)} unsafe Westphalia war treaty or art mutations rejected; PUBLIC 0")

if __name__=="__main__":
    main()
