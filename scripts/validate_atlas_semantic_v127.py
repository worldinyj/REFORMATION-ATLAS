#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
r=json.loads((R/"data/deep/atlas_v127_semantic_evidence_crosswalk.json").read_text(encoding="utf8"))
calvin=json.loads((R/"data/deep/vol04_calvin_v01.json").read_text(encoding="utf8"))
luther=json.loads((R/"data/deep/vol04_luther_v01.json").read_text(encoding="utf8"))
assert r["publication_gate"]=={"approved":False,"can_ship":False}
s={x["id"] for x in r["sources"]}
assert len(s)==3
for c in r["claims"]:
 assert set(c["source_ids"])<=s
cids={x["id"] for x in calvin["claims"]}
lids={x["id"] for x in luther["claims"]}
assert r["claims"][0]["legacy_claim_id"] in cids
assert r["claims"][1]["legacy_claim_id"] in lids
assert r["cross_volume_flags"][0]["verdict"]=="REJECT_AS_EVIDENCE"
assert "AHISTO" not in r["claims"][0]["source_ids"]
assert {x["year"] for x in r["edition_leads"]}=={1536,1539,1543,1550,1559}
print("PASS: V1.27 topical evidence replacement, edition years, non-public gate")
