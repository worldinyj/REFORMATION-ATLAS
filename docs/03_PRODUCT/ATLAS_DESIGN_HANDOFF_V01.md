# REFORMATION ATLAS · 웹 MVP 설계 패키지 V0.1

> **개요 정보 → PROJECT PLAN → PRD → TRD → UX/UI → TASKLIST → 웹 뼈대 구현 → 인물·사건별 심층 연구를 지속 추가**
> 상태: **문서 초안 작성 완료 / 설계 승인·웹 구현 미완료**.

| 순서 | 문서 | 내용 |
|---|---|---|
| 1 | [PROJECT PLAN](ATLAS_PROJECT_PLAN_V01.md) | 8권 정보·대상 독자·로드맵 |
| 2 | [PRD](ATLAS_PRD_V01.md) | 기능 18건, 화면 경로 14개, 수용 기준 10개 |
| 3 | [TRD](ATLAS_TRD_V01.md) | 정적 우선 기술 제안, 콘텐츠/권리/출판 격리 |
| 4 | [UX/UI](ATLAS_UXUI_V01.md) | 14개 와이어프레임/화면 계약, 6개 핵심 흐름, 모바일 |
| 5 | [TASKLIST](ATLAS_TASKLIST_V01.md) | 30개 작업, 선행 조건, 완료·테스트 기준 |

[전체 설계 QA](ATLAS_DESIGN_QA_V01.md) · [검증 JSON](../../data/overview/design_readiness_v01.json)

## 웹사이트를 만들기 전 확정할 사항
1. 1차 사용자: 일반 교회사 독자와 교회교육 입문자를 우선할지.
2. 기술: Astro+TypeScript 정적 사이트로 시작할지, 다른 개발 스택을 선호할지.
3. 프리뷰: 로컬 비공개부터 시작하고 원격 프리뷰 시 인증 도입 여부.
4. UI: 홈·8권·인물·연대표·문헌·주제·검색을 P0로 유지할지.

## 개발 및 콘텐츠 고도화의 구분
- **웹 뼈대:** 8권과 127개 데이터 객체의 '개요'를 탐색할 구조를 먼저 구현.
- **심층:** 위클리프·후스·루터·칼뱅 등 인물/사건별 연구가 추가되어도 동일 인물 ID·URL을 유지하고 상세 블록만 확장.
- **지도·삽화:** 지금 장소 22곳의 역사 좌표는 미확인이고 제3권 그림은 고증 대기. 무단 노출·이동 경로 오인 금지.
- **사용자 승인:** 설계 문서 초안은 검토용이며 웹 앱 코드 작성·외부 배포의 자동 허가가 아니다.

판정: `DESIGN_DRAFTS_COMPLETE`, `USER_REVIEW_PENDING`, `WEB_NOT_STARTED`, `can_ship=false`.
