# 종교개혁 ATLAS — V3.81 / 검증된 역사 주장과 실제 513편 원고의 연결 실사

**연구 기준일:** 2026-11-15  
**기반:** `research/atlas-v380-basel-integrated-readiness-audit`  
**브랜치:** `research/atlas-v381-claim-to-reader-targets-audit`  
**상태:** RESEARCH_MAPPING_COMPLETED / EDITORIAL_REVIEW_ONLY / CAN_SHIP=false

## 1. 이번에는 실제 GitHub 원고와 계약을 조사했다

V3.80에서 미확인이던 "513편의 실체와 실제 문단 위치" 문제를 조사했다.

- GitHub의 `main`은 **README.md 한 파일뿐**임을 Git Trees API로 확인했다. 따라서 `main`에서 513편을 찾지 않고 연구 브랜치 기준으로 조사해야 한다.
- 누적 연구 브랜치의 루트에는 `.github`, `assets`, `data`, `docs`, `integrations`, `research`, `scripts`, `tests` 등이 있다.
- `integrations/medium-atlas-v308/manifest.json`에 `expectedCounts.readers=513`, `sections=1539`, `sources=723`, `materialization=ON_DEMAND_FOUR_PINNED_INPUTS`, `canPublish=false`라고 명시된다.
- 실제 `data/deep/atlas_v307_remaining_overview_medium_readers.json`의 `catalogue` 배열을 읽었으며 **513개 / ID 중복 없음**을 확인했다. 단, 이 목록은 513편의 *목차와 참조 경로*이며 513편 본문이 단일 JSON에 통째로 저장된 완성본이라는 뜻은 아니다.
- `scripts/build_v308_integrated_delivery.mjs`는 V3.04·V3.05·V3.07 입력과 V3.04 개요 crosswalk를 조립해 최종 전달 JSON 2개를 **실행 시 생성**한다. 이번에는 생성기를 돌리거나 출력물의 SHA256을 검증하지 못했다.
- `data/contracts/atlas_v304_overview_medium_reading_crosswalk.json`: **97개** 개요 항목의 독서 원고 대응을 확인했다. 당초 보고된 78 직접·18 일부·1 배경은 전달 패키지의 목표 메트릭이며, 실제 AI Studio 앱에서 작동하는지 검증한 것은 아니다.
- V3.08 매니페스트는 `actualAIStudioIntegrationVerified=false`, `actualAIStudioSourceAvailable=false`를 명시한다. 즉 연결 계약 ≠ 실제 앱 반영.

## 2. 직접 열람한 5개의 기존 원고 절

| 원고 ID | 원고 JSON 경로 | 절 index | 실제 절 제목 | 활용 |
|---|---|---:|---|---|
| PERSON-BUCER | `data/deep/atlas_v264_medium_depth_humanists_and_mediators.json` | 1 | 성찬 논쟁에서 합의의 말을 찾다 | **가장 적절한 1536 협의 심화 위치** |
| THEME-COMMUNION | `data/deep/atlas_v260_medium_depth_core_comparisons.json` | 1 | 실재와 상징의 단순한 양자택일을 넘어서 | Q1의 신학적 설명과 연계; Q2~Q4는 별도 절 필요 |
| CITY-BASEL | `data/deep/atlas_v276_medium_depth_twenty_readers.json` | 0 | 1529년의 교회적 전환 | **1536년과 구별된 배경** 카드로만 |
| PERSON-KARLSTADT | `data/deep/atlas_v278_medium_depth_balanced_reform_paths.json` | 1 | 돌아온 루터와의 갈등 | 1522년 갈등을 다루므로 1536년 대표단 사건과 직접 동일시 금지 |
| MEDIUM-MARBURG | `data/deep/atlas_v254_medium_depth_ten_readers.json` | 1 | 핵심 사건과 주장 | 1529년 성찬 갈등의 배경, 1536년 협의 자체 아님 |

위 표의 절 index는 **0부터 시작하는 실제 JSON `chapters[].sections[]`의 인덱스**다. 문자열 매칭만으로 페이지 경로를 추정하지 않았으며 5개 파일 각각 직접 읽어 섹션·제목·본문 일부와 Git blob SHA를 고정했다.

## 3. 가장 중요한 발견 — 이미 1536을 언급하는 원고

`PERSON-BUCER`의 index 1 본문에는 다음 부분이 있다.

> 부처는 성찬을 둘러싼 루터와 스위스계 개혁자들의 차이를 좁히려 했다. 1536년 비텐베르크 일치협약은 그런 중재가 낳은 성과였지만 모든 개혁 진영을 지속적으로 하나로 묶지는 못했다.

이 원고는 이미 '협약 체결'과 '의미의 일치'를 구분한다. 따라서 V3.70–V3.80의 새로운 사료를 활용하여 **1536년 바젤 대표단의 문의·답변·수용 보고/승인의 구분**을 별도 심화 절 또는 자료 카드로 확장할 가치가 있다.

단, 그 기존 문장이 7월 14일·17일·20일·23일의 상세 사건을 설명하는 것은 아니다. 기존 본문에 있다는 사실과 새 주장 추가가 필요한 사실을 구분했다.

## 4. 16개 claim의 목적지 매핑 분류

구조화 산출물 `research/data/V3_81_CLAIM_TO_READER_TARGET_CROSSWALK_DRAFT.json`에서 V3.80의 C01–C16을 다음과 같이 분류했다.

| 분류 | 건수 | 처리 |
|---|---:|---|
| 기존 성찬 주제 절의 개념 보강 | 1 | THEME-COMMUNION index 1, **새 주장 원문 미존재** |
| 신규 심화 모듈 필요 | 3 | Q2 구약 성도, Q3 연합, Q4 합당하지 않은 수찬자 |
| 기존 부처 원고의 1536 사건 심화 | 6 | PERSON-BUCER index 1의 **추가 문단** 후보 |
| 7/23 부처 서신 직접 사료 미검증 | 1 | 원고 변경 보류 |
| 공식 승인 회의록 미검증 | 1 | 의결·연대 관련 원고 변경 보류 |
| 자료 아카이브 전용 | 1 | St. Gallen 사본 출전 |
| 데이터 품질검증 전용 | 2 | `für stellet`, B의 표제 생략 |
| 필사 날짜/사건 날짜 별도 등록 | 1 | 1537 표기와 1536 사건 구분 |

**총 16건**. `existing_sentence_match=false`가 전체에 설정되어 있다. 이는 기존 절이 *관련 주제*를 이미 언급하더라도 V3.80의 **특정 역사 주장 문장이 현재 본문에 정확하게 기록되었다고 확인한 것은 아니라는 의미**다.

## 5. 금지 매핑 — 시대와 자료가 다른 바젤 협약

이 통합 실사에서 가장 큰 오연결 위험은 **바젤**이라는 동일 지명이다.

- `OV-E-014` / `EVENT-BASEL_SETTLEMENT1433_1436`: **1433–1436년 후스파·바젤 공의회 협상**.
- `OV-D-007` / `DOCUMENT-BASEL_COMPACTATA`: **보헤미아 콤팍타타 문헌**, 1536년 바젤-스트라스부르 성찬 협의가 아님.
- `DOCUMENT-FORMULA_CONCORD`: **1577년 일치신조**, 후대 루터교 고백.
- `DOCUMENT-BOOK_CONCORD`: **1580년 일치신조집**, 여러 문헌을 모은 책.

이 네 개를 1536년 비텐베르크 일치협약의 동일 이벤트나 직접 출전으로 결합하지 않는다.

513편 카탈로그에서 **1536년 바젤-스트라스부르 성찬 협의만을 위한 별도 원고 ID는 발견하지 못했다.** 따라서 `PROPOSAL-EVENT-BASEL-STRASBOURG-COLLOQUY1536`이라는 제안용 식별자만 준비한다. 정식 ID를 발급하거나 실제 원고를 생성한 것으로 취급하지 않는다.

## 6. 연구 출처와 기존 원고의 source ID 스키마 차이

기존 `PERSON-BUCER` 문서의 `sources` 필드는 예를 들어 `S04`, `S05`와 같은 **기존 자료 묶음 내부 ID**를 사용한다. 반면 V3.80은 `WA_BR7_3048_TEXT`, `RHENANUS_1886_N297_422`과 같은 **연구 사료 ID**를 사용한다.

즉 두 네임스페이스를 동일시하면 잘못된 출처 연결이 생긴다. 후속 통합 시에는
`claim_id → research_source_id → canonical_source_locator → reader_id / section_index`
구조가 필요하다.

V3.81은 기존 `sources` 배열을 덮어쓰지 않고 별도의 대응표를 생성한다. 실제 앱의 데이터 계약·원고 조립이 확인될 때까지 작성/배포 기능은 차단된다.

## 7. 다음 단계 V3.82 실질 작업

1. **원본 불변 sidecar 프로토타입**: PERSON-BUCER index 1과 THEME-COMMUNION index 1에 추가할 문단의 별도 파일을 생성. 원고 원문을 수정하지 않는다.
2. **정확한 근거 묶음**: 추가 문단의 각 문장에 V3.80 Cxx, 원전 이름·판본·인쇄 쪽수, 직접 열람 단계, 금지 확장 범위를 붙인다.
3. **새 모듈 판단**: 1536 바젤 성찬 협의 독립 사건 카드를 기존 원고와 충돌하지 않는 *제안*으로 작성. 1433–1436 바젤 콤팍타타와 역사지도·연표 ID 완전 분리.
4. **검증**: 조립기 `node scripts/build_v308_integrated_delivery.mjs --check` 실행 가능 여부를 점검하고, 513편 실제 산출물·상세 본문·연결 상태를 재현 가능한 방식으로 검증.
5. **앱 검토**: Google AI Studio 소스/앱 라우트가 실제 이 GitHub 레포에 연결된 사실을 확인한 후에만 데이터 핸드오프 제안.
6. BDS 1988 p.219–226과 바디안 1536-07-23 편지는 별도 원문 미확보 게이트를 유지.

## 8. QA / 승인 상태

- PASS: `main` 저장 트리 실사 / 누적 연구 브랜치 루트 확인.
- PASS: 513편 카탈로그 513개 고유 ID 조사.
- PASS: 개요 crosswalk 97개 확인.
- PASS: 실제 기존 원고 5개 경로·본문 절·저장된 Git blob SHA 확인.
- PASS: V3.80 주장 16건 모두 대응 분류; 서로 다른 바젤 문서 4개 혼동 방지.
- PENDING: 513편 전체를 조립한 최종 JSON 생성 및 1,539절 전수 무결성 검증.
- PENDING: 실제 AI Studio 앱 소스와 배포 라우트 확인.
- PENDING: 원전 이미지 및 학술 전문가 승인.
- **CAN_SHIP=false**.

**불변 보장:** `main`, 513편 원고·본문, 앱, V3.60–V3.80 데이터의 어떤 파일도 수정하지 않는다. 모든 연구 결과를 새 브랜치의 신규 매핑과 보고서로만 보존한다.
