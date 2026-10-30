#!/usr/bin/env python3
"""V1.20 bibliographic witness integrity; fail closed."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text(encoding="utf-8"))
r=load("data/deep/vol03_wycliffe_hus_primary_witness_audit_v120.json")
p=load("data/overview/volumes_and_people_v01.json")
d=load("data/overview/events_documents_v01.json")
persons={x["id"] for x in p["people"]}
docs={x["id"] for x in d["documents"]}
assert r["release_gate"]=={"approved":False,"can_ship":False}
ids=[x["id"] for x in r["records"]]
assert len(ids)==len(set(ids))==6
for x in r["records"]:
 assert x["person_id"] in persons
 assert x["document_id"] is None or x["document_id"] in docs
 assert x["bibliographic_source"].startswith("https://")
 assert x["original_manuscript_read"] is False
 assert x["edition_full_text_read"] is False
assert next(x for x in r["records"] if x["id"]=="WIT-V120-HUS-LETTER-1415-06-30")["date_certainty"]=="uncertain"
print("PASS: V1.20 witness IDs, metadata, and no-publication gates")
