#!/usr/bin/env python3
"""V212 cross-reader sourcing and dated-event QA; do not infer historical fact certification."""
import json
from pathlib import Path
from datetime import date
root=Path(__file__).resolve().parents[1]
def load(p):return json.loads((root/p).read_text(encoding="utf-8"))
d=load("data/deep/atlas_v212_cross_reader_links_and_timeline.json")
v11=load("data/deep/atlas_v211_ten_reader_hus_augsburg_revision.json")
assert d["version"]=="2.12" and d["lineage"]["base_commit"]=="a667c1e9b972d6a8d88b8d810fa43597706ed9e0"
assert all(x is False for x in d["publication_gate"].values())
m=d["metrics"]
assert (m["reader_essays"],m["typed_links"],m["timeline"],m["comparison_topics"],m["source_records"],m["visual_candidates"])==(10,14,20,4,14,2)
assert m["original_folio_collated"]==m["expert_approvals"]==m["public_ready"]==0
readers={c["key"] for c in v11["chapters"]}
sources={s["id"] for s in d["sources"]}
assert len(readers)==10 and len(sources)==14
assert all(s["url"].startswith("https://") and s["original_folio_collated"] is False and s["rights_to_embed_image_cleared"] is False for s in d["sources"])
essays={e["reader_key"]:e for e in d["reader_essays"]}
assert set(essays)==readers
for e in essays.values():
    assert len(e["core_context_ko"])+len(e["connected_historical_explanation_ko"])>=220
    assert e["source_ids"] and set(e["source_ids"])<=sources
    assert e["linked_reader_keys"] and set(e["linked_reader_keys"])<=readers
    assert e["human_expert_review"]=="PENDING" and e["source_original_witness_collated"] is False and e["can_publish"] is False
for r in d["typed_links"]:
    assert r["from"] in readers and r["to"] in readers and r["from"]!=r["to"]
    assert set(r["source_ids"])<=sources and r["source_ids"]
    assert r["original_witness_verified"] is False and r["expert_approved"] is False and r["can_publish"] is False
for t in d["chronology"]:
    a=date.fromisoformat(t["from"])
    b=date.fromisoformat(t["to"])
    assert 1300<a.year<=b.year<1700 and a<=b
    assert t["granularity"] in ("DAY","MONTH","YEAR") and t["reader_key"] in readers
    assert t["source_ids"] and set(t["source_ids"])<=sources
    assert t["historical_original_witness_collated"] is False and t["expert_approved"] is False and t["can_publish"] is False
for x in d["comparisons"]:
    assert len(x["reader_keys"])>=3 and set(x["reader_keys"])<=readers
    assert len(x["analysis_ko"])>130 and x["caution_ko"]
    assert x["source_ids"] and set(x["source_ids"])<=sources
    assert x["expert_reviewed"] is False and x["can_publish"] is False
for v in d["visual_candidates"]:
    assert v["catalogue_url"].startswith("https://")
    assert v["embed_permission"] is False and v["rights_status"].startswith("HOLD")
assert len(d["blockers"])>=6
print("PASS V212: 10 history essays, 14 typed links, 20 dates, 4 comparisons, 14 independent source leads, 2 visual HOLD records")
