#!/usr/bin/env python3
"""Unsafe V0.9 edition/provenance mutations must fail closed."""
from __future__ import annotations
import sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_rhr_v09 import read,validate,REG

def deny(base,name,mutate):
    d=copy.deepcopy(base)
    mutate(d)
    try:validate(d)
    except (ValueError,KeyError,IndexError,TypeError,StopIteration):return
    raise AssertionError("dangerous Münster claim passed QA: "+name)

def main():
    base=read(REG)
    assert validate(base)["public"]==0
    changes=[
      ("public",lambda x:x["publication_gate"].__setitem__("publication_approved",True)),
      ("hist review",lambda x:x["publication_gate"].__setitem__("scholar_review",True)),
      ("RHR original",lambda x:x["publication_gate"].__setitem__("original_reichshofrat_case_text_read",True)),
      ("copy 1626 text read",lambda x:x["publication_gate"].__setitem__("copy1626_text_transcribed",True)),
      ("copy 1627 text read",lambda x:x["publication_gate"].__setitem__("copy1627_text_transcribed",True)),
      ("V35 decision invented",lambda x:x["publication_gate"].__setitem__("v35_individual_case_proven",True)),
      ("media rights invented",lambda x:x["publication_gate"].__setitem__("media_rights_approved",True)),
      ("canonical ID new",lambda x:x.__setitem__("new_canonical_ids",1)),
      ("webapp modified",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("canonical treaty confused",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("original directly read",lambda x:x["sources"][0].__setitem__("original_manuscript_pages_read",True)),
      ("paid case PDF falsely read",lambda x:x["sources"][0].__setitem__("full_case_pdf_read",True)),
      ("insecure source URL",lambda x:x["sources"][1].__setitem__("url","http://example.org")),
      ("wrong court search access",lambda x:x["sources"][2].__setitem__("access","PRIMARY_1655_LATIN_TEXT_COLLATED")),
      ("source dropped",lambda x:x["sources"].pop()),
      ("case omitted",lambda x:x["court_case_catalogs"].pop()),
      ("858 871 merged",lambda x:x["court_case_catalogs"][0].__setitem__("case_number",871)),
      ("858 folio count changed",lambda x:x["court_case_catalogs"][0].__setitem__("folios_catalog_total",205)),
      ("871 enlarged to 3429",lambda x:x["court_case_catalogs"][1].__setitem__("folios_catalog_total",3429)),
      ("858 K record forged",lambda x:x["court_case_catalogs"][0]["archive_subfile_signatures"].append("K. 393, Nr. 14")),
      ("871 becomes IPO judgment",lambda x:x["court_case_catalogs"][1].__setitem__("explicit_ipo_v35_adjudication_proved",True)),
      ("858 original read",lambda x:x["court_case_catalogs"][0].__setitem__("full_original_read",True)),
      ("1655 folio wrong",lambda x:x["decision_index_leads"][0].__setitem__("reported_folio","99r–100v")),
      ("1659 7/9 called 1661",lambda x:x["decision_index_leads"][1].__setitem__("date","1661-07-09")),
      ("1660 missing folio forged",lambda x:x["decision_index_leads"][2].__setitem__("reported_folio","120r–133v")),
      ("1661 subfile swapped",lambda x:x["decision_index_leads"][3].__setitem__("subfile_signature","K. 392, Nr. 1")),
      ("871 false 1659/01 ruling",lambda x:x["decision_index_leads"][4].__setitem__("date","1659-01-03")),
      ("edition snippet to original",lambda x:x["decision_index_leads"][3].__setitem__("document_text_read",True)),
      ("new lead invented",lambda x:x["decision_index_leads"].append(copy.deepcopy(x["decision_index_leads"][0]))),
      ("later copy type erased",lambda x:x["later_copy_requests"][0].__setitem__("witness_date","1661 original")),
      ("copy 1626 shelf wrong",lambda x:x["later_copy_requests"][0].__setitem__("shelfmark","Nr. 1627")),
      ("copy 1627 read invented",lambda x:x["later_copy_requests"][1].__setitem__("read_in_full",True)),
      ("no-risk conclusion erased",lambda x:x["research_conclusions"].clear()),
    ]
    for name,fn in changes:deny(base,name,fn)
    print(f"PASS: {len(changes)} unsafe RHR archive identity, ruling dates, unreviewed documents and publication mutations rejected; PUBLIC 0")

if __name__=="__main__":main()
