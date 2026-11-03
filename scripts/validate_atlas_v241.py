#!/usr/bin/env python3
"""ATLAS V241 source-criticism QA.

Catalogue-attested copies and modern original-language transcriptions are not
equivalent to direct optical comparison of 1521/1525 manuscripts or 1718 pages.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
v19=load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=load("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=load("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v40=load("data/deep/atlas_v240_1519_1521_1525_documents_and_cyprian_1718_witnesses.json")
d=load("data/deep/atlas_v241_franciscan_1521_dual_print_and_sophia_1525_original_copy.json")

assert d["version"]=="2.41"
assert d["parent_commit"]=="4cd192f83514d81b7fcac9d857a7ce44500d26ff"
assert d["baseline"]=="data/deep/atlas_v240_1519_1521_1525_documents_and_cyprian_1718_witnesses.json"
assert all(flag is False for flag in d["publication_gate"].values())
m=v19["metrics"]
assert (m["chapters"],m["sections"],m["paragraphs"],m["sentences"],m["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2
assert v40["metrics"]["original_1718_print_pages_read"]==0

def rows_by_id(rows):
    ix={row["id"]:row for row in rows}
    assert len(ix)==len(rows),"duplicate evidence ID"
    return ix
sources=rows_by_id(d["sources"])
witnesses=rows_by_id(d["witnesses"])
mapping=rows_by_id(d["print_mappings"])
readings=rows_by_id(d["first_person_microreadings"])
events=rows_by_id(d["historical_events"])
reader=rows_by_id(d["reader_sections"])
issues=rows_by_id(d["open_issues"])
assert (len(sources),len(witnesses),len(mapping),len(readings),len(events),len(reader),len(issues))==(14,9,6,9,10,7,10)
assert all(s["url"].startswith("https://") and s["original_folio_or_1718_print_page_directly_seen"] is False for s in sources.values())
assert sources["AK-REQ-1297"]["read_tier"]=="COMPLETE_ACADEMY_WITNESS_CATALOGUE_AND_REGEST"
assert sources["AK-REPLY-1298"]["read_tier"]=="FULL_GERMAN_B_DRAFT_CRITICAL_TEXT_READ"
assert sources["CY-1718-I"]["url"].endswith("bsb11709870-8")
assert sources["CY-1718-II"]["url"].endswith("bsb11286923-2")
assert sources["SOPHIA-AUTO"]["url"].endswith("DE-611-HS-3409555")
assert sources["SOPHIA-COPY"]["url"].endswith("DE-611-HS-3409718")
assert not sources["SOPHIA-COPY"]["url"].endswith("3409727")
assert all(x["source_ids"] and set(x["source_ids"])<=sources.keys()
           and x["direct_physical_original_pages_read"]==0 for x in witnesses.values())
assert len([x for x in witnesses.values() if x["doc"]=="FRANCISCAN_PETITION"])==4
assert len([x for x in witnesses.values() if x["doc"]=="ELECTOR_REPLY_TO_FRANCISCANS"])==3
assert len([x for x in witnesses.values() if x["doc"]=="SOPHIA_LETTER_1525_05_03"])==2
assert witnesses["PET-A"]["role"]=="ORIGINAL_LATIN_SENT_LETTER"
assert witnesses["PET-C"]["role"]=="SPALATIN_GERMAN_TRANSLATION"
assert witnesses["PET-D"]["role"]=="COPY_OF_PET_C"
assert witnesses["REPLY-A"]["role"]=="MELANCHTHON_LATIN_DRAFT"
assert witnesses["REPLY-B"]["text_seen"]=="DIRECT_FULL_CRITICAL_EDITION_TRANSCRIPTION"
assert witnesses["REPLY-C"]["text_seen"]=="NOT_READ"
assert witnesses["SOPHIA-ORIG"]["shelfmark"]=="Gotha Chart. A 338 fol254r–256v"
assert witnesses["SOPHIA-LATER"]["shelfmark"]=="Gotha Chart. A 338 fol257r–260bv"
assert witnesses["SOPHIA-LATER"]["role"]=="EXPLICIT_LATER_COPY_OF_SOPHIA_ORIG"
assert all(x["source_witness"] in witnesses
           and set(x["support"])<=sources.keys()
           and x["printed_page_actually_visited"] is False
           and x["actual_wording_variants_collated"] is False for x in mapping.values())
assert mapping["1718-I-PET"]["source_witness"]=="PET-C"
assert mapping["1718-I-PET"]["print_range"]=="pp367–371"
assert mapping["1718-I-REPLY"]["source_witness"]=="REPLY-A"
assert mapping["1718-I-REPLY"]["print_range"]=="pp371f"
assert mapping["1718-II-PET"]["source_witness"]=="PET-A"
assert mapping["1718-II-PET"]["number"]==53
assert mapping["1718-II-REPLY"]["source_witness"]=="REPLY-C"
assert mapping["1718-II-REPLY"]["number"]==54
assert mapping["1880-SOPHIA"]["printed_full_text_indicated"] is True
assert mapping["1942-SOPHIA"]["printed_full_text_indicated"] is False
assert not any("1718" in x["id"] and x["source_witness"]=="SOPHIA-ORIG" for x in mapping.values())
proof=d["stemma_proof"]
assert proof["confirmed_copy_arrow"]["from"]=="SOPHIA-ORIG"
assert proof["confirmed_copy_arrow"]["to"]=="SOPHIA-LATER"
assert proof["confirmed_petition_C_to_D"]["from"]=="PET-C"
assert proof["confirmed_petition_C_to_D"]["to"]=="PET-D"
assert proof["unverified_any_copying_across_print_books"] is True
assert proof["no_1718_original_print_page_directly_inspected"] is True
assert all(x["witness"] in witnesses and set(x["sources"])<=sources.keys() for x in readings.values())
assert readings["M1"]["tier"]=="ACADEMY_GERMAN_REGEST_ONLY"
assert readings["M2"]["form"]=="REPORTED_SUMMARY_NOT_PRIMARY_QUOTE"
assert readings["M3"]["tier"]=="DIRECT_CRITICAL_GERMAN_ORIGINAL_LANGUAGE"
assert readings["M6"]["tier"]=="GOTHA_2025_SHORT_QUOTE_FROM_AUTHOR_AUTOGRAPH"
assert readings["M9"]["short_anchor"]=="in die inventionis Crucis"
assert events["T6"]["date"]=="1525-05-03"
assert events["T7"]["date"]=="1525-05-05"
assert all(x["source_ids"] and set(x["source_ids"])<=sources.keys() for x in events.values())
assert all(len(x["summary_ko"])>90 and set(x["source_ids"])<=sources.keys()
           and set(x["anchor_ids"])<=readings.keys() for x in reader.values())
assert len(issues)==10 and all(x["task"] for x in issues.values())
assert d["metrics"]=={
 "source_records":14,"physical_witnesses":9,"original_source_documents_distinct":3,
 "franciscan_petition_witnesses":4,"elector_reply_witnesses":3,
 "sophia_autograph_and_explicit_copy":2,"print_mappings":6,
 "first_person_microreadings":9,"chronology_events":10,
 "korean_reader_sections":7,"open_issues":10,
 "full_original_1718_print_pages_read":0,
 "original_1521_1525_gotha_folios_seen":0,
 "secondhand_official_gotha_transcription_source_read":1,
 "previous_1529_k_archive_photo_faces":2,
 "previous_1529_conversation_original_pages":4,"webapp_publications":0}
print("PASS V241: 1521 petition A/B/C/D and reply A/B/C, precise 1718 two-book editorial selections")
print("PASS V241: Sophia 1525 autograph A338 254r–256v -> explicit later copy 257r–260bv, not two independent witnesses")
print("PASS V241: 1880 complete print vs 1942 abridgment, 3 May letter vs 5 May death does not prove no reply")
print("PASS V241: critical source texts/short source quotations only; 1718 and original Gothic pages unread, HOLD")
