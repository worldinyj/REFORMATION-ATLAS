#!/usr/bin/env python3
"""Reject fabricated IPO archive IDs and APW page authorizations."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_ipo_archive_ids_v03 import read,validate,REG

def reject(base,name,func):
    data=copy.deepcopy(base)
    func(data)
    try: validate(data)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration): return
    raise AssertionError("unsafe research change accepted: "+name)

def main():
    base=read(REG)
    assert validate(base)["public"]==0
    cases=[
      ("publication",lambda d:d["publication_gate"].__setitem__("can_publish",True)),
      ("scholar",lambda d:d["publication_gate"].__setitem__("human_scholarly_approved",True)),
      ("rights",lambda d:d["publication_gate"].__setitem__("rights_approved",True)),
      ("original",lambda d:d["publication_gate"].__setitem__("original_item_verified",True)),
      ("physical read",lambda d:d["publication_gate"].__setitem__("physical_foil_read",True)),
      ("APW read",lambda d:d["publication_gate"].__setitem__("apw_1998_direct_text_read",True)),
      ("webapp changed",lambda d:d.__setitem__("existing_app_changed",True)),
      ("new ID",lambda d:d.__setitem__("new_canonical_ids",1)),
      ("wrong work",lambda d:d.__setitem__("canonical_work_id","OV-D-014")),
      ("source insecure",lambda d:d["source_records"][0].__setitem__("url","http://example.org")),
      ("source text collated",lambda d:d["source_records"][1].__setitem__("text_completely_collated",True)),
      ("source rights",lambda d:d["source_records"][0].__setitem__("publication_rights_approved",True)),
      ("date-group unique",lambda d:d["archive_reference_group"].__setitem__("is_unique_physical_copy_signature",True)),
      ("archive date forged",lambda d:d["archive_reference_group"].__setitem__("referenced_fonds_or_group","AT-OeStA/HHStA 1618 X 24")),
      ("source removed",lambda d:d["source_records"].pop()),
      ("IPO to IPM",lambda d:d["archival_item_leads"][0].__setitem__("treaty_key","WAR-TREATY-IPM-1648")),
      ("IPM to IPO",lambda d:d["archival_item_leads"][1].__setitem__("treaty_key","WAR-TREATY-IPO-1648")),
      ("wrong archive item",lambda d:d["archival_item_leads"][0].__setitem__("registry_numeric_id",1252067)),
      ("record falsely read",lambda d:d["archival_item_leads"][0].__setitem__("direct_record_read",True)),
      ("image falsely found",lambda d:d["archival_item_leads"][0].__setitem__("original_image_found",True)),
      ("LWL prematurely equated",lambda d:d["lwl_registrations"][0].__setitem__("same_as_austrian_393786","YES")),
      ("APW wrong year",lambda d:d["critical_edition"].__setitem__("year",1648)),
      ("APW wrong range",lambda d:d["critical_edition"].__setitem__("pages_range","33–71")),
      ("critical text allegedly read",lambda d:d["critical_edition"].__setitem__("primary_latin_page_directly_inspected",True)),
      ("p121 inspected",lambda d:d["apw_indirect_page_leads"][0].__setitem__("direct_page_inspected",True)),
      ("p129 latin verified",lambda d:d["apw_indirect_page_leads"][1].__setitem__("verified_latin_words",True)),
      ("candidate upgraded",lambda d:d["apw_indirect_page_leads"][0].__setitem__("editorial_status","VERIFIED")),
      ("V34 page wrong",lambda d:d["apw_indirect_page_leads"][0].__setitem__("reported_printed_page",129)),
      ("VII1 page wrong",lambda d:d["apw_indirect_page_leads"][1].__setitem__("reported_printed_page",121)),
      ("holds closed",lambda d:d["unresolved"][0].__setitem__("status","CLOSED")),
    ]
    for label,func in cases: reject(base,label,func)
    print(f"PASS: {len(cases)} unsafe archive and tentative edition-page mutations rejected; PUBLIC 0")

if __name__=="__main__": main()
