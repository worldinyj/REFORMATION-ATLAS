#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((r/p).read_text(encoding="utf8"))
d=load("data/deep/atlas_v133_catholic_renewal_crosswalk.json")
src=load("data/deep/vol05_trent_catholic_reform_registry_v01.json")
people=load("data/overview/volumes_and_people_v01.json")
assert d["publication_gate"]=={"approved":False,"can_ship":False}
ids={x["id"] for x in people["people"]}
keys={x["research_source_key"] for x in src["source_records"]}
phases={x["key"] for x in src["phase_records"]}
assert {x["id"] for x in d["persons"]}=={"OV-P-021","OV-P-022"}<=ids
assert all(set(x["source_keys"])<=keys for x in d["persons"])
assert all(x["key"] in phases for x in d["council_periods"])
assert all(x["primary_text_collated"] is False for x in d["persons"])
print("PASS V1.33: persons, source keys, council phases and closed gate")
