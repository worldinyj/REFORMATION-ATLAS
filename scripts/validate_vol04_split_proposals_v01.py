#!/usr/bin/env python3
"""Validate split proposals without promoting them to web-publishable canonical records."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

def validate(bib, splits):
    errors = []
    parents = {x["proposal_id"]: x for x in bib["items"]}
    expected = {k for k, v in parents.items() if v["split_required_before_promotion"]}
    grouped = [x["parent_proposal_id"] for x in splits["groups"]]
    if len(grouped) != len(set(grouped)) or set(grouped) != expected:
        errors.append("split parent coverage/uniqueness")
    keys = set()
    for group in splits["groups"]:
        parent = parents.get(group["parent_proposal_id"])
        if not parent or parent["work_family"] != group["work_family"]:
            errors.append("work parent mismatch")
        children = group["children"]
        if len(children) < 2:
            errors.append("composite must have >=2 components")
        for item in children:
            key = item["split_key"]
            if key in keys or not key.startswith(group["parent_proposal_id"] + "-S"):
                errors.append("duplicate/invalid split key")
            keys.add(key)
            if not item["language"] or not item["kind"] or not isinstance(item["year"], int):
                errors.append("missing edition discriminator")
            if (item["canonical_id"] is not None or item["publication_approved"]
                or item["rights_approved"] or item["text_collated"]
                or item["source_copy_verified"] or item["source_copy_shelfmark"]):
                errors.append("unapproved promotion/source claim")
    by_parent = {g["parent_proposal_id"]: g["children"] for g in splits["groups"]}
    languages = lambda key: {c["language"] for c in by_parent[key]}
    labels = lambda key: " ".join(c["label"].lower() for c in by_parent[key])
    if languages("EDN-PROP-V04-001") != {"de", "la"} or languages("EDN-PROP-V04-002") != {"de", "la"}:
        errors.append("Augsburg language split")
    if languages("DOC-PROP-V04-010") != {"de", "la"} or "jonas" not in labels("DOC-PROP-V04-010"):
        errors.append("Apology translation distinction")
    if not {"september", "december"} <= set(labels("DOC-PROP-V04-008").split()):
        errors.append("Luther edition split")
    if not {"report", "articles"} <= set(labels("DOC-PROP-V04-004").split()):
        errors.append("Zurich composite print split")
    if any(c["kind"] == "printed_edition" for c in by_parent["EDN-PROP-V04-001"]):
        errors.append("1530 submission wrongly called print")
    if splits["publication_approved"] or splits["canonical_ids_issued"] != 0:
        errors.append("publication/id gate")
    return sorted(set(errors))

if __name__ == "__main__":
    errors = validate(load("data/deep/vol04_witness_bibliography_v02.json"),
                      load("data/deep/vol04_split_proposals_v01.json"))
    for error in errors: print("FAIL", error)
    if not errors: print("PASS five composite parents / ten provisional child identities; PUBLIC BLOCKED")
    raise SystemExit(bool(errors))
