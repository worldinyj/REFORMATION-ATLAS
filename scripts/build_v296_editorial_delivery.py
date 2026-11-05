#!/usr/bin/env python3
"""Reproduce V2.96 editorial revisions and inherited-source reading cards. No network writes."""
import argparse,copy,hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='data/deep/atlas_v295_medium_content_delivery_bundle.json'
DOSSIERS='data/deep/atlas_v205_source_dossiers.json'
OUT='data/deep/atlas_v296_edited_medium_content_delivery_bundle.json'
REPORT='docs/01_CONTENT/V296_EDITORIAL_REVISIONS_AND_READER_SOURCE_CARDS.md'
PARENT='fc46a15477afba37686efb5ec3d06870e4db3311'
def load(p):return json.loads((ROOT/p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def text(c):return '\n'.join(s['body']for s in c['sections'])
# Ordered one-for-one against V2.95's twenty ranked candidates. Existing factual content only.
REVISIONS=[
('PERSON-BARTOLOME_LASCASAS',1,'그는 원주민 사회의 법과 정치 질서를 인정하며 정복과 강제 노동, 강제 개종을 비판했다. 바야돌리드의 논쟁과 인쇄물은 이 주장을 공론화한 수단이었다. 그의 생애에서는 식민 체제에 참여했던 사람이 자신의 책임을 어떻게 다시 판단했는지에 주목할 수 있다.','인물은 식민 참여에서 비판으로의 변화, 사건은 왕권이 마련한 논쟁의 쟁점과 현지 효과를 맡는다.'),
('PERSON-JACOBUS_ARMINIUS',1,'아르미니우스와 후계자들의 논의를 은혜 없이 스스로 구원받는 주장으로 요약할 수는 없다. 인물의 활동을 읽을 때는 은혜와 믿음에 관한 질문이 같은 개혁파 교회와 목회자 교육의 자리에서 나왔다는 점에 주목해야 한다. 후계자들이 작성한 항의서의 조항은 별도로 살펴볼 수 있다.','인물은 대학·교회 안의 질문과 사후 논쟁, 문헌은 다섯 조항의 실제 내용과 유보를 맡는다.'),
('PERSON-GUILLAUME_BUDE',1,'뷔데의 관여 아래 왕실 도서관은 이탈리아와 오스만 영역 등에서 그리스어 필사본을 구했다. 책을 확보하는 일과 왕립 강독관을 제안하는 일은 서로 연결되었다. 읽을 자료와 가르칠 사람을 함께 마련하려 했다는 점에서 그의 학문 활동과 왕실 업무가 만난다.','인물은 장서·필사본과 후원 연결, 사건은 강독관 임명과 교육 권한의 제도화를 맡는다.'),
('PERSON-PETER_MELIUS',1,'멜리우스는 데브레첸의 회의와 교리 논쟁에서 공동체의 기준을 세우려 했다. 루터교와 반삼위일체 흐름을 향한 경계도 있었으므로, 그를 관용이나 논박이라는 한 단어로 분류하기 어렵다. 1567년 회의의 고백 채택과 운영 규정은 별도의 사건 해설에서 이어 읽을 수 있다.','인물은 학업·지역 목회·논박·출판, 사건은 신앙고백 채택과 지역의 결정을 맡는다.'),
('PERSON-FRANCYSK_SKARYNA',1,'스카리나는 프라하에서 성경 출판을 시작한 뒤 빌뉴스에서도 책을 냈다. 의학과 인문학의 교육을 받은 인물이 여러 도시의 인쇄 기반을 활용했다는 점이 생애를 잇는다. 구약 분책의 구성과 교회슬라브어 전통, 후대 소장본의 묶음은 성경 해설에서 구분해 살펴볼 수 있다.','인물은 이동·학문·출판 경력, 문헌은 분책·대본·언어·제본의 차이를 맡는다.'),
('THEME-CITY_POWER',0,'취리히 시의회는 논쟁을 듣는 데 머물지 않고 예배와 공공질서를 결정했다. 도시 통치의 관점에서는 종교적 판단을 누가 실행할 권한을 가졌는지에 주목할 수 있다. 츠빙글리 개인의 활동과 구분해 볼 문제다.','핵심 해설은 츠빙글리와 개혁 진영의 갈등, 주제는 시의회·재산·공공업무의 구조를 맡는다.'),
('PERSON-SIXTUS_V',1,'1588년 교황청 개편은 식스토 5세가 기존 기구와 새 업무를 한 체계에 배치한 통치 방식이었다. 인물의 활동을 읽을 때는 조직 정비와 뒤의 라틴어 성경 공인 작업이 모두 규범을 안정시키려는 과제였다는 점을 볼 수 있다. 열다섯 기구의 구성과 설립·재편의 차이는 사건 해설에서 다룬다.','인물은 행정과 성경 공인의 여러 과제, 사건은 전문 기구와 업무 배분의 재편을 맡는다.'),
('PERSON-PAUL_SPERATUS',0,'슈페라투스의 세 찬송은 1524년 초기 개신교 찬송집에 실렸다. 짧은 가사로 믿음과 은총을 설명한 활동은 이후 교회를 지도한 직무와 함께 읽을 수 있다. 찬송집의 다른 저자와 같은 해 음악책들의 구성은 문헌 해설에서 비교한다.','인물은 찬송 저자와 교회 지도자의 역할, 문헌은 여덟 곡의 구성과 다른 음악책과의 차이를 맡는다.'),
('PERSON-GUAMAN_POMA',2,'원고가 지금 남아 있다는 사실과 당시 국왕이 읽고 제안을 시행했다는 주장은 다르다. 원고 이동의 일부는 추정으로 남아 있다. 그의 생애와 발언에서는 식민 통치를 경험한 저자가 어떤 권위로 개혁을 요구했는지에 주목하고, 언어·그림·전달 형식은 작품 해설에서 살펴볼 수 있다.','인물은 현지 저자의 발언 위치와 통치 제안, 문헌은 글·그림·언어·전달 조건을 맡는다.'),
('PERSON-JOHAN_III',1,'요한의 통치에는 1571년 교회 규정의 승인과 1576년 새 예식서 도입이라는 서로 다른 결정이 있었다. 교회 조직의 기준을 세운 뒤에도 예배의 문구와 순서는 다시 논쟁이 되었다. 왕권이 개혁된 교회의 방향을 어디까지 정할 수 있는지가 그의 정책을 읽는 중심 질문이다.','인물은 왕권의 종교 정책, 문헌은 페흐트의 작성·언어·예배 형식과 수용을 맡는다.'),
('EVENT-HENRY_CONVERSION1593',0,'1593년 개종 당시 앙리 4세는 이미 1589년부터 왕위를 주장하고 있었다. 이 사건의 초점은 새로운 왕위 계승보다 국왕의 가톨릭 전환이 통치의 인정에 어떤 조건을 더했는가에 있다. 앞선 전쟁과 계승의 경위는 인물 해설과 함께 읽을 수 있다.','인물은 계승에서 통치 확보까지의 경력, 사건은 공개 개종·후속 인정·개혁파의 선택을 맡는다.'),
('PERSON-CLEMENT_MAROT',1,'마로는 1544년 사망할 때까지 시편 49편을 마련했다. 그가 완성하지 못한 작업은 베자가 이어받았다. 마로의 몫을 살피면 시인의 언어가 신앙의 노래로 옮겨진 과정을 볼 수 있다. 1562년 전체 시편집의 구성과 선율·인쇄는 별도의 문헌 해설에서 다룬다.','인물은 시인의 언어와 궁정·회중의 사용, 문헌은 전체 150편과 선율·편집·인쇄를 맡는다.'),
('PERSON-WILLIAM_TYNDALE',1,'1526년 페터 쇠퍼가 인쇄한 영어 신약은 틴들의 언어 연구가 책으로 제작되는 접점이었다. 원어를 선택하고 영어 문장을 만드는 번역자의 판단과 인쇄업자의 기술을 함께 보아야 한다. 쾰른의 중단된 시도와 보름스 출판, 검열과 후속 개정은 신약성경 해설에서 이어진다.','인물은 대본·번역의 판단과 생애 이후 영향, 문헌은 제작 장소·검열·개정의 경로를 맡는다.'),
('PERSON-ROBERT_BELLARMINE',0,'벨라르미노는 뢰번과 로마에서 가르쳤고, 로마의 강의는 『논쟁집』으로 이어졌다. 인물의 활동에서는 학문적 논박뿐 아니라 짧은 교리 교육서와 주교로서의 방문·설교를 함께 볼 필요가 있다. 여러 독자에게 가르침을 전달했다는 점이 그의 활동을 연결한다.','인물은 강의·평신도 교육·주교 직무, 문헌은 논쟁집의 구성·소장본·논박의 읽기 방식을 맡는다.'),
('REGION-POLAND_LITHUANIA',1,'1573년 바르샤바 연맹은 다른 신앙을 가진 집단들이 왕국의 평화를 약속한 중요한 사례다. 지역 개관에서는 왕위 공백과 선출, 서로 다른 집단의 협력이라는 정치적 조건을 먼저 살펴볼 수 있다. 신앙을 이유로 한 처벌을 제한한 문구와 영주·예속민의 조항은 문헌 해설에서 읽는다.','지역은 선출 정치와 신앙 공존의 조건, 문헌은 처벌 제한과 신분질서의 실제 조항을 맡는다.'),
('PERSON-HANS_TAUSEN',2,'타우센의 생애는 1536년의 결정 이전부터 도시에서 새 설교를 지지한 움직임이 있었음을 보여 준다. 설교자와 주민의 관계를 먼저 살피면 왕실의 제도화만으로는 보이지 않는 개혁의 경로가 드러난다. 주교 체포와 법적 결정, 뒤의 운영 문서는 코펜하겐 사건에서 이어 읽는다.','인물은 도시의 설교와 협력, 사건은 내전 이후 체포·법적 결정·운영 규정의 순서를 맡는다.'),
('THEME-EDUCATION',1,'도시가 교사와 학교를 지원해야 한다는 요구는 교육을 개인의 열의에만 맡기지 않으려는 흐름이었다. 루터의 1524년 권고와 멜란히톤의 활동이 이 관심을 보여 준다. 주제 해설에서는 교육의 공적 책임을, 권고문 해설에서는 도시와 가정에 제시한 구체적인 논거를 살펴볼 수 있다.','주제는 교육의 필요·공적 지원·기회 차이, 문헌은 학교 유지와 남아·여아 교육의 구체적 요청을 맡는다.'),
('PERSON-XU_GUANGQI',1,'서광계는 리치와 함께 1607년 『기하원본』의 중국어 표현과 논증을 검토했다. 그의 이름을 번역 보조자로만 두면 학자이자 관료로서의 선택과 지적 책임이 사라진다. 『원론』 앞 여섯 권이라는 범위와 정의·공리·증명을 옮기는 문제는 문헌 해설에서 살펴본다.','인물은 개종·관료의 책임·지적 선택, 문헌은 여섯 권의 번역 범위와 용어·논증의 재구성을 맡는다.'),
('PERSON-PIUS_V',1,'비오 5세 아래에서 로마 교리서·성무일도서·미사 경본이 서로 다른 용도로 제공되었다. 이 책들은 순시와 성직자 교육, 생활 규율을 반복되는 실무로 연결했다. 인물의 통치에서는 이런 수단의 결합을, 각 전례서에서는 기도·예식의 구성과 교정·인쇄의 과정을 살펴볼 수 있다.','인물은 교육·순시·전례서의 결합, 문헌은 성무일도의 기능과 실제 교정·인쇄·지역 사용을 맡는다.'),
('EVENT-THREE_HENRYS1585',0,'1584년 프랑수아 당주의 사망 뒤 나바르의 앙리가 왕위 계승자로 떠오르자 가톨릭 동맹은 이를 거부했고, 1585년 이후 전쟁이 격화되었다. 사건의 중심에는 혈통상의 계승권뿐 아니라 앙리 3세·기즈의 앙리·나바르의 앙리가 서로 다른 이해를 가졌다는 문제가 있다.','인물은 앙리 4세의 통치 확보, 사건은 세 지도자의 경쟁과 가톨릭 진영 내부의 분열을 맡는다.')]

CARD_GUIDES={
'WYCLIFFE':('위클리프의 교회론과 중세 배경','학술 개설에서 사상과 맥락을 읽고, 서지 자료에서는 저작과 편집본의 존재를 구분해 확인한다.'),
'HUS':('후스의 생애와 『교회론』 자료','생애 개설과 대학의 문헌·비평판 안내를 나누어 읽는다. 소장·편집 정보만으로 구절 대조가 완료된 것은 아니다.'),
'LUTHER1517':('1517년 논쟁의 배경','논제 사건의 개설과 번역된 논제 문서를 구분한다. 이 목록은 실제 게시 방식이나 모든 문장의 사료 검증을 대신하지 않는다.'),
'LUTHER1521':('보름스의 심문과 발언의 전승','시의 역사 안내·역사가 해설·기록 소장 안내를 구분한다. 유명한 문구를 당일 속기록과 같게 읽지 않는다.'),
'MARBURG':('마르부르크 조항의 합의와 남은 차이','현대 편집 번역과 기록 목록을 구분한다. 특히 검색 발췌로 확인한 소장 기록을 원본 직접 판독으로 표시하지 않는다.'),
'AUGSBURG':('1530년 제출·1531년 승인 인쇄·1540년 개정','판본사 해설과 비교 텍스트를 나누어 읽는다. 연도별 책의 존재와 구체적인 문구 차이는 다른 확인 수준이다.'),
'CALVIN1536':('1536년 초판과 후속 증보','초판의 여섯 장과 후속 판본의 확장을 확인하는 길이다. 교파적 관점의 출판사·기관 해설임을 함께 표시한다.'),
'CALVIN1559':('1559년 최종 라틴어판의 구성','후대의 판본사 해설과 라틴어 비평판 접근 경로를 구분한다. 링크의 존재를 원판 전체를 새로 읽었다는 뜻으로 사용하지 않는다.'),
'ZWINGLI':('취리히 개혁과 도시의 결정','인물 개설과 소장기관의 연대 안내를 함께 읽는다. 이 자료만으로 주민 전체의 동의나 자유의 확대를 단정하지 않는다.'),
'TRENT':('공의회의 결정과 교회 운영','공의회 개설과 현대 편집 영어 번역을 구분한다. 가톨릭의 공적 결정을 모든 교파가 동의한 판정으로 읽지 않는다.')}
LEGACY_TITLES={
'https://plato.stanford.edu/entries/wyclif/':'스탠퍼드 철학백과: 존 위클리프',
'https://catalog.folger.edu/record/17976':'폴저 도서관: 위클리프 편집본 서지',
'https://digiscripta.phil.muni.cz/cs/node/12908':'마사리크 대학교: 후스 문헌 안내',
'https://www.britannica.com/biography/Jan-Hus':'브리태니커: 얀 후스',
'https://www.britannica.com/event/Ninety-five-Theses':'브리태니커: 95개조 논제',
'https://www.britannica.com/event/Diet-of-Worms-Germany-1521':'브리태니커: 보름스 제국의회',
'https://suche.staatsarchiv.djiktzh.ch/detail.aspx?ID=618165':'취리히 주립문서관: 마르부르크 조항 소장 기록',
'https://www.augsburg1540.com/1530-1540-comparison-text.html':'Augsburg1540: 1530·1540 비교 텍스트',
'https://www.uecf.net/books/collected-works/chapter1319.html':'샤프의 신앙고백사: 후대 디지털 전사',
'https://www.crossway.org/articles/an-important-chapter-that-calvin-added-to-the-second-edition-of-his-institutes/':'Crossway: 『기독교강요』 제2판 증보 해설',
'https://calvin.reformation.nl/':'칼뱅 연구: 라틴어 비평판 접근 경로',
'https://www.britannica.com/biography/Huldrych-Zwingli':'브리태니커: 훌드리히 츠빙글리',
'https://www.britannica.com/event/Council-of-Trent':'브리태니커: 트리엔트 공의회'}

def build():
    old=load(BASE);b=copy.deepcopy(old);readers={c['id']:c for c in b['readers']};before={c['id']:c for c in old['readers']};edits=[]
    assert len(REVISIONS)==len(old['editorial_audit']['ranked_review_candidates'])==20
    for rank,((rid,index,new_body,reason),candidate) in enumerate(zip(REVISIONS,old['editorial_audit']['ranked_review_candidates']),1):
        assert rid in candidate['reader_ids'] and before[rid]['sections'][index]['body']!=new_body
        c=readers[rid];old_body=c['sections'][index]['body'];assert len(new_body)<len(old_body),(rid,len(new_body),len(old_body))
        c['sections'][index]['body']=new_body
        c['editorial_revision']=dict(version='2.96',base_dataset=BASE,base_reader_sha256=sha(before[rid]),revised_reader_text_sha256=sha(c['sections']),changed_section_indices=[index],historical_claims_added=False)
        edits.append(dict(rank=rank,reader_ids=candidate['reader_ids'],edited_reader_id=rid,section_index=index,heading=c['sections'][index]['heading'],before=old_body,after=new_body,characters_removed=len(old_body)-len(new_body),decision='RETAIN_BOTH_EDIT_REPEATED_EXPLANATION',rationale=reason,scope='EDITORIAL_TEXT_COMPARISON_NOT_NEW_HISTORICAL_VERIFICATION'))
        # Reciprocal related links make the division of reading tasks usable by consumers.
        for a,z in [candidate['reader_ids'],candidate['reader_ids'][::-1]]:
            if z not in readers[a]['related_readers']:readers[a]['related_readers'].append(z)
    # Expose only source records already present in V2.05 or URLs literally recorded in V2.19.
    # Preserve old access flags. They describe earlier work, never a new visit in this batch.
    dossiers=load(DOSSIERS);new_sources=[]
    for s in dossiers['sources']:
        record=copy.deepcopy(s);record['provenance']=dict(dataset=DOSSIERS,original_id=s['id']);record['exposure_note']='기존 연구 기록에서 독자용으로 옮김. 이번 회차 외부 재열람 없음.';record['revalidation_status']='NOT_REOPENED_V296'
        new_sources.append(record)
    b['sources'].extend(new_sources)
    by_url={s['url']:s['id']for s in b['sources']};sources={s['id']:s for s in b['sources']};card_by_key={};cards=[]
    for basis in b['research_basis']:
        key=basis['chapter']['key'];sid=[]
        for dossier in dossiers['dossiers']:
            if dossier['reader_key']==key:
                for source_id in dossier['reviewed_source_ids']:
                    if source_id not in sid:sid.append(source_id)
        for url in dict.fromkeys(re.findall(r'https?://[^\s]+',basis['chapter']['body'])):
            url=url.rstrip(';,')
            assert url in LEGACY_TITLES,url
            if url not in by_url:
                source_id='V296-LEGACY-'+str(len([s for s in b['sources']if s['id'].startswith('V296-LEGACY-')])+1).zfill(2)
                record=dict(id=source_id,title=LEGACY_TITLES[url],url=url,scope='REFERENCE_URL_RECORDED_IN_EXISTING_RESEARCH_NOT_REOPENED_V296',access_status='LEGACY_URL_ONLY_NOT_REOPENED_THIS_BATCH',location_note='V2.19 '+key+' 연구 본문의 출처 행',provenance=dict(dataset='data/deep/atlas_v219_structured_ten_reader_critical_editions.json',chapter_key=key),original_manuscript_read=False,original_print_folio_collated=False,revalidation_status='PENDING',exposure_note='출처 경로의 복원이다. 페이지 생존·관련 주장·판본의 재검증은 이번에 수행하지 않았다.')
                b['sources'].append(record);by_url[url]=source_id;sources[source_id]=record
            if by_url[url] not in sid:sid.append(by_url[url])
        assert sid
        title,guide=CARD_GUIDES[key]
        card=dict(id='SOURCE-CARD-'+key,reader_id='MEDIUM-'+key,title=title,reading_guide=guide,source_ids=sid,research_basis_ids=[basis['id']],verification_note='기존 연구의 참고 경로를 표시한다. 이번 회차 외부 재열람·원판 판독·문장별 감수는 하지 않았다.',status='LEGACY_REFERENCES_EXPOSED_REVALIDATION_PENDING')
        cards.append(card);card_by_key[key]=card
    communion=readers['THEME-COMMUNION'];keys=['MARBURG','AUGSBURG','CALVIN1559']
    cards.append(dict(id='SOURCE-CARD-COMMUNION',reader_id=communion['id'],title='성찬 논쟁을 비교해서 읽는 자료',reading_guide='마르부르크 합의, 아우크스부르크의 판본 변화, 칼뱅의 성례 논의를 다른 문헌으로 나누어 읽는다. 하나의 자료를 여러 교파의 공통 판정으로 삼지 않는다.',source_ids=list(dict.fromkeys(s for k in keys for s in card_by_key[k]['source_ids'])),research_basis_ids=copy.deepcopy(communion['research_basis_ids']),verification_note='세 기존 연구 원고의 참고 경로를 모았다. 비교의 모든 문장을 개별 출처와 대조한 것은 아니다.',status='LEGACY_REFERENCES_EXPOSED_REVALIDATION_PENDING'))
    for card in cards:
        c=readers[card['reader_id']];assert not c['sources']
        c['sources']=copy.deepcopy(card['source_ids']);c['source_card_id']=card['id'];c['source_basis_status']='INHERITED_REFERENCE_LINKS_EXPOSED_REVALIDATION_PENDING'
    b['reader_source_cards']=cards
    b['version']='2.96';b['kind']='EDITED_MEDIUM_CONTENT_DELIVERY_WITH_READER_SOURCE_CARDS';b['parent_commit']=PARENT
    b['editorial_note']='누적 435편을 유지하며 유사 후보 20쌍의 역할을 비교하고 20편의 반복 문단을 개정했다. 직접 출처 배열이 없던 11편에는 기존 연구의 참고 링크와 독자용 읽기 안내를 연결했다. 역사 감수나 새 외부 자료 확인을 뜻하지 않는다.'
    b['editorial_audit']=dict(previous_audit_dataset=BASE,previous_audit_status='V295_SCREENING_BASELINE_NOT_RECOMPUTED_FOR_V296',reviewed_pairs=edits,coverage=copy.deepcopy(old['editorial_audit']['coverage']),remaining_tasks=['외부 링크 생존·출처 내용의 재검증','참고 경로를 문장별 근거로 정밀 연결','다른 원고의 의미 중복·권별 균형 검토','실제 앱 스키마 대조 및 가져오기·검색·모바일 확인'],source_exposure_limit='모든 원고에 출처 ID가 있어도 모든 사실이 검증 완료되었다는 뜻은 아니다. 11편의 새 표시는 기존 연구의 참고 경로 복원이다.')
    b['consumer_contract']['source_cards']='readers[].source_card_id -> reader_source_cards[].id -> source_ids / research_basis_ids'
    b['consumer_contract']['editorial_lineage']='원래 provenance는 최초 원고, editorial_revision은 V2.95 대비 수정이다. 수정된 20편을 원본과 글자 단위로 동일하다고 표시하지 않는다.'
    b['consumer_contract']['source_context']='기존 scope·access·access_status 및 revalidation_status, 독자용 출처 안내의 verification_note를 보존한다. 새 출처 ID를 감수 완료 표시로 사용하지 않는다.'
    for p in [BASE,DOSSIERS]:b['preserved_inputs'].append(dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()))
    changed={e['edited_reader_id']for e in edits};assert len(changed)==20
    assert len({c['id']for c in b['readers']})==435
    source_ids={s['id']for s in b['sources']};assert len(source_ids)==len(b['sources'])
    card_ids={c['id']for c in cards};basis_ids={c['id']for c in b['research_basis']};ids=set(readers)
    for c in b['readers']:
        assert len(c['sections'])==3 and c['reading_question']
        assert set(c['sources'])<=source_ids and c['sources']
        assert set(c['related_readers'])<=ids and c['id']not in c['related_readers']
        assert c['title']==before[c['id']]['title'] and c['lead']==before[c['id']]['lead'] and c['reading_question']==before[c['id']]['reading_question']
        if c['id']not in changed:assert c['sections']==before[c['id']]['sections']
        else:
            e=next(e for e in edits if e['edited_reader_id']==c['id'])
            for i,s in enumerate(c['sections']):
                assert s['heading']==before[c['id']]['sections'][i]['heading']
                assert s['body']==(e['after']if i==e['section_index']else before[c['id']]['sections'][i]['body'])
    for c in cards:
        assert c['reader_id']in ids and set(c['source_ids'])<=source_ids and set(c['research_basis_ids'])<=basis_ids
        assert readers[c['reader_id']]['source_card_id']in card_ids
    for p in b['reader_groups']+b['reading_paths']+b['legacy_reading_paths']:assert set(p['reader_ids'])<=ids
    for p in b['comparisons']:assert {s['reader_id']for s in p['rows']}<=ids
    for q in b['faq']:assert set(q['related_readers'])<=ids
    assert b['research_basis']==old['research_basis']
    assert all(readers[c['id']]['sections']==c['sections']for c in old['readers']if c['id'].startswith('MEDIUM-'))
    for input_record in b['preserved_inputs']:assert hashlib.sha256((ROOT/input_record['path']).read_bytes()).hexdigest()==input_record['sha256']
    m=dict(readers=435,sections=1305,questions=435,reviewed_candidate_pairs=20,edited_readers=20,edited_sections=20,unchanged_reader_bodies=415,source_cards=len(cards),added_legacy_source_records=len(b['sources'])-len(old['sources']),source_records=len(b['sources']),unique_source_urls=len({s['url']for s in b['sources']}),body_characters_before=old['metrics']['body_characters'],body_characters=sum(len(s['body'])for c in b['readers']for s in c['sections']),characters_removed=sum(e['characters_removed']for e in edits),related_reader_links=sum(len(c['related_readers'])for c in b['readers']),new_historical_essays=0,new_external_source_visits=0,new_original_image_readings=0)
    assert m['body_characters_before']-m['body_characters']==m['characters_removed']
    b['metrics']=dict(m,reading_paths=len(b['reading_paths']),legacy_reading_paths=len(b['legacy_reading_paths']),comparisons=len(b['comparisons']),faq=len(b['faq']))
    b['publication_gate']=dict(published=False,main_changed=False,webapp_integrated=False,historian_approved=False)
    return b

def report(b):
    m=b['metrics'];by_id={c['id']:c for c in b['readers']};sources={s['id']:s for s in b['sources']}
    lines=['# V2.96 반복 설명 편집과 독자용 출처 안내','','상태: DRAFT · 공개 보류 · 실제 AI Studio 웹앱 미변경','','## 완료 범위','','V2.95의 어휘 유사도 상위 20쌍을 본문 단위로 비교하고, 각 쌍에서 한 편씩 총 20편의 문단을 줄였다. 인물·사건·문헌·주제가 맡는 설명을 구분했다. 원래 주장의 추가 검증이나 새 역사 해설 집필이 아니라 편집 개정이다. 기존 435편의 ID·제목·도입·질문을 유지했으며 세 절 구조를 보존했다. 삭제나 자동 병합은 하지 않았다.','','| 항목 | 결과 |','|---|---:|']
    for title,key in [('전체 해설','readers'),('본문 절','sections'),('읽기 질문','questions'),('비교·편집한 후보 쌍','reviewed_candidate_pairs'),('본문 개정 원고','edited_readers'),('수정한 절','edited_sections'),('본문을 그대로 유지한 원고','unchanged_reader_bodies'),('줄인 본문 문자(공백 포함)','characters_removed'),('개정 후 전체 본문 문자','body_characters'),('독자용 출처 안내','source_cards'),('기존 연구에서 노출한 추가 출처 레코드','added_legacy_source_records'),('전체 출처 레코드','source_records'),('이번 외부 자료 신규 방문','new_external_source_visits')]:lines.append('| '+title+' | '+str(m[key])+' |')
    lines+=['','## 20쌍의 편집 판단과 개정 본문','','관련 해설에는 짝 원고로 이동하는 연결을 보강했다. 이 비교는 두 원고의 역할과 반복을 검토한 것이며, 외부 사료를 대조한 역사 감수는 아니다.']
    for e in b['editorial_audit']['reviewed_pairs']:
        lines+=['','### '+str(e['rank'])+'. '+ ' / '.join(by_id[i]['title']for i in e['reader_ids']),'',e['rationale'],'','**수정 대상:** '+by_id[e['edited_reader_id']]['title']+' · '+e['heading'],'','**수정 전**','',e['before'],'','**수정 후**','',e['after'],'','줄인 문자: '+str(e['characters_removed'])+'자.']
    lines+=['','## 독자용 출처 안내 11개','','핵심 10편과 성찬 주제 1편은 출처 배열 대신 기존 연구 원고를 상속하고 있었다. 이번에는 V2.05의 자료 기록과 V2.19 연구 본문에 실제 기록된 URL을 꺼내 독자가 따라갈 수 있게 했다. 연구 본문 10편은 통합본에 계속 보존했다.','','출처 링크가 보인다는 사실과 그 출처가 모든 문장을 뒷받침한다는 판정은 다르다. 이 회차에는 링크 생존 여부·자료 내용·원판을 재열람하지 않았다. 과거의 열람 기록과 검색 발췌 기록은 그대로 보존하고 이번 재검증 상태와 구분했다.']
    for card in b['reader_source_cards']:
        lines+=['','### '+by_id[card['reader_id']]['title'],'',card['reading_guide'],'']
        for sid in card['source_ids']:
            s=sources[sid];kind=s.get('source_class',s.get('scope',s.get('access','기존 연구 참조')))
            lines.append('- ['+s['title']+']('+s['url']+') — '+kind)
        lines+=['',card['verification_note']]
    lines+=['','## 앱 전달과 이전 원고의 구분','','`'+OUT+'`은 개정된 435편과 출처 안내를 포함하는 단일 전달본이다. 이전 V2.95 전달본과 V2.19 핵심 원고, 각 회차의 원고 파일은 수정하지 않았다. 수정된 원고의 최초 위치는 `provenance`, 이번 개정 위치는 `editorial_revision`에 각각 남겼다.','','일반 목록·본문·관련 해설은 기존 필드를 계속 쓴다. 11편의 출처 읽기 안내는 `readers[].source_card_id`에서 `reader_source_cards`로 찾는다. 링크와 함께 읽기 안내 및 확인 한계를 표시해야 하며, 출처 ID 추가를 감수 완료 표시로 사용하지 않는다. 기존 비교표 6개·FAQ 12개·새 읽기 경로 18개·기존 읽기 경로 6개는 보존했다.','','## 재생성·검증','','```bash','python3 scripts/build_v296_editorial_delivery.py --check','```','','이 명령은 20개 개정 절의 전후 대응, 나머지 415편 본문 보존, 핵심 10편과 상속 연구 본문 보존, 모든 출처·관련 해설·안내·경로·비교표·FAQ 참조, 입력 체크섬 및 생성 파일 재현성을 검사한다. `--check`를 생략하면 두 산출물을 다시 만든다. 외부 네트워크와 실제 앱에 쓰지 않는다.','','기존 V2.95 재생성 검사와 검증·빌드 7종, 단일 전달본 소비 검사 및 git diff --check를 별도로 실행한다. 자동검증은 역사적 사실의 전문 감수가 아니다.','','## 남은 작업','','- 노출한 참고 자료의 링크·내용을 점검하고 문장별 근거와 연결한다.','- 이번 20쌍 이외 원고의 의미 중복과 권별 균형을 검토한다.','- 별도 개발 앱의 실제 입력 구조와 대조하고 적용 후 검색·화면 이동·모바일을 검증한다.','','main과 실제 Google AI Studio 웹앱은 변경하지 않았으며 공개 보류를 유지한다.','']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();b=build()
    for p,s in {OUT:json.dumps(b,ensure_ascii=False,indent=2)+'\n',REPORT:report(b)}.items():
        if args.check:assert (ROOT/p).read_text()==s,'Generated file drift: '+p
        else:(ROOT/p).write_text(s)
    print(json.dumps(b['metrics'],ensure_ascii=False,indent=2));print('PASS: twenty editorial diffs, unchanged bodies, inherited references, internal resolution and deterministic output')
if __name__=='__main__':main()
