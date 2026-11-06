# V3.23 — 종교개혁 ATLAS 역사 연표·개요–원고 탐색 연결망

> **DRAFT · MEDIUM · publication HOLD**. 현재 연구 브랜치용 자료이며 운영 중인 Google AI Studio 앱에 자동 반영되지 않는다. 기존 513편·1,539절 원고, 출처 723건, 개요 97건, 기존 선택 주장 22건을 수정하지 않았다.

## 1. 왜 이번 재구성이 필요한가

초기 V3.04 개요 대응표를 그대로 읽으면 웨슬리·경건주의·조선 교회사 같은 항목이 아직 **NO_MATCH**로 보인다. 그러나 V3.05와 V3.07에서 해당 원고가 추가되고, V3.10에서는 부분 범위의 개요를 실제 읽기 경로에 보강하였다. 따라서 원본 대응표에 V3.05→V3.07→V3.10 수정 이력을 적용한 **파생 연구용 연결망**을 새로 만들었다. 과거의 대응표 자체를 고쳐 역사를 지우지 않고, 출처 단계와 수정 이력을 각 항목에 남긴다.

## 2. 검증된 데이터 범위

| 항목 | 결과 |
|---|---:|
| 개요 항목 전체 | **97** |
| `DIRECT_TOPIC` | **78** |
| `PARTIAL_COVERAGE` | **19** |
| `NO_MATCH`·`BACKGROUND_ONLY` | **0** |
| 기존 원고 레지스트리 | **513편** |
| 개요에서 원고로 가는 링크 | **156건** |
| 개요에 직접 연결된 서로 다른 원고 | **107편** |
| 513편 중 개요 연결 없이 독립 레지스트리에 보존된 원고 | **406편** |
| 근거 출처가 있는 선택 역사 사건 | **17건** |
| 사건–개요 연결 | **34건** |
| 사건–원고 맥락 연결 | **23건** |
| 독립 연구 흐름 안에서의 시간 순서 링크 | **12건** |
| 기존 대응표가 금지한 다른 인물·문헌 연결 재유입 | **0건** |

**406편은 '원고가 없다'가 아니다.** 97개의 개요 항목이 참조하지 않는 독립 원고이며, 고유 ID와 데이터 경로·장 위치는 모두 보존된다. 따라서 이 숫자를 결측 콘텐츠 비율로 해석하면 안 된다.

## 3. 실제 식별자 기준 연결 예시

| 개요 ID | 개요 제목 | 최신 범위 | 연결 원고 ID |
|---|---|---|---|
| `OV-E-015` | 루터의 95개조 논제 | DIRECT_TOPIC | `MEDIUM-LUTHER1517`, `DOCUMENT-NINETY_FIVE1517` |
| `OV-E-019` | 아우크스부르크 신앙고백 제출 | DIRECT_TOPIC | `MEDIUM-AUGSBURG` |
| `OV-D-011` | 아우크스부르크 신앙고백 | DIRECT_TOPIC | `MEDIUM-AUGSBURG` |
| `OV-E-021` | 트리엔트 공의회 | DIRECT_TOPIC | `MEDIUM-TRENT` |
| `OV-D-014` | 트리엔트 공의회 교령 | PARTIAL_COVERAGE | `MEDIUM-TRENT`, `DOCUMENT-ROMAN_CATECHISM` |
| `OV-E-024` | 베스트팔렌 조약 | PARTIAL_COVERAGE | `THEME-WAR_WESTPHALIA` |
| `OV-D-015` | 베스트팔렌 평화 조약문 | PARTIAL_COVERAGE | `THEME-WAR_WESTPHALIA` |
| `OV-P-024` | 존 웨슬리 | DIRECT_TOPIC | `PERSON-JOHN_WESLEY` |
| `OV-D-017` | 웨슬리의 설교 및 공동체 규칙 | PARTIAL_COVERAGE | `DOCUMENT-METHODIST_GENERAL_RULES1743`, `PERSON-JOHN_WESLEY` |

여기서 `PRIMARY`는 현재 항목에서 우선 보여줄 읽기이고, `FOLLOWUP`은 후속 읽기이다. 양쪽 모두 역사 전문가의 전면 감수 인증을 뜻하지 않는다.

## 4. 선별 역사 사건과 날짜의 역할

### 4-1. 트리엔트 공의회

| 날짜 | 사건 | 날짜의 역할 | 출처 ID |
|---|---|---|---|
| `1545-12-13` | 제1회기 개막 | `COUNCIL_OPENING` | `TRENT-SESSION-SCHEDULE` |
| `1547-01-13` | 제6회기 칭의 교령 | `DECREE_SESSION_DATE` | `TRENT-VI-EN`, `TRENT-CHRONOLOGY-SCHOLAR` |
| `1563-07-15` | 제23회기 성직자 양성 개혁령 | `DECREE_SESSION_DATE` | `TRENT-XXIII-EN`, `TRENT-CHRONOLOGY-SCHOLAR` |
| `1563-12-04` | 최종 회기 종료 | `COUNCIL_CLOSING` | `TRENT-SESSION-SCHEDULE` |
| `1564-01-26` | 교황 비오 4세의 공의회 승인 칙서 | `PAPAL_CONFIRMATION` | `TRENT-SESSION-SCHEDULE` |

공의회 **개막–칭의 교령–성직 교육 개혁–회의 종료–교황 승인**은 별개의 날짜·행위이다. 특히 1545~1564년을 '공의회 회기 자체'라고 표시하면 회의가 종료된 1563년과 1564년 승인 절차가 섞인다. 제23회기 제18장의 신학교 입학 **12세**와 제6장의 성직록 보유 **14세** 규칙 역시 별도 범주를 유지한다.

### 4-2. 아우크스부르크 신앙고백

| 날짜 | 사건 | 날짜의 역할 | 출처 ID |
|---|---|---|---|
| `1530-06-25` | 아우크스부르크 제국의회에 신앙고백 제출 | `DOCUMENT_PRESENTATION` | `AUGSBURG-CONFUTATION`, `AUGSBURG-HISTORICAL` |
| `1531-05` | 멜란히톤 감독 1531년 공인 초판 출간 | `AUTHORIZED_PRINT_PUBLICATION_MONTH` | `AUGSBURG-HISTORICAL` |
| `1540` | 1540년 Variata 개정판 | `REVISED_EDITION_YEAR` | `AUGSBURG-1540-VARIATA` |

**1530년 제출**, **1531년 공인 초판 간행**, **1540년 개정판 Variata**를 구별한다. 1530년에 있었던 초기 인쇄와 1531년 멜란히톤 감독 판본은 한 가지 사건의 다른 표현이 아니다.

### 4-3. 웨슬리와 감리교 일반 규칙

| 날짜 | 사건 | 날짜의 역할 | 출처 ID |
|---|---|---|---|
| `1738` | 교단 해설에 따른 일반 규칙 형성 시기 | `RULES_FORMATION_YEAR_DENOMINATIONAL_ACCOUNT` | `WESLEY-UMC-GLOSSARY` |
| `1743` | 일반 규칙 소책자 출판 | `PAMPHLET_PUBLICATION_YEAR` | `WESLEY-WELLCOME-1743`, `WESLEY-UMC-GLOSSARY` |
| `1785` | 미국 감리교회에서 승인 | `LATER_DENOMINATIONAL_APPROVAL_YEAR` | `WESLEY-UMC-GLOSSARY` |

1738년의 형성은 **후대 교단 설명**, 1743년은 **소장 기관의 간행 서지**, 1785년은 **미국 교단 내 승인**에 대한 기록이다. 출처의 성격을 구분하며 1738년 원문 자필 사료를 직접 검토했다고 주장하지 않는다.

### 4-4. 베스트팔렌 조약의 서명·공표·비준

| 날짜 | 사건 | 날짜의 역할 | 출처 ID |
|---|---|---|---|
| `1648-10-24` | IPO·IPM 최종 서명·날인 | `SIGNING_AND_SEALING` | `V316-LWL-FESTIVAL` |
| `1648-10-25` | 뮌스터에서 평화 고지 및 감사예배 | `PUBLIC_PROCLAMATION` | `V316-LWL-FESTIVAL` |
| `1649-02-18` | 주요 조약 당사자 비준서의 실제 교환 | `ACTUAL_RATIFICATION_EXCHANGE` | `V316-LEXICON-EXECUTION`, `V316-APW-BIBLIOGRAPHY` |
| `1649-02-21` | 뮌스터의 공식적 비준 축하 행사 | `PUBLIC_RATIFICATION_CELEBRATION` | `V316-LWL-FESTIVAL` |

1648년 10월의 **서명·공표**와 1649년 2월의 **비준서 교환·공식 축하**를 분리한다. 이는 학술 자료·역사가의 사건 해설을 연결한 것으로, 당시 모든 원본 비준서를 실물 감정했다는 뜻은 아니다. IPO와 IPM도 서로 다른 조약문으로 유지한다.

### 4-5. 뮌스터 조약 IPM의 출판 기록

| 날짜 | 사건 | 날짜의 역할 | 출처 ID |
|---|---|---|---|
| `1648-03-03` | Privilege text says issued at Prague royal castle on 3 March 1648; an earlier publishing authorization | `PRINT_PRIVILEGE_DATE_AS_REPRODUCED` | `IPM49-SCAN-006` |
| `1649` | Edition imprint year; not treaty date | `PRINT_EDITION_YEAR` | `IPM49-SCAN-TITLE` |

**1648년 3월 3일의 인쇄특허 날짜**는 1649년 인쇄본에 수록된 특허문에 적혀 있다. 책의 **1649년 간행 표시**와는 성격이 다르다. 1649년은 월·일이 확인되지 않은 `YEAR` 정밀도이다. 따라서 1649년 2월 18일 비준서 교환 '전/후' 어느 쪽에 인쇄본을 배치해야 하는지 이 데이터만으로 결론 내리지 않는다.

## 5. 세 가지 탐색 장면

**장면 A — 신앙고백의 탄생과 변형.** 독자가 `OV-D-011` 아우크스부르크 신앙고백을 선택하면 기존 `MEDIUM-AUGSBURG` 원고를 우선 보여 준다. 연표에서는 1530년 6월 제출과 1531년 인쇄, 1540년 수정판을 서로 다른 사건으로 찾아간다. 제출 연도를 신앙고백의 유일한 간행연도로 쓰지 않는다.

**장면 B — 공의회의 사상과 제도.** `OV-D-014` 트리엔트 교령에서 `MEDIUM-TRENT`로 이동하고 1547년 칭의 교령과 1563년 신학교 개혁령을 다른 회기로 구별한다. 교육 개혁을 읽는 과정에서 12세·14세를 동일한 서품 자격으로 합쳐 버리는 오독을 막는다.

**장면 C — 조약 서명과 출판의 시간.** `OV-D-015` 베스트팔렌 조약문에서 `THEME-WAR_WESTPHALIA`를 읽고, 서로 다른 두 시간선을 펼친다. 하나는 서명→공표→비준서 교환→공식 축하, 다른 하나는 인쇄특허 발행일과 1649년판 간행연도이다. 하나의 문서에 나오는 모든 날짜를 조약 체결일로 오인하지 않는다.

## 6. 데이터 모델 및 통합 대기 상태

- `overview_nodes` 97개: 개요 식별자·제목·범위 등급·연결 수정 이력.
- `reader_registry` 513개: 실제 원고 식별자·제목·원본 데이터셋 경로·장 번호.
- `overview_reader_edges` 156개: `PRIMARY`/`FOLLOWUP`·추가된 연구 버전.
- `historical_events` 17개: 역사 사건 ID·날짜·정밀도(`YEAR`/`MONTH`/`DAY`)·사건 유형·자료 출처.
- `event_overview_edges` 및 `event_reader_edges`: 역사 사건에 관련된 읽기 경로만 지정. 당사자의 직접 참여나 인과관계는 주장하지 않는다.
- `sequence_edges` 12개: 각 문헌·사건군 내부의 앞뒤 관계. 다른 시대·지역의 사건 사이에 임의의 인과 화살표를 만들지 않는다.

**다음 단계의 웹앱 입력 후보**로 사용할 수 있도록 JSON과 별도의 통합 대기 매니페스트를 보관하되, 실제 운영 웹앱 수집·수정은 별도 작업으로 분리한다.

## 7. 출판 보류 및 다음 검증

원래 513편의 모든 역사적 주장을 개별 원사료로 다시 검증한 것은 아니다. 원고 전체의 날짜를 자동 추출한 전수 연표도 아니다. 이번 연구의 17개 사건은 기존 V3.16·V3.19·V3.22의 명시적 날짜 항목만 통합한 **선별 사건 집합**이다. 역사적 개관의 전 영역을 포괄하지 않으므로 빠진 사건이 있다고 해서 원고가 유실된 것으로 판단하면 안 된다.

이미지와 원문 저작권은 기존 방침을 따르고, 인쇄본 사진 자체를 GitHub에 복제하지 않는다. 전문가 승인, `main` 병합, Google AI Studio 앱 배포는 모두 HOLD를 유지한다.
