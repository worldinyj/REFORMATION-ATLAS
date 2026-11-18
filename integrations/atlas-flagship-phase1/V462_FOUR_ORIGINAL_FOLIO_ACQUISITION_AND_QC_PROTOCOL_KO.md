# 종교개혁 ATLAS — V4.62 원본 지면 확보 결과 및 원문 증거 승인 프로토콜

**연구일:** 2026-11-19 · **범위:** 1529년 마르부르크 제15조 K/Z, 1531·1540년 아우크스부르크 신앙고백 제10조  
**핵심 판정:** **4개 우선 대상 중 해당 조항의 16세기 원본 지면을 직접 판독·교감 완료한 건수는 0건.** 저장소의 보완 자료는 판본 목록·학술 편집본·원본 디지털 뷰어 접근 기록으로 사용한다. 존재하지 않는 사진·전사·해시를 생성하지 않는다.

## A. 이번 실제 접근 확인 — 물리적 서지와 픽셀 판독을 분리

| 우선 | 원전 특정 | 직접 연 화면/새로 확보한 경로 | 원본 조항의 직접 판독 | 접근상의 제약 |
| --- | --- | --- | --- | --- |
| 1 | **헤센 K, 제15조**, HStAM 3 Nr.245 | Hessen Arcinsys 정식 등록 페이지에서 **Show digital copies**를 눌러 실제 `digitalMediaViewer.action?archivalDescriptionId=5447099`에 도달. JPG `representationId=14439026` 연결 기록 확인 | **미완료** | 그림 본문은 자바스크립트·비동기 뷰어로 표시되며, 현재 텍스트 브라우징에는 로딩 그림만 노출 |
| 2 | **취리히 Z, 제15조**, StAZH E I 3.1 Nr.54 | 취리히 공식 문서 기록에 우스테리(Usteri) 1883년 파크시밀리 **409–413쪽** 근거. 튀빙겐 OpenDigi에서 해당 1883년 제56권 PDF 링크 확인 | **미완료** | PDF 다운로드 응답 시간 초과, 해당 지면 화면 미표시 |
| 3 | **1531 라틴어 신앙고백 제10조**, VD16 **C4734**, `bsb11411960` | MDZ 디지털 서지 288스캔 소장 기록 직접 확인 | **미완료** | MDZ 텍스트 접근에서 자바스크립트 실행 요구·열람 오류; 정확한 제10조 스캔 번호 미확정 |
| 4 | **1540 라틴어 Variata 제10조**, VD16 **C4713**, Pitts 1540 CONF | Pitts 디지털 표제지·2017년 도록 34쪽; 대체 Google Books 1540년 Rhau 인쇄본 `HmpoAAAAcAAJ`(274쪽) 및 페이지 링크도 확인 | **미완료** | Pitts C4713의 제10조 이미지 미확보. Google Books 별도 복본의 **VD16 식별 및 Pitts 판본과 동일 여부도 미검증** |

### 공식 원문 경로

- K 소장목록: https://arcinsys.hessen.de/arcinsys/showArchivalDescriptionDetails?archivalDescriptionId=5447099
- K 디지털 열람기: https://arcinsys.hessen.de/arcinsys/digitalMediaViewer.action?archivalDescriptionId=5447099
- K 교육 포털(원본 전체 디지털화 소개): https://www.hapuls.de/node/1472
- Z 취리히 소장목록: https://suche.staatsarchiv.djiktzh.ch/detail.aspx?ID=618165
- Z 1883 팩시밀리 권호: https://opendigi.ub.uni-tuebingen.de/opendigi/thstkr
- Z 1883년 직접 PDF: https://opendigi.ub.uni-tuebingen.de/opendigi/thstkr_1883/pdf
- 1531년 라틴어 MDZ: https://www.digitale-sammlungen.de/en/details/bsb11411960
- 1540년 Pitts 자료: https://dia.pitts.emory.edu/image_details.cfm?ID=6759
- 별도 1540년 Google Books 항목: https://books.google.com/books?id=HmpoAAAAcAAJ

## B. 새로 드러난 기록상의 정밀성 문제 — 'K folio 60–63'와 '60r–64v'

- HAPuls 원본 안내에는 `HStAM PA Nr.245, Bl.60–63`가 표시됨.
- 취리히의 K 원본 교차 기술에는 `HStAM Best.3 Nr.245, fol.60r–64v`가 표시됨.
- Arcinsys는 **HStAM 3 Nr.245**이라는 상위 서지·문서 단위를 직접 확인해 준다.

이러한 표기의 차이만으로 누락 지면이나 원본이 둘이라는 주장을 만들어서는 안 된다. **아카이브가 내놓는 실제 원본 페이지별 잎 번호·앞뒷면과 각 기록의 표기 관습**을 대조하여 정리해야 한다. 오늘 작업에서는 K의 제15조가 몇 번째 JPG인지 확정하지 않았다.

## C. 원문 확보 뒤 적용할 단일 승인 규칙 — 기술적인 'HOLD'를 자동 해제하지 않기

`research/data/ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json`에 네 개의 목표 문헌과 확인된 접근 경로·장애·정확한 원문 미확보 상태를 기록했다.

`primary-source-evidence-gate.mjs`는 각 조항에 다음 **5개 독립 조건**을 모두 요구한다.

1. **해당 조항의 원본 이미지를 직접 육안 확인했는가**(`directOriginalLeafViewed=true`).
2. **보존본의 SHA256 해시**가 있는가(`originalImageSha256`).
3. **정확한 잎·스캔·캔버스 위치**가 있는가(`leafOrCanvas`).
4. **그 잎에서 읽은 원어 외교적 전사**가 있는가(`diplomaticGermanText` 또는 `diplomaticLatinText`).
5. **사람이 원문 판독 QC를 통과시켰는가**(`transcriptionReview=HUMAN_QC_PASS`).

1540년 Google Books를 대체 원전으로 사용하는 경우에는 해당 책이 **C4713과 동일한 서지상 판본인지**를 추가 검증해야 한다. 같은 1540년 인쇄본이라는 이유로 동일하다고 표시할 수 없다. 실제로 다른 소장 복본일 수 있으므로 **판본 동일성과 물리적 복본 동일성**도 구별한다.

위 5개 조건 충족은 '해당 원본 지면을 직접 읽었다'라는 **기록상의 준비 요건**일 뿐, 원문 전사의 진위·판본 교감·역사 해석의 최종 승인에는 역사 전문가가 반드시 필요하다. **이 체크를 통과해도 `canShip`는 결코 자동으로 true가 되지 않도록 구현했다.**

## D. 대조 실무 규격

### 마르부르크 제15조 K ↔ Z

- K 서명본과 Z 서명본 각각의 제15조 잎을 저장·해시·잎 번호 지정.
- 독일어 철자·수정 흔적·삽입 장소를 직접 분리 전사. 글자 확실성 낮은 경우 `uncertain` 태그 사용.
- 취리히 문서보관소가 증명한 **제7·13·15조 Z 추가문구**는 초기 이문 힌트로 사용하되 **미판독 원문 글자를 지어내지 않음**.
- 1883년 우스테리 파크시밀리를 얻으면 **19세기 사진 재현물**이라는 별도 사료 유형으로 표기한다. 2014년 K 기반 편집본 및 *Reformierte Bekenntnisschriften* Z 기반 판본과 독립 비교.
- 화면에 넣기 전 최소한 **K/Z 병렬 원문, 서로 다른 문구의 정확한 지점, 이미지의 출처와 법적 사용 범위, 두 판본의 독립 검토자 기록**을 요구.

### 아우크스부르크 제10조 1531 ↔ 1540

- 1531년 C4734의 해당 인쇄 지면과 1540년 C4713의 해당 인쇄 지면을 각각 지정.
- 1858년 『Corpus Reformatorum』 제26권 357쪽의 비교는 **검토용 기준점**으로 활용. `vere adsint et distribuantur`와 `cum pane et vino vere exhibeantur`의 16세기 인쇄 철자와 판면 위치를 확인.
- 1858년 비판판에 보이는 내용은 **1531·1540년 원본 사진 확인 결과가 아니라 편집판 비교**로 유지. 해당 비판판의 `exhibeatur/exhibeantur` 자동 추출 차이를 별도 원전 이문이라고 재분류하지 않음.
- 확실히 검증된 원문과 단순 해설문을 구별해 원문을 최소 인용하고, 2인 전문가 판정 및 교파사 해석 한계를 독립 유지.

## E. 이 단계의 실행·결과 구분

| 검증 | V4.62 결과 |
| --- | --- |
| 4개 기관 원전의 접근 경로 확인 | **완료** |
| K의 Arcinsys 디지털 JPG 뷰어 직접 도달 | **완료(뷰어만)** |
| Z 1883 파크시밀리 PDF 링크 확인 | **완료(지면 접근 시간 초과)** |
| 정확한 원전 제15조·제10조 이미지 4개 | **0/4** |
| 원문 이미지별 SHA256·정확한 잎·전사·사람 QC | **0/4** |
| 고위험 주장 역사학자 승인 | **0건** |
| 독자 파일럿 | **0명** |
| 출시 승인 | **불가** |

**향후 원본 확보 절차:** 기관 웹 열람기에서 위 네 페이지를 직접 내려받을 수 있을 때, 저작권·열람조건을 준수해 연구용으로 보관한다. 이미지별 해시와 개별 잎 ID를 증거 기록에 넣고 사람 판독 검토 후 두 쌍을 병렬 교감한다. 파일이 준비되지 않았거나 기관 UI가 제한되면 다른 사료 해설을 원본 지면으로 바꿔치기하지 않는다.

**의사결정:** 연구 브랜치에서만 진행하며, 기존 `main`, AI Studio 운영 앱, 역사 원고 원문은 수정하지 않는다. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`를 유지한다.
