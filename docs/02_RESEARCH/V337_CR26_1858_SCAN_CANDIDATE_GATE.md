# V3.37 — 1858 CR 스캔 후보 검증 장부 (2026-11-08)

**현재 게이트:** `CANDIDATE_METADATA_VERIFIED / VOLUME_AND_TARGET_FOLIOS_UNVERIFIED / DRAFT_HOLD`

## 1. 자료 식별

- Commons: https://commons.wikimedia.org/wiki/File:Corpus_reformatorum_(IA_corpusreformato09melagoog).pdf
- IA 식별자: `corpusreformato09melagoog`
- 원문 다운로드 안내: https://archive.org/download/corpusreformato09melagoog/corpusreformato09melagoog.pdf
- Commons에서 확인 가능한 메타데이터: **1858년 발행, 420 PDF 페이지, 29.19MB, NYPL 소장 Google 디지털화, IA 등록**.
- **주의:** 1858년 발행이라는 정보만으로 *Corpus Reformatorum* 제26권인지, 263–336 인쇄면을 포함하는지 **확정 불가**. Commons 메타데이터의 `corpusreformato09melagoog`는 **IA 스캔 식별자**이며 권차 9를 의미한다고 단정할 수 없음.
- 이 회차 웹 PDF 원본 호출은 큰 파일 용량으로 실패했으며 로컬 다운로드도 네트워크 오류로 실패. 해당 420쪽의 특정 인쇄면을 **0면 판독**.
- 따라서 제4·7·8조 원 인쇄면 대조 **미완료**.

## 2. 확인 가능한 별도 사료

- Bibliotheca Augustana는 기반 인쇄본을 *CR XXVI* (1858) **263–336쪽**이라고 명기: https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca00.html
- Schaff 역시 제26권(1858) **263쪽 이후**가 아우크스부르크 신앙고백 1531 초판 계열의 이문 포함 비평본임을 기술: https://www.uecf.net/books/collected-works/chapter1319.html
- 독립된 1540 Variata 발췌 PDF (33면): https://www.augsburg1540.com/uploads/1/3/8/9/138903771/1540_latin_text_from_corpus_reformandum.pdf
- 1540 발췌 PDF 0-based p.1의 실제 이미지에서, 인쇄 349–350쪽의 편집 머리말 `Ex variata Editione Wittembergensi a. 1540 ... (Ed. 3.)` 및 초판(Ed.1)과 개정판(Ed.2/4) 대조 방식 재확인. **이것은 1531 초판 263–336쪽의 원 인쇄면 판독이 아니다.**

## 3. 증거 계약

| 항목 | 값 |
| --- | --- |
| target_edition | CR XXVI (1858), 1531계열 인쇄 263–336 |
| metadata_verified_candidate_id | corpusreformato09melagoog |
| candidate_publication_year | 1858 |
| candidate_pdf_pages | 420 |
| candidate_volume_26_confirmed | NO |
| candidate_target_263_336_confirmed | NO |
| print_pages_CA_IV_VII_VIII_read | 0 |
| digital_transcription_discrepancy_pairs | 4 |
| discrepancies_resolved_against_1858_print | 0 |
| historical_variant_promotions | 0 |
| original_corpus_updates | 0 |
| publish_authorized | NO |

## 4. 다음 실제 연구 과제

1. **제26권임을 입증할 표제면 또는 권차 표기를 직접 판독**. 1858년과 420 PDF쪽만으로는 미충족.
2. 263–336 **인쇄 쪽번호→PDF 0-based 페이지** 정합성 2개 지점 이상(예: 263, 275, 300) 대조.
3. 조항 IV, VII, VIII가 등장하는 양면 스캔에서 OCR이 아닌 **인쇄 글자 이미지 판독**. 각 조항 `image_page`, `print_page`, `exact_reading`, `uncertainty`를 별도 기록.
4. `iustificenter`, `consentiere`, `malii`, `sentibant` 네 그룹은 결과 확인 전 **WEB_TRANSCRIPTION_DISCREPANCY_OPEN** 유지.
5. 완전한 출처 교감 전 웹앱 원문 자동 치환 금지. `main` 수정 및 PR 병합 금지.

## 5. 연구적 의미

1540 Variata 발췌본에서 실물 인쇄 이미지가 확인된 사실은 분명하지만, 그것이 1531 초판의 오류 네 건을 판정해 주지는 않는다. 본 게이트는 '확보한 스캔 후보'와 '검증된 사료 본문'의 혼동을 예방한다.
