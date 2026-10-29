#!/usr/bin/env python3
"""Negative-source assertions for 1670 woman/widow and old vs new guild source identity."""
from __future__ import annotations
import sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_kramergilde_three_people_v17 import load,validate,REG
def reject(base,name,fn):
    d=copy.deepcopy(base)
    fn(d)
    try:validate(d)
    except (ValueError,KeyError,IndexError,TypeError,StopIteration):return
    raise AssertionError("unsafe person/source inference passed: "+name)
def main():
    d=load(REG);assert validate(d)["published"]==0
    changes=[
      ("publish",lambda x:x["publication_gate"].__setitem__("can_publish",True)),
      ("historian approved",lambda x:x["publication_gate"].__setitem__("historian_approved",True)),
      ("1931 p270 falsely read",lambda x:x["publication_gate"].__setitem__("Ketteler_1931_p270_read",True)),
      ("1719 original falsely read",lambda x:x["publication_gate"].__setitem__("original_1719_register_read",True)),
      ("Geisberg 1934 p256 original falsely read",lambda x:x["publication_gate"].__setitem__("Geisberg_1934_p256_direct_read",True)),
      ("Geisberg Ketteler manuscript falsely equated",lambda x:x["publication_gate"].__setitem__("Geisberg_book_equated_to_Ketteler_original",True)),
      ("IPA V35 fake verdict",lambda x:x["publication_gate"].__setitem__("individual_IPO_V35_case_verified",True)),
      ("museum image clearance",lambda x:x["publication_gate"].__setitem__("art_rights_approved",True)),
      ("main branch modification",lambda x:x.__setitem__("main_modified",True)),
      ("Google app modification",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("new canon IDs",lambda x:x.__setitem__("new_canonical_ids",1)),
      ("wrong canon document",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("source removed",lambda x:x["sources"].pop()),
      ("http URL",lambda x:x["sources"][0].__setitem__("url","http://example.com")),
      ("local historian misrepresented as original",lambda x:x["sources"][0].__setitem__("direct_1719_original_read",True)),
      ("Geisberg 1934 p256 falsely seen",lambda x:x["sources"][4].__setitem__("direct_1931_page_read",True)),
      ("art allowed without rights",lambda x:x["sources"][6].__setitem__("media_rights_approved",True)),
      ("Maria removed",lambda x:x["person_candidates"].pop(0)),
      ("Maria year changed",lambda x:x["person_candidates"][0].__setitem__("year",1671)),
      ("Maria surname changed",lambda x:x["person_candidates"][0].__setitem__("name","Maria Other")),
      ("Maria widow erased",lambda x:x["person_candidates"][0].__setitem__("context","woman admitted as full member")),
      ("Maria promoted to original member",lambda x:x["person_candidates"][0].__setitem__("actual_original_member_row_read",True)),
      ("Maria religion fabricated",lambda x:x["person_candidates"][0].__setitem__("confession","REFORMED")),
      ("1719 Neuhaus denied",lambda x:x["person_candidates"][1].__setitem__("evidence_grade","REJECTED_FOR_FAITH")),
      ("1719 Amtsohn erased",lambda x:x["person_candidates"][1].__setitem__("context","Christian guild applicant")),
      ("1719 direct printed row fabricated",lambda x:x["person_candidates"][1].__setitem__("printed_1931_member_row_read",True)),
      ("1720 merchant original signature invented",lambda x:x["person_candidates"][2].__setitem__("original_archive_shelfmark","A II0 96r")),
      ("1720 person dated 1797",lambda x:x["person_candidates"][2].__setitem__("year",1797)),
      ("old guild book removed",lambda x:x["archival_book_leads"].pop()),
      ("Geisberg original book equated",lambda x:x["archival_book_leads"][0].__setitem__("proven_same_as_Ketteler_original",True)),
      ("Geisberg book pseudo shelfmark",lambda x:x["archival_book_leads"][0].__setitem__("modern_shelfmark","Stadtarchiv 5/270")),
      ("Gesamtgilde mistaken for Kramer",lambda x:x["archival_book_leads"][2].__setitem__("title","Ketteler 1719 guild book")),
      ("museum image download fabricated",lambda x:x["museum_objects"][0].__setitem__("downloaded",True)),
      ("museum rights fabricated",lambda x:x["museum_objects"][1].__setitem__("publishing_rights",True)),
      ("review marked complete",lambda x:x["remaining_checks"][0].__setitem__("completed",True)),
      ("holds removed",lambda x:x["editorial_limits"].clear())
    ]
    for name,fn in changes:reject(d,name,fn)
    print(f"PASS: {len(changes)} unsafe widow identity, 1719 status, Geisberg manuscript and §35 publication claims rejected; PUBLIC 0")
if __name__=="__main__":main()
