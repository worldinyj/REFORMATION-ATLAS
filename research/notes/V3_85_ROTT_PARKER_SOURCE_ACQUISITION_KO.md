# REFORMATION-ATLAS V3.85 — Rott(1978) / 재수록 판본 / Parker MS119 원전 확보

**작성:** 2026-11-16  
**연구 브랜치:** `research/atlas-v385-rott-reprint-parker-source-recovery`  
**단계:** RESEARCH_DRAFT. `main`, 513편 원고, AI Studio 웹앱 수정 없음.

## 1. 이번에 확인한 문헌상의 새 성과

### Rott 논문의 두 서지 경로

1. **1978 최초 게재본:** Jean Rott [= Hans-Georg Rott], 「Martin Bucer und die Schweiz: Drei unbekannte Briefe von Zwingli, Bucer und Vadian (1530, 1531, 1536)」, *Zwingliana* **14/9 (1978), 461–492쪽**. 특히 489쪽은 Rüsch(1983)의 인용이 지목한 위치.
   - 공식 학술지 아카이브는 `14/9 (1978)`을 수록: https://zwingliana.ch/issue/archive
   - **한계:** 실제 논문 PDF·489쪽 전사·각주를 직접 열지 못함.
2. **1986 재수록본:** Jean Rott, *Investigationes Historicae: Églises et société au XVIe siècle*, **제2권 203–234쪽**. Brill 제공 학술서지의 두 판본 동등 인용을 확인함.
   - https://brill.com/edcollchap/book/9789047414209/front-8.pdf
   - PDF 검색 텍스트 1344–1355행의 `ROTT, BUCER UND DIE SCHWEIZ`에 명시.
   - **중요:** 최초 게재본 489쪽을 단순 덧셈으로 재수록본 **231쪽**에 해당한다고 *추정*할 수 있지만, 재편집·표·쪽나눔 변경 가능성이 있으므로 **231쪽을 확정 출처로 인용 금지**.
   - Brill 서지 PDF의 스크린샷은 접속 403 오류로 실패. PDF 텍스트를 본 것이지 스크린샷 페이지를 대조한 것은 아님.

### 동일 저자·이름 혼동 해소

프랑스 국립도서관 BnF의 정식 저자 전거:
- **Rott, Jean (1911–1998)**, 전체 이름 **Jean Georges Gustave**.
- **Jean-Georges Rott**, **Hans-Georg Rott**는 동일인의 다른 표기.
- 링크: https://catalogue.bnf.fr/ark:/12148/cb11922721n
- ATLAS 엔터티 권장: `person:rott-jean-1911-1998`, 표준명 **Jean Rott**, 대체명에 나머지 표기를 저장. **서로 다른 역사학자로 분리하지 말 것**.

## 2. Parker MS119 — 원본 확보의 확인된 경로와 막힌 경로

**기준 서신:** 1536-08-04 Joachim Vadian → Martin Bucer, Cambridge Corpus Christi College, Parker Library **MS119, item 71**.

- 현대 Parker 목록(집계): https://iiif.biblissima.fr/collections/manifest/780facf6a47bf2addec17f9498ef58363cb4c8a0
- 페이지 검토 대상: **199, 200, 205, 206**. 카탈로그의 201–206 Farel 항목과 겹치는 부분은 실제 이미지의 페이지·서신 경계 검증 필요.
- Stanford 카탈로그 링크: https://parker.stanford.edu/parker/catalog/xs417vg0804
  - **결과:** 웹 접속 `Request Rejected`.
- IIIF manifest URL: https://dms-data.stanford.edu/data/manifests/Parker/xs417vg0804/manifest.json
  - **결과:** 직접 접근 불가. canvas 수, image service URL, 파일 해시 **확보하지 못함**.
- 공식 소장기관 안내: Corpus Christi College는 `Parker on the Web` 디지털 자료를 무료로 열람할 수 있다고 안내하며, **원고 이미지 문의처는 `parker-library@corpus.cam.ac.uk`**로 명시함.
  - https://www.corpus.cam.ac.uk/articles/parker-web
  - https://www.corpus.cam.ac.uk/parker-library/college-archives

**서지 변이:** James(1912)에서 `pridie Non. Aug. 1566`이 확인되고 현대 목록은 `pridie Nonas Augusti 1536`. 1536년을 **현대 카탈로그 기반 잠정 기준**으로 채택하지만, 원본 날짜를 판독하지 않았으므로 1566이 오기임을 필사본 수준에서 확정했다고 쓰면 안 됨.

## 3. 케임브리지 원고 이미지 및 날짜 확인 문의 초안 (영어 / 미발송)

**To:** parker-library@corpus.cam.ac.uk  
**Subject:** Scholarly enquiry — CCCC Parker MS 119, item 71 (Vadian to Bucer, 4 August 1536), manuscript pages and date

Dear Sub-Librarian,

I am preparing a source-critical research dataset on correspondence surrounding the Wittenberg Concord of 1536. I am trying to verify the manuscript evidence for a letter from Joachim Vadian to Martin Bucer in **Corpus Christi College, Parker Library MS 119, item 71**.

The modern manuscript catalogue identifies it as dated **4 August 1536** (*pridie Nonas Augusti 1536*), with text on **pp. 199–200** and a reported continuation on **pp. 205–206**. However, M. R. James's 1912 printed catalogue, volume I, p. 281, apparently reads **1566** for the year.

Could you please clarify:
1. Whether the year **1536** is legible on the manuscript itself, and whether **1566** in the James catalogue is an acknowledged typographical or transcription error;
2. Whether item 71 is an **autograph, contemporary copy, or later transcript**;
3. Whether there is a stable image or IIIF canvas link for **pp. 199–200 and 205–206**, and how the intervening Farel letter is physically arranged;
4. Whether a scholarly citation and small manuscript excerpt can be reproduced online, and under which conditions.

I have found the Parker digital catalogue entry (`xs417vg0804`), but the web interface and linked IIIF manifest were inaccessible from my current research environment. Any guidance on obtaining the relevant images for source comparison would be greatly appreciated.

With thanks and best regards,

[Name]  
REFORMATION-ATLAS research project

## 4. Zwingliana 편집부 문의 초안 (독일어 / 미발송)

**담당:** Zwingliana Redaktion — 공식 문의처 https://zwingliana.ch/about/contact  
**Betreff:** Forschungsanfrage: Rott, „Martin Bucer und die Schweiz“, Zwingliana 14/9 (1978), S. 489

Sehr geehrte Redaktion,

für ein quellenkritisches Forschungsprojekt zur Korrespondenz Joachim Vadians und Martin Bucers im Jahr 1536 benötige ich die **Originalveröffentlichung** von Jean (Hans-Georg) Rott:

*Martin Bucer und die Schweiz: Drei unbekannte Briefe von Zwingli, Bucer und Vadian (1530, 1531, 1536)*, **Zwingliana 14/9 (1978), S. 461–492**, besonders **S. 489**.

Die Ausgabe 14/9 ist im Online-Archiv aufgeführt, doch konnte ich den zugehörigen Volltext in meiner Forschungsumgebung nicht direkt öffnen. Eine Bibliographie weist außerdem auf den Wiederabdruck in **Rott, Investigationes Historicae, Bd. II (1986), S. 203–234** hin.

Könnten Sie mir bitte einen **stabilen PDF-Link oder die Artikelkennung** nennen? Falls die Originaldatei nicht verfügbar ist, wäre auch ein Hinweis auf die Seitenentsprechung bzw. eine digitale Ausgabe des Wiederabdrucks hilfreich.

Mit freundlichen Grüßen

[Name]  
REFORMATION-ATLAS Forschungsprojekt

## 5. 증거 게이트와 다음 조사

| 주장 | 이번 단계의 결론 |
|---|---|
| Rott의 Jean / Hans-Georg 표기 | **동일 저자, BnF 전거 확인** |
| 1978년 출처 14/9, 461–492쪽 | **서지 확인** |
| 1986년 재수록 II권 203–234쪽 | **서지 확인** |
| 1978년 489쪽 실제 본문 판독 | **미완료** |
| 재수록본 231쪽과 최초 489쪽의 동일성 | **검증되지 않은 쪽수 계산** |
| Parker MS119 날짜 행 직접 판독 | **미완료** |
| 원본/사본 판별 | **미완료** |
| 1536.7.23과 7.25의 동일성 | **미해결** |

다음 단계 V3.86은 **실제로 확보된 이미지/논문 원문의 정밀 대조**를 우선하며, 기관 문의문은 사용자의 명시적인 발송 지시가 있기 전까지 미발송 상태로 둔다.

**릴리스 상태:** `can_ship=false` / `main` 및 웹앱 미수정.
