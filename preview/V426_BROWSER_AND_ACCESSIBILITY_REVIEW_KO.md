# 종교개혁 ATLAS V4.26 — L0 미리보기 접근성·브라우저 시험 준비

> 2026-11-17 · L0 내부 검토 · **공개 보류(can_ship=false)**

## 이번에 실제로 고친 것

기존 V4.25 미리보기 HTML에 세 가지 사용자 동작 수정이 들어갔다. 첫째, 상단 '본문으로 건너뛰기'가 `#main`으로 해시를 바꿀 때 히스토리 라우터가 첫 화면으로 되돌아오는 경로를 없앴다. 둘째, 최초 페이지 로드 시 `main.focus()`로 강제 초점을 이동하지 않고 사용자가 화면을 옮길 때만 초점이 본문으로 가도록 했다. 셋째, 검색 문자열을 전부 지웠을 때 검색 라우트와 입력 초점을 유지해 새 검색어를 계속 입력할 수 있게 했다.

V4.26의 화면 상단 버전과 하단 표기도 V4.26으로 바꿨지만, 실제 상위 역사 원고의 출처 버전은 V4.23이다. 8권 본문·6주제·42개 주제 연결·6장 입문 서술과 보류 중인 역사 주장 자체는 그대로다.

## 실행할 브라우저 검증

브라우저 회귀시험 스크립트: `research/tests/v426_multi_engine_browser_probe.cjs`

GitHub Actions: `.github/workflows/atlas-v426-browser-matrix.yml`

검증 매트릭스는 Chromium과 WebKit 두 엔진에 각각 1440×900, 768×1024, 375×812, 320×700 네 화면 크기를 적용한다. 로컬 file:// URL의 **실제 HTML Git blob**을 대조한 뒤 8권 탐색, 6주제 탐색, 각 주제의 7개 시대권 연결, 6장 입문·앞뒤 이동, 검색·검색어 제거, 본문 바로가기, 키보드 초점, 가로 넘침, JavaScript 오류, 외부 요청 여부를 자동화했다. 각 엔진의 화면 캡처 및 JSON 결과는 Actions artifact로 보존하도록 지정했다.

GitHub Actions UI에서 직접 결과 확인: https://github.com/worldinyj/REFORMATION-ATLAS/actions/workflows/atlas-v426-browser-matrix.yml

이 연구 브랜치의 워크플로는 push 이벤트로 실행하도록 정의돼 있다. **이 문서 작성 시점에는 이 세션에서 실제 Actions job의 실행 성공, 이미지 artifact 및 전체 화면에 대한 사람의 시각 검수를 확인하지 못했다.** 따라서 브라우저 시각검수 PASS를 선포하지 않는다.

## macOS에서 실제 검증 실행 (저장소 루트에서)

```zsh
git fetch origin research/atlas-v426-chromium-verified-offline-preview-l0
git switch research/atlas-v426-chromium-verified-offline-preview-l0

mkdir -p /tmp/atlas-v426-node
npm install --prefix /tmp/atlas-v426-node --no-save --no-package-lock playwright@1.56.1
/tmp/atlas-v426-node/node_modules/.bin/playwright install chromium webkit

NODE_PATH=/tmp/atlas-v426-node/node_modules ATLAS_BROWSER_ENGINE=chromium node research/tests/v426_multi_engine_browser_probe.cjs
NODE_PATH=/tmp/atlas-v426-node/node_modules ATLAS_BROWSER_ENGINE=webkit node research/tests/v426_multi_engine_browser_probe.cjs
```

동작하면 `research/artifacts/V426_browser_checks/chromium/` 및 `webkit/` 아래에 PNG와 `V426_*_BROWSER_REPORT.json`이 실제로 생성된다. **이번 GitHub 커밋에는 그 PNG와 결과를 생성한 것으로 주장하지 않는다.** 기존 npm 구성, AI Studio 앱, `main`, 513편 원고는 변경하지 않는다.

## 지금 확인 가능한 항목과 남은 승인

- **확인됨:** V4.26 HTML의 JavaScript 문법, 8권·6주제·42링크·6장면 등록, 모의 DOM 기반 화면 이동·검색·바로가기·초점·한글 분류 동작.
- **실제 시험 증거 미확인:** Chromium/WebKit 화면의 가로 넘침, 작은 화면 본문 가독성, WebKit 렌더링, 저장된 PNG와 JSON 리포트.
- **다른 차원의 미완료:** 교회사·교파 전문 역사 검토, 실제 비전문가 독해 시험, 현대 번역·사진·지도 권리 확인, AI Studio 스테이징, 배포 승인.

## 다음 권장 판단

실제 Actions 실행 결과의 두 엔진 점검표와 PNG를 확인한 다음, 오류가 재현된 부분만 보정한다. 이 결과를 통과해야 **비공개 AI Studio 스테이징에 V4.23의 상위 역사 텍스트를 연결**할지 판단할 수 있다. 완료되지 않은 외부 역사 검토와 저작권 승인 없이 공개하지 않는다.
