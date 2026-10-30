#!/usr/bin/env python3
"""V1.19 document/witness links, fail-closed; no file writes."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf8"))
d=load("data/contracts/atlas_person_document_witness_crosswalk_v119.json")
p=load(d["provenance"]["people"])
o=load(d["provenance"]["documents_events"])
w=load(d["provenance"]["witnesses"])
l=load(d["provenance"]["luther"])
c=load(d["provenance"]["calvin"])
ed=load(d["provenance"]["editions"])
people={x["id"] for x in p["people"]}
documents={x["id"]:x for x in o["documents"]}
events={x["id"] for x in o["events"]}
witnesses={x["id"] for x in w["objects"]}
editions={x["id"] for x in ed["editions"]}
claims={x["id"] for x in l["claims"]+c["claims"]}
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert len(d["links"])==5
for x in d["links"]:
 assert x["person_id"] in people and x["document_id"] in documents
 assert documents[x["document_id"]]["source_ids"]
 if x.get("event_id"): assert x["event_id"] in events
 if x.get("claim_id"): assert x["claim_id"] in claims
 assert set(x.get("witness_ids",[]))<=witnesses
 assert set(x.get("edition_ids",[]))<=editions
hus=next(x for x in d["links"] if x["person_id"]=="OV-P-010")
assert hus["relation"]=="later_movement_document"
assert next(x for x in d["links"] if x["person_id"]=="OV-P-016")["document_id"]=="OV-D-012"
print("PASS V1.19: five nonpublic links and resolved document/claim/witness/edition IDs")
