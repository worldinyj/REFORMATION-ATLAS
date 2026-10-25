# 00 · Google AI Studio Build 실행 전 GitHub 설계 감사 (필수)

> DRAFT / 2026-10-25. **이 지시문은 앱 생성보다 먼저 실행**합니다. 앱 코드·배포·main 변경은 이 단계의 산출물이 아닙니다.

## AI STUDIO PREBUILD PROMPT — START

당신은 Reformation Atlas의 제품 아키텍트, 모바일 UX 디자이너, React/TypeScript 엔지니어입니다. **지금은 앱을 만들지 마세요.** GitHub `worldinyj/REFORMATION-ATLAS`의 `plan/atlas-ai-studio-build-v02` 브랜치부터 실제로 읽고 확인하세요.

1. **접근부터 확인**: GitHub가 연결돼 실제 파일 내용을 읽을 수 있는지, 현재 브랜치·commit SHA·검사한 파일 경로를 보고하세요. 읽지 못하면 추측하지 말고 `PREBUILD_GATE=BLOCKED / NO BUILD`를 출력하고 필요한 연결/파일을 안내한 뒤 중지하세요.
2. **5대 설계 문서 대조**: `docs/03_PRODUCT/AI_STUDIO_BUILD_V02/` 아래의 `01_PROJECT_PLAN.md`, `02_PRD.md`, `03_TRD.md`, `04_UXUI.md`, `05_TASKLIST.md`와 `DESIGN_TOKENS.json`, `SCREEN_CONTRACT.json`, `TASKLIST.json`, 한국어·영어 06/07 프롬프트, 08 실행안내를 비교하세요.
3. **유기성·통일성·추적성**: FR-001~018, 화면 14종, 사용자 흐름 6종, Task 36개(AT-001~AT-036; P0 33/P1 3), 단계 G0→G4→P1, 화면/라우트 변수명, 글로벌 인물 ID, 출처·권리·공개 게이트, 스타일 토큰 간 모순·누락·중복을 확인하세요. Task 의존성 고아·순환도 검사합니다.
4. **역사 개요 원본 확인**: `data/overview/`의 권 8(제8권은 문헌·사상 자료실), 인물 33, 사건 34, 문헌 20, 장소 22, 주제 10, 관계 32, 출처 ID 23과 발도·위클리프·후스 3명 crosswalk를 실제 파일에서 확인하세요. 근사 날짜를 정확 일자로 변환하거나 역사 사실을 임의로 만들지 마세요.
5. **가장 중요한 제품 단계**: 우선 **OVERVIEW 개요 내용으로 웹앱 뼈대**를 만들고, 이후 **위클리프·얀 후스·루터 등 인물·사건·문헌별 DEEP_RESEARCH 심층 자료가 승인될 때** 같은 canonical ID·URL의 상세 페이지에 본문 블록을 추가합니다. 개요는 유지하고 기존 링크는 깨뜨리지 않습니다.
6. **모바일도 제1 사용 환경**: 320/360/375/390/430px 모바일부터 1열 구조·20px 여백·16px 이상 본문·검색/연대표/문헌/출처/필터·44px 권장 터치 영역·키보드 메뉴/포커스 복귀·가로 넘침 없음 점검. 태블릿 768/1024px과 데스크톱 1440px에서도 기능 동등성과 여백의 미를 유지하도록 04 UXUI·토큰을 맞춥니다.
7. **차이 조치**: `PASS/WARN/BLOCKER`로 구분하여 파일별 대조표를 만드세요. 사용자 승인 범위의 사소한 설계 문구/필드 충돌은 안전한 설계 브랜치에서 **최소 수정**, diff와 재검증을 보여주세요. 역사 원전·ID 정본·출판 승인 상태의 자의적 변경 또는 main 푸시 금지. 중대 모순은 `BLOCKED`로 중단.
8. **테스트**: 가능한 경우 실제 `python3 scripts/validate_ai_studio_design_v02.py`와 `python3 scripts/validate_atlas_overview_v01.py`를 실행하고 결과를 명시합니다. 실행하지 못했으면 `NOT RUN`으로 보고하고 통과를 주장하지 마세요.
9. **최종 감사 산출물**: `inspected_branch`, `inspected_files`, `consistency_matrix`, `findings`, `changed_files_and_diff`, `tests_run`, `unresolved_blockers`, `PREBUILD_GATE=PASS|BLOCKED`.
10. `PASS` 및 사람의 설계 범위 승인 뒤에만 `06_MASTER_BUILD_PROMPT.md`의 **B1 앱 최소 골격** 생성을 실행합니다. 이 단계에서는 공유·Publish·Cloud Run 배포를 하지 않습니다.

## AI STUDIO PREBUILD PROMPT — END

### 실행 순서
**00 사전 감사 → 문제 보완/재검증 → 설계 검토/승인 → 06 한국어 B1 마스터 생성 → 07 단계별 데이터 연결 → 모바일·데스크톱 QA → 별도 공개 승인.**

GitHub가 실제로 연결되지 않았다면 자료 접근을 먼저 해결해야 하며, 이 프롬프트를 통과했다는 이유만으로 AI Studio가 GitHub에 접근할 수 있다고 가정하지 않습니다.
