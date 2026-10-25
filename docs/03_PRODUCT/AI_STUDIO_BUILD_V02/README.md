# 종교개혁 아틀라스 · Google AI Studio Build 설계 패키지 V0.2
> 2026-10-25 · **DRAFT 설계문서 / 실제 웹앱 미생성**

기획과 역사 개요 데이터는 GitHub에 준비된 상태입니다. 사용자 요청에 맞게 **Google AI Studio Build 기반 React+TypeScript**, 현대적인 여백 중심 **Quiet Editorial Atlas** 디자인으로 설계를 일괄 갱신했습니다.

## 파일 읽는 순서

| 순서 | 산출물 | 설명 |
|---|---|---|
| 1 | [PROJECT PLAN](01_PROJECT_PLAN.md) | 8권 개요·제품 목표·범위 |
| 2 | [PRD](02_PRD.md) | 18개 기능·14화면 요구·사용자 경험 |
| 3 | [TRD](03_TRD.md) | Build/React TS·데이터/안전 게이트·확장 구조 |
| 4 | [UX/UI](04_UXUI.md) | 미니멀 디자인 시스템·화면 와이어프레임 |
| 5 | [TASKLIST](05_TASKLIST.md) | **36개 작업**·의존성·수용 조건 |
| 실행 시작 | [AI Studio 마스터 프롬프트](06_MASTER_BUILD_PROMPT.md) | 최초 앱 생성용 **복사·붙여넣기** |
| 후속 | [단계별 프롬프트](07_ITERATION_PROMPTS.md) | A~G 기능 확장/QA |
| 연동 | [GitHub Runbook](08_GITHUB_HANDOFF.md) | 가져오기·브랜치·권리/보안 |
| 토큰 | [DESIGN_TOKENS.json](DESIGN_TOKENS.json) | 화면 색상·타이포·패딩 규칙 |
| 추적 | [TASKLIST.json](TASKLIST.json) | 기계 판독용 작업표 |
| 품질 | [DESIGN_QA_V02.md](DESIGN_QA_V02.md) | 5문서·요구·작업 교차검증 |

## 현행 역사 개요 입력
8권·인물 33·사건 34·문헌 20·현대 지명 22·주제 10·관계 32·출처 ID 23 (중복 별칭 2). 장소 좌표는 미고증. AI 인물화/지도의 정식 공개 승인은 없음.

## 사용자의 실행 순서
Google AI Studio → Build → Web app → **06_MASTER_BUILD_PROMPT** 입력 → 홈 디자인/권별 탐색 미리보기 → 자료 JSON 가져오기 → **07_ITERATION_PROMPTS** 단계별 진행 → GitHub 브랜치 연동 검수.

**이 패키지의 문서 작성 완료가 웹 구현·외부 공유·운영 배포 승인인 것은 아닙니다.** 데이터 갱신과 코드/콘텐츠 공개는 별도 단계입니다.

## 추가 보조 파일
- [06_AI_STUDIO_MASTER_PROMPT.md](06_AI_STUDIO_MASTER_PROMPT.md): 영문 보조 지시문(한국어 기본 [06_MASTER_BUILD_PROMPT](06_MASTER_BUILD_PROMPT.md)과 동시에 실행하지 않음)
- [07_AI_STUDIO_ITERATION_PROMPTS.md](07_AI_STUDIO_ITERATION_PROMPTS.md): 영문 후속 명령 대안. 기본 흐름은 [07_ITERATION_PROMPTS](07_ITERATION_PROMPTS.md)
- [08_BUILD_CHECKLIST.md](08_BUILD_CHECKLIST.md): AI Studio 실제 수행 시 별도 사용자 검토표
- [SCREEN_CONTRACT.json](SCREEN_CONTRACT.json): 14개 화면의 구조적 계약
