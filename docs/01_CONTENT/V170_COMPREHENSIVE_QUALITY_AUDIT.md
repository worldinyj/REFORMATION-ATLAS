# V1.70 통합 UX·접근성·역사 콘텐츠 품질 감사

**범위**: REFORMATION-ATLAS 연구용 샘플. 별도 개발 중인 Google AI Studio 앱 및 `main` 미수정.

## 종전 대비 확장
- 기존 V1.69의 브라우저 조작 44건 검증에 더해, V1.70은 **axe-core 접근성 검사 + 뷰포트별 전체 탭 스크린샷 + 8개 브라우저 검사 × 4개 화면 = 32건**을 구성했다.
- 별도 작업으로 약 **30개의 콘텐츠 구조·출처·권리 보류·참조 게이트**를 실행하고 `audit-v170.json`을 생성한다.
- 60개 미니 강의의 본문 길이, 10개 심층 해설의 본문 길이, 동일 본문 중복, 출처 URL의 HTTPS 표기, 문헌 원본 직접 대조 여부와 시각자료 배포 승인 여부를 비교한다.

## 디자인·접근성 검토축
1. 320px 모바일, iPhone 12 프로필, 768px 태블릿, 1440px 데스크톱
2. 네 탭의 실제 자료 표시 개수와 화면 가로 넘침
3. Axe 규칙에서 serious/critical 위반 0건을 기본 목표로 설정
4. 한국어 검색·결과 없음·초기화·불러오기 실패
5. 출처 URL HTTPS, 새 창 보안 속성
6. 4개 탭별 스크린샷 자동 수집 — 사람이 직접 눈으로 확인하는 디자인 QC는 별개

## 학술 콘텐츠 검수의 한계와 우선순위
- 독서 원고의 **분량**은 학술적 정확성의 대용 지표가 아니다. 본문 길이가 1,200자 미만인 페이지는 깊이 있는 서술 보강 **우선 후보**로 분류한다.
- 미니 강의가 240자 미만이면 짧은 미니 강의로 명확히 분류하며, 심화 원고인 것처럼 과장하지 않는다.
- 모든 사료 직접 교감 상태가 false인 한, 원전 판면 확인 완료로 라벨링해서는 안 된다.
- 링크가 `https://`로 시작하는 것과 실제 외부 페이지가 정확한 소장본/판본을 가리키는 것은 별도의 검증 문제다. 외부 링크가 살아있는지 확인한 검사가 아니다.

## 적용 규칙
- `can_ship=false`와 시각자료 게시 보류를 유지한다.
- 자동 QA 통과 후에도 스크린샷에서 글자 잘림·장문 가독성·컬러 대비·시각 리듬을 수동 감수한다.
- 콘텐츠 학술 감수는 1차 문헌 판면·판본별 차이·서지 정본 관계를 직접 대조하는 후속 과제로 분리한다.

## 실행
```bash
python3 scripts/audit_atlas_v170.py
cd integrations/atlas-quality-v170
npm install
npx playwright install chromium
cd ../..
integrations/atlas-quality-v170/node_modules/.bin/playwright test --config=integrations/atlas-quality-v170/playwright.config.mjs
```
CI 증거물: `atlas-v170-editorial-audit` 및 `atlas-v170-visual-and-accessibility`. 스크린샷 결과를 전부 육안 평가했다는 의미는 아니다.
