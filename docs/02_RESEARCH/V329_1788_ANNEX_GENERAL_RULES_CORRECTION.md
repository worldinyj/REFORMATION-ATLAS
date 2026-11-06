# V3.29 — 1789년 ‘최초 수록’ 판단 정정: 1788년 부속 『일반 규칙』 발견

> **MEDIUM · DRAFT · publication HOLD**. V3.28에서의 역사적 과도한 일반화를 확인해 새로운 검증 자료로 명시적으로 **철회·정정**하는 연구 단계. 이전 브랜치의 본문을 무작정 덮어쓰거나 `main`으로 배포하지 않는다.

## 1. 결정적 발견과 정확한 확인 범위

존 J. 타이거트, *The Making of Methodism* (1898)의 **원 인쇄 106·107쪽**을 스캔 이미지에서 직접 확인했다.

- **106쪽(PDF 0부터 143쪽):** 1787년 뉴욕 윌리엄 로스판과 1788년 엘리자베스타운 셰퍼드 콜록판을 각각 소개한다. 1788년 콜록판에는 별도 표제지를 가진 『General Rules』 제19판이 **부속 문헌으로 수록**되었으며, 코크·애즈베리 서명과 **1787년 5월 28일 기재**가 있다고 기술한다. 같은 페이지의 각주는 **일부 재인쇄본에서 이런 부속 문헌들이 생략되었다**고 경고한다.
- **107쪽(PDF 0부터 144쪽):** **1789년 제5판**을 뉴욕 윌리엄 로스 인쇄로, **1790년 제6판**을 필라델피아 R. 에이킨 부자 간행으로 서술한다. 1790년 일부 부속 문헌을 별도 본문 절로 재배치한 내용도 기술한다.
- 반더빌트대학교 도서관의 희귀본 목록에서도 실제 **1788년 셰퍼드 콜록 인쇄본**을 소장한다고 확인된다.

따라서 “**1789년에 『일반 규칙』 전문이 미국 감리교 규정집에 처음 인쇄·수록되었다**”라는 V3.28의 설명은 **역사적 서지 근거와 충돌하므로 철회**한다.

### 직접 본 것과 직접 보지 않은 것

| 판독 여부 | 물리적/역사적 대상 | 판단 |
|---|---|---|
| **시각 판독 2쪽** | 1898년 타이거트 연구서 **106·107쪽** | 역사 서술·서지 설명을 그 당시 인쇄면에서 확인 |
| **원문 미판독** | 1788년 콜록판의 『일반 규칙』 별도 표제지·본문 | 타이거트의 서지·대학 희귀본 소장 정보에서 간접 확인 |
| **원문 미판독** | 1789년 제5판 『일반 규칙』 전체 | 타이거트·1912년 수집가 증언 등에서 서지 확인 |
| **원문 미판독** | 1785년 찰스 시스트 초판 제16·17문답 | 학술 인용·도서관 목록만 확인 |
| **교감 0쌍** | 1788년판과 1789년판의 동일 본문 문단 | 두 시대 인쇄본 자체를 나란히 대조하지 못함 |

**1788년에 부속 수록이 확인된다는 사실은 ‘1788년이 역사상 최초 수록’이라는 의미가 아니다.** 1785~1787년 실제 인쇄본의 부속물 여부는 아직 전수 확인하지 않았다.

## 2. 판본과 부속문헌을 분리한 연구 그래프

| 노드 | 출처가 확인한 관계·한계 |
|---|---|
| `V329-W01` (1785) | **1785_CIST_FIRST** — FIRST_EDITION_PRINT_CATALOGUED |
| `V329-W02` (1787) | **1787_NEW_YORK_ROSS** — DIFFERENT_HISTORICAL_EDITION |
| `V329-W03` (1788) | **1788_ELIZABETHTOWN_KOLLOCK** — RULES_SEPARATE_ANNEX_ATTESTED_BY_1898_HISTORIAN |
| `V329-W04` (1787) | **GENERAL_RULES_NINETEENTH** — INTERNAL_DATE_1787_05_28_NOT_1788_IMPRINT |
| `V329-W05` (1789) | **1789_FIFTH_NEW_YORK_ROSS** — HISTORIC_BIBLIOGRAPHIC_RECORD_NOT_ORIGINAL_PAGE_INSPECTION |
| `V329-W06` (1790) | **1790_SIXTH_PHILADELPHIA_AITKEN** — APPENDED_USEFUL_PIECES_REDESIGNED_AS_NUMBERED_SECTIONS |
| `V329-W07` (1992) | **FACSIMILES_FIRST_FIVE_DISCIPLINES** — POTENTIAL_SOURCE_PAGES_NOT_INSPECTED_ANNEX_POSSIBLE_OMISSION |

### 근거 있는 방향성 링크

- **`V329-REL01` — `HISTORIAN_ATTESTED_SEPARATE_ANNEX`**: `V329-W04` → `V329-W03`. 1787-dated nineteenth General Rules included as separately titled annex in 1788 edition
- **`V329-REL02` — `EDITION_SEQUENCE_NO_PASSAGE_EQUIVALENCE`**: `V329-W02` → `V329-W03`. 1787 New York Ross and 1788 Elizabeth-Town Kollock editions are different impressions
- **`V329-REL03` — `EDITION_SEQUENCE_NO_PASSAGE_EQUIVALENCE`**: `V329-W03` → `V329-W05`. 1788 annex precedes 1789 fifth; exact changed clauses unknown
- **`V329-REL04` — `LATER_SECTION_FORMAT_DEVELOPMENT`**: `V329-W05` → `V329-W06`. 1790 sixth reorganized some useful pieces into numbered sections; not all attachment positions verified
- **`V329-REL05` — `RULES_KNOWN_BUT_PRINTING_NOT_YET_PROVEN`**: `V329-W01` → `V329-W03`. 1785 Q16 refers to Rules; 1788 distinct printed annex described, no assertion that 1788 was first
- **`V329-REL06` — `FACSIMILE_NOT_AUTHENTICATED_COMPLETE`**: `V329-W03` → `V329-W07`. 1992 reprint series discoverable but annexes may have been omitted, needs physical comparison

이 링크는 도서의 **인쇄·서지 계보**를 나타내며, 문장별 저작권·개작·문헌 차용이 직접 교감됐다는 뜻이 아니다. 특히 1787년 5월 28일은 부속 『일반 규칙』 문헌에 표시된 날짜일 뿐, **1788년 책의 간행일로 전환하지 않는다.**

## 3. 구버전 정정 이력: 이전 기록은 연구 추적을 위해 보존

| 정정 카드 | 해당 버전·파일 | 판정 | 수정된 판단 |
|---|---|---|---|
| `V329-CORR01` | V3.28 `data/contracts/atlas_v328_methodist_1785_1789_witness_scope.json` | `SUPERSEDED_OVERBROAD` | 1788 edition separate-titled General Rules annex attested by 1898 printed history |
| `V329-CORR02` | V3.28 `docs/02_RESEARCH/V328_METHODIST_1785_1789_RULES_WITNESS_AUDIT.md` | `SUPERSEDED_OVERBROAD` | 1788 independent annex existed; 1789 disposition and changes still unresolved |
| `V329-CORR03` | V3.27 `docs/02_RESEARCH/V327_METHODIST_QA_EDITION_CONCORDANCE.md` | `RESTRICT_HISTORICAL_SCOPE` | Earlier annex from 1788 recorded; first-ever historical print uncertain |
| `V329-CORR04` | V3.26 `data/contracts/atlas_v326_methodist_1784_1785_discipline_witness_audit.json` | `SCOPE_CLARIFICATION` | 1788 holding at Vanderbilt and 1898/1912 bibliographic witnesses show edition existed; older 'none found' means then unavailable |

이 정정은 과거 판단을 숨기는 작업이 아니다. **일부 연구자는 1788년판을 못 찾았다는 기록을 남겼으나**, 타이거트의 상세 서지·1912년 수집가의 실물 소장 증언·현행 반더빌트대학교의 소장 기록은 **1788년판의 존재를 지지**한다. 옛 연구자의 ‘소장본을 찾지 못함’과 ‘실제 판본이 없었음’은 논리적으로 다르다.

## 4. 중간 깊이 심화 해설 — 3편·9절

### 1. 1789년 최초 수록설의 정정: 1788년 별도 『일반 규칙』

#### 새로 발견된 한 쪽의 역사적 무게

1898년 타이거트 『The Making of Methodism』 인쇄면 106쪽의 사진을 확인하자 1788년 감리교회 규정집에 『General Rules』가 별도 표제지를 가진 부속 문헌으로 수록됐다는 기술이 나타났다. V3.28의 ‘1789 최초 수록’이라는 포괄적 판단은 더 이른 사례와 충돌하여 정정해야 한다.

#### 1787년 부속 문헌 날짜와 1788년 간행연도의 차이

같은 자료에 따르면 1788년 책은 셰퍼드 콜록이 엘리자베스타운에서 간행했고, 부속된 『일반 규칙』은 코크와 애즈베리의 서명을 갖춘 제19판으로 내부 날짜가 1787년 5월 28일이었다. 1787년 서명일은 1788년 책의 인쇄일이 아니다.

#### 재인쇄본에 빠진 부속 문헌

타이거트는 1788년 및 뒤이은 책의 일부 부속 문헌이 후대 재인쇄본에서 빠졌다는 각주를 남겼다. 후대 축약판만 검색하면 원래 출판물의 범위를 오해할 위험이 있다. 부속 표제지·권말 경계·별도 인쇄물 여부는 1788년 실물을 직접 볼 때 검증할 과제다.

관련 개요: `OV-D-017`, `OV-E-027`

### 2. 1787·1788·1789·1790년 미국 감리교 판본의 계보

#### 1787년 뉴욕과 1788년 엘리자베스타운

타이거트는 1787년 뉴욕 윌리엄 로스판과 1788년 엘리자베스타운 콜록판을 서로 다른 인쇄본으로 기술한다. 반더빌트 도서관은 실제 1788년 희귀본 소장 정보를 제공한다. 따라서 1788년판을 찾지 못했다는 오래된 연구자의 말은 그 시점의 조사 한계이지 판본 자체가 없었다는 결론이 아니다.

#### 1789년 제5판의 인쇄인과 남은 본문 문제

타이거트 107쪽은 1789년 제5판을 뉴욕 윌리엄 로스 인쇄로 적는다. 1912년 감리교 신문의 수집가는 1789년 제5판의 실물도 소장했다고 보고했다. 두 기록은 서지에 힘을 더하지만 1789년 『일반 규칙』의 문단·절 번호·회원시험 변경 구절을 직접 사진으로 본 것은 아니다.

#### 1790년 제6판의 절 번호 체계

1898년 서지 연구는 1790년 필라델피아 제6판에서 이전의 일부 ‘유용한 부속 문헌’이 본문 제35절 이후의 번호 체계로 옮겨졌다고 설명한다. 문헌을 부록으로 인쇄하는 일, 본문으로 재배열하는 일, 내용을 개정하는 일은 서로 다르다. 『일반 규칙』이 정확히 어디에 놓였는지는 원본 대조로만 판정한다.

관련 개요: `OV-D-017`, `OV-E-027`

### 3. 역사적 문헌의 ‘원본 확인’과 ‘옛 연구서의 증언’ 구별

#### 이번에 직접 본 것은 1898년 역사 인쇄면이다

이번 연구에서 직접 시각적으로 확인한 두 페이지는 1898년 타이거트 저서의 인쇄면 106·107쪽이다. 거기에 서술된 1788년과 1789년 원래 책의 해당 면은 아직 직접 열어 보지 않았다. 당대 역사학자 기록과 역사 원본 교감을 같은 수준으로 표현하지 않아야 한다.

#### 1912년 수집가와 현대 대학도서관의 증거

1912년 신문 수집가는 1788년판이 가죽 제본이었다고 하고 1789년 제5판도 실제 소장했다고 적었다. 반더빌트 도서관의 현행 희귀본 소장 목록은 1788년판을 명시한다. 이 둘은 타이거트의 서지 기술을 다른 경로로 보강하지만 원래 『일반 규칙』 텍스트의 장절을 직접 교감해 주지는 않는다.

#### 정정 이력을 지우지 않고 연결하기

V3.28의 잘못된 최초 수록 해석은 연구 기록에서 삭제하거나 몰래 덮어쓰지 않고 V3.29의 정정 카드로 연결했다. 1788년 부속 수록이 확인된 역사 연구 진술과, 1788년이 실제 최초였는지·1789년에 어떤 배열 변화가 있었는지는 미완료 과제로 분리한다. 이 방식은 장래 독자가 왜 해석이 바뀌었는지 추적하게 한다.

관련 개요: `OV-D-017`

## 5. 재확인한 자료 12건

| ID | 자료 성격·열람 범위 | 주소 |
|---|---|---|
| `V329-S-TIGERT106` | `1898_PRINT_P106_VISUALLY_SCREENED` — PDF page index 143; 1788 Kollock Elizabethtown edition with separate-titled General Rules nineteenth edition signed Coke/Asbury dated 1787-05-28; reprints omitted annexed useful pieces | [원자료/서지](https://upload.wikimedia.org/wikipedia/commons/8/83/The_making_of_Methodism-_studies_in_the_genesis_of_institutions_%28IA_cu31924009792353%29.pdf) |
| `V329-S-TIGERT107` | `1898_PRINT_P107_VISUALLY_SCREENED` — PDF page index 144; 1789 fifth edition New York William Ross, 1790 sixth Philadelphia Aitken and shift of selected useful pieces into numbered sections | [원자료/서지](https://upload.wikimedia.org/wikipedia/commons/8/83/The_making_of_Methodism-_studies_in_the_genesis_of_institutions_%28IA_cu31924009792353%29.pdf) |
| `V329-S-VANDERBILT1788` | `ACADEMIC_LIBRARY_HOLDING` — 1788 Shepard Kollock edition held in Divinity Library Rare Books, edition existence independently confirmed | [원자료/서지](https://exhibitions.library.vanderbilt.edu/forging-a-nation/item/methodist-episcopal-church/) |
| `V329-S-GOOGLE1788` | `1788_DIGITAL_BOOK_METADATA` — 1788 edition published by Shepard Kollock and digitized, original appendix page not inspected | [원자료/서지](https://play.google.com/store/books/details/Methodist_Episcopal_Church_A_Form_of_Discipline_fo?id=f7FuNMZ4iLwC) |
| `V329-S-NEWS1912` | `1912_NEWSPAPER_OCR_HISTORIC_WITNESS_REPORT` — Original-era antique book collector reported calf-bound 1788 copy and original 1789 fifth edition, plus warning that facsimile reprints incomplete; page image screenshot failed | [원자료/서지](https://texashistory.unt.edu/ark:/67531/metapth1834850/m1/10/) |
| `V329-S-EMORY` | `NINETEENTH_CENTURY_HISTORY_SEARCH_EXCERPT` — Emory printed p83 says 1788 edition had not been found by that author; modern extant copy disconfirms nonexistence, PDF 23MB cannot open screenshot | [원자료/서지](https://upload.wikimedia.org/wikipedia/commons/b/bd/History_of_the_discipline_of_the_Methodist_Episcopal_church_%28IA_historyofdiscip00emor%29.pdf) |
| `V329-S-PETERSON` | `1889_HISTORIC_STUDY_BIBLIOGRAPHIC_CONTEXT` — Earlier 1789 first Rules inference from later revision history must be restricted; 1789 original full text unseen | [원자료/서지](https://www.loc.gov/item/36023388/) |
| `V329-S-BANGS` | `HISTORIC_SOURCE_SECONDARY_TEXT` — Historical author describes 1789 fifth edition General Rules temperance wording, not first-ever inclusion proof | [원자료/서지](https://ccel.org/ccel/bangs/history2/history2.ii.ii.ii.html) |
| `V329-S-ASBURY` | `EDITED_HISTORICAL_REFERENCE` — 1789 fifth-edition preface printed 20 March per editorial note, not exact membership probation effective date | [원자료/서지](https://wesley.nnu.edu/other-theologians/francis-asbury/the-journal-and-letters-of-francis-asbury-volume-ii/francis-asbury-the-letters-vol-2-chapter-4/) |
| `V329-S-FACSIMILE` | `MODERN_SPECIALIST_BIBLIOGRAPHY` — 1992 collected facsimiles of first five Discipline volumes 1785–1789; reproduction may omit independent annexes | [원자료/서지](https://allegheny.pressbooks.pub/methodistbibliography/chapter/5-2-history-and-development/) |
| `V329-S-BRIDWELL` | `1785_LIBRARY_HOLDING` — Cist first 1785 title held; membership Q16/17 original print pages not directly inspected | [원자료/서지](https://bridwell.omeka.net/exhibits/show/asbury/item/497) |
| `V329-S-DUKE` | `ACADEMIC_SEARCH_INDEX` — 1785 Q16 two-month trial and handing Rules at first meeting from secondary quotation, NOT full Rules appendix scanned | [원자료/서지](https://dukespace.lib.duke.edu/bitstreams/e31203e3-acf1-48c5-adac-e8215017dbb7/download) |

**원본 검증 방법론:** 1898년 연구서의 특정 페이지를 실제 스캔에서 읽었다는 사실을 1788년 원본 자체의 페이지 직접 판독으로 승격하지 않는다. 반대로 원본의 현행 소장 목록을 재확인하여 1788년판 자체를 가상의 출판물로 취급하지도 않는다. 1912년 신문의 기사 본문은 웹 OCR에서 확인되었지만 PDF 개별 스크린샷은 열람에 실패했으므로 시각 판독 페이지 수에 합산하지 않는다.

## 6. 추가 원본 대조가 필요한 연구 과제

- **P0 · `V329-I-1788_ANNEX_PAGE`**: Check original Kollock 1788 book's standalone General Rules 19th edition title and text
- **P0 · `V329-I-1789_FIFTH_ORIGINAL`**: Read original William Ross fifth edition complete General Rules placement and compare 1788 appendix
- **P0 · `V329-I-1785_Q16_Q17_P9`**: Directly inspect first Cist 1785 original Q16 and Q17 text, not just later thesis
- **P0 · `V329-I-1789_6MONTH_ORIGINAL`**: Validate 1789 original six-month member probation, separate from General Rules appendix history
- **P1 · `V329-I-BEFORE_1788_FIRST_PRINT`**: Compare originals 1785,1786,1787 before calling 1788 'first'
- **P1 · `V329-I-FACSIMILE_OMISSION`**: Verify 1992 facsimile and later reproductions did not omit annexes
- **P1 · `V329-I-EMORY_ACCESS_1788`**: Check Emory printed p83 'no 1788 found' alongside Vanderbilt extant 1788 copy
- **P1 · `V329-I-1789_PRINT_DATE_VS_EFFECT`**: Check whether printed March 20 1789 note and actual membership rule effective dates differ

### 독자용 콘텐츠 금지 표현

- 1789 first ever General Rules printing superseded
- 1788 first ever printing NOT proven
- 1787 May 28 internal Rules date is NOT 1788 book's imprint date
- 1898 book print screens are NOT 1788 first print scans
- 1789 six-month rule separate from appendix literature
- Modern reprints may omit separately titled appendices

## 7. 연구·배포 경계

이번 V3.29는 **역사 해석 정정 4건**, 정선 판본·부속문헌 노드 7건, 근거 연결 6건, 중간 깊이 해설 3편·9절을 신규 구조화한 것이다. 원래 ATLAS **513편·1,539절**, 개요 97건, 원래 출처 기록 723건은 수정하지 않는다.

**검증을 위해 다음과 같은 연구 산출물을 생성한다:** 정정 이력 JSON, 근거별 판본·부속문헌 그래프 JSON, 1788/1789 실제 인쇄면 후속 확인 목록 JSON. 이들은 검토용이며 사용자가 병렬 개발 중인 Google AI Studio 앱이나 `main`에 넣는 배포용 콘텐츠가 아니다.
