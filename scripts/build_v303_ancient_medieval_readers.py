#!/usr/bin/env python3
"""Check restored medium-depth essays and reproduce their reading document."""
import argparse,collections,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D='data/deep/atlas_v303_medium_depth_ancient_medieval_readers.json';M='docs/01_CONTENT/V303_ANCIENT_MEDIEVAL_MEDIUM_READERS.md'
def load(p):return json.loads((R/p).read_text())
def validate(d):
 assert d['version']=='3.03' and d['status']=='DRAFT' and d['depth']=='MEDIUM'
 assert all(v is False for v in d['publication_gate'].values())
 for p in d['preserved_inputs']:assert hashlib.sha256((R/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
 prior=load(d['preserved_inputs'][0]['path'])['catalogue'];cat=d['catalogue'];new=d['chapters'];assert cat[:455]==prior and len(cat)==475
 ids={c['id']for c in cat};sids={s['id']for s in d['sources']};assert len(ids)==475 and len(sids)==25 and len(new)==20
 assert collections.Counter(c['id'].split('-')[0]for c in new)=={'PERSON':8,'EVENT':6,'DOCUMENT':6}
 old=load('data/deep/atlas_v302_integrated_455_medium_delivery.json');bodies={s['body']for c in old['readers']for s in c['sections']};used=set()
 for i,c in enumerate(new):
  assert len(c['sections'])==3 and c['reading_question'].endswith('?') and c['lead']
  assert len(set(c['related_readers']))==3 and set(c['related_readers'])<=ids and c['id']not in c['related_readers']
  assert c['sources'] and set(c['sources'])<=sids;used.update(c['sources'])
  for s in c['sections']:assert s['heading'] and len(s['body'])>=90 and s['body']not in bodies;bodies.add(s['body'])
  assert cat[455+i]==dict(id=c['id'],title=c['title'],summary=c['lead'],dataset=D,chapter_index=i,reader_document=M,section_count=3)
 assert used==sids
 for s in d['sources']:assert s['url'].startswith('https://') and s['scope'] and s['rechecked_on_restore']is False and s['original_image_read']is False
 oldmap={r['overview_id']:r for r in load('data/contracts/atlas_v302_overview_medium_reading_crosswalk.json')['entries']};counts=collections.Counter(r['mapping_status']for r in oldmap.values())
 assert len(d['overview_link_updates'])==17 and len({u['overview_id']for u in d['overview_link_updates']})==17
 for u in d['overview_link_updates']:
  assert oldmap[u['overview_id']]['title']==u['overview_title'] and oldmap[u['overview_id']]['mapping_status']==u['previous_status']=='NO_MATCH'
  assert u['reader_id']in {c['id']for c in new} and u['new_status']=='DIRECT_TOPIC'
  counts['NO_MATCH']-=1;counts['DIRECT_TOPIC']+=1
 assert dict(counts)==d['coverage_projection']['after'] and sum(counts.values())==97
 assert d['metrics']['new_body_characters']==sum(len(s['body'])for c in new for s in c['sections'])
 assert d['metrics']['total_medium_readers']==len(cat) and d['metrics']['new_sections']==60
 assert next(u for u in d['overview_link_updates']if u['overview_id']=='OV-P-001')['reader_id']=='PERSON-IGNATIUS_ANTIOCH'
def render(d):
 m=d['metrics'];l=['# V3.03 고대·중세 교회의 심화 읽기','','상태: DRAFT · 중간 깊이 · 공개 보류','','20편(인물8·사건6·문헌6), 60절·질문20개·출처25건을 추가한다. 본문 '+str(m['new_body_characters'])+'자이며 누적 집필 목록은 455→475편이다. 통합 전달본과 검토 화면은 455편으로 보존한다. 이 수치는 실제 앱 탑재율이나 8권 완성률이 아니다.','','## 복구와 확인 범위','',d['recovery_note'],'','출처는 이전 진행에서 실제 열람한 선택 대목과 확인 범위를 대화 기록에서 복구했다. 이번 파일 복구 단계에서 새로 외부 자료를 방문하지 않았다. 25건은 출처 레코드 수이며 전편 검토·원판 교감·전문 감수 완료 수가 아니다.','','V3.02 원격 검사(실행 42026555919)는 이전 진행에서 성공을 확인했다. 모듈119개·화면53개(320·375·1440px)의 대상은 기존 455편이며 새20편 화면 검사가 아니다.','','## 출처를 읽는 주의','']
 l += ['- '+s for s in d['source_cautions']]
 l += ['','## 개요 연결 제안','','97개 항목에서 직접 대응은 38→55, 일부 범위12·배경1 유지, 직접 원고 없음은 46→29로 줄어든다. 기존 연결표나 실제 앱을 수정한 결과가 아니라 새 원고를 반영할 경우의 편집 예상치다.','','| 개요 | 항목 | 새 원고 |','|---|---|---|']
 for u in d['overview_link_updates']:l.append('| '+u['overview_id']+' | '+u['overview_title']+' | '+u['reader_id']+' |')
 l+=['','## 원고','']
 for i,c in enumerate(d['chapters'],1):
  l += [f"### {i}. {c['title']}",'',c['lead'],'','ID: `'+c['id']+'`','']
  for s in c['sections']:l+=['#### '+s['heading'],'',s['body'],'']
  l += ['**독서 질문:** '+c['reading_question'],'','출처: '+', '.join(c['sources']),'','이어서 읽기: '+', '.join(c['related_readers']),'']
 l+=['## 출처 목록','']
 for s in d['sources']:l+=['- '+s['id']+' ['+s['title']+']('+s['url']+') — '+s['scope']+'. '+s['inspection_note']]
 l+=['','## 검증과 다음 작업','','```bash','python3 scripts/build_v303_ancient_medieval_readers.py --check','```','','기존 파일 해시·475개 고유 ID·60개 신규 본문의 완전 일치 중복·출처/관련 읽기 참조·개요17건·생성 문서 일치를 검사한다. 자동 검사는 해석의 전문 감수를 대체하지 않는다. 다음 작업은 새20편 편집 검토와 475편 전달본·개요 연결·읽기 경로의 통합 갱신이다. main·기존 핵심 원고·실제 AI Studio 앱·공개 보류를 유지한다.','']
 return '\n'.join(l)
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();d=load(D);validate(d);s=render(d)
 if a.check:assert (R/M).read_text()==s,'document drift'
 else:(R/M).write_text(s)
 print('V3.03 PASS: 20 readers / 60 sections / 25 sources / 475 catalogue IDs / 17 proposed overview links; HOLD')
if __name__=='__main__':main()
