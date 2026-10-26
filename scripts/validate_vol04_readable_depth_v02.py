#!/usr/bin/env python3
"""Validate four readable VOL-04 historical narrative V0.2 chapters.

Research-only: this test is not an original-language collation or publication
authorization. Python 3.11 standard library; neither modifies nor exports content.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/deep/vol04_readable_depth_registry_v02.json"
PERSON_IDS = {"OV-P-013", "OV-P-014", "OV-P-015", "OV-P-016"}
KNOWN_PREFIX = {
    "OV-P-013": "CLM-V04-L-",
    "OV-P-014": "CLM-V04-ME-",
    "OV-P-015": "CLM-V04-ZW-",
    "OV-P-016": "CLM-V04-CA-",
}
REQUIRED_HOLDS = {
    "HOLD-V04-N2-01", "HOLD-V04-N2-02", "HOLD-V04-N2-03",
    "HOLD-V04-N2-04", "HOLD-V04-N2-05",
}

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def check() -> None:
    d = load(REGISTRY)
    if d["kind"] != "READABLE_DEEP_RESEARCH_REGISTRY":
        raise ValueError("wrong narrative registry type")
    if d["status"] != "RESEARCH_DRAFT" or d["canonical_ids_minted"] != 0:
        raise ValueError("narrative registry unexpectedly promoted")
    if d["existing_overview_unchanged"] is not True:
        raise ValueError("overview must remain immutable")
    if any(d["publication_gate"].values()):
        raise ValueError("release gate must be closed")
    if len(d["records"]) != 4 or {x["person_id"] for x in d["records"]} != PERSON_IDS:
        raise ValueError("person coverage or duplicate person")
    keys = set()
    total = 0
    for person in d["records"]:
        if (person["volume_id"] != "VOL-04" or
            not person["inherit_existing_person_id"] or
            not person["inherit_existing_depth_block_id"] or
            person["approved"] or person["publication_approved"] or
            person["review_status"] != "DRAFT_RESEARCH_NOT_PUBLIC"):
            raise ValueError("unsafe person-level record: " + person["person_id"])
        srcpath = ROOT / person["source_dataset"]
        canonical = load(srcpath)
        sources = {s["id"] for s in canonical["sources"]}
        claims = {c["id"]: c for c in canonical["claims"]}
        if person["depth_block_id"] not in str(canonical):
            raise ValueError("missing canonical depth block: " + person["person_id"])
        if person["person_id"] not in str(canonical):
            raise ValueError("person does not match original research")
        relative = Path(person["body_path"])
        if relative.is_absolute() or ".." in relative.parts or relative.suffix != ".md":
            raise ValueError("unsafe narrative document path")
        body = (ROOT / relative).read_text(encoding="utf-8")
        if len(body) < 2700 or body.count("\n## ") < 5:
            raise ValueError("narrative insufficiently developed: " + str(relative))
        if "**DRAFT" not in body or "공개 불가" not in body:
            raise ValueError("missing draft warning: " + str(relative))
        if person["person_id"] not in body or person["depth_block_id"] not in body:
            raise ValueError("narrative not linked to person/depth block")
        if len(person["sections"]) != 5:
            raise ValueError("expected five narrative modules per person")
        for sec in person["sections"]:
            key = sec["section_key"]
            if key in keys or not key or not sec["title_ko"]:
                raise ValueError("duplicate/unnamed section " + str(key))
            keys.add(key)
            total += 1
            if sec["review_status"] != "DRAFT" or sec["public_visible"] or sec["text_collated"]:
                raise ValueError("section release gate illegally open")
            if sec["source_ids_resolved_by"] != "parent_claim_source_ids":
                raise ValueError("sources must inherit from original claim registry")
            if not sec["claim_ids"] or len(set(sec["claim_ids"])) != len(sec["claim_ids"]):
                raise ValueError("missing/duplicate claim references")
            for cid in sec["claim_ids"]:
                if cid not in claims or not cid.startswith(KNOWN_PREFIX[person["person_id"]]):
                    raise ValueError("unknown claim: " + cid)
                claim_sources = claims[cid]["source_ids"]
                if not claim_sources or not set(claim_sources) <= sources:
                    raise ValueError("broken source cross-reference: " + cid)
    if total != 20:
        raise ValueError("section coverage drift")
    holds = d["known_source_cautions"]
    if {h["id"] for h in holds} != REQUIRED_HOLDS or any(h["state"] != "OPEN" for h in holds):
        raise ValueError("historical uncertainty holds disappeared")
    comparison = ROOT / "docs/01_CONTENT/VOL04/FOUR_REFORMERS_COMPARATIVE_NARRATIVE_V02.md"
    text = comparison.read_text(encoding="utf-8")
    if any(p not in text for p in PERSON_IDS):
        raise ValueError("comparative narrative missing one person")
    if text.count("NARRATIVE_DEPTH_V02.md") < 4:
        raise ValueError("comparative narrative missing backlinks")
    print("PASS: 4 narrative chapters, 20 evidence-linked sections, 5 open cautions; public=0")

if __name__ == "__main__":
    check()
