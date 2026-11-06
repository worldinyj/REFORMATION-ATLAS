#!/usr/bin/env python3
"""V3.07 reader, source-scope, catalogue and 97-overview-gap check.

No existing research files are modified. Passing means structural/editorial
consistency, not historical expert approval or primary-text collation.
"""
import collections
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC="docs/01_CONTENT/V307_REMAINING_OVERVIEW_MEDIUM_READERS.md"
FILE="data/deep/atlas_v307_remaining_overview_medium_readers.json"
V305="data/deep/atlas_v305_medium_depth_pietism_revival_readers.json"
X304="data/contracts/atlas_v304_overview_medium_reading_crosswalk.json"

def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))

def git_blob_sha(path):
    raw=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def validate():
    d=load(FILE);v305=load(V305);x304=load(X304);doc=(ROOT/DOC).read_text(encoding="utf-8")
    assert (d["version"],d["status"],d["depth"])==("3.07","DRAFT","MEDIUM")
    assert d["publication_gate"] and all(flag is False for flag in d["publication_gate"].values())
    assert d["preserved_inputs"]==[
        {"path":V305,"git_blob_sha1":"09b2c19ca4c3f2ad1a98cc9053f8aee584c27fbb"},
        {"path":X304,"git_blob_sha1":"d5008fe0c721e4f1ad6b1dbc1ceb8c4fd16a6038"},
    ]
    for p in d["preserved_inputs"]:
        assert git_blob_sha(p["path"])==p["git_blob_sha1"],p["path"]
    old=v305["catalogue"];cat=d["catalogue"];chap=d["chapters"];src=d["sources"]
    assert len(old)==495 and len(cat)==513 and cat[:495]==old
    assert len(chap)==18 and len(src)==26
    assert len({c["id"] for c in cat})==513
    assert collections.Counter(c["id"].split("-")[0] for c in chap)=={
        "PERSON":6,"EVENT":8,"DOCUMENT":2,"THEME":2}
    assert len({s["id"] for s in src})==len(src)
    catids={r["id"] for r in cat};srcids={s["id"] for s in src}
    assert {c["id"] for c in chap}.isdisjoint({r["id"] for r in old})
    used=set()
    existing_bodies={s["body"] for c in v305["chapters"] for s in c["sections"]}
    allbodies=set(existing_bodies)
    for i,c in enumerate(chap):
        assert cat[495+i]=={"id":c["id"],"title":c["title"],"summary":c["lead"],
            "dataset":FILE,"chapter_index":i,"reader_document":DOC,"section_count":3}
        assert c["lead"] and c["reading_question"].endswith("?")
        assert len(c["sections"])==3 and len(c["sources"])>=1
        assert len(c["related_readers"])>=2 and len(set(c["related_readers"]))==len(c["related_readers"])
        assert c["id"] not in c["related_readers"] and set(c["related_readers"])<=catids
        assert set(c["sources"])<=srcids
        assert c["source_basis_status"]=="SCOPED_PUBLIC_SOURCE_CHECK_NO_ORIGINAL_IMAGE"
        used.update(c["sources"])
        assert doc.count("### "+str(i+1)+". "+c["title"]+"\n")==1,c["id"]
        for sec in c["sections"]:
            assert sec["heading"] and len(sec["body"])>=110
            assert sec["body"] not in allbodies,"full duplicate section: "+c["id"]
            allbodies.add(sec["body"])
            assert doc.count("#### "+sec["heading"]+"\n")>=1
            assert doc.count(sec["body"])==1,("document drift",c["id"])
        assert doc.count("**독서 질문:** "+c["reading_question"])==1,c["id"]
    assert used==srcids,("unused sources",list(srcids-used))
    for s in src:
        assert s["url"].startswith("https://") and s["scope"] and s["inspection_note"]
        assert s["checked_on"]=="2026-11-06"
        assert s["inspection_level"]=="PUBLIC_LANDING_PAGE_OR_SEARCH_EXCERPT"
        assert s["original_image_read"] is False
        assert s["url"] in doc
    current={r["overview_id"]:r for r in x304["entries"]}
    assert len(current)==97
    for u in v305["overview_link_updates"]:
        row=current[u["overview_id"]]
        assert row["mapping_status"]=="NO_MATCH"
        current[u["overview_id"]]=dict(row,mapping_status=u["new_status"])
    before=collections.Counter(row["mapping_status"] for row in current.values())
    assert dict(before)=={"DIRECT_TOPIC":64,"PARTIAL_COVERAGE":14,
                          "BACKGROUND_ONLY":1,"NO_MATCH":18}
    updates=d["overview_link_updates"]
    assert len(updates)==18 and len({u["overview_id"] for u in updates})==18
    assert {u["overview_id"] for u in updates}=={id for id,row in current.items() if row["mapping_status"]=="NO_MATCH"}
    for u in updates:
        row=current[u["overview_id"]]
        assert row["title"]==u["overview_title"]
        assert u["previous_status"]=="NO_MATCH" and u["new_status"] in ("DIRECT_TOPIC","PARTIAL_COVERAGE")
        assert u["reader_id"] in {c["id"] for c in chap} and u["scope"]
        assert doc.count("| "+u["overview_id"]+" | "+u["overview_title"]+" | "+u["new_status"]+" |")==1
        current[u["overview_id"]]=dict(row,mapping_status=u["new_status"])
    after=collections.Counter(row["mapping_status"] for row in current.values())
    assert all(after[key]==value for key,value in {
        "DIRECT_TOPIC":78,"PARTIAL_COVERAGE":18,
        "BACKGROUND_ONLY":1,"NO_MATCH":0}.items())
    assert d["coverage_projection"]=={
        "before":{"DIRECT_TOPIC":64,"PARTIAL_COVERAGE":14,"BACKGROUND_ONLY":1,"NO_MATCH":18},
        "after":{"DIRECT_TOPIC":78,"PARTIAL_COVERAGE":18,"BACKGROUND_ONLY":1,"NO_MATCH":0},
        "actual_app_updated":False}
    assert sum(after.values())==97
    assert {u["overview_id"] for u in updates if u["new_status"]=="PARTIAL_COVERAGE"}=={
        "OV-E-001","OV-D-019","TOP-09","TOP-10"}
    m=d["metrics"];assert m=={
        "new_readers":18,"new_sections":54,"new_questions":18,
        "previous_readers":495,"total_medium_readers":513,"source_records":26,
        "new_body_characters":sum(len(s["body"]) for c in chap for s in c["sections"]),
        "new_overview_links":18,"new_original_image_readings":0}
    assert "원판" in doc and "실제 AI Studio" in doc
    print("V3.07 PASS: 18 readers / 54 sections / 26 scoped source records / 513 catalogue IDs")
    print("V3.07 GAP PROJECTION: 78 direct / 18 partial / 1 background / 0 no match; HOLD")

if __name__=="__main__":
    validate()
