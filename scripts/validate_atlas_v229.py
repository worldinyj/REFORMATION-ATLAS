#!/usr/bin/env python3
"""V229 source-critical Köhler edition identity and reading-access validation."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(name):return json.loads((R/name).read_text(encoding="utf-8"))
corpus=load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v28=load("data/deep/atlas_v228_manuscript_microtranscription_and_editorial_variant_audit.json")
d=load("data/deep/atlas_v229_koehler_1929_edition_access_and_sourcecriticism.json")
assert d["version"]=="2.29"
assert d["parent_commit"]=="02b10fe3af9dd83c31b798712774f36b2b2dd6ea"
assert d["baseline_dataset"]=="data/deep/atlas_v228_manuscript_microtranscription_and_editorial_variant_audit.json"
assert all(value is False for value in d["release_gate"].values())
assert (corpus["metrics"]["chapters"],corpus["metrics"]["sections"],corpus["metrics"]["paragraphs"],corpus["metrics"]["sentences"],corpus["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v28["metrics"]["cumulative_unique_primary_manuscript_pages"]==4
assert v28["metrics"]["full_transcription_approved"]==0
def index(xs):
    x={v["id"]:v for v in xs}
    assert len(x)==len(xs),"duplicate ID"
    return x
src=index(d["sources"]); ed=index(d["editions"]); seg=index(d["structural_evidence"]); quotes=index(d["sought_passages"]); attempts=index(d["attempts"])
assert (len(src),len(ed),len(seg),len(quotes),len(attempts))==(7,2,2,2,5)
assert all(s["url"].startswith("https://") and not s["page_40_42_image_read"] for s in src.values())
assert ed["EDITION-V229-RECONSTRUCTION"]["pages"]==141
assert ed["EDITION-V229-RECONSTRUCTION"]["google_books_id"]=="5tI8AAAAYAAJ"
assert ed["EDITION-V229-BRIEF"]["pages"]==43
assert ed["EDITION-V229-BRIEF"]["google_books_id"] is None
assert ed["EDITION-V229-RECONSTRUCTION"]["slub_id"]!=ed["EDITION-V229-BRIEF"]["slub_id"]
assert all(z["source_ids"] and set(z["source_ids"])<=src.keys() and not z["pages_40_42_direct_read"] for z in ed.values())
assert seg["SECTION-V229-RECONSTRUCT"]["pages_from"]==8 and seg["SECTION-V229-RECONSTRUCT"]["pages_to"]==38
assert seg["SECTION-V229-CRITICAL"]["pages_from"]==39 and seg["SECTION-V229-CRITICAL"]["pages_to"]==141
assert seg["SECTION-V229-CRITICAL"]["role"]=="SOURCE_CRITICAL_ANALYSIS"
assert all(z["parent_edition"] in ed and set(z["source_ids"])<=src.keys() and not z["original_page_images_seen"] for z in seg.values())
assert all(q["target_edition"]=="EDITION-V229-RECONSTRUCTION" and not q["passage_read_from_1929_original"]
           and q["exact_punctuation_and_context"] is None and not q["correction_confirmed_by_original"]
           and set(q["source_ids"])<=src.keys() for q in quotes.values())
assert quotes["QUOTE-V229-P40"]["previous_provisional_withdrawn"]=="Verba nihil aliud possunt significare"
assert quotes["QUOTE-V229-P40"]["previous_editorial_phrase"]=="Verba nihil aliud posse quam significare"
assert all(not attempt["file_bytes_verified"] and attempt["pages_visually_read"]==0 for attempt in attempts.values())
assert "HTTP_403" in attempts["ATTEMPT-V229-PDF"]["result"] and "HTTP_403" in attempts["ATTEMPT-V229-TEXT"]["result"]
assert d["philology_reconciliation"]["manuscript_readable_prefix"]=="Verba nihil aliud"
assert d["philology_reconciliation"]["is_p40_reconstructed_1529_dialogue"] is False
assert d["philology_reconciliation"]["directly_verified_in_koehler_1929"] is False
assert d["metrics"]=={"source_records":7,"distinct_1929_koehler_books":2,"verified_1929_full_book_digitization_catalogues":2,"critically_mapped_page_sections":2,"original_1929_pages_40_42_read":0,"digital_access_attempts":5,"confirmed_original_latin_full_readings":0,"new_1529_manuscript_pages_read":0,"old_1529_manuscript_unique_pages_retained":4,"marburg_kz_collations":0,"published_items":0}
print("PASS V229: original Köhler 1929 digital record identified; 141-page vs 43-page works distinct")
print("PASS V229: 1930 review confirms reconstructed pp8-38 vs critical pp39-141; exact p40 text unread/HOLD")
