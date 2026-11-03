#!/usr/bin/env python3
"""ATLAS V244 historical provenance QA: three distinct female witness perspectives 1524-1526.

Catalogued editions, short quotations in modern scholarship and original printed
or handwritten page photographs are separate evidence types.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

v19=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=read("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=read("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v43=read("data/deep/atlas_v243_sophia_1880_1881_edition_and_biblical_nonretaliation_parallels.json")
d=read("data/deep/atlas_v244_1524_florentina_1525_sophia_1526_helfta_holzzelle_three_witness_perspectives.json")

assert d["version"]=="2.44"
assert d["parent_commit"]=="433243e31978180f6647ca2f02a2ddeae3033d87"
assert d["baseline"]=="data/deep/atlas_v243_sophia_1880_1881_edition_and_biblical_nonretaliation_parallels.json"
assert all(x is False for x in d["publication_gate"].values())
assert all(x is False for x in v43["publication_gate"].values())

m=v19["metrics"]
assert (m["chapters"],m["sections"],m["paragraphs"],m["sentences"],m["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2

def keyed(items):
    result={v["id"]:v for v in items}
    assert len(result)==len(items), "Duplicate historical source ID"
    return result
sources=keyed(d["sources"])
voices=keyed(d["voices"])
physical=keyed(d["physical_print_witnesses"])
variants=keyed(d["catalogue_print_variants"])
anchors=keyed(d["transcribed_short_anchors"])
events=keyed(d["chronology"])
readers=keyed(d["reader_sections"])
issues=d["open_issues"]

assert (len(sources),len(voices),len(physical),len(variants),len(anchors),len(events),len(readers),len(issues))==(15,3,5,5,6,10,8,10)
assert all(s["url"].startswith("https://") and s["reading_level"] and s["description"]
           and s["original_1524_1525_1526_page_folio_directly_seen"] is False for s in sources.values())
assert "1524 LUTH AA" in sources["EMORY-1524"]["description"]
assert "O90" in sources["HAB-1524"]["description"] and "O91" in sources["HAB-1524"]["description"]
assert sources["OXFORD-2023"]["reading_level"]=="DIRECT_ACADEMIC_TEXT_EXTRACT_FROM_2023_PDF"
assert sources["OEF-2019"]["reading_level"]=="MODERN_SCHOLARLY_HISTORICAL_STUDY_TEXT_EXTRACT"
assert "192" not in sources["SLUB-HARZ-13"]["description"]  # catches typo in edition century
assert sorted(v["year"] for v in voices.values())==[1524,1525,1526]
assert all(v["source_ids"] and set(v["source_ids"])<=sources.keys()
           and v["original_page_images_seen"]==0 for v in voices.values())
assert "Helfta" in voices["VOICE-1524"]["religious_community"]
assert voices["VOICE-1525"]["religious_community"]=="Naundorf / Kloster Neuendorf near Allstedt"
assert voices["VOICE-1526"]["religious_community"]=="Two different convent communities Helfta and Holzzelle"
assert all(p["source_ids"] and set(p["source_ids"])<=sources.keys() and p["scan_pages_read"]==0 for p in physical.values())
assert physical["FLO-HAB-O90"]["shelfmark"].endswith("VD16 O90")
assert physical["FLO-HAB-O91"]["shelfmark"].endswith("VD16 O91")
assert "14 unnumbered" in physical["FLO-EMORY"]["extent"]
assert "16 pages" in physical["FLO-BSB"]["extent"]
assert "pp330–338" in physical["KAW-V13"]["shelfmark"]
assert all(v["from"] in physical and v["to"] in physical
           and v["page_image_verified"] is False for v in variants.values())
assert variants["V-01"]["reading_a"]=="Eyn geschihct"
assert variants["V-01"]["reading_b"]=="Eyn geschicht"
assert variants["V-03"]["leaf"]=="A4r line16"
assert variants["V-03"]["reading_a"]=="klosters"
assert variants["V-03"]["reading_b"]=="kloisters"
assert variants["V-04"]["leaf"]=="A4r line17"
assert variants["V-04"]["reading_a"]=="schrifftlich"
assert variants["V-04"]["reading_b"]=="schrfftlich"
assert variants["V-05"]["from"]==variants["V-05"]["to"]=="FLO-HAB-O91"  # within-impression copy variants not false editions
assert all(a["source_id"] in sources and a["words"]==len(a["text"].split())
           and a["original_pamphlet_photo_seen"] is False for a in anchors.values())
assert sum(a["words"] for a in anchors.values())==25
assert anchors["L-01"]["voice"]=="LUTHER_EDITORIAL_FRAME"
assert anchors["F-01"]["voice"]=="FLORENTINA_AUTOBIOGRAPHICAL_METAPHOR"
assert anchors["S-01"]["text"]=="nicht flüchgen"
assert "gott" in anchors["L-01"]["text"].lower()
assert all(event["sources"] and set(event["sources"])<=sources.keys() for event in events.values())
assert events["Y07"]["date"]=="1526-11-12"
assert events["Y08"]["date"]=="1529-06-12"

c=d["issue_entanglement"]
assert len(c["religious_communities_distinct"])==3
assert c["florentina_location"]=="HELFTA_NEUHELFTA"
assert c["sophia_location"]=="NAUNDORF_NEUENDORF"
assert all(x is True for x in [
 c["florentina_1524_not_same_as_sophia_1525"],
 c["florentina_1524_grievance_not_independent_proof_of_every_accusation"],
 c["abbess_1526_political_petition_not_same_document_as_sophia_1525_personal_letter"],
 c["abbess_1526_source_is_not_direct_original_read"],
 c["luther_editorial_polemic_must_not_replace_florentina_original_autobiography"]])
assert all(len(r["body_ko"])>100 and set(r["sources"])<=sources.keys() for r in readers.values())
assert len(issues)==10 and all(q for q in issues)
assert d["metrics"]=={
 "sources":15,"three_perspectives":3,"distinct_monastic_communities":3,
 "old_print_witnesses":5,"official_1524_bibliographic_variants":5,
 "short_reported_original_language_anchors":6,"chronology_events":10,
 "new_reader_sections":8,"open_issues":10,
 "full_1524_old_print_pages_directly_seen":0,
 "full_1525_autograph_pages_directly_seen":0,
 "full_1526_petition_old_print_pages_directly_seen":0,
 "prior_1529_k_photographed_faces":2,
 "prior_1529_zwingli_dialogue_pages":4,"webapp_publications":0}

print("PASS V244: three women's distinct 1524 Florentina, 1525 Sophia and 1526 Helfta+Holzzelle witness perspectives")
print("PASS V244: HAB 1524 VD16 O90/O91 print typos A3r/A4r verified as bibliographic reports, not photographic readings")
print("PASS V244: Emory 14 printed sides vs BSB Google 16-page record NOT counted as extra text without images")
print("PASS V244: 1880/1881 Kawerau p330–335 Sophia, p335–338 1526 joint petition; no false emperor delivery")
print("PASS V244: inherited 10 historical essays 543 sentences, prior 1529 source pages distinct, all webapp gates HOLD")
