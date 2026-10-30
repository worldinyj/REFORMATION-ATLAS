#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/"data/contracts/atlas_v138_readable_confessions.json").read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert {x["id"] for x in d["topics"]}=={"JUSTIFICATION","EUCHARIST","SAINTS_IMAGES"}
assert all(len(x["terms"])==3 for x in d["topics"])
assert len(d["sources"])==6
assert all(x["historical_original_collated"] is False for x in d["sources"])
assert d["app_hand_off"]["public_visible"] is False
print("PASS: V1.38 structure, rights and publication hold")
