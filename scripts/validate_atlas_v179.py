import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text())
d=load("data/contracts/atlas_v179_ten_reader_claim_evidence.json")
readers=load("data/deep/atlas_v178_ten_readers_standardized.json")
evidence={x["id"] for x in load("data/contracts/atlas_v163_source_evidence_cards.json")["cards"]}
assert len(d["claims"])==len(readers["chapters"])==10
assert {x["reader_key"] for x in d["claims"]}=={x["key"] for x in readers["chapters"]}
assert not d["publication_gate"]["can_ship"]
for x in d["claims"]:
 assert x["reader_source_id"] in {r["source_id"] for r in readers["chapters"]}
 assert x["claim"] and x["unverified"] and x["urls"]
 assert all(url.startswith("https://") for url in x["urls"])
 assert set(x["linked_evidence_cards"])<=evidence
 assert x["original_folio_checked"] is False and x["can_publish"] is False and x["human_review"]=="PENDING"
print("PASS: 10 source-classified claim links, original check and release gates closed")
