#!/usr/bin/env python3
"""ATLAS V239: graded source relationships for Tentzel 231-folio manuscript and 1717 edited print.

This validation does not authenticate unseen early-modern original pages.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
v19=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=read("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=read("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v38=read("data/deep/atlas_v238_seckendorff_1690_1693_subscription_and_distribution.json")
d=read("data/deep/atlas_v239_tentzel_german_fair_copy_and_1717_print_reception.json")

assert d["version"]=="2.39"
assert d["parent_commit"]=="bee7b4cb88d905415ec8f3b29f8867a987a7a844"
assert d["baseline"]=="data/deep/atlas_v238_seckendorff_1690_1693_subscription_and_distribution.json"
assert all(v is False for v in d["publication_gate"].values())
m=v19["metrics"]
assert (m["chapters"],m["sections"],m["paragraphs"],m["sentences"],m["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2
assert v38["metrics"]["first_full_1692_book_page_139_read"]==0

def idx(items):
    result={x["id"]:x for x in items}
    assert len(result)==len(items),"duplicate evidence id"
    return result
sources=idx(d["sources"])
objects=idx(d["physical_objects"])
links=idx(d["editorial_links"])
reader=idx(d["reader_sections"])
issues=idx(d["open_issues"])
assert (len(sources),len(objects),len(links),len(reader),len(issues))==(13,5,4,5,9)
assert all(s["url"].startswith("https://") and s["level"] and s["note"] and s["original_manuscript_or_early_print_page_seen"] is False for s in sources.values())
assert sources["TENTZEL-MS"]["level"]=="OFFICIAL_MANUSCRIPT_CATALOGUE"
assert sources["1717-PRINT"]["level"]=="PUBLIC_DOMAIN_DIGITAL_EDITION_METADATA"
assert "1949" in sources["1949-ARTICLE"]["id"]
assert objects["MS-A648"]["kalliope"]=="DE-611-HS-4323846"
assert objects["MS-A648"]["leaves_numbered"]==231
assert objects["MS-A648"]["chapters_complete"]==13
assert objects["MS-A648"]["chapter14"]=="HEADING_ONLY"
assert objects["MS-A648"]["first_four_folios"]=="1r–53r"
assert objects["PRINT-1717"]["vd18"]=="1042170X"
assert objects["PRINT-1717"]["numbered_pages"]==531
assert objects["PRINT-1717"]["first_four_chapter_pages"]=="1–352"
assert objects["PRINT-1688"]["content_scope"]=="BOOK_I_ONLY"
assert objects["PRINT-1692"]["target_book2_page139"]=="UNREAD"
assert objects["PRINT-1694"]["exact_textual_identity_proven"] is False
assert all(o["actual_pages_read"]==0 if "actual_pages_read" in o else o["original_pages_read"]==0 for o in objects.values())
assert all(set(o["source_ids"])<=sources.keys() for o in objects.values())
assert all(k["from"] in objects and k["to"] in objects and k["variants_directly_verified"] is False and set(k["evidence_ids"])<=sources.keys() for k in links.values())
assert links["LINK-MS-PRINT"]["manuscript_chapters"]==[1,2,3,4]
assert links["LINK-MS-PRINT"]["manuscript_folios"]=="1r–53r"
assert links["LINK-MS-PRINT"]["printed_pages"]=="1–352"
assert links["LINK-PARTIAL"]["from"]=="PRINT-1688"
assert links["LINK-PARTIAL"]["to"]=="PRINT-1692"
c=d["chapter_relation"]
assert c["manuscript_numbered_folios"]==231
assert c["written_chapters"]==13 and c["chapter14_heading_only"] is True
assert c["chapters_published_in_1717"]==[1,2,3,4]
assert c["manuscript_chapters_not_verified_in_1717"]==[5,6,7,8,9,10,11,12,13]
assert c["ms_first_four_folios"]=="1r–53r" and c["edition_first_four_pages"]=="1–352"
assert c["total_print_pages"]==531
assert c["additional_179_pages_not_assigned_to_unprinted_chapters"] is True
assert c["do_not_treat_german_as_diplomatic_latin_translation"] is True
assert c["folio_images_seen"]==0 and c["print_pages_seen"]==0
bib=d["bibliographic_discrepancy"]
assert bib["first_book_1687_from_2024_gotha_research"] is True
assert bib["early_1688_imprint_from_eton_catalogue"] is True
assert bib["whether_1687_and_1688_are_same_issue"]=="UNKNOWN"
assert bib["complete_1692_imprint_distinct_from_1688_partial"] is True
assert bib["edition_1694_distinct_from_1692"] is True
assert bib["modern_1949_article_printed_pages_screens_seen"]==2
assert all(set(r["source_ids"])<=sources.keys() and len(r["text_ko"])>70 for r in reader.values())
assert all(z["question"] for z in issues.values())
assert d["metrics"]=={
 "source_records":13,"physical_witness_or_editions":5,
 "editorial_relationships":4,"manuscript_numbered_folios":231,
 "chapters_in_manuscript":13,"chapter14_heading_only":1,
 "chapters_printed_1717_from_manuscript":4,
 "chapters_not_mapped_to_1717_print":9,"korean_reader_sections":5,
 "modern_1949_paper_pages_screen_inspected":2,
 "early_original_manuscript_or_print_pages_newly_read":0,
 "seckendorff_1692_p139_directly_read":0,"open_issues":9,
 "previous_k_archival_reproduction_faces":2,
 "previous_1529_conversation_pages":4,"webapp_publications":0}
print("PASS V239: Gotha 2026 Tentzel manuscript 231 leaves, 13 written chapters and chapter14 heading only")
print("PASS V239: first four chapters MS f1r–53r -> 1717 printed pp1–352, later nine chapters unverified in 1717")
print("PASS V239: early Book I dated 1688 cannot stand in for Book II p139 1692; 1694 separate")
print("PASS V239: only 1949 modern study PDF pp446-447 images read, old manuscripts and prints 0, public HOLD")
