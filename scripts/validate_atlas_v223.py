#!/usr/bin/env python3
"""Validate V223 evidence tiers. PASS is NOT original 1529 folio transcription."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p): return json.loads((R/p).read_text(encoding="utf-8"))
v19=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v20=read("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")
v21=read("data/deep/atlas_v221_marburg_witness_accession.json")
v22=read("data/deep/atlas_v222_original_image_routes_and_assertions.json")
d=read("data/deep/atlas_v223_marburg_critical_text_and_date_provenance.json")
assert d["version"]=="2.23"
assert d["parent_commit"]=="8307bd49e8afc102a9e1cd9f0f0719ed4e776565"
assert d["base_dataset"]=="data/deep/atlas_v222_original_image_routes_and_assertions.json"
assert all(x is False for x in d["publication_gate"].values())
assert (v19["metrics"]["chapters"],v19["metrics"]["sections"],v19["metrics"]["paragraphs"],
        v19["metrics"]["sentences"],v19["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v20["metrics"]["comparison_units"]==5 and v20["metrics"]["direct_16c_witness_collations"]==0
assert v21["metrics"]["original_exemplar_pages_read"]==0
assert v22["metrics"]["original_pages_visually_read"]==0
sources={s["id"]:s for s in d["sources"]}
variants={v["id"]:v for v in v20["variant_units"]}
sentences={s["id"]:s for s in v19["sentences"]}
passages={p["id"]:p for p in d["critical_edition_passages"]}
assert len(sources)==len(d["sources"])==7
assert len(passages)==len(d["critical_edition_passages"])==3
assert {p["article"] for p in passages.values()}=={"7","13","15"}
assert all(s["url"].startswith("https://") and s["original_folio_page_seen"] is False
           for s in sources.values())
for p in passages.values():
    assert p["source_id"]=="SRC-V223-GHDI-WA1910"
    assert p["v220_variant_id"] in variants
    assert p["article"]==variants[p["v220_variant_id"]]["article"]
    assert p["witness_assigned"]=="WA1910_EDITORIAL_TRANSCRIPTION_ONLY"
    assert p["read_status"]=="EDITORIAL_GERMAN_TEXT_READ_ORIGINAL_UNREAD"
    assert p["z_added_wording"] is p["k_parallel_wording"] is p["manuscript_folio"] is None
    assert p["context_short"] and p["semantic_outline_ko"]
    assert set(p["v219_sentence_ids"]) <= {s["id"] for s in v19["sentences"]}
    assert set(p["v219_sentence_ids"]) == set(variants[p["v220_variant_id"]]["v219_sentence_ids"])
    assert all(sentences[x]["reader_key"]=="MARBURG" for x in p["v219_sentence_ids"])
date_rows=d["date_evidence"]
assert len(date_rows)==4
assert len({x["id"] for x in date_rows})==4
assert {x["date_label"] for x in date_rows}=={"1529-10-03","1529-10-04"}
assert sum(x["date_label"]=="1529-10-03" for x in date_rows)==3
assert sum(x["date_label"]=="1529-10-04" for x in date_rows)==1
assert all(x["source_id"] in sources for x in date_rows)
attempts=d["image_access_attempts"]
assert len(attempts)==4
assert all(x["source_id"] in sources and x["verified_image_count"]==0
           and x["original_text_transcribed"] is False for x in attempts)
assert all(x["result"] not in ("SUCCESS","IMAGE_READ") for x in attempts)
rights=d["rights_decisions"]
assert len(rights)==2
assert {x["mark"] for x in rights}=={"PUBLIC_DOMAIN_MARK","NOT_ESTABLISHED"}
assert all(x["source_id"] in sources and x["app_media_approved"] is False and
           x["internal_reuse_review_completed"] is False for x in rights)
assert len(d["remaining_issues"])==5 and all(x["status"]=="OPEN" for x in d["remaining_issues"])
assert d["metrics"]=={
  "source_records":7,"edited_german_articles_context_checked":3,
  "distinct_date_metadata_observations":4,"original_image_access_attempts":4,
  "successful_original_image_page_reads":0,"verified_original_variant_wordings":0,
  "w2119_public_domain_metadata_confirmed":1,"release_gate_signoffs":0,"published_items":0
}
print("PASS V223: 3 edited article contexts, 4 date observations, 4 failed image routes")
print("PASS V223: W2119 Public Domain Mark catalogue verified; folio reads 0, variant collation 0, HOLD")
