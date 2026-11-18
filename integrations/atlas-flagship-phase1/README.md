# 종교개혁 ATLAS — Phase 1 첫 완성형 역사 탐색 화면 (연구용)

> 2026-11-18 · **기존 Google AI Studio Build 앱 미수정** · 현재 저장소는 Public · 외부 역사학자 승인 미완료 · `can_ship=false`

## 이번에 실제로 만든 화면

**주제:** 마르부르크 회담(1529)에서 아우크스부르크 신앙고백 판본(1530·1531·1540)까지.

- [독립 실행 HTML](./preview-1529-1540.html): **브라우저로 열면 동작하는** 하나의 연구용 역사 탐색 페이지. 연표의 4개 사건과 그에 맞는 원문 설명, 제4권 L0(V4.47)·L1(V4.50) 실제 텍스트, 1530·1531·1540년 서지적 구별, 자료 카드 2개를 연결한다.
- [React 컴포넌트](./AtlasFlagship1529Panel.jsx)와 [범위 제한 CSS](./atlas-flagship.css): 기존 앱 디자인을 덮어쓰지 않고 이식할 수 있도록 `atlas-fp-` 클래스 범위에서 구성한 별도 후보.
- [테스트](./preview.test.mjs): HTML의 자료 수, 오프라인 성질과 연도 버튼·L0/L1·판본 비교·사료 접기·리셋을 확인하는 Node 테스트 파일.

### 바로 열어 보는 방법

GitHub에서 [preview-1529-1540.html](./preview-1529-1540.html)을 **Raw로 내려받아** `.html` 확장자로 저장한 다음 Chrome/Edge/Safari 브라우저에서 로컬로 연다. GitHub 파일 코드 보기 화면은 HTML을 실행하지 않는다. 초기 화면은 1529년 마르부르크이고, 1540년을 누르면 비Variata의 구별과 희귀본 소장목록 링크가 나타난다. `L1 · 중급 해설` 탭과 `1530·1531·1540년 판본 비교` 버튼을 누르면 필요한 설명이 나타난다.

원고 본문과 사료 메타데이터는 HTML에 실제로 **포함**돼 있으므로 인터넷 없이 볼 수 있다. 사료 링크를 열면 외부 사이트로 이동하며 상대 사이트가 방문 기록을 수집할 수 있다. 별도의 자동 수집·원격 스크립트·분석 호출은 없다. **GitHub 저장소 자체가 Public이므로 HTML에 포함된 연구 본문은 외부에 읽힐 수 있다.** `can_ship=false`로 접근을 막는다고 생각하면 안 된다.

### 코드와 검증 범위

V8에서 시범 HTML의 JavaScript 구문을 확인했고, 별도로 **모의 DOM에 실제 HTML의 스크립트를 실행하여 16개 상호작용 검사를 PASS**했다. 이는 단순 정적 텍스트 검사보다 넓지만 **Chromium·WebKit·Safari의 렌더링/키보드 실측**을 수행했다는 뜻은 아니다. GitHub의 Node 테스트 파일은 실행 방법을 포함하지만 이 환경에서 Node 테스트 러너로 직접 실행한 것으로 기록하지 않는다.

```bash
# git checkout integration/atlas-phase1-first-flagship-reader-scene
node --test integrations/atlas-flagship-phase1/preview.test.mjs
```

## 데이터 출처

1. `research/data/ATLAS_PHASE0_FLAGSHIP_SCENE_1529_1540_PRIVATE_MODEL.json` — 사건 4개, 사료 카드 2개, 역사적 불확실성. 정확한 교통 경로·지도·인물화는 없음.
2. `research/data/V4_47_TWO_SOURCE_GROUNDED_L0_HISTORY_CORRECTIONS.json` — 제4권 최신 연구 L0.
3. `research/data/V4_50_L1_24_CHAPTER_INTEGRATED_REVISED_MASTER.json` — `L448-04-02` 중급 설명.
4. `integrations/atlas-l1-phase0/bridge.mjs` — 이미 검증된 8권·24장·6주제·42연결·6개 입문 데이터 조회.

원문에서 선택한 문장을 임의로 재작성하지 않고 사용자에게 설명할 핵심 문장은 각 문서의 기존 `readersFinding`과 `claimLimit` 필드를 이용한다. 사료는 [German History Documents](https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/the-marburg-colloquy-the-marburg-articles-1529)와 [Gruber 희귀본 목록](https://gruber.lstc.edu/confessions/augs_apol.php)에 외부 링크를 제공한다. 완전한 16세기 원전 교감이나 역사학자 확인을 했다고 표현하지 않는다.

## 기존 Google AI Studio 앱에 연결하는 방법 (계약, 실적 아님)

**기존 앱의 실제 소스, 라우트, 인증, 프레임워크 버전이 아직 확보되지 않았다.** 따라서 `App.tsx` 같은 경로를 임의로 수정하면 안 된다. 개발자는 현재 앱을 비공개 개발 환경으로 복제하고 호스트의 실제 접근 제어를 먼저 확인해야 한다. React 후보가 받는 `privatePreviewGranted`는 UI 제한이며 **권한을 검증하거나 데이터가 공개 번들에 포함되는 것을 막는 보안 조치가 아니다**.

현재 React 후보 인터페이스:

```jsx
<AtlasFlagship1529Panel
  scene={validatedSceneModel}
  atlas={researchOnlyReadOnlyBridge}
  privatePreviewGranted={hostAlreadyAuthorisedUser}
  onReturnToAtlas={({kind,id}) => hostRouterNavigate({kind,id})}
/>
```

`validatedSceneModel`과 브리지 입력 JSON은 인증·권한 제한을 실제로 처리하는 호스트 측에서 안전하게 전달해야 한다. 인증되지 않은 사용자의 브라우저에 전체 JSON을 미리 다운로드시키고, React에서만 컴포넌트를 감추는 방식을 금지한다.

실제 개발 환경에서 필요한 추가 동작검증은 (1) 기본 라우터와 뒤로 가기, (2) React 빌드/버전 적합성, (3) 320·375px 가로 넘침, (4) 키보드 및 스크린 리더, (5) 공개 주소로 접근하는 비인가 사용자 차단, (6) 문헌 링크 동작, (7) 원고의 출처별 상태 표시다.

## 다음 제품 단계

- **앱 소스 확인:** 실제 AI Studio 프로젝트의 내보낸 소스/연결 저장소에서 현재 컴포넌트와 라우터를 확인.
- **비공개 통합:** 첫 사건 화면 1개만 기존 앱 디자인 안에 이식하고 실제 브라우저 테스트.
- **역사 지도:** 정밀도가 확인된 현대 도시 위치를 실험적으로 연결하되 1529년 실제 이동 경로·국경선을 창작하지 않음.
- **확장:** 첫 화면에서 독자의 이동이 자연스러운지 확인한 뒤 제7권 한국 기독교·성서 번역 사례에 같은 구조 적용.

현재 **실제 AI Studio 앱 변경 0건 / 검증된 외부 학자 0명 / 실제 독자 테스트 0건 / `can_ship=false`**.

## V4.52 후속 — 실제 브라우저 검증 준비와 키보드 접근성 보강

작업 브랜치: `integration/atlas-phase1-browser-qa-v452` (V4.51 첫 화면 브랜치에서 분기). 운영 앱과 `main`은 수정하지 않는다.

- `preview-1529-1540.html`: 연도 선택 후 키보드 초점 복원, L0/L1 탭의 방향키·Home·End 조작, `tabpanel`과 선택 탭 연결, 화면 낭독의 범위 축소, 좁은 화면에서 가로 스크롤 연표 표시.
- `browser-smoke.test.mjs`: Chromium과 WebKit 엔진, 320/375/768/1440px, 키보드 조작, 화면의 예기치 않은 가로 넘침, 증거 링크 보안 속성, 외부 자동 전송, 첫 화면 복귀 점검 및 스크린샷 저장.
- `.github/workflows/atlas-phase1-browser-qa.yml`: *이 연구 브랜치에 push할 때만* Node 기존 테스트와 Playwright 브라우저 테스트를 시행하도록 정의. `contents: read` 이외 권한이나 배포 단계가 없다.
- `research/data/ATLAS_V452_BROWSER_QA_AND_ACCESSIBILITY_AUDIT.json`: 4개 사건·2개 사료 카드, 인라인 JSON 내용 불변, V8 스크립트 구문 통과를 기록.

**아직 확인되지 않은 것:** GitHub Actions 실행 로그, Chromium/WebKit 실제 테스트 PASS, 본래의 Chrome/Safari 앱 검증, 실제 AI Studio 통합, 역사학자·독자 승인. CI 워크플로를 *작성한 것*과 테스트가 *성공한 것*을 구별한다. 완료되지 않은 테스트를 PASS로 간주하거나 `can_ship`을 바꾸지 않는다.

작업자 점검:

```bash
# 연구 브랜치로 checkout 후 저장소 루트에서
cd integrations/atlas-flagship-phase1
npm install --no-save --no-package-lock --ignore-scripts playwright@1.56.1
npx playwright install chromium
node --test preview.test.mjs
ATLAS_BROWSER=chromium node --test browser-smoke.test.mjs
```

실제 엔진 테스트가 통과하면 다음 단계는 **스크린샷을 육안으로 비교하여 접근성·모바일 레이아웃을 조정하는 것**이며, AI Studio 이식은 실제 호스트 소스와 인증 방식을 확인하기 전에는 여전히 금지한다.

## V4.53 — 검증 코드 보정과 React 후보의 기능 정합성 강화

1. 실제 GitHub HTML 스크립트를 V8의 **모의 DOM**에서 실행한 21개 검사가 PASS. 실제 Chromium/WebKit 실행에 대한 증거는 아직 없다.
2. `preview.test.mjs`에 키보드 포커스·탭 접근성 회귀 검사 2개를 추가. 총 6개 테스트 함수를 V8 호환 검증기로 실행해 PASS. `node --test` 결과는 아직 확인되지 않았다.
3. `browser-smoke.test.mjs`의 1531년 검사를 **제목**이 아닌 `#time` 날짜 레이블 기준으로 교정.
4. React 후보(`AtlasFlagship1529Panel.jsx`)에도 독립 HTML의 **1530/1531/1540 판본 비교**, 키보드 탭, 접근성 ID 연결을 반영. 기존 데이터 이외의 역사 주장 추가 없음.
5. `react-contract.test.mjs`를 신설하고 CI에 TypeScript JSX 구문 검사를 포함. **React 실제 빌드 성공을 의미하지 않는다.**

세 가지 독자 평가 여정 및 필수 승인 조건: [V4.53 검토 기준](./V453_READER_ACCEPTANCE_AND_RELEASE_GATES.md). 기계 검증 출처와 미확인 항목: `research/data/ATLAS_V453_FLAGSHIP_INTERACTION_PARITY_AUDIT.json`.

**중요:** `main`·실제 Google AI Studio 앱·배포 작업은 건드리지 않았고, 역사 원고 변경 없이 연구 브랜치 후보만 보강했다. `can_ship=false` 유지.
