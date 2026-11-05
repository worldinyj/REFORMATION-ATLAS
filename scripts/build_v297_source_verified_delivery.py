#!/usr/bin/env python3
"""Reproduce the frozen, scoped V2.97 source check; --check never revisits websites."""
import argparse,collections,copy,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='data/deep/atlas_v296_edited_medium_content_delivery_bundle.json'
OUT='data/deep/atlas_v297_source_checked_medium_content_delivery_bundle.json'
REPORT='docs/01_CONTENT/V297_SOURCE_ACCESS_AND_SELECTED_CLAIM_CHECK.md'
PARENT='049d420585a9623ade9208775dc87e008c6097e3'
DATE='2026-11-05'
# These are recorded results of this session's web retrieval, not synthetic HTTP probes.
CHECKS=[
('SRC-V205-CUB','PAGE_RETURNED','turn298view0','중세 학술 텍스트 색인 페이지에 접근했다. 이번에는 위클리프 항목의 세부 본문을 근거 판정에 사용하지 않았다.','ACCESS_ONLY'),
('V296-LEGACY-01','PAGE_RETURNED','turn296view0','학술 개설의 생애·저작 및 종교 개혁자 절에서 예정과 교회 구성원, 후스에 대한 영향을 확인했다.','SELECTED_PASSAGES'),
('V296-LEGACY-02','ACCESS_FAILED','turn298view1','403 응답으로 이 환경에서 목록 본문을 확보하지 못했다. 자료가 사라졌다고 판정하지 않는다.','NOT_INSPECTED'),
('V296-LEGACY-03','PAGE_RETURNED','turn296view1','후스 저작의 저자·1413년 연대·판본 및 필사본 목록을 확인했다. 필사본 자체의 신규 판독은 아니다.','CATALOGUE_METADATA'),
('V296-LEGACY-04','ACCESS_FAILED','turn298view2','브리태니커 항목 본문을 열지 못했다. 후스 센터 해설과 대학 문헌 목록을 보완 경로로 사용한다.','NOT_INSPECTED'),
('V296-LEGACY-05','ACCESS_FAILED','turn296view2','브리태니커 논제 항목을 열지 못했다. 옥스퍼드의 현대 영어 번역·주석을 선택 주장에 연결한다.','NOT_INSPECTED'),
('SRC-V205-WORMS','PAGE_RETURNED','turn296view3','시의 유적 안내에서 4월 17·18일 심문과 유명한 문구의 후대 첨가 설명을 확인했다.','SELECTED_PASSAGES'),
('SRC-V205-GOTHA','PAGE_RETURNED','turn298view3','기록관 해설은 슈팔라틴이 말년에 작성한 연대기와 당대 심문 사건을 구분한다.','SELECTED_PASSAGES'),
('SRC-V205-BPB','PAGE_RETURNED','turn298view4','역사가의 해설 페이지와 저자·발행일, 파문과 제국의회 소환 배경을 확인했다. 모든 문장을 새로 검토한 것은 아니다.','SELECTED_PASSAGES'),
('V296-LEGACY-06','ACCESS_FAILED','turn298view5','브리태니커 제국의회 항목을 열지 못했다. 보름스 시·고타 도서관 자료는 접근 가능했다.','NOT_INSPECTED'),
('SRC-V205-MARB-GHDI','PAGE_RETURNED','turn297view0','현대 편집 영어 번역의 날짜·제15조와 번역 저본 안내를 확인했다.','EDITED_TRANSLATION_PASSAGES'),
('SRC-V205-MARB-ARCH','PARTIAL_PAGE_THEN_TIMEOUT','turn298view6','처음에는 소장기호와 날짜를 포함한 목록 페이지가 반환되었지만 세부 본문 재요청은 시간 초과였다. 이미지나 이문을 확인한 것으로 승격하지 않는다.','CATALOGUE_HEADER_ONLY'),
('SRC-V205-SCHAFF','PAGE_RETURNED','turn299view0','후대 역사 저술의 디지털 전사에서 저자 발행 1531년판과 1540년판 설명을 확인했다. 교파적 평가 어휘는 편집 판단과 분리한다.','SELECTED_PASSAGES'),
('SRC-V205-AUG-HIST','PAGE_RETURNED','turn297view1','1540년 개정판 안내에 접근했다. 교리가 전혀 바뀌지 않았다는 주장과 개혁파가 오해했다는 평가는 사이트의 교파적 해석으로 취급한다.','SELECTED_PASSAGES_WITH_CAUTION'),
('V296-LEGACY-07','PAGE_RETURNED','turn299view1','비교 텍스트 페이지에 접근했다. 이번에는 모든 조항의 비교와 저본의 정확성을 판정하지 않았다.','ACCESS_ONLY'),
('SRC-V205-CALVIN','PAGE_RETURNED','turn297view2','1536년 여섯 장·1539년 열일곱 장·1559년 여든 장 및 네 권의 개요를 확인했다. 개혁파 기관의 해설이다.','SELECTED_PASSAGES'),
('SRC-V205-CALVIN-COMP','PAGE_RETURNED','turn299view2','1536년과 1559년의 배열 비교를 확인했다. 칼뱅의 신학이 거의 변하지 않았다는 평가는 교파적 해석이며 별도 사실로 채택하지 않는다.','SELECTED_PASSAGES_WITH_CAUTION'),
('V296-LEGACY-08','PAGE_RETURNED','turn299view3','1539년 그리스도인의 삶에 관한 장을 추가했다는 저자의 설명을 확인했다. 출판사에 실린 후대 연구 해설이다.','SELECTED_PASSAGES'),
('V296-LEGACY-09','PAGE_RETURNED','turn299view4','제공되는 라틴어 비평판과 1560년 프랑스어 텍스트의 후대 편집 저본을 확인했다. 원판 직접 판독은 아니다.','EDITION_METADATA'),
('SRC-V205-ZB','PAGE_RETURNED','turn297view3','취리히 시의회와 1523년 결정, 개혁 지지자 내부의 반대와 처벌 설명을 확인했다. 발전 단계의 일반화나 평가적 소제목은 채택하지 않는다.','SELECTED_PASSAGES'),
('V296-LEGACY-10','ACCESS_FAILED','turn299view5','브리태니커 인물 항목을 열지 못했다. 취리히 중앙도서관의 해설을 확인 가능한 경로로 사용한다.','NOT_INSPECTED'),
('SRC-V205-TRENT','PAGE_RETURNED','turn297view4','1547년 의화와 1563년 신학교 규정의 현대 영어 번역을 확인했다. 소개문의 1546년 소집 서술은 공의회 개회 연대의 근거로 사용하지 않는다.','EDITED_TRANSLATION_PASSAGES_WITH_CAUTION'),
('V296-LEGACY-11','ACCESS_FAILED','turn299view6','브리태니커 항목을 열지 못했다. 대학의 연구 안내와 제1회기 편집 번역을 보완했다.','NOT_INSPECTED')]
EXTRA=[
('V297-HUS-CENTRE','후시네츠 후스 센터: 생애와 재판','https://www.cmjh.cz/en/master-john-hus.html','turn303view2','현지 기념기관의 교파적 관점이 있는 해설이다. 선택한 연대와 사건을 확인하며 가치 평가는 그대로 채택하지 않는다.'),
('V297-TRENT-FIRST','하노버 대학: 트리엔트 제1회기 영어 편집 번역','https://history.hanover.edu/texts/trent/ct01.html','turn303view0','1848년 Waterworth 영어 번역을 후대에 전사한 텍스트다. 1545년 원판이나 자필 회의록을 새로 읽은 것이 아니다.'),
('V297-TRENT-GUIDE','미국 가톨릭대학교 도서관: 트리엔트 연구 안내','https://guides.lib.cua.edu/c.php?g=711409&p=7421868','turn303view1','대학 도서관의 연대·서지 안내다. 목록에 나온 모든 책의 본문을 열람한 것은 아니다.')]
# reader, section index, exact existing text span, source IDs, locator, scoped paraphrase.
CLAIMS=[
('MEDIUM-WYCLIFFE',1,'교회의 참된 구성원을 하나님의 은혜와 예정에 연결하고','V296-LEGACY-01','§5 도입·§5.1 인접 본문','개설은 구원받은 공동체와 예정의 은혜를 연결한다.'),
('MEDIUM-WYCLIFFE',2,'후스의 논의에도 영향을 주었다','V296-LEGACY-01','§1.1 후반','후스와 프라하의 예로니무스에 대한 영향을 설명한다. 전승 경로의 전수 교감은 아니다.'),
('MEDIUM-HUS',1,'1413년의 『교회론』','V296-LEGACY-03','Date·Author 필드','대학 목록은 얀 후스의 해당 저작을 1413년으로 기술한다.'),
('MEDIUM-HUS',1,'1415년 콘스탄츠 공의회에서의 재판과 처형','V297-HUS-CENTRE','Constance 재판·1415년 7월 6일 단락','기관 해설은 콘스탄츠의 재판과 1415년 처형을 설명한다.'),
('MEDIUM-LUTHER1517',1,'그리스도인의 삶 전체를 회개와 연결하고','V288-S18','논제 1·2 및 주석','현대 번역은 회개를 일회적 행위에 한정하지 않는 논지를 제시한다.'),
('MEDIUM-LUTHER1517',1,'교회가 행사할 수 있는 권한의 범위를 물었다','V288-S18','논제 5·6 및 주석','교황이 형벌과 죄책을 다루는 권한을 구분한다. 이후 교리 전체의 확정으로 읽지 않는다.'),
('MEDIUM-LUTHER1521',1,'4월17일과18일 심문','SRC-V205-WORMS','Bishop’s palace 본문','시의 안내는 두 날짜에 궁정으로 소환되어 저술과 철회에 답한 일을 설명한다.'),
('MEDIUM-LUTHER1521',1,'양심을 내세운 것은 무엇이든 자신이 믿으면 옳다는 선언이 아니었다','SRC-V205-GOTHA','서두의 발언 전승과 이어지는 현대적 자유 개념 주의','성경과 논거에 구속된 양심이라는 전승 및 현대적 자율성과의 차이를 근거로 읽는 해석이다.'),
('MEDIUM-MARBURG',1,'루터에게 성찬에서 주어지는 그리스도의 실제적 임재','SRC-V205-MARB-GHDI','Abstract·제15조','편집 해제와 번역에서 루터의 입장 및 육체적 현존에 관한 차이를 확인한다.'),
('MEDIUM-MARBURG',2,'회담의 불일치는 개혁자들이 모든 것을 두고 적대했다는 뜻도','SRC-V205-MARB-GHDI','조항 1~15의 배열·제15조','다수의 공동 진술과 성찬의 미합의가 함께 담겨 있다는 범위에서 뒷받침된다.'),
('MEDIUM-AUGSBURG',2,'1531년 승인 인쇄','SRC-V205-SCHAFF','The Text Invariata and Variata: 저자 발행 1531년판 단락','후대 저술은 저자가 발행한 1531년판을 설명한다. 최초의 모든 인쇄물이라는 표현으로 바꾸지 않는다.'),
('MEDIUM-AUGSBURG',2,'1540년 수정판','SRC-V205-AUG-HIST SRC-V205-SCHAFF','History 첫 단락·1540 Variata 단락','1540년 개정판의 존재를 확인한다. 교리 변화의 유무에 관한 사이트의 평가는 이 판정에 포함하지 않는다.'),
('MEDIUM-CALVIN1536',0,'라틴어 초판은 여섯 장','SRC-V205-CALVIN','1536·1539년 초판과 개정판 단락','기관 해설은 첫 라틴어판이 여섯 장이었다고 설명한다.'),
('MEDIUM-CALVIN1536',2,'이후 여러 차례 확대되고 재구성되었다','SRC-V205-CALVIN-COMP V296-LEGACY-08','1536·1559 배열 비교·1539년 추가 장 설명','후대의 배열 비교와 증보 설명이 개정의 존재를 뒷받침한다. 모든 이동 문장의 직접 대조는 아니다.'),
('MEDIUM-CALVIN1559',1,'첫 권은 하나님을 창조주로 아는 문제를','SRC-V205-CALVIN SRC-V205-CALVIN-COMP','네 권의 주제 개요','두 해설의 목차 개요에서 창조주·구속·은혜의 수용·교회와 성례의 흐름을 확인한다.'),
('MEDIUM-CALVIN1559',2,'1559년 라틴어판과1560년 프랑스어판','V296-LEGACY-09','Originals: Barth-Niesel·Baumgartner 저본 안내','포털은 1559년 라틴어와 1560년 프랑스어의 후대 편집 저본을 구분한다.'),
('MEDIUM-ZWINGLI',0,'1523년의 논쟁들은 기존 관행을 성경에 비추어 판단할 수 있는지','SRC-V205-ZB','Durchbruch der Reformation','시의회의 1523년 결정은 확인했다. 이 구간의 성경을 판단 기준으로 삼았다는 부분은 지정 자료의 해당 단락만으로 확인하지 못해 부분 뒷받침으로 남긴다.'),
('MEDIUM-ZWINGLI',1,'개혁 지지자 모두가 시의회의 속도와 범위에 동의하지는 않았다','SRC-V205-ZB','Grebel·Manz와 시의회 비판 단락','지지자 내부에서 속도와 시의회 타협에 반대한 움직임을 설명한다.'),
('MEDIUM-TRENT',0,'1545년부터1563년까지','V297-TRENT-FIRST V297-TRENT-GUIDE','제1회기 일자·도서관 Introduction','제1회기 번역의 1545년 날짜와 도서관의 1545~1563년 범위를 확인한다.'),
('MEDIUM-TRENT',1,'신학교 규정은 성직 후보자의 교육과 훈련,주교의 감독 책임','SRC-V205-TRENT','Session XXIII·1563년 7월 15일·F','발췌 번역에서 교육·규율 훈련과 주교가 정하는 장소 및 운영 책임을 확인한다.'),
('THEME-COMMUNION',0,'폭넓은 공통 신앙을 확인했지만 성찬에 완전히 합의하지 못했다','SRC-V205-MARB-GHDI','조항 배열·제15조','공통 진술과 성찬의 미합의를 함께 담는다.'),
('THEME-COMMUNION',1,'한쪽은 그리스도의 임재를 믿고 다른 쪽은 아무 의미도 없는 기념행사로 여겼다고 설명해서는 안 된다','SRC-V205-MARB-GHDI','제15조의 공통 진술과 남은 현존 논쟁','성례의 공통 의미를 인정하면서 육체적 현존에 차이를 남긴 문장에 근거한 해석이다. 츠빙글리 성례론 전체의 검증은 아니다.')]

def load(p):return json.loads((ROOT/p).read_text())
def build():
    old=load(BASE);b=copy.deepcopy(old);sources={s['id']:s for s in b['sources']};readers={c['id']:c for c in b['readers']}
    required={s for c in old['reader_source_cards']for s in c['source_ids']}
    assert {s[0]for s in CHECKS}==required and len(CHECKS)==23
    ledger=[]
    for sid,result,ref,note,scope in CHECKS:
        record=dict(id='ACCESS-V297-'+str(len(ledger)+1).zfill(2),source_id=sid,url=sources[sid]['url'],checked_on=DATE,access_result=result,inspection_scope=scope,retrieval_ref=ref,note=note,original_image_read=False)
        ledger.append(record);sources[sid]['verification_v297']=copy.deepcopy(record)
        # Earlier access flags retain their historical meaning; this dated record is current.
    for sid,title,url,ref,note in EXTRA:
        s=dict(id=sid,title=title,url=url,scope='MODERN_INSTITUTIONAL_OR_EDITED_TRANSLATION_SELECTED_PASSAGES',provenance=dict(dataset=OUT,verification_date=DATE),verification_v297=dict(checked_on=DATE,access_result='PAGE_RETURNED',retrieval_ref=ref,note=note,original_image_read=False))
        b['sources'].append(s);sources[sid]=s
    sources['V288-S18']['verification_v297']=dict(checked_on=DATE,access_result='PAGE_RETURNED',retrieval_ref='turn300view0',inspection_scope='THESES_1_2_5_6_AND_EDITION_METADATA',note='현대 번역·주석과 제작 안내를 확인했다. 페이지의 영인 표시는 현대 재현 인쇄와 연결되므로 1517년 실물 판독으로 표시하지 않는다.',original_image_read=False)
    claims=[]
    for rid,index,span,sids,locator,note in CLAIMS:
        assert span in readers[rid]['sections'][index]['body'],(rid,span)
        ss=sids.split();assert set(ss)<=set(sources)
        assert all(sources[s].get('verification_v297',{}).get('access_result')=='PAGE_RETURNED'for s in ss)
        claims.append(dict(id='CLAIM-V297-'+str(len(claims)+1).zfill(2),reader_id=rid,section_index=index,exact_text_span=span,source_ids=ss,source_locator=locator,evidence_summary=note,status=('PARTIAL_SUPPORT_FURTHER_PASSAGE_NEEDED' if rid=='MEDIUM-ZWINGLI' and index==0 else 'SUPPORTED_IN_INSPECTED_MODERN_SOURCE_WITH_STATED_SCOPE'),expert_approved=False,original_witness_collated=False))
    warnings=[
      dict(id='CAUTION-AUGSBURG',source_ids=['SRC-V205-AUG-HIST','SRC-V205-SCHAFF'],reader_ids=['MEDIUM-AUGSBURG','THEME-COMMUNION'],note='1540년 개정판의 존재와 교리 평가를 구분한다. Augsburg1540 사이트는 변화가 교리를 바꾸지 않았다고 단정하고 상대 진영의 오해로 설명한다. 샤프의 후대 평가도 교파적 어휘를 포함한다. 어느 쪽의 평가도 중립적 사건 사실로 채택하지 않는다.'),
      dict(id='CAUTION-TRENT',source_ids=['SRC-V205-TRENT','V297-TRENT-FIRST','V297-TRENT-GUIDE'],reader_ids=['MEDIUM-TRENT'],note='GHDI 발췌의 제목과 소개문은 개회 연대의 근거로 쓰지 않는다. 기존 원고의 1545~1563년은 제1회기 번역과 대학 도서관 안내로 연결하고, GHDI는 해당 회기의 번역 조문에 한정해 사용한다.'),
      dict(id='CAUTION-OXFORD',source_ids=['V288-S18'],reader_ids=['MEDIUM-LUTHER1517'],note='옥스퍼드 페이지는 현대 영어 번역·주석을 제공하며 영인 제작 안내에 현대 재현 인쇄가 기술되어 있다. 이 페이지 열람을 1517년 초판 인쇄면의 신규 판독으로 세지 않는다.')]
    supplements={'MEDIUM-HUS':['V297-HUS-CENTRE'],'MEDIUM-LUTHER1517':['V288-S18'],'MEDIUM-TRENT':['V297-TRENT-FIRST','V297-TRENT-GUIDE']}
    access={r['source_id']:r for r in ledger}
    for card in b['reader_source_cards']:
        rid=card['reader_id'];selected=[c for c in claims if c['reader_id']==rid];assert len(selected)==2
        for sid in supplements.get(rid,[]):
            if sid not in card['source_ids']:card['source_ids'].append(sid)
            if sid not in readers[rid]['sources']:readers[rid]['sources'].append(sid)
        card['verification_history']=[dict(version='2.96',verification_note=card['verification_note'],status=card['status'])]
        card['selected_claim_ids']=[c['id']for c in selected]
        card['access_check_ids']=[access[s]['id']for s in card['source_ids']if s in access]
        card['preferred_source_ids']=list(dict.fromkeys(s for c in selected for s in c['source_ids']))
        card['warning_ids']=[w['id']for w in warnings if rid in w['reader_ids']]
        card['verification_note']='이번에는 아래의 선택 주장 2건을 현대 자료의 지정 부분과 대조했다. 원고 전체·모든 문장·원판의 검증은 아니다. 접근이 막힌 링크는 삭제하지 않고 상태를 표시했다.'
        card['status']='SELECTED_CLAIMS_CHECKED_FULL_REVIEW_PENDING'
        readers[rid]['source_basis_status']='SELECTED_CLAIMS_CHECKED_IN_MODERN_SOURCES_FULL_REVIEW_PENDING'
        readers[rid]['selected_claim_ids']=card['selected_claim_ids']
    b['version']='2.97';b['kind']='MEDIUM_CONTENT_DELIVERY_WITH_SCOPED_SOURCE_CHECK';b['parent_commit']=PARENT
    b['editorial_note']='누적 435편의 본문을 보존하고 출처 안내 11개의 기존 링크 23개를 점검했다. 원고별 선택 주장 2건씩 22건을 현대 자료의 지정 부분에 연결했다. 접근 성공·부분 반환·실패와 자료의 한계를 분리하며 역사 전문 감수나 원판 판독으로 승격하지 않는다.'
    b['source_verification']=dict(checked_on=DATE,method='연결된 자료를 웹 도구로 열고 선택 문구·메타데이터·편집 번역을 확인했다. 접근 실패는 이 환경의 결과이며 영구 삭제나 일반 이용자의 접근 불가를 뜻하지 않는다.',access_checks=ledger,supplementary_source_ids=[s[0]for s in EXTRA]+['V288-S18'],selected_claims=claims,source_cautions=warnings,not_checked='626건 전체 출처, 435편 전체 사실, 정확한 인용 전수, 원판 이미지와 필사본 이문, 이미지 권리, 실제 앱 동작은 이번 검토 대상이 아니다.')
    b['consumer_contract']['verification']='출처의 verification_v297와 reader_source_cards의 preferred_source_ids·selected_claim_ids·warning_ids를 사용한다. 접근 결과를 신뢰도 점수나 원고 전체의 검증 완료로 바꾸지 않는다. access_status 등 기존 값은 이전 회차 기록이다.'
    b['preserved_inputs'].append(dict(path=BASE,sha256=hashlib.sha256((ROOT/BASE).read_bytes()).hexdigest()))
    counts=collections.Counter(r['access_result']for r in ledger)
    b['metrics']=dict(readers=len(b['readers']),sections=sum(len(c['sections'])for c in b['readers']),questions=len(b['readers']),body_characters=old['metrics']['body_characters'],source_cards=11,legacy_urls_checked=23,pages_returned=counts['PAGE_RETURNED'],partial_pages=counts['PARTIAL_PAGE_THEN_TIMEOUT'],access_failures=counts['ACCESS_FAILED'],supplementary_pages_inspected=4,added_source_records=len(EXTRA),source_records=len(b['sources']),selected_claims=len(claims),supported_selected_claims=sum(c['status']=='SUPPORTED_IN_INSPECTED_MODERN_SOURCE_WITH_STATED_SCOPE'for c in claims),partially_supported_claims=sum(c['status']=='PARTIAL_SUPPORT_FURTHER_PASSAGE_NEEDED'for c in claims),source_cautions=len(warnings),body_revisions=0,new_historical_essays=0,new_original_image_readings=0)
    assert b['metrics']['pages_returned']+b['metrics']['partial_pages']+b['metrics']['access_failures']==23
    assert len(claims)==22 and len(sources)==len(b['sources'])
    for c,previous in zip(b['readers'],old['readers']):
        assert c['id']==previous['id'] and all(c[k]==previous[k]for k in ['title','lead','sections','reading_question','related_readers'])
        assert set(c['sources'])<=set(sources)
    for field in ['research_basis','reader_groups','reading_paths','legacy_reading_paths','comparisons','faq','publication_gate']:assert b[field]==old[field]
    for p in b['preserved_inputs']:assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256']
    return b

def report(b):
    m=b['metrics'];sv=b['source_verification'];cs={c['id']:c for c in b['readers']};ss={s['id']:s for s in b['sources']}
    lines=['# V2.97 출처 접근 점검과 선택 주장 대조','','상태: DRAFT · 공개 보류 · 실제 AI Studio 웹앱 미변경','','## 이번에 확인한 범위','','출처 안내 11개에 연결된 기존 URL 23개를 확인했다. 16개는 페이지가 반환되었고 1개는 목록 일부 반환 뒤 재요청이 시간 초과되었다. 나머지 6개는 이 환경에서 본문을 확보하지 못했다. 영구 삭제나 일반 사용자의 접근 불가로 판정하지 않는다. 보완 경로 4개도 열람했으며 그중 옥스퍼드 자료는 이미 기존 출처 목록에 있어 새 레코드는 3개만 추가했다.','','선택 주장 22건은 원고당 2건씩 지정 부분과 대조했다. 21건은 명시한 범위에서 뒷받침되며 1건은 부분 뒷받침으로 남겼다. 모든 문장이나 원고 전체에 대한 역사적 승인으로 확장하지 않는다. 435편·1,305절·질문 435개와 본문은 그대로 보존했다.','','| 항목 | 수량 |','|---|---:|']
    for title,k in [('기존 URL 점검','legacy_urls_checked'),('페이지 반환','pages_returned'),('일부 반환 후 시간 초과','partial_pages'),('접근 실패','access_failures'),('보완 경로 열람','supplementary_pages_inspected'),('새 출처 레코드','added_source_records'),('선택 주장 대조','selected_claims'),('지정 범위에서 뒷받침','supported_selected_claims'),('부분 뒷받침·추가 확인 필요','partially_supported_claims'),('출처 사용 주의','source_cautions'),('전체 출처 레코드','source_records'),('원판 신규 이미지 판독','new_original_image_readings')]:lines.append('| '+title+' | '+str(m[k])+' |')
    lines+=['','## 출처를 사용할 때 달라진 안내','']
    for w in sv['source_cautions']:lines+=['- '+w['note']]
    lines+=['','## 기존 URL 23개의 접근 결과','','페이지가 반환되었다고 전체 본문을 검토한 것은 아니다. 각 행의 범위가 이번 확인의 한계다. 과거 열람 상태는 보존하고 이번의 날짜별 결과를 별도 필드로 기록했다.','','| 출처 | 이번 접근 | 확인 범위와 제한 |','|---|---|---|']
    labels={'PAGE_RETURNED':'페이지 반환','PARTIAL_PAGE_THEN_TIMEOUT':'일부 반환·후속 시간 초과','ACCESS_FAILED':'접근 실패'}
    for a in sv['access_checks']:lines.append('| ['+ss[a['source_id']]['title']+']('+a['url']+') | '+labels[a['access_result']]+' | '+a['note']+' |')
    lines+=['','## 선택 주장 22건과 근거 위치','','각 인용 구간은 기존 한국어 원고에서 그대로 추출했다. 근거는 현대 자료의 지정 부분을 읽고 요약했으며 원판 전사나 교파별 진리 판정이 아니다.']
    for card in b['reader_source_cards']:
        lines+=['','### '+cs[card['reader_id']]['title'],'']
        for claim in [c for c in sv['selected_claims']if c['reader_id']==card['reader_id']]:
            lines+=['- **기존 본문:** '+claim['exact_text_span'],'  - **대조 위치:** '+claim['source_locator'],'  - **판정:** '+('부분 뒷받침·추가 확인 필요'if claim['status']=='PARTIAL_SUPPORT_FURTHER_PASSAGE_NEEDED'else'현대 자료의 지정 범위에서 뒷받침'),'  - **확인 범위:** '+claim['evidence_summary'],'  - **근거:** '+', '.join('['+ss[s]['title']+']('+ss[s]['url']+')'for s in claim['source_ids'])]
        lines+=['',card['verification_note']]
    lines+=['','## 전달본과 검증','','`'+OUT+'`을 사용하면 기존 본문·탐색과 함께 출처 접근 결과, 선택 주장과 근거 위치, 우선 읽을 출처 및 주의사항을 한 파일에서 읽을 수 있다. 재현 명령은 다음과 같다.','','```bash','python3 scripts/build_v297_source_verified_delivery.py --check','```','','이 명령은 웹사이트를 다시 방문하지 않는다. 이번 세션에서 기록한 결과와 기존 원고의 구간 일치, 내부 참조, 전체 본문 보존, 생성물 재현성을 검사한다. 미래의 링크 생존이나 새 역사적 사실을 자동으로 증명하지 않는다.','','이전 V2.95·V2.96 재생성 검사와 기존 검증·빌드 7종, 단일 파일의 출처·주장·안내 연결도 별도로 확인한다. 모든 이전 추적 파일과 핵심 원고를 보존한다.','','## 다음 작업','','중간 깊이의 선택 주장 확인을 유지하며, 실제 앱의 입력 구조와 대조할 전달 규격을 구체화한다. 원판 교감이나 모든 사실의 전수 감수로 범위를 늘리지 않는다. 실제 앱의 가져오기·화면 이동·모바일 표시는 앱에 적용한 뒤 검증해야 한다. main과 실제 Google AI Studio 웹앱은 변경하지 않았으며 공개 보류를 유지한다.','']
    return '\n'.join(lines)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args();b=build()
    for path,s in {OUT:json.dumps(b,ensure_ascii=False,indent=2)+'\n',REPORT:report(b)}.items():
        if args.check:assert (ROOT/path).read_text()==s,'Generated file drift: '+path
        else:(ROOT/path).write_text(s)
    print(json.dumps(b['metrics'],ensure_ascii=False,indent=2));print('PASS: original bodies, exact claim spans, source access distinctions, references and deterministic output')
if __name__=='__main__':main()
