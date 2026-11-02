#!/usr/bin/env python3
"""V218 append-only full historical reader QA. Checks textual integrity, NOT manuscript truth."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
m=load("data/deep/atlas_v218_reader_integration_manifest.json")
v11=load("data/deep/atlas_v211_ten_reader_hus_augsburg_revision.json")
v17=load("data/deep/atlas_v217_critical_edition_passages.json")
v15=load("data/deep/atlas_v215_historical_exploration_journeys.json")
assert m["version"]=="2.18" and m["parent_commit"]=="6e47db08f853e71fbbaa57e4a08277e29b412e4f"
assert all(flag is False for flag in m["publication_gate"].values())
x=m["metrics"]
assert (x["reader_chapters"],x["original_sections"],x["new_research_sections"],x["reading_sections"])==(10,70,4,74)
assert (x["original_paragraphs"],x["new_paragraphs"],x["reading_paragraphs"])==(124,4,128)
assert (x["existing_sentences_preserved"],x["focus_anchors_preserved"],x["journey_stages_preserved"])==(522,30,30)
assert x["fully_verified_original_witnesses"]==x["expert_signoff"]==0
assert len(m["chapter_deltas"])==10 and len(m["inserts"])==4
d={x["id"]:x for x in v17["substantive_paragraph_drafts"]}
assert {z["draft_id"] for z in m["inserts"]}==set(d)
body_by_reader={}
sections=[]
preview=["# 종교개혁 ATLAS · V2.18 통합 역사 연구 원고","","**연구 초안 / 공개 금지.** 기존 V2.11 원고 10편을 완전히 보존하고 V2.17 연구 문단 4개를 해당 편의 마지막에 문헌 근거 심화 절로 통합한 읽기용 연구본입니다.",""]
for chapter in v11["chapters"]:
    key=chapter["key"]
    body=chapter["body"]
    for z in [z for z in m["inserts"] if z["reader_key"]==key]:
        draft=d[z["draft_id"]]
        assert draft["reader"]==key and draft["body_ko"]==z["inserted_body"]
        assert z["original_body_codepoints"]==len(chapter["body"])
        prefix="\n\n### "+z["heading"]+"\n"
        assert z["inserted_start_char"]==len(body)+len(prefix)
        body+=prefix+z["inserted_body"]+"\n"
        assert body[z["inserted_start_char"]:z["inserted_end_char"]]==draft["body_ko"]
        assert z["approved"] is False and z["original_sixteenth_century_witness_directly_collated"] is False
        assert z["source_status"]=="LATER_CRITICAL_EDITION_OR_CATALOGUE"
        assert z["original_language_sources"]
    delta=next(x for x in m["chapter_deltas"] if x["reader_key"]==key)
    assert len(body)==delta["new_codepoints"]
    assert len(chapter["body"])==delta["old_codepoints"]
    assert body.startswith(chapter["body"])
    body_by_reader[key]=body
    preview+=["---","","## "+chapter["title"],"",body,""]
preview+=["## 역사 연구 단계와 자료의 제한","","1858년 인쇄 비평판 지면 확인은 1531년이나 1540년 원본의 판면 교감과 다릅니다. 마르부르크 합의문은 GHDI 편집 전사와 취리히 원본 소장기록을 구분합니다. 후스의 원어 시작 구절은 학술 목록 수준으로 확인했으며, 본문 전체를 판독하지 않았습니다.",""]
content=(R/"docs/01_CONTENT/V218_TEN_READER_HISTORICAL_CRITICAL_TEXT_PREVIEW.md").read_text(encoding="utf-8")
assert content=="\n".join(preview)
for s in v11["sentences"]:
    body=body_by_reader[s["reader_key"]]
    assert body[s["start_char"]:s["end_char"]].startswith(s["excerpt"])
for a in v11["focus_anchors"]:
    assert body_by_reader[a["reader_key"]][a["start_char"]:a["end_char"]]==a["exact_excerpt"]
old_sent={z["id"]:z for z in v11["sentences"]}
for stage in v15["stages"]:
    old=old_sent[stage["v211_reader_sentence_id"]]
    assert body_by_reader[stage["reading_reader_key"]][old["start_char"]:old["end_char"]].startswith(stage["v211_excerpt"])
assert len([x for x in m["chapter_deltas"] if x["added_sections"]>0])==3
print("PASS V218: ten full reader chapters, four substantive appended paragraphs, all 522 prior sentences and 30 focus links preserved; publication HOLD")
