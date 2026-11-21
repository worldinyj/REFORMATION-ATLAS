# 종교개혁 ATLAS — V4.75 역사학자 독립 검토 자료집

**제4권 · 1529 마르부르크 → 1530/1531/1540 아우크스부르크**  
**작성일:** 2026-11-21 · **상태:** 전문가에게 전달하기 위한 *초안*. **실제 요청 발송 0건, 실제 응답 0건, 최종 승인 0건**.

## 1. 검토 대상과 자료의 종류

검토 대상 원고는 [V4.72 L0·L1 개정본](./V472_MARBURG_1529_L0_L1_REVISED_READER_CANDIDATE_KO.md)이며, [V4.73 독립 HTML](./preview-v473-1529-1540.html)과 React 연구 컴포넌트에 같은 원고가 연결되어 있다. 사료 카드 6종은 다음을 뜻한다.

| ID | 자료 종류 | 확인 범위와 한계 |
| --- | --- | --- |
| [GA] | 마르부르크 15개 조항 — 영어 편집 번역 | 1910 WA 저본 영어 번역. 1529 서명 필사 원본 아님. |
| [GE] | 오시안더의 동시대 보고 | 루터교 참가자의 관점. 모든 사람의 내적 의도를 대변하지 않음. |
| [WP] | 취리히 1529년 인쇄본 W2119 | e-rara PDF 0기준 p6 제15조, p7 콜로폰. K/Z 자필 아님. |
| [ZA] | 취리히 Z 서명본 공식 목록 | K/Z 추가문구에 대한 기관 기록. 제15조 친필 원본 미판독. |
| [SC] | 필립 샤프의 역사·서지 연구 | 1847 초판·1854 제2판 기술은 후대 학자의 주장. 실물 판권면 미검증. |
| [GR] | 그루버 아우크스부르크 희귀본 목록 | 1530·1531·1540 판본의 소장 기술. 라틴어 제10조 실물 교감 아님. |

외부 기관의 원본 지면과 허가받지 않은 이미지를 이 자료집에 재배포하지 않는다. 각 카드 원본 공식 링크는 기계가 읽을 수 있는 [V4.75 JSON](../../research/data/ATLAS_V475_CROSS_VOLUME_REVIEW_BUNDLE.json)에 들어 있다.

## 2. 위험도별 역사 주장 14건 — 검토 전

| ID | 검토해야 할 주장 | 위험도 / 필요한 독립 검토자 | 관련 화면 사료 ID | 현재 |
| --- | --- | --- | --- | --- |
| V457-C01 | 1529년 10월 3일의 문서 날짜와 서명자 | LOW / 1인 | `[GA]` | 미검토 |
| V457-C02 | 제1–14조 및 제15조 공통 고백의 범위 | HIGH / 2인 | `[GA]` | 미검토 |
| V457-C03 | 그리스도의 몸과 피의 현존 방식에 관한 미해결 이견 | HIGH / 2인 | `[GA]` | 미검토 |
| V457-C04 | 상호 사랑과 기도 요청을 화해 성립으로 오인하지 않기 | MEDIUM / 1인 | `[GA]` | 미검토 |
| V457-C05 | 1530년 6월 25일 아우크스부르크 신앙고백 발표 | MEDIUM / 1인 | `[GR]` | 미검토 |
| V457-C06 | 제국회의 제출 문서와 인쇄본의 물리적 동일성 구분 | HIGH / 2인 | `[GR]` | 미검토 |
| V457-C07 | 1530년 비공인판 수량·판본 기준 | MEDIUM / 1인 | `[GR]` | 미검토 |
| V457-C08 | 1531년 라틴어·독일어 신앙고백·변증서 인쇄 | HIGH / 2인 | `[GR]` | 미검토 |
| V457-C09 | 1531년 인쇄 장소와 아우크스부르크 사건의 장소 구별 | HIGH / 2인 | `[GR]` | 미검토 |
| V457-C10 | 1540 Variata 제10조 표현 변경의 실물 교감 | HIGH / 2인 | `[GR]` | 미검토 |
| V457-C11 | 1540 비Variata 인쇄본의 소장번호·판본 확인 | HIGH / 2인 | `[GR]` | 미검토 |
| V457-C12 | 번역본·인쇄본·서명본·희귀본 목록의 증거 구분 | HIGH / 2인 | `[GA]` `[GR]` | 미검토 |
| V457-C13 | 1540 Variata 수용을 전체 교파에 일반화하지 않기 | HIGH / 2인 | `[GR]` | 미검토 |
| V457-C14 | 1540년 인물에게 후대 ‘칼뱅파’ 용어를 역투사하지 않기 | HIGH / 2인 | `[GR]` | 미검토 |

고위험 **10건**에는 서로 독립된 자격 있는 역사 전문가 **2인의 판단**이 필요하다. 단순 독자 테스트·서지 목록 조회·React 브라우저 통과는 역사적 승인을 대신하지 않는다. 현재 모든 항목의 reviewer1/reviewer2는 `null`, decision은 `PENDING`이다.

## 3. 반드시 보류할 다섯 문제

1. **HOLD-KZ** (HIGH) — K/Z signed Article 15 manuscript leaves have not been directly read; 해소 조건: `ORIGINAL_IMAGE_AND_EXPERT_REVIEW`.
2. **HOLD-1531-1540** (HIGH) — 1531/1540 Latin Article X original pages not yet directly collated; 해소 조건: `DIRECT_WITNESS_COLLATION`.
3. **HOLD-W2119-WA** (HIGH) — Printed W2119 vs later WA/GHDI text gap not enough to prove autograph stemma; 해소 조건: `TEXTUAL_HISTORY_REVIEW`.
4. **HOLD-HEPPE** (MEDIUM) — Heppe 1847/1854 real imprint pages have not been compared; 해소 조건: `TITLE_PAGE_AND_IMPRINT_CHECK`.
5. **HOLD-HUMAN** (HIGH) — Independent historian and reader studies unperformed; 해소 조건: `HUMAN_REVIEW`.

특히 W2119 인쇄본에서 제15조 미사 구절이 보이고 GHDI 영어 편집 번역의 해당 위치에서는 보이지 않는다는 사실은 **두 문헌을 읽어 얻은 관찰 결과**다. 이것만으로 K·Z 중 어느 쪽이 조판 저본이며 누구의 첨삭이 선행했는지를 확정할 수 없다. 헤페 1847·1854 관련 설명도 샤프의 서지 주장을 실물 표제면 판독과 구분해야 한다.

## 4. 실제 역사 전문가 검토표 — 미작성 양식

```text
claim_id:
reviewer_code: H01 / H02 (성명·연락처는 공개 저장소 밖에서 관리)
discipline_or_specialty:
original_source_ids_checked:
factual_anchor_edition_page_or_folio:
signed_autograph_directly_viewed: YES / NO / NOT_APPLICABLE
review_judgment: APPROVE / REVISE / HOLD
necessary_correction:
evidence_and_reasoning_summary:
date:
independent_second_opinion_obtained: YES / NO
conflict_resolved: YES / NO
```

**판정 규칙:** 직접 확인 불가능한 필사본/본문 교감은 `HOLD`로 남긴다. 1·2차 독립 의견이 어긋난 경우 무음 승인 금지, 보완 근거와 이견 해소 로그가 필요하다. 편집 초안의 ‘검토 후보’는 APPROVE가 아니며 실제 전문가 서명 0건이다.

## 5. 역사학자 전달용 필수 의제

- 마르부르크 제15조의 **공동 고백, 육체적 임재의 이견, 서로 사랑하라는 권고**를 어떻게 균형 있게 표현할 것인가?
- 1529 W2119 취리히 인쇄본 ↔ GHDI/WA 편집 번역본의 차이를 K·Z **서명 필사본의 차이로 곧바로 환원**하고 있지 않은가?
- 헤페 1847/1854의 판차는 **샤프의 서지 기록**인지, 실물의 실제 인쇄·표제지에 근거한 것인지?
- 1530년 제출본, 1531 인쇄본, 1540 Variata·비Variata의 관계를 **문헌 물성·원어 표현·후대 수용사**의 차원으로 나누었는가?
- 화면이 사료의 증거 유형을 정확히 구분하고 **미확정 사실을 확정처럼 표현하지 않는가?**

**안전:** 이메일 발송 0건·유료 원전 주문 0건·실제 역사 전문가 검토 0건·실제 독자 평가 0건. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`.
