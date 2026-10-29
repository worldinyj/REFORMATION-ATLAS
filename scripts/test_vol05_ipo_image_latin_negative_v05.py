#!/usr/bin/env python3
"""Guard against falsely promoting unviewed image frames and web Latin text."""
from __future__ import annotations
import sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_ipo_image_latin_v05 import load,validate,REG

def must_fail(base,title,mutation):
    d=copy.deepcopy(base)
    mutation(d)
    try:validate(d)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("unsafe V05 evidence change accepted: "+title)

def main():
    d=load(REG)
    assert validate(d)["released"]==0
    tests=[
      ("publish",lambda x:x["release_gate"].__setitem__("publication_approved",True)),
      ("scholar review",lambda x:x["release_gate"].__setitem__("scholar_signed_off",True)),
      ("photos rights",lambda x:x["release_gate"].__setitem__("image_redistribution_licensed",True)),
      ("original folios",lambda x:x["release_gate"].__setitem__("original_manuscript_folios_collated",True)),
      ("APW pages",lambda x:x["release_gate"].__setitem__("apw_1998_printed_pages_reviewed",True)),
      ("AI Studio",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("canonical ids",lambda x:x.__setitem__("canonical_ids_created",1)),
      ("wrong work",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("false image pixels",lambda x:x["archive_image_access_tests"][0].__setitem__("image_pixels_verified",True)),
      ("false folio",lambda x:x["archive_image_access_tests"][1].__setitem__("folio_number","f. 31r")),
      ("false clause on image",lambda x:x["archive_image_access_tests"][2].__setitem__("clause_found_on_image","IPO V §34")),
      ("fake image URL",lambda x:x["archive_image_access_tests"][0].__setitem__("linked_preview_url_observed","https://fake.invalid/img.png")),
      ("wrong image serial",lambda x:x["archive_image_access_tests"][0].__setitem__("image_index_observed",42)),
      ("fake successful image fetch",lambda x:x["archive_image_access_tests"][1].__setitem__("web_fetch_outcome","PASS")),
      ("APW portal read",lambda x:x["edition_access_tests"][0].__setitem__("outcome","TEXT_READ")),
      ("p121 claimed read",lambda x:x["edition_access_tests"][2].__setitem__("printed_pages_read",[121])),
      ("volunteer transcription called APW",lambda x:x["online_latin_source"].__setitem__("not_apw_1998_text",False)),
      ("text source called original",lambda x:x["online_latin_source"].__setitem__("not_authenticated_1648_witness",False)),
      ("second source independence asserted",lambda x:x["second_latin_source"].__setitem__("text_independence_unproven",False)),
      ("remove V35",lambda x:x["latin_clause_review"].pop(3)),
      ("V35 ref claimed original",lambda x:x["latin_clause_review"][3].__setitem__("original_printed_text_checked",True)),
      ("V34 APW invented",lambda x:x["latin_clause_review"][2].__setitem__("apw_edition_page_directly_read",121)),
      ("V37 original image invented",lambda x:x["latin_clause_review"][5].__setitem__("original_image_page",57)),
      ("VII1 mislocated",lambda x:x["latin_clause_review"][6].__setitem__("article","V")),
      ("V35 status promoted",lambda x:x["latin_clause_review"][3].__setitem__("status","APPROVED_ORIGINAL")),
      ("new theme canonical",lambda x:x["new_historical_insight"].__setitem__("old_canonical_article_modified",True)),
      ("lose caution",lambda x:x["unresolved"].clear()),
    ]
    for label,change in tests:must_fail(d,label,change)
    print(f"PASS: {len(tests)} illegal manuscript/edition/web-publication claims rejected; PUBLIC 0")

if __name__=="__main__":main()
