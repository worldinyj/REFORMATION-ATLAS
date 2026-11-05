#!/usr/bin/env python3
"""Integrate the V3.01 additions without changing frozen historical snapshots."""
import argparse, collections, copy, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='data/deep/atlas_v302_integrated_455_medium_delivery.json'
NEW='data/deep/atlas_v303_medium_depth_ancient_medieval_readers.json'
OLDMAP='data/contracts/atlas_v302_overview_medium_reading_crosswalk.json'
OUT='data/deep/atlas_v304_integrated_475_medium_delivery.json'
CROSS='data/contracts/atlas_v304_overview_medium_reading_crosswalk.json'
MANIFEST='integrations/medium-atlas-v304/manifest.json'
DOC='docs/03_PRODUCT/V304_INTEGRATED_475_READING_HANDOFF.md'
def load(p):return json.loads((ROOT/p).read_text())
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def pin(p):return dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest())
def build():
    old=load(BASE);new=load(NEW);b=copy.deepcopy(old)
    b.update(version='3.04',kind='INTEGRATED_455_MEDIUM_READING_DELIVERY',parent_commit='f1dbdb7223f16991ec346a9bc4109536683fb470',editorial_note='455편 기존 원고와 20편 새 원고의 본문을 보존한 통합 초안. 새 출처의 과거 확인 범위를 유지하며 외부 자료를 재확인하지 않았다.')
    b['preserved_inputs'] += [pin(BASE),pin(NEW),pin(OLDMAP)]
    for s in new['sources']:
        s=copy.deepcopy(s);s['original_id']=s['id'];s['id']='V303-'+s['id'];s['provenance']=dict(dataset=NEW);b['sources'].append(s)
    for i,c in enumerate(new['chapters']):
        r=copy.deepcopy(c);r['sources']=['V303-'+s for s in r['sources']];r['reader_type']=r['id'].split('-')[0];r['research_basis_ids']=[]
        r['source_basis_status']='V301_SCOPED_INSPECTION_INHERITED_NOT_RECHECKED'
        r['provenance']=dict(dataset=NEW,chapter_index=i,reader_document='docs/01_CONTENT/V303_ANCIENT_MEDIEVAL_MEDIUM_READERS.md',original_chapter_sha256=hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode()).hexdigest())
        b['readers'].append(r)
        next(g for g in b['reader_groups'] if g['id']=='TYPE-'+r['reader_type'])['reader_ids'].append(r['id'])
    specs=[
      ('REGION-EARLY-CHURCH','REGION','고대 교회: 이동과 도시의 공동체','PERSON-IGNATIUS_ANTIOCH DOCUMENT-DIDACHE PERSON-AMBROSE_MILAN PERSON-AUGUSTINE_HIPPO DOCUMENT-AUGUSTINE_CONFESSIONS','지역 공동체의 실천은 어떻게 전해졌는가?','지역을 잇는 편집 경로이며 직접 영향의 계보가 아니다.'),
      ('TIME-COUNCILS-313-1054','CHRONOLOGY','313~1054년: 허용·공의회·분열','EVENT-MILAN_POLICY313 EVENT-NICAEA325 PERSON-ATHANASIUS_ALEXANDRIA DOCUMENT-NICENE_CREED325 EVENT-CONSTANTINOPLE381 EVENT-CHALCEDON451 EVENT-EAST_WEST_SCHISM1054','공식 결정과 이후 수용은 어떻게 달랐는가?','사건 연대와 후대 증언의 작성 시점을 구분한다.'),
      ('ISSUE-MEDIEVAL-LEARNING','ISSUE','중세의 공동생활과 학문','PERSON-BENEDICT_NURSIA DOCUMENT-RULE_BENEDICT PERSON-ANSELM_CANTERBURY DOCUMENT-CUR_DEUS_HOMO EVENT-MEDIEVAL_UNIVERSITIES PERSON-THOMAS_AQUINAS DOCUMENT-SUMMA_THEOLOGIAE PERSON-CATHERINE_SIENA','직무·규칙·논증은 권위와 어떤 관계인가?','수도원과 대학을 하나의 제도나 단선적인 발전 단계로 합치지 않는다.')]
    for id,axis,title,ids,q,limit in specs:b['reading_paths'].append(dict(id=id,axis=axis,title=title,reader_ids=ids.split(),reading_question=q,interpretive_limit=limit,status='EDITORIAL_NAVIGATION_DRAFT'))
    b['source_dataset_notes'].append(dict(dataset=NEW,note=new['recovery_note']))
    # Preserve the older verification audit as an explicitly scoped historical record.
    b['metrics']=dict(old['metrics'],readers=475,sections=1425,questions=475,body_characters=sum(len(s['body']) for r in b['readers'] for s in r['sections']),source_records=675,new_historical_essays=0,integrated_v303_readers=20,added_reading_paths=3)
    b['editorial_audit']['v304_review']=dict(reviewed_reader_ids=[c['id'] for c in new['chapters']],body_revisions=0,scope='본문 편집 검토와 연결 정리. 외부 자료 재검증·원판 대조·전문 감수 아님.',distinctions=['성찬 빈도와 양형 영성체','후스의 생애·처형과 사후 공동체','프라하 강령·헤프 절차·바젤 협약','저술 성립과 1521년 인쇄·서문','발도의 활동과 후대 발도파 개혁 수용'])
    cross=copy.deepcopy(load(OLDMAP));cross.update(version='3.04',parent_commit=b['parent_commit']);cross['preserved_inputs'] += [pin(OLDMAP),pin(NEW)]
    idx={r['id']:r for r in b['readers']};rows={r['overview_id']:r for r in cross['entries']}
    for u in new['overview_link_updates']:
        row=rows[u['overview_id']];assert row['mapping_status']==u['previous_status'];prior=row['reader_links'];row.update(mapping_status=u['new_status'],scope=u['scope'])
        row['reader_links']=[dict(reader_id=u['reader_id'],role='PRIMARY',title=idx[u['reader_id']]['title'])]+[dict(l,role='FOLLOWUP' if l['role']=='PRIMARY' else l['role']) for l in prior if l['reader_id']!=u['reader_id']]
    counts=collections.Counter(r['mapping_status']for r in cross['entries'])
    cross['metrics'].update(direct_topic=counts['DIRECT_TOPIC'],partial_coverage=counts['PARTIAL_COVERAGE'],background_only=counts['BACKGROUND_ONLY'],no_match=counts['NO_MATCH'],default_readable=counts['DIRECT_TOPIC']+counts['PARTIAL_COVERAGE'],reading_links=sum(len(r['reader_links'])for r in cross['entries']),unique_readers=len({l['reader_id']for r in cross['entries']for l in r['reader_links']}))
    for r in b['readers']:
        assert len(r['sections'])==3 and set(r['sources'])<={s['id']for s in b['sources']}
        assert set(r['related_readers'])<=idx.keys()
    assert len(idx)==475 and len({s['id']for s in b['sources']})==675
    assert b['readers'][:455]==old['readers'] and b['sources'][:650]==old['sources']
    assert b['source_verification']==old['source_verification']
    assert b['metrics']['body_characters']==old['metrics']['body_characters']+new['metrics']['new_body_characters']
    newids={c['id']for c in new['chapters']};assert newids=={id for p in b['reading_paths'][21:]for id in p['reader_ids']}
    grouped=[id for g in b['reader_groups']for id in g['reader_ids']];assert len(grouped)==len(set(grouped))==475
    for r in cross['entries']:
        for l in r['reader_links']:assert idx[l['reader_id']]['title']==l['title']
    for e in cross['exclusions']:assert not set(e['forbidden_reader_ids'])&{l['reader_id']for l in rows[e['overview_id']]['reader_links']}
    assert counts=={'DIRECT_TOPIC':55,'PARTIAL_COVERAGE':12,'BACKGROUND_ONLY':1,'NO_MATCH':29}
    sections=[(c['id'],s['body'])for c in b['readers']for s in c['sections']];seen={};duplicates=[]
    for id,body in sections:
        if body in seen and (id in newids or seen[body]in newids):duplicates.append([seen[body],id])
        seen[body]=id
    assert not duplicates
    return b,cross

def document(b,x):
    return '\n'.join(['# V3.04 — 475편 통합 전달본','','상태: DRAFT · 중간 깊이 · 공개 보류','','기존455편과 V3.03 새20편을 통합했다. 본문·질문 개정0건이며 475편·1425절·475질문·출처675레코드다. 고유 URL 수나 감수 완료 수가 아니다. 기존455편과 출처650건, 선택 주장22건은 보존했다.','','개요97개 중 직접55·일부12·배경1·직접 원고 없음29개다. 직접 읽기는38→55, 기본 조회 가능 항목은50→67개로 늘었다. 새3개 읽기 경로는 신규20편 전체를 포함하며 총24개 경로가 된다. 경로는 역사적 인과·직접 영향 관계를 뜻하지 않는다.','','새 출처는 V303-Sxx로 구분하고 이전 확인일·복구일·재확인하지 않았다는 상태를 함께 제공한다. V3.01의 이전 확인 기록도 그대로 남긴다. 이번 외부 자료 방문·원판 교감·전문 감수는 수행하지 않았다. 복구된 출처 기록을 신규 접근 성공이나 선택 주장 검증으로 바꾸지 않는다.','','325년/후대 신경, 381년/382년 증언, 1054년 개인 대상 파문/장기간 분열, 신학대전의 본문/보충부를 구분한다. 새60절의 완전 일치 중복 검사는 의미상 중복의 전수 감수를 뜻하지 않는다.','','## 사용과 재현','','```bash','python3 scripts/build_v304_integrated_delivery.py --check','node --test integrations/medium-atlas-v304/*.test.mjs','node integrations/medium-atlas-v304/browser-check.mjs','```','','전달본: `'+OUT+'`。개요 연결: `'+CROSS+'`。검토 화면: `integrations/medium-atlas-v304/index.html`。개요 bridge는 별도 모듈 API이며 화면에 개요 목록 UI를 추가한 것은 아니다.','','기존 V3.02 전달본·모듈·화면과 V3.03 원고를 수정하지 않는다. 실제 AI Studio 앱의 소스·라우트와 통합한 결과는 아니다. main·핵심 원고·실제 앱·공개 보류는 유지한다. 다음 집필은 남은29개 직접 원고 없음 항목을 기준으로 후대 부흥·한국 교회와 초기 공동체·수도원 확산의 공백을 검토한다.','']).replace('。','; ')

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();b,x=build();raw=dump(b)
    manifest=dict(contractVersion='3.04',mode='EDITORIAL_PREVIEW_ONLY',canPublish=False,input=dict(version='3.04',path=OUT,sha256=hashlib.sha256(raw.encode()).hexdigest()),expectedCounts=dict(readers=475,sections=1425,sources=675,guides=11,claims=22,paths=24),actualAIStudioIntegrationVerified=False,actualAIStudioSourceAvailable=False)
    files={OUT:raw,CROSS:dump(x),MANIFEST:dump(manifest),DOC:document(b,x)}
    for f,s in files.items():
        if a.check:assert (ROOT/f).read_text()==s,'Generated drift: '+f
        else:(ROOT/f).parent.mkdir(parents=True,exist_ok=True);(ROOT/f).write_text(s)
    print('V3.04 PASS: 475 readers / 1425 sections / 675 source records / 24 paths / 55 direct overview links; prior bodies preserved; HOLD')
if __name__=='__main__':main()
