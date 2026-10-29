#!/usr/bin/env python3
"""Münster citizen admission V1.0 negative evidence tests."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_citizenship_v10 import read,validate,REG

def rejects(obj,title,fn):
    d=copy.deepcopy(obj);fn(d)
    try:validate(d)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("unsafe Münster citizen-source edit passed: "+title)

def run():
    d=read(REG)
    assert validate(d)["public"]==0
    changes=[
      ("publish",lambda x:x["publication_gate"].__setitem__("can_publish",True)),
      ("human review",lambda x:x["publication_gate"].__setitem__("human_scholar_approved",True)),
      ("copy original read",lambda x:x["publication_gate"].__setitem__("copy_1626_primary_transcribed",True)),
      ("MLA expanded",lambda x:x["publication_gate"].__setitem__("archival_MLA_413_5_identified",True)),
      ("Bürgerbrief original read",lambda x:x["publication_gate"].__setitem__("original_1677_citizen_letter_read",True)),
      ("V35 law case fabricated",lambda x:x["publication_gate"].__setitem__("explicit_V35_case_adjudicated",True)),
      ("image republished",lambda x:x["publication_gate"].__setitem__("contemporary_art_rights_verified",True)),
      ("web app touched",lambda x:x.__setitem__("ai_studio_changed",True)),
      ("new IDs",lambda x:x.__setitem__("new_canonical_ids",1)),
      ("wrong treaty",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("remove academic source",lambda x:x["sources"].pop()),
      ("insecure source",lambda x:x["sources"][0].__setitem__("url","http://invalid.example")),
      ("Gimpel PDF claimed visually seen",lambda x:x["sources"][1].__setitem__("access","FULL_PDF_VISUAL_READ")),
      ("Weidner page screenshot lied",lambda x:x["sources"][2].__setitem__("access","ORIGINAL_1661_MS_READ")),
      ("source original read",lambda x:x["sources"][3].__setitem__("primary_17th_century_object_read",True)),
      ("photo rights fabricated",lambda x:x["sources"][8].__setitem__("media_reuse_cleared",True)),
      ("remove 1661 record",lambda x:x["artifact_records"].pop(0)),
      ("1661 copy becomes original",lambda x:x["artifact_records"][0].__setitem__("material_witness","ORIGINAL_1661_PARCHMENT")),
      ("1661 normative reporting erased",lambda x:x["artifact_records"][0].__setitem__("reporting_non_catholics","ABSENT")),
      ("1661 council date confused",lambda x:x["artifact_records"][1].__setitem__("original_act_date","1661-08-13")),
      ("MLA copy claim",lambda x:x["artifact_records"][2].__setitem__("holding","Landesarchiv 1626 same original verified")),
      ("1677 citizenship date changed",lambda x:x["artifact_records"][3].__setitem__("original_act_date","1661-05-15")),
      ("1677 applicant sanctioned",lambda x:x["artifact_records"][3].__setitem__("actual_noncatholic_person_sanctioned",True)),
      ("1677 rejection invented",lambda x:x["citizenship_1677"].__setitem__("religious_exclusion_of_non_catholics_directly_proved",True)),
      ("IPO V35 trial invented",lambda x:x["citizenship_1677"].__setitem__("IPO_V35_explicitly_invoked",True)),
      ("1677 original folio invented",lambda x:x["citizenship_1677"].__setitem__("individual_folio_signature_verified","f. 74r")),
      ("person name changed",lambda x:x["citizenship_1677"].__setitem__("person_name_original_reported","Another name")),
      ("magistrate swapped",lambda x:x["citizenship_1677"].__setitem__("reported_magistrate","Another magistrate")),
      ("witnesses removed",lambda x:x["citizenship_1677"]["witnesses_reported"].clear()),
      ("followup false original",lambda x:x["archival_followups"][0].__setitem__("direct_source_read",True)),
      ("MLA falsely identified",lambda x:x["archival_followups"][0].__setitem__("copy_or_original_status","ORIGINAL_1661")),
      ("political image shown as citizen letter",lambda x:x["visual_reference_candidate"].__setitem__("linked_to_1677_civic_letter",True)),
      ("downloaded image falsely licensed",lambda x:x["visual_reference_candidate"].__setitem__("cleared_for_webapp",True)),
      ("source cautions removed",lambda x:x["historical_interpretation"].clear()),
    ]
    for title,fn in changes:rejects(d,title,fn)
    print(f"PASS: {len(changes)} false witness, named-1677 citizen, confession, copyright and public-release changes rejected; PUBLIC 0")

if __name__=="__main__":run()
