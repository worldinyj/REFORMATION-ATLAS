#!/usr/bin/env python3
"""Adversarial mutations: wrong dates, source types, false article V35 judgments, fake approvals."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_guild_regulament_v13 import read,validate,REG

def denied(d,name,change):
    sample=copy.deepcopy(d);change(sample)
    try:validate(sample)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("illegal history claim accepted: "+name)
def main():
    d=read(REG);assert validate(d)["public"]==0
    changes=[
        ("publish",lambda x:x["release_gate"].__setitem__("can_publish",True)),
        ("historian",lambda x:x["release_gate"].__setitem__("historian_signed_off",True)),
        ("1661 original read",lambda x:x["release_gate"].__setitem__("original_1661_guild_regulament_read",True)),
        ("1681 original read",lambda x:x["release_gate"].__setitem__("original_1681_council_edict_read",True)),
        ("Bischof 1926 read",lambda x:x["release_gate"].__setitem__("modern_1926_Bischof_original_read",True)),
        ("V35 success",lambda x:x["release_gate"].__setitem__("post_1648_individual_v35_case_verified",True)),
        ("image clearance",lambda x:x["release_gate"].__setitem__("artwork_rights_cleared",True)),
        ("main modified",lambda x:x.__setitem__("main_modified",True)),
        ("app modified",lambda x:x.__setitem__("ai_studio_modified",True)),
        ("canon minted",lambda x:x.__setitem__("new_canonical_ids",1)),
        ("wrong original work",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
        ("source removed",lambda x:x["sources"].pop()),
        ("unsafe source",lambda x:x["sources"][0].__setitem__("url","http://untrusted.example")),
        ("Deter full HTML instead archive manuscript",lambda x:x["sources"][0].__setitem__("kind","FIRSTHAND_GUILD_ORIGINAL")),
        ("Weidner PDF screenshot was seen",lambda x:x["sources"][1].__setitem__("access_level","PDF_PAGE_IMAGES_AUTHENTICATED")),
        ("scholar article original text invented",lambda x:x["sources"][0].__setitem__("primary_1661_or_1681_manuscript_read",True)),
        ("museum original folio",lambda x:x["independent_check"].__setitem__("confirm_exact_1681_folio",True)),
        ("museum full guild law",lambda x:x["independent_check"].__setitem__("confirm_full_1661_guild_law",True)),
        ("1661 norm from Aug22 to Aug18",lambda x:x["chronology"][3].__setitem__("date","1661-08-18")),
        ("1681 edict moved to 1648",lambda x:x["chronology"][4].__setitem__("date","1648-10-24")),
        ("1690 statute moved 1661",lambda x:x["chronology"][5].__setitem__("date","1661-08-22")),
        ("1536 deleted",lambda x:x["chronology"].pop(0)),
        ("1690 item claimed firsthand",lambda x:x["chronology"][5].__setitem__("actual_dated_primary_text_read",True)),
        ("remove original target",lambda x:x["primary_witness_leads"].pop()),
        ("guild regulation shelfmark invented",lambda x:x["primary_witness_leads"][0].__setitem__("actual_17th_century_archive_shelfmark","MLA 413–4")),
        ("guild secondhand converted firsthand",lambda x:x["primary_witness_leads"][0].__setitem__("original_firsthand_transcription",True)),
        ("Bischof intermediary removed",lambda x:x["primary_witness_leads"][0].__setitem__("provenance","17th century guild law original read")),
        ("1661 election folio wrong",lambda x:x["primary_witness_leads"][1].__setitem__("label","Münster 1681 fol. 96r")),
        ("1681 edict folio wrong",lambda x:x["primary_witness_leads"][2].__setitem__("label","Münster 1681 fol. 95r")),
        ("MLA council draft called guild text",lambda x:x["primary_witness_leads"][3].__setitem__("actual_17th_century_archive_shelfmark","Unambiguous guild law 1661 Aug22")),
        ("corporate rule mislabeled 1681",lambda x:x["legal_effects"][0].__setitem__("instrument","1681 municipal election")),
        ("1690 jurisdiction falsely 1648",lambda x:x["legal_effects"][4].__setitem__("instrument","1648 IPO V35")),
        ("1681 election falsely 1661",lambda x:x["legal_effects"][5].__setitem__("instrument","1661 total sovereignty")),
        ("guild political primary certainty fabricated",lambda x:x["legal_effects"][1].__setitem__("direct_original_confirmation",True)),
        ("legal distinction erased",lambda x:x.__setitem__("historical_legal_boundary","Guild ban automatically proves IPO V35 denied individual")),
        ("all holds deleted",lambda x:x["unresolved"].clear()),
    ]
    for title,fn in changes:denied(d,title,fn)
    print(f"PASS: {len(changes)} unsafe Münster guild act, 1681 folio, V35 litigation, image rights and publication mutations rejected; PUBLIC 0")
if __name__=="__main__":main()
