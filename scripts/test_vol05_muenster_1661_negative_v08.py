#!/usr/bin/env python3
"""Deliberately invalid history/evidence mutations must never validate."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_1661_v08 import load,validate,REG

def must_reject(base,title,func):
    altered=copy.deepcopy(base);func(altered)
    try:validate(altered)
    except (ValueError,KeyError,IndexError,TypeError,StopIteration):return
    raise AssertionError("unsafe source promotion was accepted: "+title)

def main():
    d=load(REG);assert validate(d)["public"]==0
    mods=[
      ("publish",lambda x:x["publication_gate"].__setitem__("can_publish",True)),
      ("historian approval",lambda x:x["publication_gate"].__setitem__("historian_review",True)),
      ("original manuscripts read",lambda x:x["publication_gate"].__setitem__("original_manuscripts_read",True)),
      ("V35 judgment falsely found",lambda x:x["publication_gate"].__setitem__("individual_V35_rights_enforcement_verified",True)),
      ("IPO manuscript falsely collated",lambda x:x["publication_gate"].__setitem__("original_IPO_latin_collated",True)),
      ("photo license fabricated",lambda x:x["publication_gate"].__setitem__("media_rights_approved",True)),
      ("create canonical IDs",lambda x:x.__setitem__("new_canonical_ids",1)),
      ("AI Studio changed",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("wrong treaty work",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("remove source",lambda x:x["sources"].pop()),
      ("http archive URL",lambda x:x["sources"][0].__setitem__("url","http://archive.invalid")),
      ("DDB original suddenly copy",lambda x:x["sources"][0].__setitem__("kind","LWL_REGEST_OF_18TH_C_COPY")),
      ("LWL original falsely direct",lambda x:x["sources"][1].__setitem__("kind","1661_ORIGINAL_TEXT_READ")),
      ("1661 original read falsely",lambda x:x["sources"][0].__setitem__("direct_original_document_text_read",True)),
      ("photo rights falsely certified",lambda x:x["sources"][0].__setitem__("licensed_for_image_reuse",True)),
      ("shelf entry swapped",lambda x:x["document_records"][0].__setitem__("legacy_signature","Nr. 1626")),
      ("original becomes paper copy",lambda x:x["document_records"][0].__setitem__("catalog_declared_witness_type","18TH_CENTURY_PAPER_COPY_OF_1661_REGULATION")),
      ("Senden incorrectly generalized",lambda x:x["document_records"][0].__setitem__("legal_scope","Entire Münster civic independence dissolved")),
      ("copy 1626 becomes 1661 original",lambda x:x["document_records"][1].__setitem__("catalog_declared_witness_type","ORIGINAL_PARCHMENT")),
      ("copy 1627 becomes 1661 original",lambda x:x["document_records"][2].__setitem__("catalog_declared_witness_type","ORIGINAL_PARCHMENT")),
      ("LWL 1626 and 1627 swapped",lambda x:x["document_records"][1].__setitem__("legacy_signature","Nr. 1627")),
      ("August thirteen falsely digitized",lambda x:x["document_records"][1].__setitem__("digitization_reported",True)),
      ("August eighteen false religious report",lambda x:x["document_records"][2].__setitem__("religious_subject_reporting",True)),
      ("nonCatholic reporting erased",lambda x:x["document_records"][1].__setitem__("religious_subject_reporting",False)),
      ("fake expulsion trial",lambda x:x["document_records"][1].__setitem__("explicit_IPO_article_V35_in_document",True)),
      ("invented original reading",lambda x:x["document_records"][0].__setitem__("original_witness_text_collated",True)),
      ("fictitious original frame count",lambda x:x["document_records"][0].__setitem__("digitized_image_count",44)),
      ("timeline removed",lambda x:x["chronology"].pop()),
      ("Vienna case shelfmark invented",lambda x:x["archival_investigation_next"][0].__setitem__("exact_case_signature","AT-OeStA 1661 Original fol 99")),
      ("city council primary read fabricated",lambda x:x["archival_investigation_next"][3].__setitem__("original_file_read",True)),
      ("interpretive holds erased",lambda x:x["historical_interpretation_guardrails"].clear()),
      ("unlicensed art selected",lambda x:x["representative_image_policy"].__setitem__("selected_artwork","Ter Borch 1648")),
      ("Dutch-Spain painting wrongly reused",lambda x:x["representative_image_policy"].__setitem__("avoid_ter_borch_dutch_spanish_1648_picture_as_1661_muenster_bishop_event",False)),
    ]
    for label,change in mods:must_reject(d,label,change)
    print(f"PASS: {len(mods)} unsafe Münster 1661 history/copy/original/IPO publication changes rejected; PUBLIC 0")

if __name__=="__main__":main()
