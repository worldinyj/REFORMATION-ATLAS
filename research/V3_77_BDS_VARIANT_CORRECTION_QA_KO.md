# 종교개혁 ATLAS V3.77 — BDS 1988 사본 표제·어형 정정 사본 및 회귀검증

**연구 기준일:** 2026-11-14  
**계승:** research/atlas-v376-claim-evidence-matrix  
**브랜치:** research/atlas-v377-bds-apparatus-correction-qa  
**상태:** RESEARCH_ONLY / DRAFT / NOT_APPROVED / CAN_SHIP=false

## 1. 실제 완료 작업

V3.61의 `research/data/V3_61_FOUR_QUESTIONS_WITNESS_CROSSWALK_DRAFT.json`을 읽고, 해당 사본은 보존하면서 오류 두 항목만 반영한 별도 완성 JSON 파일을 생성했다.

- **수정 JSON** `research/data/V3_77_FOUR_QUESTIONS_WITNESS_CROSSWALK_CORRECTED_DRAFT.json`
- **읽기 전용 QA 스크립트** `research/tools/validate_v377_witness_patch.py`
- **원본 Git blob SHA** `d277b723d35db913d2e58e983274dc047ec2b87b`, 수정본 `correction_provenance`에 고정
- GitHub 저장 후 원본 및 수정본을 **다시 가져와서** 외부 검증 실행: source SHA, A 어형, B 생략, 기타 사본 이문 유지, Q1~Q4 본문 데이터 유지, can_ship=false, 원본 불변, **7/7 PASS**.
- Python QA 파일은 재현을 위해 저장하였다. 이번 작업 중 GitHub에서 재조회한 두 JSON에 대한 동등한 JS 검증은 실행하여 통과했으나, Python 파일 자체를 로컬에서 실행했다고 보고하지 않는다.

## 2. 1988년판 p.218의 문서 교감 원칙

기관 본문: https://digi.hadw-bw.de/view/bds6_1/0222  
DOI: https://doi.org/10.11588/diglit.29831#0222

### 2.1 V361-V01 어형

1988년 편집 해설은 A의 예시를 `für stellet`, B·C·D의 예시를 `fürstellt`로 명시한다. V3.61 JSON의 A `stellet`는 `für` 부분이 누락된 전사다.

**수정:** `forms.A="für stellet"`.  
**유보:** 이는 해당 학술판 편집 장치의 **어형 비교 예시**이고, 이를 Q1~Q4 중 특정 질문의 문장에 억지로 연결하지 않는다.

### 2.2 V361-V04 표제

p.218의 편집 기본 본문(Leittext)은 `Erlüterung der Witembergischen Articklen durch die predicanten von Straßburg gegeben`이라는 제목을 제시한다. `a)—a) B`는 B 사본에서 해당 구간이 생략된다는 각주 장치다. C와 D에는 서로 다른 대체 표제가 인용된다.

**수정:** `forms.B=null` (해당 제목 구간 생략); `forms.A`는 편집 기본 본문에 나타나는 제목의 읽기임을 밝히되, A 원고 표제의 물리적 진위는 직접 대조하지 못했다는 표시를 보존.

**유보:** 현재 증거가 B에 *모든 형태의 머리글이나 표제가 전혀 없다*는 광범위한 판단까지 입증한 것은 아니다. 이 각주가 표시한 범위의 **해당 기본 표제 생략**으로 해석한다.

## 3. 부수적으로 확인한 p.217의 원고 계보

기관 본문: https://digi.hadw-bw.de/view/bds6_1/0221

BDS 제16문서 편집자는 A를 Zürich Staatsarchiv `E II 337`, B를 `E II 347`, C를 Basel UB `MSA VI 43a`, D를 St. Gallen Stadtarchiv `Tr. Q 1b, Nr.31, Anlage B`로 열거한다. D는 `1536-07-23 부처→바디안` 개인 서신과 **다른 원고**이므로 혼합하지 않는다.

이는 기존 V3.76 증거 매트릭스의 원고 식별 항목을 유지할 이유이며, 현재 D 사본의 현대 청구기호·실물 이미지는 아직 직접 검증하지 못했다.

## 4. 증거와 공개 등급

| 검증 대상 | 결과 |
|---|---|
| BDS p.218 웹 OCR 내용 | PASS |
| 1988 학술판 페이지 고해상도 스크린샷 대조 | NOT_DONE |
| V3.61 원본 GitHub 읽기 및 SHA 보존 | PASS |
| 정정 JSON 신규 저장 | PASS |
| 정정/원본 재조회 후 일곱 가지 핵심 JS 검증 | PASS (7/7) |
| Python 읽기 전용 QA 코드 저장 | PASS |
| Python QA 파일의 실제 로컬 실행 | NOT_RUN_IN_THIS_TURN |
| BDS A·B 사본의 필사 원본 교감 | NOT_DONE |
| 16세기 사료의 필사자·표제 자필 여부 | NOT_DONE |
| Q1~Q4 정확한 문장별 A–D 대조 | NOT_DONE |
| 전문가 승인 및 513편/웹앱 반영 | NOT_APPROVED |

## 5. 출처 계층과 품질 규칙

- 1988 비평판의 **편집 장치**를 확인한 것이지 16세기 물리적 사본의 외교적 완전 전사가 아니다.
- 기본 본문(lemma), 사본별 variant, 편집 주석을 다른 필드로 취급한다.
- 원본 V3.61 JSON은 역사적 연구 이력으로 보존; 정정 사본에 소스 SHA와 수정 내역을 명시한다.
- 잘못된 원본을 삭제하거나 조용히 덮어쓰지 않는다.
- 서신 7/17 연대 갈등 및 7/23 Bucer→Vadian 직접 확인 문제는 **이번 수정 범위 밖**이다.

## 6. V3.78 권장 연구

1. BDS 6/1 인쇄 p.219–226의 실제 본문·주석을 구간별로 읽고, 4문답에 나타난 정확한 시작·종결 문장을 식별한다.
2. 기존 Barge 1905 II 부록 50 pp.603–606의 Q1~Q4를 BDS의 문장 단위와 각각 대조해, `TOPICAL_ONLY`에서 `SENTENCE_ALIGNMENT_CHECKED`로 올릴 수 있는 항목만 승격.
3. 변경 사항을 검사하는 추가 회귀 테스트를 513편 콘텐츠 매핑과 연계하되, 실질적인 원고 패치는 전문 검수 이후에만 작성.
4. 1536년 7월 23일 Bucer→Vadian 서신에 대한 미발송 기관 조회문은 독립 후속 과제로 유지.

## 7. 최종 판정

**V3.77 작업 완료 범위:** 2개 이문 정정이 반영된 JSON 연구 사본, 회귀검증 프로그램, 한국어 보고서 작성. 다만 원전 교감의 전체 승인·출판은 불가하므로 `CAN_SHIP=false` 유지. main, 기존 역사 원고 513편, 앱, V3.61의 원본 파일 모두 변경하지 않음.
