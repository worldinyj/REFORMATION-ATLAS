#!/usr/bin/env python3
"""VOL-04 non-public provenance graph adapter (V0.3).

Read-only review graph: work -> provisional edition -> comparison -> registered
source URL, with carefully scoped person/event associations.
NO public exporter, canonical IDs, HTTP API or web bundle.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

from build_vol04_edition_ui_review_v02 import (
    inputs, make_review_view, make_public_projection, safe_review_destination
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "data/deep/vol04_comparison_provenance_crosswalk_v01.json"

def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def build_review_graph(d: dict | None = None, reg: dict | None = None) -> dict:
    d = inputs() if d is None else d
    reg = read(REGISTRY) if reg is None else reg
    base = make_review_view(d)  # validates parent/edition/case consistency
    public = make_public_projection(d)
    if public["records"] or public["release_approved"]:
        raise ValueError("public projection unexpectedly nonempty")
    if reg.get("status") != "UNAPPROVED_PROVENANCE_CROSSWALK":
        raise ValueError("research registry status changed")
    if any(reg.get(x) is not False for x in
           ("publication_approved", "access_verified_this_revision",
            "source_text_collated", "human_approved")):
        raise ValueError("unverified scholarly or release approval assertion")
    gates = reg.get("release_gate", {})
    if gates.get("can_ship") is not False or gates.get("allow_web_import") is not False:
        raise ValueError("release gate open")
    if gates.get("requires_separate_manifest") is not True:
        raise ValueError("human release manifest bypass")
    registered = reg["source_records"]
    if len(registered) != 7:
        raise ValueError("comparison source inventory drift")
    source_index = {}
    urls = set()
    for rec in registered:
        key, url = rec["research_source_key"], rec["url"]
        parts = urlsplit(url)
        if not key.startswith("CMP-SRC-PROP-") or key in source_index:
            raise ValueError("bad/duplicate research source key")
        if parts.scheme != "https" or not parts.netloc or url in urls:
            raise ValueError("bad/duplicate source URL")
        if not rec.get("classification") or not rec.get("label_ko"):
            raise ValueError("unclassified source")
        if (rec.get("verification_state") != "LINK_REGISTERED_NOT_RECHECKED"
                or rec.get("original_witness") is not False
                or rec.get("rights_approved") is not False
                or rec.get("publication_approved") is not False
                or rec.get("canonical_source_id") is not None):
            raise ValueError("source evidence/rights prematurely promoted")
        source_index[key] = rec
        urls.add(url)
    base_cases = {case["research_case_key"]: case for case in base["cases"]}
    research_cases = {case["case_id"]: case for case in d["comparisons"]["comparison_cases"]}
    links = reg["comparisons"]
    if len(links) != len(base_cases) or len({x["case_id"] for x in links}) != len(links):
        raise ValueError("duplicate/incomplete comparison mapping")
    people = {x["id"]: x for x in read("data/overview/volumes_and_people_v01.json")["people"]}
    events = {x["id"]: x for x in read("data/overview/events_documents_v01.json")["events"]}
    works = {x["id"]: x for x in read("data/overview/events_documents_v01.json")["documents"]}
    expected_work_ids = {"OV-D-011", "OV-D-012"}
    if not expected_work_ids <= set(works):
        raise ValueError("missing stable work identifiers")
    graph_cases = []
    linked_source_keys = []
    for entry in links:
        key = entry["case_id"]
        if key not in base_cases or entry["work_reference"] != base_cases[key]["work_reference_review_only"]:
            raise ValueError("case/work reference mismatch")
        source_keys = entry["source_keys"]
        research_urls = research_cases[key]["sources"]
        if len(source_keys) != len(set(source_keys)) or len(source_keys) != len(research_urls):
            raise ValueError("duplicated/incomplete source linkage")
        if any(sk not in source_index for sk in source_keys):
            raise ValueError("unknown research source")
        if [source_index[sk]["url"] for sk in source_keys] != research_urls:
            raise ValueError("comparison source URL mismatch or order drift")
        linked_source_keys.extend(source_keys)
        if not entry.get("caution_ko"):
            raise ValueError("missing historical association caution")
        for rel in entry["related_people"]:
            if rel["id"] not in people or not rel.get("relation"):
                raise ValueError("unknown person or unqualified relationship")
        for rel in entry["related_events"]:
            if rel["id"] not in events or not rel.get("relation"):
                raise ValueError("unknown event or unqualified relationship")
        graph_cases.append({
            "research_case_key":key,
            "work_reference_review_only":entry["work_reference"],
            "tab":base_cases[key]["tab"],
            "editions":base_cases[key]["editions"],
            "observation_ko":base_cases[key]["observation_ko"],
            "interpretation_ko":base_cases[key]["interpretation_ko"],
            "evidence_level":base_cases[key]["evidence_level"],
            "source_links_review_only":[{
                "research_source_key":sk,
                "url":source_index[sk]["url"],
                "classification":source_index[sk]["classification"],
                "verified_in_this_revision":False,
            } for sk in source_keys],
            "people_context":entry["related_people"],
            "events_context":entry["related_events"],
            "caution_ko":entry["caution_ko"],
            "public_visible":False,
            "route":None,
        })
    if set(linked_source_keys) != set(source_index):
        raise ValueError("unreferenced/stray source record")
    if {c["research_case_key"] for c in graph_cases} != set(base_cases):
        raise ValueError("comparison coverage")
    return {
        "schema_version":"0.3",
        "kind":"RESEARCH_PROVENANCE_GRAPH_ONLY",
        "web_import_allowed":False,
        "publication_approved":False,
        "public_records":[],
        "cases":graph_cases,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-output", help="Optional JSON OUTSIDE the repository only")
    args = parser.parse_args()
    graph = build_review_graph()
    if args.review_output:
        target = safe_review_destination(args.review_output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("RESEARCH ONLY / NEVER DEPLOY:", target)
    print("PASS VOL04 V0.3 | cases=3 sources=7 publication=0")

if __name__ == "__main__":
    main()
