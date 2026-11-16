# 종교개혁 ATLAS — V3.84 원전 교감 기록
## Cambridge Parker Library MS 119, item 71: 바디안→부처 서신의 1536/1566 판본 충돌

**기준일:** 2026-11-16  
**브랜치:** `research/atlas-v384-parker-ms119-catalog-date-collation`  
**상태:** RESEARCH_DRAFT / NOT PUBLISHED

### 1. 신규 확인 — 1912년 인쇄 목록 자체에 연도 오류가 존재할 가능성

케임브리지 Corpus Christi College 소장 필사본 MS 119의 **제71항목**에 있는 바디안(Joachim Vadian)→부처(Martin Bucer) 서신의 날짜가 아래와 같이 다르다.

| 출처 | 표기 | 현대 날짜 | 실제 검증한 것 |
|---|---|---|---|
| M. R. James, *A Descriptive Catalogue of the Manuscripts in the Library of Corpus Christi College, Cambridge*, Vol. I (1912), **인쇄 p.281, MS119 item 71** | **`data pridie Non. Aug. 1566`** | 1566-08-04 | 인쇄본 PDF 검색 텍스트 (실제 PDF 페이지 이미지 미검토) |
| Parker Library / Biblissima MS119 현대 목록 | **`data pridie Nonas Augusti 1536`** | **1536-08-04** | 소장목록 본문 (실제 필사본 이미지 미검토) |
| E. G. Rüsch, 「Um das Abendmahl」 (1983) | **1536년 8월 4일** Vadian→Bucer, *Zwingliana* XIV, p.489 참조 | 1536-08-04 | 학술 논문 검색 가능 본문의 각주 (PDF 인쇄면 이미지 미검토) |

1912년 항목에는 명백히 `1566`이라는 연도가 적혀 있다. 그러나 부처는 **1551년 2월 28일** 사망했고(프랑스 국립도서관 BnF 인명 전거), 현대 Parker 목록 및 1983년 연구는 **1536년**으로 일치한다.

따라서 이번 연구의 보수적 판정은:
- **`PROBABLE_1912_CATALOG_TYPO`** — 1912년 목록의 **1566**은 **1536**의 오기일 가능성이 매우 높음.
- **`HIGH_CONFIDENCE_CATALOG_COLLATION_NOT_PRIMARY_DATE_READING`** — 아직 실제 16세기 필사본의 날짜 행을 확인하지 못했으므로 '원고에 1536년이라고 적혀 있음'으로 표현하지 않음.
- 1912년의 표기는 후속 교감 연구를 위해 **원형 그대로 별도 기록**할 것.

검증 출처:
1. James (1912), p.281, item 71: https://www.corpus.cam.ac.uk/sites/default/files/downloads/m.r._james_cccc_catalogue_1912_vol._i.pdf
2. 현대 Parker/Biblissima MS119: https://iiif.biblissima.fr/collections/manifest/780facf6a47bf2addec17f9498ef58363cb4c8a0
3. Rüsch (1983), *Theologische Zeitschrift* 39: https://www.e-periodica.ch/cntmng?pid=thz-001%3A1983%3A39%3A%3A470
4. 부처의 사망일 BnF 전거: https://catalogue.bnf.fr/ark:/12148/cb11929851j

### 2. 라틴어 원문 표기의 해석

- `pridie Nonas Augusti`: **8월의 노네스(Nonae)**는 8월 5일; `pridie`는 하루 전날이므로 **8월 4일**을 의미한다.
- 따라서 **연도의 충돌(1566↔1536)**과 **월일(8월 4일)**은 별도 항목으로 관리한다. 월일 자체는 일치한다.
- 주목: 바디안의 8월 4일 서신이 부처의 7월 25일 서신에 대한 답신인지는 **아직 확증하지 못함**. 두 서신은 발신 방향이 반대여도 자동적인 답신 관계를 추론하지 말 것.

### 3. Cambridge MS119에서 확인할 정확한 위치

| 항목 | 위치 | 출처 |
|---|---|---|
| Parker MS119, **제71서신** | **pp.199–200** | James(1912) p.281 및 Parker 현대 목록 |
| 제71서신의 연속 부분 | **pp.205–206** | 현대 Parker 목록의 전승 설명 |
| 중간 부분 pp.201–204 | **Guillaume Farel→Bucer (1550년)** 편지 | 현대 Parker 목록 |

이 구조 때문에 MS119 전체를 한 번에 페이지 199–206으로 묶어 '바디안 편지 8쪽'이라고 기술하면 안 된다. **제71서신의 앞부분과 이어지는 뒷부분은 비연속 위치**에 있다. 201–204쪽은 다른 서신이다.

M. R. James는 MS119 전체를 `Codex chartaceus in folio, seculo xvi scriptus`로 설명했다. 그러나 해당 **제71항목**을 친필 원본(`autograph`)이라고 명시하지는 않았다. 반면 다른 항목에는 원본/사본 표기가 따로 있는 경우가 있다. '원본 미표기 = 필사본으로 확정'도 아니다. **원본/사본 상태는 계속 UNRESOLVED**.

### 4. 1978년 Rott 연구의 원문 확보 시도

- 서명: Rott, *Martin Bucer und die Schweiz: drei unbekannte Briefe von Zwingli, Bucer und Vadian (1530, 1531, 1536)*.
- 서지: *Zwingliana* 14 (1978), pp.461–492; 1983년 Rüsch가 **p.489**를 참조.
- 공식 온라인 아카이브: https://www.irg.uzh.ch/de/publikationen/zwingli/zwingliana-online.html
- *Zwingliana* 편집 플랫폼 아카이브: https://zwingliana.ch/issue/archive
- 확인 범위: 학술지 아카이브와 논문 서지/수록 면수.
- **미완료**: Rott 논문 PDF 본문·p.489 이미지·실제 라틴어 전사와 비평주.
- 1983년 논문에 인용된 `Est mihi res cum solis atque unicis papistis` 구절은 **Rüsch의 1983년 학술 인용 경유**로 표시하고, Rott 1978 원문을 직접 본 것처럼 표기하지 않는다.

### 5. 디지털 원고 사본 접근 실패 기록

- Parker 목록 링크: https://parker.stanford.edu/parker/catalog/xs417vg0804
  - 접근 결과: 보안/요청 거절 페이지 노출.
- IIIF manifest: https://dms-data.stanford.edu/data/manifests/Parker/xs417vg0804/manifest.json
  - 접근 결과: 웹 도구에서 직접 읽기 불가. **manifest 내용이나 원고 이미지를 확인한 것으로 기재 금지**.
- James(1912) 대용량 PDF는 검색 텍스트를 확보했지만, 웹 PDF 스크린샷 시도는 파일 크기 제한(약 32MB)으로 실패함.
- **특정 원고 이미지 권리:** Biblissima는 Parker 이미지에 CC BY-NC 4.0 안내를 제공하나, 학술·상업 출판의 고해상도 이용은 Parker Library와 직접 확인이 필요하다. 현 단계에서는 원고 이미지 자체를 프로젝트에 저장하지 않는다.

### 6. 1536년 여름 서신 연구에 미치는 영향

기존 V3.83의 서신 연결은 그대로 보존하되 아래와 같이 강화한다.

1. **1536-07-23 부처→바디안:** 원고 미확인, 날짜 및 `Vadian BW V p.339` 인쇄본 직접 미확인. **BLOCKED**.
2. **1536-07-25 부처→바디안:** 취리히 중앙도서관 `Ms S 41, Nr.33`, 올바른 Kalliope ID `CH-002121-2-991170608445805501`. **RESEARCH_ONLY**.
3. **1536-08-04 바디안→부처:** Cambridge MS119 제71서신, 현재 현대 목록 날짜 1536이 우세하나 **1912년 목록의 1566 오기를 반드시 표기**. **RESEARCH_ONLY**.
4. **1536-08-06 불링거→바디안:** HBBW 875, `Vadian BW V pp.341–343`, 비평판 확인. **출처 명시 해설만 가능**.

### 7. V3.85 실제 다음 작업

1. **Parker Library MS119 제71서신**에 대하여 pp.199–200, pp.205–206 사진/IIIF 사본을 확보하고 날짜 행의 숫자를 직접 읽기.
2. **Rott(1978) p.489**의 라틴어 본문·편집주를 직접 확인하여 MS119와 같은 텍스트 계통인지 확인.
3. **1536년 7월 23일 / 25일**은 별도 원전 확보 없이는 여전히 병합 금지.
4. 소장기관 문의용 문안은 기존 V3.78/V3.82 초안에서 참조할 수 있으나 **실제 메일은 발송하지 않았음**.

**릴리스 게이트:** `can_ship=false`. main/513편 원고/AI Studio 웹앱 변경 없음.
