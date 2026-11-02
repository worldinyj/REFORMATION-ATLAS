#!/usr/bin/env python3
"""V237 bibliography identity and 1691 actual release/1692 imprint provenance QA.

This validator cannot certify unseen manuscript/print pages or source-text stemmata.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def get(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
corpus=get("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=get("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=get("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v36=get("data/deep/atlas_v236_jonas_1529_letter_double_copy_and_textual_transmission.json")
d=get("data/deep/atlas_v237_gotha_jonas_accession_1691_1692_provenance.json")
assert d["version"]=="2.37"
assert d["parent_commit"]=="cb851cd310c596846ef8dac154b47f4570ec2c01"
assert d["baseline"]=="data/deep/atlas_v236_jonas_1529_letter_double_copy_and_textual_transmission.json"
assert all(v is False for v in d["publication_gate"].values())
assert (corpus["metrics"]["chapters"],corpus["metrics"]["sections"],
        corpus["metrics"]["paragraphs"],corpus["metrics"]["sentences"],
        corpus["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2

def indexed(rows):
    res={x["id"]:x for x in rows}
    assert len(res)==len(rows),"duplicate document ID"
    return res
src=indexed(d["sources"])
assert len(src)==9
assert all(x["url"].startswith("https://") and x["level"] and x["finding"] for x in src.values())
assert src["GOTHA-BLOG"]["level"]=="FULL_INSTITUTIONAL_2024_ARTICLE"
assert src["BSB-BOOK"]["level"]=="DIGITAL_OBJECT_IDENTIFIED_VIEWER_UNREACHABLE"
assert src["CR1834"]["level"]=="DIGITAL_BOOK_CATALOGUE_NOT_TARGET_TEXT"
assert d["accession"]["wrong_id"]=="DE-611-HS-4254430"
assert d["accession"]["correct_jonas_id"]=="DE-611-HS-4254434"
assert d["accession"]["repaired_in_v236_parent"] is True
assert "1552" in d["accession"]["wrong_work"]
assert d["accession"]["gotha_folio"]=="Chart. A 453, 24v–25v"
older=indexed(v36["sources"])
assert older["A453"]["url"].endswith("DE-611-HS-4254434")
assert not older["A453"]["url"].endswith("4254430")
assert v36["witness_objects"][0]["shelfmark"]=="Chart. A 453, Bl. 24v–25v"
assert d["imprint"]["first_book_publication"]==1687
assert d["imprint"]["complete_publication"]=="autumn 1691"
assert d["imprint"]["title_page_year"]==1692
assert d["imprint"]["actual_1692_print_page_read"] is False
assert d["digitized_1692"]["object_id"]=="bsb10716130"
assert d["digitized_1692"]["viewer_url"].endswith("/bsb10716130")
assert d["digitized_1692"]["viewer_opened"] is False
assert d["digitized_1692"]["iiif_download_verified"] is False
assert d["digital_iiif"]["candidate_url"].endswith("/bsb10716130/manifest")
assert d["digital_iiif"]["canvas_ids_extracted"]==0
assert d["digital_iiif"]["original_images_1692_read"]==0
timeline=indexed(d["timeline"])
assert len(timeline)==6
assert [x["year"] for x in d["timeline"]]==[1680,1686,1687,1688,1691,1692]
assert all(x["source_ids"] and set(x["source_ids"])<=src.keys() for x in timeline.values())
assert d["research_network"]["bias_limit"]
assert len(d["research_network"]["phases"])==3
ladder=indexed(d["witness_ladder"])
assert len(ladder)==6
assert all(x["read_pages"]==0 for x in ladder.values() if x["id"]!="L-1997")
assert ladder["L-1997"]["read_pages"]==1
reader=indexed(d["reader_sections"])
assert len(reader)==5 and [x["id"] for x in d["reader_sections"]]==list(range(1,6))
assert all(x["refs"] and set(x["refs"])<=src.keys() and len(x["summary_ko"])>70 for x in reader.values())
issues=indexed(d["open_issues"])
assert len(issues)==8 and all(x["question"] for x in issues.values())
assert d["metrics"]=={
 "catalogue_id_fixes_in_parent_v236":1,
 "new_1529_manuscript_pages_seen":0,
 "source_records":9,
 "publication_timeline_events":6,
 "documentary_ladder_levels":6,
 "korean_scholarly_reader_sections":5,
 "original_1691_1692_book_pages_seen":0,
 "existing_k_official_photographed_faces":2,
 "existing_zwingli_melanchthon_original_pages":4,
 "open_issues":8,
 "webapp_publications":0}
print("PASS V237: repaired Jonas catalogue ID 4254434 not Menius 1552 ID 4254430")
print("PASS V237: Seckendorff first book 1687, actual full edition autumn 1691, title imprint 1692")
print("PASS V237: BSB MDZ digitization ID verified from official Gotha article; printed p139 not read; no public assets")
