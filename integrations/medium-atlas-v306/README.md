# V3.06 — 495편 심화정보 통합 검토 화면

V3.04의 기존 475편과 V3.05의 신규 20편을 입력 동일성 확인 후 **읽기 전용 메모리 결합**으로 보여 줍니다. 검토용 화면의 검색·3절 본문·관련 읽기·출처·질문·URL 상태·모바일 폭을 제공하며, 27개 경로를 선택할 수 있습니다. 새 출처 22건의 확인 기록은 V3.05의 원래 범위 그대로 표시하고 이번 버전의 재확인으로 표시하지 않습니다.

저장소 루트에서 다음을 실행합니다.

\`\`\`bash
python3 -m http.server 8765 --bind 127.0.0.1
\`\`\`

접속: http://127.0.0.1:8765/integrations/medium-atlas-v306/

검토가 끝나면 Ctrl+C로 서버를 종료합니다. 외부 배포가 아닌 로컬 검토입니다.

검증 및 전달본 재현:

\`\`\`bash
node --test integrations/medium-atlas-v306/*.test.mjs
node scripts/build_v306_integrated_delivery.mjs --check
node scripts/build_v306_integrated_delivery.mjs --export /tmp/atlas-v306-delivery
\`\`\`

GitHub Actions는 동일 입력으로 495편 JSON과 개요97항목 대응표 JSON을 산출하고, Chromium 320·375·1440px 검토 화면 검사를 수행하여 결과와 스크린샷을 아티팩트로 남깁니다. 한국어 글꼴을 갖춘 CI 환경 기준으로 검사합니다.

이 화면은 실제 Google AI Studio 앱의 최신 코드·라우트·컴포넌트 연결 완료를 뜻하지 않습니다. Safari·실기기·스크린리더 전문 검사와 역사학자 검토는 별도입니다. 연구 문서, main, 실제 앱을 건드리지 않았으며 publication HOLD입니다.
