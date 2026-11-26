# V5.39 — 실행 검증 및 독립형 사이트

## 이번 결과
- 전체 V5.37 데이터로 실제 JS를 모의 DOM에서 실행: 102/102. 본문 527줄 및 심층 링크 152개 비교.
- 초기 시험의 줄바꿈 비교 오판, 호스트 URL API 부재, 중첩 Markdown 표시 문제를 구별하고 수정. 실제 Node 실행 시 native URL 사용.
- 본문 건너뛰기 경로, 전문가 검토 안내, 사례 증거 경계 개선.
- `site/`에 원본 해시로 확인한 30개 파일 직접 구성. 사이트 구성 커밋 ec89b334921778e2d70b4b132db2dce882820f7c.

## 실행 (로컬 저장소에서)
```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory research/v539/site
```
브라우저에서 http://127.0.0.1:8765/ 를 연다. 별도 ZIP 빌드 불필요. 기존 앱과 분리.

## 검증 재현
```sh
node research/v539/simulated_dom_qa.mjs
# 별도 Playwright 환경에서 (설치 및 Chromium 준비 필요)
python3 research/v539/browser_qa.py --output /tmp/atlas-browser-qa
```
모의 DOM 시험은 연결 환경에서 실제 코드 실행 완료. Chromium 브라우저 시험 스크립트는 작성만 완료, 실행하지 않았다. 직접 GitHub 접속이 불가능한 로컬 환경과 연결 도구의 파일 전달 제약으로 실제 사이트 전체를 브라우저에 로드하지 못했다. ZIP 빌더도 미실행. 화면 품질, CSP, 실제 이미지 디코딩, 출처·좌표·신학 전문가 검토는 여전히 보류. 연구 브랜치 및 can_ship=false 유지. AI Studio 적용 또는 배포 없음.
