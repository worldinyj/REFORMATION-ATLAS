#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
x=json.loads((R/"data/deep/atlas_v217_critical_edition_passages.json").read_text(encoding="utf-8"))
assert x["version"]=="2.17" and x["parent_commit"]=="10ffa58b21821e39675906295a64611b3b9000d0"
assert all(v is False for v in x["publication_gate"].values())
m=x["metrics"]
assert (m["passage_units"],m["source_records"],m["editorial_proposals"],m["substantive_korean_paragraph_drafts"])==(6,9,5,4)
assert m["facsimile_pages_of_1858_print_inspected"]==2
assert m["original_16c_manuscript_or_print_folios_collated"]==m["scholarly_signoffs"]==0
sources={s["id"] for s in x["sources"]}
passages={p["id"] for p in x["passages"]}
assert len(sources)==9 and len(passages)==6
for s in x["sources"]:
    assert s["url"].startswith("https://")
    assert s["sixteenth_century_original_folio_directly_read"] is False
for p in x["passages"]:
    assert p["source_ids"] and set(p["source_ids"])<=sources
    assert len(p["observation_ko"])>95 and len(p["short_excerpt"].split())<10
    assert p["sixteenth_century_original_folio_read"] is False and p["scholar_approved"] is False and p["can_publish"] is False
for p in x["substantive_paragraph_drafts"]:
    assert len(p["body_ko"])>250 and p["can_publish"] is False
for f in x["editorial_proposals"]:
    assert set(f["passage_ids"])<=passages and f["human_approved"] is False
assert len(x["v216_linked_dossiers"])==3 and len(x["unresolved"])==4
print("PASS V217: 6 historical-language scope notes; 2 pages of 1858 critical edition seen; 0 direct 16c witnesses; research HOLD")
