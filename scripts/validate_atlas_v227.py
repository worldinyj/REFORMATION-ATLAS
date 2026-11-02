#!/usr/bin/env python3
"""V227 QA: verified manuscript images ≠ diplomatic transcription ≠ K/Z collation."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def get(p): return json.loads((R/p).read_text(encoding="utf-8"))
a19=get("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
a20=get("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")
a21=get("data/deep/atlas_v221_marburg_witness_accession.json")
a22=get("data/deep/atlas_v222_original_image_routes_and_assertions.json")
a23=get("data/deep/atlas_v223_marburg_critical_text_and_date_provenance.json")
a24=get("data/deep/atlas_v224_primary_facsimile_retrieval_gate.json")
a25=get("data/deep/atlas_v225_marburg_fair_copy_print_transmission.json")
a26=get("data/deep/atlas_v226_1529_print_annotation_provenance_audit.json")
d=get("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")

assert d["version"]=="2.27" and d["parent_commit"]=="fb33bf1602395738b40801035716dcf4e124e252"
assert d["base_dataset"]=="data/deep/atlas_v226_1529_print_annotation_provenance_audit.json"
assert all(val is False for val in d["publication_gate"].values())
assert (a19["metrics"]["chapters"],a19["metrics"]["sections"],a19["metrics"]["paragraphs"],a19["metrics"]["sentences"],a19["metrics"]["full_integrated_codepoints"]) == (10,74,128,543,35102)
assert a20["metrics"]["comparison_units"]==5
assert a21["metrics"]["original_exemplar_pages_read"]==0
assert a22["metrics"]["original_pages_visually_read"]==0
assert a23["metrics"]["successful_original_image_page_reads"]==0
assert a24["metrics"]["direct_original_pages_read"]==0
assert a25["metrics"]["original_page_reads"]==0
assert a26["metrics"]["primary_pages_read"]==0

def indexed(items):
    result={x["id"]:x for x in items}
    assert len(result)==len(items), "Duplicate entity ID"
    return result
sources=indexed(d["sources"])
comparisons=indexed(d["comparison_axes"])
issues=indexed(d["open_issues"])
assert len(sources)==7 and len(comparisons)==6 and len(issues)==5
assert all(x["url"].startswith("https://") for x in sources.values())
assert sources["SRC-V227-MS-ITEM"]["shelfmark"]=="Ms Z XI 313.1"
assert sources["SRC-V227-MS-ITEM"]["catalogued_date"]=="1529-09-30"
assert sources["SRC-V227-MS-ITEM"]["rights_mark"]=="Public Domain Mark"
assert sources["SRC-V227-MS-IIIF"]["canvas_count"]==4
assert sources["SRC-V227-MS-PDF"]["pdf_page_count"]==5
artifact=d["artifact"]
assert set(artifact["source_ids"])=={"SRC-V227-MS-ITEM","SRC-V227-MS-PDF","SRC-V227-MS-IIIF"}
assert artifact["date"]=="1529-09-30"
assert artifact["shelfmark"]=="Zentralbibliothek Zürich Ms Z XI 313.1"
assert artifact["is_marburg_articles_k_or_z"] is False
assert artifact["full_manuscript_transcription"] is None
assert artifact["critical_interpretive_translation"] is None
assert artifact["exact_author_hand_authenticated_by_this_project"] is False
assert artifact["pdf_page_count"]==5 and artifact["catalogue_page_count"]==4
pages=artifact["canvas_pages"]
assert len(pages)==4
assert [p["manuscript_page"] for p in pages]==[1,2,3,4]
assert [p["pdf_page_index"] for p in pages]==[1,2,3,4]
assert [p["iiif_image_id"] for p in pages]==["1379285","1379288","1379289","1379291"]
assert all(p["visual_inspected"] is True and p["full_line_transcription_complete"] is False
           and p["iiif_canvas_id"].endswith("/"+p["iiif_image_id"]) for p in pages)
assert artifact["directly_observed_original_pages"]==artifact["visual_page_count_verified"]==4
assert artifact["kz_articles_original_pages_read"]==0
for cmp in comparisons.values():
    assert cmp["source_ids"] and set(cmp["source_ids"]) <= sources.keys()
    assert cmp["interpretation_ko"] and cmp["zwingli_summary_ko"] and cmp["osiander_summary_ko"]
    assert cmp["winner_claim_confirmed"] is False
assert comparisons["CMP-V227-OUTCOME"]["source_ids"]==["SRC-V227-ZW-OCT20","SRC-V227-OSIANDER","SRC-V227-SIGNED"]
reader=d["reader_edition_draft"]
sections=indexed(reader["sections"])
assert len(sections)==3 and set(reader["section_ids"])==sections.keys()
assert all(x["support_ids"] and set(x["support_ids"]) <= sources.keys()
           for x in sections.values())
assert all(x["status"]=="OPEN" for x in issues.values())
assert d["metrics"]=={
 "new_primary_manuscript_items":1,
 "original_manuscript_pages_visually_inspected":4,
 "iiif_canvas_ids_verified":4,
 "source_records":7,"eye_witness_comparison_axes":6,
 "reader_sections":3,"open_issues":5,
 "full_manuscript_transcripts_approved":0,
 "marburg_kz_original_article_pages_read":0,
 "verified_kz_addition_readings":0,
 "published_items":0}
print("PASS V227: original 1529 Melanchthon–Zwingli manuscript 4/4 images observed and IIIF IDs checked")
print("PASS V227: comparison axes 6; original transcript 0; Marburg Z/K Article 7,13,15 remains 0; HOLD")
