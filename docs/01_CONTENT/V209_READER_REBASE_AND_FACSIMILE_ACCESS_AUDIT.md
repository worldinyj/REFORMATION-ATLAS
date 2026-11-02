# V2.09 · 10편 독자용 통합 원고(연구 초안)과 편집 참조 재구성

## 실제 완료된 범위
V2.08에서 완성된 역사 편집문단 7개를 기존 V2.02 10편 중 5편에 적용하여 **별도의 V2.09 통합 연구 원고**를 생성했다. 나머지 5편은 글자 단위로 원본과 동일하다. V2.02 자체에는 일절 손대지 않았으며, V2.09는 출판 승인되지 않은 DRAFT다.

| 항목 | 결과 |
|---|---:|
| reader_count | 10 |
| revised_reader_count | 5 |
| unchanged_reader_count | 5 |
| changed_paragraph_count | 7 |
| total_paragraph_review_units | 124 |
| section_count | 70 |
| focus_count | 30 |
| retired_focus_excerpt_anchors | 8 |
| reused_focus_excerpt_anchors | 22 |
| original_codepoints | 33179 |
| new_codepoints | 33060 |
| original_nonwhitespace_chars | 25404 |
| new_nonwhitespace_chars | 25320 |
| reviewed_witness_images | 0 |
| expert_approvals | 0 |

## 적용한 문단 교정 7개
* REV-V208-HUS-003 — HUS / PAR-V204-HUS-003 (297 → 218 codepoints).
* REV-V208-LUTHER1521-004 — LUTHER1521 / PAR-V204-LUTHER1521-004 (136 → 230 codepoints).
* REV-V208-MARBURG-002 — MARBURG / PAR-V204-MARBURG-002 (354 → 323 codepoints).
* REV-V208-AUGSBURG-002 — AUGSBURG / PAR-V204-AUGSBURG-002 (287 → 222 codepoints).
* REV-V208-AUGSBURG-005 — AUGSBURG / PAR-V204-AUGSBURG-005 (308 → 281 codepoints).
* REV-V208-TRENT-002 — TRENT / PAR-V204-TRENT-002 (250 → 223 codepoints).
* REV-V208-TRENT-003 — TRENT / PAR-V204-TRENT-003 (201 → 217 codepoints).

## 역사·신학적 맥락에 대한 교차 점검
* **WORK_IDENTITY** (WYCLIFFE, HUS): 동일 라틴어 제목 De ecclesia를 두 작품의 동일성으로 오인하지 않는다. / 미완료: 양 저작의 필사본 본문 구절 직접 교감
* **LUTHER_CHRONOLOGY** (LUTHER1517, LUTHER1521): 1517년 논제·서한·게시 전승과 1521년 심문·칙령을 서로 다른 자료 층위로 유지한다. / 미완료: 동시대 증인과 칙령 원본 변형 비교
* **WORMS_1521_EDICT** (LUTHER1521): 보름스 칙령의 5월 8일 문안과 5월 26일 서명·공표를 문서 전승 설명에 넣었다. / 미완료: 독일어 인쇄판 영인 판면의 직접 확인
* **SACRAMENT_MARBURG_AUGSBURG** (MARBURG, AUGSBURG): 마르부르크 제15조의 부분 합의/이견과 아우크스부르크 제10조의 다른 시기·정치적 맥락을 구별한다. / 미완료: 1529 마르부르크 Z/K 및 1531·1540 아우크스부르크 라틴어 이문 교감
* **AUGSBURG_VARIATA** (AUGSBURG): 1530년 제출·비공인 인쇄물, 1531년 공인 인쇄판, 1540년 개정판을 구별한다. / 미완료: 원판 인쇄본 서지 및 조항 IV/X 직접 대조
* **CALVIN_EDITION_SEQUENCE** (CALVIN1536, CALVIN1559): 1536년 초판 6장, 1539년 17장, 1559년 라틴어 최종판 4권 80장 및 1560년 프랑스어판을 분리했다. / 미완료: 개별 문장 이동을 다루는 비평판 직접 검토
* **ZURICH_VS_MARBURG** (ZWINGLI, MARBURG): 1523년 취리히 논쟁과 1529년 마르부르크 회담은 별도 사건이며 종교 강제의 문제를 생략하지 않는다. / 미완료: 취리히 시의회 원본 사건 기록
* **COUNCIL_1547_VS_1563** (TRENT): 1547년 제6회기 의롭다 함과 1563년 제23회기 신학교 규정을 별도 역사적 조치로 설명한다. / 미완료: 라틴어 교령과 지역 시행 문서
* **HUMANITIES_PUBLICATION** (HUS, LUTHER1521, MARBURG, AUGSBURG, TRENT): 7문단의 본문 개정안은 독립 편집 연구 초안이며 원본 사료 교감이나 공개 승인 상태가 아니다. / 미완료: 실제 문헌학적 심사, 사료 근거 위치 점검 및 저작권 검토

## 기술적 근거·기존 참조의 이전
1. 절의 경계 70개와 문단 124개를 V2.09 본문으로 다시 계산했다. 외부 링크/원어 사료가 정확한 문장과 연결됐다는 검증은 아니다.
2. V2.04의 기존 핵심 검토 과제 30개 중 원고 내용이 바뀌지 않은 **22개**는 고유 원문 구절의 새 위치를 자동 확인했다.
3. 변경된 문단 내부에 있던 **8개**의 과거 구절 앵커는 오해를 막기 위해 RETIRED 표시했다. 새 교정 문장과의 정확한 위치 연결은 편집자의 검토가 필요하다.
4. V2.07의 521개 문장 오프셋은 **구 V2.02 전용**이므로 새 원고에 그대로 연결하지 않는다.

## 역사 인쇄본 원본 접근 시도
1521년 보름스 칙령 `VD16 D 924` 소장본 BSB `Res/4 H.ref.287`의 디지털 식별자 `bsb00056424`를 확인했다. DDE의 디지털 서지에서 MDZ 원본으로 링크되었으나, 이 환경에서는 뷰어와 IIIF manifest가 읽히지 않았다. 원본 인쇄물 실제 영인 판면의 직접 비교: **0건**.

자료 경로: https://tueditions.ulb.tu-darmstadt.de/v/pa000008-0107
실물 디지털 뷰어: https://www.digitale-sammlungen.de/view/bsb00056424

## 다음 단계 V2.10
신규 7문단의 문장별 검토·중복 어휘 정돈과 8개 retired focus의 재고정, 새 V2.09 원고에 대한 새 70절/124문단/문장 개별 라벨의 회귀검증을 진행한다. 실물 소장본 영인 판독과 실제 원전의 이문 교감은 외부 뷰어 접근 가능 시에만 완료로 표시한다.

**RESEARCH DRAFT / `can_ship=false`; main, Google AI Studio 웹앱 미변경.**