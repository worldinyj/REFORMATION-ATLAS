# 콘텐츠 → 제품 개발 문서 전환 V0.1

**지금은 제품 구현 전 단계.** 콘텐츠 시범 데이터를 먼저 확보한다.

## 산출물 순서
1. `PROJECT_PLAN.md`: 프로젝트 목적, 이용자, 콘텐츠 경험, 정보구조, MVP 범위.
2. `PRD.md`: 기능 요구, 유즈케이스, 수용 기준, 접근성, 비기능 요구의 사용자 관점.
3. `TRD.md`: 저장 구조, API, 검색, 지도·관계도·연대표 렌더링, 보안, 배포.
4. `UXUI.md`: 사이트맵, 탐색 시나리오, 와이어프레임, 디자인 시스템, 모바일 우선 UI.
5. `TASKLIST.md`: 우선순위, 의존성, 검증 방법, 완료 정의, 단계별 진척.

## 필요한 콘텐츠 증빙
- PER-0001~0003, 사건·관계 데이터의 고유 ID
- 1개 이상의 논쟁적 역사 주장에 대한 사실/전승 구분 사례
- 지도 1개, 관계도 1개, 인물화 가이드 1개
- 출처·이미지 권리 대장
- 탐색 관점별 시나리오(연도 / 지도 / 인물 / 사상 / 문헌)

## 개발 기술 결정은 추후
백엔드, 프런트엔드, 콘텐츠 관리 도구, 호스팅은 초기 사용자 시나리오와 데이터 크기가 확정된 후 TRD에서 결정한다. 현재 기술 스택을 확정하지 않는다.

## G4 공통 계약 초안 (2026-10-25)
- [8권 공통 데이터 모델 설계](G4_ATLAS_DATA_CONTRACT_V01.md) · [G4 Gate 대조](G4_DATA_READINESS_V01.md) · [JSON 계약](../../data/contracts/atlas_contract_v01.json).
- 글로벌 인물·사건·관계·장소 ID를 유지하고, 원전 접근 범위·역사적 확실성·편집 리뷰·공개 승인을 독립 상태로 분리.
- 제3권 V0.9-P4의 10점 이미지·지도 안전 캡션/14개 주장 링크로 시범 연결했다. **읽기 전용 projection 계약**이며 원본 데이터 이관 및 웹 구현은 미수행.
- G3 역사학 감수, G4 정본 검증과 Human Approver 승인 완료 전에는 G5/PRD/TRD/UXUI/TASKLIST에 '확정' 상태를 부여하지 않는다.

## 8권 공통 웹 MVP 설계 패키지 V0.1 (2026-10-25)
- [문서 패키지 목차](ATLAS_DESIGN_HANDOFF_V01.md) · [교차검증](ATLAS_DESIGN_QA_V01.md) · [기계 판독용 게이트](../../data/overview/design_readiness_v01.json).
- PROJECT PLAN → PRD → TRD → UX/UI → TASKLIST 모두 **DRAFT 초안 작성**. PRD 18기능, TRD 매핑 18/18, UX/UI 14화면, TASKLIST 30개.
- 사용자 승인/웹 앱 구현/운영 배포는 미실행, 제3권 연구 및 `main` 미변경.

## Google AI Studio Build 맞춤 8권 웹 MVP 설계 V0.2 (2026-10-25)
- [설계 패키지 목차](AI_STUDIO_BUILD_V02/README.md) · [프로젝트 계획](AI_STUDIO_BUILD_V02/01_PROJECT_PLAN.md) → [PRD](AI_STUDIO_BUILD_V02/02_PRD.md) → [TRD](AI_STUDIO_BUILD_V02/03_TRD.md) → [UX/UI](AI_STUDIO_BUILD_V02/04_UXUI.md) → [TASKLIST](AI_STUDIO_BUILD_V02/05_TASKLIST.md).
- Google AI Studio Build **React+TypeScript** 기반 설계. **Quiet Editorial Atlas** 미니멀 에디토리얼 스타일(여백·타이포 중심)과 토큰 사용. 기존 Astro 추천 V0.1 대신 이 문서를 AI Studio 구현 시 우선 참조.
- [한국어 마스터 앱 생성 프롬프트](AI_STUDIO_BUILD_V02/06_MASTER_BUILD_PROMPT.md), [7단계 후속 프롬프트](AI_STUDIO_BUILD_V02/07_ITERATION_PROMPTS.md), [GitHub 안전 동기화](AI_STUDIO_BUILD_V02/08_GITHUB_HANDOFF.md), [QA 15/15](AI_STUDIO_BUILD_V02/DESIGN_QA_V02.md).
- 36 Task (P0 33 / P1 3) 전부 NOT_STARTED. 설계 DRAFT, 웹앱 실제 생성/외부 공유/배포/메인 병합 **미실행**.
