# REFORMATION ATLAS — Google AI Studio Build 설계 패키지 V0.2

> **2026-10-25 | 전체 설계문서 일괄 작성 완료 · 사용자 검토용 DRAFT**
>
> 기존 방침: **8권 개요를 먼저 정리 → 웹의 뼈대 개발 → 인물·사건·원전 심층 내용을 증분 추가.**
> 이번 패키지는 실제 AI Studio 앱 생성이나 Cloud Run 배포를 **수행한 결과가 아닙니다**.

## 읽는 순서 — 5개 설계 문서
1. [PROJECT PLAN V0.2](01_PROJECT_PLAN.md) — 프로젝트 목표·8권·Google AI Studio 기반 실행 계획
2. [PRD V0.2](02_PRD.md) — 사용자 여정·14개 화면·FR 18개·디자인 요구/수용기준
3. [TRD V0.2](03_TRD.md) — React+TypeScript 데이터/컴포넌트·출처/공개 게이트·실제 개발 순서
4. [UX/UI V0.2](04_UXUI.md) — Quiet Editorial Atlas, 8권 사이트맵·홈/상세 텍스트 와이어프레임·모바일
5. [TASKLIST V0.2](05_TASKLIST.md) — 36개 작업(P0 33 / P1 3), 선행·완료·검증 기준

## Google AI Studio에서 사용할 때
6. [AI Studio FIRST MASTER PROMPT](06_AI_STUDIO_MASTER_PROMPT.md) — **처음 한 번 붙여 넣는 B1 생성 지시문**
7. [AI Studio ITERATION PROMPTS](07_AI_STUDIO_ITERATION_PROMPTS.md) — 데이터/검색/인물/QA/동기화 등 B2~B4 프롬프트
8. [AI Studio 실행 전·진행 체크리스트](08_BUILD_CHECKLIST.md) — 실제 시연 확인과 배포 방지 점검

## 한국어 버전 마스터 프롬프트
- [첫 실행용 한국어 지시문](06_MASTER_BUILD_PROMPT.md)도 제공한다. **06_AI_STUDIO_MASTER_PROMPT.md 또는 한국어 지시문 중 하나만 골라 처음 실행**한다. 두 프롬프트를 연달아 넣어 기존 앱을 재생성하지 않는다. 두 문서는 동일한 B1 목적의 선택지다.

## 기계 판독용 규격
- [디자인 토큰 JSON](DESIGN_TOKENS.json)
- [14개 화면 계약 JSON](SCREEN_CONTRACT.json)
- [36개 작업 기준 JSON](TASKLIST.json) · [콘텐츠 관리용 미러 JSON](../../../data/overview/ai_studio_tasklist_v02.json)
- [설계 QA 판정 JSON](../../../data/overview/ai_studio_design_readiness_v02.json)
- [읽기 전용 설계 QA 스크립트](../../../scripts/validate_ai_studio_design_v02.py)

## 비주얼 한 줄 요약
**현대적인 역사 아틀라스 — 넉넉한 여백, 차분한 컬러, 큰 편집형 타이포, 4/2/1 반응형 8권 카드, 미니멀 타임라인.**

- #F7F8F5 바탕, #1C2925 잉크, #205F50 포인트
- 본문 720px 정도, 전체 1200px, 장식과 그림자 최소
- 이미지 없이도 완성도 높은 텍스트 기반 화면
- 얀 후스/루터/위클리프 심층 연구가 추가되어도 인물 ID·상세 URL 유지

## 실행 원칙
1. Google AI Studio Build(Web)에서 **06의 PROMPT만 먼저 실행**.
2. 미리보기 디자인을 검수하고, 07의 B2~B4 프롬프트를 하나씩 사용.
3. 자료 파일을 가져오지 못했다면 '실제 자료 127건을 임포트했다'고 주장하지 않고 DEMO라고 표시.
4. 공유·Publish·Cloud Run 배포와 GitHub main 변경은 별도 사용자 승인.
5. 원본 제3권 고위험 AI 역사 이미지 및 미검증 지도 좌표를 공개하지 않음.

## 상태
- V0.1 (Astro 가정) 설계 문서는 보존.
- V0.2 (AI Studio Build / React 가정) 설계 문서는 **새 별도 브랜치/폴더**.
- PROJECT PLAN/PRD/TRD/UXUI/TASKLIST: 작성됨(DRAFT).
- 웹 구축: 0건, 앱 미리보기 검증: 미실행, 서비스 공개: 미승인.

### 기계 판독 기준 안내
- `TASKLIST.json`의 36개 `AT-001~036`이 V0.2 정식 작업 ID다.
- `data/overview/ai_studio_tasklist_v02.json`은 같은 36개 작업을 참조하는 호환용 미러. 서로 다른 수량/의존성이 되면 자동 검증이 실패한다.
- 아직 앱 개발은 시작하지 않았으며, AI Studio 앱 생성/동기화 시 PRD 18요구사항·14화면의 범위를 다시 점검한다.
