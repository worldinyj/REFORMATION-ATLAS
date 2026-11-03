#!/usr/bin/env python3
"""V242 provenance and word-sense QA.

Do not certify individual 16th-century folios or 1718 printed pages unseen.
Institutional modern transcriptions are explicitly not optical originals.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
v19=load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=load("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=load("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v41=load("data/deep/atlas_v241_franciscan_1521_dual_print_and_sophia_1525_original_copy.json")
d=load("data/deep/atlas_v242_gotha_cyprian_rebinding_and_sophia_1525_lexical_source_criticism.json")

assert d["version"]=="2.42"
assert d["parent_commit"]=="6313c4a0c56b5377293d7b0b31456173741ba78f"
assert d["baseline"]=="data/deep/atlas_v241_franciscan_1521_dual_print_and_sophia_1525_original_copy.json"
assert all(value is False for value in d["publication_gate"].values())
assert all(value is False for value in v41["publication_gate"].values())
m=v19["metrics"]
assert (m["chapters"],m["sections"],m["paragraphs"],m["sentences"],m["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2
assert v41["metrics"]["full_original_1718_print_pages_read"]==0

def by_id(rows):
    ids={item["id"]:item for item in rows}
    assert len(ids)==len(rows),"duplicate evidence id"
    return ids
src=by_id(d["sources"])
timeline=by_id(d["provenance_timeline"])
objects=by_id(d["manuscript_objects"])
edges=by_id(d["confirmed_edges"])
not_edges=by_id(d["nonedges"])
anchors=by_id(d["textual_anchors"])
questions=by_id(d["case_questions"])
attempts=by_id(d["access_attempts"])
reader=by_id(d["reader_sections"])
issues=by_id(d["open_issues"])
assert tuple(map(len,(src,timeline,objects,edges,not_edges,anchors,questions,attempts,reader,issues)))==(13,10,6,3,6,7,6,5,6,10)
assert all(x["url"].startswith("https://") and x["read_status"] for x in src.values())
assert src["GOTHA-WATER-2025"]["read_status"]=="FULL_ARTICLE_DIRECT_READ"
assert src["GOTHA-SOPHIA-2025"]["read_status"]=="FULL_ARTICLE_WITH_AUTOGRAPH_QUOTATIONS_DIRECT_READ"
assert src["JENA-1525-IMAGE"]["read_status"]=="EXACT_FACSIMILE_LEAD_FOUND_IMAGES_NOT_VISUALLY_READ"
assert src["KAW-1880"]["read_status"]=="ORIGINAL_1880_PRINT_PAGE_330_TO_335_NOT_READ"
assert src["CY-1718-I"]["read_status"]=="DIGITAL_OBJECT_VALID_TEXT_367_TO_372_NOT_READ"
assert src["CY-1718-II"]["read_status"]=="DIGITAL_OBJECT_VALID_TEXT_234_TO_240_NOT_READ"
assert all(x["source_ids"] and set(x["source_ids"])<=src.keys() for x in timeline.values())
assert timeline["P03"]["evidence_class"]=="PROBABLE_DISASTER_CAUSATION_NOT_PROVEN"
assert timeline["P07"]["evidence_class"]=="DOCUMENT_ARCHIVAL_REBINDING"
assert "Chart A336" in timeline["P07"]["claim_ko"]
assert objects["M-SOPHIA-1525"]["shelfmark"]=="Gotha Chart A338 fol254r–256v"
assert objects["M-SOPHIA-COPY"]["shelfmark"]=="Gotha Chart A338 fol257r–260bv"
assert objects["M-ELECTOR-LATIN"]["shelfmark"]=="Gotha Chart A379 fol30rv"
assert all(obj["digital_folio_images_seen"]==0 and set(obj["source_ids"])<=src.keys() for obj in objects.values())
assert edges["E1"]["from"]=="M-SOPHIA-1525" and edges["E1"]["to"]=="M-SOPHIA-COPY"
assert edges["E1"]["relation"]=="LATER_COPY_EXPLICITLY_OF_ORIGINAL"
assert edges["E2"]["relation"]=="SPALATIN_GERMAN_TRANSLATION_OF_LATIN_REQUEST"
assert all(e["textual_variants_verified"] is False for e in edges.values())
assert all(n["denied_claim"] and n["reason"] for n in not_edges.values())
assert "1613" in not_edges["N2"]["denied_claim"]
assert "1525" in not_edges["N1"]["denied_claim"]
assert anchors["A01"]["excerpt"]=="nicht flüchgen"
assert anchors["A01"]["lemma"]=="fluchen"
assert anchors["A06"]["excerpt"]=="flygen"
assert anchors["A06"]["lemma"]=="fliehen"
assert anchors["A01"]["folio"]=="254r"
assert anchors["A06"]["folio"]=="255r"
assert anchors["A05"]["excerpt"]=="Jch bin jo etwaß ewangliß"
assert anchors["A05"]["lemma"]=="evangelisch"
assert all(len(a["excerpt"].split())==a["words"] and a["source_id"] in src and a["original_folio_visual_read"] is False for a in anchors.values())
assert sum(a["words"] for a in anchors.values())==22
assert all(q["sources"] and set(q["sources"])<=src.keys() and len(q["answer_ko"])>70 for q in questions.values())
assert all(x["url"].startswith("https://") and x["actual_print_pages_read"]==0 for x in attempts.values())
assert attempts["ATT1718-I"]["result"]=="WEB_INTERNAL_ERROR"
assert attempts["ATT1718-IIIF"]["result"]=="WEB_INTERNAL_ERROR_AND_CONTAINER_DNS_FAILURE"
assert len(reader)==6
assert all(len(x["content_ko"])>120 and set(x["supports"])<=anchors.keys() for x in reader.values())
assert all(x["task"] for x in issues.values())
assert d["metrics"]=={
    "new_documentary_sources":13,
    "provenance_timeline_events":10,
    "tracked_manuscript_objects":6,
    "confirmed_archival_or_edition_edges":3,
    "explicitly_rejected_inferences":6,
    "original_language_short_anchors":7,
    "source_criticism_case_questions":6,
    "original_access_attempts":5,
    "korean_reader_sections":6,
    "open_issues":10,
    "new_original_manuscript_or_18c_print_pages_read":0,
    "prior_1529_k_photographic_faces":2,
    "prior_1529_other_autograph_pages":4,
    "webapp_publications":0}
print("PASS V242: 1525 flüchgen=fluchen (curse) vs flygen=fliehen (flee) independently typed")
print("PASS V242: 1717 Cyprian reshelving / five rebinding volumes ≠ source documents' original physical order")
print("PASS V242: Sophia later copy not independent witness; 1613 flood unproven for each folio; modern transcriptions ≠ scans")
print("PASS V242: 1718/1880/Jena original target pages unread, old 10 essay corpus preserved, publication HOLD")
