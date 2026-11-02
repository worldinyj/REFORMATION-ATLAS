# V2.14 · 종교개혁 장소·사건·인물·문헌·현재 소장처 통합 연구 가제티어

이번 연구 지도 데이터는 **도시 핀 10개와 성터 위치 1개**를 제공한다. 도시는 현대 중심 좌표이며 중세·근대초 회의실·인쇄소 위치를 증명하지 않는다. 책의 인쇄 장소와 현대 소장 도서관의 좌표도 구별한다.

## 연구 지표
| 항목 | 수량 |
|---|---:|
| source_events | 19 |
| event_location_links | 19 |
| unique_places | 11 |
| geojson_features | 11 |
| historic_site_reported_coordinates | 1 |
| modern_approximate_city_centres | 10 |
| history_persons | 10 |
| historical_document_objects | 14 |
| modern_witness_holdings | 6 |
| new_source_records | 15 |
| site_essays | 11 |
| inspected_original_language_critical_transcription_records | 1 |
| source_original_folio_images_collated | 0 |
| public_geocodes_verified | 0 |
| human_scholar_approvals | 0 |
| public_items | 0 |

## 역사 장소별 심화 해설
### 코지 흐라데크 · Kozí hrádek
후스가 1413년 집필 활동을 한 코지 흐라데크 성터다. 오늘날 보이는 유적의 안내 좌표와 15세기 저술의 정확한 필사 위치는 다르다. 프라하 국립도서관 IV H 19의 소장 주소를 이 장소로 옮기지 않는다.
- 지리적 정밀도: HISTORIC_SITE_COORD_FROM_HERITAGE_WEBSITE
- 연구 좌표: 49.3898372, 14.7229983 (현재 지점 안내용)
- 근거: SRC-V214-KOZI, SRC-V214-HUS-CASTLE

### 콘스탄츠 · Konstanz
1415년 후스의 심리와 처형이 있었던 도시다. 후센슈타인과 같은 후대 기념물의 설치 지점은 처형 장소를 재현하려는 기억의 장소이지 1415년 정확한 현장 좌표라고 단정하지 않는다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 47.663, 9.176 (현재 지점 안내용)
- 근거: SRC-V214-HUS-CONST

### 비텐베르크 · Lutherstadt Wittenberg
1517년의 루터 논제와 1531년 아우크스부르크 승인 인쇄판의 배경 도시는 비텐베르크다. 학술 논제의 성문 게시 행동 자체는 논쟁의 대상이므로 성당 문에 직접 핀을 고정하지 않는다. 1530년 문서 제출은 아우크스부르크에서 벌어졌다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 51.868, 12.648 (현재 지점 안내용)
- 근거: SRC-V214-WITT, SRC-V214-AUGSBURG

### 보름스 · Worms
1521년 루터 심문과 제국 칙령의 정치적 장소다. 디지털 비평판은 5월 8일 문안과 26일 서명·공표의 단계 차이를 다룬다. 도시 중심 좌표는 황제의 서명 장소나 심문 당시 특정 방을 보장하지 않는다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 49.63, 8.36 (현재 지점 안내용)
- 근거: SRC-V214-WORMS

### 취리히 · Zürich
1523년 두 차례 종교 논쟁과 시의회 개혁이 이루어진 도시다. 1527년 펠릭스 만츠의 익사형 판결은 주립문서관 B VI 251에 남았으며 현대 비평 전사에서 원어 표현을 확인할 수 있다. 문서 소장처·도시 중심·리마트강 처형 지점을 각각 구분한다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 47.376, 8.542 (현재 지점 안내용)
- 근거: SRC-V214-ZURICH, SRC-V214-MANZ-CATALOG, SRC-V214-MANZ-TRANS

### 마르부르크 · Marburg
1529년 루터와 츠빙글리 진영의 대화와 합의문이 작성된 도시다. 합의문 제15조의 성만찬 이견과 상호 사랑 약속을 함께 설명해야 한다. 후대 편집 문서에 적힌 10월 3일과 일부 서지 기록의 3·4일 표현 차이는 별도 대조가 필요하다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 50.811, 8.77 (현재 지점 안내용)
- 근거: SRC-V214-MARBURG

### 아우크스부르크 · Augsburg
1530년 6월 25일 신앙고백이 제국의회에 제출된 도시다. 주교 궁전 건물 관련 역사 기록은 있어도 도시 중심 핀이 실제 문서 낭독 방의 위치를 뜻하지는 않는다. 이듬해 공인 인쇄본은 비텐베르크와 연결된다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 48.371, 10.898 (현재 지점 안내용)
- 근거: SRC-V214-AUGSBURG

### 바젤 · Basel
칼뱅의 『기독교강요』 1536년 라틴어 초판이 나온 인쇄 도시다. 프랑수아 1세에게 보내는 헌사 작성일이나 칼뱅이 머문 정확한 인쇄소 주소를 이 도시 좌표로 자동 확정하지 않는다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 47.56, 7.589 (현재 지점 안내용)
- 근거: SRC-V214-BASEL

### 스트라스부르 · Strasbourg
1539년 칼뱅 『기독교강요』 확대판의 인쇄 도시다. 현대 소장 도서관의 주소나 비평판 인쇄사의 다른 도시를 이 사건의 실제 출판지로 대체해서는 안 된다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 48.583, 7.752 (현재 지점 안내용)
- 근거: SRC-V214-STRASBOURG

### 제네바 · Genève
1559년 칼뱅 『기독교강요』 최종 라틴어판과 1560년 프랑스어판의 인쇄 도시다. 1560년 장 크레스팽 인쇄본의 현존 소장처는 투르로 확인되므로 제네바의 인쇄지와 프랑스 소장 기관을 별개 객체로 기록한다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 46.204, 6.144 (현재 지점 안내용)
- 근거: SRC-V214-GENEVA-1559, SRC-V214-GENEVA-1560

### 트렌토 · Trento
1545년 공의회 개회, 1547년 제6회기 의롭다 함 교령, 1563년 제23회기 신학교 규정의 도시다. 도시 중심부를 세 회의의 특정 좌석 위치로 제시하지 않으며, 각 교구의 규정 시행 장소와 분리한다.
- 지리적 정밀도: MODERN_CITY_CENTROID_APPROXIMATE
- 연구 좌표: 46.067, 11.122 (현재 지점 안내용)
- 근거: SRC-V214-TRENT

## 사건 19건: 실제 장소와 자료의 연결
- **EVENT-GEO-V214-01** 1413-01-01 ~ 1413-12-31, 후스 『De ecclesia』 저술 → PLACE-V214-KOZI (HISTORICAL_COMPOSITION_SITE); 근거 SRC-V212-HUS-MSS, SRC-V214-KOZI
- **EVENT-GEO-V214-02** 1415-07-06 ~ 1415-07-06, 후스 처형 → PLACE-V214-KONSTANZ (EXECUTION_CITY); 근거 SRC-V212-HUS, SRC-V214-HUS-CONST
- **EVENT-GEO-V214-03** 1517-10-31 ~ 1517-10-31, 루터 95개 논제 문헌일 → PLACE-V214-WITTENBERG (ACADEMIC_DOCUMENT_CITY_NOT_PROVEN_POSTING_SITE); 근거 SRC-V212-1517, SRC-V214-WITT
- **EVENT-GEO-V214-04** 1521-05-08 ~ 1521-05-08, 보름스 칙령 문안 시점 → PLACE-V214-WORMS (EDICT_PREPARATION_CITY); 근거 SRC-V212-WORMS, SRC-V214-WORMS
- **EVENT-GEO-V214-05** 1521-05-26 ~ 1521-05-26, 보름스 칙령 서명·공표 → PLACE-V214-WORMS (EDICT_ISSUANCE_CITY); 근거 SRC-V212-WORMS, SRC-V214-WORMS
- **EVENT-GEO-V214-06** 1523-01-29 ~ 1523-01-29, 취리히 첫 논쟁 → PLACE-V214-ZURICH (CIVIC_DISPUTATION_CITY); 근거 SRC-V212-ZURICH, SRC-V214-ZURICH
- **EVENT-GEO-V214-07** 1523-10-01 ~ 1523-10-31, 취리히 두 번째 논쟁 → PLACE-V214-ZURICH (CIVIC_DISPUTATION_CITY); 근거 SRC-V212-ZURICH, SRC-V214-ZURICH
- **EVENT-GEO-V214-08** 1527-01-05 ~ 1527-01-05, 펠릭스 만츠 처형 → PLACE-V214-ZURICH (EXECUTION_CITY_NOT_EXACT_SPOT); 근거 SRC-V212-ZURICH, SRC-V214-MANZ-CATALOG
- **EVENT-GEO-V214-09** 1529-10-03 ~ 1529-10-03, 마르부르크 조항 → PLACE-V214-MARBURG (COLLOQUY_ARTICLE_CITY); 근거 SRC-V212-MARBURG, SRC-V214-MARBURG
- **EVENT-GEO-V214-10** 1530-06-25 ~ 1530-06-25, 아우크스부르크 신앙고백 제출 → PLACE-V214-AUGSBURG (CONFESSION_PRESENTATION_CITY); 근거 SRC-V212-AUGSBURG, SRC-V214-AUGSBURG
- **EVENT-GEO-V214-11** 1531-01-01 ~ 1531-12-31, 라우 승인 인쇄본 → PLACE-V214-WITTENBERG (APPROVED_BOOK_PRINTING_CITY); 근거 SRC-V212-AUGSBURG, SRC-V214-AUGSBURG
- **EVENT-GEO-V214-12** 1536-01-01 ~ 1536-12-31, 기독교강요 라틴어 초판 → PLACE-V214-BASEL (BOOK_PRINTING_CITY); 근거 SRC-V212-CALVIN, SRC-V214-BASEL
- **EVENT-GEO-V214-13** 1539-01-01 ~ 1539-12-31, 기독교강요 중간 확대판 → PLACE-V214-STRASBOURG (BOOK_PRINTING_CITY); 근거 SRC-V212-CALVIN, SRC-V214-STRASBOURG
- **EVENT-GEO-V214-14** 1540-01-01 ~ 1540-12-31, Variata 수정판 → PLACE-V214-WITTENBERG (REVISED_BOOK_PRINTING_CITY); 근거 SRC-V212-VARIATA, SRC-V214-AUGSBURG
- **EVENT-GEO-V214-15** 1545-12-13 ~ 1545-12-13, 트리엔트 개회 → PLACE-V214-TRENTO (COUNCIL_OPENING_CITY); 근거 SRC-V212-TRENT, SRC-V214-TRENT
- **EVENT-GEO-V214-16** 1547-01-13 ~ 1547-01-13, 제6회기 의롭다 함 교령 → PLACE-V214-TRENTO (COUNCIL_DOCTRINAL_DECREE_CITY); 근거 SRC-V212-TRENT-DEC, SRC-V214-TRENT
- **EVENT-GEO-V214-17** 1559-01-01 ~ 1559-12-31, 기독교강요 최종 라틴어판 → PLACE-V214-GENEVA (LATIN_BOOK_PRINTING_CITY); 근거 SRC-V212-CALVIN, SRC-V214-GENEVA-1559
- **EVENT-GEO-V214-18** 1560-01-01 ~ 1560-12-31, 기독교강요 프랑스어판 → PLACE-V214-GENEVA (FRENCH_BOOK_PRINTING_CITY); 근거 SRC-V212-CALVIN, SRC-V214-GENEVA-1560
- **EVENT-GEO-V214-19** 1563-07-15 ~ 1563-07-15, 제23회기 신학교 규정 → PLACE-V214-TRENTO (COUNCIL_DISCIPLINARY_DECREE_CITY); 근거 SRC-V212-TRENT-DEC, SRC-V214-TRENT

## 현대 소장기관: 역사 사건 지도에 핀을 표시하지 않음
- **HOLD-V214-HUS-PRAHA** National Library of Czech Republic, Prague — IV H 19 fols 1r–95r. 1413 저술장소 코지 흐라데크 아님
- **HOLD-V214-WORMS-MUNICH** Bayerische Staatsbibliothek, Munich — Res/4 H.ref.287 (VD16 D 924). 보름스 1521 제국 정치 사건지와 구분
- **HOLD-V214-MANZ-ZURICH** Staatsarchiv Zürich, Zürich — B VI 251 fol 40r–41v. 주립문서관은 판결문 소장기관이며 리마트강 처형지 아님
- **HOLD-V214-AUGSBURG-DALLAS** Bridwell Library, Dallas — BRA2651/A-B. 비텐베르크 출판지·아우크스부르크 제출지 아님
- **HOLD-V214-CALVIN1559-PRINCETON** Princeton Theological Seminary Library, Princeton — Digital collection record. 제네바 인쇄지와 구분
- **HOLD-V214-CALVIN1560-TOURS** Centre d'Études Supérieures de la Renaissance, Tours — SR DB 2/14770. 제네바 장 크레스팽 인쇄지와 다른 현대 소장처

## 원어 원문 대조 단계별 구분
- DDE-WORMS-TRANSCRIPTION: SCHOLARLY_CRITICAL_EDITION_INTRODUCTION. 1521년 5월 8일 문안 처리와 26일 공표의 차이를 비평판 해설에서 확인.
- MANZ1527-GERMAN-EDITION: ORIGINAL_LANGUAGE_SCHOLARLY_TRANSCRIPTION_READ. 원어 비평 전사본이 1527년 1월 5일 익사형 판결을 포함함. 기록의 원어 전사 읽기와 필사본 사진 직접 판독은 구분.
- CALVIN1560-BOOK-CATALOGUE: PRINT_BIBLIOGRAPHIC_CATALOGUE. 인쇄지 제네바와 소장지 투르가 다름을 도서관 서지에서 확인.

## 남은 역사 지리 검증
- MANZ_RIVER: 리마트강 익사형의 실제 현장 좌표 미확정 / 지도 정책: Zürich city centre only
- MARBURG_CASTLE: 1529년 회담 장소의 성 내부 지점 미검증 / 지도 정책: Marburg city centre only
- AUGSBURG_PALACE: 1530 제국의회 문서 낭독실 좌표 미검증 / 지도 정책: Augsburg city centre only
- KONSTANZ_MEMORIAL: 후대 기념비와 1415년 현장의 위치 차이 / 지도 정책: Konstanz city centre only
- WITTENBERG_DOOR: 95개 논제 성문 게시 역사 전승 논쟁 / 지도 정책: Wittenberg city centre only
- COPY_HOLDINGS: 프라하·뮌헨·댈러스·프린스턴·투르의 소장처와 인쇄/사건 장소 분리 / 지도 정책: Holdings separate tab and NO event pin

**모든 정보는 RESEARCH_ONLY이며 지도 파일에 공개승인이나 영인 이미지 권리가 포함되지 않는다.**