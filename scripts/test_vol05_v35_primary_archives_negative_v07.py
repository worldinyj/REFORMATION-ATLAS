#!/usr/bin/env python3
"""Reject premature claims of §35 enforcement, catalog certainty or publication."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_v35_primary_archives_v07 import read,validate,REG

def must_reject(base,title,change):
    item=copy.deepcopy(base)
    change(item)
    try:validate(item)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("unsafe archive claim accepted: "+title)

def main():
    d=read(REG)
    assert validate(d)["public"]==0
    cases=[
        ("release",lambda x:x["publication_gate"].__setitem__("can_publish",True)),
        ("scholar",lambda x:x["publication_gate"].__setitem__("human_historian_approved",True)),
        ("primary read",lambda x:x["publication_gate"].__setitem__("individual_local_original_read",True)),
        ("V35 case",lambda x:x["publication_gate"].__setitem__("actual_v35_enforcement_case_proven",True)),
        ("image rights",lambda x:x["publication_gate"].__setitem__("media_reuse_cleared",True)),
        ("treaty original",lambda x:x["publication_gate"].__setitem__("original_treaty_collated",True)),
        ("new canonical",lambda x:x.__setitem__("canonical_ids_minted",1)),
        ("webapp",lambda x:x.__setitem__("ai_studio_modified",True)),
        ("wrong treaty",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
        ("source removed",lambda x:x["sources"].pop()),
        ("source http",lambda x:x["sources"][0].__setitem__("url","http://example.org")),
        ("primary original falsely read",lambda x:x["sources"][0].__setitem__("physical_original_directly_read",True)),
        ("case falsely confirmed",lambda x:x["sources"][6].__setitem__("individual_v35_case_confirmed",True)),
        ("art photo reuse",lambda x:x["sources"][10].__setitem__("photo_redistribution_licensed",True)),
        ("St Servatius wrong date",lambda x:x["findings"][0].__setitem__("date","1648")),
        ("St Servatius not V3",lambda x:x["findings"][0].__setitem__("context_article","IPO V §35")),
        ("St Servatius lawsuit claimed",lambda x:x["findings"][0].__setitem__("local_primary_case_file_read",True)),
        ("1712 date erased",lambda x:x["findings"][1].__setitem__("statement_ko","1648년 두 Wesensarchive 정식 창설")),
        ("Muenster missing 1648 erased",lambda x:x["findings"][2].__setitem__("statement_ko","뮌스터 1648년 의사록 212권 보존")),
        ("invented judicial full book read",lambda x:x["findings"][3].__setitem__("local_primary_case_file_read",True)),
        ("2024 full research book fictitious",lambda x:x["findings"][4].__setitem__("evidence_level","FULL_ORIGINAL_COURT_REVIEW")),
        ("court target made read",lambda x:x["archival_target_series"][3].__setitem__("individual_item_read",True)),
        ("St Servatius shelfmark forged",lambda x:x["archival_target_series"][1].__setitem__("exact_item_shelfmark","H-1649-X")),
        ("Muenster AII20 case fabricated",lambda x:x["archival_target_series"][2].__setitem__("exact_item_shelfmark","A II Nr.20, fol. 1648/25")),
        ("judicial fonds as case",lambda x:x["archival_target_series"][3].__setitem__("exact_item_shelfmark","B-Acta jud 1649:23")),
        ("art miscaption",lambda x:x["visual_reference_candidate"].__setitem__("title","St Servatius 1649")),
        ("art falsely St Servatius",lambda x:x["visual_reference_candidate"].__setitem__("not_st_servatius",False)),
        ("art loaded",lambda x:x["visual_reference_candidate"].__setitem__("used_in_webapp",True)),
        ("uncertainty erased",lambda x:x["unresolved"].clear()),
        ("evidence hierarchy erased",lambda x:x.__setitem__("query_method","Every parish result proves V35 court implementation")),
    ]
    for label,change in cases:must_reject(d,label,change)
    print(f"PASS: {len(cases)} fabricated local V35/copy/archive/release changes rejected, PUBLIC 0")

if __name__=="__main__": main()
