#!/usr/bin/env python3
"""V230 regression: catalogue provenance, copying dates and edition distinctions.

A passing check does NOT authenticate historical handwriting or inspect original folios.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
corpus=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=read("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v28=read("data/deep/atlas_v228_manuscript_microtranscription_and_editorial_variant_audit.json")
v29=read("data/deep/atlas_v229_koehler_1929_edition_access_and_sourcecriticism.json")
d=read("data/deep/atlas_v230_gotha_anonymous_manuscript_copies_heppe_lineage.json")
assert d["version"]=="2.30"
assert d["parent_commit"]=="0d30e27718acfef51deb0793798dcd217da16a8d"
assert d["baseline_dataset"]=="data/deep/atlas_v229_koehler_1929_edition_access_and_sourcecriticism.json"
assert all(v is False for v in d["publication_gate"].values())
assert all(v is True for v in d["source_levels"].values())
assert (corpus["metrics"]["chapters"],corpus["metrics"]["sections"],corpus["metrics"]["paragraphs"],corpus["metrics"]["sentences"],corpus["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v28["metrics"]["cumulative_unique_primary_manuscript_pages"]==4
assert v29["metrics"]["original_1929_pages_40_42_read"]==0
def index(rows):
    result={x["id"]:x for x in rows}
    assert len(result)==len(rows),"duplicate ID"
    return result
sources=index(d["sources"]);witnesses=index(d["manuscript_witnesses"])
objects=index(d["related_document_objects"]);rels=index(d["reported_relationships"])
requests=index(d["acquisition_requests"]);claims=index(d["research_claims"])
issues=index(d["open_issues"])
assert (len(sources),len(witnesses),len(objects),len(rels),len(requests),len(claims),len(issues))==(10,3,4,5,4,4,5)
assert all(s["url"].startswith("https://") and s["original_pages_read"] is False for s in sources.values())
assert set(witnesses)=={"W-V230-GOTHA-A401","W-V230-GOTHA-B1482","W-V230-GOTHA-B493"}
assert sum(w["leaves"] for w in witnesses.values())==28
assert all(w["original_image_read"] is False and w["witness_text_read"] is False
           and set(w["source_ids"])<=sources.keys() for w in witnesses.values())
assert witnesses["W-V230-GOTHA-A401"]["shelfmark"]=="Chart. A 401, Bl. 41r–50v"
assert witnesses["W-V230-GOTHA-B1482"]["shelfmark"]=="Chart. B 1482, Bl. 187r–196v"
assert witnesses["W-V230-GOTHA-B493"]["shelfmark"]=="Chart. B 493, Bl. 22r–29v"
assert witnesses["W-V230-GOTHA-A401"]["editorial_wa_range"]=="WA30/3 110–143"
assert witnesses["W-V230-GOTHA-B1482"]["editorial_wa_range"]=="WA30/3 92–143"
assert witnesses["W-V230-GOTHA-B493"]["editorial_wa_range"]=="WA30/3 92–144, 2. Version"
assert witnesses["W-V230-GOTHA-B493"]["attributed_scribe"].startswith("Johann Mattenberg")
assert witnesses["W-V230-GOTHA-B493"]["copy_date"] is None
assert witnesses["W-V230-GOTHA-B493"]["collection_created_after"]=="1570"
assert all(set(x["source_ids"])<=sources.keys() for x in objects.values() if "source_ids" in x)
assert objects["W-V230-MEL1529"]["original_images_already_inspected"]==4
assert objects["ED-V230-KOEHLER1929"]["directly_read_target_pages"] is False
for relation in rels.values():
    assert relation["from"] in (witnesses.keys()|objects.keys())
    assert relation["to"] in (witnesses.keys()|objects.keys())
    assert relation["sources"] and set(relation["sources"])<=sources.keys()
    assert relation["does_not_prove_textual_ancestry"] is True
h=d["heppe_bibliographic_lineage"]
assert h["first_edition"]["year"]==1847 and h["second_edition"]["year"]==1854
assert h["first_edition"]["title_page_seen"] is False
assert h["second_edition"]["title_page_seen"] is False
assert h["facsimile_original_context"].startswith("Hessian")
assert h["sixteenth_century_original_folio_read_via_reprint"] is False
assert h["resolution"].startswith("BIBLIOGRAPHIC_EDITION_SEQUENCE_RESOLVED_PROVISIONALLY")
assert len(set((h["prior_v224_issue"],h["prior_v226_issue"])))==2
for request in requests.values():
    assert request["target"] in (witnesses.keys()|objects.keys())
    assert request["prepared_not_sent"] and not request["request_sent"] and not request["image_acquired"]
assert all(x["status"]=="OPEN" for x in issues.values())
assert all(x["sources"] and set(x["sources"])<=sources.keys() for x in claims.values())
assert d["metrics"]=={
    "new_archival_report_copy_witnesses":3,"registered_manuscript_leaves":28,
    "catalogue_supported_wa_links":3,"reported_copy_recension_crosschecks":2,
    "bibliography_edition_years_distinguished":2,"new_primary_images_read":0,
    "unique_1529_handwritten_original_pages_unchanged":4,
    "koehler_1929_p40_42_original_pages_read":0,
    "marburg_k_z_variant_pages_read":0,
    "access_requests_prepared_not_sent":4,"webapp_publications":0}
print("PASS V230: Gotha catalogued report copies 10+10+8 leaves and three WA editorial links")
print("PASS V230: Mattenberg is a later copyist; Heppe 1847/1854 are editions; no new images or Z/K witness readings; HOLD")
