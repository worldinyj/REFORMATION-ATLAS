#!/usr/bin/env python3
"""VOL-04 event narratives: five research-only reader episodes and provenance checks.

Does NOT verify manuscript wording or grant release permission.
Python standard library; no writes.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/deep/vol04_event_narrative_registry_v01.json"
DATASETS = [
    "data/deep/vol04_luther_v01.json",
    "data/deep/vol04_zwingli_v01.json",
    "data/deep/vol04_melanchthon_v01.json",
    "data/deep/vol04_calvin_v01.json",
]
EXPECTED = {
    "EP-V04-1525-01": (1525, None),
    "EP-V04-1529-01": (1529, "OV-E-018"),
    "EP-V04-1530-01": (1530, "OV-E-019"),
    "EP-V04-1541-01": (1541, None),
    "EP-V04-1553-01": (1553, None),
}

def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

def reject(reason: str) -> None:
    raise ValueError(reason)

def check(data: dict | None = None) -> dict:
    reg = load("data/deep/vol04_event_narrative_registry_v01.json") if data is None else data
    if reg["kind"] != "VOL04_EVENT_NARRATIVES_RESEARCH_ONLY" or reg["status"] != "DRAFT":
        reject("research-only status changed")
    if reg["web_app_modified"] is not False or reg["overview_mutated"] is not False:
        reject("web/overview mutations are forbidden")
    if reg["canonical_ids_minted"] != 0 or any(reg["release"].values()):
        reject("unapproved public release")
    episodes = reg["episodes"]
    if reg["event_count"] != 5 or len(episodes) != 5:
        reject("five-episode inventory changed")
    if {e["episode_id"] for e in episodes} != set(EXPECTED):
        reject("episode identities missing or duplicated")
    overview = load("data/overview/events_documents_v01.json")
    people = load("data/overview/volumes_and_people_v01.json")
    overview_events = {x["id"]: x for x in overview["events"]}
    overview_docs = {x["id"]: x for x in overview["documents"]}
    canonical_people = {x["id"]: x for x in people["people"]}
    crosswalk = load("data/deep/vol04_four_reformers_crosswalk_v01.json")
    deep_ids = {x["deep_event_id"]: x for x in crosswalk["event_crosswalk"]}
    sources, claims = {}, {}
    for file in DATASETS:
        d = load(file)
        for s in d["sources"]:
            if s["id"] in sources:
                reject("duplicate source registration " + s["id"])
            sources[s["id"]] = s
        for c in d["claims"]:
            if c["id"] in claims:
                reject("duplicate claim " + c["id"])
            claims[c["id"]] = c
    unique_paths = set()
    source_edges = 0
    for ep in episodes:
        key = ep["episode_id"]
        expyear, expcanonical = EXPECTED[key]
        if ep["year"] != expyear or ep["existing_event_id"] != expcanonical:
            reject("year or canonical event identity mismatch: " + key)
        if expcanonical:
            if overview_events[expcanonical]["year_start"] != expyear:
                reject("wrong original event year")
            if ep["route_policy"] != "EXISTING_OVERVIEW_ID_REFERENCE_ONLY":
                reject("original event route unsafe")
        elif ep["route_policy"] != "NO_NEW_PUBLIC_ROUTE":
            reject("candidate illegally exposed as route")
        if ep["date_precision"] not in ("year","day","period") or not ep["date_label"]:
            reject("invented date precision")
        if (ep["approval"] is not False or ep["publication_approved"] is not False
                or ep["source_text_collated"] is not False
                or ep["media_rights_approved"] is not False
                or ep["review_state"] != "DRAFT_HISTORICAL_REVIEW"):
            reject("event publication/claims promoted")
        if not ep.get("critical_hold"):
            reject("uncertainty hold removed")
        if not ep["related_person_ids"] or any(p not in canonical_people for p in ep["related_person_ids"]):
            reject("unknown canonical person")
        if any(p not in overview_docs for p in ep["related_document_ids"]):
            reject("unknown document")
        if not ep["linked_deep_event_ids"] or any(d not in deep_ids for d in ep["linked_deep_event_ids"]):
            reject("unknown crosswalk event")
        for deepid in ep["linked_deep_event_ids"]:
            if deep_ids[deepid]["year_start"] != expyear:
                reject("deep candidate wrong year")
            if expcanonical and deep_ids[deepid]["canonical_event_id"] != expcanonical:
                reject("duplicate canonical event linkage")
            if not expcanonical and deep_ids[deepid]["canonical_event_id"] is not None:
                reject("candidate must not get canonical ID automatically")
        p = Path(ep["body_path"])
        if p.is_absolute() or ".." in p.parts or p.suffix != ".md" or str(p) in unique_paths:
            reject("invalid or repeated episode path")
        unique_paths.add(str(p))
        body = (ROOT / p).read_text(encoding="utf-8")
        if len(body) < 3100 or body.count("\n## ") < 4:
            reject("episode lacks developed reader narrative: " + str(p))
        if "**DRAFT" not in body or "비공개" not in body:
            reject("episode missing editorial draft disclosure")
        if expcanonical:
            if expcanonical not in body:
                reject("existing event ID not reused")
        elif not any(d in body for d in ep["linked_deep_event_ids"]):
            reject("candidate record not noted in story")
        if len(set(ep["claim_ids"])) != len(ep["claim_ids"]) or not ep["claim_ids"]:
            reject("episode claim references invalid")
        if len(set(ep["source_ids"])) != len(ep["source_ids"]) or not ep["source_ids"]:
            reject("episode source references invalid")
        if set(ep["claim_ids"]) - set(claims) or set(ep["source_ids"]) - set(sources):
            reject("orphan claims or sources")
        registered_sources = set(ep["source_ids"])
        for claim_id in ep["claim_ids"]:
            if not set(claims[claim_id]["source_ids"]) <= registered_sources:
                reject("original claim/source trace broken: " + claim_id)
        if not ep["extra_source_urls"] or len(set(ep["extra_source_urls"])) != len(ep["extra_source_urls"]):
            reject("missing/duplicate institutional evidence")
        for url in ep["extra_source_urls"]:
            parts = urlsplit(url)
            if parts.scheme != "https" or not parts.hostname:
                reject("invalid evidence URL")
        source_edges += len(ep["source_ids"])
    return {"episodes": len(episodes),"historical_source_edges":source_edges,
            "canonical_events_reused":sum(e["existing_event_id"] is not None for e in episodes),
            "research_candidates":sum(e["existing_event_id"] is None for e in episodes),
            "publication_approved":False}

if __name__ == "__main__":
    result = check()
    print("PASS: 5 reader episodes; reused 2 events, 3 candidates; "
          f"{result['historical_source_edges']} source links; PUBLIC 0")
