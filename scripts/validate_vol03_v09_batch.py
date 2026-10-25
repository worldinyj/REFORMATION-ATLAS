#!/usr/bin/env python3
"""VOL-03 V0.9 read-only consistency checks. Python 3.11+, standard library only.

Run from any directory:
    python3 scripts/validate_vol03_v09_batch.py
    python3 scripts/validate_vol03_v09_batch.py --illustrations-zip /path/to/REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip

This script does not alter, install, approve, publish, or merge any asset.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def check(condition: bool, description: str, failures: list[str]) -> None:
    print(f"{'PASS' if condition else 'FAIL'} {description}")
    if not condition:
        failures.append(description)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--illustrations-zip", type=Path, help="Optional ORIGINAL image ZIP to validate, never installs it")
    args = parser.parse_args()

    graph = load("data/vol03_integrated_catalog_v08.json")
    claims = load("data/vol03_primary_claims.json")
    batch = load("data/vol03_batch_source_review_v09.json")
    visual = load("data/vol03_visual_review_v09_p2.json")
    points = load("data/vol03_map_points.json")
    presentation = load("data/vol03_presentation_index.json")
    stage = load("assets/illustrations/vol03/ILLUSTRATION_STAGE.json")
    manifest = load("assets/asset_manifest.json")

    failures: list[str] = []
    node_ids = {n["id"] for n in graph["nodes"]}
    claim_ids = {c["id"] for c in claims["claims"]}
    source_ids = {n["id"] for n in graph["nodes"] if n["type"] == "source_reference"}
    map_assets = {a["asset_id"] for a in manifest if a["asset_id"].startswith("MAP-")}
    staged = {a["id"]: a for a in stage["assets"]}

    check(len(graph["nodes"]) == len(node_ids) == 182, "182 unique original graph nodes", failures)
    check(len(graph["edges"]) == 365, "365 original graph edges", failures)
    check(all(e["from"] in node_ids and e["to"] in node_ids for e in graph["edges"]), "all graph edge endpoints exist", failures)
    check(len(claim_ids) == len(claims["claims"]) == 14, "14 unique legacy claims", failures)
    check(len(batch["records"]) == 4, "four bounded primary-source reviews A-D", failures)
    check({c for r in batch["records"] for c in r["claim_ids"]} == claim_ids, "all 14 claims covered", failures)
    check(all(c in claim_ids for r in batch["records"] for c in r["claim_ids"]), "all claim links valid", failures)
    check(all(s in source_ids for r in batch["records"] for s in r["source_ids"]), "all evidence source IDs valid", failures)
    check(len(map_assets) == 4 and len(points["points"]) == 13, "four maps and thirteen modern reference points", failures)
    check(len(visual["reviewed_visuals"]) == 10 and len(staged) == 6, "six staged illustrations plus four maps reviewed", failures)
    check(all((v["id"] in map_assets if v["id"].startswith("MAP-") else v["id"] in staged) for v in visual["reviewed_visuals"]), "all 10 visual asset IDs exist", failures)
    check(all(v["review_status"] == "DRAFT" for v in visual["reviewed_visuals"]), "all media review records remain DRAFT", failures)

    media = presentation["people_pages"] + presentation["visual_story_pages"]
    check(all(card["media_id"] in staged for card in media), "web media links resolve to staging records", failures)
    check(all(not card["media_safe_to_display"] for card in media), "no staged media exposed on web", failures)
    check(all(not card.get("is_published", False) for card in media), "no preview record published", failures)

    gates = [graph["publication_gate"], batch["publication_gate"], visual["publication_gate"], presentation["publication_gate"]]
    check(all(not g["approved"] and not g["can_ship"] for g in gates), "all publication gates closed", failures)
    check(stage["state"] == "BINARY_PENDING_LOCAL_IMPORT", "original image binaries still pending local import", failures)
    check(all(not (ROOT / v["relative_path"]).exists() for v in stage["assets"]), "draft WebP assets not silently installed in working tree", failures)
    check(all((ROOT / a["relative_path"]).is_file() for a in manifest if a["asset_id"] in map_assets), "all original SVG maps actually on disk", failures)

    if args.illustrations_zip is not None:
        archive = args.illustrations_zip
        check(archive.is_file(), "optional illustration archive exists", failures)
        if archive.is_file():
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            check(digest == visual["original_image_zip_sha256"], "illustration ZIP hash matches", failures)
            try:
                with zipfile.ZipFile(archive) as z:
                    check(z.testzip() is None, "illustration ZIP CRC clean", failures)
                    for asset in stage["assets"]:
                        matching = [i for i in z.namelist() if i.endswith("/" + asset["file"])]
                        check(len(matching) == 1, f"archive member {asset['id']}", failures)
                        if len(matching) == 1:
                            digest = hashlib.sha256(z.read(matching[0])).hexdigest()
                            check(digest == asset["webp_sha256"], f"WebP hash {asset['id']}", failures)
            except (OSError, zipfile.BadZipFile) as exc:
                failures.append(f"ZIP error: {exc}")

    print(f"\n{'PASS' if not failures else 'FAIL'} V0.9-P3 verification; issues={len(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
