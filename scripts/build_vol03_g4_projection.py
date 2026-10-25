#!/usr/bin/env python3
"""Build or validate a nonpublic, read-only VOL-03 G4 projection.

Default mode checks the transformation without writing files. The optional
--output argument writes a review-only JSON snapshot and MUST NOT be used as
a publication artifact. Python 3.11+ standard library only.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/contracts/atlas_contract_v01.json"


def read(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def build() -> dict:
    source = read("data/vol03_integrated_catalog_v08.json")
    base_events = {x["id"]: x for x in read("data/events.json")}
    ext_events = {x["id"]: x for x in read("data/vol03_extension.json")["events"]}
    events = {**base_events, **ext_events}
    claims = {x["id"]: x for x in read("data/vol03_primary_claims.json")["claims"]}
    contract = read("data/contracts/atlas_contract_v01.json")
    review = read("data/vol03_v13_review_gates.json")
    release = source["publication_gate"]
    if release["approved"] or release["can_ship"] or contract["release_gate"]["can_ship"] or review["publication_gate"]["can_ship"]:
        raise ValueError("Publishing gate unexpectedly open")
    prepared = []
    for node in source["nodes"]:
        item = {
            "id": node["id"],
            "type": node["type"],
            "title_ko": node["title"],
            "volume_ids": ["VOL-03"],
            "source_ids": list(node.get("source_ids", [])),
            "review_status": node.get("review_status", "DRAFT"),
            "public_visible": False,
        }
        if node["type"] == "event":
            event = events.get(node["id"])
            if event is None:
                raise ValueError("Missing canonical event: " + node["id"])
            label = event.get("date_label") or event.get("date_display")
            precision = event.get("date_precision")
            date = event.get("date_start")
            if not label and not date:
                raise ValueError("No event time metadata: " + node["id"])
            if not precision:
                raise ValueError("Missing event date precision: " + node["id"])
            # A historical date is copied from the canonical source, never fabricated.
            item["date"] = {
                "date_label": label or date,
                "date_precision": precision,
                "year_start": event.get("year_start"),
                "year_end": event.get("year_end"),
                "date_start": date,
            }
            item["entity_links"] = event.get("person_ids", event.get("actor_ids", [])) + event.get("location_ids", [])
        elif node["type"] == "claim":
            c = claims.get(node["id"])
            if c is None:
                raise ValueError("Claim ID is missing: " + node["id"])
            item["certainty"] = c["certainty"]
            item["statement_access"] = c["evidence_tier"]
            item["entity_links"] = [c["subject_id"]]
        elif node["type"] in ("asset_pending_binary", "asset_committed", "map_view"):
            item["asset_state"] = ("BINARY_PENDING_LOCAL_IMPORT" if node["type"] == "asset_pending_binary" else "DRAFT")
            item["rights_status"] = "REVIEW_PENDING"
            item["requires_human_approval"] = True
        prepared.append(item)
    return {
        "schema_version": "0.1",
        "volume_id": "VOL-03",
        "kind": "READ_ONLY_REVIEW_PROJECTION",
        "source": "data/vol03_integrated_catalog_v08.json",
        "canonical_modified": False,
        "publication_gate": {"approved": False, "can_ship": False},
        "nodes": prepared,
        "edges": list(source["edges"]),
    }


def validate(out: dict) -> list[str]:
    faults: list[str] = []
    contract = read("data/contracts/atlas_contract_v01.json")
    required = contract["normalized_projection_v01"]["required"]
    base = read("data/vol03_integrated_catalog_v08.json")
    claims = read("data/vol03_primary_claims.json")["claims"]
    if len(out["nodes"]) != len(base["nodes"]) or len(out["nodes"]) != 182:
        faults.append("source node count drift")
    if len(out["edges"]) != len(base["edges"]) or len(out["edges"]) != 365:
        faults.append("source edge count drift")
    ids = [n["id"] for n in out["nodes"]]
    node_ids = set(ids)
    if len(ids) != len(node_ids):
        faults.append("duplicate projected IDs")
    for node in out["nodes"]:
        if any(k not in node for k in required):
            faults.append("missing required fields: " + node["id"])
        if node["public_visible"] or node["review_status"] != "DRAFT":
            faults.append("unsafe publication state: " + node["id"])
        if any(s not in node_ids for s in node["source_ids"]):
            faults.append("unresolved source ID: " + node["id"])
        if node["type"] == "event":
            if node["date"]["date_precision"] not in contract["normalized_projection_v01"]["date"]["precision_values"]:
                faults.append("invalid time precision: " + node["id"])
        if node["type"] == "claim" and not node["source_ids"]:
            faults.append("claim without evidence: " + node["id"])
    if {x["id"] for x in claims} != {n["id"] for n in out["nodes"] if n["type"] == "claim"}:
        faults.append("claim coverage drift")
    if any(e["from"] not in node_ids or e["to"] not in node_ids for e in out["edges"]):
        faults.append("dangling edge")
    if out["publication_gate"]["approved"] or out["publication_gate"]["can_ship"]:
        faults.append("open release gate")
    return faults


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, help="Optional local review snapshot, not a publication artifact")
    args = p.parse_args()
    try:
        projection = build()
        faults = validate(projection)
        for error in faults:
            print("FAIL " + error)
        if faults:
            return 1
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(projection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print("WROTE REVIEW-ONLY SNAPSHOT: " + str(args.output))
        print("PASS G4 read-only adapter | nodes=%d edges=%d claims=%d public=0" % (
            len(projection["nodes"]), len(projection["edges"]),
            sum(n["type"] == "claim" for n in projection["nodes"])))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as e:
        print("FAIL: " + str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
