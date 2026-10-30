#!/usr/bin/env python3
"""V1.25 research integrity gate, fail closed and read only."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(name):
 return json.loads((R/("data/deep/vol03_v125_"+name+".json")).read_text(encoding="utf8"))
d={n:load(n) for n in ("source_registry","claim_registry","witness_registry","passage_plan","constance_textual_audit","bibliographic_discrepancies","editorial_decisions","publication_gate_matrix")}
assert all(x["publication_gate"]=={"approved":False,"can_ship":False} for x in d.values())
sources={x["id"] for x in d["source_registry"]["sources"]}
assert len(sources)==14
claims=d["claim_registry"]["claims"]
assert len(claims)==20 and len({x["id"] for x in claims})==20
assert all(set(x["source_ids"])<=sources and x["public_approved"] is False for x in claims)
for witness in d["witness_registry"]["witnesses"]:
 assert set(witness["source_ids"])<=sources and witness["direct_folio_verified"] is False
for w in d["witness_registry"]["witnesses"][:2]:
 assert "Genesis" in w["excludes"] and "Exodus" in w["excludes"]
assert len(d["passage_plan"]["passages"])==5
assert all(p["collated"] is False for p in d["passage_plan"]["passages"])
assert len(d["constance_textual_audit"]["panels"])==3
assert all(set(p["source_ids"])<=sources for p in d["constance_textual_audit"]["panels"])
assert len(d["bibliographic_discrepancies"]["discrepancies"])==4
assert len(d["editorial_decisions"]["decisions"])==6
assert d["publication_gate_matrix"]["gates"]["main_merge"]=="blocked"
print("PASS: V1.25 source/provenance, manuscripts, passages, Hus panels and publication gates")
