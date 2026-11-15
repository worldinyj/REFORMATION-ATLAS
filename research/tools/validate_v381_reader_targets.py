#!/usr/bin/env python3
"""REFORMATION-ATLAS V3.81 research-only crosswalk validation.

Usage: python3 research/tools/validate_v381_reader_targets.py
Never edits content, readers, app sources, or research records.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP_PATH = ROOT / "research/data/V3_81_CLAIM_TO_READER_TARGET_CROSSWALK_DRAFT.json"

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def blob_sha(path):
    raw = (ROOT / path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def main():
    data = load("research/data/V3_81_CLAIM_TO_READER_TARGET_CROSSWALK_DRAFT.json")
    assert data["release"]["can_ship"] is False
    assert data["release"]["main_edited"] is False
    assert data["release"]["essays_513_edited"] is False
    assert data["release"]["webapp_modified"] is False
    manifest = load("integrations/medium-atlas-v308/manifest.json")
    catalogue = load("data/deep/atlas_v307_remaining_overview_medium_readers.json")["catalogue"]
    overview = load("data/contracts/atlas_v304_overview_medium_reading_crosswalk.json")["entries"]
    assert manifest["expectedCounts"]["readers"] == 513
    assert manifest["actualAIStudioSourceAvailable"] is False
    assert len(catalogue) == len({x["id"] for x in catalogue}) == 513
    assert len(overview) == len({x["overview_id"] for x in overview}) == 97
    assert len(data["actual_readers"]) == 5
    for anchor in data["actual_readers"]:
        f = anchor["source_file"]
        assert blob_sha(f) == anchor["source_git_blob_sha"], f"file drift: {f}"
        doc = load(f)
        chapter = doc["chapters"][anchor["source_chapter_index_in_file"]]
        assert chapter["id"] == anchor["reader_id"]
        section = chapter["sections"][anchor["section_index"]]
        assert section["heading"] == anchor["heading"]
        assert section["body"].startswith(anchor["body_excerpt"])
        catalogue_entry = next(x for x in catalogue if x["id"] == anchor["reader_id"])
        assert catalogue_entry["dataset"] == f
        assert catalogue_entry["chapter_index"] == anchor["catalogue_chapter_index"]
    original = load("research/data/V3_80_BASEL_PUBLICATION_READINESS_AUDIT.json")
    prior_claim_ids = {x["claim_id"] for x in original["claims"]}
    claims = data["claims"]
    assert len(claims) == len(prior_claim_ids) == 16
    assert {x["claim_id"] for x in claims} == prior_claim_ids
    for c in claims:
        assert c["publication"] == "BLOCKED"
        assert c["exact_paragraph_id"] is None
        assert c["confirmed_existing_sentence_match"] is False
        if c["reader_id"] is not None:
            assert c["reader_id"] in {a["reader_id"] for a in data["actual_readers"]}
            assert c["source_target"]["chapter_id"] == c["reader_id"]
    false_friends = data["forbidden_false_friend_links"]
    assert {"EVENT-BASEL_SETTLEMENT1433_1436",
            "DOCUMENT-BASEL_COMPACTATA",
            "DOCUMENT-FORMULA_CONCORD",
            "DOCUMENT-BOOK_CONCORD"} == {x["existing_reader_id"] if "existing_reader_id" in x else x["existing_id"] for x in false_friends}
    forbidden = {"EVENT-BASEL_SETTLEMENT1433_1436",
                 "DOCUMENT-BASEL_COMPACTATA",
                 "DOCUMENT-FORMULA_CONCORD",
                 "DOCUMENT-BOOK_CONCORD"}
    assert not any(c["reader_id"] in forbidden for c in claims)
    assert data["safety"]["strict_export"] == []
    assert data["missing_entry"]["direct_event_or_document_in_513_catalogue"] is False
    print("PASS V3.81: 513 catalogue IDs, 97 overview entries, 5 pinned reader anchors")
    print("PASS V3.81: 16 claim ID mappings, four false-friend exclusions, public export blocked")

if __name__ == "__main__":
    main()
