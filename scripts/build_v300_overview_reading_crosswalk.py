#!/usr/bin/env python3
"""Reproduce the editorial navigation crosswalk for 97 existing overview records."""
import argparse,collections,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
INPUTS=['data/overview/volumes_and_people_v01.json','data/overview/events_documents_v01.json','data/overview/relationships_and_themes_v01.json']
DELIVERY='data/deep/atlas_v297_source_checked_medium_content_delivery_bundle.json'
OUT='data/contracts/atlas_v300_overview_medium_reading_crosswalk.json'
DOC='docs/03_PRODUCT/V300_OVERVIEW_TO_MEDIUM_READING_HANDOFF.md'
# Explicit navigation choices. These are not identity aliases or historical influence edges.
CHOICES={}
def choose(i,status,scope,primary='',followup='',background=''):
    CHOICES[i]=dict(mapping_status=status,scope=scope,reader_links=[dict(reader_id=r,role=role)for role,s in [('PRIMARY',primary),('FOLLOWUP',followup),('BACKGROUND',background)]for r in s.split()])
choose('OV-P-008','BACKGROUND_ONLY','개요의 12세기 발도 개인과 심화의 16세기 발도파 계곡은 다르다. 후대 공동체 배경으로만 연결한다.',background='REGION-WALDENSIAN_VALLEYS')
choose('OV-P-009','DIRECT_TOPIC','위클리프의 생애·교회 권위 문제를 다루는 해설이다. 모든 저작의 원문 해설을 뜻하지 않는다.','MEDIUM-WYCLIFFE')
choose('OV-P-010','DIRECT_TOPIC','후스 개인을 다루는 해설이며 사후 후스파 전체와 동일시하지 않는다.','MEDIUM-HUS')
choose('OV-P-013','DIRECT_TOPIC','루터 개인의 개요에서 1517년과 1521년의 서로 다른 국면을 고른다.','MEDIUM-LUTHER1517 MEDIUM-LUTHER1521',followup='DOCUMENT-CHRISTIAN_FREEDOM')
choose('OV-P-014','DIRECT_TOPIC','멜란히톤 개인의 교육과 공적 신앙 설명을 연결한다.','PERSON-MELANCHTHON',followup='MEDIUM-AUGSBURG')
choose('OV-P-015','DIRECT_TOPIC','츠빙글리와 취리히 개혁의 해설이다.','MEDIUM-ZWINGLI',followup='MEDIUM-MARBURG')
choose('OV-P-016','DIRECT_TOPIC','칼뱅의 두 판본을 구분해 선택한다. 인물 개요와 개별 판본의 범위는 다르다.','MEDIUM-CALVIN1536 MEDIUM-CALVIN1559',followup='CITY-GENEVA')
choose('OV-P-017','DIRECT_TOPIC','메노 시몬스 개인과 공동체 지도 활동을 연결한다.','PERSON-MENNO_SIMONS',followup='DOCUMENT-MENNO_FOUNDATION1539')
choose('OV-P-018','DIRECT_TOPIC','틴들의 번역 경력과 신약성경 제작을 구분한다.','PERSON-WILLIAM_TYNDALE',followup='DOCUMENT-TYNDALE_NT')
choose('OV-P-019','DIRECT_TOPIC','크랜머 개인과 공동기도서의 형성을 구분한다.','PERSON-CRANMER',followup='DOCUMENT-COMMON_PRAYER')
choose('OV-P-020','DIRECT_TOPIC','녹스 개인과 스코틀랜드 개혁의 지역 맥락을 연결한다.','PERSON-KNOX',followup='REGION-SCOTLAND')
choose('OV-P-021','DIRECT_TOPIC','로욜라의 이냐시오를 연결한다. 고대 안디옥의 이그나티우스와 다르다.','PERSON-IGNATIUS',followup='DOCUMENT-SPIRITUAL_EXERCISES1548')
choose('OV-P-022','DIRECT_TOPIC','아빌라의 테레사와 기도·수도 개혁을 연결한다.','PERSON-TERESA_AVILA',followup='DOCUMENT-INTERIOR_CASTLE1577')
choose('OV-E-009','BACKGROUND_ONLY','1378~1417년 대분열을 독립적으로 설명한 해설은 없다. 동시대 인물의 배경으로만 읽는다.',background='MEDIUM-WYCLIFFE MEDIUM-HUS')
choose('OV-E-010','BACKGROUND_ONLY','12세기 운동의 시작을 후대 발도파의 개혁파 수용과 합치지 않는다.',background='REGION-WALDENSIAN_VALLEYS')
choose('OV-E-011','PARTIAL_COVERAGE','위클리프의 사상 배경은 읽을 수 있으나 영어 성경 번역 운동 전체의 독립 해설은 아니다.','MEDIUM-WYCLIFFE',followup='THEME-PRINT_TRANSLATION')
choose('OV-E-012','PARTIAL_COVERAGE','후스 해설에 1415년 재판과 처형이 포함된다. 재판 전 과정을 따로 다룬 사건 원고는 아니다.','MEDIUM-HUS')
choose('OV-E-015','DIRECT_TOPIC','1517년 논쟁의 사건 맥락을 먼저 읽고 논제 문헌으로 이어진다.','MEDIUM-LUTHER1517',followup='DOCUMENT-NINETY_FIVE1517')
choose('OV-E-016','DIRECT_TOPIC','1521년 심문을 중심으로 읽는다. 보름스 칙령은 후속 법적 문서다.','MEDIUM-LUTHER1521',followup='DOCUMENT-EDICT_WORMS1521')
choose('OV-E-017','PARTIAL_COVERAGE','1527년 조항의 설명을 제공한다. 문헌 해설이 회의의 전 과정을 복원한 기록은 아니다.','DOCUMENT-SCHLEITHEIM')
choose('OV-E-018','DIRECT_TOPIC','1529년 성찬 회담과 공통 신앙·미합의의 문제를 다룬다.','MEDIUM-MARBURG',followup='THEME-COMMUNION')
choose('OV-E-019','DIRECT_TOPIC','1530년 신앙고백 제출을 연결한다. 1555년 종교평화는 다른 사건이므로 연결하지 않는다.','MEDIUM-AUGSBURG')
choose('OV-E-020','DIRECT_TOPIC','1536년 초판 사건만 연결한다. 1559년 최종판으로 자동 대체하지 않는다.','MEDIUM-CALVIN1536')
choose('OV-E-021','DIRECT_TOPIC','1545~1563년 공의회의 개관을 연결한다. 모든 회기의 문장을 직접 읽었다는 뜻은 아니다.','MEDIUM-TRENT')
choose('OV-E-022','DIRECT_TOPIC','1555년 화의의 사건·정치적 의미와 문헌 설명을 연결한다. 1530년 신앙고백과 다르다.','THEME-AUGSBURG_PEACE',followup='DOCUMENT-AUGSBURG_PEACE1555')
choose('OV-E-023','DIRECT_TOPIC','30년전쟁 개관을 연결하되 마지막 절은 1648년 화약도 함께 다룬다는 범위를 표시한다.','THEME-WAR_WESTPHALIA',followup='EVENT-BOHEMIAN_REVOLT1618 EVENT-PEACE_PRAGUE1635')
choose('OV-E-024','PARTIAL_COVERAGE','전쟁 개관의 1648년 화약 절을 제공한다. 개별 조약 체결 과정과 모든 조항의 독립 해설은 아니다.','THEME-WAR_WESTPHALIA')
choose('OV-D-005','PARTIAL_COVERAGE','후스의 1413년 『교회론』이 포함된 인물 해설이다. 위클리프의 같은 제목 저작과 합치지 않는다.','MEDIUM-HUS')
choose('OV-D-008','DIRECT_TOPIC','1517년 논제 문헌을 직접 다루는 해설로 연결한다.','DOCUMENT-NINETY_FIVE1517',followup='MEDIUM-LUTHER1517')
choose('OV-D-009','DIRECT_TOPIC','1520년 루터의 해당 저술을 설명한다.','DOCUMENT-CHRISTIAN_FREEDOM')
choose('OV-D-010','DIRECT_TOPIC','슐라이트하임 조항의 내용과 공동체 기준을 설명한다.','DOCUMENT-SCHLEITHEIM')
choose('OV-D-011','DIRECT_TOPIC','1530년 신앙고백과 후속 판본의 구분을 읽는다. 1555년 화의 문헌과 합치지 않는다.','MEDIUM-AUGSBURG')
choose('OV-D-012','DIRECT_TOPIC','개요가 가리키는 1536년 초판을 우선한다. 1559년판은 다른 판본으로 명시한 후속 읽기다.','MEDIUM-CALVIN1536',followup='MEDIUM-CALVIN1559')
choose('OV-D-013','DIRECT_TOPIC','1549년 초판과 이후 개정을 함께 다루는 공동기도서 해설이다.','DOCUMENT-COMMON_PRAYER')
choose('OV-D-014','PARTIAL_COVERAGE','공의회 개관에서 교리·신학교 규정을 읽는다. 개별 교령 전체의 전문이나 판본별 해설은 아니다.','MEDIUM-TRENT',followup='DOCUMENT-ROMAN_CATECHISM')
choose('OV-D-015','PARTIAL_COVERAGE','1648년 종교 질서를 다룬 개관을 제공한다. 뮌스터·오스나브뤼크 조약문 전체를 대신하지 않는다.','THEME-WAR_WESTPHALIA')
choose('OV-D-020','PARTIAL_COVERAGE','16세기 중심의 세 쟁점 해설을 연결한다. 시대 횡단의 전체 문헌군이나 원문 전문이 아니다.','THEME-SCRIPTURE_AUTHORITY THEME-COMMUNION THEME-PRINT_TRANSLATION')
choose('TOP-01','PARTIAL_COVERAGE','16세기 권위 논쟁의 비교를 연결한다. 전 시대의 성경 권위사를 포괄하지 않는다.','THEME-SCRIPTURE_AUTHORITY')
choose('TOP-02','PARTIAL_COVERAGE','위클리프·후스와 교회 통치의 선택 사례를 연결한다. 고대부터 이어지는 교회론 전체는 아니다.','MEDIUM-WYCLIFFE MEDIUM-HUS DOCUMENT-HOOKER_LAWS')
choose('TOP-03','PARTIAL_COVERAGE','16세기 성찬 논쟁을 우선하고 중세 선구자의 개관을 후속으로 둔다. 모든 저자의 성찬론을 구절별 대조한 문헌군은 아니다.','THEME-COMMUNION MEDIUM-MARBURG',followup='MEDIUM-WYCLIFFE MEDIUM-HUS')
choose('TOP-04','PARTIAL_COVERAGE','16세기 은총·칭의 비교를 제공한다. 아우구스티누스와 후대 부흥까지 모두 집필한 것은 아니다.','THEME-GRACE_FAITH_WORKS',followup='MEDIUM-TRENT')
choose('TOP-05','PARTIAL_COVERAGE','도시 권력·학교·규율의 선택 사례다. 모든 시대의 개혁과 정치 권력 관계를 포괄하지 않는다.','THEME-CITY_POWER THEME-EDUCATION THEME-CHURCH_DISCIPLINE')
choose('TOP-06','PARTIAL_COVERAGE','아우크스부르크·트리엔트 등 16세기 사례를 연결한다. 니케아 문헌과 고대 공의회 전체는 미연결이다.','MEDIUM-AUGSBURG MEDIUM-TRENT DOCUMENT-BOOK_CONCORD')
choose('TOP-07','PARTIAL_COVERAGE','16세기 번역·인쇄와 영어·독일어 성경의 사례다. 한글 초기 번역사는 미연결이다.','THEME-PRINT_TRANSLATION DOCUMENT-TYNDALE_NT DOCUMENT-LUTHER_BIBLE1534')
choose('TOP-08','BACKGROUND_ONLY','초기 근대의 경건·선교 배경은 있으나 경건주의·감리교·대각성의 독립 해설을 대신하지 않는다.',background='DOCUMENT-TRUE_CHRISTIANITY GLOBAL-INDIA_JAPAN GLOBAL-CHINA')

def load(p):return json.loads((ROOT/p).read_text())
def generate():
    p,e,t=map(load,INPUTS);bundle=load(DELIVERY);readers={c['id']:c for c in bundle['readers']};rows=[]
    for category,path,entries in [('PERSON',INPUTS[0],p['people']),('EVENT',INPUTS[1],e['events']),('DOCUMENT',INPUTS[1],e['documents']),('TOPIC',INPUTS[2],t['ideas'])]:
        for record in entries:
            choice=CHOICES.get(record['id'],dict(mapping_status='NO_MATCH',scope='현재 435편 목록에서 이 개요 항목을 직접 다루는 심화 원고를 확인하지 못했다. 이름이나 시대가 비슷한 원고로 자동 대체하지 않는다.',reader_links=[]))
            links=[dict(link,title=readers[link['reader_id']]['title'])for link in choice['reader_links']]
            rows.append(dict(overview_id=record['id'],category=category,title=record.get('name_ko',record.get('title')),period=record.get('period',record.get('date_label')),overview_summary=record['summary'],overview_dataset=path,overview_record=record,mapping_status=choice['mapping_status'],scope=choice['scope'],reader_links=links,status='EDITORIAL_NAVIGATION_DRAFT'))
    ids={r['overview_id']for r in rows};assert len(rows)==len(ids)==97 and set(CHOICES)<=ids
    for r in rows:
        assert (r['mapping_status']=='NO_MATCH')==(not r['reader_links'])
        assert len({l['reader_id']for l in r['reader_links']})==len(r['reader_links'])
        assert set(l['reader_id']for l in r['reader_links'])<=set(readers)
        if r['mapping_status']=='BACKGROUND_ONLY':assert all(l['role']=='BACKGROUND'for l in r['reader_links'])
        elif r['reader_links']:assert any(l['role']=='PRIMARY'for l in r['reader_links'])
    exclusions=[dict(overview_id=i,forbidden_reader_ids=s.split(),reason=reason)for i,s,reason in [
      ('OV-P-001','PERSON-IGNATIUS','안디옥의 이그나티우스와 로욜라의 이냐시오는 다른 인물'),
      ('OV-D-005','MEDIUM-WYCLIFFE','후스와 위클리프의 동명 교회론은 다른 저작'),
      ('OV-E-019','THEME-AUGSBURG_PEACE DOCUMENT-AUGSBURG_PEACE1555','1530년 신앙고백 제출과 1555년 화의는 다른 사건'),
      ('OV-E-020','MEDIUM-CALVIN1559','1536년 초판 사건과 1559년판을 구분'),
      ('OV-E-014','CITY-BASEL EVENT-BASEL_REFORM1529','1433~1436년 콤팍타타와 16세기 바젤 개혁을 구분')]]
    by_id={r['overview_id']:r for r in rows}
    for x in exclusions:assert not set(x['forbidden_reader_ids'])&{l['reader_id']for l in by_id[x['overview_id']]['reader_links']}
    counts=collections.Counter(r['mapping_status']for r in rows)
    result=dict(version='3.00',kind='OVERVIEW_TO_MEDIUM_READING_NAVIGATION',status='DRAFT',parent_commit='73ff5fcb286ab7f42b7e2bb1c32ef377d7426951',publication_gate=dict(published=False,main_changed=False,webapp_integrated=False),input_scope='저장소의 개요 인물33·사건34·문헌20·주제10만 대조한다. 장소·관계32·실제 앱의 최신 데이터는 이 분모에 포함하지 않는다.',preserved_inputs=[dict(path=f,sha256=hashlib.sha256((ROOT/f).read_bytes()).hexdigest())for f in INPUTS+[DELIVERY]],mapping_policy='명시적인 읽기 안내다. ID 동일성·역사적 영향·원문 전수검증을 주장하지 않는다. 기본 조회는 PRIMARY만 반환하고 FOLLOWUP·BACKGROUND는 명시적 선택에서만 반환한다.',entries=rows,exclusions=exclusions,metrics=dict(overview_records=97,people=33,events=34,documents=20,topics=10,direct_topic=counts['DIRECT_TOPIC'],partial_coverage=counts['PARTIAL_COVERAGE'],background_only=counts['BACKGROUND_ONLY'],no_match=counts['NO_MATCH'],default_readable=counts['DIRECT_TOPIC']+counts['PARTIAL_COVERAGE'],reading_links=sum(len(r['reader_links'])for r in rows),unique_readers=len({l['reader_id']for r in rows for l in r['reader_links']}),excluded_false_matches=len(exclusions),new_historical_essays=0))
    return result

def document(x):
    labels={'DIRECT_TOPIC':'대응 주제 해설','PARTIAL_COVERAGE':'일부 범위 해설','BACKGROUND_ONLY':'배경 자료만','NO_MATCH':'직접 원고 없음'}
    lines=['# V3.00 개요 항목에서 심화 읽기로 연결','','상태: DRAFT · 공개 보류 · 실제 AI Studio 앱 미반영','','## 무엇을 대조했는가','','저장소에 실제로 있는 인물 33·사건 34·문헌 20·주제 10, 총 97개 개요 레코드를 최신 435편 전달본과 대조했다. 아래 수치는 이 97개 항목에 한정하며 8권 전체 편찬 완료율이나 실제 앱의 완료율이 아니다. 장소·관계 데이터와 실앱 최신 소스는 포함하지 않았다.','','| 연결 상태 | 항목 수 |','|---|---:|']
    for k,n in [('대응 주제 해설','direct_topic'),('일부 범위 해설','partial_coverage'),('배경 자료만','background_only'),('직접 원고 없음','no_match')]:lines.append('| '+k+' | '+str(x['metrics'][n])+' |')
    lines+=['','기본 조회에서 읽을 수 있는 항목은 '+str(x['metrics']['default_readable'])+'개다. 일부 범위 해설을 해당 항목 전체의 완성으로 세지 않는다. 배경 자료는 사용자가 후속·배경 읽기를 선택할 때만 반환한다. 이름이 비슷하다는 이유로 연결을 추정하지 않는다.','','## 연결표','','| 개요 ID | 항목 | 상태 | 심화 읽기 | 범위 |','|---|---|---|---|---|']
    for r in x['entries']:lines.append('| '+r['overview_id']+' | '+r['title']+' | '+labels[r['mapping_status']]+' | '+'; '.join(l['title']+' ['+l['role']+']'for l in r['reader_links'])+' | '+r['scope']+' |')
    lines+=['','## 잘못된 연결을 막는 사례','']
    for e in x['exclusions']:lines.append('- '+e['overview_id']+': '+e['reason']+'.')
    lines+=['','## 호출 예시','','```js',"import {createMediumAtlas} from '../../integrations/medium-atlas-v298/adapter.mjs';","import {createOverviewReadingBridge} from '../../integrations/overview-readings-v300/bridge.mjs';",'','const atlas = createMediumAtlas(delivery);','const bridge = createOverviewReadingBridge(crosswalk, atlas);',"const initial = bridge.resolve('OV-D-012'); // 1536년 초판을 우선", "const extended = bridge.resolve('OV-D-012', {includeRelated: true}); // 1559년판 추가", "const missing = bridge.resolve('OV-P-024'); // 웨슬리: 직접 원고 없음",'```','','`delivery`는 기존 V2.97 전달본 객체, `crosswalk`는 `data/contracts/atlas_v300_overview_medium_reading_crosswalk.json` 객체다. 이 모듈은 fetch나 앱 상태 변경을 하지 않는다. 결과의 `readers[].id`로 V2.98의 `getReader()`를 호출한다. 이 ID를 실제 앱의 라우트나 개요 ID와 같다고 처리하지 않는다.','','개요 항목의 상태가 일부 범위 또는 배경 자료이면 `scope` 안내를 함께 표시한다. 대응 원고가 없을 때 다른 원고로 자동 대체하지 않는다. 역방향 `forReader(readerId)`는 읽기 탐색용 연결이며 영향 관계나 직접 참석의 증거가 아니다.','','## 재생성·검증','','```bash','python3 scripts/build_v300_overview_reading_crosswalk.py --check','node --test integrations/overview-readings-v300/bridge.test.mjs','```','','생성기는 원래 개요 ID·제목·레코드와 입력 체크섬, 435편 ID 참조, 배경·후속 역할, 잘못된 연결 배제 규칙을 검사한다. 원본 개요·본문은 수정하지 않는다. 노드 검사는 기본/후속 조회와 없는 항목 처리, 역방향 연결, 오류 입력을 검사한다.','','## 계획 대비 드러난 공백','','435편의 전체 수와 기존 개요의 충족 범위는 다르다. 고대·중세 일부·후대 부흥·한국 교회사에는 직접 연결할 원고가 남아 있지 않으며 표에서 확인할 수 있다. 이 공백은 앱의 검색 오류가 아니라 현재 집필 범위의 차이다. 다음 집필의 우선순위를 이 표의 직접 원고 없음 항목에서 정할 수 있다.','','실제 AI Studio 앱의 개요 ID와 구조가 이 저장소 스냅샷과 같은지는 아직 확인하지 않았다. 실제 앱에 적용하기 전에 그 데이터를 대조해야 한다. 별도 검토 화면이 열려 있다는 사실과 실앱 탑재는 구분한다. main·기존 원고·실제 앱을 보존하고 공개 보류를 유지한다.','']
    return '\n'.join(lines)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args();x=generate()
    for f,s in {OUT:json.dumps(x,ensure_ascii=False,indent=2)+'\n',DOC:document(x)}.items():
        if args.check:assert (ROOT/f).read_text()==s,'Generated file drift: '+f
        else:(ROOT/f).write_text(s)
    print(json.dumps(x['metrics'],ensure_ascii=False,indent=2));print('PASS: 97 overview records, explicit reading targets, scope distinctions and reproducibility')
if __name__=='__main__':main()
