#!/usr/bin/env python3
"""Fail-closed negative test of MLA and modern Zumbusch fonds references."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_archive_crosswalk_v11 import load,validate,REG

def reject(base,name,change):
    d=copy.deepcopy(base);change(d)
    try:validate(d)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("unsafe source manipulation accepted: "+name)

def main():
    d=load(REG)
    assert validate(d)["published"]==0
    edits=[
      ("publish",lambda x:x["publication_gate"].__setitem__("can_publish",True)),
      ("historian",lambda x:x["publication_gate"].__setitem__("historian_approved",True)),
      ("MLA original read",lambda x:x["publication_gate"].__setitem__("MLA_original_folio_read",True)),
      ("copy 1626 read",lambda x:x["publication_gate"].__setitem__("Urkunden_1626_copy_read",True)),
      ("letter currently found",lambda x:x["publication_gate"].__setitem__("original_1677_letter_located_currently",True)),
      ("original read",lambda x:x["publication_gate"].__setitem__("original_1677_letter_read",True)),
      ("V35 verdict invented",lambda x:x["publication_gate"].__setitem__("V35_individual_case_proven",True)),
      ("media rights",lambda x:x["publication_gate"].__setitem__("images_rights_cleared",True)),
      ("main changed",lambda x:x.__setitem__("main_modified",True)),
      ("new OV IDs",lambda x:x.__setitem__("new_canonical_ids",1)),
      ("AI Studio changed",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("wrong doc canonical",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("one source lost",lambda x:x["sources"].pop()),
      ("broken URL",lambda x:x["sources"][0].__setitem__("url","http://fake.example")),
      ("complete Gimpel PDF falsely seen",lambda x:x["sources"][4].__setitem__("access","FULL_PDF_ORIGINAL_TEXT")),
      ("first original read",lambda x:x["sources"][1].__setitem__("original_physical_document_read",True)),
      ("DDB photo rights",lambda x:x["sources"][5].__setitem__("redistribution_rights_cleared",True)),
      ("MLA wrong institution",lambda x:x["archive_links"][0].__setitem__("expanded","Münster Stadtarchiv")),
      ("MLA abbreviation erased",lambda x:x["archive_links"][0].__setitem__("abbreviation_resolved",False)),
      ("MLA folios become original read",lambda x:x["archive_links"][0].__setitem__("original_folio_read",True)),
      ("MLA 4135 exchanged",lambda x:x["archive_links"][1].__setitem__("label","MLA 413–6 fol. 126r–128r")),
      ("same MLA and 1626 physical copy claimed",lambda x:x["archive_links"][1].__setitem__("identical_to_LWL1626","YES_VERIFIED")),
      ("MLA folio falsely read",lambda x:x["archive_links"][1].__setitem__("witness_directly_read",True)),
      ("1982 unlisted ignored",lambda x:x["archive_links"][2].__setitem__("old_catalog_state","CURRENTLY_INDEXED_AS_1677")),
      ("1982 original present shelfmark fabricated",lambda x:x["archive_links"][2].__setitem__("current_individual_shelfmark","C-Arm Zumbusch 28")),
      ("found as present letter",lambda x:x["archive_links"][3].__setitem__("specific_1677_letter_in_modern_catalog","FOUND")),
      ("Akten28 becomes letter",lambda x:x["archive_links"][3]["examples"][0].__setitem__("is_1677_letter",True)),
      ("Urk37 becomes letter",lambda x:x["archive_links"][3]["examples"][1].__setitem__("is_1677_letter",True)),
      ("Akten28 changes years",lambda x:x["archive_links"][3]["examples"][0].__setitem__("date","1677")),
      ("1677 applicant renamed",lambda x:x["letter_metadata"].__setitem__("person","Grete Other")),
      ("1677 denied letter fabricated",lambda x:x["letter_metadata"].__setitem__("unlawful_citizenship_denial_established",True)),
      ("V35 used fabricated",lambda x:x["letter_metadata"].__setitem__("IPO_V35_cited",True)),
      ("1677 current shelf invented",lambda x:x["letter_metadata"].__setitem__("current_shelfmark","C-Arm Zumbusch 28")),
      ("1677 original read fabricated",lambda x:x["letter_metadata"].__setitem__("physical_original_read",True)),
      ("1661 texts collated fabricated",lambda x:x["crosswalk_tests"][0].__setitem__("verbatim_collation",True)),
      ("same physical 1661 source fabricated",lambda x:x["crosswalk_tests"][0].__setitem__("same_physical_copy","YES")),
      ("current fonds proof becomes letter",lambda x:x["crosswalk_tests"][1].__setitem__("individual_letter_item_found",True)),
      ("council record merged with judge rule",lambda x:x["crosswalk_tests"][2].__setitem__("same_physical_record",True)),
      ("followup claimed done",lambda x:x["next_target"][0].__setitem__("found",True)),
      ("editorial holds gone",lambda x:x["editorial_holds"].clear()),
    ]
    for name,fn in edits:reject(d,name,fn)
    print(f"PASS: {len(edits)} fabricated MLA/1677 Bürgerbrief identity, rights, V35 and publication mutations rejected; PUBLIC 0")

if __name__=="__main__":main()
