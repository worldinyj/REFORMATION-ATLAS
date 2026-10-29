#!/usr/bin/env python3
"""Adversarial record mutations: historical 1653 Revers must never become unqualified IPO V35 litigation."""
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_1653_revers_v19 import load,validate,REG
def reject(base,label,mut):
    d=copy.deepcopy(base);mut(d)
    try:validate(d)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("false historical claim ACCEPTED: "+label)
def main():
    d=load(REG);assert validate(d)["public"]==0
    tests=[
        ("publish",lambda x:x["gates"].__setitem__("publish",True)),
        ("historian",lambda x:x["gates"].__setitem__("historian_approved",True)),
        ("APW full",lambda x:x["gates"].__setitem__("APW_pages_237_238_read",True)),
        ("1649 feb",lambda x:x["gates"].__setitem__("Feb1649_folio5v_read",True)),
        ("1649 mar",lambda x:x["gates"].__setitem__("Mar1649_folio13v_read",True)),
        ("1649 sep",lambda x:x["gates"].__setitem__("Sept1649_compromise_original_read",True)),
        ("1653 revers",lambda x:x["gates"].__setitem__("July1653_Revers_original_read",True)),
        ("1655 deed",lambda x:x["gates"].__setitem__("year1655_purchase_deed_read",True)),
        ("V35 verdict",lambda x:x["gates"].__setitem__("IPO_V35_individual_verdict_found",True)),
        ("media permission",lambda x:x["gates"].__setitem__("media_rights_cleared",True)),
        ("main",lambda x:x.__setitem__("main_modified",True)),
        ("studio",lambda x:x.__setitem__("ai_studio_modified",True)),
        ("canon minted",lambda x:x.__setitem__("new_canonical_ids",1)),
        ("different treaty ID",lambda x:x.__setitem__("canonical_document_id","OV-D-999")),
        ("parent changed",lambda x:x.__setitem__("parent","unverified-history.json")),
        ("lost source",lambda x:x["sources"].pop()),
        ("insecure source",lambda x:x["sources"][0].__setitem__("url","http://unknown.example")),
        ("1994 book original",lambda x:x["sources"][1].__setitem__("tier","DIRECT_1653_MANUSCRIPT")),
        ("APW protected website invented read",lambda x:x["sources"][4].__setitem__("tier","FULL_APW_CRITICAL_PAGES_READ")),
        ("unofficial text = authoritative",lambda x:x["sources"][8].__setitem__("tier","ORIGINAL_ARCHIVE_TEXT")),
        ("historical image rights fabricated",lambda x:x["sources"][3].__setitem__("image_rights_approved",True)),
        ("1642 arrival rewritten",lambda x:x["chronology"][0].__setitem__("date","1643")),
        ("1649 guild date rewritten",lambda x:x["chronology"][4].__setitem__("date","1653-07-04")),
        ("1649 september unapproved original",lambda x:x["chronology"][5].__setitem__("original_record_read",True)),
        ("1653 reversal same as 1649 refusal",lambda x:x["chronology"][6].__setitem__("date","1649-03-03")),
        ("1655 property earlier than revers",lambda x:x["chronology"][7].__setitem__("date","1647")),
        ("1653 Revers 30 not 12",lambda x:x["revers"].__setitem__("sisters_cap",30)),
        ("one house purchase forbidden",lambda x:x["revers"].__setitem__("one_house_allowed",False)),
        ("additional land unrestricted",lambda x:x["revers"].__setitem__("additional_land_restricted",False)),
        ("inheritance terms removed",lambda x:x["revers"].__setitem__("local_sisters_inheritance_waiver_reported",False)),
        ("German confessor removed",lambda x:x["revers"].__setitem__("German_secular_confessor_reported",False)),
        ("Papal provision removed",lambda x:x["revers"].__setitem__("papal_mendicant_order_condition_reported",False)),
        ("1653 original signature invented",lambda x:x["revers"].__setitem__("archive_shelfmark","A VIII 226 fol.5v")),
        ("1653 full original read invented",lambda x:x["revers"].__setitem__("contemporaneous_original_read",True)),
        ("1653 same act as permanent grant invented",lambda x:x["revers"].__setitem__("identical_to_permanent_residence_act_proven",True)),
        ("1964 editor altered",lambda x:x["edition"].__setitem__("editor","Another")),
        ("APW pagination 270",lambda x:x["edition"].__setitem__("pages","270")),
        ("APW falsely accessible",lambda x:x["edition"].__setitem__("digital_access","FULL_PAGE_READ")),
        ("APW text falsely read",lambda x:x["edition"].__setitem__("APW_full_text_read",True)),
        ("APW original folio altered",lambda x:x["edition"].__setitem__("original_city_folio","A II 20 Bd79 fol13v")),
        ("1653 archival signature invented",lambda x:x["original_leads"][4].__setitem__("locator","A XI 53")),
        ("1649 folio actually read fabricated",lambda x:x["original_leads"][0].__setitem__("original_read",True)),
        ("original chronology removed",lambda x:x["original_leads"].pop()),
        ("legal boundaries lost",lambda x:x["legal_boundaries"].clear()),
        ("archive research removed",lambda x:x["next_tasks"].pop())
    ]
    for name,mut in tests:reject(d,name,mut)
    print(f"PASS: {len(tests)} 1649/1653 false legal, timing, property, APW access and publication mutations rejected; PUBLIC 0")
if __name__=="__main__":main()
