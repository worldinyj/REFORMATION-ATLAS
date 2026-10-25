# VOL-04 · 네 인물 원전·사건·관계 ID 통합 검토 V0.1

> 2026-10-25 · **연구용 편집 계약 / 승인 전 공개 불가**. 기존 `data/overview/`와 Google AI Studio 웹 코드는 변경하지 않았다.
> [JSON 전체 대응표](../../../data/deep/vol04_four_reformers_crosswalk_v01.json)

## 개요
- 대상: 루터 `OV-P-013`, 멜란히톤 `OV-P-014`, 츠빙글리 `OV-P-015`, 칼뱅 `OV-P-016` — 인물 네 명 모두 기존 정본 ID를 유지한다.
- 심층 데이터 총량: **출처 등록 61건 / 주장 61건 / 연대 앵커 43건**.
- 43개 연대 앵커를 모두 분류해 **기존 개요 사건 재사용 7건 / 별도 연구 사건 후보 36건**으로 구분. **중복 7건을 새 정식 사건으로 발급하지 않음**.
- 자료 동일성 관리: 마르부르크 당대 자료 3개(루터파 목격자·츠빙글리 목격자·공동 15개 조항)는 서로 다른 문서지만, 각 연구 파일 안의 중복 등록 3쌍은 동일 자료를 가리킨다.
- 문헌/판본 검토 제안 **17건**, 관계 추가 제안 **2건**. 모두 canonical `OV-*` ID가 아닌 **PROPOSAL** 번호이며 자동으로 정식 레코드를 늘리지 않는다.

## 1. 기존 사건 재사용: 7개 심층 앵커
| 깊이 사건 | 연결할 기존 사건 | 접근 방식 |
|---|---|---|
| `DEEP-V04-E-001` 1517 논제 | `OV-E-015` | 개요 사건의 심층 링크 |
| `DEEP-V04-E-005` 1521 보름스 | `OV-E-016` | 개요 사건의 심층 링크 |
| `DEEP-V04-E-008` 1529 마르부르크 | `OV-E-018` | 루터 관점 |
| `DEEP-V04-ZW-E-007` 1529 마르부르크 | `OV-E-018` | 츠빙글리 관점, **같은 회담** |
| `DEEP-V04-E-009` 1530 신앙고백 | `OV-E-019` | 신학·수용 맥락(루터 현장 참석 아님) |
| `DEEP-V04-ME-E-005` 1530 신앙고백 | `OV-E-019` | 멜란히톤의 작성·공적 문서 |
| `DEEP-V04-CA-E-002` 1536 강요 초판 | `OV-E-020` | **1536 초판만**, 1559 최종판과 합병 금지 |

### 주의: 1527 사건의 동명이년도 위험
`OV-E-017`의 **슐라이트하임 신앙고백**과 `DEEP-V04-ZW-E-006`의 **펠릭스 만츠 처형**은 모두 1527년이지만 **다른 사건**이다. 같은 연도이고 재세례파 관련이라는 이유로 자동 병합하면 안 된다.

## 2. 마르부르크 증거의 새 발견: 멜란히톤 직접 참석
독일 역사문서 아카이브 GHDI의 [1529년 공동 조항](https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/ghdi%3Adocument-4311)에는 **필리프 멜란히톤의 서명**이 있다. [루터파 목격자 보고](https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/ghdi%3Adocument-4284)와 [츠빙글리의 당대 보고](https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/ghdi%3Adocument-4300)도 그가 회담에 참여했음을 뒷받침한다.

- 기존 `OV-R-012`: 츠빙글리 → `OV-E-018`, 참석 관계 이미 있음.
- 기존 `OV-R-013`: 루터 → `OV-E-018`, 참석 관계 이미 있음.
- **추가 제안 `REL-PROP-V04-001`**: **멜란히톤 `OV-P-014` → `OV-E-018` (`historical_participant`)**.
- 이는 서명·발언을 확인한 출처를 바탕으로 한 **새 역사관계 후보**이며 사용자/역사 담당자 승인 전에는 기존 overview `OV-R` 정본 목록을 변경하지 않는다.

또한 칼뱅과 멜란히톤의 교류는 박물관 해설이 있으나, **직접 사료·편지 재검증 전** 새 관계로 확정하지 않는다(`REL-PROP-V04-002` HOLD).

## 3. 문헌 및 판본: 문서와 저작을 구별
- **1529 마르부르크**: 공동 15개 조항, 루터파 오지안더 목격자 보고, 츠빙글리의 보고 **서로 다른 문헌 3건**. 단일 공통 문헌으로 합치지 않는다.
- **1530 신앙고백 `OV-D-011`**: 1530 문안/1531 인쇄본/1540 `Variata`를 같은 저작 계열의 **다른 판본/문면**으로 등록 제안. 1531 『변증서』는 **독립 저술**이므로 합치지 않는다.
- **칼뱅 『기독교강요』 `OV-D-012`**: 1536 라틴 초판(6장), 1541 첫 프랑스어판, 1559 후기 라틴어판(4권 80장), 1560 후기 프랑스어판은 다른 판본/언어 관계다. 1559 출판을 **1536 사건 `OV-E-020`에 병합하지 않는다**.
- **루터 저작**: 1522 신약과 1534 완역 성경은 서로 다른 출판 사건과 문헌이므로 각각 문헌 후보.
- **1523 츠빙글리 67개 조항·1521 멜란히톤 신학총론·1541 제네바 교회규정·1549 칼뱅–불링거 합의**는 현 개요에 정식 독립 문헌 ID가 없어 **후보**만 등록.

## 4. 신학적·역사적 안전 규칙
- **HOLD-V04-01:** 1517 church-door posting not asserted as certain. 정리 규칙: `NO_AUTHENTIC_POSTING_SCENE`
- **HOLD-V04-02:** 1518 Melanchthon inaugural 28 vs 29 August. 정리 규칙: `KEEP_1518_AUGUST_APPROXIMATE`
- **HOLD-V04-03:** 1523 Zurich first disputation 27 vs 29 January. 정리 규칙: `KEEP_1523_JANUARY_APPROXIMATE`
- **HOLD-V04-04:** 1527 Felix Manz death not the Schleitheim Confession event OV-E-017. 정리 규칙: `PROHIBIT_AUTO_MERGE`
- **HOLD-V04-05:** 1530 Augsburg original, 1531 print, 1540 Variata are different textual witnesses. 정리 규칙: `LINK_EDITIONS_NOT_IDENTICAL_TEXT`
- **HOLD-V04-06:** 1536 Institutes first edition vs 1559 four-book final edition. 정리 규칙: `PROHIBIT_1559_EVENT_MERGE_TO_1536_EVENT`
- **HOLD-V04-07:** 1549 Zurich Consensus signatories Calvin and Bullinger, not Zwingli who died 1531. 정리 규칙: `NO_ZWINGLI_PARTICIPANT_RELATION`
- **HOLD-V04-08:** 1553 Servetus execution city judicial authority versus Calvin theology. 정리 규칙: `NO_CALVIN_ONLY_JUDGE_RELATION`
- **HOLD-V04-09:** Marburg 1529 three original witness objects—joint articles, Zwingli account, Osiander account—must remain distinct. 정리 규칙: `THREE_WITNESSES_ONE_EVENT`
- **HOLD-V04-10:** Luther in 1530 Augsburg confession: context and influence not physical Diet attendance. 정리 규칙: `NO_LUTHER_HISTORICAL_PARTICIPANT_FROM_TIMELINE_ASSOCIATION`

## 5. 웹앱 인수 및 작업 보류
```text
인물의 안정된 URL (/people/OV-P-013…016)
   ├─ 8권 개요 OVERVIEW (변경 없음)
   ├─ 심층 근거 블록 DEEP_RESEARCH (승인 후에만)
   ├─ 기존 사건 OV-E-* (같은 사건은 한 번만)
   ├─ 새로운 연구용 사건 DEEP-V04-* (정식 사건 미승격)
   ├─ 문헌의 원문·번역·판본 제안 (검수 전)
   └─ 시각 후보 ZIP (rights/historical review 전 공개 금지)
```

현재 상태: `DRAFT_INTEGRATION_REVIEW` / `can_ship=false` / `webapp_modified=false`. **AI Studio Build 저장소/코드/검색 색인을 변경하지 않았다.**
