# V3.04 475편 검토 화면

저장소 루트에서 `python3 -m http.server 8765 --bind 127.0.0.1` 실행 후 `/integrations/medium-atlas-v304/`를 연다. 475편·24개 경로를 읽으며 SHA256 불일치는 오류로 표시한다. `bridge.mjs`는 97개 개요 항목의 명시적인 읽기 연결 API다.

```bash
python3 scripts/build_v304_integrated_delivery.py --check
node --test integrations/medium-atlas-v304/*.test.mjs
node integrations/medium-atlas-v304/browser-check.mjs
```

62개 모듈 검사와 320·375·1440px의 53개 화면 검사다. 각 폭에서 신규20편 전체의 본문·질문과 복구 출처 안내, 새 경로를 확인한다. 브라우저 검사는 Playwright·Chromium이 필요하며 `ATLAS_PLAYWRIGHT_MODULE`로 설치 경로를 지정할 수 있다. 결과와 PNG는 임시 `atlas-v304-browser-review`에 남긴다.

V3.03 출처는 이전 확인일·기록 복구일·재확인하지 않았다는 상태를 분리한다. 기존 V3.01 기록과 선택 주장22건의 수위를 유지한다. 이번 외부 자료 재검증·역사 전문 감수·실제 AI Studio 앱 검증은 아니다. 기존 V3.02 스냅샷은 보존하며 공개 HOLD다.
