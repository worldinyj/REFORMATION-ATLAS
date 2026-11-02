#!/usr/bin/env python3
"""Structural QA, not original manuscript collation or human scholarship approval."""
import json
from pathlib import Path
from datetime import date
root=Path(__file__).resolve().parents[1]
def rd(p): return json.loads((root/p).read_text(encoding="utf-8"))
x=rd("data/deep/atlas_v212_historical_connections_and_comparisons.json")
old=rd("data/deep/atlas_v211_ten_reader_hus_augsburg_revision.json")
assert x["version"]=="2.12" and x["lineage"]["parent_commit"]=="a667c1e9b972d6a8d88b8d810fa43597706ed9e0"
assert all(v is False for v in x["publication_gate"].values())
m=x["metrics"]
assert (m["reader_chapters"],m["new_contextual_essays"],m["typed_relationships"],m["chronology_entries"],m["comparison_topics"],m["source_records"],m["visual_rights_candidates"])==(10,10,14,19,4,14,2)
assert m["original_folio_collations"]==m["expert_approvals"]==m["public_items"]==0
readers={c["key"] for c in old["chapters"]}
src={s["id"]:s for s in x["source_register"]}
assert len(readers)==10 and len(src)==14
for s in src.values():
  assert s["url"].startswith("https://")
  assert s["original_witness_collated"] is False and s["image_rights_approved"] is False
def source_ok(y):
  assert y["source_ids"] and set(y["source_ids"])<=set(src)
essays={e["reader_key"]:e for e in x["reader_connections"]}
assert len(essays)==10 and set(essays)==readers
for e in essays.values():
  source_ok(e)
  assert len(e["body_ko"])>240 and e["title_ko"] and e["reader_question_ko"]
  assert all(i in readers for i in e["linked_reader_keys"])
  assert e["status"]=="RESEARCH_DRAFT_NOT_SOURCE_CERTIFIED"
  assert e["original_folio_collated"] is False and e["expert_approved"] is False and e["can_publish"] is False
assert len(x["historical_relations"])==14
for r in x["historical_relations"]:
  source_ok(r)
  assert r["from_reader_key"] in readers and r["to_reader_key"] in readers
  assert r["from_reader_key"]!=r["to_reader_key"]
  assert r["relationship_kind"] and r["explanation_ko"] and r["overclaim_guard_ko"]
  assert r["human_scholar_review"]=="PENDING" and r["original_witness_quotation_collated"] is False and r["can_publish"] is False
assert len(x["chronology"])==19
for row in x["chronology"]:
  source_ok(row)
  assert date.fromisoformat(row["start_date"])<=date.fromisoformat(row["end_date"])
  assert row["reader_key"] in readers and row["date_precision"] in ("YEAR","MONTH","DAY")
  assert row["expert_approved"] is False and row["can_publish"] is False
assert len(x["comparisons"])==4
for row in x["comparisons"]:
  source_ok(row)
  assert len(row["reader_keys"])>=3 and set(row["reader_keys"])<=readers
  assert len(row["analysis_ko"])>90 and row["historian_review"]=="PENDING" and row["can_publish"] is False
assert len(x["visual_candidates"])==2
for v in x["visual_candidates"]:
  assert v["catalogue_url"].startswith("https://")
  assert v["rights_status"]=="NOT_VERIFIED_DO_NOT_REUSE" and v["image_folio_inspected"] is False and v["can_publish"] is False
assert len(x["blockers"])>=5
print("PASS V212 10 narratives / 14 relationships / 19 chronology records / 4 comparison themes / 14 source links / rights+publication HOLD")
