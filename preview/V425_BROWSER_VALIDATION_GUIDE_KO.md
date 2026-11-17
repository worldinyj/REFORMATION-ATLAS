# ATLAS V4.25 — 실제 브라우저 검증과 미리보기 개선

> **연구용 브랜치 · 내부 편집 미리보기 · can_ship=false**
>
> V4.24 콘텐츠 탐색 HTML의 키보드 접근성과 주제 분류 표시를 수정했습니다. Chromium/Playwright 브라우저 검증 코드와 GitHub Actions 워크플로도 작성했습니다. 코드가 **작성·정적 실행된 것**과 **실제 브라우저 검증을 완료한 것**은 구분합니다.

## 이미 적용한 실제 화면 개선

1. **키보드 초점:** 메뉴·연결 버튼을 눌러 다음 화면으로 가면 `main`으로 초점을 옮깁니다. 텍스트 검색 중에는 검색 입력창 초점을 유지합니다.
2. **한국어 표시:** 내부 분류 `CORE_CASE` / `CONTEXT_BRIDGE` / `LIMITED_CONTEXT_NOT_DOCTRINE`를 독자 화면에서 **핵심 사례 / 맥락 연결 / 제한된 배경**으로 나타냅니다. 근거 데이터 자체는 보존합니다.
3. **제8권의 구조:** 제1~7권에는 권당 6개 주제 연결이 있지만 제8권은 주제 아카이브 자체이므로, 제8권에 동일한 6개 앵커가 없다고 오류로 판정하지 않습니다.

## 현재 확인 상태

V4.25의 실제 HTML 내 JavaScript를 추출해 **모의 DOM 환경에서 실행**했습니다. 8권과 6주제 목록, 개별 상세 화면, 입문 6장면, ‘후스’ 검색, 42개 논리적 연결, 초점 이동, 한글 분류 표시가 통과했습니다. 보고된 구조 오류는 0건입니다.

단, 이는 **실제 Chrome/Chromium/Safari 브라우저 화면 테스트는 아닙니다.** Playwright 테스트 코드와 자동화 워크플로를 추가했지만 GitHub Actions의 실제 성공 결과 또는 PNG를 아직 확인하지 못했습니다. 따라서 실제 브라우저 검증은 **미완료**입니다.

## Mac에서 실제 Chromium 테스트 실행

저장소 루트에서 다음을 순서대로 실행하면 됩니다. 기존 프로젝트 npm 파일은 변경하지 않습니다.

```zsh
git fetch origin research/atlas-v425-browser-e2e-visual-check-l0
git switch research/atlas-v425-browser-e2e-visual-check-l0

mkdir -p /tmp/atlas-v425-tools
npm install --prefix /tmp/atlas-v425-tools --no-save --no-package-lock playwright@1.56.1
/tmp/atlas-v425-tools/node_modules/.bin/playwright install chromium

NODE_PATH=/tmp/atlas-v425-tools/node_modules node research/tests/v425_browser_probe.cjs
```

실제 실행하면 `research/artifacts/V425_browser_checks/`에 데스크톱·태블릿·모바일 PNG와 `V425_BROWSER_REPORT.json`이 생성됩니다. 테스트 코드를 작성했다는 사실만으로 이 결과물이 이미 존재하는 것은 아닙니다.

## GitHub Actions 실행

워크플로: [atlas-v425-browser-check.yml](../.github/workflows/atlas-v425-browser-check.yml)

- V4.25 연구 브랜치에 대한 push 또는 수동 dispatch를 지원하도록 설정했습니다.
- 1440×900, 768×1024, 375×812, 320×700의 네 화면 크기를 검사합니다.
- 실제 브라우저에서 8권·6주제·6장면, 주제→권 클릭, 장면 이동, 검색, 키보드 초점, 모바일 가로 넘침, 자원 요청 및 런타임 예외를 확인합니다.
- 실제 실행 시 결과 PNG·JSON을 Actions artifact로 업로드하도록 작성했습니다.
- 이 문서 작성 시점에는 실제 workflow job 통과와 artifact 업로드 완료를 관찰하지 못했습니다. **검증 통과로 표기하지 않습니다.**

## 다음 결정

Chromium 테스트를 실제 실행해 결과와 스크린샷을 확인한 뒤 필요한 UI만 수정합니다. 그 다음에 Mac Safari/VoiceOver 또는 실제 모바일 검토와 AI Studio 스테이징 연계를 진행합니다.

역사 전문가 심사, 실제 독자 평가, 출처·사진·현대 번역 재사용 허가, 공개 승인과 `main` 병합은 모두 별도의 미완료 조건입니다. `can_ship=false`.
