#!/usr/bin/env python3
"""VOL05 IPO Latin clause audit: reference/quotation-level QA only.

Passing does not confirm an authenticated 1648 treaty witness or a collation
against an APW critical edition. No research data is publishable by default.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REGISTRY="data/deep/vol05_ipo_latin_clause_audit_v01.json"
BASE="data/deep/vol05_war_westphalia_research_v01.json"
CLAUSES={
    "IPO-LAT-V-1":("V","1","LEGAL_CONTINUITY"),
    "IPO-LAT-V-2":("V","2","NORMAL_YEAR_1624_01_01"),
    "IPO-LAT-V-34":("V","34","PRIVATE_DEVOTION_PROTECTION"),
    "IPO-LAT-V-36":("V","36","ORDERED_EMIGRATION_STILL_ENVISAGED"),
    "IPO-LAT-V-37":("V","37","MINIMUM_EMIGRATION_PERIODS"),
    "IPO-LAT-VII-1":("VII","1","REFORMED_CONFESSION_INCLUSION"),
    "IPO-LAT-VII-2":("VII","2","OTHER_RELIGIONS_EXCLUDED"),
    "IPO-LAT-VIII-2":("VIII","2","CONSTRAINED_ALLIANCE"),
}
ACCESSES={
    "LATIN_TEXT_READ_WEB","SELECTED_TRANSLATION_EXCERPTS_READ", "INSTITUTIONAL_ARCHIVE_CATALOG_READ",
    "INSTITUTIONAL_RESOURCE_DESCRIPTION_READ","PORTAL_REFERENCED_BUT_DIRECT_FETCH_TIMEOUT",
    "GERMAN_TEXT_EXCERPTS_READ","SEARCH_SNIPPET_ONLY","PRIOR_EXISTING_SUMMARY",
}

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def reject(message):
    raise ValueError(message)

def validate(data=None):
    d=load(REGISTRY) if data is None else data
    if d["kind"]!="VOL05_IPO_LATIN_CLAUSE_AUDIT_RESEARCH_ONLY" or d["status"]!="DRAFT_RESEARCH_NOT_PUBLIC":
        reject("research-only classification changed")
    if (d["volume_id"],d["existing_event_id"],d["existing_work_id"])!=("VOL-05","OV-E-024","OV-D-015"):
        reject("canonical parent identity drift")
    if d["parent_registry"]!=BASE or d["treaty_key"]!="WAR-TREATY-IPO-1648" or d["treaty_date"]!="1648-10-24":
        reject("IPO conflated with IPM or Dutch–Spanish treaty")
    if d["new_canonical_ids"]!=0 or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        reject("canonical ID or app mutation")
    gates=d["release_gate"]
    if set(gates)!={"scholarly_review","editorial_review","printed_latin_collated","complete_multilingual_collation","media_rights_approved","publish","can_ship"} or any(gates.values()):
        reject("research publication gate bypass")
    base=load(BASE)
    if base["existing_document_id"]!="OV-D-015" or "OV-E-024" not in base["existing_event_ids"]:
        reject("missing previous research/canonical mapping")
    if "WAR-TREATY-IPO-1648" not in {t["treaty_key"] for t in base["treaty_instruments"]}:
        reject("parent is not IPO")
    if d["research_docs"]!=["docs/01_CONTENT/VOL05/IPO_1648_LATIN_CLAUSE_AUDIT_V01.md"]:
        reject("research deliverable registry mismatch")
    for path in d["research_docs"]:
        p=Path(path)
        if p.is_absolute() or ".." in p.parts or not p.suffix==".md":
            reject("invalid research path")
        body=(ROOT/p).read_text(encoding="utf-8")
        if len(body)<4500 or body.count("\n## ")<6 or "DRAFT_RESEARCH_NOT_PUBLIC" not in body:
            reject("missing full historical research narrative")
        for chapter in ["§34","§36","§37","§2","제7조","제8조"]:
            if chapter not in body:
                reject("key section omitted from reader research")
    sources=d["source_records"]
    if len(sources)!=8:
        reject("seven distinct evidence-level references required")
    idx={}
    for s in sources:
        key=s["key"]
        parsed=urlparse(s["url"])
        if key in idx or not key.startswith("IPO-SRC-") or parsed.scheme!="https" or not parsed.netloc:
            reject("duplicate source or invalid HTTPS")
        if s["access"] not in ACCESSES or not s["source_witness"] or not s["usage"] or not s["kind"]:
            reject("no meaningful source evidence tier")
        if s["critical_edition_verified"] is not False or s["original_instrument_collated"] is not False:
            reject("unauthorized claim of APW/1648 print collation")
        if s["rights_clearance"] is not False or s["public_visible"] is not False or s["canonical_source_id"] is not None:
            reject("source promoted or rights invented")
        idx[key]=s
    if idx["IPO-SRC-01"]["access"]!="LATIN_TEXT_READ_WEB":
        reject("online Latin location not observed")
    if idx["IPO-SRC-04"]["access"]!="PORTAL_REFERENCED_BUT_DIRECT_FETCH_TIMEOUT":
        reject("APW portal direct reading falsely claimed")
    if idx["IPO-SRC-05"]["access"]!="GERMAN_TEXT_EXCERPTS_READ":
        reject("historic German transcript source changed")
    anchors=d["clause_anchors"]
    if len(anchors)!=8 or {a["key"] for a in anchors}!=set(CLAUSES):
        reject("eight known clause anchors must remain distinct")
    original_by_article={(c["article"],c["section"]):c for c in base["article_anchors"]}
    for item in anchors:
        key=item["key"]
        if (item["article"],item["paragraph"],item["claim_key"])!=CLAUSES[key]:
            reject("clause ID/meaning misattribution: "+key)
        if (item["article"],item["paragraph"]) not in original_by_article and key not in {
            "IPO-LAT-V-36","IPO-LAT-V-37"
        }:
            reject("new clause not aligned with baseline study")
        if not item["latin_locator"] or len(item["latin_locator"].split())>6 or not item["meaning_ko"] or not item["caution_ko"]:
            reject("no short locator or Korean interpretation/caution")
        if item["latin_source_key"]!="IPO-SRC-01" or item["english_source_key"]!="IPO-SRC-02":
            reject("text source roles confused")
        if (item["observed_at"]!="ONLINE_LATIN_TRANSCRIPTION_SECTION" or
            item["original_signature_page"] is not None or item["original_manuscript_read"] is not False or
            item["original_print_read"] is not False or item["critical_latin_collated"] is not False or
            item["english_parallel_line_collated"] is not False or item["publication_approved"] is not False):
            reject("unverified physical witness/parallel text claim")
    if {x["key"] for x in d["crosscheck_notes"]}!={"IPO-AUDIT-V-34-37","IPO-AUDIT-VII-NUMBER","IPO-AUDIT-VIII-POWER"}:
        reject("three critical historical review cautions required")
    if any("PRINT" in x["status"] and x["status"].endswith("COMPLETE") for x in d["crosscheck_notes"]):
        reject("fabricated print collation")
    if len(d["critical_holds"])<7 or not all(d["critical_holds"]):
        reject("missing historical, collation or rights caveats")
    # The earlier narratives MUST carry the corrected §§34, 36, 37 contrast.
    for rel in [
        "docs/01_CONTENT/VOL05/EVENT_1648_WESTPHALIA_PEACE_V01.md",
        "docs/01_CONTENT/VOL05/AUGSBURG_1555_WESTPHALIA_1648_LEGAL_COMPARE_V01.md",
    ]:
        t=(ROOT/rel).read_text(encoding="utf-8")
        if not all(needle in t for needle in ["34","36","37"]):
            reject("old unqualified emigration narrative not amended")
    return {"clauses":8,"sources":8,"review_corrections":3,"public_records":0}

if __name__=="__main__":
    result=validate()
    print(f"PASS: IPO {result['clauses']} Latin locations, {result['sources']} sources, 3 corrections, PUBLIC 0")
