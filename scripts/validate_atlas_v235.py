#!/usr/bin/env python3
"""ATLAS V235: historical Julian weekday and four witnesses cross-validation.

This is a source-evidence integrity check, NOT authentication of original handwriting.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
v19=load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=load("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v34=load("data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json")
d=load("data/deep/atlas_v235_osiander_jonas_julian_weekday_eyewitness_comparison.json")
assert d["version"]=="2.35"
assert d["parent_commit"]=="39512e84376bba2f67a64d669973be99e8ff3141"
assert d["baseline"]=="data/deep/atlas_v234_k_two_original_photo_faces_and_15_article_korean_reader.json"
assert d["publication_hold"] is True
assert all(x is False for x in d["publication_gate"].values())
assert (v19["metrics"]["chapters"],v19["metrics"]["sections"],v19["metrics"]["paragraphs"],v19["metrics"]["sentences"],v19["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v34["metrics"]["official_k_1529_original_photographed_faces_visually_read"]==2

def julian_weekday(year,month,day):
    # Astronomical Julian day number for Julian calendar (not Gregorian datetime).
    a=(14-month)//12
    y=year+4800-a
    m=month+12*a-3
    jdn=day+(153*m+2)//5+365*y+y//4-32083
    return ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"][jdn%7]

assert len(d["julian_dates"])==6
for v in d["julian_dates"]:
    year,month,day=map(int,v["date"].split("-"))
    assert (year,month)==(1529,9) or (year,month)==(1529,10)
    assert julian_weekday(year,month,day)==v["day"],v
assert {x["date"]:x["day"] for x in d["julian_dates"]}["1529-10-04"]=="Monday"
assert julian_weekday(1529,10,5)=="Tuesday"
assert julian_weekday(1529,10,2)=="Saturday"

src={x["id"]:x for x in d["sources"]}
assert len(src)==len(d["sources"])==10
assert all(x["url"].startswith("https://") and x["autograph_folio_seen"] is False for x in src.values())
w=d["weekday_correction"]
assert w["original"]=="Am montag"
assert w["original_has_numeric_day"] is False
assert w["modern_edition_bracket"]=="[5. Oktober]"
assert w["normalized_date"]=="1529-10-04"
assert w["jonas_scholarly_quote"]=="Hodie, die lunae [4. Oktober]"
assert set(w["evidence_ids"])<=src.keys()
assert "Modern editorial" in w["provenance"]
assert len(d["witnesses"])==4
assert {x["id"] for x in d["witnesses"]}=={"osiander","jonas","melanchthon","zwingli"}
assert all(set(x["source_ids"])<=src.keys() for x in d["witnesses"])
assert next(x for x in d["witnesses"] if x["id"]=="osiander")["earlier_recollections_secondhand"] is True
assert len(d["axes"])==5 and len({x["id"] for x in d["axes"]})==5
assert len(d["hessian_participants"])==5
assert next(x for x in d["hessian_participants"] if x["id"]=="lambert")["status"]=="POSSIBLE_ATTENDANCE"
assert len(d["reader_chapters"])==5
assert len(d["open_issues"])==6
assert d["metrics"]=={
 "sources":10,"julian_dates":6,"editorial_date_corrections":1,
 "witness_accounts":4,"collation_axes":5,"local_historiographic_people":5,
 "reader_chapters":5,"new_original_manuscript_pages_read":0,
 "previous_k_photo_faces":2,"previous_other_1529_original_pages":4,
 "open_issues":6,"published_items":0}
print("PASS V235: Julian-calendar Mon 4 Oct, Tue 5 Oct; Osiander original 'Am montag' != editorial [5 Oct]")
print("PASS V235: Jonas 4 Oct short quote indirect scholarly source, four witnesses, five local names graded")
print("PASS V235: original K/Z and CR1834 read=0, earlier 2+4 reproduction/other manuscript pages retained; HOLD")
