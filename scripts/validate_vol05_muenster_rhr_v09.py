#!/usr/bin/env python3
"""Münster Reichshofrat Vienna inventory: 2 cases, 5 decision-lead locations.
This QA only checks provenance and conservative research release statuses.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_muenster_reichshofrat_case_inventory_v09.json"
PREV="data/deep/vol05_muenster_1661_documents_v08.json"
REPORT="docs/01_CONTENT/VOL05/MUENSTER_REICHS_HOFRAT_1655_1661_CASES_V09.md"
GATES={"scholar_review","original_reichshofrat_case_text_read","copy1626_text_transcribed","copy1627_text_transcribed","v35_individual_case_proven","media_rights_approved","publication_approved"}
KNOWN={
"MUE-RHR-ANT4-858":(858,1655,1661,3429,["K. 389, Nr. 5","K. 390, Nr. 1","K. 391, Nr. 1","K. 392, Nr. 1","K. 393, Nr. 1"],"MUNICIPAL_VS_BISHOP_GARRISON_IUS_PRAESIDII"),
"MUE-RHR-ANT4-871":(871,1659,1660,205,["K. 393, Nr. 14"],"DISOBEDIENCE_DUTCH_STATES_TROOP_RECRUITMENT")}
LEADS={
"RHR09-L-1655-0812":("MUE-RHR-ANT4-858","1655-08-12","K. 390, Nr. 1","79r–86v"),
"RHR09-L-1659-0709":("MUE-RHR-ANT4-858","1659-07-09",None,"77r–79v"),
"RHR09-L-1660-0523":("MUE-RHR-ANT4-858","1660-05-23",None,None),
"RHR09-L-1661-0307":("MUE-RHR-ANT4-858","1661-03-07","K. 393, Nr. 1","69r–88r"),
"RHR09-L-1660-0103":("MUE-RHR-ANT4-871","1660-01-03","K. 393, Nr. 14","134r (start only; full range unknown)")
}

def read(file):return json.loads((ROOT/file).read_text(encoding="utf8"))
def bad(msg):raise ValueError(msg)

def validate(d=None):
    d=read(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_MUENSTER_REICHS_HOFRAT_CASE_INVENTORY_V09","DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        bad("research draft/canonical identity drift")
    if d["parent"]!=PREV or d["new_canonical_ids"]!=0 or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        bad("unapproved main/overview/AI Studio changes")
    if set(d["publication_gate"])!=GATES or any(d["publication_gate"].values()):
        bad("scholar, full-original-text, individual V35 or rights gates bypassed")
    parent=read(PREV)
    if parent["canonical_event_id"]!=d["canonical_event_id"] or parent["canonical_document_id"]!=d["canonical_document_id"]:
        bad("parent research chain broken")
    sources=d["sources"]
    if len(sources)!=10 or len({s["source_key"] for s in sources})!=10:
        bad("ten distinct source descriptions required")
    bysrc={}
    for s in sources:
        u=urlparse(s["url"])
        if u.scheme!="https" or not u.netloc or not s["source_key"].startswith("RHR09-S"):
            bad("bad URL/reference")
        if not s["scope"] or not s["kind"] or not s["access"]:
            bad("unrecorded source evidence tier")
        for flag in ("original_manuscript_pages_read","full_case_pdf_read","image_reuse_licensed","publish_approved"):
            if s[flag] is not False:bad("unverified source contents falsely approved")
        bysrc[s["source_key"]]=s
    if "INDEXED_RESULT_READ_DIRECT_OPEN_CACHE_MISS" != bysrc["RHR09-S01"]["access"]:
        bad("case 858 full page access falsely claimed")
    if "INDEXED_RESULT_READ_DIRECT_OPEN_CACHE_MISS" != bysrc["RHR09-S02"]["access"]:
        bad("case 871 full page access falsely claimed")
    if "SEARCH_RESULTS_TEXT_READ_NO_CASE_MANUSCRIPT" != bysrc["RHR09-S03"]["access"]:
        bad("decision index search snippets promoted to primary verdict")
    if "Public inventory search" not in bysrc["RHR09-S04"]["scope"]:
        bad("paid full-text access qualifier missing")
    cases=d["court_case_catalogs"]
    if len(cases)!=2 or {x["key"] for x in cases}!=set(KNOWN):
        bad("two distinct cases 858 and 871 required")
    for c in cases:
        num,start,end,folios,signs,topic=KNOWN[c["key"]]
        if (c["case_number"],c["catalog_volume"],c["years_start"],c["years_end"],c["folios_catalog_total"],c["archive_subfile_signatures"],c["topic_key"])!=(num,4,start,end,folios,signs,topic):
            bad("case number/folios/signature/subject conflation")
        if c["series"]!="Antiqua" or c["citable_smartlink"]!=f"https://www.rhrdigital.de/antiqua.4.{num}":
            bad("invalid exact legal case locator")
        if not c["source_keys"] or not set(c["source_keys"])<=set(bysrc):
            bad("unreferenced court case inventory")
        if c["source_level"]!="CATALOG_SUMMARY_AND_SEARCH_EXCERPT_NOT_DIRECT_MANUSCRIPT":
            bad("inventory incorrectly represented as full text")
        if c["full_original_read"] is not False or c["explicit_ipo_v35_adjudication_proved"] is not False:
            bad("unread verdict or V35 individual lawsuit claimed")
    leads=d["decision_index_leads"]
    if len(leads)!=5 or {x["key"] for x in leads}!=set(LEADS):
        bad("five exact decision-index leads expected")
    for item in leads:
        if (item["case_key"],item["date"],item["subfile_signature"],item["reported_folio"])!=LEADS[item["key"]]:
            bad("opinion/judgment date or folio drift")
        if item["source_key"]!="RHR09-S03" or item["evidence_tier"]!="SEARCH_EXCERPT_OF_CATALOG_DECISIONS" or item["document_text_read"] is not False:
            bad("unread ruling incorrectly called authentic text")
        if not item["description"]:bad("legal act classification missing")
    copies=d["later_copy_requests"]
    if len(copies)!=2 or {x["key"] for x in copies}!={"RHR09-COPY-1626","RHR09-COPY-1627"}:
        bad("two independent 1661 instructions required")
    for x in copies:
        for fl in ("original_copy_images_obtained","read_in_full"):
            if x[fl] is not False:bad("18th-century copies not directly obtained")
        if x["witness_date"]!="18th century" or "Landesarchiv NRW" not in x["holding_institution"]:
            bad("late copy type or archive missing")
        if not x["request_subject_de"] or not x["claims_allowed"]:
            bad("scholarly question and limited claims missing")
    c={x["key"]:x for x in copies}
    if ("Nr. 1626" not in c["RHR09-COPY-1626"]["shelfmark"] or "Nr. 1627" not in c["RHR09-COPY-1627"]["shelfmark"]):
        bad("later copies swapped")
    if len(d["research_conclusions"])<9 or not any("No full-file text was copied" in s for s in d["research_conclusions"]):
        bad("rights and primary reading limits omitted")
    text=(ROOT/REPORT).read_text(encoding="utf8")
    if len(text)<5500 or text.count("\n## ")<7 or "DRAFT_RESEARCH_NOT_PUBLIC" not in text:
        bad("detailed Korean research article missing")
    for s in ("858","871","3,429","205","1655","1659","1660","1661","1626","1627","§35","미확인"):
        if s not in text:bad("historical fact/caveat omitted from report "+s)
    return {"cases":2,"subfiles":6,"leads":5,"later_copies":2,"sources":10,"direct_v35":0,"public":0}

if __name__=="__main__":
    result=validate()
    print("PASS VOL05 V0.9: 2 specific Reichshofrat cases, 6 subfiles, 5 decisions index leads, 2 unexamined copies, PUBLIC 0")
