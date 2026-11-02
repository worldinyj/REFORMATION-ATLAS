# 종교개혁 ATLAS V2.23 — 마르부르크 1529년 문헌의 본문·판본·날짜 증거 분리

> **연구 전용 / 공개 HOLD.** 기존 V2.19 10편 74절 128문단 543문장 35,102코드포인트, 30개 주장 위치 및 30개 탐색 연결을 변경하지 않는다. V2.20~V2.22는 덮어쓰지 않는다. V2.23에서 **1529년 원본 판면 직접 판독은 0건**이다.

## 1. 실제 추가 작업과 현재의 도달 수준

이번에는 서로 다른 유형의 자료에 접근한 결과를 개별 기록으로 관리했다.

| 출처 | 실제 확인 | 확인하지 못한 것 |
|---|---|---|
| [GHDI 독일어 전사](https://germanhistorydocs.org/de/von-den-reformationen-bis-zum-dreissigjaehrigen-krieg-1500-1648/die-marburger-religionsgespraeche-die-marburger-artikel-1529) | **직접 HTML 본문 접근 성공**. 제7·13·15조 문맥을 1910년 *Weimarer Ausgabe*에 기초한 편집 독일어 전사에서 확인 | 서명 필사본 K/Z의 정확한 글자·변형 |
| [DigiRef 학술 아카이브](https://flugschriften.reformationsportal.de/recherche-im-gesamtbestand/listeneinstieg?cHash=b4cace5da9c214d4d23e5163b49d0c2c&tx_joreformation_pi1004listenuebersicht%5Baction%5D=detail&tx_joreformation_pi1004listenuebersicht%5Bcontroller%5D=Mapservice&tx_joreformation_pi1004listenuebersicht%5BjoDel%5D=1&tx_joreformation_pi1004listenuebersicht%5BjoDetailView%5D=stat_showcase_00000023) | K 소장원본 Best.3 Nr.245, 60r–64v, 학술 편집자 Clemens Joos, **자료 날짜 1529-10-04** 등 검색 색인의 상세 메타데이터 확인 | 실제 원본 영상: 직접 접근 시 자동 접속제한 페이지로 대체 |
| [e-rara W2119 개별 서지](https://www.e-rara.ch/zuz/content/titleinfo/170052) | ZB Zürich 5.174,5 = **VD16 W2119**, [4]잎, Froschauer 1529; **Public Domain Mark**, 자유 다운로드 안내 및 DOI | 실제 이미지와 IIIF 매니페스트: 이 환경에서는 직접 열리지 않음 |
| [취리히 원본 Z 목록](https://suche.staatsarchiv.djiktzh.ch/detail.aspx?ID=618165) | 1529-10-03, **제7·13·15조 Z 추가 문구가 K에는 없다는 소장 기록** | Z 사본의 추가 문구 원형·행 번호·여백 기입 형태 |
| [HAPuls 원본 이미지 자료](https://www.hapuls.de/node/1472) | K 원본 이미지 전체를 소개하는 공개 항목, 소장 정보 | 네트워크 시간초과로 이미지 바이트 획득 실패 |

**중요:** GHDI에서 읽은 독일어 텍스트는 1529년 기록에 기반한 **후대 편집 전사**다. 원본 필사본 화면을 직접 판독했다고 표현하지 않는다. HAPuls의 [별도 현대어 페이지](https://www.hapuls.de/node/1473)는 Oberman 1994년 편집본에 기초하여 제시되므로 독일어 현대화 표현을 원문 철자와 섞지 않는다.

## 2. 1910년 편집 전사에서 직접 확인한 제7·13·15조의 문맥

| 조항 | 짧은 독일어 문맥 표지 | 연구자의 한국어 요지 | 원본 Z/K 이문 |
|---|---|---|---|
| **7** | `glaube sey vnser gerechtigkeit fur got` | 믿음에 의한 하나님 앞의 의와, 그리스도를 통해 의롭게 여김받는 논리 | **미판독** |
| **13** | `mag man frey halten oder lassen` | 교회 관습이 명백히 하나님의 말씀에 어긋나지 않는 경우의 자유와 이웃을 배려한 질서 | **미판독** |
| **15** | `dißer Zeit nit vergleicht haben` | 성만찬에 관해 공유하는 신앙과 그리스도 몸·피의 육체적 현존에 남은 불일치, 상호 사랑 | **미판독** |

위의 짧은 인용은 모두 GHDI에 게재된 1910년 편집 전사의 **조항 위치를 식별하는 표지**이다. 취리히 원본에만 더해진 구절의 직접 인용이 아니다. 특히 제15조에서 '완전히 합의하지 못했다'는 취지를, 15개 조항 전부에 합의하지 않았다고 확대 해석하면 안 된다. 나머지 조항의 신앙 고백과 성만찬의 미해결 쟁점을 함께 설명해야 한다.

데이터셋에서 `PASS-V223-ART07/13/15`는 기존 `V220-MAR-07/13/15` 및 V2.19 연결 문장 ID에 연결되지만, `z_added_wording`, `k_parallel_wording`, `manuscript_folio`를 모두 **null**로 보존한다. 따라서 CI 통과가 실제 추가 구절의 원문 확보를 의미하지 않는다.

## 3. 1529년 10월 3일과 4일: 날짜를 한 개로 합치지 않음

| 자료 | 표기 | 자료 유형 |
|---|---|---|
| 취리히 원본 Z 문서관 목록 | **1529-10-03** | 보존기관의 문서 날짜 |
| GHDI/WA 1910 전사 서두 | **Tertia Octobris**, 즉 10월 3일 | 편집 전사에 보존된 본문 자체의 표기 |
| 취리히 W2119 인쇄본의 서지상 표제 | **dritten Tags Octobers** | 1529년 인쇄본 표제를 후대 서지로 기록 |
| DigiRef K 학술 디지털자료 | **1529-10-04** | 현대 디지털 아카이브의 자료 날짜 항목 |

이런 차이는 본문 작성일, 서명 또는 문서 완료일, 편집자가 붙인 사건 날짜 등으로 설명될 **가능성**이 있으나 아직 증명되지 않았다. 특히 DigiRef의 4일 표기가 다른 세 자료의 3일 표기와 다르다는 이유로 그 자체를 '잘못된 날짜'라고 단정하지 않는다. V2.23 데이터에서는 네 관찰을 `INSTITUTIONAL_DOCUMENT_DATE_METADATA`, `1910_EDITED_TEXT_INCIPIT`, `IMPRINT_CATALOGUED_TITLE_DATE`, `MODERN_SCHOLARLY_PORTAL_EVENT_DATE`로 분리했다.

연구 후속 과제는 해당 DigiRef 기록의 실제 원본 문서 면, 서명과 종결 날짜, 학술 편집자의 날짜 설명을 살펴 **왜 4일로 기술했는지** 확인하는 것이다.

## 4. 이미지 접근 실패 기록은 연구 데이터

이번 환경에서 네 경로를 시도했다. HAPuls 원본 이미지 소개 페이지는 응답 시간초과, DigiRef 상세 페이지는 접속제한 화면, e-rara W2119 개별 페이지는 다운로드 오류, IIIF 매니페스트는 접근 불가였다. 해당 오류는 자료 자체의 소실이나 원본의 비공개를 뜻하지 않고, **이번 접근 세션의 기술적 제한**으로 기록한다. 명확한 URL을 유지해 후속 조사에서 검증을 반복 가능하게 한다.

연구용 이미지 확보 절차에서는 (1) 소장기관 제공 원본 파일 또는 IIIF 이미지, (2) 이미지 파일/원본 식별자, (3) 해당 면과 제7/13/15조 위치, (4) 전사 원문과 독립 검수 기록을 필수 항목으로 둔다. 원문을 읽지 않은 상태에서 자동 OCR 결과나 편집본 문장을 원본의 확정 판독으로 저장하는 것을 금지한다.

## 5. 권리와 공개 심사

e-rara의 **W2119 Public Domain Mark**는 전 세기의 인쇄본 이미지를 합법적으로 사용할 수 있는 방향에서 중요한 추가 확인이다. e-rara는 무료 다운로드 가능함을 밝히고, 소장기관·저자·지속식별자 등을 출처로 명시하거나 활용 사실을 알려 달라고 요청한다. 그러나 이 정보만으로 **취리히 필사본 Z, 헤센 K의 이미지, 후대 편집자의 저작권 및 ATLAS 자체 미디어 검수**가 승인된 것은 아니다. 앱 공개 판단은 별도다.

## 6. 다음 실제 교감 순서

1. K: DigiRef와 HAPuls의 이미지 파일에 접속하여 **60r–64v** 원본 면별 순서와 제7·13·15조 구간을 기록한다.
2. W2119: e-rara IIIF 매니페스트 또는 소장기관 다운로드에서 **1529년 인쇄본 이미지**를 확보한다. 4장 양면의 판면·초기 철자와 구두점을 기록하되, Z/K와 자동 동일시하지 않는다.
3. Z: 취리히 문서관 E I 3.1 Nr.54 원본 또는 마이크로필름을 통해 **Z에만 있다는 세 추가 구절**을 필사·행 번호와 함께 확인한다.
4. W2118: Zwingli MvK A 81,8과 VD16 W2118의 일치 여부를 개별 서지로 확인한다.
5. Z/K 원본·취리히 인쇄본·GHDI 1910·RBS(Z)/MBW(K+Z)를 비교하고 역사학/신학 전문 감수를 실시한다.
6. 독자 원고 반영은 별도 승인 후 진행한다. 기존 10편의 문장 오프셋과 30개 주장/탐색 연결을 불필요하게 변경하지 않는다.

**V2.23 연구 성과:** 편집된 독일어 원문 3개 조항의 문맥 재확인, 서로 다른 날짜 증거 4건의 구분, 이미지 접근 실패 4경로의 재현 가능한 기록, W2119의 공용영역 표지 확인. **원본 1529년 직접 판독 0건, Z/K 추가 문구 실제 대조 0건, 전문가 승인 0건, 웹앱 공개 0건.**

데이터: `data/deep/atlas_v223_marburg_critical_text_and_date_provenance.json`  
검증: `scripts/validate_atlas_v223.py`
