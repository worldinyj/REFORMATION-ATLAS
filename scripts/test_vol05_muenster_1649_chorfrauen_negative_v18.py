#!/usr/bin/env python3
"""Negative cases: reject mixed archival folios, invented 1649 denials, automatic guild-widow rights."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_1649_chorfrauen_v18 import load,validate,REG

def reject(base,name,mut):
    x=copy.deepcopy(base);mut(x)
    try:validate(x)
    except (ValueError,TypeError,KeyError,IndexError,StopIteration):return
    raise AssertionError("unsupported early-modern claim passed: "+name)
def main():
    base=load(REG);assert validate(base)["published"]==0
    edits=[
      ("published",lambda x:x["gates"].__setitem__("public_approved",True)),
      ("scholar",lambda x:x["gates"].__setitem__("historian_review",True)),
      ("1649 Feb folio falsely read",lambda x:x["gates"].__setitem__("council_1649_feb_original_read",True)),
      ("1649 Mar original",lambda x:x["gates"].__setitem__("guild_1649_mar_original_read",True)),
      ("1647 original",lambda x:x["gates"].__setitem__("episcopal_1647_mandate_original_read",True)),
      ("APW critical edition read",lambda x:x["gates"].__setitem__("APW_III_D1_pages_original_read",True)),
      ("red book read",lambda x:x["gates"].__setitem__("red_book_original_read",True)),
      ("IPO individual lawsuit",lambda x:x["gates"].__setitem__("individual_IPO_V35_lawsuit_confirmed",True)),
      ("image permissions",lambda x:x["gates"].__setitem__("visual_rights_cleared",True)),
      ("main changed",lambda x:x.__setitem__("main_modified",True)),
      ("overview changed",lambda x:x.__setitem__("overview_modified",True)),
      ("app changed",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("new ID",lambda x:x.__setitem__("new_canonical_ids",1)),
      ("wrong original doc",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("source omitted",lambda x:x["sources"].pop()),
      ("insecure URL",lambda x:x["sources"][0].__setitem__("url","http://www.example.org")),
      ("Jakobi misrepresented as primary",lambda x:x["sources"][0].__setitem__("original_17c_document_read",True)),
      ("OUP chapter falsely read",lambda x:x["sources"][4].__setitem__("tier","BOOK_COMPLETE_TEXT_COLLATED")),
      ("museum copyrighted artwork approved",lambda x:x["sources"][3].__setitem__("media_rights_approved",True)),
      ("folio missing",lambda x:x["folios"].pop()),
      ("Feb 25 becomes Mar 3",lambda x:x["folios"][0].__setitem__("date","1649-03-03")),
      ("Feb 25 folio swapped",lambda x:x["folios"][0].__setitem__("scholar_locator","A II 20 Bd79 fol13v")),
      ("Mar 3 folio swapped",lambda x:x["folios"][1].__setitem__("scholar_locator","Stadtarchiv Münster A II 20 Bd. 79 fol. 5v")),
      ("1647 attached original falsely read",lambda x:x["folios"][2].__setitem__("original_read",True)),
      ("guild red book equated Ketteler",lambda x:x["folios"][3].__setitem__("scholar_locator","Ketteler 1931 1719 p270")),
      ("APW original actually seen",lambda x:x["folios"][0].__setitem__("critical_edition_directly_read",True)),
      ("APW wrong page",lambda x:x["folios"][0].__setitem__("edition","APW III D1 p100")),
      ("1649 council declared full consent",lambda x:x["positions"][0].__setitem__("position","UNCONDITIONAL_COMPLETE_CONSENT")),
      ("guild approved settlement",lambda x:x["positions"][1].__setitem__("position","APPROVED_FORCED_SETTLEMENT")),
      ("papal delegates misdated",lambda x:x["positions"][2].__setitem__("date","1661")),
      ("episcopal mandate misdated",lambda x:x["positions"][3].__setitem__("date","1649-03-03")),
      ("1589 member count invented",lambda x:x["guild_house_widow_participation"].__setitem__("guild_members_present",820)),
      ("1589 widows 0",lambda x:x["guild_house_widow_participation"].__setitem__("widows_of_masters_present",0)),
      ("widow = auto guild member",lambda x:x["guild_house_widow_participation"].__setitem__("independent_member_rights_proven",True)),
      ("Maria wrongly confirmed by 1589 count",lambda x:x["guild_house_widow_participation"].__setitem__("does_not_confirm_Maria_Schuerman_1670_membership",False)),
      ("municipal religious school = V35 verdict",lambda x:x["legal_distinctions"][0].__setitem__("individual_IPO_V35_case",True)),
      ("rights claim made local court case",lambda x:x["legal_distinctions"][1].__setitem__("verified_as_regional_governance_case",True)),
      ("one event removed",lambda x:x["events"].pop()),
      ("1649 Feb became 1648 treaty",lambda x:x["events"][3].__setitem__("date","1648-10-24")),
      ("1649 Mar original falsely read",lambda x:x["events"][4].__setitem__("dated_original_folio_read",True)),
      ("critical caveats removed",lambda x:x["caveats"].clear()),
      ("next original work removed",lambda x:x["next_original_work"].pop())
    ]
    for name,mut in edits:reject(base,name,mut)
    print(f"PASS: {len(edits)} unsafe Münster canoness, council folio, widow guild rights, article V35 and public-release changes rejected; PUBLIC 0")
if __name__=="__main__":main()
