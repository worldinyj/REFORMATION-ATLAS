# REFORMATION-ATLAS V3.88 — Rott(1978) 원문 취득 실증 및 PDF 쪽수 검사

- 기준일: 2026-11-16
- 브랜치: `research/atlas-v388-source-acquisition-runtime-audit`
- 상태: **RESEARCH_DRAFT** (`can_ship=false`)
- 기반: V3.87. 본문 513편, `main`, Google AI Studio 웹앱은 변경하지 않음.

## 1. 연구 목표

Jean/Hans-Georg Rott, 「Martin Bucer und die Schweiz: drei unbekannte Briefe von Zwingli, Bucer und Vadian (1530, 1531, 1536)」, *Zwingliana* 14/9 (1978), pp.461–492.

**직접 확인할 인쇄면:** p.489와 p.491. 1983년 Rüsch 논문의 주석에 이 인쇄면이 지목되지만, **Rott(1978)의 원문 이미지**는 아직 읽지 못했다.

## 2. 온라인 경로 검증 — 성공한 것과 실패한 것

1. **학술지 공식 아카이브**: https://zwingliana.ch/issue/archive  
   1978년 `14/9 (1978)` 항목을 목록에서 확인했다. 그러나 웹 검색 환경에 표시된 목록에는 개별 **해당 호의 링크 및 논문 상세 ID**가 노출되지 않았다.
2. **학술지의 실제 PDF URL 형식**: https://zwingliana.ch/article/download/8155/6686  
   이 자료는 2005년 *Zwingliana* XXXII의 **다른 서평 PDF**이다. 웹 PDF 도구로 열고 첫 페이지의 **인쇄 쪽수 181을 이미지로 대조했다**.  
   **중요:** 이 URL은 실재하는 공식 다운로드 방식의 **작동 확인 사례**일 뿐 Rott 논문의 PDF가 아니다.
3. **Rott 1978 전용 article/download URL**: **여전히 미확인.** 주변 숫자를 조합하거나 다른 연도의 문서를 Rott 원본이라고 바꾸지 않았다.
4. **컨테이너 실제 HTTPS 접속**: `https://zwingliana.ch/issue/archive`에 Python `urllib`로 접속했으나  
   `[Errno -3] Temporary failure in name resolution`으로 실패. 별도 컨테이너 다운로드도 실패했다. 즉, **사이트가 비공개라는 뜻이 아니라 현재 로컬 런타임의 네트워크 접근 제약**이다.

## 3. V3.88 실행 도구와 검증 내역

실제 시험한 로컬 Python 파일: `resolve_and_verify_rott_v388.py`.

- 로컬 스크립트 SHA-256: `f1926788983421ca03e6e720a2bd3921efcb5d51f9c1d07214d1b5f6df9fa2fb`
- 스크립트는 Python 표준 라이브러리로 OJS **공식 발행호 → 정확한 논문 제목 → PDF galley 또는 citation_pdf_url**을 탐색한다.
- HTTPS 및 `zwingliana.ch` 도메인만 허용하며, 의도치 않은 리디렉션과 중복·모호한 링크를 거절한다.
- `--download`를 명시한 경우에만 PDF 파일을 저장하고, `%PDF-` 파일 시그니처/용량 제한/SHA256을 기록하며 파일 덮어쓰기를 거절한다.
- `--inspect-pdf /path/to/file.pdf`은 PyMuPDF가 설치되어 있을 때 **실제 인쇄 쪽수 489·491을 표시한 것으로 보이는 PDF 페이지 인덱스만 후보로 추출**한다. 이 기능은 원본 이미지 판독을 **대체하지 않는다**.

### 실제 실행한 시험

- `--self-test`: **PASS**, 모의 HTML 9개 검증(다른 호, 다른 논문, 다른 도메인, 중복 PDF 링크 등에 대한 차단 포함).
- `--discover`: **FAILED**, 외부 DNS 접근 실패. 실제 발행호/논문/PDF ID 모두 미확보.
- **합성 시험 PDF**: 독립적으로 생성한 5페이지 문서(각각 가상의 인쇄 쪽수 487–491). `--inspect-pdf`로
  - 인쇄면 489 → PDF **0부터 시작하는 인덱스 2**
  - 인쇄면 491 → PDF **0부터 시작하는 인덱스 4**
  가 출력됐다.
- 합성 시험 PDF는 **Rott 원문이 아닌 가짜 테스트 데이터**이며, 489와 491은 페이지 매핑 로직의 검사에만 사용했다.
- 시험 PDF의 489 페이지를 별도 PNG로 렌더링해 육안으로 **시험용 인쇄 쪽수 표시가 맞는지 확인**했다. **원문 Rott p.489를 확인한 것은 아님**.

**정직한 경계:** 로컬에서 시험한 V3.88 전체 스크립트는 이 연구 브랜치의 JSON에 **파일명·SHA256·실행 결과로 추적**되며, GitHub에 구현 전체를 업로드한 것으로 주장하지 않는다. V3.87의 공개 GitHub 원전 검색 스크립트는 이미 연구 브랜치에서 계승됐다.

## 4. 사료의 증거 등급

| 자료 | 판독 상태 | 공개 적합성 |
|---|---|---|
| 공식 발행호 14/9, 1978 | 목록만 확인 | 서지 정보로만 |
| 2005년 별도 PDF | 첫 페이지 이미지 확인 | **Rott의 근거로 사용 불가** |
| 1978년 Rott PDF | 파일 URL·본문 모두 미확보 | **BLOCKED** |
| Rott 인쇄 p.489 | 원문 이미지 미확인 | **BLOCKED** |
| Rott 인쇄 p.491 | 원문 이미지 미확인 | **BLOCKED** |
| Cambridge Parker MS 119 | 목록 수준, 원고 이미지 미판독 | **RESEARCH_ONLY** |
| 7월 23일·25일 부처 서신의 동일성 | 증거 부족 | **BLOCKED** |

기존 취리히 **정정 Kalliope ID** `CH-002121-2-991170608445805501`을 유지한다. 오류였던 ID를 본문 후보로 다시 사용하지 않는다.

## 5. 다음 권장 작업 — V3.89

**가장 짧은 실증 경로:** 해당 논문의 **정확한 아카이브 개별 PDF 링크**를 기관·학술 검색 서비스에서 확인하는 것. 새로 생성한 로컬 도구는 네트워크가 가능한 환경에서 이 경로의 확인과 파일 해시 기록에 사용할 수 있다.

PDF를 실제 입수한 다음에는 (1) PDF 전체 페이지 수 확인, (2) 인쇄 p.489·491의 **실제 PDF 인덱스** 확인, (3) 화면 이미지 검증 및 원문·편집주 제한적 전사, (4) Cambridge MS119와 출처 계보의 독립 대조 순서로 진행한다.

*PDF 직접 취득 0건. 학술기관 발송 0건. 공개 원고 변경 0건.*
