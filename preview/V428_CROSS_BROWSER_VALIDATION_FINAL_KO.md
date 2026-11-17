# 종교개혁 ATLAS V4.28 — 실제 Chromium·WebKit 브라우저 검증 완료

> 2026-11-17 · 연구용 L0 미리보기 · 기능·반응형 검증 **PASS** · 역사 전문가·독자·저작권·공개 심사는 **미완료**

## 1. 이전 단계에서 실제로 발견한 결함과 수정 결과

V4.27에서는 두 브라우저에 각각 236개 검사를 실행했다. Chromium은 **232/236**으로 메뉴에서 역사권으로 이동할 때 키보드 초점 확인 4건이 실패했다. WebKit은 **232/236**으로 태블릿·모바일의 일부 화면이 가로로 넘쳤다.

V4.28의 첫 실행은 Chromium **236/236**, WebKit **235/236**이었다. WebKit 320px의 제6권 `VOL-06`에서 마지막 1건의 가로 넘침이 남았다.

원인을 구분해 세 가지 UI 수정을 적용했다.

1. 라우터 메뉴 클릭을 즉시 렌더링한 뒤 중복 해시 이벤트를 한 번 건너뛰어, 클릭 직후 본문 초점이 빠지는 시점을 없앴다.
2. 콘텐츠·카드·앵커의 최소 너비와 1열 그리드 조건을 보강하고, 모바일 내비게이션을 **2×2 메뉴 그리드**로 바꾸어 네 메뉴가 320px에서 모두 보이도록 했다.
3. 제6권처럼 제목이 긴 경우에도 `word-break: normal`과 `overflow-wrap: anywhere`로 제목 자체가 화면 폭을 확장하지 않게 했다.

그 결과 최종 원본 HTML을 실제 브라우저에서 다시 실행했고 **두 엔진 모두 전체 통과**했다.

## 2. 실제 시험 범위와 최종 결과

| 시험 환경 | 1440×900 | 768×1024 | 375×812 | 320×700 | 최종 결과 |
|---|---|---|---|---|---|
| Chromium | 시험 | 시험 | 시험 | 시험 | **236/236 PASS** |
| WebKit | 시험 | 시험 | 시험 | 시험 | **236/236 PASS** |

**전체 472/472검사 통과, 실패 0건.** 검사에는 8권·6주제·입문 6장면, 42개 논리적 앵커의 화면·링크, 메뉴/장면 앞뒤 이동, 실제 검색어 입력, 키보드 건너뛰기·초점 확인, 가로 넘침, JavaScript 오류 및 외부 네트워크 요청 여부가 포함된다.

테스트는 **체크아웃한 HTML의 Git blob SHA를 선검증**한 뒤 Playwright Chromium/WebKit에서 `file://`로 실행했다. 이는 시뮬레이션이 아닌 실제 브라우저의 검사 결과다.

- **검증한 HTML Git blob:** `f822e320e99db4f0764553e074c2d0bb2479479f`
- **검증 보고서 Git blob:** `627069ce27ebe7a90ec7ea5b6b9cadc7a9b67d08`
- **구조화된 실제 결과:** [V428_BROWSER_E2E_RESULTS.json](../research/artifacts/V428_browser_evidence/V428_BROWSER_E2E_RESULTS.json)
- **자동화 검사 코드:** [v428_multi_engine_browser_probe.cjs](../research/tests/v428_multi_engine_browser_probe.cjs)
- **GitHub Actions:** [atlas-v428-browser-evidence.yml](../.github/workflows/atlas-v428-browser-evidence.yml)

## 3. 실제 스크린샷 확인

다음 3개 파일은 실제 테스트 엔진이 생성한 대표 화면이다.

- [Chromium 1440px: 8권 역사 첫 화면](../research/artifacts/V428_browser_checks/chromium/desktop-volumes.png)
- [WebKit 320px: 6개 주제 목록](../research/artifacts/V428_browser_checks/webkit/small-mobile-themes.png)
- [WebKit 320px: 제6권 본문과 6개 주제 연결](../research/artifacts/V428_browser_checks/webkit/small-mobile-VOL-06.png)

대표 화면을 실제로 검토한 결과, PC에서는 8권이 2열 카드로 배치되고, 소형 모바일에서는 내비게이션이 2×2 형태이며, 제6권 긴 제목이 두 줄로 표시되고 본문과 탐색 앵커가 화면 안에 유지된다. **스크린샷 점검은 대표 화면 육안 확인**이며 전체 화면·모든 가능한 기기에 대한 인간 사용성 시험을 의미하지 않는다.

## 4. 역사 원고와 배포의 경계

이번 V4.28은 **화면 동작만 수정**했다. V4.23에서 고정한 8권 서술, 6개 주제, 42개 연결, 입문 원고 6장면의 내장 JSON은 상위 V4.27과 **동일**하다. 별도 AI Studio 앱·기존 역사 연구 자료·`main` 브랜치는 변경하지 않았다.

브라우저 검증 PASS가 곧 역사적 타당성, 편집 승인, 외부 이미지·번역문 재사용 권리, 실제 사용자 이해도, 운영 서비스 안정성의 PASS를 뜻하지 않는다. 독립적인 전문 역사 교열, 비전문 독자 실측 시험, 이미지·문헌 저작권 확인, AI Studio 스테이징 사용성 평가와 최종 게시 승인이 필요하다.

**`can_ship=false`, `can_merge_main=false`, `AI_Studio_modified=false` 유지.**

## 5. 다음 권장 작업

**V4.29: 8권 L0의 실제 비공개 독자 평가와 AI Studio 스테이징 연계 범위 정리.** 모바일 기본 탐색이 실제 엔진에서 검증됐으므로 더 많은 미시 UI 파일을 만드는 대신, V4.23 콘텐츠를 웹앱의 임시 검토 환경에서 연결하고 역사·교파 편집자 및 비전문 독자의 이해도를 실제 관찰해야 한다. 외부 공개는 계속 보류한다.
