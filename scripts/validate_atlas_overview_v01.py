#!/usr/bin/env python3
"""Validate eight-volume overview content without modifying source files.

Standard library only. DRAFT data can be used for planning, not public release.
Usage: python3 scripts/validate_atlas_overview_v01.py
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / "data" / "overview"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    source = load(PREFIX / "source_register_v01.json")
    people_data = load(PREFIX / "volumes_and_people_v01.json")
    document_data = load(PREFIX / "events_documents_v01.json")
    place_data = load(PREFIX / "places_v01.json")
    related = load(PREFIX / "relationships_and_themes_v01.json")
    crosswalk = load(PREFIX / "legacy_person_crosswalk_v01.json")
    backlog = load(PREFIX / "editorial_backlog_v01.json")
    legacy = load(ROOT / "data/vol03_integrated_catalog_v08.json")
    errors = []

    def check(ok: bool, label: str) -> None:
        print(("PASS " if ok else "FAIL ") + label)
        if not ok:
            errors.append(label)

    volumes = people_data["volumes"]
    persons = people_data["people"]
    events = document_data["events"]
    documents = document_data["documents"]
    places = place_data["places"]
    relationships = related["relationships"]
    topics = related["ideas"]
    sources = source["sources"]

    vol_ids = {x["id"] for x in volumes}
    source_ids = {x["id"] for x in sources}
    all_content = volumes + persons + events + documents + places + topics
    all_ids = [x["id"] for x in all_content]
    identifiers = set(all_ids)
    check(vol_ids == {f"VOL-{i:02d}" for i in range(1, 9)}, "all eight historical volume IDs")
    check(len(all_ids) == len(identifiers), "no duplicate content identifiers")
    check(len(sources) == len(source_ids), "source IDs unique")
    check(len(all_content) == 127 and len(relationships) == 32, "baseline 127 records and 32 relationships")

    for item in all_content:
        refs = item.get("source_ids", [])
        if item["id"].startswith("OV-L-"):
            check(item["evidence_status"] == "LOCATION_REFERENCE_NOT_YET_VERIFIED" and refs == [], "unverified places clearly flagged " + item["id"])
        else:
            check(bool(refs) and all(r in source_ids for r in refs), "source links " + item["id"])
        for volume in item.get("volume_ids", []):
            check(volume in vol_ids, "volume link " + item["id"] + ":" + volume)
        if item["id"].startswith(("OV-", "TOP-")) and "public_visible" in item:
            check(item["public_visible"] is False, "nonpublic record " + item["id"])
    for src in sources:
        parsed = urlparse(src["url"])
        check(parsed.scheme == "https" and bool(parsed.netloc), "HTTPS source " + src["id"])
        check(src["content_copied"] is False, "no copied source body " + src["id"])
        if src["id"] in {"SRC-O-021", "SRC-O-022"}:
            check(src.get("alias_of") == "SRC-O-001" and src["independent_source"] is False, "deduplicated source alias " + src["id"])
    check(sum(s["review_status"] == "WEB_CHECKED" for s in sources) == 11, "only eleven marked spot-checked sources")

    for edge in relationships:
        check(edge["from_id"] in identifiers and edge["to_id"] in identifiers, "relation endpoints " + edge["id"])
        check(all(x in source_ids for x in edge["source_ids"]), "relation evidence " + edge["id"])
        check(edge["public_visible"] is False, "relation not public " + edge["id"])
    check(len({x["id"] for x in relationships}) == len(relationships), "relation IDs unique")

    allowed = {"day", "year", "period", "range", "approximate_period", "approximate_year"}
    for e in events:
        check(e["date_precision"] in allowed, "date precision " + e["id"])
        check(isinstance(e["year_start"], int), "date has sort year " + e["id"])
        if e["year_end"] is not None:
            check(isinstance(e["year_end"], int) and e["year_end"] >= e["year_start"], "date range valid " + e["id"])
        if e["date_precision"] == "day":
            check("일" in e["date_label"], "exact day label explicit " + e["id"])
        check(e["review_status"] == "DRAFT" and e["public_visible"] is False, "date remains draft " + e["id"])
    for d in documents:
        check(d["full_text_included"] is False and d["witness_level"] == "INTRODUCTORY_DESCRIPTION_ONLY", "no copyrighted full source body " + d["id"])
    for p in places:
        check(p["geolocation_status"] == "UNMAPPED_MODERN_PLACE_ONLY" and p["historical_site_confirmed"] is False, "no false historical coordinates " + p["id"])
    for t in topics:
        check(t["volume_id"] == "VOL-08" and all(v in vol_ids for v in t["related_volumes"]), "VOL-08 cross-cutting theme " + t["id"])

    check(len(crosswalk["pairs"]) == 3, "three preexisting VOL-03 person identities mapped")
    graph_ids = {x["id"]: x for x in legacy["nodes"]}
    person_ids = {x["id"] for x in persons}
    for match in crosswalk["pairs"]:
        check(match["overview_id"] in person_ids and match["canonical_id"] in graph_ids, "canonical mapping " + match["overview_id"])
        check(graph_ids.get(match["canonical_id"], {}).get("title") == match["verified_name_in_graph"], "canonical title matches " + match["overview_id"])
    check(legacy["publication_gate"]["approved"] is False and legacy["publication_gate"]["can_ship"] is False, "legacy material remains embargoed")

    for volume in volumes:
        overview_path = ROOT / "docs/01_CONTENT/OVERVIEW" / (volume["id"] + "_OVERVIEW_V01.md")
        check(overview_path.is_file(), "overview manuscript exists " + volume["id"])
        if overview_path.is_file():
            overview_text = overview_path.read_text(encoding="utf-8")
            check(volume["id"] in overview_text and len(overview_text) >= 500, "substantive manuscript " + volume["id"])
        if volume["id"] != "VOL-08":
            check(any(volume["id"] in x["volume_ids"] for x in persons), "volume has people " + volume["id"])
            check(any(volume["id"] in x["volume_ids"] for x in events), "volume has events " + volume["id"])
            check(any(volume["id"] in x["volume_ids"] for x in documents), "volume has documents " + volume["id"])
        else:
            check(len(topics) >= 10, "VOL-08 has cross-volume topics, not forced chronological events")
    check(source["public_release"] is False, "source register not for public release")
    for k, data in [("people", people_data), ("events", document_data), ("places", place_data), ("relations", related)]:
        check(data["publication_gate"]["approved"] is False and data["publication_gate"]["can_ship"] is False, k + " publication gate locked")
    check(bool(backlog["items"]), "editorial follow-up backlog retained")
    print(f"RESULT {'FAIL' if errors else 'PASS'} | overview={len(all_content)} relations={len(relationships)} sources={len(sources)} issues={len(errors)}")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
