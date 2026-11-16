# REFORMATION-ATLAS V3.87 — Rott(1978) 원전 PDF 확보 경로 자동화

**기준일:** 2026-11-16  
**기반:** V3.86, \`research/atlas-v386-rott-page-citation-and-1536-theology-map\`  
**연구 브랜치:** \`research/atlas-v387-rott-ojs-pdf-discovery\`  
**검증 상태:** RESEARCH_DRAFT. 웹앱·main·513편 역사 원고 미변경. 원전 이미지를 확보하지 못했으며 이메일도 발송하지 않음.

## 1. 확인한 사실과 한계

- 『Zwingliana』의 **공식 아카이브**에서 **14/9 (1978)** 발행호가 보인다.
  - https://zwingliana.ch/issue/archive
- 취리히대 종교개혁사 연구소는 『Zwingliana』의 디지털 전문 자료 제공을 소개한다.
  - https://www.irg.uzh.ch/de/publikationen/zwingli/zwingliana-online.html
- Jean Rott [= Hans-Georg Rott], **「Martin Bucer und die Schweiz: drei unbekannte Briefe von Zwingli, Bucer und Vadian (1530, 1531, 1536)」**, *Zwingliana* **14/9 (1978), pp.461–492**. **대조 우선 인쇄면은 p.489와 p.491**.
- 재수록본: Rott, *Investigationes Historicae* II (1986), **pp.203–234**. 원문 인쇄면의 정확한 대응 쪽수는 검증되지 않았다.
  - https://brill.com/edcollchap/book/9789047414209/front-8.pdf
- V3.86에서 Rüsch(1983)의 **해당 489·491쪽에 대한 2차 인용**은 확인했으나, **Rott(1978) 자체의 PDF·489쪽·491쪽은 아직 확보하지 못했다**.
- 현재 검색 도구에서는 아카이브의 "14/9 (1978)" **표시만 확인**되었고, 인접한 논문 상세 링크나 다운로드 링크는 표면화되지 않았다.
- 로컬 실행 환경에서는 \`zwingliana.ch\` 도메인의 DNS 조회가 실패했고, 별도의 다운로드 시도도 실패했다. 이는 자료가 실제로 비공개라는 증거가 아니다.

## 2. 이번에 추가한 도구

파일: \`research/scripts/resolve_v387_zwingliana_rott.py\`  
요구사항: Python 3.8 이상, 표준 라이브러리만 사용, 외부 패키지 불필요.

### 사용 순서

저장소 루트에서:

\`\`\`bash
python3 research/scripts/resolve_v387_zwingliana_rott.py --self-test
python3 research/scripts/resolve_v387_zwingliana_rott.py
\`\`\`

두 번째 명령은 **조회만** 한다. 공식 아카이브 → 14/9 (1978) 발행호 → Rott 논문 상세 페이지 → PDF galley 링크의 순서로 확인한다. 발행호/논문/PDF 후보가 0개 또는 중복되면 임의의 ID를 추정하지 않고 **실패 처리**한다.

**PDF 원문을 로컬 임시 영역에 확보할 때에만** 다음을 명시적으로 실행:

\`\`\`bash
python3 research/scripts/resolve_v387_zwingliana_rott.py --download --out-dir /tmp/reformation-atlas-sources
\`\`\`

동작 조건:
1. 출처 링크는 HTTPS 및 공식 도메인으로 제한한다.
2. 다운로드 파일에 \`%PDF-\` 서명이 있는지 확인한다.
3. 최대 20 MiB 용량 제한을 두고, 이미 존재하는 파일은 덮어쓰지 않는다.
4. SHA-256, 파일 크기, 실제 링크 및 취득 상태를 보고한다.
5. **GitHub 저장소에는 PDF 원본을 커밋하지 않는다.**

실제 PDF를 획득한 후에도 **printed p.489/p.491의 PDF 페이지 인덱스는 자동으로 추정하지 않는다**. 반드시 인쇄 쪽수와 화면상의 실제 쪽을 대조해야 한다. PDF 시각 교감에는 웹 PDF 스크린샷을 확인하고, 라틴어 원문은 직접 인쇄면에 근거해 전사한다.

### 테스트 범위 명시

- 로컬에서 동일한 HTML 선택 로직의 **모의 페이지 검사 7개를 수행해 PASS**하였다.
- **GitHub에 저장된 파일을 새로 내려받아 동일 환경에서 실행한 것은 아직 아니다.**
- 실제 인터넷을 통해 OJS 웹사이트를 순회한 성공 사례 **0건**.
- Rott 논문 PDF 수집 **0건** / 489·491쪽 직접 판독 **0쪽**.

## 3. 검증 상태표

| 자료 | 이번 버전 | 다음 조건 |
|---|---|---|
| 공식 아카이브 14/9 (1978) 항목 | 확인 | 실제 발행호 URL 획득 |
| Rott 개별 논문 ID | 미확정 | 공식 상세 페이지에서 판독 |
| Rott PDF galley URL | 미확정 | 공식 다운로드 링크 획득 |
| Rott p.489 | 미판독 | PDF 인쇄면 이미지 직접 대조 |
| Rott p.491 | 미판독 | PDF 인쇄면 이미지 직접 대조 |
| 1986년 재수록 쪽수 대응 | 미확정 | 실제 두 판본 대조 |
| Parker MS119 1536-08-04 | 목록 확인 | 실제 필사본 이미지 판독 |
| Bucer→Vadian 1536-07-23/25 동일성 | 미확정 | 원고/1905년 인쇄판 직접 대조 |

## 4. 실질적인 다음 작업 — V3.88

1. 공식 사이트를 사용할 수 있는 네트워크 환경에서 **도구를 직접 실행**하여 개별 issue/article/galley 주소를 확보한다.
2. 원문 PDF가 확보되면 **489·491쪽의 본문과 주석을 실제 화면에서 대조**하고 필요한 짧은 라틴어만 전사한다.
3. Parker MS119의 원고 이미지를 함께 검토해 Rott가 사용한 텍스트 계통, 날짜, 원고·사본 상태를 추적한다.
4. **Rott 원문을 직접 확인하지 못했다는 상태는 풀지 않는다.** 1536-07-23/25 동일성도 여전히 보류한다.

**배포 승인:** \`can_ship=false\`. 인터넷·기관 접근이 어려운 현재 환경에서 실제 원문을 확보하지 못한 점을 명시적으로 기록하였다.
