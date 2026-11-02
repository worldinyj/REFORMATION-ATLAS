#!/usr/bin/env python3
"""V232 Marburg source-critical chronology QA.

Checks attribution and provenance flags only; does NOT verify historical autography
independently and does NOT upgrade OCR or archive entries to visual readings.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
corpus=load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=load("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v31=load("data/deep/atlas_v231_wa1910_critical_edition_and_marburg_witness_apparatus.json")
d=load("data/deep/atlas_v232_marburg_1529_documentary_chronology_melanchthon_autograph.json")
assert d["version"]=="2.32"
assert d["parent_commit"]=="4ef66e3895721fa09c91f4d141c2108cdb013915"
assert d["baseline_dataset"]=="data/deep/atlas_v231_wa1910_critical_edition_and_marburg_witness_apparatus.json"
assert all(v is False for v in d["publication_gate"].values())
assert (corpus["metrics"]["chapters"],corpus["metrics"]["sections"],corpus["metrics"]["paragraphs"],corpus["metrics"]["sentences"],corpus["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v31["metrics"]["printed_1910_images_seen"]==0
assert v31["metrics"]["original_zk_collations"]==0
def idx(a):
    x={row["id"]:row for row in a}
    assert len(x)==len(a),"repeated ID"
    return x
s=idx(d["sources"]);docs=idx(d["documents"]);events=idx(d["chronology"])
dist=idx(d["evidence_distinctions"]);attempts=idx(d["external_image_access_attempts"])
issues=idx(d["open_issues"])
reader=idx(d["reader_edition_ko"]["sections"])
assert (len(s),len(docs),len(events),len(dist),len(attempts),len(issues),len(reader))==(11,5,6,4,3,6,3)
assert all(x["url"].startswith("https://") for x in s.values())
assert s["SRC-V232-WLB-2018"]["published_year"]==2018
assert s["SRC-V232-WLB-2018"]["evidence_level"]=="SCHOLARLY_PDF_TEXT_READ_NOT_MANUSCRIPT_ORIGINAL_IMAGE"
assert docs["DOC-V232-WLB826"]["shelfmark"]=="Cod. hist. 2° 889–26, fol. 36r–36v"
assert docs["DOC-V232-WLB826"]["physical_original_scholarly_identified"] is True
assert docs["DOC-V232-WLB826"]["claimed_1529_handwritten_original"] is True
assert docs["DOC-V232-GOTHA832"]["claimed_1529_handwritten_original"] is False
assert docs["DOC-V232-GOTHA-JONAS"]["claimed_1529_handwritten_original"] is False
assert docs["DOC-V232-GOTHA832"]["handwriting"].startswith("Konrad Meusel")
assert docs["DOC-V232-MBW825"]["inscribed_date"]=="1529-10-03"
assert docs["DOC-V232-MBW825"]["signing_date_interpreted_by_mbw"]=="1529-10-04"
for obj in docs.values():
    assert obj["source_ids"] and set(obj["source_ids"])<=s.keys()
    assert obj["original_source_not_seen"] is True
for e in events.values():
    assert e["date_window"][0]<=e["date_window"][1]
    assert e["source_ids"] and set(e["source_ids"])<=s.keys()
    assert set(e["document_ids"])<=docs.keys()
assert events["EVENT-V232-3"]["claim_type"]=="TWO_DATE_FIELDS_NOT_SINGLE_EVENT_TIMESTAMP"
assert events["EVENT-V232-5"]["date_window"]==["1529-10-04","1529-10-05"]
assert events["EVENT-V232-6"]["date_window"]==["1529-10-16","1529-10-17"]
assert all(x["source_ids"] and set(x["source_ids"])<=s.keys() and x["no_historical_final_adjudication"] for x in dist.values())
assert all(x["source_ids"] and set(x["source_ids"])<=s.keys() and x["bytes_downloaded"]==0 and x["original_print_pages_seen"]==0 for x in attempts.values())
assert all(x["status"]=="OPEN" and x["question"] for x in issues.values())
assert all(x["source_ids"] and set(x["source_ids"])<=s.keys() for x in reader.values())
assert d["metrics"]=={
    "new_1529_autograph_exemplar_located":1,
    "new_original_1529_images_read":0,
    "new_editorial_regest_sources":6,
    "source_records":11,
    "dated_events":6,
    "document_objects":5,
    "source_critical_distinctions":4,
    "open_issues":6,
    "old_unique_1529_conversation_images_retained":4,
    "wa1910_print_pages_proofread":0,
    "k_z_signed_witness_pages_proofread":0,
    "published_items":0}
print("PASS V232: WLB original Melanchthon 4/5 Oct autograph correctly distinguished from Gotha later copies")
print("PASS V232: inscribed Oct3 vs signing Oct4 MBW, Oct16-17 later reports; 1910 scan proofread=0; hold")
