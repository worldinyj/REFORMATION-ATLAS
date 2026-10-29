#!/usr/bin/env python3
"""Negative edition-access tests: no fictional 1931 p270 reading, guild folio or V35 person."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_kramergilde_archive_audit_v16 import read,validate,REG

def blocked(base,label,change):
    d=copy.deepcopy(base);change(d)
    try:validate(d)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("false admission/document claim passed: "+label)

def main():
    base=read(REG)
    assert validate(base)["public"]==0
    changes=[
      ("public",lambda x:x["publication_gate"].__setitem__("can_publish",True)),
      ("scholar",lambda x:x["publication_gate"].__setitem__("historian_approved",True)),
      ("p270 read",lambda x:x["publication_gate"].__setitem__("publisher_scan_p270_read",True)),
      ("1719 register read",lambda x:x["publication_gate"].__setitem__("original_1719_guild_entry_read",True)),
      ("current signature invented",lambda x:x["publication_gate"].__setitem__("current_kramergilde_register_shelfmark_confirmed",True)),
      ("V35 trial invented",lambda x:x["publication_gate"].__setitem__("individual_confessional_V35_lawsuit_verified",True)),
      ("image license fabricated",lambda x:x["publication_gate"].__setitem__("original_image_rights_approved",True)),
      ("main touched",lambda x:x.__setitem__("main_modified",True)),
      ("overview touched",lambda x:x.__setitem__("overview_modified",True)),
      ("studio touched",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("new ID",lambda x:x.__setitem__("new_canonical_ids",1)),
      ("wrong work",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("p270 declared actually read",lambda x:x["bibliography"].__setitem__("original_print_p270_read",True)),
      ("1719 source originally read",lambda x:x["bibliography"].__setitem__("original_member_register_read",True)),
      ("1719 member misnamed",lambda x:x["bibliography"].__setitem__("indirect_person","Another merchant")),
      ("1719 Amtsohn changed",lambda x:x["bibliography"].__setitem__("indirect_member_class","Denied")),
      ("wrong official pages",lambda x:x["bibliography"].__setitem__("printed_pages",[253,296])),
      ("delete academic source",lambda x:x["sources"].pop()),
      ("archive bad URL",lambda x:x["sources"][0].__setitem__("url","http://invalid.com")),
      ("IA item falsely opened",lambda x:x["sources"][1].__setitem__("access","FULL_1931_P270_READ")),
      ("Academy original p270 falsely read",lambda x:x["sources"][2].__setitem__("ketteler_1931_p270_read",True)),
      ("uni archive history original first-hand",lambda x:x["sources"][3].__setitem__("original_guild_read",True)),
      ("printed page task marked read",lambda x:x["reading_tasks"][1].__setitem__("result","FULLY_COLLATED")),
      ("guild archive source fabricated",lambda x:x["reading_tasks"][2].__setitem__("result","IDENTIFIED")),
      ("treasury original said seen",lambda x:x["reading_tasks"][3].__setitem__("result","ORIGINAL_READ")),
      ("entry source linked to original",lambda x:x["provenance_edges"][5].__setitem__("status","VERIFIED")),
      ("confession V35 ruled",lambda x:x["provenance_edges"][6].__setitem__("status","VERIFIED")),
      ("Ketteler archival role made 80K",lambda x:x["archival_history"].__setitem__("number_of_judicial_catalog_units_minimum",80000)),
      ("archive evacuation date invented",lambda x:x["archival_history"].__setitem__("archive_evacuated_year",1648)),
      ("same guild book claimed located",lambda x:x["archival_history"].__setitem__("never_claimed_same_kramergilde_book_located",False)),
      ("contact sent invented",lambda x:x["access_channels"][2].__setitem__("status","EMAIL_SENT")),
      ("public scan accessed invented",lambda x:x["access_channels"][0].__setitem__("status","PDF_RENDERED")),
      ("editorial limits removed",lambda x:x["editorial_limits"].clear())
    ]
    for label,fn in changes:blocked(base,label,fn)
    print(f"PASS: {len(changes)} fake Ketteler 1931 p270 readings, 1719 original sources, V35 cases and publication approvals rejected; PUBLIC 0")
if __name__=="__main__":main()
