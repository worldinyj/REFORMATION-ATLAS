#!/usr/bin/env python3
"""V3.77 source-preserving witness correction audit.

Run: python3 research/tools/validate_v377_witness_patch.py
Reads only JSON in the repository; never modifies source or corrected files.
"""
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / "research/data/V3_61_FOUR_QUESTIONS_WITNESS_CROSSWALK_DRAFT.json"
NEW = ROOT / "research/data/V3_77_FOUR_QUESTIONS_WITNESS_CROSSWALK_CORRECTED_DRAFT.json"
EXPECTED_SOURCE_BLOB_SHA = "d277b723d35db913d2e58e983274dc047ec2b87b"

def fail(message):
    raise AssertionError(message)

def variants(data):
    items = data["witness_variant_examples"]
    ids = [x["id"] for x in items]
    assert len(ids) == len(set(ids)), "Duplicate witness ID"
    return {x["id"]: x for x in items}

def main():
    old = json.loads(OLD.read_text(encoding="utf-8"))
    new = json.loads(NEW.read_text(encoding="utf-8"))
    a, b = variants(old), variants(new)
    assert set(a) == set(b)
    assert old["version"] == "V3.61"
    assert new["release"]["can_ship"] is False
    assert new["correction_provenance"]["source_blob_sha"] == EXPECTED_SOURCE_BLOB_SHA
    assert a["V361-V01"]["forms"]["A"] == "stellet"
    assert b["V361-V01"]["forms"] == {"A":"für stellet","B":"fürstellt","C":"fürstellt","D":"fürstellt"}
    assert a["V361-V04"]["forms"]["B"] == "Erlüterung ..."
    assert b["V361-V04"]["forms"]["B"] is None
    assert b["V361-V04"]["forms"]["A"].startswith("Erlüterung der Witembergischen Articklen")
    assert "facsimile-verified" in b["V361-V04"]["forms"]["A"]
    assert b["V361-V04"]["assigned_to_question_unit"] is None
    # Compare against source after reconstructing only the approved replacements.
    expected = deepcopy(old)
    v = variants(expected)
    v["V361-V01"]["forms"]["A"] = "für stellet"
    v["V361-V04"]["forms"] = deepcopy(b["V361-V04"]["forms"])
    v["V361-V04"]["status"] = b["V361-V04"]["status"]
    for field in ("version","as_of","branch","parent"):
        expected[field] = new[field]
    expected["release"]["status"] = new["release"]["status"]
    expected["correction_provenance"] = deepcopy(new["correction_provenance"])
    assert expected == new, "Unapproved alteration of inherited research fields"
    assert len(old["question_units"]) == len(new["question_units"]) == 4
    assert old["question_units"] == new["question_units"], "Question units changed"
    for claim in new["question_units"]:
        assert claim["can_publish"] is False
    print("PASS: two witness variants corrected; Q1-Q4 and other fields preserved")
    print("PASS: source blob SHA recorded; publication gated; no file modified")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
