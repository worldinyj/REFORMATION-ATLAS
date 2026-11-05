#!/usr/bin/env python3
"""Check restored medium-depth essays and reproduce their reading document."""
import argparse,collections,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D='data/deep/atlas_v305_medium_depth_pietism_revival_readers.json';M='docs/01_CONTENT/V305_PIETISM_REVIVAL_MEDIUM_READERS.md'
def load(p):return json.loads((R/p).read_text())
def validate(d):
 assert d['version']=='3.05' and d['status']=='DRAFT' and d['depth']=='MEDIUM'
 assert all(v is False for v in d['publication_gate'].values())
 for p in d['preserved_inputs']:assert hashlib.sha256((R/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
 prior=load(d['preserved_inputs'][0]['path'])['catalogue'];cat=d['catalogue'];new=d['chapters'];assert cat[:475]==prior and len(cat)==495
 ids={c['id']for c in cat};sids={s['id']for s in d['sources']};assert len(ids)==495 and len(sids)==22 and len(new)==20
 assert collections.Counter(c['id'].split('-')[0]for c in new)=={'PERSON':8,'EVENT':6,'DOCUMENT':6}
 old=load('data/deep/atlas_v304_integrated_475_medium_delivery.json');bodies={s['body']for c in old['readers']for s in c['sections']};used=set()
 for i,c in enumerate(new):
  assert len(c['sections'])==3 and c['reading_question'].endswith('?') and c['lead']
  assert len(set(c['related_readers']))==3 and set(c['related_readers'])<=ids and c['id']not in c['related_readers']
  assert c['sources'] and set(c['sources'])<=sids;used.update(c['sources'])
  for s in c['sections']:assert s['heading'] and len(s['body'])>=90 and s['body']not in bodies;bodies.add(s['body'])
  assert cat[475+i]==dict(id=c['id'],title=c['title'],summary=c['lead'],dataset=D,chapter_index=i,reader_document=M,section_count=3)
 assert used==sids
 for s in d['sources']:assert s['url'].startswith('https://') and s['scope'] and s['checked_on']=='2026-11-06' and s['original_image_read']is False
 oldmap={r['overview_id']:r for r in load('data/contracts/atlas_v304_overview_medium_reading_crosswalk.json')['entries']};counts=collections.Counter(r['mapping_status']for r in oldmap.values())
 assert len(d['overview_link_updates'])==11 and len({u['overview_id']for u in d['overview_link_updates']})==11
 for u in d['overview_link_updates']:
  assert oldmap[u['overview_id']]['title']==u['overview_title'] and oldmap[u['overview_id']]['mapping_status']==u['previous_status']=='NO_MATCH'
  assert u['reader_id']in {c['id']for c in new} and u['new_status']in ['DIRECT_TOPIC','PARTIAL_COVERAGE']
  counts['NO_MATCH']-=1;counts[u['new_status']]+=1
 assert dict(counts)==d['coverage_projection']['after'] and sum(counts.values())==97
 assert d['metrics']['new_body_characters']==sum(len(s['body'])for c in new for s in c['sections'])
 assert d['metrics']['total_medium_readers']==len(cat) and d['metrics']['new_sections']==60
 assert next(u for u in d['overview_link_updates']if u['overview_id']=='OV-D-017')['new_status']=='PARTIAL_COVERAGE'
 assert next(u for u in d['overview_link_updates']if u['overview_id']=='OV-E-027')['new_status']=='PARTIAL_COVERAGE'
def render(d):
 m=d['metrics'];l=['# V3.05 경건주의·영미 부흥·근대 선교의 출발','','상태: DRAFT · 중간 깊이 · 공개 보류','','인물8·사건6·문헌6, 새20편·60절·질문20개를 작성했다. 본문 '+str(m['new_body_characters'])+'자, 출처22레코드이며 누적 집필 목록은475→495편이다. 기존475편 전달본과 검토 화면은 보존한다. 실제 AI Studio 앱 탑재율이나 8권 전체 완성률을 뜻하지 않는다.','','## 자료의 확인 범위','','현대 학술·기관·교파 해설, 역사 문헌 전사의 선택 대목, PDF 추출 텍스트, 서지와 검색 결과만의 확인을 나누었다. 독일어 원판과 찬송집의 전편·악보·부흥 회심 사례 전체를 새로 대조하지 않았다. 원판 이미지 판독0면. 확인 범위 밖의 전문 감수나 모든 명제의 검증 완료를 주장하지 않는다.','','## 개요 연결 제안','','97개 항목의 직접 대응은55→64, 일부 범위12→14, 배경1 유지, 직접 원고 없음29→18이다. 감리교 운동 전체에는 초기 모임만, 설교와 규칙 항목에는 규칙만 제공하므로 일부 범위로 제한한다. 이는 새 원고 반영 시의 예상 범위이며 기존 연결표와 실제 앱은 수정하지 않았다.','','| 개요 | 항목 | 상태 | 새 원고 |','|---|---|---|---|']
 for u in d['overview_link_updates']:l.append('| '+u['overview_id']+' | '+u['overview_title']+' | '+u['new_status']+' | '+u['reader_id']+' |')
 l+=['','## 출처 주의','']+['- '+v for v in d['source_cautions']]+['','## 원고','']
 for i,c in enumerate(d['chapters'],1):
  l += [f"### {i}. {c['title']}",'',c['lead'],'','ID: `'+c['id']+'`','']
  for t in c['sections']:l+=['#### '+t['heading'],'',t['body'],'']
  l+=['**독서 질문:** '+c['reading_question'],'','출처: '+', '.join(c['sources']),'','이어서 읽기: '+', '.join(c['related_readers']),'']
 l+=['## 출처 목록','']
 for t in d['sources']:
  l+=['- '+t['id']+' ['+t['title']+']('+t['url']+') — '+t['scope']+'. '+t['inspection_note']]
  for url in t.get('additional_urls',[]):l+=['  - 추가 확인 대목: '+url]
 l+=['','## 검증과 다음 단계','','```bash','python3 scripts/build_v305_pietism_revival_readers.py --check','```','','입력 해시·495개 ID·60개 신규 절의 완전 일치 중복·출처·관련 읽기·개요11건과 문서 일치를 검사한다. 구조 검사는 역사 전문 감수가 아니다. 다음은 새20편의 편집 검토와495편 전달본·개요 연결·읽기 경로 갱신이다. 이후 한국 교회사 및 남은 초기 공동체·수도원 확산 항목의 공백을 보강한다. main·핵심 원고·실제 앱·공개 HOLD 유지.','']
 return '\n'.join(l)
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();d=load(D);validate(d);s=render(d)
 if a.check:assert (R/M).read_text()==s,'document drift'
 else:(R/M).write_text(s)
 print('V3.05 PASS: 20 readers / 60 sections / 22 sources / 495 catalogue IDs / 11 proposed overview links; HOLD')
if __name__=='__main__':main()
