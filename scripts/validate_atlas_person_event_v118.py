#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding="utf-8"))
d=read("data/contracts/atlas_person_event_crosswalk_v118.json")
p=read("data/overview/volumes_and_people_v01.json")
e=read("data/overview/events_documents_v01.json")
l=read("data/deep/vol04_luther_v01.json")
c=read("data/deep/vol04_calvin_v01.json")
people={x["id"]:x for x in p["people"]}
events={x["id"]:x for x in e["events"]}
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert len(d["people"])==4 and len(d["relations"])==6
for x in d["people"]:
 assert x["id"] in people and x["volume_id"] in people[x["id"]]["volume_ids"]
for x in d["relations"]:
 assert x["person_id"] in people and x["event_id"] in events
assert l["parent_person_id"]=="OV-P-013"
assert c["person_id"]=="OV-P-016"
assert all(x["id"] != "OV-P-009" or x["volume_id"]=="VOL-03" for x in d["people"])
print("PASS: V1.18 references and private publication gate")
