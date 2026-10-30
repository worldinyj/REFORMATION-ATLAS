#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/"data/deep/atlas_v135_trent_sessions_teresa_editions.json").read_text(encoding="utf8"))
assert data["publication_gate"]=={"approved":False,"can_ship":False}
assert len(data["sessions"])==7
assert len({x["session"] for x in data["sessions"]})==7
assert all(x["latin_original_collated"] is False for x in data["sessions"])
assert data["teresa"]["person_id"]=="OV-P-022"
assert data["teresa"]["manuscript"]["facsimile_collated"] is False
assert data["teresa"]["edition_1588"]["city"]=="Salamanca"
print("PASS V1.35: closed gate, seven sessions, Teresa provenance")
