#!/usr/bin/env python3
"""Integrate the V3.01 additions without changing frozen historical snapshots."""
import argparse, collections, copy, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='data/deep/atlas_v297_source_checked_medium_content_delivery_bundle.json'
NEW='data/deep/atlas_v301_medium_depth_precursors_hussite_readers.json'
OLDMAP='data/contracts/atlas_v300_overview_medium_reading_crosswalk.json'
OUT='data/deep/atlas_v302_integrated_455_medium_delivery.json'
CROSS='data/contracts/atlas_v302_overview_medium_reading_crosswalk.json'
MANIFEST='integrations/medium-atlas-v302/manifest.json'
DOC='docs/03_PRODUCT/V302_INTEGRATED_455_READING_HANDOFF.md'
def load(p):return json.loads((ROOT/p).read_text())
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def pin(p):return dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest())
def build():
    old=load(BASE);new=load(NEW);b=copy.deepcopy(old)
    b.update(version='3.02',kind='INTEGRATED_455_MEDIUM_READING_DELIVERY',parent_commit='8ff254b5d94e03916977a125799f872ea6870d4f',editorial_note='435편 기존 원고와 20편 새 원고의 본문을 보존한 통합 초안. 새 출처의 과거 확인 범위를 유지하며 외부 자료를 재확인하지 않았다.')
    b['preserved_inputs'] += [pin(BASE),pin(NEW),pin(OLDMAP)]
    for s in new['sources']:
        s=copy.deepcopy(s);s['original_id']=s['id'];s['id']='V301-'+s['id'];s['provenance']=dict(dataset=NEW);b['sources'].append(s)
    for i,c in enumerate(new['chapters']):
        r=copy.deepcopy(c);r['sources']=['V301-'+s for s in r['sources']];r['reader_type']=r['id'].split('-')[0];r['research_basis_ids']=[]
        r['source_basis_status']='V301_SCOPED_INSPECTION_INHERITED_NOT_RECHECKED'
        r['provenance']=dict(dataset=NEW,chapter_index=i,reader_document='docs/01_CONTENT/V301_PRECURSORS_HUSSITE_MEDIUM_READERS.md',original_chapter_sha256=hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode()).hexdigest())
        b['readers'].append(r)
        next(g for g in b['reader_groups'] if g['id']=='TYPE-'+r['reader_type'])['reader_ids'].append(r['id'])
    specs=[
      ('REGION-MEDIEVAL-REFORM','REGION','중세 개혁: 리옹에서 보헤미아로','PERSON-VALDES_LYON EVENT-POOR_LYON DOCUMENT-WYCLIFFITE_BIBLE PERSON-JEROME_PRAGUE PERSON-MILIC_KROMERIZ PERSON-MATTHIAS_JANOV','서로 다른 지역의 개혁 요구는 무엇이 달랐는가?','읽기 비교이며 발도에서 후스까지 직접적인 계보를 확정하지 않는다.'),
      ('TIME-HUSSITE-1378-1436','CHRONOLOGY','1378~1436년: 분열·성배·협상','EVENT-WESTERN_SCHISM1378 DOCUMENT-HUS_DE_ECCLESIA1413 EVENT-LAY_CHALICE1414 EVENT-HUS_EXECUTION1415 EVENT-FOUR_ARTICLES1420 DOCUMENT-FOUR_ARTICLES1420 DOCUMENT-CHEB_JUDGE1432 EVENT-BASEL_SETTLEMENT1433_1436 DOCUMENT-BASEL_COMPACTATA','강령과 협상 절차, 최종 정착은 어떻게 다른가?','저술·사건·문헌을 잇는 편집 순서다. 협약의 성립·공표를 하나의 날짜로 합치지 않는다.'),
      ('ISSUE-HUSSITE-POWER','ISSUE','후스파의 선택: 성찬·무력·교회 질서','PERSON-JAKOUBEK_STRIBRO PERSON-JAN_ZIZKA PERSON-PETR_CHELCICKY DOCUMENT-NET_TRUE_FAITH PERSON-JAN_ROKYCANA','같은 개혁 요구 안에서 폭력과 교회 질서를 어떻게 다르게 판단했는가?','후스파 전체가 같은 성찬론·폭력관을 공유했다고 가정하지 않는다.')]
    for id,axis,title,ids,q,limit in specs:b['reading_paths'].append(dict(id=id,axis=axis,title=title,reader_ids=ids.split(),reading_question=q,interpretive_limit=limit,status='EDITORIAL_NAVIGATION_DRAFT'))
    b['source_dataset_notes'].append(dict(dataset=NEW,note=new['source_scope_note']))
    # Preserve the older verification audit as an explicitly scoped historical record.
    b['metrics']=dict(old['metrics'],readers=455,sections=1365,questions=455,body_characters=sum(len(s['body']) for r in b['readers'] for s in r['sections']),source_records=650,new_historical_essays=0,integrated_v301_readers=20,added_reading_paths=3)
    b['editorial_audit']['v302_review']=dict(reviewed_reader_ids=[c['id'] for c in new['chapters']],body_revisions=0,scope='본문 편집 검토와 연결 정리. 외부 자료 재검증·원판 대조·전문 감수 아님.',distinctions=['성찬 빈도와 양형 영성체','후스의 생애·처형과 사후 공동체','프라하 강령·헤프 절차·바젤 협약','저술 성립과 1521년 인쇄·서문','발도의 활동과 후대 발도파 개혁 수용'])
    cross=copy.deepcopy(load(OLDMAP));cross.update(version='3.02',parent_commit=b['parent_commit']);cross['preserved_inputs'] += [pin(OLDMAP),pin(NEW)]
    idx={r['id']:r for r in b['readers']};rows={r['overview_id']:r for r in cross['entries']}
    for u in new['overview_link_updates']:
        row=rows[u['overview_id']];assert row['mapping_status']==u['previous_status'];prior=row['reader_links'];row.update(mapping_status=u['new_status'],scope=u['scope'])
        row['reader_links']=[dict(reader_id=u['reader_id'],role='PRIMARY',title=idx[u['reader_id']]['title'])]+[dict(l,role='FOLLOWUP' if l['role']=='PRIMARY' else l['role']) for l in prior if l['reader_id']!=u['reader_id']]
    counts=collections.Counter(r['mapping_status']for r in cross['entries'])
    cross['metrics'].update(direct_topic=counts['DIRECT_TOPIC'],partial_coverage=counts['PARTIAL_COVERAGE'],background_only=counts['BACKGROUND_ONLY'],no_match=counts['NO_MATCH'],default_readable=counts['DIRECT_TOPIC']+counts['PARTIAL_COVERAGE'],reading_links=sum(len(r['reader_links'])for r in cross['entries']),unique_readers=len({l['reader_id']for r in cross['entries']for l in r['reader_links']}))
    for r in b['readers']:
        assert len(r['sections'])==3 and set(r['sources'])<={s['id']for s in b['sources']}
        assert set(r['related_readers'])<=idx.keys()
    assert len(idx)==455 and len({s['id']for s in b['sources']})==650
    assert b['readers'][:435]==old['readers'] and b['sources'][:626]==old['sources']
    assert b['source_verification']==old['source_verification']
    assert b['metrics']['body_characters']==old['metrics']['body_characters']+new['metrics']['new_body_characters']
    newids={c['id']for c in new['chapters']};assert newids=={id for p in b['reading_paths'][18:]for id in p['reader_ids']}
    grouped=[id for g in b['reader_groups']for id in g['reader_ids']];assert len(grouped)==len(set(grouped))==455
    for r in cross['entries']:
        for l in r['reader_links']:assert idx[l['reader_id']]['title']==l['title']
    for e in cross['exclusions']:assert not set(e['forbidden_reader_ids'])&{l['reader_id']for l in rows[e['overview_id']]['reader_links']}
    assert counts=={'DIRECT_TOPIC':38,'PARTIAL_COVERAGE':12,'BACKGROUND_ONLY':1,'NO_MATCH':46}
    sections=[(c['id'],s['body'])for c in b['readers']for s in c['sections']];seen={};duplicates=[]
    for id,body in sections:
        if body in seen and (id in newids or seen[body]in newids):duplicates.append([seen[body],id])
        seen[body]=id
    assert not duplicates
    return b,cross

def document(b,x):
    lines=['# V3.02 — 455편 통합 전달본과 개요 연결','','상태: DRAFT · 중간 깊이 · 공개 보류','','기존 435편과 V3.01의 20편을 하나의 전달본으로 통합했다. 새 집필은 0편이며 누적 455편·1,365절·455질문·출처 레코드 650건이다. URL 중복을 제거한 고유 자료 수나 검증 완료 수가 아니다. 기존 원고 435편과 새 20편의 본문·질문은 그대로 보존했다.','','## 편집 검토','','20편의 본문과 V3.01 출처 범위를 읽고 아래 경계를 확인했다. 본문 개정은 0건이다. 같은 내용을 다룬다는 이유로 인물·사건·문헌을 삭제하지 않고 읽는 역할을 나누었다. 원문 전수 대조나 외부 자료의 신규 확인은 수행하지 않았다.','','| 원고 | 편집상 초점 |','|---|---|']
    notes=['창시자의 선택과 후대 공동체 구분','후스의 조수가 아닌 별도 경력·1416년 처형','군사 지도력과 후스파 전체의 입장 구분','성찬 빈도가 아닌 양형 영성체','지역 선출과 교황 승인 구분','개혁 지지와 무력 거부 구분','설교와 돌봄·후대 낙인 표현 주의','빈번한 성찬과 양형 영성체 구분','인물 생애보다 집단 형성·설교 허가','1378년 내부 분열과 동서 분열 구분','1415년 재판·처형과 사후 전쟁 구분','1414년 실천과 성배 상징 형성','1420년 결집 과정·적용 주체','1433년 논의·1436년 공표 구분','저자와 1413년 성립 확인·동명 저작 주의','강령의 요구·권리와 처벌의 병존','종교 조건과 황제 정치 약속 구분','번역 명칭과 실제 제작·필사 구분','1432년 절차 합의와 최종 내용 구분','중엽 성립과 1521년 인쇄·후대 서문 구분']
    for c,n in zip(b['readers'][435:],notes):lines.append('| '+c['title']+' | '+n+' |')
    lines+=['','신규 60개 본문 절을 기존 1,305절 및 신규 절과 문자열로 비교해 완전 일치 중복은 없었다. 의미 중복이 전혀 없다는 판정은 아니다. 특히 발도/리옹 빈자, 야코우베크/성배 실천, 프라하 강령 사건/문헌, 바젤 협상/협약, 첼치츠키/그물은 인물→사건→문헌 또는 사건→문헌 순서로 읽는다.','','## 읽기 연결과 범위','','새 읽기 경로 3개를 추가해 총 21개가 됐다. 3개 경로는 새 20편을 모두 포함하며 역사적 영향 관계나 자동 연대 데이터로 사용하지 않는다. 기존 18개 경로와 원고의 관련 읽기는 보존했다. 개요 연결 12개에는 새 원고를 PRIMARY로 두고 이전 연결은 FOLLOWUP 또는 BACKGROUND로 보존했다.','','| 개요 연결 상태 | 이전 | 갱신 |','|---|---:|---:|','| 직접 대응 | 26 | 38 |','| 일부 범위 | 15 | 12 |','| 배경만 | 4 | 1 |','| 직접 원고 없음 | 52 | 46 |','','97개 개요 중 기본 조회 가능한 항목은 41→50개다. 8권 전체 완성률이나 실제 앱 탑재율은 아니다. 원본 개요 레코드 97개와 잘못된 이름·판본 연결 배제 규칙 5개를 보존했다.','','## 호출과 재현','','```js',"import {createMediumAtlas} from '../../integrations/medium-atlas-v302/adapter.mjs';","import {createOverviewReadingBridge} from '../../integrations/medium-atlas-v302/bridge.mjs';",'const atlas = createMediumAtlas(delivery);','const bridge = createOverviewReadingBridge(crosswalk, atlas);',"bridge.resolve('OV-E-014'); // 1433~1436년 바젤 협상", "atlas.getReader('DOCUMENT-BASEL_COMPACTATA');",'```','','`delivery`: `'+OUT+'`  / `crosswalk`: `'+CROSS+'`. V2.98·V3.00 소비 코드는 동결하고 455편용 모듈을 별도 제공한다. 새 24개 출처는 `V301-Sxx`로 이름 공간을 분리한다. `priorInspection`은 V3.01의 과거 확인 일자·범위·메모이며 `access.status=NOT_CHECKED`는 V2.97 방식의 접근 재검증을 추가로 수행하지 않았다는 뜻이다. 과거 검색 발췌·초록 확인을 전편 확인이나 선택 주장 검증으로 승격하지 않는다. 기존 선택 주장 22건과 추가 확인 필요 1건도 그대로 유지한다.','','```bash','python3 scripts/build_v302_integrated_delivery.py --check','node --test integrations/medium-atlas-v302/*.test.mjs','```','','별도 검토 화면은 `integrations/medium-atlas-v302/index.html`에서 455편 전달본을 읽는다. 기존 V2.99 화면은 435편 스냅샷으로 보존한다. 실제 AI Studio 앱의 최신 소스·라우트와의 통합 및 그 앱의 모바일 검증은 미수행이다. 다음 작업은 남은 46개 직접 원고 없음 항목의 범위·우선순위를 정해 중간 깊이로 보강하는 것이다.','']
    return '\n'.join(lines)
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();b,x=build();raw=dump(b)
    manifest=dict(contractVersion='3.02',mode='EDITORIAL_PREVIEW_ONLY',canPublish=False,input=dict(version='3.02',path=OUT,sha256=hashlib.sha256(raw.encode()).hexdigest()),expectedCounts=dict(readers=455,sections=1365,sources=650,guides=11,claims=22,paths=21),actualAIStudioIntegrationVerified=False,actualAIStudioSourceAvailable=False)
    files={OUT:raw,CROSS:dump(x),MANIFEST:dump(manifest),DOC:document(b,x)}
    for f,s in files.items():
        if a.check:assert (ROOT/f).read_text()==s,'Generated drift: '+f
        else:(ROOT/f).parent.mkdir(parents=True,exist_ok=True);(ROOT/f).write_text(s)
    print('V3.02 PASS: 455 readers / 1365 sections / 650 source records / 21 paths / 38 direct overview links; prior bodies preserved; HOLD')
if __name__=='__main__':main()
