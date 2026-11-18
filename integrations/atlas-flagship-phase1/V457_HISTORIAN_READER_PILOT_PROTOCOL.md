# 종교개혁 ATLAS — V4.57 역사학자·독자 검토 실행 프로토콜

**문서 상태:** 검토 자료 준비 완료 · 역사학자 서명 0 · 실제 독자 0 · 배포 불가 (`can_ship=false`)  
**대상:** 제4권 연구 시범 화면, 1529 마르부르크 → 1530·1531·1540 아우크스부르크 자료  
**원칙:** 소수의 문서와 평가 도구를 먼저 정확히 완성하고, 전문 검토·독자 실측 전에는 연구 초안을 운영 앱에 이식하지 않는다.

## 1. 결과물과 연결

| 작업 데이터 | 경로 |
| --- | --- |
| 역사적 주장 14건·근거/한계·전문가 미승인 상태 | `research/data/ATLAS_V457_CLAIM_SOURCE_CRITICAL_REGISTER.json` |
| 독자 과제 3개·객관식 9문항·정답 및 평가 기준 | `research/data/ATLAS_V457_READER_PILOT_INSTRUMENT.json` |
| 오프라인 결정적 채점 로직 | `integrations/atlas-flagship-phase1/score-reader-session.mjs` |
| 참조 무결성/채점·거부조건 자동검증 | `integrations/atlas-flagship-phase1/reader-pilot-contract.test.mjs` |
| 연구 시범 역사 장면 데이터 | `research/data/ATLAS_PHASE0_FLAGSHIP_SCENE_1529_1540_PRIVATE_MODEL.json` |

## 2. 사료 등급과 연구상 확인 사실

1. **마르부르크 15개 조항:** German History in Documents and Images는 1529년 10월 3일의 15개 조항을 편집·영어 번역해 공개한다. 제15조는 성찬에 대한 공통 진술과 현존 방식의 미합의를 함께 기록하며 마지막에 상호 사랑과 기도를 권한다. 이 사실을 ‘제15조에서 전부 불일치’ 또는 ‘성찬론의 완전 합의’로 바꾸면 안 된다.
   - https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/the-marburg-colloquy-the-marburg-articles-1529
2. **아우크스부르크 제출과 인쇄본:** 그루버 희귀본 소장목록은 1530년 제국회의 제출, 1530년 인쇄물, 1531년 신앙고백·변증서 인쇄, 1540년 Variata와 같은 해 비Variata 소장본을 서로 구별한다. **목록에 있는 기술과 전체 원문 직접 교감은 다른 검증 단계**다.
   - https://gruber.lstc.edu/confessions/augs_apol.php
3. **문헌 사용 제한:** 독일사 문헌 사이트의 영어 편집 번역과 희귀본 목록의 실물 서지기술은 동일한 사료 유형이 아니다. 원문 인용은 저작권·판본 검토 없이는 UI에 장문 전재하지 않는다.

## 3. 역사학자 검토 절차

- 1차 검토: 종교개혁사 또는 고백문서사 분야 전문가 1인이 14건 각각에 `APPROVE / REVISE / HOLD` 및 근거 자료·원어 대조 필요 여부를 기록.
- 2차 검토: **HIGH 10건은 독립적인 두 번째 전문가 검토**를 요구. 특히 1529년 제15조, 1530년 제출 실물 대조, 1531년 출판지·언어, 1540년 Variata/비Variata 식별을 우선.
- `REVISE`는 수정할 문장과 검증된 출처를 명시하여 별도 콘텐츠 변경 기록을 작성. `HOLD`는 앱 승격 금지.
- 기존 미해결 표식 `C417-11`, `C417-12`는 별도 이력 검증 없이 신생 V457 주장 ID와 일대일로 동일시하지 않는다.
- **특별 경고:** 그루버의 1540년 비Variata 소장본은 관련 소개 문단에서 물건 번호가 명확하지 않다. 번호를 추정하지 말고 목록 담당자 또는 상세 서지로 대조.
- **시대착오 경고:** 그루버 설명에 등장하는 ‘칼뱅주의자들(Calvinists)’의 표현을 1540년 당시 당사자들이 스스로 사용한 공식 명칭으로 인용하지 않는다. 후대의 서술 용어인지 전문 검토가 필요.

### 주장별 검토 준비 상태

| 주장 ID | 범위 | 위험 | 출처 페이지 대조 | 전문가 판정 |
| --- | --- | --- | --- | --- |
| V457-C01 | Marburg date | LOW | SOURCE_PAGE_SUPPORTED | **미실시** |
| V457-C02 | Marburg agreement | HIGH | SOURCE_PAGE_SUPPORTED | **미실시** |
| V457-C03 | Marburg disagreement | HIGH | SOURCE_PAGE_SUPPORTED | **미실시** |
| V457-C04 | Marburg charity not settlement | MEDIUM | SOURCE_PAGE_SUPPORTED | **미실시** |
| V457-C05 | Augsburg presentation | MEDIUM | SOURCE_PAGE_SUPPORTED | **미실시** |
| V457-C06 | 1530 prints versus submission | HIGH | SOURCE_PAGE_SUPPORTED_WITH_LIMITS | **미실시** |
| V457-C07 | 1530 unofficial print counts | MEDIUM | SOURCE_PAGE_SUPPORTED_WITH_LIMITS | **미실시** |
| V457-C08 | 1531 publications | HIGH | SOURCE_PAGE_SUPPORTED | **미실시** |
| V457-C09 | 1531 places chronology | HIGH | SOURCE_PAGE_SUPPORTED_WITH_LIMITS | **미실시** |
| V457-C10 | 1540 Variata | HIGH | SOURCE_PAGE_SUPPORTED_WITH_LIMITS | **미실시** |
| V457-C11 | 1540 non-Variata | HIGH | SOURCE_PAGE_SUPPORTED_WITH_LIMITS | **미실시** |
| V457-C12 | Source type and certainty | HIGH | SOURCE_PAGE_SUPPORTED_WITH_LIMITS | **미실시** |
| V457-C13 | Confessional reception | HIGH | NEEDS_ADDITIONAL_SOURCES | **미실시** |
| V457-C14 | Anachronistic label | HIGH | NEEDS_ADDITIONAL_SOURCES | **미실시** |

**검토 기록 서식(각 주장별 1건):**
```text
claim_id:
reviewer_code: H01 / H02  (실명은 별도 안전한 채널에서 관리)
area_of_expertise:
review_outcome: APPROVE | REVISE | HOLD
checked_source_ids:
original_language_or_edition_checked: YES | NO | NOT_APPLICABLE
reason_and_evidence:
required_rewrite:
reviewed_on:
second_reviewer_outcome:
resolution_status: UNRESOLVED | RESOLVED
```

## 4. 독자 파일럿 — 운영자가 그대로 수행할 순서

**사전 조건:** 별도 안내문과 참여 동의를 확보하고, 적어도 6명(목표 8명)을 모집한다. 종교 정체성은 묻지 않는다. 주제 친숙도만 자발적으로 구분할 수 있다. 실명·로그인·이메일·종교적 민감정보를 기록하지 않는다.

- **과제 1 / 4분:** 1529년 연표와 L1 설명을 읽고 ‘합의한 점’과 ‘남은 이견’을 설명하게 한다.
- **과제 2 / 4분:** 1530·1531·1540년 연표와 판본 비교를 이용해 **제출·인쇄·Variata**의 관계를 설명하게 한다.
- **과제 3 / 4분:** 두 기관의 문헌 카드를 확인하여 **편집 번역 사료와 희귀본 서지목록**의 차이와 아직 모르는 정보를 말하게 한다.

각 과제 후 해당하는 3개 문항에 답한다. 총 9개 문항의 정답은 평가 JSON 안에 있으므로 **응답 전에는 독자에게 그 파일을 공개하지 않는다.** 공개 GitHub 저장소에는 정답이 있으므로 개방형 평가를 한다면 유출 가능성을 통제해야 한다.

**개인 합격(사전 등록):** 9문항 중 7개 이상, 핵심 7문항 중 6개 이상, 세 과제 모두 완료.  
**파일럿 판단 기준:** 실제 참여자 최소 6명, 개인 합격률 80% 이상, 전체 과제 완료율 80% 이상, 핵심 오해코드가 동일하게 2명 이상에게서 반복되지 않을 것.

위 수치는 **초기 파일럿 평가를 위한 사전 가설적 기준**이지 검증된 교육 효과 수치가 아니다. 파일럿에 통과해도 역사학자 승인·보안 검토를 면제하지 않는다.

### 관찰 데이터 서식 — 앱에서 자동 수집하지 않음

```text
session_id: P01 (익명 코드)
completed_tasks: {"TASK-01":true,"TASK-02":false,"TASK-03":true}
answers: {"Q01":"B","Q02":"C", ...}  (정답 사후 채점)
navigation_or_accessibility_issue:
misconception_in_own_words:   (개인식별 표현 없이 요약)
moderator_note:
```

## 5. 출시 판단 규칙

| 관문 | 통과 기준 | V4.57 현재 |
| --- | --- | --- |
| 내부 데이터 연결 검증 | 모든 질문이 존재하는 주장과 과제에 연결 | 자동검사 코드 준비 |
| 사료 대조 | 출처 페이지와 문장·서지 단위 대조 | 공개 웹페이지 예비 대조 |
| 역사 전문가 | HIGH 주장 2인 독립 검토, HOLD 0건 | **0명 / 미실시** |
| 독자 파일럿 | 최소 6명과 위 사전 기준 | **0명 / 미실시** |
| 웹 호스트/보안 | 실제 Google AI Studio 인증·라우트·서버 데이터 접근 제어 검증 | **미실시** |
| 릴리스 | 위 선행조건 모두 충족한 뒤 별도 승인 | **불가** |

`main`에 병합하지 않음. AI Studio 운영 앱 미변경. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`.

## 6. 다음 의사결정

전문 검토가 완료되기 전까지 이벤트를 무작정 늘리지 않는다. 기존 4개 사건의 연구 정확도와 3개 독자 여정의 이해·오해를 먼저 측정한다. 이후 한 차례 품질 개선을 시행하고 동일 도구로 재평가하여, 첫 화면의 정보 구조를 다른 권에 적용할지 결정한다.
