#!/usr/bin/env python3
"""Rebuild V219 structured ten-reader historical text and verify exact Unicode anchors.
Passing CI checks data structure only, NOT historical truth or 16c witness collation.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rd(p):return json.loads((R/p).read_text(encoding="utf-8"))
x=rd("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v11=rd("data/deep/atlas_v211_ten_reader_hus_augsburg_revision.json")
v17=rd("data/deep/atlas_v217_critical_edition_passages.json")
v18=rd("data/deep/atlas_v218_reader_integration_manifest.json")
v15=rd("data/deep/atlas_v215_historical_exploration_journeys.json")
assert x["version"]=="2.19" and x["ancestry"]["parent_commit"]=="4bffe5b645c1522f399b8b714922008d6d55a696"
assert all(value is False for value in x["publication_gate"].values())
m=x["metrics"]
assert (m["chapters"],m["sections"],m["paragraphs"],m["preserved_v211_sentences"],m["preserved_v211_focus_anchors"],m["journey_stage_bridges"],m["added_critical_sections"])==(10,74,128,522,30,30,4)
assert m["sentences"]==len(x["sentences"])==m["preserved_v211_sentences"]+m["added_sentences"]
assert m["original_16c_folios_collated"]==m["expert_signoffs"]==m["public_app_items"]==0
old={c["key"]:c for c in v11["chapters"]}
new={c["key"]:c for c in x["chapters"]}
draft={z["id"]:z for z in v17["substantive_paragraph_drafts"]}
assert len(new)==len(old)==10
nav={n["reader_key"]:n["sections"] for n in x["sections"]}
para={p["id"]:p for p in x["paragraphs"]}
sent={s["id"]:s for s in x["sentences"]}
assert len(para)==128
old_sent={s["id"]:s for s in v11["sentences"]}
for key,orig in old.items():
    body=orig["body"]
    additions=[z for z in v18["inserts"] if z["reader_key"]==key]
    for z in additions:
        assert draft[z["draft_id"]]["body_ko"]==z["inserted_body"]
        prefix="\n\n### "+z["heading"]+"\n"
        assert z["inserted_start_char"]==len(body)+len(prefix)
        body+=prefix+z["inserted_body"]+"\n"
        assert body[z["inserted_start_char"]:z["inserted_end_char"]]==z["inserted_body"]
    assert body==new[key]["body"] and body.startswith(orig["body"])
    cursor=0
    for s in nav[key]:
        assert s["start_char"]==cursor and s["end_char"]>cursor
        assert s["publication_approved"] is False
        cursor=s["end_char"]
    assert cursor==len(body)
    assert len(nav[key])==len(next(n for n in v11["sections"] if n["reader_key"]==key)["sections"])+len(additions)
    assert x["per_reader_checks"][key]["codepoints_integrated"]==len(body)
    assert new[key]["review_status"]=="PENDING"
assert m["full_integrated_codepoints"]==sum(len(z["body"]) for z in new.values())
for p in para.values():
    assert new[p["reader_key"]]["body"][p["start_char"]:p["end_char"]]==p["text_exact"]
    assert p["section_id"] in {s["id"] for s in nav[p["reader_key"]]}
    assert p["publication_approved"] is False
for s in sent.values():
    text=new[s["reader_key"]]["body"][s["start_char"]:s["end_char"]]
    assert len(text)==s["codepoints"] and text[:110]==s["excerpt"]
    p=para[s["passage_id"]]
    assert p["reader_key"]==s["reader_key"] and p["section_id"]==s["section_id"]
    assert p["start_char"]<=s["start_char"]<s["end_char"]<=p["end_char"]
    assert s["source_original_witness_checked"] is False and s["expert_approved"] is False and s["can_publish"] is False
    if s["source_v211_sentence_id"]:
        old_s=old_sent[s["source_v211_sentence_id"]]
        assert (s["reader_key"],s["start_char"],s["end_char"],s["excerpt"])==(old_s["reader_key"],old_s["start_char"],old_s["end_char"],old_s["excerpt"])
    else: assert s["source_v217_draft_id"] in draft
for p in para.values():
    units=sorted((s for s in sent.values() if s["passage_id"]==p["id"]),key=lambda z:z["start_char"])
    assert units
    cursor=p["start_char"]
    for s in units:
        assert not new[p["reader_key"]]["body"][cursor:s["start_char"]].strip()
        cursor=s["end_char"]
    assert not new[p["reader_key"]]["body"][cursor:p["end_char"]].strip()
assert sum(s["source_v211_sentence_id"] is not None for s in sent.values())==522
original_anchors={a["id"]:a for a in v11["focus_anchors"]}
for a in x["focus_anchors"]:
    oa=original_anchors[a["source_v211_anchor_id"]]
    assert (a["reader_key"],a["start_char"],a["end_char"],a["exact_excerpt"])==(oa["reader_key"],oa["start_char"],oa["end_char"],oa["exact_excerpt"])
    assert new[a["reader_key"]]["body"][a["start_char"]:a["end_char"]]==a["exact_excerpt"]
    assert a["id"] in sent[a["source_sentence_id"]]["v219_focus_anchor_ids"]
assert len(x["v215_stage_sentence_bridge"])==len(v15["stages"])==30
stage={s["id"]:s for s in v15["stages"]}
for z in x["v215_stage_sentence_bridge"]:
    s=stage[z["v215_stage_id"]]
    assert z["source_v211_sentence_id"]==s["v211_reader_sentence_id"]
    current=sent[z["v219_sentence_id"]]
    assert current["source_v211_sentence_id"]==s["v211_reader_sentence_id"]
    assert new[s["reading_reader_key"]]["body"][current["start_char"]:current["end_char"]].startswith(s["v211_excerpt"])
    assert z["offset_shift"] is False and z["can_publish"] is False
assert len(x["source_notes"])==4
assert all(n["original_sixteenth_century_witness_collated"] is False and n["can_publish"] is False for n in x["source_notes"])
preview=["# 종교개혁 ATLAS V2.19 · 10편 구조화 연구 독자 원고","","> 1858년 비평판과 문헌 목록의 범위에서 연구한 내용이며 출판 보류 상태입니다."]
for c in x["chapters"]:preview+=["---","",c["body"],""]
preview+=["## 공개 제한","16세기 원전 사본·원본 인쇄판의 직접 교감 및 학술 전문가 승인 미완료."]
assert (R/"docs/01_CONTENT/V219_TEN_READER_STRUCTURED_RESEARCH_PREVIEW.md").read_text(encoding="utf-8")=="\n".join(preview)
print(f"PASS V219: 10 readers, 74 sections, 128 paragraphs, {m['sentences']} sentence indices, 30 focus + 30 stage links, publication HOLD")
