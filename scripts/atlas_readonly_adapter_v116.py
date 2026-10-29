#!/usr/bin/env python3
"""Read-only, fail-closed V1.16 cross-volume projection. Never writes to source datasets."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/contracts/atlas_cross_volume_compat_v115.json"

def read(rel):
    path = (ROOT / rel).resolve()
    if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
        raise ValueError("Invalid source path: " + rel)
    return json.loads(path.read_text(encoding="utf-8"))

def adapt():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["migration_mode"] == "read_only_projection_no_source_mutation"
    assert contract["release_gate"]["can_ship"] is False
    result = []
    seen = set()
    for projection in contract["projections"]:
        original = read(projection["source"])
        rows = [original["content_block"]] if projection["collection"] == "content_block" else original[projection["collection"]]
        for source_row in rows:
            mapping = projection["map"]
            record_id = source_row[mapping["id"]]
            if record_id in seen:
                raise ValueError("Duplicate ID: " + record_id)
            seen.add(record_id)
            sources = source_row[mapping["source_ids"]]
            if not isinstance(sources, list) or not sources:
                raise ValueError("Missing provenance: " + record_id)
            raw_volumes = source_row.get(mapping["volume_ids"]) if "volume_ids" in mapping else projection.get("default_volume_ids")
            if isinstance(raw_volumes, str):
                volume_ids = [raw_volumes]
            elif isinstance(raw_volumes, list):
                volume_ids = raw_volumes
            else:
                raise ValueError("Volume missing: " + record_id)
            if not volume_ids or not all(v.startswith("VOL-") for v in volume_ids):
                raise ValueError("Invalid volume: " + record_id)
            date_precision = source_row.get("date_precision", source_row.get("precision"))
            date_label = source_row.get("date_label", source_row.get("date"))
            if date_precision is not None and date_precision not in contract["date_precisions"]:
                raise ValueError("Unknown date precision: " + record_id)
            record = {
                "id": record_id,
                "type": projection["type"],
                "title_ko": source_row[mapping["title_ko"]],
                "volume_ids": volume_ids,
                "source_ids": sources,
                "review_status": source_row.get(mapping["review_status"], "DRAFT") if "review_status" in mapping else "DRAFT",
                "public_visible": False,
                "publication_approved": False,
                "source_file": projection["source"],
                "date_label": date_label,
                "date_precision": date_precision,
            }
            if source_row.get("public_visible") is True or source_row.get("publication_approved") is True:
                raise ValueError("Unexpected public input in research adapter: " + record_id)
            result.append(record)
    return {"schema_version": "1.16-read-only", "status": "DRAFT_RESEARCH_NOT_PUBLIC", "publication_gate": {"approved": False, "can_ship": False}, "records": result}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate without emitting JSON")
    args = parser.parse_args()
    data = adapt()
    if args.check:
        print("PASS: %d records; all retained as non-public." % len(data["records"]))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
