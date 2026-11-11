# 종교개혁 ATLAS V3.68 — WA Br 7 제3048호 디지털 원판 접근 게이트

**기준일:** 2026-11-11  
**부모:** `research/atlas-v367-wabr3048-source-identity-gate`  
**현재:** `research/atlas-v368-wabr7-scan-access-gate`  
**상태:** RESEARCH_ONLY / DRAFT / NOT_APPROVED / CAN_SHIP=false

## 1. 연구 질문

1536년 7월 20일 Wolfgang Capito → Martin Luther 서신을 수록한 *D. Martin Luthers Werke*, Briefwechsel Bd.7 (Weimar 1937), Nr.3048, pp.466–468의 **실제 인쇄 지면**을 확보·판독할 수 있는가? 본문을 판독하지 않은 상태에서 내용이나 서신 간 인과관계를 확정하지 않는다.

## 2. 이번 회차의 확인 자료

| 출처 | 확인된 범위 | 증거등급 |
|---|---|---|
| SLUB Dresden 서지목록 https://katalog.slub-dresden.de/id/0-1072308576 | WA Briefwechsel Bd.7의 1937년 원판과 1969년 복각, 2002년 판본 구분 | BIBLIOGRAPHIC_RECORD |
| 독일어 Wikisource 마르틴 루터 페이지 https://de.wikisource.org/wiki/Martin_Luther | WA BR Bd.7 (1937)와 복각판 (1969)의 Internet Archive 연결 목록 | DIGITIZATION_LINK_DIRECTORY |
| 2015 카피토 서신집 (V3.66에서 본문 p.455 검수) | Capito III Ep.619의 참조 원천 `WA Br 7:466–468, Nr.3048` | DERIVED_EDITORIAL_LOCATOR |
| 온라인 2015 서신집: https://tile.loc.gov/storage-services/master/gdc/gdcebookspublic/20/20/71/95/37/2020719537/2020719537.pdf | 현대 영어 요약; WA 1937의 원어 본문은 아님 | MODERN_EDITORIAL_SUMMARY |

**핵심 제한:** 위 확인은 목표 페이지 **이미지를 직접 열고 판독한 것과 다르다.** 이번 회차에는 WA Br 7 pp.466–468의 원판 이미지·원어 전문을 확보하지 못했으므로 `ORIGINAL_TEXT_VERIFIED=false`를 유지한다.

## 3. 검색에서 발견한 위험한 판본 혼동

WA에서 *Schriften* (저작 본편) Bd.7 (1897), *Deutsche Bibel* Bd.7 (1931), *Briefwechsel* Bd.7 (1937)는 전혀 다른 책이다. 이들의 `Band 7`을 혼동해서는 안 된다. 본 연구의 고정 식별자는 **WA / Briefwechsel (WA Br) / Bd.7 (1937) / Nr.3048 / pp.466–468**이다.

같은 숫자 `3048`을 사용한 BAKFJ의 별도 편집번호 역시 동음이의 위험이다(V3.67). `WA_BR:7:3048`과 `BAKFJ:3048`을 병합하지 않는다.

## 4. 원어 대조 전 보류하는 핵심 주장

- 카피토가 실제로 ‘바젤 대표단이 이미 귀환했다’라고 썼는지: **미확인**.
- 카피토가 바젤의 모든 성직자가 협약을 승인했다고 썼는지: **미확인**.
- 7월 19일 미코니우스 서신과 7월 20일 카피토 서신 사이의 직접 인과관계: **미입증**.
- 7월 17일의 사건 유형(파견·회담 종료·문서 작성·귀환): **미해결**.

## 5. 재현 가능한 다음 조사 절차 (V3.69)

1. Wikisource WA BR Bd.7의 Internet Archive **실제 item ID 및 개별 파생파일 URL** 추출; 1937년 원판인지 1969년 복각인지 분리.
2. 해당 판본의 목차·쪽수 보정표를 확인하고 인쇄 pp.466–468에 대응하는 스캔 프레임 번호를 확정.
3. **해당 세 면을 이미지로 직접 육안 검수**하고, 인쇄된 Nr.3048, 날짜, 발신·수신, 원어 문장과 각주를 순서대로 전사. 이미지 미검증 시 OCR 추측 전사 금지.
4. 원문과 *Capito Correspondence* III Ep.619(2015)의 영어 편집 요약을 문장 단위 대조하여 `DIRECT_QUOTE` / `EDITORIAL_SUMMARY` / `HISTORICAL_INFERENCE`로 태깅.
5. HBBW VI Nr.866의 원어 서신 본문을 별도 확보한 뒤 7월 19·20일 두 서신의 시간·정보 출처를 대조.
6. 전문가 검토 이후에만 기존 513편 역사 원고와 웹앱의 수정 제안.

## 6. QA

- [x] WA Br 7의 1937년 서지/복각 구분
- [x] 인터넷 복제본 링크 목록 식별
- [x] 저작 본편·성경판·서신집의 세 가지 '7권' 혼동 위험 분리
- [ ] Internet Archive 실제 item ID·이미지 프레임 특정
- [ ] WA Br 7 pp.466–468 원어 문장·각주 직접 판독
- [ ] HBBW 866 원어 서신 직접 대조
- [ ] 전문가 승인
- **CAN_SHIP=false**

본 회차에서는 기존 연구 결과의 증거 등급을 과대평가하지 않으며, main, 기존 513편, 앱, 원전 파일에 변경을 가하지 않는다.
