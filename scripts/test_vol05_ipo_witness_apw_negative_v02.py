#!/usr/bin/env python3
"""Mutations that must fail before IPO source catalog links can be published."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_ipo_witness_apw_v02 import load,validate,REL

def rejected(baseline,label,mutator):
    data=copy.deepcopy(baseline)
    mutator(data)
    try:
        validate(data)
    except (ValueError,KeyError,IndexError,TypeError,StopIteration):
        return
    raise AssertionError("unsafe research revision accepted: "+label)

def main():
    baseline=load(REL)
    assert validate(baseline)["public"]==0
    mutations=[
      ("approval",lambda d:d["publication_gate"].__setitem__("can_ship",True)),
      ("scholarly fabricated",lambda d:d["publication_gate"].__setitem__("scholar_approved",True)),
      ("apw directly compared fabricated",lambda d:d["publication_gate"].__setitem__("apw_primary_text_directly_compared",True)),
      ("original folios fabricated",lambda d:d["publication_gate"].__setitem__("original_manuscript_folios_collated",True)),
      ("rights fabricated",lambda d:d["publication_gate"].__setitem__("media_reuse_approved",True)),
      ("app changed",lambda d:d.__setitem__("ai_studio_modified",True)),
      ("new IDs",lambda d:d.__setitem__("new_canonical_ids",1)),
      ("wrong work",lambda d:d.__setitem__("canonical_work_id","OV-D-014")),
      ("wrong treaty event",lambda d:d.__setitem__("canonical_event_id","OV-E-023")),
      ("relabel LWL que2599",lambda d:d["sources"][0].__setitem__("url","https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=2595&url_tabelle=tab_quelle")),
      ("relabel LWL que2595",lambda d:d["sources"][1].__setitem__("url","https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=2599&url_tabelle=tab_quelle")),
      ("insecure source",lambda d:d["sources"][2].__setitem__("url","http://www.archivinformationssystem.at/")),
      ("fake photograph read",lambda d:d["sources"][0].__setitem__("authenticated_original_page_read",True)),
      ("APW portal read fabricated",lambda d:d["sources"][9].__setitem__("access","CRITICAL_TEXT_READ")),
      ("LWL PDF original",lambda d:d["sources"][6].__setitem__("kind","1648_SIGNED_ORIGINAL_FACSIMILE")),
      ("missing witness",lambda d:d["witnesses"].pop()),
      ("forged archival shelfmark",lambda d:d["witnesses"][0].__setitem__("exact_shelfmark","AT-OeStA/HHStA UR AUR 1648 X 14/24")),
      ("mistaken physical reading",lambda d:d["witnesses"][0].__setitem__("physical_image_read",True)),
      ("witness identity prematurely merged",lambda d:d["witnesses"][1].__setitem__("relationship_status","SAME_PHYSICAL_COPY")),
      ("IPO-K changed to IPM",lambda d:d["witnesses"][1].__setitem__("witness_type","IMPERIAL_FRENCH_TREATY")),
      ("wrong Oschmann",lambda d:d["editions"][0].__setitem__("editor","Other Editor")),
      ("wrong APW pages",lambda d:d["editions"][0].__setitem__("pages","33–71")),
      ("1998 critical text falsely read",lambda d:d["editions"][0].__setitem__("direct_text_read",True)),
      ("PDF changed to original",lambda d:d["editions"][2].__setitem__("kind","ORIGINAL_TREATY_SCAN")),
      ("duplicate anchor",lambda d:d["clause_links"][0].__setitem__("old_anchor_key","IPO-LAT-V-2")),
      ("fabricated original folio",lambda d:d["clause_links"][0].__setitem__("folio","f.20r")),
      ("fabricated APW page",lambda d:d["clause_links"][1].__setitem__("apw_edition_page","p.143")),
      ("original text directly compared",lambda d:d["clause_links"][0].__setitem__("original_document_directly_compared",True)),
      ("critical edited text directly compared",lambda d:d["clause_links"][0].__setitem__("critical_edition_directly_compared",True)),
      ("artificially closed holds",lambda d:d["unresolved"][0].__setitem__("status","CLOSED")),
    ]
    for label,mutator in mutations:
        rejected(baseline,label,mutator)
    print(f"PASS: {len(mutations)} forbidden IPO witness and publication mutations rejected; PUBLIC 0")

if __name__=="__main__":
    main()
