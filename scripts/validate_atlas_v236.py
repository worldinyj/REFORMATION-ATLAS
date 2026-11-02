#!/usr/bin/env python3
"""V236 review gates: two 17c Jonas copies, Monday date and indirect Latin praise.

No scanned original or CR printed column is certified by this validator.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
v19=load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=load("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=load("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
v35=load("data/deep/atlas_v235_osiander_jonas_julian_weekday_eyewitness_comparison.json")
d=load("data/deep/atlas_v236_jonas_1529_letter_double_copy_and_textual_transmission.json")

assert d["version"]=="2.36"
assert d["parent_commit"]=="71fc367b927a5c387e4103da642df3c04eb4f0c5"
assert d["baseline"]=="data/deep/atlas_v235_osiander_jonas_julian_weekday_eyewitness_comparison.json"
assert all(value is False for value in d["publication_gate"].values())
assert (v19["metrics"]["chapters"],v19["metrics"]["sections"],v19["metrics"]["paragraphs"],
        v19["metrics"]["sentences"],v19["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2
assert v35["metrics"]["new_original_manuscript_pages_read"]==0
assert v35["weekday_correction"]["normalized_date"]=="1529-10-04"

def ix(rows):
    result={x["id"]:x for x in rows}
    assert len(result)==len(rows),"duplicate evidence ID"
    return result
sources=ix(d["sources"])
objects=ix(d["witness_objects"])
latin=ix(d["latin_anchors"])
checks=ix(d["interpretive_checks"])
chapters=ix(d["reader_draft"]["chapters"])
assert (len(sources),len(objects),len(latin),len(checks),len(chapters))==(11,5,3,6,5)
assert all(x["url"].startswith("https://") and x["original_image_read"] is False for x in sources.values())
assert sources["A453"]["access"]=="DIRECT_ARCHIVAL_HTML"
assert sources["A453"]["url"].endswith("DE-611-HS-4254434")
assert not sources["A453"]["url"].endswith("4254430")
assert sources["B28"]["access"]=="DIRECT_ARCHIVAL_HTML"
assert sources["FUDGE1997"]["access"]=="DIRECT_PDF_TEXT_AND_PAGE0_SCREENSHOT_PROOFREAD"
assert sources["SECKENDORFF1692"]["access"]=="2024_DRESDEN_CHURCH_ARCHIVE_LIBRARY_CATALOGUE_NOT_1692_TEXT"
assert all(x["source_id"] in sources and x["image_read"] is False for x in objects.values())
assert objects["COPY-A453"]["shelfmark"]=="Chart. A 453, Bl. 24v–25v"
assert objects["COPY-A453"]["copy_century"]==17
assert objects["COPY-A453"]["dated_formula_in_catalogue"]=="Lunae post Michaelis"
assert objects["COPY-A453"]["is_contemporary_original"] is False
assert objects["COPY-B28"]["shelfmark"]=="Chart. B 28, Bl. 41v–43r"
assert objects["COPY-B28"]["copyist"]=="Konrad Meusel"
assert objects["COPY-B28"]["is_contemporary_original"] is False
assert objects["COPY-B28"]["aquila_title_mentioned"] is True
assert objects["COPY-B28"]["aquila_controlled_role"]=="Bezug [nicht dokumentiert]"
assert objects["COPY-A453"]["addressee_confirmed"]=="Wilhelm Reiffenstein"
assert objects["COPY-B28"]["addressee_confirmed"]=="Wilhelm Reiffenstein"
assert objects["PRINT-1692"]["reference"]=="Lib. II, Sect. 17, § XLVII, Additio, S. 139f"
assert objects["PRINT-1834-JONAS"]["reference"]=="CR I col. 1097, Nr. 634"
assert objects["PRINT-1834-MEL"]["reference"]=="CR I col. 1106f, Nr. 639"
assert latin["JONAS-OCOL"]["quote"]=="in Oecolampadio mira bonitas naturae et clementia"
assert latin["JONAS-DATE"]["quote"]=="Lunae post Michaelis"
assert latin["JONAS-MONDAY"]["quote"]=="Hodie, die lunae"
assert sum(x["words"] for x in latin.values())==13
assert all(len(x["quote"].split())==x["words"] and x["source_id"] in sources
           and x["original_manuscript_spelling_confirmed"] is False for x in latin.values())
assert len(d["open_issues"])==8
assert all(x["support_ids"] and set(x["support_ids"])<=sources.keys() for x in checks.values())
assert checks["TWO-COPIES"]["status"]=="PHYSICAL_DISTINCTION_CERTAIN_GENEALOGY_UNKNOWN"
assert set(chapters)=={1,2,3,4,5}
assert all(x["title"] and x["body"] for x in chapters.values())
assert d["metrics"]=={
"source_records":11,"archival_jonas_copy_objects_newly_added":1,
"archival_jonas_copy_objects_total":2,"source_witness_or_edition_objects":5,
"indirect_latin_anchors":3,"brief_quotes_total_words":13,
"interpretive_checks":6,"reader_chapters":5,"unresolved":8,
"direct_original_1529_letter_pages_read":0,"original_17c_letter_copy_images_read":0,
"direct_1692_or_1834_print_pages_read":0,"previous_k_official_photo_faces":2,
"previous_1529_other_ms_pages":4,"published_items":0}
print("PASS V236: two distinct Gotha 17c copies not two independent eyewitnesses")
print("PASS V236: Jonas praise via 1997 article p268; indirect text only; Aquila recipient ambiguity")
print("PASS V236: CR I 1097 / 1106f are columns, not scanned PDF page indices; original-read gates HOLD")
