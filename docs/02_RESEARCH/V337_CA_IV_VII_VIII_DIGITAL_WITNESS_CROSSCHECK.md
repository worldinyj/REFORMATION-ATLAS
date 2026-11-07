# V3.37 후속 — CA IV/VII/VIII 온라인 라틴어 전사 교차검토

**상태:** WEB_TEXT_CROSSCHECK_ONLY / PRIMARY_1858_PRINT_NOT_YET_READ / PUBLICATION_HOLD  
**부모:** `V337_CR26_1858_EDITION_SPLIT_IMAGE_AUDIT.md`  
**비교 일자:** 2026-11-08  
**범위:** 기존 중(中) 수준 심화정보; 원고/앱/기존 계약 미변경

## 1. 사료와 증거 등급

| ID | 증거 | 주소 | 검증 수준 |
|---|---|---|---|
| BA-IV | Bibliotheca Augustana 제4조 | https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca04.html | 편집 웹 전사 직접 열람 |
| BA-VII | Bibliotheca Augustana 제7조 | https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca07.html | 편집 웹 전사 직접 열람 |
| BA-VIII | Bibliotheca Augustana 제8조 | https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca08.html | 편집 웹 전사 직접 열람 |
| SCHAFF | Philip Schaff, *Creeds of Christendom* III, Augsburg Confession 라틴어 | https://ccel.org/ccel/schaff/creeds3/creeds3.iii.ii.html | **독립된 후기 학술 편집 본문** 직접 열람, 1858 CR 스캔 대체 불가 |
| CR26-BIB | Google Books, *Corpus reformatorum* 26 (1858) | https://books.google.com/books?id=zxERAAAAIAAJ | 서지/검색 페이지 확인, 원 인쇄면 시각 확인과 구별 |
| CR26-SCAN-CANDIDATE | NYPL Google digitization 재배포, `corpusreformato09melagoog` (1858) | https://commons.wikimedia.org/wiki/File:Corpus_reformatorum_(IA_corpusreformato09melagoog).pdf | **후보 스캔 소재 발견, 현재 회차 본문 페이지 직접 판독 불가**. 권·인쇄 페이지 식별 및 실제 면 검증 필요 |

BA 서문은 기반 자료가 CR XXVI (1858), 263–336쪽이라고 표기한다. 이 출처 관계는 BA의 개별 오기까지 1858 인쇄본에 존재함을 입증하지 않는다. Schaff 역시 1531 editio princeps 전통을 따르는 별도의 후대 편집자로서 CR XXVI를 인용한다.

## 2. 웹 전사 간 표기 비교 — 원본 교감과 혼동 금지

| ID | 조항 | BA의 실제 웹 표기 | Schaff의 실제 웹 표기 | 관찰 | 판정 |
|---|---|---|---|---|---|
| W01 | IV | `gratis iustificenter` | `gratis ... justificentur` | `iustificenter` 대 정동사 수동형 `justificentur`; 고전적 i/j 정규화는 별도 요소 | DIGITAL_WITNESSES_DIFFER / CR26_IMAGE_OPEN |
| W02 | VII | `satis est consentiere` | `satis est consentire` | 부정사 표기 차이 | DIGITAL_WITNESSES_DIFFER / CR26_IMAGE_OPEN |
| W03 | VIII | `hypocritae et malii` | `hypocritæ et mali` | `malii` 대 `mali`, ae/æ는 정규화 사항 | DIGITAL_WITNESSES_DIFFER / CR26_IMAGE_OPEN |
| W04 | VIII | `et sentibant ministerium` | `sentiebant ministerium` | 동사 표기 차이 | DIGITAL_WITNESSES_DIFFER / CR26_IMAGE_OPEN |

이 비교 결과는 **두 웹 출처 사이의 불일치**를 실제로 재현한 것이다. **원판 인쇄에 무엇이 쓰여 있는지, 1531 초판과 1540 Variata 사이의 진짜 이문인지**를 증명하는 것은 아니다. `iustificenter`가 문맥상 비문처럼 보인다는 언어학적 추정과 원 인쇄면 판독은 구별한다.

## 3. 내용 이해에 미치는 영향

- 제4조: '인간 자신의 공로나 행위가 아니라 그리스도를 통한 믿음으로 은혜롭게 의롭다 하심을 받는다'는 핵심 구조는 두 후대 전사에 공통적으로 확인된다. 다만 인용용 라틴어 표기 확정은 원본 확인 후에 한다.
- 제7조: '복음 교리와 성례 집례의 일치'가 참된 교회 일치의 핵심이라는 구조가 두 전사에 공통으로 드러난다.
- 제8조: 교회에 악인과 위선자가 섞여 있어도 성례의 유효성이 집례자의 도덕성에 의해 자동 무효가 되는 것은 아니라는 논의 및 도나투스파 비판이 두 전사에 공통이다.
- 제7·8조의 교회론을 1540년 Variata의 표현 확대와 혼동하지 말고 별도 서술한다.

## 4. 다음 검증 단위 — 우선순위

1. CR XXVI 1858 **263–336쪽 인쇄면**의 직접 열람 경로 확보(스캔 내 페이지 식별 및 해당 면 화면 판독). `corpusreformato09melagoog`는 권 일치 확인이 끝나지 않았으므로 원전 검증 증거로 승격 금지.
2. 원 인쇄 이미지에서 제4·7·8조 각각 **인쇄면 번호, 줄, 각주, 실제 글자 판독**을 기록.
3. 각 W01–W04에 `print_1858_reading`, `original_page`, `image_reference`, `verification_date`, `reviewer`를 추가. 원본 미열람 상태에서 값을 추측해 채우지 않는다.
4. 판본 차이가 아닌 웹 전사 오류로 입증된 것만 웹앱 표시 원문 교정 제안으로 승격한다.
5. 그때까지 연구 브랜치 및 Draft PR 유지. `main` / Google AI Studio 공개자료 변경 금지.

## 5. 정량 기록

- 웹 전사 직접 확인: BA 3개 조항 + Schaff 3개 조항.
- 정합성 비교: 4개 표기 쌍.
- 전사 간 불일치 재현: 4/4.
- CR XXVI 1858 **1531판 해당 인쇄면 직접 확인**: 0.
- 역사적 이문 확정: 0.
- 기존 코퍼스 변경: 0.
