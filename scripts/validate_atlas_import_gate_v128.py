#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
get=lambda p:json.loads((root/p).read_text(encoding="utf8"))
a=get("data/deep/atlas_v128_vol04_claim_source_audit.json")
l=get("data/deep/vol04_luther_v01.json")
c=get("data/deep/vol04_calvin_v01.json")
assert a["publication_gate"]=={"approved":False,"can_ship":False}
assert len(a["records"])==32
assert all(x["all_ids_resolve"] and not x["publication_approved"] for x in a["records"])
for dataset,person in ((l,"luther"),(c,"calvin")):
    source_ids={s["id"] for s in dataset["sources"]}
    claim_ids={x["id"] for x in dataset["claims"]}
    relevant=[x for x in a["records"] if x["person"]==person]
    assert len(relevant)==16
    assert {x["claim_id"] for x in relevant}==claim_ids
    assert all(set(x["source_ids"])<=source_ids for x in relevant)
print("PASS: 32 claims / 0 unresolved refs / all publication gates closed")
