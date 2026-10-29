#!/usr/bin/env python3
"""VOL05 original local archives and specific Augsburg St Servatius research.

Fail-closed source levels. This proves availability of described series, not
any individual IPO V §35 litigation, manuscript transcription, or art rights.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_ipo_v35_primary_archive_leads_v07.json"
PARENT="data/deep/vol05_ipo_v35_regional_reception_v06.json"
GATES={"human_historian_approved","individual_local_original_read","actual_v35_enforcement_case_proven",
       "original_treaty_collated","media_reuse_cleared","can_publish"}
EXPECTED_FINDINGS={"VA7-F01-SERVATIUS","VA7-F02-AUGS-ARCHIVE",
                   "VA7-F03-MUENSTER-COUNCIL","VA7-F04-MUENSTER-JUDICIAL","VA7-F05-MUENSTER-BOOK"}
EXPECTED_TARGETS={"VA7-AUG-CITY-COUNCIL","VA7-AUG-HOSPITAL","VA7-MUE-RATS","VA7-MUE-JUD"}
EXPECTED_DOCS={
"docs/01_CONTENT/VOL05/IPO_V35_AUGSBURG_ST_SERVATIUS_1649_V07.md":
["성 세르바티우스","1649","1712","1757","§3","§35"],
"docs/01_CONTENT/VOL05/IPO_V35_MUENSTER_DIGITAL_COUNCIL_COURT_V07.md":
["뮌스터","1648년","결락","A II Nr. 20","Judicialakten","§35"]}

def read(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def reject(reason): raise ValueError(reason)

def validate(data=None):
    d=read(REG) if data is None else data
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_IPO_V35_LOCAL_ARCHIVE_FOLLOWUP","DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        reject("research object or canonical parents changed")
    if d["parent_research"]!=PARENT or d["canonical_ids_minted"]!=0 or d["main_modified"] is not False or d["ai_studio_modified"] is not False:
        reject("unauthorized public app or ID assertion")
    if set(d["publication_gate"])!=GATES or any(d["publication_gate"].values()):
        reject("premature history, image, or release approval")
    base=read(PARENT)
    if base["existing_event_id"]!=d["canonical_event_id"] or base["existing_document_id"]!=d["canonical_document_id"]:
        reject("prior V35 regional source lost")
    if any(item["direct_application_of_v35_proved"] is not False for item in base["region_cases"]):
        reject("parent has no individual V35 enforcement case")
    sources=d["sources"]
    if len(sources)!=14 or len({x["source_key"] for x in sources})!=14:
        reject("fourteen distinct referenced sources required")
    idx={}
    for item in sources:
        url=urlparse(item["url"])
        if not item["source_key"].startswith("VA7-S") or url.scheme!="https" or not url.hostname:
            reject("duplicate or invalid reference")
        if not item["kind"] or not item["access"] or not item["scope"]:
            reject("source access and limitations unspecified")
        if (item["physical_original_directly_read"] is not False or
            item["individual_v35_case_confirmed"] is not False or
            item["photo_redistribution_licensed"] is not False or
            item["publication_approved"] is not False):
            reject("original/individual lawsuit or publication approval fabricated")
        idx[item["source_key"]]=item
    if idx["VA7-S01"]["scope"]!="St Servatius 1649 parity":
        reject("named St Servatius 1649 source disappeared")
    cases=d["findings"]
    if len(cases)!=5 or {x["finding_id"] for x in cases}!=EXPECTED_FINDINGS:
        reject("five research findings required")
    byid={x["finding_id"]:x for x in cases}
    for case in cases:
        if not case["source_keys"] or not set(case["source_keys"])<=set(idx):
            reject("finding missing or orphan source")
        if case["local_primary_case_file_read"] is not False or not case["not_proven"]:
            reject("historical observation promoted into specific local V35 judgment")
        if not case["statement_ko"] or not case["context_article"] or not case["evidence_level"]:
            reject("history assertion without evidence class")
    augs=byid["VA7-F01-SERVATIUS"]
    if augs["date"]!="1649" or augs["location"]!="Augsburg" or augs["context_article"]!="IPO V §3 and city charity institution":
        reject("1649 hospital management misdated or turned into V35 case")
    admin=byid["VA7-F02-AUGS-ARCHIVE"]
    if "1712" not in admin["statement_ko"] or "1757" not in admin["statement_ko"]:
        reject("1648 administrative parity conflated with formal archive establishment")
    mue=byid["VA7-F03-MUENSTER-COUNCIL"]
    if "A II Nr.20" not in mue["statement_ko"] or "212" not in mue["statement_ko"] or "1648" not in mue["statement_ko"] or "결락" not in mue["statement_ko"]:
        reject("digitized 212 volumes and missing 1648 year must be explicit")
    court=byid["VA7-F04-MUENSTER-JUDICIAL"]
    if "65권" not in court["statement_ko"] or "1,161" not in court["statement_ko"]:
        reject("judicial protocol and case-series counts conflated")
    if byid["VA7-F05-MUENSTER-BOOK"]["evidence_level"]!="ACADEMIC_PROJECT_AND_PUBLISHER_SUMMARY_ONLY":
        reject("2024 book abstracts falsely promoted to full text")
    targets=d["archival_target_series"]
    if len(targets)!=4 or {x["target_id"] for x in targets}!=EXPECTED_TARGETS:
        reject("four physical source paths expected")
    for t in targets:
        if not t["query_keywords_de"] or t["individual_item_read"] is not False or t["holdings_claim_source"] not in idx:
            reject("archival goal falsely read or no evidence")
    target={x["target_id"]:x for x in targets}
    if target["VA7-AUG-HOSPITAL"]["exact_item_shelfmark"] is not None:
        reject("specific St Servatius archival shelfmark not proven")
    if target["VA7-MUE-RATS"]["exact_item_shelfmark"]!="A II Nr. 20 (series-level only; NOT a case file)":
        reject("Muenster fonds mistaken for individual case ID")
    if target["VA7-MUE-JUD"]["exact_item_shelfmark"]!="B-Acta jud (collection-level, no individual case number)":
        reject("court collection reference mistaken for named lawsuit")
    art=d["visual_reference_candidate"]
    if art["year"]!=1742 or art["title"]!="Augsburg: Hl. Geist-Spital" or art["object_id"]!="bav:HVO-OBJ-00000HVBSA111702":
        reject("1742 art object misattributed as 1649 St Servatius")
    if art["not_st_servatius"] is not True or art["not_1649_scene"] is not True or art["downloaded"] is not False or art["used_in_webapp"] is not False:
        reject("uncleared artwork wrong facility/date or used in app")
    if art["source_key"]!="VA7-S11":
        reject("artwork catalog not linked")
    if len(d["unresolved"])<8 or not any("1648" in x and "missing" in x for x in d["unresolved"]):
        reject("missing 1648 volume warning lost")
    if "institutional confessional parity" not in d["query_method"] or "individual V35 enforcement" not in d["query_method"]:
        reject("research evidence separation rule erased")
    for rel,words in EXPECTED_DOCS.items():
        text=(ROOT/rel).read_text(encoding="utf-8")
        if len(text)<3900 or text.count("\n## ")<5 or "DRAFT_RESEARCH_NOT_PUBLIC" not in text:
            reject("not enough readable research or status: "+rel)
        for word in words:
            if word not in text:
                reject("missing critical regional history/date/source caution: "+word)
    return {"sources":14,"findings":5,"archive_targets":4,"local_case_proven":0,"public":0}

if __name__=="__main__":
    x=validate()
    print("PASS VOL05 V0.7 original archive leads: 5 facts, 4 research archives, 14 sources, direct V35 lawsuits 0, PUBLIC 0")
