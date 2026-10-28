#!/usr/bin/env python3
"""Negative-path checks: never silently publish or reassign research episodes."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_vol04_05_next_events_v01 import read, validate

def reject(original, name, mutate):
    modified=copy.deepcopy(original)
    mutate(modified)
    try:
        validate(modified)
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise AssertionError("unsafe research change accepted: " + name)

def main():
    base=read("data/deep/vol04_05_next_events_registry_v01.json")
    assert validate(base)["chapters"]==4
    tests=[
        ("public approval",lambda x:x["publication_gate"].__setitem__("approved",True)),
        ("human approval",lambda x:x["publication_gate"].__setitem__("human_approval",True)),
        ("rights approval",lambda x:x["publication_gate"].__setitem__("rights_approval",True)),
        ("canonical issue",lambda x:x.__setitem__("canonical_ids_issued",1)),
        ("web change",lambda x:x.__setitem__("ai_studio_unchanged",False)),
        ("claimed full collation",lambda x:x.__setitem__("original_text_collated",True)),
        ("wrong volume 1555",lambda x:x["cases"][3].__setitem__("volume_id","VOL-04")),
        ("wrong event 1555",lambda x:x["cases"][3].__setitem__("canonical_event_id","OV-E-019")),
        ("fake event Zurich",lambda x:x["cases"][1].__setitem__("canonical_event_id","OV-E-017")),
        ("wrong year",lambda x:x["cases"][0].__setitem__("year_start",1520)),
        ("unauthorized release",lambda x:x["cases"][2].__setitem__("release_approved",True)),
        ("media permission fabricated",lambda x:x["cases"][0].__setitem__("media_reuse_approved",True)),
        ("source gone",lambda x:x["cases"][3]["source_urls"].clear()),
        ("insecure url",lambda x:x["cases"][2]["source_urls"].append("http://example.org")),
        ("unknown canonical person",lambda x:x["cases"][2]["existing_people"].append("OV-P-999")),
        ("Prayer Book link gone",lambda x:x["cases"][2]["existing_documents"].clear()),
        ("unknown claim",lambda x:x["cases"][0]["claim_ids"].append("CLM-WRONG")),
        ("uncertainty erased",lambda x:x["cases"][0].__setitem__("evidence_limit_ko","")),
    ]
    for name, mutate in tests:
        reject(base, name, mutate)
    print(f"PASS: {len(tests)} unsafe research mutations rejected; public=0")

if __name__=="__main__":
    main()
