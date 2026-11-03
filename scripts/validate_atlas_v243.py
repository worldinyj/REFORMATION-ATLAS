#!/usr/bin/env python3
"""V243: reject false original-image readings and unwarranted biblical direct-quotation claims."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
v19=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=read("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=read("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v42=read("data/deep/atlas_v242_gotha_cyprian_rebinding_and_sophia_1525_lexical_source_criticism.json")
d=read("data/deep/atlas_v243_sophia_1880_1881_edition_and_biblical_nonretaliation_parallels.json")

assert d["version"]=="2.43"
assert d["parent_commit"]=="ad07e9c3467d47a94dd1af80fdf7c938f87134de"
assert d["parent_data"]=="data/deep/atlas_v242_gotha_cyprian_rebinding_and_sophia_1525_lexical_source_criticism.json"
assert all(flag is False for flag in d["publication_gate"].values())
assert all(flag is False for flag in v42["publication_gate"].values())
m=v19["metrics"]
assert (m["chapters"],m["sections"],m["paragraphs"],m["sentences"],m["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2

def index(rows):
    ix={x["id"]:x for x in rows}
    assert len(ix)==len(rows),"duplicate id"
    return ix
src=index(d["sources"])
units=index(d["textual_units"])
par=index(d["biblical_parallels"])
critic=index(d["source_criticism"])
readers=index(d["reader_sections"])
checks=index(d["access_results"])
assert (len(src),len(units),len(par),len(critic),len(readers),len(checks))==(11,5,4,6,6,5)
assert all(s["url"].startswith("https://") and s["reading"] and s["kind"] for s in src.values())
assert src["KAW-1880-PDF"]["reading"]=="ACTUAL_PDF_REDIRECTED_TO_ANTIBOT_CHALLENGE"
assert src["SLUB-V13"]["reading"]=="DIRECT_INSTITUTIONAL_CATALOGUE"
assert src["SOPHIA-2025"]["reading"]=="DIRECT_FULL_INSTITUTIONAL_ARTICLE_WITH_EARLY_GERMAN_MICRO_EXCERPTS"
bib=d["exact_sophia_edition"]
assert bib["volume"]==13
assert bib["volume_designation_year"]==1880
assert bib["physical_printed_issue_year_reported_by_slub"]==1881
assert bib["slub_catalogue_notation"]=="13.1880(1881)+Index"
assert bib["target_printed_pages"]=="330–335"
assert bib["kawerau_p330_335_actual_page_seen"]==0
assert bib["jena_exact_pdf_discovered_but_blocked"] is True
assert bib["year_issue_vs_print_not_automatically_identical"] is True

assert units["T1"]["original"]=="nicht flüchgen"
assert units["T1"]["sense"]=="NOT_TO_CURSE"
assert units["T5"]["original"]=="flygen"
assert units["T5"]["sense"]=="FLEE_PHYSICAL_DANGER"
assert units["T2"]["original"]=="nicht argeß mit argem begaben"
assert units["T3"]["original"]=="wey vnß der her selbest lernet"
assert units["T4"]["original"]=="Jch bin jo etwaß ewangliß"
assert all(len(x["original"].split())==x["words"] and x["source"]=="SOPHIA-2025" and x["text_status"]=="READ_GOTHA_2025_EXCERPT_NOT_PHOTO" for x in units.values())
assert sum(x["words"] for x in units.values())==19
assert {p["biblical_ref"] for p in par.values()}=={"Romans 12:14","Romans 12:17","1 Peter 3:9","Matthew 5:44"}
assert all(p["actual_1525_specific_verse_citation_proven"] is False and p["source"] in src and set(p["sophia_units"])<=units.keys() for p in par.values())
assert par["B2"]["source"]=="RO12-GREEK"
assert "κακὸν ἀντὶ κακοῦ" in par["B3"]["original_greek"]
assert par["B4"]["parallel_strength"]=="THEMATIC_NOT_VERBATIM"
assert all(z["question"] and z["answer"] for z in critic.values())
assert all(r["title"] and len(r["text"])>90 and set(r["refs"])<=units.keys() for r in readers.values())
assert all(ch["url"].startswith("https://") and ch["original_print_page_images_seen"]==0 for ch in checks.values())
assert checks["A1"]["result"]=="ANTIBOT_POW_CHALLENGE"
assert checks["A3"]["result"]=="WEB_INTERNAL_ERROR"
assert len(d["open_issues"])==10
assert d["metrics"]=={
 "source_records":11,"original_sophia_short_text_units":5,"short_sophia_excerpt_words":19,
 "biblical_parallel_candidates":4,"source_critical_interpretations":6,"reader_sections":6,
 "original_access_checks":5,"open_issues":10,"confirmed_old_print_pages_read_this_version":0,
 "confirmed_1525_manuscript_folios_read_this_version":0,
 "confirmed_1718_original_print_pages_read_this_version":0,
 "old_core_essays_preserved":10,"old_core_search_sentences_preserved":543,"published_web_items":0}
print("PASS V243: quote corpus 5 Sophia micro units/19 words; flüchgen=curse, flygen=flee")
print("PASS V243: biblical Greek Romans12:14,17; 1Peter3:9; Matt5:44 THEMATIC, not direct verbatim 1525 proven")
print("PASS V243: Harz year 13=1880 volume, issued 1881 per SLUB; 1880 PDF file path known but anti-bot")
print("PASS V243: no claimed Sophia manuscript/Kawerau1881/Cyprian1718 original pages; V219 source corpus and HOLD intact")
