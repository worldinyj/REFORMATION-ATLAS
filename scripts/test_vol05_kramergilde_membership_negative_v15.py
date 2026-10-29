#!/usr/bin/env python3
"""Reject invented 1779 endpoint, confessional-denial outcomes and unreviewed image rights."""
from __future__ import annotations
import sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_kramergilde_membership_v15 import load,validate,REG

def expect_failure(base,name,mutation):
    x=copy.deepcopy(base);mutation(x)
    try:validate(x)
    except (KeyError,ValueError,TypeError,IndexError,StopIteration):return
    raise AssertionError("unverified guild fact promoted: "+name)

def main():
    d=load(REG)
    assert validate(d)["public"]==0
    mutations=[
      ("public",lambda d:d["publication_gate"].__setitem__("can_publish",True)),
      ("historian",lambda d:d["publication_gate"].__setitem__("historian_approved",True)),
      ("1931 page read",lambda d:d["publication_gate"].__setitem__("ketteler_1931_article_pages_read",True)),
      ("original guild book",lambda d:d["publication_gate"].__setitem__("original_kramergilde_member_book_read",True)),
      ("Neuhaus firsthand",lambda d:d["publication_gate"].__setitem__("anton_neuhaus_original_admission_read",True)),
      ("V35 verdict invented",lambda d:d["publication_gate"].__setitem__("confessional_exclusion_individual_verdict_verified",True)),
      ("image rights invented",lambda d:d["publication_gate"].__setitem__("visual_reuse_rights_approved",True)),
      ("main modified",lambda d:d.__setitem__("main_modified",True)),
      ("overview modified",lambda d:d.__setitem__("overview_modified",True)),
      ("app modified",lambda d:d.__setitem__("ai_studio_modified",True)),
      ("canonical ID created",lambda d:d.__setitem__("new_canonical_ids",1)),
      ("wrong treaty",lambda d:d.__setitem__("canonical_document_id","OV-D-014")),
      ("source removed",lambda d:d["sources"].pop()),
      ("unsafe URL",lambda d:d["sources"][0].__setitem__("url","http://example.org")),
      ("Archive.org falsely read",lambda d:d["sources"][5].__setitem__("access","FULL_SCAN_READ")),
      ("guild book falsely inspected",lambda d:d["sources"][2].__setitem__("original_guild_admissions_register_read",True)),
      ("1931 full page falsely read",lambda d:d["sources"][0].__setitem__("full_ketteler_1931_pages_read",True)),
      ("guild source image licensed",lambda d:d["sources"][4].__setitem__("source_image_reuse_cleared",True)),
      ("end year 1779 erroneous",lambda d:d["bibliographic_correction"].__setitem__("end_year",1779)),
      ("start year fabricated",lambda d:d["bibliographic_correction"].__setitem__("start_year",1661)),
      ("Ketteler pagination wrong",lambda d:d["bibliographic_correction"].__setitem__("pages_end",296)),
      ("article directly read fictitious",lambda d:d["bibliographic_correction"].__setitem__("full_scanned_article_text_directly_read",True)),
      ("no member",lambda d:d["individual_candidates"].clear()),
      ("Neuhaus religious classification",lambda d:d["individual_candidates"][0].__setitem__("religious_confession","REFORMED")),
      ("Neuhaus denied",lambda d:d["individual_candidates"][0].__setitem__("religious_exclusion_claim",True)),
      ("Neuhaus V35 lawsuit",lambda d:d["individual_candidates"][0].__setitem__("IPO_article_V35_invoked",True)),
      ("Neuhaus original archive guessed",lambda d:d["individual_candidates"][0].__setitem__("original_shelfmark","A II 0 fol 96r")),
      ("Neuhaus 1719 shifted",lambda d:d["individual_candidates"][0].__setitem__("admission_year",1720)),
      ("Neuhaus Amtsohn deleted",lambda d:d["individual_candidates"][0].__setitem__("admission_mode_original_reported","REJECTED")),
      ("oath order removed",lambda d:d["administrative_process"].__setitem__("citizen_oath_before_guild_membership","NOT_REQUIRED")),
      ("registration lag changed",lambda d:d["administrative_process"].__setitem__("guild_vs_treasury_register_timing_gap_years_max_reported",20)),
      ("treasury original falsely read",lambda d:d["administrative_process"].__setitem__("oath_admission_procedure_direct_read",True)),
      ("1810 abolition moved to 1661",lambda d:d["guild_house"].__setitem__("abolition_date","1661-08-22")),
      ("1810 members 142 declared new entries",lambda d:d["guild_house"].__setitem__("number_members_1810_from_1823_list",1420)),
      ("guild house 1589 changed",lambda d:d["guild_house"].__setitem__("original_construction_year",1648)),
      ("1810 date rewritten in timeline",lambda d:next(t for t in d["chronology"] if t["key"]=="K15-T-1810").__setitem__("date","1661-08-22")),
      ("timeline original read",lambda d:d["chronology"][0].__setitem__("primary_contemporary_text_read",True)),
      ("ambiguous extraction grain",lambda d:d["research_schema_proposal"].__setitem__("grain","TOTAL_COUNTS_ONLY")),
      ("unsafe inferences erased",lambda d:d["research_schema_proposal"]["prohibited_inferences"].clear()),
      ("followup dropped",lambda d:d["original_investigations"].pop()),
      ("editorial holds erased",lambda d:d["editorial_holds"].clear())
    ]
    for label,change in mutations:expect_failure(d,label,change)
    print(f"PASS: {len(mutations)} unsafe guild admission, edition-year, 1719 confession, 1810 abolishment and public/rights mutations rejected; PUBLIC 0")

if __name__=="__main__":main()
