#!/usr/bin/env python3
"""Research-only structural and source-link QA: VOL-04/05 episode expansion.

Validates identifiers and review gates, NOT historical accuracy, complete
original-language collation, authorial attribution or image reproduction rights.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATH = "data/deep/vol04_05_next_events_registry_v01.json"
SOURCES = [
    "data/deep/vol04_luther_v01.json",
    "data/deep/vol04_zwingli_v01.json",
    "data/deep/vol04_melanchthon_v01.json",
    "data/deep/vol04_calvin_v01.json",
]
EXPECTED = {
    "EP-V04-WORMS-1521": ("VOL-04", "OV-E-016", 1521, 1521),
    "EP-V04-ZURICH-1523-27": ("VOL-04", None, 1523, 1527),
    "EP-V04-ENGLAND-1533-59": ("VOL-04", None, 1533, 1559),
    "EP-V05-AUGSBURG-1555": ("VOL-05", "OV-E-022", 1555, 1555),
}

def read(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def validate(reg=None):
    reg = read(PATH) if reg is None else reg
    if reg["kind"] != "REFORMATION_NEXT_EVENTS_RESEARCH_ONLY":
        raise ValueError("wrong data contract")
    if any(reg["publication_gate"].values()) or reg["canonical_ids_issued"] != 0:
        raise ValueError("publication or canonical ID gate opened")
    if reg["overview_unchanged"] is not True or reg["ai_studio_unchanged"] is not True:
        raise ValueError("overview or AI Studio modifications asserted")
    if reg["original_text_collated"] is not False:
        raise ValueError("falsely claiming original-language collation")
    episodes = reg["cases"]
    if len(episodes) != 4 or set(e["episode_key"] for e in episodes) != set(EXPECTED):
        raise ValueError("wrong or duplicated episode inventory")
    overview = read("data/overview/events_documents_v01.json")
    people = read("data/overview/volumes_and_people_v01.json")
    event_ids = {x["id"]: x for x in overview["events"]}
    doc_ids = {x["id"] for x in overview["documents"]}
    person_ids = {x["id"] for x in people["people"]}
    crosswalk = read("data/deep/vol04_four_reformers_crosswalk_v01.json")
    deep_ids = {x["deep_event_id"]: x for x in crosswalk["event_crosswalk"]}
    claims = {}
    for path in SOURCES:
        dataset = read(path)
        source_ids = {s["id"] for s in dataset["sources"]}
        for claim in dataset["claims"]:
            if not claim["source_ids"] or not set(claim["source_ids"]) <= source_ids:
                raise ValueError("pre-existing source/claim link broken")
            claims[claim["id"]] = claim
    seen_paths = set()
    source_links = 0
    for e in episodes:
        key = e["episode_key"]
        volume, existing, year_start, year_end = EXPECTED[key]
        if (e["volume_id"], e["canonical_event_id"], e["year_start"], e["year_end"]) != (volume, existing, year_start, year_end):
            raise ValueError("canonical/volume/date drift: " + key)
        if existing:
            original = event_ids[existing]
            if original["year_start"] != year_start or volume not in original["volume_ids"]:
                raise ValueError("canonical event refers to wrong era/volume")
            if e["route_policy"] != "REFERENCE_EXISTING_OVERVIEW_EVENT":
                raise ValueError("incorrect route policy for existing event")
        elif e["route_policy"] != "NO_NEW_CANONICAL_EVENT_ROUTE":
            raise ValueError("invented route")
        if (e["status"] != "DRAFT_RESEARCH_NOT_PUBLIC"
            or e["approved"] is not False
            or e["release_approved"] is not False
            or e["full_original_collation"] is not False
            or e["media_reuse_approved"] is not False):
            raise ValueError("case release gate opened: " + key)
        if not e["evidence_limit_ko"]:
            raise ValueError("critical evidence caution removed")
        if any(p not in person_ids for p in e["existing_people"]):
            raise ValueError("unknown person ID")
        if any(d not in doc_ids for d in e["existing_documents"]):
            raise ValueError("unknown document ID")
        if e["deep_event_ref"] is not None:
            d = deep_ids[e["deep_event_ref"]]
            if d["year_start"] < year_start or d["year_start"] > year_end:
                raise ValueError("crosswalk event year mismatch")
            if existing and d["canonical_event_id"] != existing:
                raise ValueError("existing event crosswalk mismatch")
            if not existing and d["canonical_event_id"] is not None:
                raise ValueError("research-only crosswalk promoted")
        rel = Path(e["body_path"])
        if rel.is_absolute() or ".." in rel.parts or rel.suffix != ".md" or str(rel) in seen_paths:
            raise ValueError("unsafe or duplicate narrative file path")
        seen_paths.add(str(rel))
        body = (ROOT / rel).read_text(encoding="utf-8")
        if len(body) < 3000 or body.count("\n## ") < 4:
            raise ValueError("missing developed chapter")
        if "DRAFT_RESEARCH_NOT_PUBLIC" not in body:
            raise ValueError("missing explicit publication block")
        if existing and existing not in body:
            raise ValueError("chapter missing canonical event ID")
        if not existing and e["deep_event_ref"] and e["deep_event_ref"] not in body:
            raise ValueError("chapter missing candidate identifier")
        if len(set(e["claim_ids"])) != len(e["claim_ids"]) or any(c not in claims for c in e["claim_ids"]):
            raise ValueError("orphaned or repeated claims")
        urls = e["source_urls"]
        if not urls or len(urls) != len(set(urls)):
            raise ValueError("missing or repeated source links")
        for url in urls:
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError("invalid URL")
        source_links += len(urls)
    # Semantic boundaries: the Schleitheim canonical event is not Manz's trial;
    # the Augsburg Confession of 1530 is not the Peace of 1555.
    by_id = {e["episode_key"]: e for e in episodes}
    if by_id["EP-V04-ZURICH-1523-27"]["canonical_event_id"] is not None:
        raise ValueError("1527 Manz/Schleitheim event conflation")
    if "OV-D-010" not in by_id["EP-V04-ZURICH-1523-27"]["existing_documents"]:
        raise ValueError("Schleitheim document edge lost")
    if by_id["EP-V05-AUGSBURG-1555"]["volume_id"] != "VOL-05":
        raise ValueError("1555 border with Volume 05 lost")
    if "OV-D-013" not in by_id["EP-V04-ENGLAND-1533-59"]["existing_documents"]:
        raise ValueError("Prayer Book must retain existing ID")
    return {"chapters":len(episodes), "source_urls":source_links,"public_records":0}

if __name__ == "__main__":
    result=validate()
    print(f"PASS: {result['chapters']} chapters, {result['source_urls']} linked institutional URLs, public=0")
