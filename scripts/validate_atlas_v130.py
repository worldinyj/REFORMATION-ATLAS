#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((r/p).read_text(encoding="utf8"))
v=read("data/deep/atlas_v130_remaining_claim_review.json")
p=read("data/contracts/atlas_v130_cross_volume_private_manifest.json")
assert len(v["remaining_claims"])==20
assert sum(c["person"]=="luther" for c in v["remaining_claims"])==10
assert sum(c["person"]=="calvin" for c in v["remaining_claims"])==10
assert all(c["source_scope_match"] and not c["semantic_content_verified"] for c in v["remaining_claims"])
assert v["publication_gate"]=={"approved":False,"can_ship":False}
assert p["publication_gate"]=={"approved":False,"can_ship":False}
assert all(not x["public"] for x in p["volumes"])
print("PASS V1.30: 20 source-ID checks and fail-closed cross-volume manifest")
