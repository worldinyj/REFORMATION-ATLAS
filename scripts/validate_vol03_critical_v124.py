#!/usr/bin/env python3
"""V1.24 fail-closed cross-document research QA. Standard library only."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE="data/deep/vol03_v124_"
def load(s):
    return json.loads((ROOT/(BASE+s+".json")).read_text(encoding="utf8"))
catalog=load("source_and_manuscript_catalog")
passages=load("passage_witness_matrix")
hus=load("hus_proceedings_crosswalk")
claims=load("claim_decision_register")
for x in (catalog,passages,hus,claims):
    assert x["publication_gate"]=={"approved":False,"can_ship":False}
source_ids={s["id"] for s in catalog["sources"]}
assert len(source_ids)==len(catalog["sources"])==8
manuscripts={m["id"]:m for m in catalog["records"]}
assert len(manuscripts)==4
for row in manuscripts.values():
    assert row["source_id"] in source_ids
    assert row["manuscript_collated"] is False
for id in ("MS-E617","MS-E618"):
    assert manuscripts[id]["genesis_present"] is False
    assert manuscripts[id]["exodus_present"] is False
assert manuscripts["MS-MAN-E89"]["version"]=="MIXED_EV_LV"
assert len(passages["passages"])==3
for p in passages["passages"]:
    assert p["verified_folio"] is None
    assert p["passage"] and p["needed"]
assert len(hus["events"])==3
assert hus["events"][0]["genre"]=="hearings"
assert hus["events"][1]["genre"]=="official_sentence"
assert hus["events"][2]["genre"]=="edited_eyewitness_narrative"
for e in hus["events"]:
    assert set(e["source_ids"])<=source_ids
assert len(claims["items"])==8
for claim in claims["items"]:
    assert claim["sources"] and set(claim["sources"])<=source_ids
    assert claim["claim_status"] in ("supported_from_catalog","supported_from_summary","supported_from_secondary","supported_from_transcription","rejected")
assert {x["id"] for x in claims["items"] if x["claim_status"]=="rejected"}=={"V124-C07","V124-C08"}
print("PASS: V1.24 8 sources, 4 physical/edition witness records, 3 passages, 3 council stages, 8 claims")
