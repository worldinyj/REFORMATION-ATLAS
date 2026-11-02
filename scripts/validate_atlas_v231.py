#!/usr/bin/env python3
"""V231 QA for 1910 WA editorial OCR + 1908/2014 evidence stratification.

Passing this checker never implies scanned-page proofreading or a 1529 autograph reading.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n): return json.loads((R/n).read_text(encoding="utf-8"))
v19=load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=load("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v29=load("data/deep/atlas_v229_koehler_1929_edition_access_and_sourcecriticism.json")
v30=load("data/deep/atlas_v230_gotha_anonymous_manuscript_copies_heppe_lineage.json")
d=load("data/deep/atlas_v231_wa1910_critical_edition_and_marburg_witness_apparatus.json")
assert d["version"]=="2.31"
assert d["parent_commit"]=="54ff75a8c08d61955b92978beb1a7c07a1ebe755"
assert d["baseline_dataset"]=="data/deep/atlas_v230_gotha_anonymous_manuscript_copies_heppe_lineage.json"
assert all(v is False for v in d["publication_gate"].values())
assert (v19["metrics"]["chapters"],v19["metrics"]["sections"],v19["metrics"]["paragraphs"],v19["metrics"]["sentences"],v19["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v29["metrics"]["original_1929_pages_40_42_read"]==0
assert v30["metrics"]["new_archival_report_copy_witnesses"]==3
assert v30["metrics"]["new_primary_images_read"]==0

def unique(xs):
    obj={r["id"]:r for r in xs}
    assert len(obj)==len(xs)
    return obj
sources=unique(d["sources"])
readings=unique(d["reading_units"])
sections=unique(d["reader_sections"])
assert len(sources)==9 and len(readings)==7 and len(sections)==3
assert all(x["url"].startswith("https://") and x["original_page_image_read"] is False for x in sources.values())
assert all(x["source_ids"] and set(x["source_ids"])<=sources.keys()
    and x["level"] and x["ko"] and x["genre"] for x in readings.values())
assert readings["U1"]["normalized"]=="Philippus concessit, verba nihil aliud quam significare"
assert readings["U2"]["normalized"]=="non solum significare, sed simul etiam efficere"
assert readings["U3"]["normalized"] is None
assert readings["U4"]["level"]=="EDITOR_1910_HYPOTHESIS_OCR"
assert readings["U5"]["level"]=="EDITORIAL_APPARATUS_OCR_UNVERIFIED_SIGLA"
assert readings["U6"]["source_ids"]==["SCHUBERT1908","ZARCH"]
assert readings["U7"]["source_ids"]==["SILVA2014"]
assert d["claim_latin1910"]==readings["U1"]["normalized"]
assert d["previous_koehler_indirect_reading"]=="Verba nihil aliud posse quam significare"
assert d["conclusion_on_wording"]=="DIFFERENT_SOURCE_LAYER_NOT_SAME_WITNESS_VARIANT_YET"
assert d["chronology_cautions"]["no_direct_1529_ink_date_inference"] is True
assert d["report_vs_agreement_caution"]
assert set(x["id"] for x in d["reader_sections"])==sections.keys()
assert {u for x in sections.values() for u in x["unit_ids"]}==readings.keys()
assert len(d["open_issues"])==7 and all(d["open_issues"])
assert d["metrics"]=={
 "sources":9,"textual_reading_units":7,"wa1910_units":5,"independent_scholarship_units":2,
 "reader_sections":3,"open_issues":7,"printed_1910_images_seen":0,
 "new_1529_original_pages_seen":0,"original_zk_collations":0,
 "prior_unique_other_1529_manuscript_pages":4,"webapp_publications":0}
print("PASS V231: directly retrieved WA 1910 edited report OCR and critical apparatus; Latin claim/reply distinguished")
print("PASS V231: 1908 Z additions and 2014 partial agreement are scholars' interpretations, not original K/Z readings")
print("PASS V231: 1910 printed scan images 0, K/Z original folios 0, published 0 — HOLD")
