# V1.69 · 실 브라우저 E2E 및 모바일 화면 검증

**범위:** Google AI Studio 앱과 main을 변경하지 않는 격리형 연구용 Chromium 테스트.

## 4가지 브라우저 화면 조건
- 320×700: 소형 모바일
- iPhone 12 브라우저 프로필: 모바일 터치 및 뷰포트
- 768×1024: 태블릿
- 1440×900: 데스크톱

## 11개 E2E 시나리오 × 4개 화면 = 44개 실행 항목
1. 탭 4종과 카드 개수 10/5/8/11 확인
2. 한국어 검색 및 결과 없음 복구
3. 외부 출처 링크에 안전한 새창 속성 확인
4. 탭별 가로 오버플로 검증
5. 언어·검색·상태 요소 접근성 점검
6. 공개 제한 안내 유지
7. 스크린샷 수집
8. 키보드 탭 컨트롤 접근
9. 버튼과 입력창 터치/레이아웃 크기 확인
10. JSON 서버 503 오류 시 안내
11. 외부 링크 HTTPS 검증
12. 뷰포트 크기 변경 후 데이터 상태 복원

실제 테스트 파일에는 explorer 6건, resilience 5건으로 **총 11개** 테스트가 있다. 위 항목 4~5처럼 한 테스트에 여러 점검이 포함되므로 위 번호는 세부 체크리스트다.

## 사용
```bash
cd integrations/atlas-explorer-v169
npm install
npx playwright install chromium
cd ../..
integrations/atlas-explorer-v169/node_modules/.bin/playwright test --config=integrations/atlas-explorer-v169/playwright.config.mjs
```

CI는 Chromium을 실제 설치하고 페이지를 로드하여 클릭, 검색, URL, 뷰포트 크기를 점검한다. 스크린샷, 실패 시 비디오와 추적은 GitHub Actions의 `atlas-v169-browser-evidence` 아티팩트에 저장한다. 성공적인 기능 테스트가 역사 콘텐츠의 사실 검증이나 이미지 저작권 승인을 대신하지 않는다.

## 공개 금지 상태
연구용 화면의 `canPublish=false` 및 이미지 게시 차단 상태를 지속 유지한다. 웹앱 실서비스 적용은 별도 편집/권리/스키마 승인 대상이다.
