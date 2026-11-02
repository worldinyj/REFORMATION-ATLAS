#!/usr/bin/env python3
"""V238 documentary QA: 1690 subscription, author book plans, 1692 freight, 1693 circulation.

Passing assertions do not authenticate unpublished handwriting, infer global print
runs, infer a volume's 139th printed page, or grant rights for reproductions.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))

v19=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=read("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=read("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v37=read("data/deep/atlas_v237_gotha_jonas_accession_1691_1692_provenance.json")
d=read("data/deep/atlas_v238_seckendorff_1690_1693_subscription_and_distribution.json")

assert d["version"]=="2.38"
assert d["parent_commit"]=="550fd18cadba1e4353b470721fd33f7c791b11d6"
assert d["baseline"]=="data/deep/atlas_v237_gotha_jonas_accession_1691_1692_provenance.json"
assert all(value is False for value in d["publication_gate"].values())
m19=v19["metrics"]
assert (m19["chapters"],m19["sections"],m19["paragraphs"],
        m19["sentences"],m19["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2
assert v37["digitized_1692"]["object_id"]=="bsb10716130"

def idx(items):
    found={v["id"]:v for v in items}
    assert len(found)==len(items),"nonunique IDs"
    return found
s=idx(d["sources"])
rec=idx(d["documentary_records"])
reader=idx(d["reader_sections"])
issues=idx(d["open_issues"])
assert (len(s),len(rec),len(reader),len(issues))==(13,8,5,8)
assert all(v["url"].startswith("https://") and
           v["original_page_visually_inspected"] is False for v in s.values())
assert all(r["source_ids"] and set(r["source_ids"])<=s.keys() for r in rec.values())
assert [r["date"] for r in d["documentary_records"]]==sorted(r["date"] for r in rec.values())
assert rec["D02"]["quantity"]==69 and rec["D02"]["reichstaler"]==138
assert rec["D02"]["claim"]=="PAID_FOR_COPIES_NOT_SHIPPED_COPIES"
assert rec["D03"]["claim"]=="AUTHOR_PLAN_AND_PORTRAIT_MAKING"
assert rec["D04"]["claim"]=="FINISHED_WORK_PRESENTATION_DRAFT_NOT_PROOF_RECEIVED"
assert rec["D05"]["claim"]=="COPY_OF_RECEIPT_NOT_ORIGINAL"
assert rec["D06"]["transport_packages"]==2
assert rec["D06"]["claim"]=="TWO_BALES_NOT_TWO_BOOKS"
assert rec["D07"]["quantity"]==120
assert rec["D07"]["unit_price_reichstaler"]==4
assert rec["D07"]["total_price_reichstaler"]==480
assert rec["D07"]["quantity"]*rec["D07"]["unit_price_reichstaler"]==rec["D07"]["total_price_reichstaler"]
assert rec["D08"]["quantity"]==62
assert rec["D08"]["claim"]=="DELIVERY_MAY_OVERLAP_120_ACCOUNTED_COPIES"
assert all(v is True for v in d["quantitative_guardrails"].values())
assert d["edition_controversy"]["first_book_imprint_not_verified"] is True
assert d["edition_controversy"]["second_1694_original_imprint_not_seen"] is True
assert d["edition_controversy"]["full_title_year_1692"] is True
assert d["edition_controversy"]["complete_release_autumn_1691_source_reported"] is True
assert [r["id"] for r in d["reader_sections"]]==["R1","R2","R3","R4","R5"]
assert all(len(r["paragraph_ko"])>70 and set(r["source_ids"])<=s.keys() for r in reader.values())
assert d["metrics"]=={
    "source_records":13,
    "archival_dated_documentary_records":8,
    "author_written_letters_catalogued":2,
    "shipping_and_distribution_records":3,
    "original_historical_pages_read_this_version":0,
    "first_full_1692_book_page_139_read":0,
    "korean_reader_sections":5,
    "open_issues":8,
    "previous_archive_k_photo_faces":2,
    "previous_other_1529_handwritten_pages":4,
    "webapp_publications":0}
print("PASS V238: 1690-1693 eight archival records and thirteen explicitly ranked sources")
print("PASS V238: 69 advances != shipments, 2 bales != 2 books, 120 accounts != total print run, 62 nonadditive")
print("PASS V238: no 1692 p139, no original administrative folios, no public assets; V219 10 essays retained")
