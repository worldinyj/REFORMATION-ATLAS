#!/usr/bin/env python3
"""Fail-closed mutation tests for Trent Latin/print witness boundaries."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_trent_latin_witness_v01 import read,validate,PATH

def reject(original,label,mutator):
    changed=copy.deepcopy(original)
    mutator(changed)
    try:
        validate(changed)
    except (ValueError, KeyError, TypeError, IndexError, StopIteration):
        return
    raise AssertionError("unsafe change accepted: "+label)

def main():
    base=read(PATH)
    assert validate(base)["released"] == 0
    attacks=[
      ("release", lambda d:d["publication_gate"].__setitem__("can_ship",True)),
      ("human", lambda d:d["publication_gate"].__setitem__("human_approved",True)),
      ("rights", lambda d:d["publication_gate"].__setitem__("copy_image_rights_approved",True)),
      ("collation", lambda d:d["publication_gate"].__setitem__("latin_print_collated",True)),
      ("parallel",lambda d:d["publication_gate"].__setitem__("parallel_translation_collated",True)),
      ("new ID",lambda d:d.__setitem__("created_canonical_ids",1)),
      ("new work",lambda d:d.__setitem__("work_id","OV-D-015")),
      ("wrong volume",lambda d:d.__setitem__("volume_id","VOL-04")),
      ("source promoted",lambda d:d["source_records"][0].__setitem__("canonical_source_id","SRC-123")),
      ("source image rights",lambda d:d["source_records"][0].__setitem__("rights_approved",True)),
      ("physical line verified",lambda d:d["source_records"][0].__setitem__("primary_print_folio_verified",True)),
      ("unsecured URL",lambda d:d["source_records"][0].__setitem__("url","http://invalid.example")),
      ("out of scope source",lambda d:d["source_records"][0].__setitem__("access","LATIN_DIRECT_1564")),
      ("publication",lambda d:d["anchors"][0].__setitem__("public_visible",True)),
      ("false Latin collation",lambda d:d["anchors"][0].__setitem__("physical_text_line_verified",True)),
      ("false parallel translation",lambda d:d["anchors"][0].__setitem__("full_latin_english_parallel_collation",True)),
      ("false source attribution",lambda d:d["anchors"][0].__setitem__("latin_display_source_key","TR-LAT-SRC-PROP-08")),
      ("wrong session",lambda d:d["anchors"][2].__setitem__("session_number",22)),
      ("wrong seminary type",lambda d:d["anchors"][3].__setitem__("section_kind","DOCTRINAL_DECREE_CHAPTER")),
      ("missing scholar caution",lambda d:d["anchors"][0].__setitem__("interpretation_guard","")),
      ("too long quote",lambda d:d["anchors"][0].__setitem__("latin_lemma"," ".join(["word"]*40))),
      ("1564 converted 1621",lambda d:d["print_copies"][4].__setitem__("printing_year",1564)),
      ("wrong 1564 format",lambda d:d["print_copies"][2].__setitem__("format","folio")),
      ("unverified shelfmark",lambda d:d["print_copies"][0].__setitem__("shelfmark","FORGED")),
      ("research hold erased",lambda d:d["relation_issues"].clear()),
    ]
    for name, fn in attacks:
        reject(base,name,fn)
    print(f"PASS: {len(attacks)} unsafe Latin witness/rights/edition regressions rejected, PUBLIC 0")

if __name__=="__main__":
    main()
