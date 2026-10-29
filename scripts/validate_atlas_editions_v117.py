#!/usr/bin/env python3
"""V1.17 fail-closed edition/reference checks."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text(encoding="utf-8"))
d=load("data/contracts/atlas_person_work_edition_crosswalk_v117.json")
p=load("data/overview/volumes_and_people_v01.json")
v3=load("data/vol03_document_witnesses.json")
calvin=load("data/deep/vol04_calvin_v01.json")
assert d["publication_gate"]=={"approved":False,"can_ship":False}
person_ids={x["id"] for x in p["people"]}
assert d["people"][0]["id"]==calvin["person_id"] and d["people"][0]["id"] in person_ids
work_ids={x["id"] for x in d["works"]}
edition_ids={x["id"] for x in d["editions"]}
assert len(edition_ids)==len(d["editions"])
claims={x["id"] for x in calvin["claims"]}
for e in d["editions"]:
    assert e["work_id"] in work_ids and set(e["claim_ids"])<=claims
    assert e["direct_copy_collated"] is False
assert {(e["year"],e["language"]) for e in d["editions"]}=={(1536,"la"),(1541,"fr"),(1559,"la"),(1560,"fr")}
originals={x["id"]:x for x in v3["objects"]}
for record in d["vol03_document_map"]:
    assert record["id"] in originals
    assert record["kind"]==originals[record["id"]]["kind"]
    if "based_on_id" in record:
        assert record["based_on_id"]==originals[record["id"]]["based_on_id"]
print("PASS V1.17: 4 separate Calvin editions and 8 VOL03 witness objects; not public")
