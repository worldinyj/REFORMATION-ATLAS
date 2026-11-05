#!/usr/bin/env python3
"""Validate V3.01 editorial additions and render their Korean reading document."""
import argparse, collections, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA='data/deep/atlas_v301_medium_depth_precursors_hussite_readers.json'
DOC='docs/01_CONTENT/V301_PRECURSORS_HUSSITE_MEDIUM_READERS.md'
def load(path):return json.loads((ROOT/path).read_text())
def validate(d):
    assert d['version']=='3.01' and d['depth']=='MEDIUM' and d['status']=='DRAFT'
    assert d['parent_commit']=='cc04e7db4aad6af34c1c184ec37e03dd679a5949'
    assert all(v is False for v in d['publication_gate'].values())
    for item in d['preserved_inputs']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
    prior=load(d['preserved_inputs'][0]['path'])['catalogue']; chapters=d['chapters']; cat=d['catalogue']
    assert cat[:435]==prior and len(cat)==455 and len(chapters)==20
    allids={x['id'] for x in cat}; newids={x['id'] for x in chapters}; sids={s['id']for s in d['sources']}
    assert len(allids)==455 and len(newids)==20 and not newids&{x['id']for x in prior}
    assert len(sids)==len(d['sources'])==24
    assert collections.Counter(x['id'].split('-')[0]for x in chapters)=={'PERSON':8,'EVENT':6,'DOCUMENT':6}
    used=set(); bodies=set()
    for index,c in enumerate(chapters):
        assert len(c['sections'])==3 and c['reading_question'].endswith('?') and c['lead']
        assert c['sources'] and set(c['sources'])<=sids;used.update(c['sources'])
        assert len(c['related_readers'])==3 and set(c['related_readers'])<=allids
        assert c['id'] not in c['related_readers'] and len(set(c['related_readers']))==3
        for s in c['sections']:
            assert s['heading'] and len(s['body'])>=120
            assert s['body'] not in bodies; bodies.add(s['body'])
        assert cat[435+index]==dict(id=c['id'],title=c['title'],summary=c['lead'],dataset=DATA,chapter_index=index,reader_document=DOC,section_count=3)
    assert used==sids
    for s in d['sources']:assert s['url'].startswith('https://') and s['scope'] and s['inspection_note'] and s['checked_on']=='2026-11-05'
    x=load('data/contracts/atlas_v300_overview_medium_reading_crosswalk.json')
    old={r['overview_id']:r for r in x['entries']}; before=collections.Counter(r['mapping_status']for r in x['entries']);after=before.copy()
    updates=d['overview_link_updates'];assert len({r['overview_id']for r in updates})==12
    for r in updates:
        assert old[r['overview_id']]['mapping_status']==r['previous_status']
        assert old[r['overview_id']]['title']==r['overview_title']
        assert r['new_status']=='DIRECT_TOPIC' and r['reader_id']in newids
        after[r['previous_status']]-=1;after['DIRECT_TOPIC']+=1
    assert d['coverage_projection']['before']==dict(before) and d['coverage_projection']['after']==dict(after)
    assert sum(after.values())==97 and after=={'DIRECT_TOPIC':38,'PARTIAL_COVERAGE':12,'BACKGROUND_ONLY':1,'NO_MATCH':46}
    assert d['metrics']==dict(new_readers=20,new_sections=60,new_questions=20,previous_readers=435,total_medium_readers=455,source_records=24,new_body_characters=sum(len(s['body'])for c in chapters for s in c['sections']),new_overview_direct_links=12,new_original_image_readings=0)
def render(d):
    m=d['metrics']; lines=['# V3.01 선구자·후스파 심화 읽기','','상태: DRAFT · 중간 수준 · 공개 보류','','인물 8편·사건 6편·문헌 6편을 추가했다. 누적 집필 목록은 435→455편이다. 새 본문은 '+str(m['new_body_characters'])+'자, 60절과 독서 질문 20개이며 출처 기록은 24건이다. 기존 편집 전달본과 검토 UI는 435편으로 유지한다. 실제 AI Studio 앱에 반영한 편수나 8권 전체의 완성률을 뜻하지 않는다.','','## 이번 보강의 방향','','성찬 빈도와 양형 영성체, 후스의 생애와 후스파의 사후 역사, 프라하 강령과 헤프의 절차 합의와 바젤 협약을 나누어 설명한다. 사건 원고는 전개와 행위자를, 문헌 원고는 요구·권위·독서의 한계를 다룬다. 같은 소재가 등장해도 본문을 복제하지 않았다.','','## 출처와 확인 범위','',d['source_scope_note'],'','22건의 현대 해설·학술 자료·서지 기록과 역사 문헌의 현대 영어 발췌·서문 번역 2건을 구별했다. 검색 발췌와 초록만 확인한 자료는 아래에 표시한다. 출처 수를 원문 대조 수나 역사 명제의 완전한 검증 수로 계산하지 않는다.','','## 개요 공백 보강','','| 개요 ID | 항목 | 이전 상태 | 직접 연결할 새 원고 |','|---|---|---|---|']
    for r in d['overview_link_updates']:lines.append('| '+r['overview_id']+' | '+r['overview_title']+' | '+r['previous_status']+' | '+r['reader_id']+' |')
    lines+=['','455편 원고와 새 연결을 합쳐 검토할 경우 97개 개요 항목 중 직접 설명은 26→38, 일부 설명은 15→12, 배경만은 4→1, 직접 원고 없음은 52→46이다. 기본 읽기 가능한 항목은 41→50으로 늘어난다. 이는 검토용 예상 범위이며 V3.00의 동결된 연결 모듈이나 실제 앱 상태를 바꾸지 않는다.','','## 심화 원고','']
    for i,c in enumerate(d['chapters'],1):
        lines += [f"### {i}. {c['title']}",'',c['lead'],'',f"ID: `{c['id']}` · {c['group']}",'']
        for s in c['sections']:lines += ['#### '+s['heading'],'',s['body'],'']
        lines += ['**독서 질문:** '+c['reading_question'],'','출처: '+', '.join(c['sources']),'','이어서 읽기: '+', '.join(c['related_readers']),'']
    lines+=['## 출처 목록','']
    for s in d['sources']:lines += [f"- {s['id']} [{s['title']}]({s['url']}) — {s['scope']}. {s['inspection_note']}"]
    lines+=['','## 보존·검증·다음 단계','','기존 435편과 V2.97 편집 전달본, V3.00 연결표, 기존 핵심 원고를 수정하지 않았다. 입력의 SHA256, 누적 455개 ID, 새 원고의 관련 읽기·출처 참조, 12개 개요 연결 및 97개 항목의 분모를 검사한다. 자동 검사는 역사적 해석의 전문가 승인을 대체하지 않는다.','','```bash','python3 scripts/build_v301_precursors_hussite_readers.py --check','python3 scripts/build_v300_overview_reading_crosswalk.py --check','node --test integrations/overview-readings-v300/bridge.test.mjs integrations/medium-atlas-v298/adapter.test.mjs','```','','다음 권장 작업은 새 20편의 출처 범위와 문장 중복을 편집 검토한 뒤 455편 전달본과 개요 연결을 한 번에 갱신하는 것이다. 새 집필을 계속 늘리기 전에 읽기 화면에서 이번 보강을 검토할 수 있게 연결한다. 이후 남은 46개 직접 원고 없음 항목에서 다음 묶음을 선택한다. main·실제 앱·공개 상태는 별도 승인 없이 바꾸지 않는다.','']
    return '\n'.join(lines)
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--check',action='store_true');args=a.parse_args()
    d=load(DATA);validate(d);out=render(d)
    if args.check:assert (ROOT/DOC).read_text()==out,'Generated document drift'
    else:(ROOT/DOC).write_text(out)
    print('V3.01 PASS: 20 readers / 60 sections / 24 sources / 455 catalogue IDs / 12 overview links; HOLD')
if __name__=='__main__':main()
