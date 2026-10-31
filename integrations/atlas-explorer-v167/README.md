# V1.67 · 독립형 종교개혁 역사 탐색 미리보기

V1.66 읽기 전용 데이터 어댑터를 사용하는 **별도 정적 HTML/JavaScript 샘플**이다. 기존 Google AI Studio 앱과 `main` 브랜치를 변경하지 않는다. 네 범주(심층 해설 10건, 판본 5건, 증거 카드 8건, 역사 도시 11건)를 선택하고 한글 검색어로 표시 결과를 걸러낼 수 있다.

## 구조
- `index.html`: 키보드 초점 표시, 접근성 레이블, 반응형 카드 레이아웃, 공개 불가 안내
- `explorer.mjs`: 동일 저장소의 기존 연구 JSON을 요청하여 V1.66 `buildAtlasPreview`에 전달한 후 미리보기 카드 렌더링
- `../ai-studio-readonly-v166/adapter.mjs`: 원본 데이터 변환, 잘못된 ID 또는 공개 설정에 대한 차단 규칙
- 외부 이미지, 영인 PDF, 실제 지도 타일, 데이터베이스 쓰기, 브라우저 저장소 변경 없음

## 로컬 실행
연구 브랜치를 로컬에 체크아웃했다면 저장소 **루트**에서 `python3 -m http.server 8765`를 실행하고 브라우저에서 `http://localhost:8765/integrations/atlas-explorer-v167/`을 연다. ES 모듈 및 JSON 파일 로딩은 `file://`보다 로컬 HTTP 서버를 권장한다.

**제한**: 여기서 만든 화면은 정적 샘플 UI이며 원격 배포·일반 공개 승인이 아니다. 서비스용 앱 스키마도 별도로 확인해야 한다. 도시 지도는 좌표를 카드로 표시하며 실제 지도가 아니다.

## 검증
`node --test integrations/ai-studio-readonly-v166/adapter.test.mjs`, `python3 scripts/validate_atlas_v167.py` 및 V1.65 통합 QA로 원본 데이터 참조·구조·배포 금지를 확인한다. 실제 시각적 브라우저 검수는 별도 단계다.
