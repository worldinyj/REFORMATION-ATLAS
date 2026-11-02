#!/usr/bin/env python3
"""V228: original micro-reading vs later editorial quotation integrity.

Machine pass does NOT certify manuscript palaeography or Kohler edition pagination.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def get(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
v19=get("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v20=get("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")
v21=get("data/deep/atlas_v221_marburg_witness_accession.json")
v22=get("data/deep/atlas_v222_original_image_routes_and_assertions.json")
v23=get("data/deep/atlas_v223_marburg_critical_text_and_date_provenance.json")
v24=get("data/deep/atlas_v224_primary_facsimile_retrieval_gate.json")
v25=get("data/deep/atlas_v225_marburg_fair_copy_print_transmission.json")
v26=get("data/deep/atlas_v226_1529_print_annotation_provenance_audit.json")
v27=get("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
d=get("data/deep/atlas_v228_manuscript_microtranscription_and_editorial_variant_audit.json")

assert d["version"]=="2.28"
assert d["parent_commit"]=="41e1b605cb49957a3b71495a26d871f3d8eb15aa"
assert d["baseline_dataset"]=="data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json"
assert all(flag is False for flag in d["publication_gate"].values())
assert all(flag is True for flag in d["methods"].values())
assert (v19["metrics"]["chapters"],v19["metrics"]["sections"],
        v19["metrics"]["paragraphs"],v19["metrics"]["sentences"],
        v19["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v20["metrics"]["direct_16c_witness_collations"]==0
assert v21["metrics"]["original_exemplar_pages_read"]==0
assert v22["metrics"]["original_pages_visually_read"]==0
assert v23["metrics"]["successful_original_image_page_reads"]==0
assert v24["metrics"]["direct_original_pages_read"]==0
assert v25["metrics"]["original_page_reads"]==0
assert v26["metrics"]["primary_pages_read"]==0
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v27["metrics"]["marburg_kz_original_article_pages_read"]==0

def by_id(rows):
    index={x["id"]:x for x in rows}
    assert len(index)==len(rows),"duplicate id"
    return index
src=by_id(d["sources"])
folios=by_id(d["folio_assessment"])
micro=by_id(d["micro_readings"])
edits=by_id(d["editorial_variants"])
checks=by_id(d["interpretive_tests"])
issues=by_id(d["open_issues"])
assert (len(src),len(folios),len(micro),len(edits),len(checks),len(issues))==(8,4,6,2,4,5)
assert set(folios)=={"PAGE-V228-1","PAGE-V228-2","PAGE-V228-3","PAGE-V228-4"}
assert [x["image_id"] for x in d["folio_assessment"]]==[x["iiif_image_id"] for x in v27["artifact"]["canvas_pages"]]
assert [x["pdf_page_zero_index"] for x in d["folio_assessment"]]==[1,2,3,4]
assert all(x["visual_read"] and x["full_text_transcribed"] is False for x in folios.values())
assert all(x["source_ids"]==["SRC-V228-MS-PDF"] for x in folios.values())
assert all(x["url"].startswith("https://") for x in src.values())
assert all(x["page"] in folios and set(x["source_ids"])<=src.keys()
           and x["text_is_full_sentence"] is False
           and x["status"].startswith("DIRECT_IMAGE_")
           and x["confidence"]=="HIGH" for x in micro.values())
assert micro["READ-V228-P1-VERBA"]["token"]=="Verba nihil aliud"
assert all("possunt" not in x["token"] and "posse" not in x["token"]
           for x in micro.values()),"editorial continuation must not be encoded as directly seen"
assert set(edits)=={"ED-V228-1950","ED-V228-1971"}
assert all("posse quam significare" in x["candidate_full_phrase"]
           and not x["claims_original_authograph_exact"]
           and not x["claims_koehler_book_pp_read"]
           and set(x["source_ids"])<=src.keys() for x in edits.values())
assert all(x["support_ids"] and set(x["support_ids"]) <= (src.keys() | micro.keys() | edits.keys()) for x in checks.values())
assert all(x["status"]=="OPEN" for x in issues.values())
fix=d["prior_reading_correction"]
assert fix["corrected_research_status"]=="PROVISIONAL_WITHDRAWN"
assert fix["initial_v228_user_facing_provisional_phrase"]=="Verba nihil aliud possunt significare"
assert fix["preferred_editorial_comparison"]=="Verba nihil aliud posse quam significare"
assert fix["do_not_replace_manuscript_diplomatic_text_with_editorial_quote"] is True
assert d["metrics"]=={
 "primary_manuscript_objects_new":0,"original_manuscript_pages_reinspected":4,
 "cumulative_unique_primary_manuscript_pages":4,"high_confidence_micro_reading_anchors":6,
 "editorial_variant_comparison_candidates":2,"philological_inference_checks":4,
 "unresolved_actions":5,"full_transcription_approved":0,
 "original_marburg_kz_pages_read":0,"published_items":0}
print("PASS V228: 4 re-inspected autograph document pages, 6 selective readings, no full-page reconstruction")
print("PASS V228: 'posse quam' remains indirect 1929 quotation; 'possunt' provisional withdrawn; K/Z HOLD")
