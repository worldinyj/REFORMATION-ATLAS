# V3.08 · 513편 통합 심화 읽기 검토 화면

V3.04 475편, V3.05 20편, V3.07 18편을 중간 깊이로 통합합니다. 기존 원고를 덮어쓰지 않고 원본 입력 파일 네 개의 SHA256 또는 Git blob SHA1을 확인한 뒤 읽기 전용으로 조립합니다. 결과는 **513편·1539절·723 출처 레코드·31개 읽기 경로**입니다.

개요 97개 중 직접 대응 78, 부분 18, 배경 1, 원고 없음 0입니다. 97개 모두 *직접* 대응하거나 전문 역사 감수를 완료했다는 뜻이 아닙니다. 원판 이미지·고문헌 대조 및 외부 전문 역사 감수는 하지 않았으며 공개 HOLD를 유지합니다.

## 검토 화면

저장소 루트에서 python3 -m http.server 8765 --bind 127.0.0.1 명령 실행 후 http://127.0.0.1:8765/integrations/medium-atlas-v308/ 에 접속합니다. 종료는 Ctrl+C입니다.

기능: 한국어·영문 검색, 분야·읽기 경로 필터, 12편 목록 페이지 나눔, 세 절 본문·독서 질문·관련 해설·출처, 출처의 확인 범위 표기, URL에 검색/선택 상태 보존 및 키보드 탐색. 모든 표시 문자열은 textContent로 다루고, 원고를 HTML로 실행하지 않습니다.

## 재현

node --test integrations/medium-atlas-v308/*.test.mjs

node scripts/build_v308_integrated_delivery.mjs --check

node scripts/build_v308_integrated_delivery.mjs --export /tmp/atlas-v308-delivery

Chrome/Chromium 기반 별도 화면검사는 node integrations/medium-atlas-v308/browser-check.mjs 입니다. Playwright 1.56.1과 Chromium 설치가 필요하며, 한글 렌더링에는 한국어 글꼴이 필요합니다. CI는 JSON 산출물과 화면검사 결과/캡처를 서로 별도로 보관합니다.

이 화면은 정식 AI Studio 앱이 아닙니다. 최신 실서비스 라우트·개요 ID·컴포넌트와의 연결 검증, 실기기·Safari·스크린리더 검사, 사료 원본 전문 교감, 공개는 완료로 계산하지 않습니다.
