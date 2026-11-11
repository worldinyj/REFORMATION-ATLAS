# 종교개혁 ATLAS V3.62 — 바젤 성찬 협의의 사본·연대·편집 정합성 감사

- 기준일: 2026-11-11
- 부모 브랜치: `research/atlas-v361-basel-four-questions-witness-crosswalk`
- 작업 브랜치: `research/atlas-v362-basel-witness-chronology-qa`
- 상태: RESEARCH_ONLY / DRAFT / NOT_APPROVED / CAN_SHIP=false
- 범위: 연구 산출물만 추가. main, 513편 역사 원고, 앱, 원본 사료 불변.

## 1. 독립 확인한 서지적 자료

1. Hermann Barge, *Andreas Bodenstein von Karlstadt*, 2권 (Leipzig, 1905)의 제2권 제목은 *Karlstadt als Vorkämpfer des laienchristlichen Puritanismus*이며, 제1권과 구별되어야 한다. 공개 도서목록: https://openlibrary.org/books/OL13993004M/Andreas_Bodenstein_von_Karlstadt
2. 디지털 Karlstadt 학술판의 서지목록은 Barge 1905, 2권과 Barge 1904년 성찬문서 연대 연구를 별도로 등재한다: https://dev2.hab.de/apps/edoc/view.html?id=kgk_bibliography
3. 최근 Simon Sulzer 연구에서는 1536-07-17 Basel의 Karlstadt와 Grynäus가 Strasbourg에 왔다는 설명, Bucer·Capito의 설명을 듣고 돌아왔다는 논의, 1536-09-24 스위스 개신교 측 모임 계획을 서술하고 Barge II 부록 50, pp.603–606을 주석으로 인용한다. 이는 현대 2차 연구의 **간접 진술**이다. Basel 의회 원본이나 1905 인쇄 본문을 직접 교감한 증거로 취급하지 않는다.
   - https://regionalia.blb-karlsruhe.de/files/21006/BLB_Abendschein_Simon_Sulzer.pdf

## 2. V3.61 내부 정합성 발견 — 표제 문제

V3.61의 한국어 Markdown 표는 `Erlüterung ...`을 A사본의 표제처럼 제시한다. 그러나 동 버전의 구조화 JSON `V361-V04` 항목은 A를 `BDS editorial headword, not established manuscript title`이라고 구별하고, B에 `Erlüterung ...`을 둔다. 두 파일은 현재 서로 일치하지 않는다.

### 판정
- 상태: INTERNAL_CONTRADICTION_CONFIRMED (두 연구 파일의 서로 다른 기재를 직접 대조함)
- 역사적 정답: UNRESOLVED (1988년 비평판 p.218 인쇄 이미지와 A/B/C/D 표제 위치를 직접 재교감해야 확정)
- 즉시 공개할 수정문: 없음.
- 편집 지침: 현재 단계에서는 `Erlüterung`을 특정 사본 A의 필사 표제로 단정하지 말고 ‘1988년 편집판에서 소개되는 표제 계열’이라고만 기술한다.

## 3. 1536-07-17 날짜 충돌: 사건 유형을 분리해야 함

| 주장/기록 | 근거 계층 | 현재 게이트 |
|---|---|---|
| 1536-07-17이 대표단 파견과 연결 | Barge 1905의 역사 서술에 대한 V3.60/61 OCR 계승 기록 | ORIGINAL_PRINT_AND_MUNICIPAL_REGISTER_UNCHECKED |
| 1536-07-17에 협의 종료·설명문이 연결 | BDS 1988 p.217에 대한 V3.61 기록 | EDITION_IMAGE_UNCHECKED_IN_THIS_PASS |
| 1536-07-17 Karlstadt·Grynäus Strasbourg 방문 | 현대 Simon Sulzer 연구 서술 | SECONDARY_ACCOUNT_ONLY |
| 1536-07-29 Karlstadt→Bullinger | HBBW 목록 No.870, V3.61 검토 | EDITORIAL_INDEX_ONLY |
| 1536-08-02 바젤 관련 보고와 필사본의 1537-08-02 | 서로 다른 역사 주장/기재 | DO_NOT_COLLAPSE_DATES |

중요: 1536-07-17에 ‘방문’, ‘파견’, ‘협의 종료’, ‘문서 작성’이 모두 일어났다고 단정하지 않는다. 현대 연구가 방문이라고 기술한다는 것만으로 바르게의 ‘파견’과 BDS의 ‘8일 협의’ 해석이 해결되는 것은 아니다. `date_value`, `event_type`, `source_statement`, `source_kind`, `certainty`를 분리 관리한다.

## 4. 네 문답의 신학적 해석 제한

- Q1: 성찬에서의 참된 임재 언어를 물리적 혼합·영속적 자연 결합과 동일시하지 않는다.
- Q2: 구약 성도들의 그리스도 참여 문제를 다룬다. 표현의 정확한 어휘 비교는 미완료.
- Q3: 그리스도와 신자의 연합 언어를 다룬다. '자연적'이라는 말의 당대 의미를 후대 교리 용어로 무리하게 번역하지 않는다.
- Q4: 고린도전서 11장의 책망받는 공동체 구성원에 초점을 둔 답변을 불신자 일반에 관한 포괄적 신학 명제로 확장하지 않는다.

모든 항목은 V3.61 교감표를 계승한 주제 수준 분류이며 새로운 외교적 전사로 확인된 문장별 이문이 아니다.

## 5. 사본 동일성 및 누락문장 판정

- KiAr Mscr 23a:66, BDS A–D, Barge의 Gernlerianae I, Basel Staatsarchiv Kirchenakten A9 fol.405–410은 **서로 자동 동일시 금지**.
- 바르게의 ‘다른 바젤 사본에서는 마지막 유보 문구가 없다’는 진술은 현재 `BARGE_EDITOR_REPORTED_VARIANT`만 인정.
- 두 번째 사본의 인쇄 또는 원본 이미지를 확인하기 전에는 빠진 문장의 기원(축약·필사 오류·의도적 삭제)을 판단하지 않는다.

## 6. V3.63 작업 우선순위

1. BDS 6/1 pp.217–218의 **실제 인쇄 이미지**에서 A와 B의 표제 기재 위치를 재검증해 두 V3.61 파일의 충돌 해소.
2. Basel Staatsarchiv Kirchenakten A9 fol.405–410 공식 현행 서가번호·이미지 접근 확인.
3. HBBW 6 No.866과 870의 **편지 본문** 열람 후, 7월 17/19/29일 사건 연동 여부 검증.
4. Barge 1905 II pp.603–606은 38MB PDF 접근 한계로 이번 단계의 인쇄 원본 고해상도 재교감이 불가능했다. 단일 페이지 이미지 접근 경로를 확보하여 Q1~Q4 문장 단위 교감.
5. 전문 검수 전까지 CAN_SHIP=false를 유지한다.

## 7. 데이터 품질 테스트 (수동 게이트)

- [x] V3.60→V3.61 브랜치 비교로 추가 파일 2개 확인
- [x] V3.61 Markdown·JSON 두 파일 직접 열람
- [x] 동일 버전 내부 표제 A/B 충돌 식별
- [x] 현대 2차 연구에서 1536-07-17 관련 서술 및 Barge 부록 50 인용 경로 확인
- [ ] BDS p.218 인쇄 원본 표제 직접 교감
- [ ] A9 fol.405–410 직접 확인
- [ ] HBBW 서신 두 건 본문 검토
- [ ] 원전 외교적 전사 완료
- [ ] 전문가 승인·공개
