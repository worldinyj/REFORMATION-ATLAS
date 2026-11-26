# V5.38 — 독립형 역사 ATLAS 미리보기
기존 AI Studio 앱과 무관한 정적 연구용 앱. 8권, 24장, 3단계 읽기, 지도, 사례, 인물, 문헌, 신학·지역 해설, 검색 기능. 모든 데이터를 DOM textContent 또는 제한된 Markdown 렌더러로 표현하며 원본 HTML을 실행하지 않는다. 외부 CDN 및 로그인 없음. 운영 데이터 변경 없음.

## 실행
로컬 저장소에서 V5.38 연구 브랜치를 동기화한다.
```sh
python3 research/v538/app/build_standalone.py --output /tmp/ATLAS_V538_REVIEW.zip
unzip /tmp/ATLAS_V538_REVIEW.zip -d /tmp/atlas-v538-review
cd /tmp/atlas-v538-review
python3 -m http.server 8765 --bind 127.0.0.1
```
브라우저에서 http://127.0.0.1:8765/ 접속. file:// 직접 실행은 지원하지 않는다. ZIP 생성 스크립트 및 브라우저 화면은 현재 실행 미검증. Markdown의 일부 형식(표, 번호 목록, 인용 등)은 문자 그대로 표시될 수 있다. 인물화 WebP 2개는 제외. 시각 자료는 정적 SVG이며 대화형 지도 엔진은 아니다. core_qa.json은 실제 입력을 사용한 코어 함수 검사만 기록한다. can_ship=false, can_import_ai_studio=false.

## 브라우저 인수 기준
1. 8권과 24장 링크, 깊이별 읽기 및 다음 장 이동
2. 지도 권 선택, 52개 사례, 좌표 미확정 표시
3. 인물 10명, 문헌 도해 5개, 신학·지역 해설 11편
4. 루터/타밀어/서상륜 검색, 빈 검색 및 결과 없음
5. SVG 누락 처리, 키보드 탐색, 모바일 360px·768px·1440px
6. 개발자 콘솔 오류, CSP, 악성 URL/HTML 표시 검토
7. 기존 운영 앱 및 main 브랜치 미변경 확인

실제 브라우저 E2E 미실시. 역사 및 신학 전문가 검토 역시 미완료.
