#!/usr/bin/env python3
"""Read-only V3.80 publication-readiness QA for REFORMATION-ATLAS.

Run at repository root or any directory:
    python3 research/tools/validate_v380_readiness.py
Requires only Python 3 standard library. It never edits any input.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research/data/V3_80_BASEL_PUBLICATION_READINESS_AUDIT.json"
PARENT = ROOT / "research/data/V3_76_BASEL_CLAIM_EVIDENCE_MATRIX_DRAFT.json"
LEGACY = ROOT / "research/data/V3_61_FOUR_QUESTIONS_WITNESS_CROSSWALK_DRAFT.json"
CORRECTED = ROOT / "research/data/V3_77_FOUR_QUESTIONS_WITNESS_CROSSWALK_CORRECTED_DRAFT.json"
EXPECTED_PARENT_BLOB = "2f19d004548c52590f200da50177a5c0e4c0c8b0"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def by_id(rows):
    ids = [x["id"] for x in rows]
    assert len(ids) == len(set(ids)), "Duplicate witness IDs"
    return {x["id"]: x for x in rows}

def main():
    audit, parent, legacy, corrected = map(load, (DATA, PARENT, LEGACY, CORRECTED))
    claims = audit["claims"]
    claim_ids = [x["claim_id"] for x in claims]
    source_ids = parent["sources"].keys()
    levels = audit["classifications"]
    assert audit["lineage"]["input_matrix_git_blob_sha"] == EXPECTED_PARENT_BLOB
    assert len(claims) == len(parent["claims"]) == 16
    assert len(set(claim_ids)) == 16
    assert set(claim_ids) == {x["claim_id"] for x in parent["claims"]}
    assert len(parent["sources"]) == 10
    assert all(set(x["source_ids"]).issubset(source_ids) for x in claims)
    level_ids = [id for ids in levels.values() for id in ids]
    assert len(level_ids) == 16 and set(level_ids) == set(claim_ids)
    for item in claims:
        assert item["evidence_level"] in levels
        assert item["claim_id"] in levels[item["evidence_level"]]
        assert item["may_publish_as_is"] is False
        assert item["may_update_513_essays"] is False
        assert item["status"] == "EVIDENCE_AUDITED_NOT_RELEASED"
    assert audit["release"]["can_ship"] is False
    assert audit["release"]["legacy_513_edited"] is False
    assert audit["release"]["ai_studio_modified"] is False
    a, b = by_id(legacy["witness_variant_examples"]), by_id(corrected["witness_variant_examples"])
    assert a["V361-V01"]["forms"]["A"] == "stellet"
    assert b["V361-V01"]["forms"]["A"] == "für stellet"
    assert a["V361-V04"]["forms"]["B"] == "Erlüterung ..."
    assert b["V361-V04"]["forms"]["B"] is None
    assert set(x["id"] for x in audit["duplicate_testimony_families"]) == {
        "BRIEFFER_LETTER_1536_07_21",
        "CAPITO_LETTER_1536_07_20",
        "ERLAUTERUNG_BASLE_STRASBOURG_1536",
        "BUCER_VADIAN_1536_07_23",
    }
    assert audit["qa"]["page219_to226_sentence_corroboration"] is False
    assert all(scene["essay_locator"] is None for scene in audit["publication_items"])
    print("PASS V3.80: 16 claims / 10 sources; 6+5+5 classifications; 4 testimony families")
    print("PASS: legacy variants excluded, release blocked, essay locations unresolved")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, KeyError, TypeError, ValueError, OSError) as exc:
        print("FAIL V3.80:", exc, file=sys.stderr)
        sys.exit(1)
