#!/usr/bin/env python3
"""ATLAS V240: direct primary-language text through a critical edition is NOT original-folio imaging."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def get(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
v19=get("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=get("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=get("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v39=get("data/deep/atlas_v239_tentzel_german_fair_copy_and_1717_print_reception.json")
d=get("data/deep/atlas_v240_1519_1521_1525_documents_and_cyprian_1718_witnesses.json")
assert d["version"]=="2.40"
assert d["parent_commit"]=="1f2f044b1c4d081a4492542e4a4782d0cea8d3c0"
assert d["baseline"]=="data/deep/atlas_v239_tentzel_german_fair_copy_and_1717_print_reception.json"
assert all(value is False for value in d["publication_gate"].values())
m=v19["metrics"]
assert (m["chapters"],m["sections"],m["paragraphs"],m["sentences"],m["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2
assert v39["metrics"]["seckendorff_1692_p139_directly_read"]==0
def idx(rows):
    result={x["id"]:x for x in rows}
    assert len(result)==len(rows), "duplicate ID"
    return result
src=idx(d["sources"])
wit=idx(d["witnesses"])
links=idx(d["edition_links"])
micro=idx(d["microreadings"])
readers=idx(d["reader_sections"])
issues=idx(d["open_issues"])
assert (len(src),len(wit),len(links),len(micro),len(readers),len(issues))==(14,8,5,10,6,9)
assert all(x["url"].startswith("https://") and x["original_manuscript_folio_image_seen"] is False for x in src.values())
assert src["AK1519"]["read_level"]=="DIRECT_FULL_1519_LATIN_CRITICAL_TRANSCRIPTION"
assert src["AK1521"]["read_level"]=="DIRECT_FULL_1521_GERMAN_CRITICAL_TRANSCRIPTION"
assert src["GOTHA1525"]["read_level"]=="DIRECT_FULL_GOTHA_2025_SCHOLARLY_TRANSCRIPTION"
assert src["CY1718-DIGI"]["read_level"]=="1718_PRINT_BOOK_OBJECT_TARGET_PAGES_NOT_READ"
assert all(set(w["source_ids"])<=src.keys() and w["manuscript_visual_pages_read"]==0 for w in wit.values())
assert {w["id"] for w in d["witnesses"]}=={"1519-A","1519-B","1521-A","1521-B","1521-C","1525-JUN2","1525-JUN18","1525-JUL12"}
assert wit["1519-A"]["primary_text_directly_read_in_critical_edition"] is True
assert wit["1519-B"]["primary_text_directly_read_in_critical_edition"] is False
assert wit["1521-B"]["primary_text_directly_read_in_critical_edition"] is True
assert wit["1521-C"]["primary_text_directly_read_in_critical_edition"] is False
assert wit["1521-A"]["scribal_agent"]=="Philipp Melanchthon"
assert wit["1525-JUL12"]["primary_text_directly_read_in_critical_edition"] is True
assert all(e["witness_id"] in wit and e["printed_page_image_read"] is False and set(e["source_ids"])<=src.keys() for e in links.values())
assert links["P-1519"]["witness_id"]=="1519-A"
assert links["P-1519"]["printed"]=="pp109–111 No15"
assert links["P-1521"]["witness_id"]=="1521-C"
assert links["P-1521"]["printed"]=="pp238–240 No54"
assert links["P-1525-JUL12"]["printed"]=="pp361f"
s=d["structural_distinction"]
assert s["first_book_year"]==1717 and s["second_book_year"]==1718
assert s["cyprian1718_p109_111_from_1519_latin_A"] is True
assert s["cyprian1718_p238_240_from_1521_german_C"] is True
assert s["academy1521_online_text_uses_german_B"] is True
assert s["manuscript_a648_chapters5_13_not_proven_in_1718_second_book"] is True
assert s["sourcebook_1718_printed_page_image_read"] is False
assert s["gotha_original_folios_directly_read"] is False
assert all(x["witness_id"] in wit and x["source_ids"] and set(x["source_ids"])<=src.keys()
           and x["original_excerpt"] and x["interpretation_ko"] for x in micro.values())
assert micro["M02"]["original_excerpt"]=="nondum tamen hactenus in manus nostras pervenit"
assert micro["M03"]["original_excerpt"]=="in omnibus rebus honestis et licitis"
assert micro["M09"]["witness_id"]=="1525-JUL12"
assert all(len(x["text_ko"])>=85 and set(x["anchors"])<=micro.keys() for x in readers.values())
assert len(issues)==9 and all(x["question"] for x in issues.values())
assert d["metrics"]=={
    "source_records":14,"documentary_witnesses":8,
    "printed_1718_source_links":5,"primary_microreadings":10,
    "korean_reader_sections":6,"open_issues":9,
    "critical_edition_1519_and_1521_primary_texts_read":2,
    "gotha_2025_historic_news_source_transcriptions_read":1,
    "original_1718_print_pages_read":0,
    "original_gotha_early_manuscript_pages_read":0,
    "original_tentzel_a648_pages_read":0,
    "previous_1529_k_archive_photo_faces":2,
    "previous_1529_conversation_original_pages":4,"published_items":0}
print("PASS V240: 1519 four-paragraph Latin and 1521 German primary text directly READ from critical editions")
print("PASS V240: Gotha July 12 1525 manuscript text quoted in 2025 academic transcription, not original scanned page")
print("PASS V240: Cyprian 1718 No15 from 1519 A, No54 from 1521 C vs modern B, 1525 three print links")
print("PASS V240: all 1717/1718 prints and Gotha original handwriting unviewed; publication HOLD, V219 original history preserved")
