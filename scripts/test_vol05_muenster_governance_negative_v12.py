#!/usr/bin/env python3
"""Reject counterfactual chronology, forged folios, private-law verdicts and release."""
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_governance_v12 import read,validate,REG

def fail_as_expected(base,label,change):
    d=copy.deepcopy(base)
    change(d)
    try:validate(d)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("unsafe history edit was ACCEPTED: "+label)

def main():
    base=read(REG)
    assert validate(base)["public"]==0
    cases=[
      ("public",lambda d:d.__setitem__("publication_approved",True)),
      ("historian",lambda d:d.__setitem__("historian_approved",True)),
      ("original",lambda d:d.__setitem__("original_manuscripts_read",True)),
      ("V35 suit",lambda d:d.__setitem__("individual_V35_case_proven",True)),
      ("media",lambda d:d.__setitem__("media_reuse_approved",True)),
      ("main edited",lambda d:d.__setitem__("main_modified",True)),
      ("AI app edited",lambda d:d.__setitem__("ai_studio_modified",True)),
      ("new canonical",lambda d:d.__setitem__("new_canonical_ids",1)),
      ("wrong work",lambda d:d.__setitem__("document_id","OV-D-014")),
      ("wrong parent",lambda d:d.__setitem__("parent","unapproved.json")),
      ("photo used",lambda d:d.__setitem__("media_used_in_app",True)),
      ("one timeline dropped",lambda d:d["timeline"].pop()),
      ("1657 altered to 1661",lambda d:d["timeline"][0].__setitem__("date","1661-10-21")),
      ("1661 siege altered to 1657",lambda d:d["timeline"][1].__setitem__("date","1657-03-26")),
      ("1661 judge date changed",lambda d:d["timeline"][2].__setitem__("date","1661-08-18")),
      ("1661 council date changed",lambda d:d["timeline"][3].__setitem__("date","1661-08-13")),
      ("1661 appointment not Aug19",lambda d:d["timeline"][4].__setitem__("date","1661-08-13")),
      ("guild suppressed earlier",lambda d:d["timeline"][5].__setitem__("date","1648")),
      ("citizen wrongly rejected",lambda d:d["timeline"][6].__setitem__("label","Greiteke denied city citizenship")),
      ("1677 moved 1661",lambda d:d["timeline"][6].__setitem__("date","1661-05-15")),
      ("1681 changed 1648",lambda d:d["timeline"][7].__setitem__("date","1648-10-24")),
      ("1681 made unrestricted",lambda d:d["timeline"][7].__setitem__("label","absolute restored city sovereignty")),
      ("manuscript false examined",lambda d:d["timeline"][0].__setitem__("contemporaneous_manuscript_read",True)),
      ("missing manuscript",lambda d:d["archival_locators"].pop()),
      ("MLA draft confused",lambda d:d["archival_locators"][0].__setitem__("locator","MLA 413–5")),
      ("MLA witness paper original",lambda d:d["archival_locators"][1].__setitem__("original_text_read",True)),
      ("council wrong manuscript",lambda d:d["archival_locators"][2].__setitem__("locator","AA II 0, fol.96r")),
      ("council fake modern accession",lambda d:d["archival_locators"][2].__setitem__("modern_shelfmark_confirmed",True)),
      ("1681 folio misquoted",lambda d:d["archival_locators"][3].__setitem__("locator","AA II 0, fol.95r")),
      ("source URL list shortened",lambda d:d["source_urls"].pop()),
      ("academic secondary lost",lambda d:d["source_urls"][0].__class__ and d["source_urls"].__setitem__(0,"https://invalid.example")),
      ("1657 LWL art swapped",lambda d:d["source_urls"].__setitem__(3,d["source_urls"][2])),
      ("hostile HTTP source",lambda d:d["source_urls"].__setitem__(4,"http://www.loc.gov/pictures/item/2016645785/")),
      ("unresolved erased",lambda d:d["unresolved"].clear()),
    ]
    for label,mut in cases:fail_as_expected(base,label,mut)
    print(f"PASS: {len(cases)} false Münster siege dates, guild law, archival folios, licenses and release statuses rejected; PUBLIC 0")
if __name__=="__main__":main()
