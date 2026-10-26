#!/usr/bin/env python3
"""Mutation regression checks for the research-only VOL-04 event registry."""
from __future__ import annotations
import copy
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/"scripts"))
from validate_vol04_event_narratives_v01 import check, load  # noqa: E402

def rejects(baseline, fn, label):
    modified = copy.deepcopy(baseline)
    fn(modified)
    try:
        check(modified)
    except (ValueError, KeyError, IndexError, TypeError):
        return
    raise AssertionError("unsafe mutation accepted: " + label)

def main():
    data = load("data/deep/vol04_event_narrative_registry_v01.json")
    assert check(data)["episodes"] == 5
    bad = [
        ("publication gate", lambda d: d["release"].__setitem__("approved",True)),
        ("fake new ID", lambda d: d.__setitem__("canonical_ids_minted",1)),
        ("web mutation", lambda d: d.__setitem__("web_app_modified",True)),
        ("case publication", lambda d: d["episodes"][0].__setitem__("publication_approved",True)),
        ("case approval", lambda d: d["episodes"][0].__setitem__("approval",True)),
        ("collation fabrication", lambda d: d["episodes"][0].__setitem__("source_text_collated",True)),
        ("wrong year", lambda d: d["episodes"][1].__setitem__("year",1530)),
        ("wrong canonical ID", lambda d: d["episodes"][1].__setitem__("existing_event_id","OV-E-019")),
        ("forged candidate route", lambda d: d["episodes"][3].__setitem__("route_policy","EXISTING_OVERVIEW_ID_REFERENCE_ONLY")),
        ("duplicate ID", lambda d: d["episodes"][4].__setitem__("episode_id","EP-V04-1530-01")),
        ("orphan claim", lambda d: d["episodes"][0]["claim_ids"].append("CLM-UNKNOWN")),
        ("lost source provenance", lambda d: d["episodes"][0]["source_ids"].pop()),
        ("false relationship", lambda d: d["episodes"][0]["linked_deep_event_ids"].append("DEEP-V04-E-008")),
        ("invented person", lambda d: d["episodes"][4]["related_person_ids"].append("OV-P-999")),
        ("unverified media rights", lambda d: d["episodes"][0].__setitem__("media_rights_approved",True)),
        ("removed hold", lambda d: d["episodes"][3].__setitem__("critical_hold","")),
        ("untrusted URL", lambda d: d["episodes"][2]["extra_source_urls"].append("http://example.org")),
    ]
    for name, fn in bad:
        rejects(data, fn, name)
    print(f"PASS: {len(bad)} unsafe event alterations rejected; five narrative episodes remain drafts")

if __name__ == "__main__":
    main()
