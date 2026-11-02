#!/usr/bin/env python3
"""V216 claim/source scope ledger QA, NOT historical truth/expert approval."""
from pathlib import Path
from collections import Counter
import json
R=Path(__file__).resolve().parents[1]
def rd(p):return json.loads((R/p).read_text(encoding="utf-8"))
x=rd("data/deep/atlas_v216_scene_claim_evidence_ledger.json")
v15=rd("data/deep/atlas_v215_historical_exploration_journeys.json")
v14=rd("data/deep/atlas_v214_geography_and_witness_provenance.json")
assert x["version"]=="2.16" and x["lineage"]["parent_commit"]=="b9c4a4964fc074b5ba7be01e088804a45fdec9e5"
assert all(flag is False for flag in x["publication_gate"].values())
m=x["metrics"]
assert (m["reader_routes"],m["stages_reviewed"],m["one_narrow_claim_per_stage"],m["high_priority_source_dossiers"],m["registered_sources"],m["source_gap_queues"])==(5,30,30,16,20,6)
assert m["original_witness_folios_collated"]==m["human_history_claims_approved"]==m["publication_approvals"]==m["webapp_changes"]==0
src={s["id"]:s for s in x["source_registry"]}
stages={s["id"]:s for s in v15["stages"]}
v14_events={e["id"] for e in v14["event_links"]}
assert len(src)==20
for s in src.values():
  assert s["url"].startswith("https://")
  assert s["locator"] and s["scope"] and s["source_kind"]
  assert s["original_folio_image_collated"] is False
  assert s["original_translation_copyright_cleared"] is False
  assert s["expert_approved"] is False and s["can_publish"] is False
claims={c["id"]:c for c in x["scene_claims"]}
assert len(claims)==30 and len(stages)==30
assert {c["stage_id"] for c in claims.values()}==set(stages)
for c in claims.values():
  stage=stages[c["stage_id"]]
  assert c["id"] and c["claim_ko"] and c["claim_limitations_ko"]
  assert (c["v211_sentence_id"],c["v212_essay_id"],c["v214_event_id"])==(stage["v211_reader_sentence_id"],stage["v212_context_essay_id"],stage["v214_event_id"])
  assert c["inspection_status"] in x["methodology"]["grades"]
  assert c["evidence_links"]
  for link in c["evidence_links"]:
    assert link["source_id"] in src
    assert link["locator"] and link["relevance"]
  assert c["claim_text_not_vetted_by_historian"] is True
  assert c["original_folio_image_inspected"] is False
  assert c["public_claim_approved"] is False and c["can_publish"] is False
assert dict(Counter(c["inspection_status"] for c in claims.values()))==m["source_adequacy_levels"]
dossiers={d["id"]:d for d in x["priority_dossiers"]}
assert len(dossiers)==16
assert len({d["stage_id"] for d in dossiers.values()})==16
for d in dossiers.values():
  assert d["stage_id"] in stages and d["linked_claim_id"] in claims
  assert claims[d["linked_claim_id"]]["stage_id"]==d["stage_id"]
  assert d["source_ids"] and set(d["source_ids"])<=set(src)
  assert d["focused_claim_ko"] and d["what_checked_ko"] and d["recommended_editorial_action_ko"]
  assert d["priority"]=="P1"
  assert d["primary_witness_image_read"] is False and d["exact_original_language_passage_collated"] is False
  assert d["scholarly_signoff"] is False and d["can_publish"] is False
for q in x["unresolved_evidence_work"]:
  assert q["source_ids"] and set(q["source_ids"])<=set(src)
  assert q["priority"] in ("P0","P1") and q["action_ko"]
assert len(x["training_warnings"])>=6
print("PASS V216: 30 stage-level provisional claims, 16 source dossiers, 20 sourced records, 6 witness-collation work queues; NO HISTORICAL OR PUBLIC APPROVAL")
