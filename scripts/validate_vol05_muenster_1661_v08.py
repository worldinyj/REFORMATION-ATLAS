#!/usr/bin/env python3
"""VOL05 Münster 1661 object-level catalog/regest provenance audit.

NOT a validation of original manuscripts, photographed image contents, a
Reichshofrat case judgment or enforcement of IPO Article V section 35.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_muenster_1661_documents_v08.json"
PREV="data/deep/vol05_ipo_v35_primary_archive_leads_v07.json"
REPORT="docs/01_CONTENT/VOL05/MUENSTER_1648_1661_MUNICIPAL_RIGHTS_V08.md"
GATES={"historian_review","original_manuscripts_read","individual_V35_rights_enforcement_verified",
       "original_IPO_latin_collated","media_rights_approved","can_publish"}
DOC_IDS={
"MUE-DOC-1661-03-26-SENDEN":("1661-03-26","ORIGINAL_PARCHMENT","V08-S01","Fb. Münster No. 4446"),
"MUE-DOC-1661-08-13-STADTRICHTER":("1661-08-13","18TH_CENTURY_PAPER_COPY_OF_1661_REGULATION","V08-S02","Nr. 1626"),
"MUE-DOC-1661-08-18-RAT":("1661-08-18","18TH_CENTURY_PAPER_COPY_OF_1661_INSTRUCTION","V08-S03","Nr. 1627"),
}
RESEARCH_TARGETS={"MUE-REICHS-1655-1661","MUE-1661-REG-1626","MUE-1661-REG-1627","MUE-RATS-1650-1655"}

def load(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
def reject(msg):raise ValueError(msg)

def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
       "VOL05_MUENSTER_POST_WESTPHALIA_DOCUMENT_LEVEL_CROSSWALK",
       "DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        reject("wrong draft document identity or canonical parent")
    if d["parent_registry"]!=PREV or d["new_canonical_ids"]!=0 or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        reject("canonical/public boundary crossed")
    if set(d["publication_gate"])!=GATES or any(d["publication_gate"].values()):
        reject("uncollated original, false V35 proof or publication prematurely approved")
    old=load(PREV)
    if old["canonical_event_id"]!=d["canonical_event_id"] or old["canonical_document_id"]!=d["canonical_document_id"]:
        reject("previous documentary research crosslink missing")
    if old["publication_gate"]["actual_v35_enforcement_case_proven"] is not False:
        reject("previous direct V35 enforcement not proved")
    sources=d["sources"]
    if len(sources)!=10 or len({s["source_key"] for s in sources})!=10:
        reject("10 unique sources required")
    source={}
    for s in sources:
        url=urlparse(s["url"])
        if not s["source_key"].startswith("V08-S") or url.scheme!="https" or not url.hostname or not s["kind"] or not s["scope"] or not s["access_level"]:
            reject("invalid or untyped source link")
        for flag in ("direct_original_document_text_read","direct_17th_century_folio_collated","licensed_for_image_reuse","public_approved"):
            if s[flag] is not False:
                reject("unread original or unlicensed source marked fully read/approved")
        source[s["source_key"]]=s
    if (source["V08-S01"]["kind"],source["V08-S02"]["kind"],source["V08-S03"]["kind"])!=(
        "DDB_CATALOG_OF_ORIGINAL_PARCHMENT","LWL_REGEST_OF_18TH_C_COPY","LWL_REGEST_OF_18TH_C_COPY"):
        reject("original parchment and 18th-century transcript regests conflated")
    if "5S2DC42KLMFXCNUM2XIG3YXJIZ6RZNZQ" not in source["V08-S01"]["url"]:
        reject("DDB physical object ID changed")
    if "regest=112845" not in source["V08-S02"]["url"] or "regest=112846" not in source["V08-S03"]["url"]:
        reject("LWL regest IDs must not be swapped")
    docs=d["document_records"]
    if len(docs)!=3 or {x["research_id"] for x in docs}!=set(DOC_IDS):
        reject("three dated separate documents required")
    by={x["research_id"]:x for x in docs}
    for key,doc in by.items():
        date,wt,src,shelf=DOC_IDS[key]
        if (doc["document_date"],doc["catalog_declared_witness_type"],doc["legacy_signature"])!=(date,wt,shelf):
            reject("document date, original/copy type, or signature wrong")
        if doc["source_keys"]!=[src] or not set(doc["source_keys"])<=set(source):
            reject("document has missing or incorrect primary catalog description")
        if doc["original_bytes_inspected"] is not False or doc["original_witness_text_collated"] is not False or doc["explicit_IPO_article_V35_in_document"] is not False:
            reject("archive catalog improperly represented as read original or specific V35 judgment")
        if doc["digitized_image_count"] is not None or not doc["regest_or_catalog_read"]:
            reject("missing catalog verification or invented image count")
        if not doc["legal_scope"] or not doc["repository"] or not doc["fonds"]:
            reject("unbounded legal or archival context")
    if by["MUE-DOC-1661-03-26-SENDEN"]["digitization_reported"] is not True:
        reject("original parchment is digitized according to its catalog")
    if "Gogericht zu Senden" not in by["MUE-DOC-1661-03-26-SENDEN"]["legal_scope"] or "NOT comprehensive" not in by["MUE-DOC-1661-03-26-SENDEN"]["legal_scope"]:
        reject("Senden transfer incorrectly characterized as all city liberties")
    if by["MUE-DOC-1661-08-13-STADTRICHTER"]["religious_subject_reporting"] is not True:
        reject("1661 non-Catholic residents reporting clause omitted")
    if by["MUE-DOC-1661-08-18-RAT"]["religious_subject_reporting"] is not False:
        reject("August 18 hospital officers instruction conflated with August 13 religious reporting")
    if by["MUE-DOC-1661-08-13-STADTRICHTER"]["digitization_reported"] is not False or by["MUE-DOC-1661-08-18-RAT"]["digitization_reported"] is not False:
        reject("18th-century copies falsely read as digitized originals")
    periods=d["chronology"]
    if len(periods)!=4 or {x["phase_key"] for x in periods}!={"MUE-V08-PHASE-1648","MUE-V08-PHASE-1650","MUE-V08-PHASE-1655-1661","MUE-V08-PHASE-1661"}:
        reject("1648/1650/1655-61/1661 chronology needs distinct events")
    for x in periods:
        if not x["source_keys"] or not set(x["source_keys"])<=set(source) or x["archive_primary_case_read"] is not False:
            reject("unread imperial court sources promoted")
    targets=d["archival_investigation_next"]
    if len(targets)!=4 or {t["target_key"] for t in targets}!=RESEARCH_TARGETS:
        reject("four next actual archival investigations required")
    for t in targets:
        if not t["source_keys"] or not set(t["source_keys"])<=set(source) or t["original_file_read"] is not False or not t["question"]:
            reject("archive follow-up missing or falsely marked read")
    v={t["target_key"]:t for t in targets}
    if v["MUE-REICHS-1655-1661"]["exact_case_signature"] is not None:
        reject("Vienna court original case shelfmark still unknown")
    if "series;" not in v["MUE-RATS-1650-1655"]["exact_case_signature"]:
        reject("municipal council series reference is not an individual file")
    if len(d["historical_interpretation_guardrails"])<9 or not any("18th-century" in x for x in d["historical_interpretation_guardrails"]):
        reject("transmission and legal caution erased")
    image=d["representative_image_policy"]
    if image["selected_artwork"] is not None or image["downloads"]!=0 or image["avoid_ter_borch_dutch_spanish_1648_picture_as_1661_muenster_bishop_event"] is not True:
        reject("unverified event painting reused")
    text=(ROOT/REPORT).read_text(encoding="utf8")
    if len(text)<6000 or text.count("\n## ")<8 or "DRAFT_RESEARCH_NOT_PUBLIC" not in text:
        reject("reader-facing substantial critical account missing")
    for phrase in ("1661년 3월 26일","1661년 8월 13일","1661년 8월 18일","18세기","1626","1627",
        "재판권","비가톨릭","Hospitalsherren","Sterbherren","§35","미확인"):
        if phrase not in text:
            reject("missing witness distinction or history caveat "+phrase)
    return {"document_items":3,"actual_originals_cataloged":1,"later_copy_regests":2,
            "source_count":10,"relevant_v35_judgments_read":0,"public":0}

if __name__=="__main__":
    s=validate()
    print(f"PASS VOL05 V0.8: {s['document_items']} dated items (1 original catalog, 2 later-copy regests), {s['source_count']} sources, V35 judgments 0, PUBLIC 0")
