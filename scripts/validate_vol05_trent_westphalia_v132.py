#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf8"))
v=load("data/deep/atlas_v132_trent_westphalia_review.json")
t=load("data/deep/vol05_trent_catholic_reform_registry_v01.json")
l=load("data/deep/vol05_trent_latin_witness_alignment_v01.json")
w=load("data/deep/vol05_war_westphalia_research_v01.json")
assert v["publication_gate"]=={"approved":False,"can_ship":False}
assert len(v["sessions"])==len(t["sessions"])==8
assert len(v["latin_anchors"])==len(l["anchors"])==4
assert len(v["treaties"])==len(w["treaty_instruments"])==3
assert v["counts"]["trent_sources"]==len(t["source_records"])==11
assert v["counts"]["latin_sources"]==len(l["source_records"])==10
assert v["counts"]["westphalia_sources"]==len(w["source_records"])==11
assert [p["id"] for p in v["cross_volume_people"]]==["OV-P-021","OV-P-022"]
assert all(not p["not_verified_against_print"] is False for p in v["latin_anchors"])
print("PASS V1.32: 8 sessions / 4 anchors / 3 treaties / no publication")
