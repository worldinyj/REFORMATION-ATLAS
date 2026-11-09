# 종교개혁 ATLAS V3.42.1 — 1858년 CR XXVI 실제 인쇄면과 1531년 초판 4개 표기 교감

**작성:** 2026-11-09 · **상태:** `RESEARCH_DRAFT_HOLD` · **선행:** V3.41.1  
**연구 성과:** 앞선 V3.37~3.41에서 미확정이었던 W01~W04 네 표기가 **1531년 Rhau 인쇄본**과 **1858년 『Corpus Reformatorum』 제26권의 실제 인쇄 이미지**에서 각각 어떻게 쓰였는지 비교 완료. 웹 전사 불일치의 층위 확인. **기존 원고·웹앱·main 미변경**.

## 1. 접근 실패에서 이미지 판독으로 — 검증 가능한 경로

처음에 29MB PDF 원본 전체를 GitHub Actions에서 내려받으려 했으나 다음과 같이 실패했다.
- Wikimedia Commons 원본 PDF: HTTP **429 Too Many Requests**.
- Internet Archive 원본 PDF: TLS **UNEXPECTED_EOF_WHILE_READING**.

대체 방법으로 **동일한 Commons 파일의 개별 PDF 페이지를 렌더링한 JPEG**를 요청했다. 기관의 스캔 파일 420개 PDF 이미지와 원책 인쇄 쪽번호의 관계를, 기존 스크립트가 아니라 **표본 인쇄면의 실제 머리말을 보고** 대조했다.

- Wikimedia Commons 자료: https://commons.wikimedia.org/wiki/File:Corpus_reformatorum_(IA_corpusreformato09melagoog).pdf
- 원래 소장: New York Public Library; Google 디지털화; Commons 재배포; 자료 서지: 1858년.
- 원본 저작물: *Philippi Melanthonis Opera quae supersunt omnia*, Corpus Reformatorum XXVI, 1858년, Heinrich Ernst Bindseil 편집.
- 별도 서지 검증: https://books.google.com/books?id=zxERAAAAIAAJ (CR 제26권 1858 및 신앙고백 263쪽 이하).

**물리적 주의:** 이 PDF는 **PDF 이미지 1매에 인쇄면 2쪽**이 들어 있다. 따라서 PDF 페이지 번호를 그대로 인쇄 쪽번호라고 기록하지 않는다.

| 확인한 PDF 이미지(1부터 번호) | 실제 원책 인쇄면 | 본문 |
|---|---|---|
| **162** | **275–276** | 제4조 칭의, 제5·6조, 제7조 시작 |
| **163** | **277–278** | 제7조의 계속과 제8조 전체, 제9조 이하 |
| 269 | 489–490 | 권차·인쇄쪽번호 대조를 위한 표본 |
| 273 | 497–498 | 동일한 대응 규칙 재확인 |
| 275 | 501–502 | 동일한 대응 규칙 재확인 |

W01~W04의 실제 글자에 대해서는 PDF 전체 파일 다운로드 완료 여부가 아니라 **PDF 페이지 162·163에서 추출된 1858 인쇄면 시각 판독**을 증거로 삼았다. 첫 500px 표본 16매로 쪽번호 대응을 확인한 뒤 1280px 이미지 12매에서 실제 본문을 점검했다.

## 2. 원전 이미지 — 직접 증거

- 1858 CR XXVI **인쇄 275–276쪽**: https://thumb.wikimedia.org/wikipedia/commons/thumb/3/37/Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf/page162-1280px-Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf.jpg
- 1858 CR XXVI **인쇄 277–278쪽**: https://thumb.wikimedia.org/wikipedia/commons/thumb/3/37/Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf/page163-1280px-Corpus_reformatorum_%28IA_corpusreformato09melagoog%29.pdf.jpg
- 1531년 원 인쇄본, 뮌헨 BSB **Canvas 15**: https://www.digitale-sammlungen.de/en/view/bsb00103368?page=15
- 1531년 원 인쇄본, 뮌헨 BSB **Canvas 16**: https://www.digitale-sammlungen.de/en/view/bsb00103368?page=16
- 현대 Bibliotheca Augustana의 명시적인 기준: https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca00.html (`Corpus Reformatorum XXVI, 1858, p.263–336`).
- 비교용 Schaff *Creeds of Christendom*: https://ccel.org/ccel/schaff/creeds3/creeds3.iii.ii.html

## 3. 기존 4개 의심 표기의 3중 교감 결과

| ID | 조항 | **1531년 뮌헨 실제 인쇄본** | **1858 CR XXVI 실제 인쇄면** | BA 온라인 표기 | 판정 |
|---|---|---|---|---|---|
| W01 | IV, 칭의 | `iustificentur` | **275쪽 `iustificentur`** | `iustificenter` | 두 역사적 인쇄본 일치; 웹 전사만 다름 |
| W02 | VII, 교회 | `consentire` | **277쪽 `consentire`** | `consentiere` | 두 역사적 인쇄본 일치; 웹 전사만 다름 |
| W03 | VIII, 교회 | `mali` | **277쪽 `mali`** | `malii` | 두 역사적 인쇄본 일치; 웹 전사만 다름 |
| W04 | VIII, 교회 | `ſentie-` / 다음 줄 `bant` | **277쪽 `sentiebant`** | `sentibant` | 원문 조판 형태는 다르나 정규화한 단어는 같음 |

**핵심 결론:** BA 웹의 네 표기를 '1531→1858 비평 편집 과정의 원래 이문'으로 기록하면 안 된다. 직접 본 두 역사적 인쇄본은 네 곳 모두 동일한 **정규화 읽기**를 갖고 있으며, BA 웹 문자열은 그 어느 쪽과도 일치하지 않는다. 따라서 **4건을 온라인 전사 불일치로 확정**할 수 있다. 단, BA의 잘못된 문자열이 원래 입력, OCR, 후대 수정 중 어디서 발생했는지 **원인 귀속은 아직 미확정**이다.

W04는 예외적으로 원래 **1531년 실제 인쇄의 줄바꿈**이 해설의 핵심이다. 한 행의 `ſentie-`와 다음 행의 `bant`를 이어야 한다. 1858년에는 `sentiebant`가 한 줄로 인쇄되어 있으며, BA의 `sentibant`는 양쪽 인쇄본의 표기와 다르다.

Schaff의 W01 `justificentur`는 라틴 문자 `i/j` 정규화 관습이 다르므로 **역사적 신학적 의미 변동이라고 오판하지 않는다**.

## 4. 학술적 한계 — 어디까지 입증되었는가?

**이 연구가 입증한 것:**
1. 실제 1531년 뮌헨 인쇄본의 제4·7·8조에 있는 네 단어의 정규화된 읽기.
2. 실제 1858년 CR XXVI 인쇄 275·277쪽에 있는 동일 네 단어의 읽기.
3. BA가 'CR XXVI 263–336쪽'에서 가져왔다고 표기한 웹 전사의 네 문자열이 이번 대조 인쇄본과 다른 사실.

**이 연구가 아직 입증하지 않은 것:**
1. 1530년 황제에게 제출한 필사 원본의 정확한 네 단어.
2. 모든 1531년 생존 소장본에서 인쇄 중 교정이 없었다는 주장.
3. BA 웹 표기가 **어떤 전산·편집 과정에서** 잘못되었는지의 확정.
4. 제4·7·8조의 네 철자 외의 모든 판본 차이 해결. 특히 1540 Variata는 제4조 등에서 **실제 문장 개정**이 있는 별도 역사적 판본이다.

즉 **네 표기의 교감이 끝났다고 1531년과 1540년 모든 역사적 이문이 없다고 추론하지 않는다**.

## 5. 중(中) 수준 독자용 해설 초안

### 같은 문헌을 옮긴 두 책의 한 단어가 온라인에서는 왜 달라질까요?

종교개혁 문서를 읽다 보면 현대 웹사이트에 실린 라틴어 문장과 16세기 인쇄본이 다른 경우가 있습니다. 그렇다고 이것이 곧 종교개혁자의 생각이 변했다는 뜻은 아닙니다.

아우크스부르크 신앙고백 제4조는 은혜로 의롭다 하심을 받는다는 내용을 설명합니다. 1531년 인쇄본과 1858년 비평판은 해당 문장을 같은 라틴어 동사로 전합니다. 그러나 후대 웹 전사에서는 다른 어미로 표시된 적이 있습니다. 제7·8조의 몇 단어에서도 같은 현상이 확인됐습니다.

원문을 정확히 소개하려면 **역사적 문장 개정**과 **옮겨 적는 과정에서 생긴 표기 차이**를 구별해야 합니다. 실제 1540년 개정판에서 서술이 확장된 부분은 역사적 개정으로 다루고, 인쇄된 두 원전과 불일치하는 현대 웹 전사는 별도로 교정 대상으로 표시합니다.

## 6. 보존·출판 게이트 및 다음 과제

- [x] Commons/IA PDF의 인쇄면↔PDF 번호 대응 확인.
- [x] **1858 CR XXVI 인쇄 275쪽과 277쪽 실제 인쇄 글자 직접 판독**.
- [x] V3.41의 1531 인쇄본 단어 네 건과 모두 비교 완료.
- [x] BA 디지털 전사 불일치 **4/4 확정**.
- [ ] 온라인 전사 작성·교정 이력 확인. 그 전에는 '오류 생성 원인' 특정 금지.
- [ ] 필요하다면 1531년 다른 개별 인쇄본과 교감하여 press correction 주장 검토.
- [ ] 승인 전 독자용 원고·웹앱 자동 반영 및 `main` 병합 금지.

**정량 결과:** 1531년 인쇄 이미지 2면 + 1858년 인쇄 이미지 2면(275·277, 다른 구간 276·278도 화면 확인), 4개 단어 양쪽 인쇄본 일치, 웹 전사 불일치 4건, 자동 게시 0건. 모든 결론은 `data/contracts/atlas_v342_cr26_1858_direct_print_collation.json`에서 소장본·인쇄면·디지털 이미지와 연결된다.

**상태:** Draft PR · Publication HOLD. 기존 513편 통합 원고·1,539절·723 출처, `main`, Google AI Studio 웹앱 미변경.
