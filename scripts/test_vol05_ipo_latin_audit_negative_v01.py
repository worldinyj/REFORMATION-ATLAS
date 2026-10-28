#!/usr/bin/env python3
"""Fail-closed research mutation tests for the 1648 IPO Latin text audit."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_ipo_latin_audit_v01 import load,validate,REGISTRY

def must_reject(original,label,change):
    altered=copy.deepcopy(original)
    change(altered)
    try:
        validate(altered)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):
        return
    raise AssertionError("invalid IPO history change was accepted: "+label)

def main():
    data=load(REGISTRY)
    assert validate(data)["public_records"]==0
    cases=[
        ("publication",lambda d:d["release_gate"].__setitem__("publish",True)),
        ("human editorial clearance",lambda d:d["release_gate"].__setitem__("editorial_review",True)),
        ("scholarly clearance",lambda d:d["release_gate"].__setitem__("scholarly_review",True)),
        ("fake critical collation",lambda d:d["release_gate"].__setitem__("printed_latin_collated",True)),
        ("fabricated multilingual collation",lambda d:d["release_gate"].__setitem__("complete_multilingual_collation",True)),
        ("fabricated rights",lambda d:d["release_gate"].__setitem__("media_rights_approved",True)),
        ("new canonical IDs",lambda d:d.__setitem__("new_canonical_ids",1)),
        ("wrong corpus",lambda d:d.__setitem__("existing_work_id","OV-D-014")),
        ("IPO changed to IPM",lambda d:d.__setitem__("treaty_key","WAR-TREATY-IPM-1648")),
        ("app modified",lambda d:d.__setitem__("ai_studio_modified",True)),
        ("source URL unsecured",lambda d:d["source_records"][0].__setitem__("url","http://example.com")),
        ("source public",lambda d:d["source_records"][0].__setitem__("public_visible",True)),
        ("physical witness fiction",lambda d:d["source_records"][0].__setitem__("original_instrument_collated",True)),
        ("APW portal falsely fetched",lambda d:d["source_records"][3].__setitem__("access","LATIN_TEXT_READ_WEB")),
        ("critical edition falsely verified",lambda d:d["source_records"][3].__setitem__("critical_edition_verified",True)),
        ("wrong article for Reformed",lambda d:d["clause_anchors"][5].__setitem__("article","II")),
        ("Normaljahr wrong year",lambda d:d["clause_anchors"][1].__setitem__("claim_key","NORMAL_YEAR_1618")),
        ("erase coerced migration",lambda d:d["clause_anchors"][3].__setitem__("claim_key","COERCIVE_MIGRATION_ABOLISHED")),
        ("mismatch emigration paragraph",lambda d:d["clause_anchors"][4].__setitem__("paragraph","36")),
        ("sovereignty unlimited",lambda d:d["clause_anchors"][7].__setitem__("claim_key","UNRESTRICTED_SOVEREIGNTY")),
        ("original signed page fabricated",lambda d:d["clause_anchors"][0].__setitem__("original_signature_page","folio 10")),
        ("printed Latin falsely read",lambda d:d["clause_anchors"][0].__setitem__("original_print_read",True)),
        ("Latin English parallel falsely collated",lambda d:d["clause_anchors"][1].__setitem__("english_parallel_line_collated",True)),
        ("public clause",lambda d:d["clause_anchors"][2].__setitem__("publication_approved",True)),
        ("Latin English attribution swapped",lambda d:d["clause_anchors"][0].__setitem__("latin_source_key","IPO-SRC-02")),
        ("missing seventh article",lambda d:d["clause_anchors"].pop()),
        ("missing critical note",lambda d:d["crosscheck_notes"].pop()),
        ("empty holds",lambda d:d["critical_holds"].clear()),
        ("unverified publication status",lambda d:d.__setitem__("status","APPROVED")),
    ]
    for label,change in cases:
        must_reject(data,label,change)
    print(f"PASS: {len(cases)} unsafe IPO Latin/rights/article/forced-migration mutations rejected; PUBLIC 0")

if __name__=="__main__":
    main()
