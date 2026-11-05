# V3.02 integrated reading preview

455편 통합 전달본을 소비하는 별도 검토 화면과 Node/브라우저 공용 모듈이다. 기존 V2.98·V2.99·V3.00 파일은 그대로 보존한다. 실제 AI Studio 앱에 반영하거나 공개하지 않는다.

저장소 루트에서 `python3 -m http.server 8765 --bind 127.0.0.1`을 실행한 뒤 `http://127.0.0.1:8765/integrations/medium-atlas-v302/`를 연다. 검색·세 절 본문·질문·관련 해설·출처·21개 읽기 경로를 확인할 수 있다. manifest의 SHA256과 맞지 않는 자료는 오류로 표시한다.

```bash
python3 scripts/build_v302_integrated_delivery.py --check
node --test integrations/medium-atlas-v302/*.test.mjs
node integrations/medium-atlas-v302/browser-check.mjs
```

`adapter.mjs`는 455편·650개 출처 레코드를 읽는다. `bridge.mjs`는 별도로 불러온 V3.02 개요 연결표와 함께 사용한다. 개요 연결은 현재 화면의 별도 UI가 아니라 모듈 인터페이스로 제공된다. `manifest.json`의 경로·해시와 예상 개수를 확인한 뒤 데이터를 전달한다.

V3.01의 24개 출처는 `priorInspection`에 이전 확인 일자·범위·메모를 전달한다. 이번에 외부 자료를 다시 방문하지 않았으므로 접근 재검증 상태나 선택 주장 검증으로 승격하지 않는다. 기존 22개 선택 주장·11개 안내의 확인 범위도 유지한다.

브라우저 검사는 Playwright와 Chromium이 필요하다. `ATLAS_PLAYWRIGHT_MODULE`로 설치된 Playwright의 절대 경로를 지정할 수 있다. 320·375·1440px에서 기존 44개 검사와 새 9개 검사를 실행한다. 각 폭에서 신규 20편의 본문·질문을 모두 표시하고 V3.01 확인 기록, 새 읽기 경로, 수평 넘침도 확인한다. 결과 JSON과 화면 PNG는 임시 경로 `atlas-v302-browser-review`에 기록한다. `ATLAS_UI_ARTIFACT_DIR`로 경로를 바꿀 수 있다. 브라우저가 없으면 실패하며 통과로 세지 않는다.

GitHub Actions는 Chromium·한글 글꼴을 준비하고 동일 검사를 실행해 결과와 PNG를 14일 보관한다. 이번 로컬 환경에서는 Chromium 다운로드가 실패했으므로 로컬 화면 검사 통과를 주장하지 않는다. GitHub 실행 결과를 별도로 확인한다. 실기기·Safari·실제 AI Studio 앱의 검증은 포함하지 않는다.
