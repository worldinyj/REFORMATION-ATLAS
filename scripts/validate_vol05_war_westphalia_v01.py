#!/usr/bin/env python3
"""VOL05 war/Westphalia research: canonical references, treaty identity, fail-closed gate.

This asserts editorial consistency, not original-language critical collation,
completeness of translated treaty excerpts, or public publication approval.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REGISTRY="data/deep/vol05_war_westphalia_research_v01.json"
EXPECTED_EVENTS={"OV-E-022":(1555,None),"OV-E-023":(1618,1648),"OV-E-024":(1648,None)}
EXPECTED_PHASES=[
    ("WAR-PHASE-01",1618,1623,"BOHEMIAN_PALATINATE"),
    ("WAR-PHASE-02",1625,1629,"DANISH"),
    ("WAR-PHASE-03",1630,1635,"SWEDISH"),
    ("WAR-PHASE-04",1635,1648,"FRANCO_SWEDISH"),
]
EXPECTED_TREATIES={
    "WAR-TREATY-IPO-1648":("IPO","Osnabrück","1648-10-24"),
    "WAR-TREATY-IPM-1648":("IPM","Münster","1648-10-24"),
    "WAR-TREATY-DUTCH-SPAIN-1648":("MUNSTER_DUTCH_SPANISH","Münster","1648-01-30"),
}
EXPECTED_CLAUSES={
    "WAR-CL-IPO-V-1":("V","1"),
    "WAR-CL-IPO-V-2":("V","2"),
    "WAR-CL-IPO-V-3":("V","3"),
    "WAR-CL-IPO-V-34":("V","34"),
    "WAR-CL-IPO-VI":("VI",None),
    "WAR-CL-IPO-VII-1":("VII","1"),
    "WAR-CL-IPO-VII-2":("VII","2"),
    "WAR-CL-IPO-VIII-2":("VIII","2"),
}
EXPECTED_PATHS={
    "docs/01_CONTENT/VOL05/EVENT_1618_1648_THIRTY_YEARS_WAR_V01.md",
    "docs/01_CONTENT/VOL05/EVENT_1648_WESTPHALIA_PEACE_V01.md",
    "docs/01_CONTENT/VOL05/AUGSBURG_1555_WESTPHALIA_1648_LEGAL_COMPARE_V01.md",
}

def read(path: str):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def reject(msg):
    raise ValueError(msg)

def validate(d=None):
    d=read(REGISTRY) if d is None else d
    if d["kind"] != "VOL05_WAR_WESTPHALIA_RESEARCH_ONLY" or d["status"]!="DRAFT_RESEARCH_NOT_PUBLIC" or d["volume_id"]!="VOL-05":
        reject("research classification changed")
    if d["ai_studio_modified"] is not False or d["overview_modified"] is not False or d["canonical_ids_minted"]!=0:
        reject("overview or AI studio mutation or invented ID")
    expected_gates={"human_approval","historical_editorial_approval","original_treaty_text_collated","rights_approval","publication_approved","can_ship"}
    if set(d["release_gate"])!=expected_gates or any(d["release_gate"].values()):
        reject("release must fail closed")
    if d["existing_document_id"]!="OV-D-015" or d["existing_event_ids"]!=["OV-E-022","OV-E-023","OV-E-024"]:
        reject("pre-existing canonical IDs changed")
    overview=read("data/overview/events_documents_v01.json")
    events={e["id"]:e for e in overview["events"]}
    documents={x["id"]:x for x in overview["documents"]}
    for eid,years in EXPECTED_EVENTS.items():
        obj=events[eid]
        if (obj["year_start"],obj["year_end"])!=years or obj["volume_ids"]!=["VOL-05"]:
            reject("historical parent event mismatch: "+eid)
    if documents["OV-D-015"]["volume_ids"]!=["VOL-05"]:
        reject("Westphalia documents assigned wrong volume")
    src=d["source_records"]
    if len(src)!=11:
        reject("source inventory drift")
    source_index={}
    for s in src:
        key=s["source_key"]
        u=urlparse(s["url"])
        if key in source_index or not key.startswith("WAR-SRC-") or u.scheme!="https" or not u.hostname:
            reject("duplicate/missing source or URL")
        if any(not s[k] for k in ["kind","evidence_level"]):
            reject("source type/access missing")
        if (s["canonical_source_id"] is not None or s["complete_original_text_collated"] is not False or
            s["reuse_rights_approved"] is not False or s["public_visible"] is not False):
            reject("source improperly promoted")
        source_index[key]=s
    def check_evidence(keys):
        if not keys or len(keys)!=len(set(keys)) or not set(keys)<=set(source_index):
            reject("orphan, duplicate, or empty source links")
    paths=set()
    if len(d["narratives"])!=3:
        reject("three research chapters required")
    for n in d["narratives"]:
        path=n["path"]
        if path in paths or path not in EXPECTED_PATHS:
            reject("unrecognized/duplicate research path")
        paths.add(path)
        if n["event_id"] not in EXPECTED_EVENTS or not n["research_key"].startswith("WAR-NARR-"):
            reject("unlinked event chapter")
        check_evidence(n["source_keys"])
        body=(ROOT/path).read_text(encoding="utf-8")
        if len(body)<4300 or body.count("\n## ")<5 or "DRAFT_RESEARCH_NOT_PUBLIC" not in body:
            reject("chapter too short or not marked unpublished: "+path)
        if n["event_id"] not in body:
            reject("canonical event ID missing from narrative")
    if paths!=EXPECTED_PATHS:
        reject("missing one narrative")
    phases=d["conflict_periods"]
    if len(phases)!=4:
        reject("exactly four academic phase anchors")
    for p,expect in zip(phases,EXPECTED_PHASES):
        if (p["phase_key"],p["year_start"],p["year_end"],p["classification"])!=expect:
            reject("phase identity/date changed")
        if p["analytical_periodization"] is not True or p["no_claim_of_armistice_between_phases"] is not True or not p["milestones_en"]:
            reject("phase falsely represented as literal ceasefire")
        check_evidence(p["source_keys"])
    treaties=d["treaty_instruments"]
    if len(treaties)!=3 or {t["treaty_key"] for t in treaties}!=set(EXPECTED_TREATIES):
        reject("three separate peace treaty instruments required")
    tr={}
    for t in treaties:
        key=t["treaty_key"]
        if (t["document_kind"],t["site"],t["signing_date"])!=EXPECTED_TREATIES[key]:
            reject("treaty counterparty/location/date conflated")
        if t["primary_full_text_collated"] is not False or not t["signatories_context"] or not t["topics"]:
            reject("unverified treaty text or missing context")
        check_evidence(t["source_keys"])
        if set(t["not_same_as"]) != set(EXPECTED_TREATIES)-{key}:
            reject("treaty identity exclusions erased")
        tr[key]=t
    for key in ("WAR-TREATY-IPO-1648","WAR-TREATY-IPM-1648"):
        if tr[key]["old_style_date"]!="1648-10-14":
            reject("old-style date confusion")
    if tr["WAR-TREATY-DUTCH-SPAIN-1648"]["ratification_oath_date"]!="1648-05-15":
        reject("Dutch-Spanish January signing vs May oath conflation")
    clauses=d["article_anchors"]
    if len(clauses)!=8 or {c["clause_key"] for c in clauses}!=set(EXPECTED_CLAUSES):
        reject("IPO clause inventory drift")
    for c in clauses:
        if (c["article"],c["section"])!=EXPECTED_CLAUSES[c["clause_key"]]:
            reject("wrong article, especially VII vs II")
        if c["treaty_key"]!="WAR-TREATY-IPO-1648":
            reject("IPO legal provision incorrectly assigned to IPM")
        if c["direct_original_language_collated"] is not False or c["public_visible"] is not False or not c["summary_ko"]:
            reject("unverified original language clause or empty assertion")
        check_evidence(c["source_keys"])
    # Semantic ties preserved across revisions.
    by_type={c["interpretation_label"]:c for c in clauses}
    if "NORMAL_YEAR_1624_01_01" not in by_type or by_type["NORMAL_YEAR_1624_01_01"]["article"]!="V":
        reject("1624 normal year lost")
    if "REFORMED_CONFESSION_INCLUSION" not in by_type or by_type["REFORMED_CONFESSION_INCLUSION"]["article"]!="VII":
        reject("Reformed confession not in Article VII")
    art=d["media_research_only"]
    if len(art)!=1:
        reject("one research illustration only")
    img=art[0]
    if (img["event_date"],img["actual_event_treaty_key"])!=("1648-05-15","WAR-TREATY-DUTCH-SPAIN-1648"):
        reject("ter Borch painting attached to wrong peace treaty")
    if set(img["does_not_depict"])!={"WAR-TREATY-IPO-1648","WAR-TREATY-IPM-1648"}:
        reject("painting exclusion metadata missing")
    if (img["national_gallery_inventory"],img["rijksmuseum_display_inventory"])!=("NG896","SK-C-1683"):
        reject("art object original/loan context lost")
    if img["image_downloaded"] is not False or img["reproduction_rights_approved"] is not False:
        reject("unlicensed history picture")
    check_evidence(img["source_keys"])
    holds=d["historical_holds"]
    if len(holds)<9 or len({h["key"] for h in holds})!=len(holds) or any(h["state"]!="OPEN" for h in holds):
        reject("uncertainty holds closed without review")
    return {"chapters":3,"phases":4,"treaties":3,"clauses":8,"sources":len(src),"public":0}

if __name__=="__main__":
    out=validate()
    print("PASS VOL05 war/Westphalia: 3 chapters, 4 phases, 3 treaties, 8 IPO clauses, 11 source records, PUBLIC 0")
