# 종교개혁 ATLAS V3.69 — WA Br 7 디지털 진입점 및 제3048호 인쇄면 접근 감사

**기준일**: 2026-11-11
**계승**: research/atlas-v368-wabr7-scan-access-gate
**작업 브랜치**: research/atlas-v369-wabr7-digital-entrypoint-audit
**상태**: RESEARCH_ONLY / DRAFT / NOT_APPROVED / CAN_SHIP=false

## 연구 질문
1536년 7월 20일 Wolfgang Capito → Martin Luther 서신의 원어 편집본(*D. Martin Luthers Werke*, Briefwechsel Bd. 7, 1937, Nr.3048, pp.466–468)을 직접 판독할 수 있는 정확한 스캔 파일·페이지 URL을 확정할 수 있는가?

## 확인된 외부 접근 경로 (2026-11-11)

| 자원 | URL | 확인 수준 |
|---|---|---|
| 독일어 Wikisource / Martin Luther / Briefwechsel (WA BR) | https://de.wikisource.org/wiki/Martin_Luther | Bd.7 (1937)와 1969 복각판에 대한 Internet Archive 링크 목록이 존재함: LINK_DIRECTORY_ONLY |
| Lutherdansk / Weimarer Ausgabe / Abteilung 4 Briefwechsel | https://www.lutherdansk.dk/WA/D.%20Martin%20Luthers%20Werke,%20Weimarer%20Ausgabe%20-%20WA.htm | Bd.7 = Briefe 1534–1536, PDF와 flipbook 항목 표시: LINK_DIRECTORY_ONLY |
| SLUB Dresden catalog | https://katalog.slub-dresden.de/id/0-1072308576 | 1937 원판, 1969 복각, 2002 판본의 서지적 차이 확인: BIBLIOGRAPHIC_ONLY |
| Marburg digital repository search result | https://archiv.ub.uni-marburg.de/eb/2020/0500 | Bd.5의 기관 디지털 복제본 존재 확인. 이는 *Bd.7 사본이 존재한다는 증거가 아님*: OTHER_VOLUME_ONLY |
| 2015 Capito Correspondence vol.3 | https://tile.loc.gov/storage-services/master/gdc/gdcebookspublic/20/20/71/95/37/2020719537/2020719537.pdf | V3.66에서 확인한 Ep.619의 WA Br 7 pp.466–468 Nr.3048 출전 정보. 원어 본문 아님: DERIVED_BIBLIOGRAPHY |

## 실패 및 미검증 기록

- Internet Archive의 **정확한 item identifier**: NOT_VERIFIED.
- 해당 아이템의 PDF/JP2/페이지별 캔버스 URL: NOT_VERIFIED.
- 인쇄 p.466, 467, 468에 해당하는 스캔 프레임 번호: NOT_VERIFIED.
- 1937년 원판 목표 지면의 고해상도 시각 검수: NOT_DONE.
- 1536년 7월 20일 편지의 실제 라틴어/독일어 문장 및 편집 각주 전사: NOT_DONE.
- HBBW 제866호와의 원문 문장별 비교: NOT_DONE.

**핵심 판정**: 디지털 링크를 포함하는 웹 목록의 존재를 확인한 성과를, 스캔 원문 자체를 확보한 성과로 승격하지 않는다. 제3048호의 내용은 기존 V3.66의 현대 편집 요약을 넘어 확장하지 않는다.

## 사료 ID 및 중복 방지

- `WA_BR:7:3048` = 1937 Briefwechsel 제7권, 인쇄 466–468쪽, Capito→Luther, 1536-07-20.
- `CAPITO_CORRESPONDENCE:3:619` = 2015년판 제619호, WA Br 7 Nr.3048을 참고한 현대 편집 요약.
- `HBBW:6:866` = Myconius→Bullinger/Bibliander/Pellikan, 1536-07-19. 본문 미검수.
- 다른 서신편집 프로젝트에서 같은 숫자 3048이 사용되어도 동일 문서로 병합하지 않는다.
- 디지털 복각본 1969년판과 1937년 원판을 별도 물리적 인쇄 간행물/디지털 사본으로 관리한다.

## 다음 조치 (V3.70)

1. Lutherdansk에서 Briefwechsel Bd.7 PDF 항목의 *실제 링크 목적지*를 기록하거나 Wikisource Bd.7 1937 Internet Archive 링크의 ID를 확보.
2. 실제 복제본의 발행정보·표지·인쇄 페이지 466의 위치를 확인한 뒤 466–468쪽을 시각 검수.
3. Nr.3048과 발신/수신/날짜를 검증하고 편집 원어의 문장 및 각주를 보존 가능한 범위에서 전사.
4. 2015 Ep.619의 현대 해설을 원어의 문장과 대조. 각 문장에 DIRECT_PRINT, MODERN_SUMMARY, INTERPRETATION을 분리 태깅.
5. HBBW 866 원전 확보와 1536년 7월 19~20일 연대 비교를 그다음 진행.
6. 만약 접근 제한이 유지된다면 독일 기관 열람신청 또는 허용 범위의 학술 복제 서비스로 전환하되 본문을 추측해 채우지 않는다.

## 안전한 수정 범위
이번 브랜치에는 이 연구 문서만 추가한다. `main`, 기존 513편 원고, 웹앱, 사본 원본, V3.60–V3.68 문서 불변. 모든 공개 승인 게이트 보류.
