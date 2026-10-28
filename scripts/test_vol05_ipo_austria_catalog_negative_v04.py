#!/usr/bin/env python3
"""Fail-closed test suite for 1648 original archive catalog evidence."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_ipo_austria_direct_catalog_v04 import read,validate,REG

def must_reject(base,title,transform):
    changed=copy.deepcopy(base)
    transform(changed)
    try: validate(changed)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration): return
    raise AssertionError("unsafe IPO catalog modification accepted: "+title)

def main():
    data=read(REG)
    assert validate(data)["public"]==0
    cases=[
      ("public",lambda d:d["publication_gate"].__setitem__("can_ship",True)),
      ("scholar",lambda d:d["publication_gate"].__setitem__("scholarly_approved",True)),
      ("editor",lambda d:d["publication_gate"].__setitem__("editorial_approved",True)),
      ("original Latin",lambda d:d["publication_gate"].__setitem__("physical_folios_collated",True)),
      ("1998 page",lambda d:d["publication_gate"].__setitem__("apw_original_page_collated",True)),
      ("image reuse",lambda d:d["publication_gate"].__setitem__("archive_photo_reuse_approved",True)),
      ("canonical ID",lambda d:d.__setitem__("canonical_ids_minted",1)),
      ("wrong work",lambda d:d.__setitem__("canonical_document_id","OV-D-014")),
      ("app mutated",lambda d:d.__setitem__("app_modified",True)),
      ("drop catalog",lambda d:d["direct_archival_catalogs"].pop()),
      ("change IPO to IPM",lambda d:d["direct_archival_catalogs"][0].__setitem__("treaty_key","WAR-TREATY-IPM-1648")),
      ("change IPM to IPO",lambda d:d["direct_archival_catalogs"][2].__setitem__("treaty_key","WAR-TREATY-IPO-1648")),
      ("wrong imperial record",lambda d:d["direct_archival_catalogs"][0].__setitem__("archive_item_id",2594304)),
      ("wrong Mainz IPO title",lambda d:d["direct_archival_catalogs"][1].__setitem__("copy_designation","Kaiserliches Exemplar")),
      ("wrong imperial seals",lambda d:d["direct_archival_catalogs"][0].__setitem__("seal_count",35)),
      ("wrong Mainz seals",lambda d:d["direct_archival_catalogs"][1].__setitem__("seal_count",41)),
      ("wrong IPM seal count",lambda d:d["direct_archival_catalogs"][2].__setitem__("seal_count",35)),
      ("image list count wrong",lambda d:d["direct_archival_catalogs"][0].__setitem__("listed_image_count",79)),
      ("images falsely read",lambda d:d["direct_archival_catalogs"][0].__setitem__("image_pixels_read",True)),
      ("manuscript falsely collated",lambda d:d["direct_archival_catalogs"][1].__setitem__("text_from_original_manuscript_read",True)),
      ("image rights fabricated",lambda d:d["direct_archival_catalogs"][2].__setitem__("rights_to_republish_images",True)),
      ("date-signature uniqueness fabricated",lambda d:d["direct_archival_catalogs"][2].__setitem__("shared_signature_uniquely_identifies_physical_copy",True)),
      ("imperial calendar shift",lambda d:d["direct_archival_catalogs"][0].__setitem__("original_catalog_date","1648-10-24")),
      ("unknown source URL",lambda d:d["direct_archival_catalogs"][1].__setitem__("uri","http://example.org")),
      ("PARES and Austrian equated",lambda d:d["indirect_catalogs_preserved"][0].__setitem__("relationship_to_new_direct_item_2594304","SAME_VERIFIED")),
      ("LWL and Austrian equated",lambda d:d["indirect_catalogs_preserved"][2].__setitem__("relationship_to_direct_items","SAME_VERIFIED")),
      ("APW edition year forged",lambda d:d["critical_edition"].__setitem__("edition_year",1648)),
      ("APW original text falsely read",lambda d:d["critical_edition"].__setitem__("text_page_photographed_or_direct_read",True)),
      ("121 page swapped",lambda d:d["secondary_page_corroborations"][0].__setitem__("reported_apw_page",129)),
      ("129 page swapped",lambda d:d["secondary_page_corroborations"][1].__setitem__("reported_apw_page",121)),
      ("academic citation upgraded",lambda d:d["secondary_page_corroborations"][1].__setitem__("apw_page_direct_read",True)),
      ("original Latin statement fabricated",lambda d:d["secondary_page_corroborations"][0].__setitem__("original_latin_verified",True)),
      ("unresolved erased",lambda d:d["unresolved"].clear()),
    ]
    for label,func in cases: must_reject(data,label,func)
    print(f"PASS: {len(cases)} unsafe manuscript/catalog/APW/copyright assertions rejected, PUBLIC 0")

if __name__=="__main__": main()
