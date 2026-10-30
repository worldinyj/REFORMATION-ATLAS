#!/usr/bin/env python3
"""V1.29 semantic-review linkage: validates audit structure, not historical truth."""
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
get=lambda p:json.loads((r/p).read_text(encoding="utf8"))
d=get("data/deep/atlas_v129_vol04_semantic_reviews.json")
l=get("data/deep/vol04_luther_v01.json")
c=get("data/deep/vol04_calvin_v01.json")
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert d["reviewed_count"]==len(d["cases"])==12
assert len({x["id"] for x in d["cases"]})==12
ids={x["id"] for x in l["claims"]+c["claims"]}
assert all(x["claim_id"] in ids for x in d["cases"])
assert all(x["url"].startswith("https://") and x["publication_approved"] is False for x in d["cases"])
assert all(x["original_primary_text_collated"] is False for x in d["cases"])
assert sum(x["claim_id"].startswith("CLM-V04-L-") for x in d["cases"])==6
assert sum(x["claim_id"].startswith("CLM-V04-CA-") for x in d["cases"])==6
print("PASS V1.29: twelve claim-to-source review records, no public release")
