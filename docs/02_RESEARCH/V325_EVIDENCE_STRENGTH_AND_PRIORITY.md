# V3.25 — 사료 강도·연결 관계 검증 우선순위 심화 감사

> **DRAFT · MEDIUM · publication HOLD**. V3.24의 12개 관계를 1개도 삭제·수정하지 않고, **주장별 근거 등급**과 **후속 원사료 대조 우선순위**를 별도 계층으로 추가했다. 이번 단계에서 당대 인쇄물의 새 실물 페이지를 직접 판독하지 않았다.

## 핵심 결과

V3.24까지 연결된 원고 513편, 개요 97건, 관계 12건의 데이터 구조를 그대로 계승하였다. 각 관계의 증거가 원본 사진인지, 후대 교정 전사인지, 도서관 서지인지, 역사학자의 해석인지 분리했다. **A·B·C·D는 이 특정 주장에 대한 증거의 범위**를 구분하는 편집 코드이지, 역사학적 진실의 확률이나 연구자의 절대적 신뢰성 평가가 아니다.

| 관계 ID | 기존 연결 종류 | 근거 구분 | 다음 검토 | 판단에 남길 제한 |
|---|---|---|---|---|
| `V324-R01` | `DOCUMENTED_INTELLECTUAL_INFLUENCE` | `C_SECONDARY_SYNTHESIS` | **P1** | 후스의 영향은 전기 연구에서 확인되지만 구절별 텍스트 차용은 미교감 |
| `V324-R02` | `FORMAL_CONFUTATION_OF` | `B_EDITED_HISTORIC_DOCUMENT` | **P0** | 정식 반박 대상 관계는 역사 문서 편집본이 뒷받침하되 당시 원인쇄본 미교감 |
| `V324-R03` | `APOLOGETIC_REBUTTAL_OF` | `B_EDITED_HISTORIC_DOCUMENT` | **P0** | 공식 반박문에 대한 변증이라는 문헌 관계, 초안과 최종 인쇄문 변별 필요 |
| `V324-R04` | `DEFENSE_OF_CONFESSIONAL_DOCUMENT` | `C_SECONDARY_SYNTHESIS` | **P1** | 1530 고백서의 변호 목적과 반박문 답변 목적을 별개 간선으로 유지 |
| `V324-R05` | `AUTHORIAL_EDITION_REVISION` | `B_INSTITUTIONAL_BIBLIOGRAPHY` | **P1** | 1531 초판에서 1540 개정판으로의 저자 개정 계보, 실제 원문 이문 검증은 아님 |
| `V324-R06` | `AUTHORIAL_EDITION_REVISION` | `B_INSTITUTIONAL_BIBLIOGRAPHY` | **P1** | BnF와 학술도서관의 판본 서지; 1539·1543·1550 중간판 반드시 보존 |
| `V324-R07` | `REPORTED_STRUCTURAL_INFLUENCE` | `D_INTERPRETATIVE_CLAIM` | **P1** | 칼뱅 초판과 루터 소교리문답의 구조적 영향은 도서관 해설의 학술 해석이며 문장 차용 미확인 |
| `V324-R08` | `INSTITUTIONAL_FOLLOW_UP_PUBLICATION` | `C_SECONDARY_INSTITUTIONAL_HISTORY` | **P1** | 트리엔트 의결–1566 로마 교리서 후속 관계, 발의·편집·교황 발행 단계를 각각 구분 |
| `V324-R09` | `DOCUMENT_AUTHORSHIP` | `B_INSTITUTIONAL_BIBLIOGRAPHY` | **P2** | 슈페너의 저술 귀속은 도서관 전시; 1675 원본이 아니라 1841 전시본 |
| `V324-R10` | `FORMATION_TO_PRINT_PUBLICATION` | `D_DENOMINATIONAL_ACCOUNT` | **P0** | 1738 형성–1743 출판은 후대 교단 해설; 1784 채택과 1785 출판/승인 이견에 연결됨 |
| `V324-R11` | `TREATY_RATIFICATION_PROCEDURE` | `C_HISTORIAN_SECONDARY` | **P1** | 1648 서명–1649 비준서 교환 구분은 역사가의 2차 연구, 외교 원본문서 감정은 아님 |
| `V324-R12` | `PRINT_PRIVILEGE_REPRODUCED_IN_LATER_EDITION` | `A_SCANNED_REPRINT_EXACT_SCOPE` | **P0** | 실제 본 1649 인쇄면 안의 1648-03-03 인쇄특허 날짜만 직접 스캔 근거; 특허 원본 검증은 아님 |

## 원문 확인의 우선순위

| 순위 | 원래 열린 쟁점 | 운영상 긴급도 점수 | 추후 확인할 내용 |
|---|---|---:|---|
| **P0** | `V324-ISS01` — 1784-versus-1785-American-Methodist-adoption | 12 | Collate minutes or edition of 1784 Christmas Conference and 1785 Discipline; keep 1785 inherited V323 event source-qualified. |
| **P0** | `V324-ISS02` — Augsburg-Confutation-primary-witness | 11 | Compare archival prints/manuscripts with historical published translation and 1531 Apology |
| **P0** | `V324-ISS06` — 1648-1649-physical-print-variants | 11 | Acquire and compare 1648 and 1649 same-treaty actual scan pages |
| **P1** | `V324-ISS03` — Wycliffe-Hus-direct-textual-borrowing | 9 | Compare dated De Ecclesia passages or verified Latin scholarly editions |
| **P1** | `V324-ISS04` — Trent-Roman-Catechism-document-status | 9 | Verify initiating decree, 1566 imprint and editorial mediation |
| **P1** | `V324-ISS05` — Luther-Calvin-structural-influence | 9 | Compare 1529 German catechism and 1536 Latin Institutes parallel thematic sections |

**점수 계산:** `영향도×2 + 증거 공백 + 독자 노출`. 각 항목은 1~3점의 편집 판단이다. P0 10점 이상, P1 8~9점, P2 7점 이하. **이 점수는 사실일 확률, 원문 인증의 정확도, 학계 합의도와 무관하다.** 증거가 약한 관계라도 잘못 이해했을 때 독자에게 큰 영향이 있으면 우선 확인하도록 배치한다.

## 추가 사료 조사: 감리교 일반 규칙의 1784년 채택과 1785년 인쇄

| 시기 | 실제 연구상 사건의 분류 | 증거 |
|---|---|---|
| `1738` (`YEAR`) | `RULES_FORMULATION_IN_LATER_DENOMINATIONAL_ACCOUNT` | `V325-UMC-GLOSSARY` |
| `1743` (`YEAR`) | `ORIGINAL_GENERAL_RULES_PAMPHLET_PUBLICATION` | `V325-UMC-GLOSSARY` |
| `1784-12` (`MONTH`) | `CHRISTMAS_CONFERENCE_ADOPTION_ORGANIZATION` | `V325-UMC-HISTORY`, `V325-UMC-FOUNDATIONAL`, `V325-UMC-ASK-DISCIPLINE` |
| `1785` (`YEAR`) | `FIRST_AMERICAN_DISCIPLINE_PRINT_IMPRINT_YEAR` | `V325-VANDERBILT-EXHIBITION`, `V325-WORLDCAT-CIST` |
| `1785` (`YEAR`) | `LATER_GLOSSARY_APPROVAL_TERM_UNRESOLVED` | `V325-UMC-GLOSSARY` |

**이번 교차 확인의 역사적 결론:** 연합감리교회 공식 역사와 기본 문헌 안내는 1784년 12월 크리스마스 연회에서 조직된 미국 감리교회가 수정된 일반 규칙을 채택했다고 설명한다. 밴더빌트 대학교 도서관은 1785년 첫 규정집 출판을 설명하고, 월드캣의 독립 서지는 **1785년 필라델피아 찰스 시스트 인쇄본**을 식별한다. 그 인쇄물의 제목은 **1784년 12월 연회**를 가리킨다. 인쇄본의 제목에 나온 회의연도를 인쇄본의 발행연도로 사용하면 잘못된다.

그러나 감리교회 용어사전은 여전히 일반 규칙이 **1785년에 승인되었다**고 명시한다. 이 표현이 1784년 채택과 구별되는 또 다른 승인 단계인지, 1785년 출판을 포괄적으로 서술한 것인지는 회의록과 1785년 규정집 인쇄면을 직접 대조하기 전까지 **확정하지 않는다.** 특히 오래된 출판물의 제목에 쓰인 날짜로 인쇄본의 실제 출판일을 추정하지 않는다.

### 새로 확인한 웹·서지 자료

| 출처 ID | 기관·사료의 성격 | 확인 범위 |
|---|---|---|
| `V325-UMC-HISTORY` | [DENOMINATIONAL_OFFICIAL_HISTORY](https://www.umc.org/en/content/doctrinal-standards-in-american-methodism) | December 1784 Christmas Conference adopted slightly modified General Rules; action date of organized church |
| `V325-UMC-FOUNDATIONAL` | [DENOMINATIONAL_OFFICIAL_OVERVIEW](https://www.umc.org/en/content/foundational-documents) | General Rules adopted continuing guidelines within MEC when organized in 1784 |
| `V325-UMC-GLOSSARY` | [DENOMINATIONAL_LATER_GLOSSARY](https://www.umc.org/en/content/glossary-general-rules-the) | 1991-dictionary-derived page gives 1738 rule making, 1743 pamphlet, 1785 approved by American Methodist church |
| `V325-VANDERBILT-EXHIBITION` | [ACADEMIC_LIBRARY_EXHIBITION](https://exhibitions.library.vanderbilt.edu/forging-a-nation/item/methodist-episcopal-church/) | 1784 conference established church; first A Form of Discipline published 1785, displayed holding is 1788 edition |
| `V325-WORLDCAT-CIST` | [LIBRARY_BIBLIOGRAPHIC_CATALOGUE](https://search.worldcat.org/ko/title/62832611) | 1785 Philadelphia Charles Cist printed volume, title describes Baltimore meeting 27 December 1784; 35,[1] pages; catalogue only |
| `V325-UMC-ASK-DISCIPLINE` | [DENOMINATIONAL_HISTORICAL_EXPLAINER](https://www.umc.org/en/content/ask-the-umc-when-was-the-first-book-of-discipline-created) | Calls first Discipline adopted in 1784 and refers to 1784 edition; publishing year must be separately proven by imprint |

연합감리교회의 서로 다른 웹페이지는 각각의 글을 확인한 것이지만 **독립적인 사료 소장기관 3곳이 되는 것은 아니다.** 따라서 같은 교단의 요약 3건을 독립된 당대 원본 3건으로 점수화하지 않는다. 도서관의 서지는 실물 소장·출판 정보에 유리하지만, 이 도구에서 1785년 원본 책장을 직접 이미지로 판독한 것은 아니다.

## 중간 깊이 역사 해설: 2편·6절

### 1. 1784년 채택과 1785년 인쇄: 같은 규칙의 두 시간

#### 웨슬리의 규칙은 먼저 공동체를 위한 것이었다

일반 규칙의 형성 연도를 1738년으로 보는 것은 감리교회가 보존하는 후대 역사 해설에 근거한다. 1743년에는 규칙을 담은 소책자가 출판되었다. 규칙이 만들어져 실제 공동체에서 사용되기 시작한 과정과 책으로 인쇄되어 배포되는 과정은 같은 종류의 역사 사건이 아니다. ATLAS에서는 두 해를 한 개의 '창립일'로 합치지 않는다.

#### 1784년 크리스마스 연회의 채택과 1785년 필라델피아 인쇄

연합감리교회의 역사 설명은 1784년 12월 볼티모어의 크리스마스 연회에서 수정된 일반 규칙을 채택했다고 기록한다. 반면 밴더빌트 대학 도서관 전시는 초기 미국 감리교회 규정집이 1785년에 처음 간행되었다고 설명한다. 월드캣 서지는 1785년 필라델피아 찰스 시스트 인쇄의 책을 특정하면서 제목이 1784년 연회를 회고한다고 기록한다. 한 권의 책에 1784년 회의가 적혀 있어도 그 자체의 인쇄 연도는 1785년일 수 있다.

#### 승인 1785년이라는 표현은 별도 주석에 남긴다

연합감리교회 용어사전은 미국 감리교회의 일반 규칙 승인을 1785년으로 적는다. 이것이 1784년 회의에서의 채택과 별도의 1785년 승인 결정을 뜻하는지, 인쇄·발행을 넓게 표현한 것인지는 당대 회의 결정문과 1785년 규정집 해당 조항의 직접 대조를 통해 확인해야 한다. 현재 공개 가능한 요약은 '1784년 채택, 1785년 출판 서지 확인'이며, 1785년이 최초이자 유일한 승인이라는 주장은 보류한다.

관련 개요: `OV-D-017`, `OV-E-027`

### 2. 연결 화살표에도 근거 등급이 필요한 이유

#### 직접 인쇄면과 뒤늦은 해설이 증명하는 내용은 다르다

V3.24 관계 가운데 1649년 뮌스터 조약 인쇄본에 1648년 3월의 인쇄특허가 재수록되었다는 진술은 과거 직접 살펴본 특정 인쇄면에 한정된다. 반면 위클리프가 후스에게 끼친 영향이나 루터 소교리문답과 칼뱅 강요의 구조적 연관은 역사학자와 학술 도서관이 편집한 설명에 근거한다. 한쪽의 구체적인 판독 사실을 다른 쪽의 해석적 주장과 같은 종류의 증거처럼 취급하지 않아야 한다.

#### 서지로 확인된 판본 연혁은 본문 이문 검증이 아니다

아우크스부르크 신앙고백의 1531년 인쇄와 1540년 Variata, 칼뱅 강요의 1536년과 1559년 저자판 사이에는 분명한 출판 계보가 있다. 하지만 특정 문장을 1531년판과 1540년판의 실제 사진에서 나란히 읽은 작업과 후대 도서관 서지에서 판본의 존재를 확인한 작업은 같지 않다. ATLAS는 '개정된 판본'의 존재를 설명하면서 문장 단위 변형의 내용은 대조 완료 이전에 단정하지 않는다.

#### 검토 우선순위는 역사적 확신도 수치가 아니다

독자가 역사적 숫자와 날짜를 잘못 이해할 위험, 아직 원사료를 확보하지 못한 정도, 웹앱 화면에서 노출될 가능성에 따라 검증 순서를 정할 수 있다. 그러나 이러한 운영용 우선순위 점수를 곧바로 사건이 사실일 확률이나 연구자의 학술적 확신도로 제시하는 것은 부적절하다. V3.25는 중요도와 위험을 관리하기 위한 편집 순서를 명시할 뿐 전문가 역사 감수나 원전 직접 검증을 대신하지 않는다.

관련 개요: `OV-D-011`, `OV-D-012`, `OV-D-015`

## 웹앱 심층정보 전달 시 안전장치

- **조건부 서술 가능:** 『일반 규칙』의 1738년 형성은 후대 교단 역사 해설, 1743년은 소책자 출판 연도이다.
- **분리해서 서술:** 미국 감리교회는 1784년 12월 구성되었고 규칙 채택을 교단 공식 설명이 기록한다. 1785년에는 초기 미국 규정집이 인쇄되었다는 도서관 서지가 존재한다.
- **승인 미확정:** 단독으로 '1785년 최초 승인'이라고 표기하지 않는다. 추가 회의록 판독 없이 '1785년은 오타'라고 고쳐서도 안 된다.
- **판본 주의:** 『기독교강요』 1536년/1559년, 아우크스부르크 신앙고백 1531년/1540년의 연혁은 도서관·역사 출처로 구분하지만 인쇄면 사이의 특정 문장 이문을 검증했다는 뜻이 아니다.
- **외교 사료 주의:** 1649년 인쇄본의 특허문 재수록은 1648년 특허 발급 원본 또는 1648년 IPM 인쇄판을 물리적으로 검증한 사실이 아니다.
- **계보 주의:** 반박·재반박, 개정, 제도적 채택, 출판/간행을 모두 하나의 ‘영향’ 관계로 병합하지 않는다.

## 연구 동결과 다음 검증

V3.24에 추가한 문헌 그래프 관계는 자동 검증을 거쳐서만 평가된다. V3.25는 문헌 관계를 추가로 확장하는 단계가 아니라, 이미 만든 관계의 한계를 더 명시하고 검증 작업을 계획에 연결하는 단계다. 513편 전체 역사적 진술을 사실 확인한 것이 아니며, 전문가 검토·`main` 병합·Google AI Studio 운영 웹앱 반영은 전부 보류한다.
