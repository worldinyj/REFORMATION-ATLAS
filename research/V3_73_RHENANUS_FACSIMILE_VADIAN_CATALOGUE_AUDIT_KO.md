# 종교개혁 ATLAS V3.73 — 레나누스 1886 판면 접근 검증·바디안 서신 개별 원고 검색 경로 감사

**기준일:** 2026-11-14  
**계승 브랜치:** `research/atlas-v372-brieffer-1886-direct-edition-and-vadian-gate`  
**현 브랜치:** `research/atlas-v373-rhenanus-facsimile-vadian-catalogue-audit`  
**상태:** RESEARCH_ONLY / DRAFT / NOT_APPROVED / CAN_SHIP=false  
**변경 경계:** 신규 연구 파일만. `main`, 기존 역사 원고 513편, Google AI Studio 웹앱, 과거 보고서는 수정하지 않음.

## 1. V3.73 목표 및 최종 판정

목표는 (A) Horawitz–Hartfelder 1886 인쇄 p.421–422 시각 교감, (B) *Vadianische Briefsammlung* V p.339 독립 원어 본문 또는 해당 서신 디지털 원본 확보였다.

**이번 단계는 두 가지 원문 이미지 대조를 완료하지 못했다.** 대신 실제 인쇄판의 신뢰 가능한 서지 대조, 검색결과의 오연결 배제, Vadianische Sammlung의 원고 단위 디지털 목록 및 PDF 자산 경로 확인까지 완료하였다. 확인되지 않은 판독문을 새로 만들지 않는다.

## 2. 레나누스 1886: 동일 판본의 서로 다른 소장본 식별

- 프랑스국립도서관 BnF 공식 서지: https://catalogue.bnf.fr/ark:/12148/cb31206298d — Horawitz·Hartfelder, *Briefwechsel des Beatus Rhenanus*, Leipzig 1886, XXIV+700쪽.
- Google Books, 바이에른주립도서관 소장 디지털화본: https://books.google.com/books/about/Briefwechsel_des_Beatus_Rhenanus.html?id=y0WcfekwCksC
- Google Books, Cornell 소장 디지털화본: https://books.google.com/books?id=gSE2AQAAMAAJ
- 앞선 V3.72 직접 판독 OCR 원천: Internet Archive item `bub_gb_T6sUAAAAYAAJ`, https://archive.org/details/bub_gb_T6sUAAAAYAAJ
- V3.72 출전 결과를 그대로 보존: 서신 **Nr.297**, 작성일 1536-07-21, 1886판 **서신 시작 인쇄 p.421**, 대표단 7월 14일 출발 기록은 **인쇄 p.422**.

검증한 BnF·Google Books의 **서지 및 디지털 원천 정보는 1886년판의 정체성을 입증하지만 p.421–422 글자들을 시각 확인했다는 증거가 아니다.** 판면 이미지 접근은 PENDING.

### 링크 무결성 경보

검색 결과 중 한 URL은 ‘Renano Briefwechsel.pdf’라는 이름과 책 표지를 검색 결과에 노출했지만, 실제 웹 PDF 열람은 전혀 다른 1685년 Petar Bogdani의 *Cuneus Prophetarum*으로 우회되었다.
- 문제 링크: https://docenti.unimc.it/claudio.micaelli/teaching/2021/24241/files/Renano%20Briefwechsel.pdf
- 실제 도착: `pdf.arkiva.me/Libra/1685/1685-PDF-L-Cuneus-Prophetarum-Ceta-e-profetenve.pdf`.
- **판정:** WRONG_DOCUMENT_REDIRECT. 해당 PDF는 **1886년 Rhenanus 원문 증거에서 제외**.
- 재현 QA: 링크 문구/검색 스니펫으로 파일을 신뢰하지 말고, 실제 연 URL·표지·저자·출판연도·목표 인쇄쪽을 각각 확인한다.

## 3. 바디안 서신집: 공식 아카이브의 개별 편지 자산 연결 확인

- 성갈렌 역사학회 출판목록: https://www.hvsg.ch/mitteilungen.php — *Vadianische Briefsammlung* V, 2. Hälfte, **1536–1540**, 1905, 역사학회 간행물 **29/2**.
- 장크트갈렌 기록보관소의 연구 안내: https://stadtarchiv.ch/forschungsprojekte/vadianische-briefsammlung/
- 해당 설명에 따르면 컬렉션은 4,500건 이상의 원본·사본 편지로 구성되며 swisscollections·장크트갈렌 도서관망에서 개별 항목을 검색할 수 있다. 편지별 목록에는 디지털 원고와 기존 편집판 발췌 연결이 포함될 수 있다.
- Kalliope 총괄 목록: https://kalliope-verbund.info/gnd/findingaid?fa.enum=1&fa.id=CH-002121-2-991170432739305501 — 컬렉션 `VadSlg Ms 30–41a`, 3790개 카탈로그 항목으로 표시됨(전체 4500건 원고수와 목록 항목수는 서로 다른 단위).
- 항목 연결의 실제 예(다른 역사적 편지임): https://kalliope-verbund.info/ead?ead.id=CH-002121-2-991170525759305501 는 `VadSlg Ms 34:60` 원고 PDF `https://han.stadtarchiv.ch/inhalt/VadSlg_Ms_34_60.pdf`를 제공한다. 1536-07-23 부처 편지와 **무관한 1541년 편지**이다.
- 다른 실제 예: https://kalliope-verbund.info/CH-002121-2-991170524626305501 는 `VadSlg Ms 35:114`에 대해 **원고 PDF**와 **편집본 PDF**를 별도로 연결한다.

이 예들은 **개별 원고·편집본의 공식 다운로드 체계가 실재한다**는 사실만 증명한다. 특정 1536-07-23 부처→바디안 서신의 현재 청구기호나 PDF를 확인했다는 뜻이 아니다.

## 4. 검색 미완료 및 재인용 상태 유지

대상: Martin Bucer → Joachim Vadian, 1536-07-23. 종전 인용: *Vadianische Briefsammlung* V p.339, 1937 WA Br 7 Nr.3048 편집 각주에서 재인용.

- 정확한 **현행 원고 청구기호**: 미확인.
- Kalliope 및 swisscollections의 **개별 카드 ID**: 미확인.
- 공식 `han.stadtarchiv.ch` **해당 편지 원고 PDF**: 미확인.
- *Vadianische Briefsammlung* V **인쇄 p.339 이미지·원어 본문**: 미확인.
- 1937년 각주의 `parate discedent` 문구: 이미지 교감 전 원어 철자·문법 확정 금지.

별도 주의: Kalliope에서 다른 날짜의 'Bucer→Vadian' 문서나 1533년 현대 Bucer 서신집을 찾았더라도 1536-07-23 편지로 오인·대체 금지.

## 5. 원전 독립성의 엄격한 판정

| 증거 | V3.73 현재 접근 | 사료 본문 직접 대조 |
|---|---|---|
| Brieffer→Rhenanus, 1536-07-21 | 1886년판 Nr.297 OCR (V3.72); BnF/Google Books 판본 재확인 | 편집 OCR YES, 인쇄 이미지 NO |
| Capito→Luther, 1536-07-20 | WA Br 7 Nr.3048 OCR (V3.70) | 편집 OCR YES, 인쇄 이미지 NO |
| Bucer→Vadian, 1536-07-23 | WA Br 7 편집자 재인용 및 1905판 서지 | 1905 독립 본문 NO |
| 원고 PDF 연결 체계 | 공식 기록보관소·Kalliope에서 확인 | **대상 서신 원고는 NO** |

**사료 갱신 없음:** 1536년 7월 14일 출발, 7월 20일 협의 진행, 7월 23일 출발 준비라는 기존 잠정 시간축은 유지하되 V3.73에서 새로운 직접 사본을 확인한 것처럼 증거 등급을 올리지 않는다.

## 6. V3.74 실행 가능한 권장작업

1. Kalliope의 `Vadianische Briefsammlung` **Bd.3(1530년대 해당 원고 묶음)** 내에서 작성자 `Bucer`, 수신자 `Vadian`, 날짜 `1536-07-23` 또는 `23 Julii` 조합으로 개별 목록을 찾는다. 묶음/권 번호는 실제 목록에서 날짜 범위를 다시 검증한 뒤에만 확정.
2. swisscollections 레코드의 **현재 Signatur**를 확보한 다음 해당 `han.stadtarchiv.ch` 원고·편집본 PDF를 직접 열어 원어를 검증한다.
3. 공개 인쇄판을 우선 확보할 경우 1905년 역사학회 29/2 분책 또는 합본의 **정확한 페이지 체계**에서 p.339의 원문을 대조한다.
4. Rhenanus 1886 인쇄 p.421–422는 BnF 또는 Google Books의 **실제 페이지 이미지**로 시각 대조한다. 링크 리다이렉트·표지 불일치가 있으면 즉시 제외한다.
5. 모두 확인되면 기존 V3.70~V3.72의 날짜 주장에 증거 출처를 직접 연결하고 513편 수정 제안은 전문가 검수 이후 별도 진행한다.

## 7. QA 및 배포 게이트

- PASS: 1886판 공공기관 서지·복수 디지털 소장본 경로 확인.
- PASS: 오연결 PDF를 1886판 교감 자료에서 배제.
- PASS: 성갈렌 서신 컬렉션의 현재 온라인 목록·개별 원고 및 편집본 디지털 배포 체계 확인.
- PENDING: 1886 p.421–422 육안 교감.
- PENDING: 1905 Vadian V p.339 직접 판독 및 1536-07-23 서신 원고 카드 식별.
- PENDING: 전문가 검토 및 본문 출판.
- **CAN_SHIP=false**.
