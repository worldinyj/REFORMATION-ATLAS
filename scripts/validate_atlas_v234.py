#!/usr/bin/env python3
"""V234: actual 2017 archive photo of 1529 K; 15 historical articles still edited 1910 text."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
v19=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=read("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v33=read("data/deep/atlas_v233_mbw826_indirect_latin_folio_autography_and_mbw825_k_index.json")
d=read("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
assert d["version"]=="2.34"
assert d["parent_commit"]=="754b17e4eed61c89d4bdbbeb0208ef400ad0e216"
assert d["baseline"]=="data/deep/atlas_v233_mbw826_indirect_latin_folio_autography_and_mbw825_k_index.json"
assert all(x is False for x in d["publication_gate"].values())
assert (v19["metrics"]["chapters"],v19["metrics"]["sections"],v19["metrics"]["paragraphs"],v19["metrics"]["sentences"],v19["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v33["metrics"]["new_primary_pages_read"]==0
def unique(rows):
    out={z["id"]:z for z in rows}
    assert len(out)==len(rows), "duplicate source or evidence ID"
    return out
src=unique(d["sources"]); faces=unique(d["k_image"]["face_descriptions"])
assert len(src)==8
assert all(s["url"].startswith("https://") for s in src.values())
assert src["HESSEN2017"]["level"]=="PDF_SCREEN_PAGENO9_DIRECT_VISUAL"
assert src["GHDI1910"]["level"]=="FULL_EDITORIAL_HTML_READ"
img=d["k_image"]
assert img["source"]=="HESSEN2017"
assert img["shelfmark"]=="Hessisches Staatsarchiv Marburg Best. 3 Nr.245 fol.60r–64v"
assert img["pdf_index"]==9 and img["printed_page"]==10
assert img["faces_reproduced_and_visually_inspected"]==2
assert img["actual_archive_iiif_folios_read"]==0
assert img["image_in_github"] is False and img["rights_unreviewed"] is True
assert set(faces)=={"FACE_A","FACE_B"}
assert all(z["exact_original_folio_from_caption"] is None
           and z["full_text_read"] is False
           and z["article_7_13_15_read"] is False for z in faces.values())
names=d["signatories"]
assert len(names)==10 and len(set(n["name_normalized"] for n in names))==10
assert [n["order"] for n in names]==list(range(1,11))
assert all(n["image_visualized"] is True and n["exact_spelling_diplomatically_proofread"] is False for n in names)
assert names[0]["name_normalized"]=="Martin Luther"
assert names[6]["name_normalized"]=="Johannes Oecolampadius"
assert names[7]["name_normalized"]=="Huldrych Zwingli"
articles=d["articles"]
assert len(articles)==15
assert [a["article"] for a in articles]==list(range(1,16))
assert len({a["title_ko"] for a in articles})==15
assert all(len(a["explanation_ko"])>=20 for a in articles)
assert all(a["evidence"]=="GHDI edited WA30/3 (1910) pp160–171" for a in articles)
assert all(a["original_k_article_read"] is False
           and a["original_z_article_read"] is False
           and a["publication_approved"] is False for a in articles)
assert [a["article"] for a in articles if a["reported_z_addition"]]==[7,13,15]
assert "임재" in articles[-1]["explanation_ko"]
bridges=unique(d["bridges"])
assert len(bridges)==4
assert set(x for b in bridges.values() for x in b["articles"])=={1,2,3,4,5,6,7,8,9,10,11,13,15}
assert bridges["BRIDGEVAR"]["articles"]==[7,13,15]
assert d["cr1834"]["actual_page_image_read"] is False
assert len(d["open_issues"])==6
assert d["metrics"]=={
"source_records":8,"official_k_1529_original_photographed_faces_visually_read":2,
"official_2017_pages_read":1,"new_korean_article_summaries":15,
"signature_names_crosschecked":10,"thematic_bridges":4,
"original_k_iiif_folios_read":0,"kz_7_13_15_direct_collations":0,
"cr1834_letter_pages_read":0,"prior_distinct_1529_conversation_pages":4,
"published_items":0}
print("PASS V234: Hessen archival publication p10 original K autograph photo TWO faces visually seen")
print("PASS V234: 15 original Korean article readers from GHDI WA1910; ALL K/Z variant and media rights HOLD")
print("PASS V234: 10 person signature labels corroborated; distinct previous 4 original conversation pages retained")
