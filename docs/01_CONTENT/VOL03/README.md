# VOL-03 · 종교개혁의 선구자 | Deep Research V0.4
**상태: DRAFT** (기초 공개 학술자료를 토대로 한 심화 연구 초안, 사람의 역사학 감수 전)

## 읽는 순서
1. [00_VOLUME_EDITORIAL.md](00_VOLUME_EDITORIAL.md): 연구 대상, 용어, 편집 범위
2. [01_WALDENSIANS.md](01_WALDENSIANS.md): 발도·왈도파와 1532년 개혁파 연결
3. [02_WYCLIF_LOLLARDS.md](02_WYCLIF_LOLLARDS.md): 위클리프·영어 성경·롤라드파
4. [03_HUS_AND_PRAGUE.md](03_HUS_AND_PRAGUE.md): 후스와 프라하의 개혁
5. [04_HUSSITE_MOVEMENTS.md](04_HUSSITE_MOVEMENTS.md): 후스파 전쟁·프라하 4개조·형제단
6. [05_SYNTHESIS_AND_PITFALLS.md](05_SYNTHESIS_AND_PITFALLS.md): 계보·신학 차이·후대 수용
7. [08_THEOLOGY_EUCHARIST_COMPARE.md](08_THEOLOGY_EUCHARIST_COMPARE.md): 위클리프·후스·야쿠베크 성찬론 비교
8. [09_PRAGUE_ARTICLES_AND_COMPACTATA.md](09_PRAGUE_ARTICLES_AND_COMPACTATA.md): 1420~1437 협상의 역사
9. [10_WALDENSIAN_MEMORY_AND_SOURCES.md](10_WALDENSIAN_MEMORY_AND_SOURCES.md): 1532년과 후대 역사 기억
10. [06_TIMELINE.md](06_TIMELINE.md): 날짜 정확도를 함께 표시한 연대표
11. [07_FACTCHECK_MATRIX.md](07_FACTCHECK_MATRIX.md): 단정 금지와 검증 과제
12. [05_SOURCE_REGISTER.md](05_SOURCE_REGISTER.md): 학술·전시 출처 35건과 실제 접근 범위

## 연결 산출물
- [볼륨 3 구조화 확장 데이터](../../../data/vol03_extension.json): 추가 인물 6명, 운동 4개, 위치 8곳, 사건 16건, 관계 7개
- [자체 제작 편집 가능한 SVG 관계도](../../../assets/diagrams/AST-0002_vol03_movement-pathways.svg)
- [원본 매체 관리대장](../../../assets/asset_manifest.json)
- [VOL-03 검증 스크립트](../../../scripts/validate_vol03.py)

- [검증 수준별 주장 카드](../../../data/vol03_primary_claims.json): V0.3 원전 검증 11건, DRAFT
- [주장 카드 스키마 해설](12_CLAIM_DATA_GUIDE.md): 서지·번역·원문 접근 수준 구분

## 스코프와 권한
- 이 저장소에는 **원고 Markdown과 JSON/SVG가 기준 자산**이다.
- Word V0.2 검토본 및 갱신된 V0.3 원전 검증 증보본은 대화에서 별도 다운로드로 제공되며, 현재 GitHub의 바이너리 자산으로 커밋되지 않았다.
- 기존 `docs/foundation-v0-1` 브랜치를 기반으로 한 후속 작업이다. `main`은 변하지 않았다.
- `PR`을 `DRAFT`로 유지한다. 검토 완료 전 발표·공개 승인 금지.

## 후속 내용 검토 순서
- [ ] 공인된 원전 판본을 통한 후스 『교회에 관하여』 및 위클리프 성찬론 심화 검증
- [ ] 프라하 4개조·1436년 콤팍타타 원문 및 번역의 차이 검토
- [ ] 왈도파 여성 설교 참여, 1532년 찬포랑 세부 경과 교차 검증
- [ ] 개신교/가톨릭/체코 지역사 관점의 교차 감수
- [ ] 검증된 좌표·시점별 경계에 근거한 실제 역사 지도 별도 제작
- [ ] AI 생성 역사 재현 인물화의 정확성·표현 검수 및 승인
- [ ] 이후 16세기 종교개혁(VOL-04)과 교차 링크

## 원전 대조 V0.3
- [11_PRIMARY_SOURCE_AUDIT_V03.md](11_PRIMARY_SOURCE_AUDIT_V03.md): 직접 확인한 판본·장·쪽수·편집본 제한을 구분한 사료 검증 기록.
- 다음 원문 검증의 미완료 항목(후스 라틴어 비평판 및 콤팍타타 공식 문서 전문)은 **미확인** 상태 유지.

## V0.3 내용 교정 노트
- **1433년 핵심 문안 3개와 2019 비평판 수록 문서 10개**를 분리하여 설명(원문 전문 직접 대조는 미완료).
- 후스와 루터 활동 시기 차이를 '한 세대 이상'에서 '약 100년'으로 표현 교정.
- 신규 원전 검증 항목은 [11_PRIMARY_SOURCE_AUDIT_V03.md](11_PRIMARY_SOURCE_AUDIT_V03.md)에 연결.

## V0.4 문헌 판본 및 사료 계보
- [13_DOCUMENT_PROVENANCE_AND_EDITION_V04.md](13_DOCUMENT_PROVENANCE_AND_EDITION_V04.md): 프라하 4개조 1844/1937 편집본 구분 및 콤팍타타 1433 핵심 3문안/2019 학술판 10문서 구분.
- [문헌-판본 JSON](../../../data/vol03_document_witnesses.json): 8개 역사 문헌 및 온라인 전사/현대 학술판 객체.
- [역사 주장 카드](../../../data/vol03_primary_claims.json): 기존 11건에서 14건으로 확장.
- 1433-11-30의 잠정 합의와 1437-12-23의 후속 조치를 사건 ID EVT-0019·0020으로 추가하되, 원전 미대조임을 명시.
- 1436년 이흘라바 선포와 1433년 프라하 합의는 서로 다른 사건.
