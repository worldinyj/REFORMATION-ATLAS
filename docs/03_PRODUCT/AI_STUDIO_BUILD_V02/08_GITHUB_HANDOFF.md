# 08 · Google AI Studio + GitHub 안전한 작업 안내

> DRAFT / 2026-10-25 · 공식 설명: [Build](https://ai.google.dev/gemini-api/docs/aistudio-build-mode), [Full-stack](https://ai.google.dev/gemini-api/docs/aistudio-fullstack), [Deploy](https://ai.google.dev/gemini-api/docs/aistudio-deploying).

## 1. 권장 개발 순서
1. Google AI Studio → **Build** → Web app 선택.
2. [06_MASTER_BUILD_PROMPT.md](06_MASTER_BUILD_PROMPT.md) 원문을 붙여넣어 **홈·8권·공통 템플릿** 생성.
3. Code 및 내부 Preview에서 실제 결과를 검토.
4. 개요 데이터가 필요한 시점에 원본 `data/overview/` JSON 5종 + `legacy_person_crosswalk_v01.json`을 명시적으로 추가. 앱이 GitHub 저장소를 자동으로 읽는다고 가정하지 않음.
5. [07_ITERATION_PROMPTS.md](07_ITERATION_PROMPTS.md) A~G 단계별 진행.
6. GitHub 연동·브랜치 정리·프리뷰 접근 권한은 **실제 사용자 계정에서 직접** 설정.

## 2. GitHub 가져오기/양방향 동기화
- 공식 Build 가이드: Build 입력창의 **파일 추가(+) → Import from GitHub**로 기존 프로젝트를 가져올 수 있다.
- 공식 동기화 경로: **Settings → GitHub**에서 저장소를 연결하고 Push/Pull, 충돌 시 diff 확인.
- **중요:** 현 저장소는 역사 연구 문서/데이터가 많은 저장소이지 이미 작동하는 웹 앱 저장소가 아니다. AI Studio가 루트에 React 파일을 만들어 기존 프로젝트를 덮어쓰지 않도록 앱은 **별도 feature 브랜치**, 가능하면 `apps/web/`에 정리.
- 별도 앱 생성 후 ZIP export → GitHub 새 브랜치 반영 방식도 가능한 대안. 자동 Git 동기화 충돌이 나면 우선 동기화를 중단하고 변경을 보존한다.
- 연동을 실제로 수행하지 않았으므로 **연결 완료 또는 GitHub에 앱이 배포됐다고 표시하지 않는다**.

## 3. 원본 보존 원칙
`data/`, `docs/01_CONTENT/`, `assets/`, `scripts/`, `.github/workflows/` 및 기존 연구 브랜치는 변경·삭제하지 않는다. AI Studio가 작업한 결과의 브랜치 diff에 이 경로가 있으면 멈추고 검토한다.

## 4. 프리뷰와 외부 공개의 차이
Google AI Studio 앱은 기본 비공개일 수 있으나 사용자가 **Share**를 수행하면 공유 상대가 앱 코드에 접근할 수 있다. **Publish/Cloud Run 배포**는 별개이며 서비스 사용/계정에 따라 요금이 발생하거나 자격요건이 있을 수 있다. 사용자가 승인하기 전 둘 다 실행하지 않는다.

현재 모든 개요 원고는 DRAFT. 자체 공개 게이트와 별개로 **GitHub public 저장소 자체의 원문 가시성**도 확인해야 한다. 클라이언트에서 CSS 숨김이나 noindex로 자료를 보호하면 안 된다.

## 5. Gemini/Firebase
MVP는 정적 탐색이므로 필요하지 않다. 불필요하게 Gemini API 호출을 추가하지 않는다. 훗날 API를 도입하면 **서버 측 Secrets** 사용. 브라우저 코드·git에 API 키가 있으면 절대 안 된다.

## 6. 디자인/품질 첫 검수표
- [ ] 로고·타이포·Hero가 단정하고 여백이 충분하다.
- [ ] 8권 카드가 4/2/1열로 배열된다.
- [ ] VOL-08이 시대가 아니라 사상/문헌 허브다.
- [ ] 메뉴/검색/직접 링크가 실제 동작한다.
- [ ] 320/375/768/1440px 레이아웃·키보드 접근 정상.
- [ ] JSON 입력이 없다면 빈 상태를 정직하게 표시한다.
- [ ] 거짓 역사 지도/미승인 AI 초상 없음.
- [ ] Share/Publish/Cloud Run/메인 병합은 실행하지 않았다.

## 7. 후속 심층 콘텐츠
AI Studio 앱의 사람·사건·문헌 상세 URL/ID를 그대로 유지하여 위클리프·후스·루터 등의 원전/비평/시각자료 승인된 깊이 블록만 추가한다. 기존 개요를 지우고 전부 다시 만드는 방식은 피한다.
