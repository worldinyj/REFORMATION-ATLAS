# 종교개혁 ATLAS — V3.89 Rott(1978) 과거 개별 논문 경로 복구 기록

**연구 기준일:** 2026-11-16  
**브랜치:** `research/atlas-v389-rott-legacy-permalink-provenance`  
**연구 상태:** RESEARCH_DRAFT / 원전 대조 미완료  
**상위 버전:** V3.88 (`research/atlas-v388-source-acquisition-runtime-audit`)

## 1. 이번에 처음 확보한 구체적 개별 논문 주소

2026년 8월 종교개혁사 블로그 *Zwinglius Redivivus*의 「De convitiis Eckii: Zwingli Drops the Hammer on Johannes Eck」에서, 1978년 Hans Georg/Jean Rott의 해당 논문으로 연결하는 **실제 외부 링크**를 발견했다.

- 원문 링크를 제공한 외부 페이지: https://zwingliusredivivus.wordpress.com/category/zwingliana/
- 링크 텍스트: *Martin Brucer und die Schweiz: Drei unbekannte Briefe von Zwingli, Brucer und Vadian (1530, 1531, 1536)*. 이 외부 게시물에는 `Brucer`라는 철자 오기가 있음. 정식 학술지 서명은 `Bucer`임.
- **실제로 연결된 구 주소:** https://www.zwingliana.ch/index.php/zwa/article/view/910/820
- URL 경로에서 식별 가능한 숫자: **910**과 **820**.
- 블로그 글을 통해 **문헌의 개별 기록을 가리키는 역사적 OJS 주소가 존재했다는 사실**을 확인했다.
- 그러나 해당 링크를 실제 열어보니 **404 Not Found**로 응답한다. 이 원인(웹사이트 이전, 누락, 서버 라우팅 변경 등)은 직접 확인되지 않았다.
- `910`은 URL 경로의 과거 논문 ID 후보이며 `820`은 두 번째 경로 구성요소다. 후자를 현대식 PDF galley ID로 단정하지 않는다.
- 공식 학술지의 **새 논문 URL, 실제 PDF galley, 파일 해시**는 여전히 미확정.

**핵심:** 구 주소가 발견되었다는 사실을 **실제 PDF를 읽었다는 사실**로 처리하지 않는다.

## 2. 교차 검증을 위한 보존 자료

| 구분 | 출처 | 확인 내용 |
|---|---|---|
| 과거 개별 링크 출처 | *Zwinglius Redivivus*, 2026년 8월 게시물 | (910/820) 링크의 앵커와 논문 지시 |
| 공식 학술지 발행호 목록 | https://zwingliana.ch/issue/archive | 14/9 (1978) 발행호의 존재 |
| 학술 서지 | https://brill.com/edcollchap/book/9789047414209/front-8.pdf | Rott(1978), 『Zwingliana』 14권 461–492쪽, 1986년 재수록 203–234쪽 |
| 1983년 학술 인용 | https://www.e-periodica.ch/cntmng?pid=thz-001%3A1983%3A39%3A%3A470 | 원본 Rott의 489·491쪽이 인용되는 구체적 연구 맥락 |

**등급 분리:** 블로그의 링크는 논문 원문이 아니라 제3자의 과거 경로 인용이다. 현재 404가 발생해 PDF가 확보되지 않았고, 1978년 489·491쪽도 직접 판독하지 못했다.

## 3. 확인한 접근 실패와 금지사항

1. `www.zwingliana.ch/index.php/zwa/article/view/910/820` → **HTTP 404**, 본문 불가.
2. 경로 구조를 현대 `/article/view/910` 또는 `/article/download/910/820`로 바꾸어 접근 시도했으나, **접근 가능한 논문 본문을 얻지 못함**.
3. 현재 사이트의 발행호 14/9 목록은 조회 가능하지만, 웹 도구에 정확한 논문 상세 링크가 노출되지 않았다.
4. Internet Archive/Wayback 공개 URL 접근 시도도 **이 환경에서 성공하지 못함**.
5. 같은 경로 숫자가 다른 학술지에도 나타날 수 있으므로, **도메인과 실제 링크 출처를 함께 검증**해야 한다.
6. 예전에 확인한 2005년 별도 논문의 PDF 다운로드가 작동한다는 사실은 **Rott PDF를 특정한 증거가 아니다**.

## 4. 품질 검증 도구

`research/scripts/validate_v389_legacy_permalink.py`:

- 구 URL의 **HTTPS, 공식 도메인, 정확한 경로**를 검증.
- `910`/ `820`을 정확하게 분리하되, 후자의 의미를 **UNKNOWN_FROM_LINK_ALONE**으로 유지.
- 현재 404와 공식 새 URL 미확보 상태를 그대로 보존.
- 미검증 `PDF` 및 원문 이미지 확인 플래그를 TRUE로 바꾸면 오류 처리.
- 취리히 원고의 **정정 청구 목록 ID** `CH-002121-2-991170608445805501`을 보존.
- 1536년 7월 23일/25일 서신의 동일성 미해결 및 `can_ship=false` 유지.

**시험:** 동일 내용의 Python 스크립트를 로컬 컨테이너에서 합성 JSON으로 시험했으며, 정상 데이터 점검과 **6가지 오류 주입 테스트**가 통과했다. GitHub의 저장된 데이터에 대한 재조회 검증은 별도로 수행한다.

## 5. 공식 학술지에 보낼 링크 이전 문의 초안 — 독일어 (미발송)

**Betreff:** Alter OJS-Permalink zu Rott (1978), Zwingliana 14/9, S. 461–492 — aktuelle PDF-Adresse

Sehr geehrte Redaktion,

für das Forschungsprojekt REFORMATION-ATLAS suche ich den digitalen Volltext des Aufsatzes von Jean (Hans-Georg) Rott, **„Martin Bucer und die Schweiz: Drei unbekannte Briefe von Zwingli, Bucer und Vadian (1530, 1531, 1536)“**, *Zwingliana* 14/9 (1978), S. 461–492.

In einem älteren externen Literaturhinweis habe ich den folgenden OJS-Permalink gefunden:

**https://www.zwingliana.ch/index.php/zwa/article/view/910/820**

Der Link führt derzeit zu einer 404-Seite. Dürfte ich Sie um den **gültigen aktuellen Artikel-Link, die PDF-Galley-URL oder einen dauerhaften Identifikator** bitten? Besonders relevant sind für unsere Quellenprüfung die Druckseiten **489 und 491**.

Eine spätere bibliographische Angabe verweist zudem auf den Wiederabdruck in Rott, *Investigationes Historicae*, Bd. II (1986), S. 203–234. Falls die Erstveröffentlichung nicht direkt erreichbar ist, wäre auch ein Verweis auf die archivierte Datei oder den Wiederabdruck hilfreich.

Vielen Dank für Ihre Hilfe und freundliche Grüße

[Name]  
REFORMATION-ATLAS Forschungsprojekt

**발송하지 않음.** 공식 도메인의 현재 담당 이메일을 새로 추정하지 않고 공개 연락 양식을 통해 전달할 수 있도록 초안만 보존.

## 6. V3.90의 가장 효과적인 다음 단계

1. 출판사 OJS **구 주소 `910/820`을 근거로 이전된 정식 논문 주소**를 확인한다. 기존처럼 광범위한 제목 검색을 반복하지 않는다.
2. **Rott PDF 실제 파일**을 확보해 PDF 서명, 해시, 인쇄 489·491쪽을 직접 검사한다.
3. Parker MS119의 199–200쪽 및 205–206쪽 이미지에서 날짜 행과 출전 관례를 별도로 대조한다.
4. 1536년 부처→바디안 서신의 **7월 23일/25일 동일성은 별도 증거 없이는 계속 보류**한다.

**릴리스:** `can_ship=false`. 기존 513편 원고와 `main`·AI Studio 웹앱은 변경하지 않았다.
