#!/usr/bin/env python3
"""Validate V1.15 compatibility contract and representative legacy data (no modifications)."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
load=lambda p: json.loads((ROOT/p).read_text(encoding="utf-8"))
c=load("data/contracts/atlas_cross_volume_compat_v115.json")
assert c["migration_mode"]=="read_only_projection_no_source_mutation"
assert c["release_gate"]["approved"] is False and c["release_gate"]["can_ship"] is False
assert c["publication_policy"]["default_visible"] is False
assert len(c["projections"])>=3
for x in c["projections"]:
    assert (ROOT/x["source"]).is_file()
    d=load(x["source"])
    if x["collection"]=="content_block":
        records=[d["content_block"]]
    else:
        records=d[x["collection"]]
    assert records, x["source"]
    for r in records:
        assert r["id"]
        assert all(s in r for s in ["id"])
        assert x["map"]["id"] in r
        assert x["map"]["source_ids"] in r
        assert isinstance(r[x["map"]["source_ids"]],list)
        if "public_visible" in x["map"]:
            assert r[x["map"]["public_visible"]] is False
        if "default_volume_ids" in x:
            assert all(v.startswith("VOL-") for v in x["default_volume_ids"])
d=load("data/deep/vol05_education_map_timeline_v114.json")
assert d["publication_gate"]["can_ship"] is False
assert len(d["routes"])==2
e={x["id"]:x for x in d["events"]}
assert e["EV-PAD-PERMIT-1652"]["type"]=="authorization"
assert e["EV-PAD-ARRIVAL-1658"]["type"]=="movement_and_teaching_start"
print("PASS: V1.15 read-only compatibility contract, sample projection sources and release gates")
