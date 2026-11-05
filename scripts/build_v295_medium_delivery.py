#!/usr/bin/env python3
"""Build or verify the frozen V2.95 delivery bundle and editorial audit. Stdlib only."""
import argparse, collections, copy, hashlib, itertools, json, math, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOGUE = 'data/deep/atlas_v294_medium_depth_nordic_kingdoms_churches_bibles.json'
PREVIOUS = 'data/deep/atlas_v273_medium_content_delivery_bundle.json'
OUTPUT = 'data/deep/atlas_v295_medium_content_delivery_bundle.json'
REPORT = 'docs/01_CONTENT/V295_MEDIUM_CONTENT_INTEGRATION_AND_EDITORIAL_AUDIT.md'
PARENT = 'd2915bb0ede3653c42e1e3ba28bc26d9ec2f6ef1'

def read(path): return json.loads((ROOT / path).read_text())
def digest(value): return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def file_hash(path): return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
def normalized(text): return re.sub(r'\s+', '', text)
def body(reader): return '\n'.join(s['body'] for s in reader['sections'])

def build():
    catalogue = read(CATALOGUE)['catalogue']
    previous = read(PREVIOUS)
    previous_readers = {c['id']:c for c in previous['readers']}
    datasets = {e['dataset']:read(e['dataset']) for e in catalogue}
    readers, sources, notes = [], [], []
    for path, data in datasets.items():
        version = 'V' + re.search(r'atlas_v(\d+)_', path).group(1)
        for s in data.get('sources', []):
            sources.append(dict(copy.deepcopy(s), id=version+'-'+s['id'], provenance={'dataset':path, 'original_id':s['id']}))
        notes.append(dict(dataset=path, source_scope_note=data.get('source_scope_note',''), additional_basis=copy.deepcopy(data.get('additional_basis',[])), editorial_note=data.get('editorial_note','')))
    raw_by_id = {}
    for entry in catalogue:
        path = entry['dataset']
        raw = datasets[path]['chapters'][entry['chapter_index']]
        assert raw['id'] == entry['id']
        raw_by_id[raw['id']] = raw
        if raw['id'] in previous_readers:
            c = copy.deepcopy(previous_readers[raw['id']])
            for key in ['title','lead','sections','reading_question']:
                assert c[key] == raw[key], (c['id'], key)
        else:
            version = 'V' + re.search(r'atlas_v(\d+)_',path).group(1)
            c = copy.deepcopy(raw)
            c['sources'] = [version+'-'+s for s in raw.get('sources',[])]
            c['related_readers'] = raw.get('related_readers', ['MEDIUM-'+s for s in raw.get('related_core',[])])
            c['provenance'] = {key:entry[key] for key in ['dataset','chapter_index','reader_document']}
        c['provenance']['original_chapter_sha256'] = digest(raw)
        c['reader_type'] = c['id'].split('-')[0]
        c['source_basis_status'] = 'EXPLICIT_SOURCE_RECORDS' if c['sources'] else 'INHERITED_RESEARCH_BASIS_REQUIRES_CITATION_REVIEW'
        readers.append(c)
    ids = {c['id'] for c in readers}
    by_id = {c['id']:c for c in readers}
    source_ids = {s['id'] for s in sources}
    assert len(readers) == len(ids) == 435
    assert len(source_ids) == len(sources)
    for c in readers:
        assert len(c['sections']) == 3 and c['reading_question']
        assert set(c['sources']) <= source_ids
        assert set(c['related_readers']) <= ids
        assert c['id'] not in c['related_readers']
    # Keep legacy comparisons/FAQ and their linked readers available inside this file.
    for comparison in previous['comparisons']:
        assert {row['reader_id'] for row in comparison['rows']} <= ids
    for faq in previous['faq']:
        assert set(faq['related_readers']) <= ids
    groups = []
    for prefix, title in [('MEDIUM','핵심 해설'),('THEME','쟁점과 생활'),('REGION','지역 개관'),('GLOBAL','세계 연결'),('PERSON','인물'),('DOCUMENT','문헌'),('CITY','도시'),('EVENT','사건')]:
        groups.append(dict(id='TYPE-'+prefix,title=title,reader_ids=[c['id'] for c in readers if c['reader_type']==prefix]))
    paths = []
    def path(i, axis, title, entries, question, limit):
        selected=entries.split()
        assert len(selected)==len(set(selected)) and set(selected)<=ids,(i,set(selected)-ids)
        paths.append(dict(id=i,axis=axis,title=title,reader_ids=selected,reading_question=question,interpretive_limit=limit,status='EDITORIAL_NAVIGATION_DRAFT'))
    path('REGION-GERMAN','REGION','독일 지역: 논쟁에서 교회 질서로','MEDIUM-LUTHER1517 MEDIUM-LUTHER1521 EVENT-SPEYER_PROTEST DOCUMENT-AUGSBURG_PEACE1555 DOCUMENT-FORMULA_CONCORD','논쟁과 정치적 타협, 교파 내부 합의는 어떤 순서와 차이를 갖는가?','현대 독일 국경을 당시 제국 및 영방과 동일시하지 않는다.')
    path('REGION-SWISS','REGION','스위스 도시: 개혁과 갈라진 공동체','CITY-ZURICH MEDIUM-ZWINGLI EVENT-ZURICH_BAPTISM1525 CITY-GENEVA DOCUMENT-CONSENSUS_TIGURINUS','같은 도시 개혁에서 출발해도 다른 공동체가 형성된 이유는 무엇인가?','도시별 정책과 개혁파·재세례파의 선택을 같은 흐름으로 합치지 않는다.')
    path('REGION-ENGLISH','REGION','잉글랜드·스코틀랜드: 왕권·예배·교회 통치','REGION-ENGLAND DOCUMENT-ACT_SUPREMACY1534 DOCUMENT-COMMON_PRAYER EVENT-ELIZABETHAN_SETTLEMENT REGION-SCOTLAND DOCUMENT-FIRST_DISCIPLINE1560','왕실과 의회, 성직자와 회중은 교회 질서에 어떻게 관여했는가?','두 왕국의 법적 질서와 개혁 시기를 구분한다.')
    path('REGION-FRENCH-LOW','REGION','프랑스·저지대: 박해·항쟁·공존','REGION-FRANCE EVENT-ST_BARTHOLOMEW1572 DOCUMENT-NANTES_EDICT1598 REGION-LOW_COUNTRIES DOCUMENT-ACT_ABJURATION1581 EVENT-UTRECHT1579','종교적 보호와 통치권의 변화는 어떤 관계를 맺었는가?','지역을 가로지르는 비교 순서이며 전체가 하나의 연대순 사건 사슬은 아니다.')
    path('REGION-NORDIC','REGION','북유럽: 왕의 개혁과 지역의 적용','REGION-DENMARK_NORWAY PERSON-CHRISTIAN_III EVENT-NORWAY_REFORMATION1537 REGION-SWEDEN DOCUMENT-SWEDISH_ORDINANCE1571 REGION-ICELAND EVENT-SKALHOLT_EXECUTIONS1550 DOCUMENT-GUDBRANDUR_BIBLE1584','공통된 왕권이나 교파 아래서 지역의 전환 시기는 왜 달랐는가?','선정된 지역을 비교하는 경로이며 전체가 연대순은 아니다.')
    path('REGION-EAST-GLOBAL','REGION','동중부 유럽과 세계: 언어·선교·권한','REGION-POLAND_LITHUANIA REGION-TRANSYLVANIA DOCUMENT-TRUBAR_CATECHISM1550 GLOBAL-INDIA_JAPAN PERSON-XU_GUANGQI DOCUMENT-NUEVA_CORONICA1615','새로운 언어와 현지 참여자는 종교 변화에 어떤 역할을 했는가?','지리적 비교이며 모두를 같은 교파나 같은 개혁 운동의 직접 결과로 묶지 않는다.')
    path('TIME-BACKGROUND','CHRONOLOGY','14~15세기 배경에서 1516년까지','MEDIUM-WYCLIFFE MEDIUM-HUS EVENT-WITTENBERG_UNIVERSITY1502 DOCUMENT-ERASMUS_NT1516','중세의 문제 제기와 대학·원어 연구는 어떻게 다른 배경을 제공했는가?','후대 종교개혁으로 향하는 필연적 진보나 직접 영향 관계를 뜻하지 않는다.')
    path('TIME-1517-1525','CHRONOLOGY','1517~1525년: 공개 논쟁과 번역','DOCUMENT-NINETY_FIVE1517 EVENT-LEIPZIG1519 MEDIUM-LUTHER1521 DOCUMENT-SEPTEMBER_TESTAMENT EVENT-ZURICH_BAPTISM1525 DOCUMENT-TWELVE_ARTICLES','교회 권위에 대한 논쟁은 어떤 서로 다른 행동으로 이어졌는가?','같은 시기라는 이유만으로 모든 사건을 하나의 진영이나 인과 사슬로 연결하지 않는다.')
    path('TIME-1527-1541','CHRONOLOGY','1527~1541년: 고백과 도시·왕국의 결정','DOCUMENT-SCHLEITHEIM MEDIUM-AUGSBURG MEDIUM-CALVIN1536 EVENT-COPENHAGEN1536 DOCUMENT-DANISH_ORDINANCE1537_1539 DOCUMENT-GENEVA_ORDINANCES1541','공동체의 고백과 통치자의 결정은 어떻게 제도에 남았는가?','연대별 선택 사례이며 지역별 발전 단계나 우열을 뜻하지 않는다.')
    path('TIME-1542-1563','CHRONOLOGY','1542~1563년: 공의회·전쟁·법적 타협','EVENT-ROMAN_INQUISITION1542 EVENT-SCHMALKALD_WAR1546 DOCUMENT-AUGSBURG_PEACE1555 EVENT-ELIZABETHAN_SETTLEMENT EVENT-WASSY1562 DOCUMENT-HEIDELBERG_CATECHISM','교파 경계의 확립과 정치적 공존은 어떤 긴장을 만들었는가?','선택된 사례 목록으로 트리엔트 공의회 등 해당 시기 전체 사건을 대체하지 않는다.')
    path('TIME-1564-1598','CHRONOLOGY','1564~1598년: 교파 형성과 공존의 조건','DOCUMENT-PROFESSIO_FIDEI1564 DOCUMENT-ROMAN_MISSAL1570 DOCUMENT-WARSAW_CONFEDERATION DOCUMENT-FORMULA_CONCORD EVENT-UPPSALA1593 DOCUMENT-NANTES_EDICT1598','공동의 신앙 기준과 다른 신앙의 보호는 어떻게 함께 나타났는가?','각 법과 문헌이 보호하거나 제외한 집단은 서로 다르다.')
    path('TIME-1603-1658','CHRONOLOGY','1603~1658년: 교육·전쟁·보호의 축소','DOCUMENT-TIANZHU_SHIYI1603 DOCUMENT-KING_JAMES_BIBLE1611 EVENT-DORT1618 EVENT-WHITE_MOUNTAIN1620 EVENT-PEACE_PRAGUE1635 EVENT-POLISH_BRETHREN1658','17세기의 제도와 전쟁은 앞선 공존의 조건을 어떻게 바꾸었는가?','유럽과 아시아의 비교이며 직접적인 사건 간 인과나 동일한 정치 질서를 뜻하지 않는다.')
    path('ISSUE-AUTHORITY','ISSUE','성경과 권위: 누가 판단하는가','PERSON-ERASMUS THEME-SCRIPTURE_AUTHORITY MEDIUM-LUTHER1521 DOCUMENT-HOOKER_LAWS DOCUMENT-PROFESSIO_FIDEI1564','성경의 권위에 동의하면서도 해석과 통치의 기준은 왜 달랐는가?','현재 교파의 정답을 역사 전체에 거슬러 적용하지 않는다.')
    path('ISSUE-TRANSLATION','ISSUE','번역·인쇄·독자: 책은 어떻게 전해졌는가','THEME-PRINT_TRANSLATION DOCUMENT-ERASMUS_NT1516 DOCUMENT-LUTHER_BIBLE1534 DOCUMENT-GUSTAV_VASA_BIBLE1541 DOCUMENT-GUDBRANDUR_BIBLE1584 DOCUMENT-LIMA_CATECHISM1584','언어·후원·인쇄 장소는 책의 제작과 사용에 어떤 차이를 만들었는가?','모든 번역이 개신교의 저술은 아니며 출판과 실제 소유·독서를 구분한다.')
    path('ISSUE-COMMUNION','ISSUE','성찬과 예배: 같은 식탁의 다른 기준','THEME-COMMUNION MEDIUM-MARBURG DOCUMENT-CONSENSUS_TIGURINUS DOCUMENT-COMMON_PRAYER DOCUMENT-ROMAN_MISSAL1570 DOCUMENT-RED_BOOK1576','교리의 설명과 예배의 구체적인 형식은 어디서 만나는가?','성례 합의와 예배서 채택을 같은 범위의 일치로 설명하지 않는다.')
    path('ISSUE-COEXISTENCE','ISSUE','강제·피난·공존: 누구를 보호했는가','THEME-REFUGEES PERSON-CASTELLIO THEME-AUGSBURG_PEACE DOCUMENT-WARSAW_CONFEDERATION EVENT-EDICT_NANTES DOCUMENT-NANTES_EDICT1598','양심·시민적 권리·공적 예배의 허용은 어떻게 달랐는가?','법적 보호를 현대의 보편적 종교 자유와 동일시하지 않는다.')
    path('ISSUE-DAILY-LIFE','ISSUE','교육·구빈·가족: 본당의 일상','THEME-EDUCATION THEME-POOR_RELIEF THEME-WOMEN_FAMILY THEME-MARRIAGE_COURTS PERSON-PEDER_PALLADIUS THEME-PARISH_REGISTERS','새 규정은 생활의 어떤 부분에 개입했으며 실제 이행은 어떻게 확인하는가?','중앙 규정의 존재가 모든 지역 주민의 동일한 경험을 보장하지 않는다.')
    path('ISSUE-MEMORY','ISSUE','기록과 기억: 당사자의 말과 후대의 해석','PERSON-JOHN_FOXE PERSON-JEAN_CRESPIN DOCUMENT-MAGDEBURG_CENTURIES PERSON-GUAMAN_POMA EVENT-STANGEBRO1598','자료 작성자의 목적과 후대의 기념은 사건의 이해에 어떤 영향을 주는가?','서로 다른 장르의 기록을 중립적인 사건 집계로 취급하지 않는다.')
    # This index is an editorial reading order, NOT a date database inferred from IDs.
    assert collections.Counter(p['axis'] for p in paths)=={'REGION':6,'CHRONOLOGY':6,'ISSUE':6}
    research_basis=[]
    core_path='data/deep/atlas_v219_structured_ten_reader_critical_editions.json'
    core=read(core_path)
    for c in readers:
        if not c['sources']:
            basis=c.get('basis',c.get('existing_basis',{}))
            assert basis.get('dataset')==core_path
            keys=basis.get('chapter_keys',[basis.get('chapter_key')])
            c['research_basis_ids']=[]
            for chapter_key in keys:
                chapter=next(k for k in core['chapters'] if k['key']==chapter_key)
                key='BASIS-V219-'+chapter['key']
                c['research_basis_ids'].append(key)
                if not any(b['id']==key for b in research_basis):
                    research_basis.append(dict(id=key,dataset=core_path,chapter=copy.deepcopy(chapter),source_notes=[n for n in core['source_notes'] if n.get('reader_key')==chapter['key']],scope='EXISTING_EDITORIAL_RESEARCH_NOT_NEW_HISTORICAL_VERIFICATION',status='DRAFT'))
        else: c['research_basis_ids']=[]
    # Fingerprint checks are exact textual checks, not an originality or plagiarism verdict.
    fingerprints=collections.defaultdict(list)
    paragraphs=collections.defaultdict(list)
    for c in readers:
        fingerprints[normalized(body(c))].append(c['id'])
        for n,s in enumerate(c['sections']):paragraphs[normalized(s['body'])].append(dict(reader_id=c['id'],section_index=n))
    exact=[v for v in fingerprints.values() if len(v)>1]
    repeated=[v for v in paragraphs.values() if len(v)>1]
    # Word TF-IDF cosine, with numbers/punctuation stripped. Rank only; no automatic deletion.
    token_counts=[collections.Counter(re.findall(r'[가-힣A-Za-z]{2,}',body(c))) for c in readers]
    df=collections.Counter(t for c in token_counts for t in c)
    vectors=[]
    for counts in token_counts:
        v={t:(1+math.log(n))*math.log(1+len(readers)/df[t]) for t,n in counts.items()}
        norm=math.sqrt(sum(w*w for w in v.values()))
        vectors.append({t:w/norm for t,w in v.items()})
    similarities=[]
    for i,j in itertools.combinations(range(len(readers)),2):
        a,b=vectors[i],vectors[j]
        if len(a)>len(b):a,b=b,a
        score=sum(w*b.get(t,0) for t,w in a.items())
        similarities.append((score,i,j))
    ranked=[dict(reader_ids=[readers[i]['id'],readers[j]['id']],score=round(s,6),status='EDITORIAL_REVIEW_CANDIDATE_NOT_CONFIRMED_DUPLICATE') for s,i,j in sorted(similarities,reverse=True)[:20]]
    decisions=[
      dict(reader_ids=['EVENT-EDICT_NANTES','DOCUMENT-NANTES_EDICT1598'],status='RETAIN_COMPLEMENTARY_WITH_OVERLAP',evidence='개설은 협상·권리·시행과 철회를 설명하고, 문헌 해설은 특별 조항·별도 보장·사본과 등록본을 구분한다. 예배 제한과 공포·시행의 구분은 반복된다.',next_action='사건 개설을 먼저 읽고 문헌으로 이동하도록 경로에 배치했다. 추후 편집 시 반복 설명을 줄이되 지금은 원고를 보존한다.'),
      dict(reader_ids=['THEME-AUGSBURG_PEACE','DOCUMENT-AUGSBURG_PEACE1555'],status='RETAIN_COMPLEMENTARY_WITH_OVERLAP',evidence='주제 개설은 1530년과 1555년의 구분 및 영방·이주·성과를 설명하고, 문헌 해설은 보호 제외 집단과 성직 영주의 직무·재산 문제를 보강한다. 이주와 현대 종교 자유의 구분은 반복된다.',next_action='주제에서 문헌으로 이어 읽는다. 향후 공통 설명의 분량을 줄이고 조항의 차이를 더 선명히 편집한다.')]
    incoming=collections.Counter(t for c in readers for t in c['related_readers'])
    coverage=[
      dict(volume='VOL-01',title='초대·고대교회',status='DEFERRED_NOT_ASSESSED',representative_reader_ids=[],gap='이번 435편 목록은 고대교회 전 범위의 집필 완료 근거가 아니다.'),
      dict(volume='VOL-02',title='중세교회와 개혁 배경',status='SELECTED_BACKGROUND_ONLY',representative_reader_ids=['MEDIUM-WYCLIFFE','MEDIUM-HUS'],gap='중세 전 시대·동방교회·수도 전통을 포괄하는 목차와 목표량은 미확정이다.'),
      dict(volume='VOL-03',title='종교개혁의 선구자',status='DRAFT_COVERAGE_PRESENT',representative_reader_ids=['MEDIUM-WYCLIFFE','MEDIUM-HUS','REGION-WALDENSIAN_VALLEYS'],gap='대표 원고는 있으나 권 전체의 누락 점검과 역사 감수는 별도다.'),
      dict(volume='VOL-04',title='16세기 종교개혁',status='BROAD_DRAFT_COVERAGE',representative_reader_ids=['MEDIUM-LUTHER1517','MEDIUM-ZWINGLI','MEDIUM-CALVIN1559','REGION-ENGLAND','THEME-ANABAPTISTS'],gap='개혁파·루터파·재세례파와 지역 간 균형을 검토하고 유사 주제의 중복을 정리해야 한다.'),
      dict(volume='VOL-05',title='가톨릭 개혁과 갈등',status='BROAD_DRAFT_COVERAGE',representative_reader_ids=['MEDIUM-TRENT','THEME-CATHOLIC_RENEWAL','EVENT-ST_BARTHOLOMEW1572','DOCUMENT-NANTES_EDICT1598'],gap='교리·전례·교육·강제·공존의 설명 균형 및 출처별 확인 수위를 검토해야 한다.'),
      dict(volume='VOL-06',title='부흥과 세계선교',status='EARLY_MODERN_PRECURSORS_ONLY',representative_reader_ids=['DOCUMENT-TRUE_CHRISTIANITY','EVENT-PROPAGANDA1622'],gap='웨슬리·대각성 등 후대 부흥을 다룬 독립 항목은 현재 목록에 없다. 초기 근대 사례로 완성을 주장하지 않는다.'),
      dict(volume='VOL-07',title='세계와 한국 교회사',status='SELECTED_EARLY_GLOBAL_CONNECTIONS',representative_reader_ids=['GLOBAL-AMERICAS','GLOBAL-INDIA_JAPAN','GLOBAL-CHINA','PERSON-GUAMAN_POMA'],gap='한국 교회사와 후대 아프리카·아시아의 전개를 포괄하는 독립 구성은 현재 목록에서 확인되지 않는다.'),
      dict(volume='VOL-08',title='사상과 문헌 아카이브',status='BROAD_DRAFT_COVERAGE',representative_reader_ids=['THEME-SCRIPTURE_AUTHORITY','THEME-COMMUNION','DOCUMENT-LUTHER_BIBLE1534','DOCUMENT-ROMAN_MISSAL1570'],gap='문헌 목록의 폭과 원판 직접 검토의 깊이는 다르며 전체 판본 대조·전문 감수는 미완이다.')]
    for v in coverage:assert set(v['representative_reader_ids'])<=ids
    audit=dict(method='435편 전수 텍스트·참조 검사, 94,395쌍의 어휘 유사도 순위, 별도 2쌍의 본문 비교. 역사적 정확성 전수 감수가 아니다.',exact_duplicate_bodies=exact,exact_repeated_sections=repeated,similarity_method='본문 한글·영문 2자 이상 어휘의 TF-IDF cosine. 활용형·동의어를 정규화하지 않는 편집 후보 추출이다. 순위는 중복 확정이나 표절 판정이 아니다.',ranked_review_candidates=ranked,reviewed_pairs=decisions,readers_without_outgoing_links=[c['id'] for c in readers if not c['related_readers']],readers_without_incoming_links=[c['id'] for c in readers if not incoming[c['id']]],readers_with_inherited_basis_only=[c['id'] for c in readers if not c['sources']],coverage=coverage)
    used_sources={s for c in readers for s in c['sources']}
    metrics=dict(readers=len(readers),sections=sum(len(c['sections'])for c in readers),questions=len(readers),body_characters=sum(len(s['body'])for c in readers for s in c['sections']),source_records=len(sources),unique_source_urls=len({s['url']for s in sources}),source_datasets=len(datasets),used_source_records=len(used_sources),inherited_research_basis=len(research_basis),related_reader_links=sum(len(c['related_readers'])for c in readers),type_groups=len(groups),new_reading_paths=len(paths),legacy_reading_paths=len(previous['reading_paths']),comparisons=len(previous['comparisons']),faq=len(previous['faq']),body_pairs_screened=len(similarities),exact_duplicate_body_groups=len(exact),exact_repeated_section_groups=len(repeated),ranked_review_candidates=len(ranked),editorially_reviewed_pairs=len(decisions),new_historical_essays=0)
    inputs=[CATALOGUE,PREVIOUS]+list(datasets)+[core_path]
    bundle=dict(version='2.95',kind='MEDIUM_CONTENT_DELIVERY_AND_EDITORIAL_AUDIT',status='DRAFT',depth='MEDIUM',parent_commit=PARENT,editorial_note='기존 435편의 본문을 보존한 통합 전달본이다. 이번 회차는 신규 집필 대신 통합·편집 점검·탐색 경로를 완성한다. 자동검증과 역사 감수를 구분하며 실제 앱은 변경하지 않는다.',preserved_inputs=[dict(path=p,sha256=file_hash(p)) for p in dict.fromkeys(inputs)],readers=readers,sources=sources,research_basis=research_basis,reader_groups=groups,reading_paths=paths,legacy_reading_paths=copy.deepcopy(previous['reading_paths']),comparisons=copy.deepcopy(previous['comparisons']),faq=copy.deepcopy(previous['faq']),source_dataset_notes=notes,editorial_audit=audit,consumer_contract=dict(reader_lookup='readers[].id',source_lookup='readers[].sources -> sources[].id',basis_lookup='readers[].research_basis_ids -> research_basis[].id',navigation='reader_groups[].reader_ids / reading_paths[].reader_ids -> readers[].id',comparison='comparisons[].rows[].reader_id -> readers[].id',faq='faq[].related_readers -> readers[].id',source_context='scope·access·provenance·source_dataset_notes를 보존한다.',source_id_policy='자료별 V번호-원래ID. URL이 같아도 서로 다른 확인 수위를 합치지 않는다.',load_policy='본문·출처 레코드·상속 연구 본문·탐색은 이 파일 안에서 해석 가능하다. provenance 파일은 상세 감사 추적용이며 일반 화면 이동을 위해 로드할 필요가 없다.',search='title·lead·sections[].heading·sections[].body를 로컬 인덱싱 가능. 원시 JSON 안의 판본 ID나 검증 메타데이터를 일반 본문으로 노출하지 않는다.',chronology='CHRONOLOGY 경로는 편집자가 선정한 읽기 순서다. 각 항목의 정확한 연대 필드나 지도 좌표 데이터로 사용하지 않는다.',publication='EDITORIAL_DRAFT. 실제 앱 가져오기·검색·모바일 검증·공개 승인은 별도다.'),metrics=metrics,publication_gate=dict(published=False,main_changed=False,webapp_integrated=False,historian_approved=False))
    # Complete local resolution and legacy text preservation.
    basis_ids={b['id']for b in research_basis}
    for c in readers:
        assert set(c['research_basis_ids'])<=basis_ids
        raw=raw_by_id[c['id']]
        assert all(c[k]==raw[k]for k in ['title','lead','sections','reading_question'])
    for c in previous['readers']:
        assert all(by_id[c['id']][k]==c[k]for k in ['title','lead','sections','reading_question','sources','related_readers'])
    assert set(itertools.chain.from_iterable(g['reader_ids']for g in groups))==ids
    assert sum(len(g['reader_ids'])for g in groups)==435
    assert len({p['id']for p in paths})==len(paths)
    for p in previous['reading_paths']:assert set(p['reader_ids'])<=ids
    return bundle

def markdown(b):
    m=b['metrics'];a=b['editorial_audit'];names={c['id']:c['title']for c in b['readers']}
    lines=['# V2.95 심화정보 435편 통합·편집 점검·앱 전달 안내','','상태: DRAFT · 공개 보류 · 실제 AI Studio 웹앱 미변경','','## 이번 회차의 목적','','추가 집필을 반복하기보다 누적 원고를 실제로 전달하고 읽을 수 있게 정리한다. 신규 역사 해설은 0편이며 기존 435편을 한 파일로 통합했다. 본문·제목·도입·질문은 원래 원고와 일치한다. 출처 ID에 자료별 V번호를 붙여 충돌을 피하고 접근 범위와 상속 연구 근거를 보존했다.','','## 통합 결과','','| 항목 | 수량 |','|---|---:|']
    for title,key in [('해설','readers'),('본문 절','sections'),('읽기 질문','questions'),('본문 문자(공백 포함)','body_characters'),('출처 레코드(고유 URL 수와 다름)','source_records'),('고유 출처 URL 문자열','unique_source_urls'),('원고가 수록된 데이터 파일','source_datasets'),('상속 연구 본문','inherited_research_basis'),('관련 해설 연결','related_reader_links'),('분야별 목록','type_groups'),('새 읽기 경로','new_reading_paths'),('기존 읽기 경로 보존','legacy_reading_paths'),('기존 비교표 보존','comparisons'),('기존 FAQ 보존','faq')]:lines.append('| '+title+' | '+str(m[key])+' |')
    lines+=['','출처 레코드 수는 독립적인 사료·기관의 수가 아니다. 동일 URL이 여러 회차에서 다른 범위로 기록될 수 있어 레코드를 임의로 합치지 않았다. URL의 생존 여부나 본문 정확성을 이번에 전수 재조회하지 않았다.','','## 분야별 현황','','| 분야 | 해설 수 |','|---|---:|']
    for g in b['reader_groups']:lines.append('| '+g['title']+' | '+str(len(g['reader_ids']))+' |')
    lines+=['','## 지역·연대·쟁점별 읽기 경로','','각 축 6개씩 총 18개다. 연대 경로는 편집 순서이며 모든 항목의 정밀 연대를 제공하는 데이터베이스가 아니다. 지역 경로는 비교를 위해 시기를 오갈 수 있다. 이 경로에 포함되지 않은 항목도 분야 목록에서 모두 접근할 수 있다.']
    for p in b['reading_paths']:
        lines+=['','### '+p['title'],'',' → '.join(names[i] for i in p['reader_ids']),'','**질문:** '+p['reading_question'],'','**해석의 범위:** '+p['interpretive_limit']]
    lines+=['','## 중복·누락 점검','','435편의 본문과 참조를 전수 검사했다. 본문 전체를 비교한 '+str(m['body_pairs_screened'])+'쌍 중 공백 제거 후 완전히 같은 본문 묶음은 '+str(m['exact_duplicate_body_groups'])+'개, 완전히 같은 절 묶음은 '+str(m['exact_repeated_section_groups'])+'개다. 이 수치는 의미가 비슷한 설명이 없다는 뜻이 아니다. 어휘 유사도 상위 20쌍은 편집 후보로 기록했으며 자동으로 삭제하거나 합치지 않았다.','','### 본문을 비교한 두 쌍']
    for d in a['reviewed_pairs']:
        lines+=['','- **'+names[d['reader_ids'][0]]+' / '+names[d['reader_ids'][1]]+'**: '+d['evidence']+' '+d['next_action']]
    lines+=['','### 어휘 유사도 상위 후보','','점수는 한글·영문 2자 이상 어휘의 TF-IDF cosine 값이다. 활용형·동의어를 정규화하지 않아 편집 우선순위를 잡는 보조 자료로만 쓴다. 전체 본문의 의미 중복이나 표절을 판정한 것이 아니다.','','| 순위 | 첫 해설 | 둘째 해설 | 점수 |','|---:|---|---|---:|']
    for i,p in enumerate(a['ranked_review_candidates'],1):lines.append('| '+str(i)+' | '+names[p['reader_ids'][0]]+' | '+names[p['reader_ids'][1]]+' | '+str(p['score'])+' |')
    lines+=['','### 연결과 출처의 남은 편집 과제','','- 직접 출처 배열 대신 이전 연구 근거를 상속한 원고: '+str(len(a['readers_with_inherited_basis_only']))+'편. 해당 핵심 연구 본문 10편과 기존 사료 주석을 `research_basis`에 함께 담았다. 이것은 모든 문장의 출처를 새로 확인했다는 뜻이 아니다.','- 관련 해설로 나가는 연결이 없는 원고: '+str(len(a['readers_without_outgoing_links']))+'편. 원래 연결을 임의로 추가하지 않았으며 분야 목록에서 모두 접근할 수 있다.','- 다른 원고의 관련 해설에서 들어오는 연결이 없는 원고: '+str(len(a['readers_without_incoming_links']))+'편. 전체 ID는 JSON의 편집 점검 항목에 기록했다. 읽기 경로와 분야 목록은 별도 탐색 수단이다.','','## 8권 계획의 현재 범위와 공백','','이 표는 대표 해설의 존재를 점검한 것이다. 권별 목표 수량이 확정되지 않아 완료율을 계산하지 않으며, 대표 항목이 있다는 이유로 그 권을 완성으로 판정하지 않는다.','','| 권 | 확인한 범위 | 대표 항목 | 남은 범위 |','|---|---|---|---|']
    labels={'DEFERRED_NOT_ASSESSED':'후속 범위·미평가','SELECTED_BACKGROUND_ONLY':'일부 배경 원고','DRAFT_COVERAGE_PRESENT':'대표 초안 확보','BROAD_DRAFT_COVERAGE':'폭넓은 초안 확보','EARLY_MODERN_PRECURSORS_ONLY':'초기 근대 사례 중심','SELECTED_EARLY_GLOBAL_CONNECTIONS':'일부 초기 세계 연결'}
    for v in a['coverage']:lines.append('| '+v['volume']+' '+v['title']+' | '+labels[v['status']]+' | '+', '.join(names[i] for i in v['representative_reader_ids'])+' | '+v['gap']+' |')
    lines+=['','## 앱 개발자에게 전달할 파일','','`'+OUTPUT+'` 하나에서 435편 본문, 자료별 출처, 상속 연구 본문, 분야 목록과 읽기 경로, 기존 비교표·FAQ를 읽을 수 있다. 과거 35개 원고 데이터 파일을 앱에서 순서대로 불러올 필요가 없다.','','| 화면 기능 | 파일 안의 위치 | 연결 기준 |','|---|---|---|','| 목록·상세 | `readers` | `id` |','| 관련 해설 | `readers[].related_readers` | 같은 파일의 해설 ID |','| 출처 | `sources` | 자료별 V번호를 붙인 출처 ID |','| 상속 연구 근거 | `research_basis` | `readers[].research_basis_ids` |','| 분야 목록 | `reader_groups` | `reader_ids` |','| 지역·연대·쟁점 탐색 | `reading_paths` | `axis`, `reader_ids` |','| 기존 비교·질문 | `comparisons`, `faq`, `legacy_reading_paths` | 기존 해설 ID |','','목록에는 제목과 도입을, 상세에는 본문 세 절과 질문을 표시한다. 출처의 scope/access 및 확인 한계를 보존한다. 편집용 provenance·검증 상태는 본문과 분리해 다룬다. `source_basis_status`가 상속 연구인 원고를 출처가 전혀 없거나 감수 완료인 것으로 표시해서는 안 된다. 연대 경로에서 지도 좌표나 정확한 날짜를 자동 추출하지 않는다.','','## 검증과 재생성','','저장소 루트에서 다음 명령을 사용한다.','','```bash','python3 scripts/build_v295_medium_delivery.py --check','```','','이 명령은 모든 입력 파일 체크섬, 435편 본문의 원본 일치, 자료별 출처 ID의 유일성, 관련 해설·분야·경로·비교표·FAQ 참조, 상속 연구 연결, 생성 파일의 재현성을 검사한다. `--check`를 생략하면 동일한 두 산출물을 다시 생성한다. 외부 네트워크나 앱에 쓰지 않는다.','','기존 검증·빌드 7종 및 git diff --check도 별도로 실행한다. 역사적 사실의 전문 감수, 외부 출처 재조회, 실제 앱의 가져오기·검색·모바일 화면 검증은 이 구조 검사와 다른 작업이다.','','## 다음 우선순위','','1. 어휘 유사도 상위 후보를 본문 단위로 검토하고 필요한 공통 설명을 줄인다.','2. 직접 출처 배열이 없는 11편(핵심 10편과 성찬 주제)의 기존 연구 근거를 독자용 출처 표기로 정리한다.','3. 현재 16세기 중심의 범위를 유지할지 확인한 뒤 권별 필수 항목을 정한다. 고대·후대 부흥·한국사를 기존 435편의 완료 범위로 계산하지 않는다.','4. 별도 개발 앱의 실제 입력 구조와 대조하고 전달본을 적용한 뒤 검색·연결·모바일을 확인한다.','','기존 핵심 원고 10편·543문장과 이전 추적 파일은 보존한다. main과 실제 Google AI Studio 웹앱은 변경하지 않았으며 공개 보류를 유지한다.','']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    b=build(); outputs={OUTPUT:json.dumps(b,ensure_ascii=False,indent=2)+'\n',REPORT:markdown(b)}
    for p,text in outputs.items():
        if args.check:assert (ROOT/p).read_text()==text, 'Generated file drift: '+p
        else:(ROOT/p).write_text(text)
    print(json.dumps(b['metrics'],ensure_ascii=False,indent=2));print('PASS: original text, references, preserved input hashes, deterministic delivery and editorial report')
if __name__=='__main__': main()
