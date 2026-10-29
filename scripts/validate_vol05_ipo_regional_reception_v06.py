#!/usr/bin/env python3
"""VOL05 Treaty V35 social rights vs V3 regional institutional parity.

Structural consistency and evidence-tier checks, NOT direct archival collation
or proof of any individual post-1648 Article V §35 enforcement.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_ipo_v35_regional_reception_v06.json"
PARENT="data/deep/vol05_ipo_image_access_latin_text_v05.json"
DOC="docs/01_CONTENT/VOL05/IPO_V35_FIVE_CITIES_CIVIC_RIGHTS_V06.md"
CITY_MAP={
"IPO-RR-AUGSBURG-1648":("Augsburg","IPO_ART_V_PAR_3"),
"IPO-RR-BIBERACH-1649":("Biberach an der Riss","IPO_ART_V_PAR_3"),
"IPO-RR-DINKELSBUEHL-1654":("Dinkelsbuehl","IPO_ART_V_PAR_3"),
"IPO-RR-RAVENSBURG-1648":("Ravensburg","IPO_ART_V_PAR_3"),
"IPO-RR-MUENSTER-PRETREATY":("Muenster","IPO_ART_V_PAR_35_CONTEXT_ONLY"),
}
RIGHTS={"IPO-V35-GUILD","IPO-V35-INHERITANCE","IPO-V35-HOSPITAL","IPO-V35-BURIAL"}
GATE={"scholar_review","regional_archival_primary_records_collated","v35_post_treaty_enforcement_proven","media_rights_approved","publication_approved","can_ship"}

def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def wrong(msg): raise ValueError(msg)

def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["existing_event_id"],d["existing_document_id"])!=(
        "VOL05_IPO_V35_REGIONAL_RECEPTION_RESEARCH","DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        wrong("wrong research object, volume, or existing canonical ID")
    if d["parent_registry"]!=PARENT or d["created_canonical_ids"]!=0 or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        wrong("unapproved app/public canonical change")
    if set(d["release_gate"])!=GATE or any(d["release_gate"].values()):
        wrong("human/primary-source/publication gate bypass")
    overview=load("data/overview/events_documents_v01.json")
    e=next(x for x in overview["events"] if x["id"]=="OV-E-024")
    w=next(x for x in overview["documents"] if x["id"]=="OV-D-015")
    if "VOL-05" not in e["volume_ids"] or "VOL-05" not in w["volume_ids"]:
        wrong("existing atlas volume mapping changed")
    base=load(PARENT)
    if base["canonical_event_id"]!=d["existing_event_id"] or base["canonical_document_id"]!=d["existing_document_id"]:
        wrong("lost previous IPO V35 textual source")
    parent_v35=next((c for c in base["latin_clause_review"] if c["article"]=="V" and c["paragraph"]=="35"),None)
    if parent_v35 is None or parent_v35["original_printed_text_checked"] is not False:
        wrong("V35 is missing/unlawfully promoted in previous manuscript audit")
    sources=d["source_records"]
    if len(sources)!=13 or len({x["key"] for x in sources})!=13:
        wrong("thirteen distinct source records required")
    src={}
    for x in sources:
        uri=urlparse(x["url"])
        if not x["key"].startswith("RR-SRC-") or uri.scheme!="https" or not uri.netloc:
            wrong("invalid provenance link")
        if not x["source_type"] or not x["claim_scope"]:
            wrong("evidence kind/claim scope missing")
        if x["original_city_council_minutes_examined"] is not False or x["reproduced_image_rights_approved"] is not False or x["publication_approved"] is not False:
            wrong("unread local original or rights falsely confirmed")
        src[x["key"]]=x
    c=d["region_cases"]
    if len(c)!=5 or {x["key"] for x in c}!=set(CITY_MAP):
        wrong("five defined regional cases required")
    for x in c:
        city,legal=CITY_MAP[x["key"]]
        if (x["location"],x["legal_anchor"])!=(city,legal):
            wrong("wrong city or V3/V35 claim linkage")
        if x["direct_application_of_v35_proved"] is not False or x["post_treaty_local_original_records_read"] is not False:
            wrong("§35 individual enforcement falsely claimed")
        if not x["source_keys"] or not set(x["source_keys"])<=set(src) or not x["historical_observations"] or not x["risk"]:
            wrong("regional source or caveat missing")
        if not x["evidence_level"] or not x["outcome"]:
            wrong("regional evidence classification missing")
    cases={x["key"]:x for x in c}
    if cases["IPO-RR-BIBERACH-1649"]["time_focus"]!="1548 and 1648–1649":
        wrong("church's 1548 vs municipal parity 1649 confused")
    if cases["IPO-RR-MUENSTER-PRETREATY"]["time_focus"]!="1587 and 1590s":
        wrong("PRE-1648 burial dispute misdated as treaty implementation")
    if "RETROSPECTIVE" not in cases["IPO-RR-DINKELSBUEHL-1654"]["evidence_level"]:
        wrong("1653 school/1654 celebration described as primary archival proof")
    topics=d["article_35_implementation_topics"]
    if len(topics)!=4 or {x["key"] for x in topics}!=RIGHTS:
        wrong("four social rights domains must remain")
    for x in topics:
        if x["regional_application_evidence_found"] is not False or x["legal_source_key"]!="RR-SRC-01":
            wrong("unverified V35 direct application")
        if not x["candidate_archives"] or not x["title_ko"]:
            wrong("archive follow-up target missing")
        if not set(x.get("adjacent_context_evidence_keys",[]))<=set(src):
            wrong("invalid regional social-rights context")
    if d["core_method"]!="Separate IPO Article V §3 urban institutional parity from Article V §35 individual civic rights; pre-1648 antecedents and post-1648 retrospective reports are distinct evidence types.":
        wrong("methodological distinction silently erased")
    if len(d["editorial_holds"])<9 or not any("1587" in s or "pre-1648" in s for s in d["editorial_holds"]):
        wrong("critical history uncertainties removed")
    text=(ROOT/DOC).read_text(encoding="utf-8")
    if len(text)<5700 or text.count("\n## ")<8 or "DRAFT_RESEARCH_NOT_PUBLIC" not in text:
        wrong("reader history chapter incomplete")
    for word in ["§3","§35","1548","1649","1653","1654","1587","1590","길드","장례","미확인"]:
        if word not in text:
            wrong("important history caveat missing from chapter: "+word)
    return {"cities":5,"source_records":13,"civic_rights":4,"direct_enforcement":0,"public":0}

if __name__=="__main__":
    x=validate()
    print("PASS VOL05 IPO regional V0.6: five cases, thirteen sources, four civic-rights domains, direct V35 enforcement 0, PUBLIC 0")
