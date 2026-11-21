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

## V4.54 — 실제 Chromium의 대표 UI 재구성본 시험 및 모바일 복귀 개선

- **발견·수정:** 좁은 화면에서 1540년까지 연표를 넘겼다가 ‘1529년으로 돌아가기’를 눌러도 연표의 좌측 시작 부분이 다시 나타나지 않았다. 초기화 시 가로 연표를 왼쪽으로 복귀시키고 독자를 화면 상단으로 이동하게 수정했다.
- **인지성:** 모바일에서만 “연표를 좌우로 밀어 다른 사건을 보세요.”를 노출하며, 비교 표의 열/행 제목에는 `scope`를 지정했다.
- **React 동등 기능:** React 후보에도 초기화 버튼, 모바일 탐색 안내, 가로 스크롤을 위한 별도 연표 래퍼, 키보드·판본 비교 기능을 유지했다.
- **회귀 검사:** `browser-smoke.test.mjs`와 `react-contract.test.mjs`에 관련 조건을 추가했다.

### 검증 범위 및 통제

로컬 환경의 **실제 Chromium 브라우저**에서 320·375·768·1440px의 대표 UI 재구성본을 테스트했고 네 화면 크기에서 기능·모바일 가로 넘침·초기화 동작 모두 PASS 했다. 이것은 단순 V8 모의 DOM이 아닌 실제 Chromium 렌더링 테스트다.

다만 네트워크 및 파일 전송 제약 때문에 **GitHub HTML 전체를 그대로 로드하지는 못했다.** 브라우저 시험용 파일의 사건·문헌·역사 원고 텍스트는 축약한 테스트 데이터다. 실제 GitHub HTML의 **인라인 JavaScript 코드와 시험용 JavaScript는 글자 단위로 일치**하며, 양쪽 모두 길이 4266, FNV-1a 값 `6edc912b`로 대조했다. 레이아웃 CSS도 같은 주요 규칙을 이용했으나 GitHub의 CSS와 완전히 동일한 파일이라고 주장하지 않는다.

이 4/4 PASS는 **전체 원본 HTML의 실제 브라우저 검증, WebKit 실행, Node 테스트 러너의 CI 완료, React 앱 빌드·AI Studio 이식, 원전 검토, 실제 독자 평가를 대신하지 않는다.** 근거와 미검증 사항은 `research/data/ATLAS_V454_CHROMIUM_FIXTURE_BROWSER_AUDIT.json`에 기록.

후속 우선순위는 실행 가능한 GitHub CI에서 **원본 그대로** Playwright 테스트 로그와 스크린샷을 확보한 뒤 오탐/실패를 해결하는 것이다. 출시 제한 `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false` 유지.

## V4.55 — 정확한 Git 원본의 실제 Chromium 검증 (2026-11-18)

**원본 동일성:** `preview-1529-1540.html`을 GitHub 연결에서 읽은 후 파일 자체의 `git hash-object`를 계산하여 Git Blob SHA-1 `c5906c70752089c218b9bdef8b9ed2fb452000cd`와 정확히 일치함을 확인했다. 전체 UTF-8 파일은 22,498바이트이고 역사 L0/L1 원고는 축약되지 않았다.

**실제 브라우저:** Chromium 144.0.7559.96 + Python Playwright 1.57.0에서 320·375·768·1440px × 각 32건 = **128/128 PASS**. 원본 HTML 전체를 `page.set_content`로 브라우저에 전달했다. 로컬 `file://` 탐색은 관리자 정책으로 차단되어 사용하지 않았다. 이 결과는 실제 렌더링 시험이지만 원격 배포 사이트 또는 WebKit/Safari 시험이 아니다.

**React 후보:** `AtlasFlagship1529Panel.jsx`도 Git Blob SHA `2e5a1f73334ed3e807ace3a2556c78bf7c1511c6`와 일치하는 파일로 TypeScript 5.8.3 JSX transpile 구문 오류 **0건**. 가상 React 모의 런타임으로 9개 상태/구조 검사 PASS. **실제 React 라이브러리와 기존 AI Studio 앱으로 빌드한 결과는 아니다**.

**새로운 가독성 개선 항목:** 독립 HTML은 본문을 `textContent`로 표시하므로 `###`, `**` 같은 Markdown 표시가 그대로 노출된다. React 후보에는 최소한의 Markdown 표현이 있지만 두 화면의 가독성 일치가 부족하다. 후속 V4.56에서 원본 내용을 수정하지 않고 안전한 Markdown DOM 구성으로 개선하되 `innerHTML`을 쓰지 않고 회귀검사를 반복하는 방안을 우선한다.

자세한 구조화 감사 파일: `research/data/ATLAS_V455_EXACT_ORIGINAL_CHROMIUM_AND_JSX_AUDIT.json`. 실제 스크린샷과 실행 코드, 원본 파일이 포함된 증거 ZIP은 현재 대화의 로컬 산출물로 보존했으며 GitHub 저장소에 업로드하지 않았다.

**출시 상태 유지:** `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`. 역사학자 승인, 실제 독자 시험, 실제 호스트 인증 및 WebKit 검증은 미완료다.

## V4.56 — 역사 원고 표시 개선, 안전한 Markdown AST 공유

- `preview-1529-1540.html`은 역사 연구용 `l0.text` / `l1.text`의 기존 **JSON 문자열을 한 글자도 바꾸지 않고** `document.createElement`와 `document.createTextNode`만으로 제목·굵은 글씨·기울임 글씨·문단·구분선을 렌더링한다. `innerHTML` 사용 금지.
- `research-markdown.mjs`의 `parseResearchMarkdown`를 React 후보 `AtlasFlagship1529Panel.jsx`에서 직접 가져다 쓴다. 독립 HTML은 오프라인 사용을 위해 동일한 파서 함수를 코드에 내장한다. `markdown-contract.test.mjs`가 내장 함수와 외부 모듈의 일치성을 검사한다.
- **허용된 표현 범위만 지원:** 제목 `#`–`####`, `**bold**`, `*italic*`, 빈 줄로 구분한 문단, `---`. 표·목록·중첩 표현·원시 HTML을 완전히 지원하는 CommonMark 파서가 아니며, 지원하지 않는 부분을 자동으로 과해석하지 않는다.
- Chromium 144.0.7559.96에서 **320·375·768·1440px × 23건 = 92/92 PASS**, 로컬 `node --test markdown-contract.test.mjs` **4/4 PASS**, GitHub 원본을 읽은 모의 DOM 회귀 **7/7 PASS**, TypeScript 5.8.3 JSX 구문검사 오류 **0건**. 실제 Google AI Studio 앱 빌드 및 WebKit 실측으로 오해하지 않는다.
- `preview.test.mjs`, `browser-smoke.test.mjs`, `react-contract.test.mjs`는 새 의미론적 DOM 기준으로 보강했고 CI에 Markdown 계약 테스트를 추가했다.

연구 증거: `research/data/ATLAS_V456_SAFE_MARKDOWN_RENDERER_PARITY_AUDIT.json`. 브라우저 스크린샷·전후 비교 그림·로컬 실행 스크립트는 이번 대화의 산출물로 제공한다.

**중요:** 원전 교감·역사학자 승인·실제 독자 평가·정식 React 빌드·AI Studio 호스트 인증 검증 전까지 `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`를 유지하며 `main` 및 기존 운영 앱은 변경하지 않는다.

## V4.57 — 역사적 주장 14건과 실제 독자 평가 도구의 사전 설계

- **역사 사료 대조:** GHDI 마르부르크 15개 조항, 그루버 희귀본 아우크스부르크 자료 페이지를 다시 읽어 첫 대표 화면의 역사 주장 **14건**을 주장·근거·확인 한계별로 등록했다. 그중 **HIGH 10건**은 전문가 미승인 상태로 분리한다. 1540년 비Variata 설명의 소장번호 불명확, 그루버 문구의 ‘Calvinists’ 후대 서술 가능성도 위험으로 기록했다.
- **독자 여정:** ① 1529년 합의와 불일치, ② 1530·1531·1540년 제출·인쇄·판본, ③ 번역 문서와 소장목록의 근거 차이. 총 3개 과제와 **9개 이해도 문항**을 준비했다.
- **평가 기준 사전 등록:** 최소 6명(목표 8명), 개인 9문항 중 7개 이상 및 핵심 7문항 중 6개 이상·세 과제 완료, 전체 개인 합격률 80% 이상, 과제 완료율 80% 이상, 같은 고위험 오해가 2명 이상 반복 시 설계 보류.
- **오프라인 채점기:** `score-reader-session.mjs` 및 `reader-pilot-contract.test.mjs` 신설. 주장/사료/문항의 일치성과 임계값 판정을 검증하는 **5개 함수가 V8 모의 Node 적응 실행에서 PASS**. **실제 `node --test`·GitHub Actions 완료는 확인하지 못했으므로 혼동하지 않는다**. CI에는 별도 Node-only 연구 데이터 검증 job을 추가.
- **인간 평가 0:** 실제 참여자, 역사 전문가, 독립 서지 검토자, 운영 앱 빌드/인증은 아직 검증하지 않았다. 파일럿 답안은 공개 연구 저장소에 있으므로 참가자에게 정답을 사전 공개하지 않도록 진행 절차에 명시했다.

**검토 실행 문서:** [V4.57 역사학자·독자 프로토콜](./V457_HISTORIAN_READER_PILOT_PROTOCOL.md)

**데이터:** `research/data/ATLAS_V457_CLAIM_SOURCE_CRITICAL_REGISTER.json`, `research/data/ATLAS_V457_READER_PILOT_INSTRUMENT.json`, `research/data/ATLAS_V457_REVIEW_AND_PILOT_GATE_AUDIT.json`.

**출시 차단:** 원고·장면·실제 AI Studio 운영 앱·`main`을 변경하지 않았고 `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false` 유지.

**다음 단계:** 새 연표 이벤트 추가보다 먼저 고위험 10건 원전·서지 전문가 검토와 실제 독자 6–8명 파일럿을 수행하고, 발견된 오해를 원고/정보 구조에 반영할지 판단한다.

## V4.58 — 마르부르크 원어·1531/1540 판본 증거표 (고위험 10건)

역사학자에게 전달할 **원어·실물 서지 증거표**를 구성했다. GHDI 독일어/영어 전사, Gruber 희귀본 목록, 에모리 Pitts 1540 Variata 디지털 소장 기록, 에모리 Kessler 2017 전시 도록 34쪽, 후대 학술·고백사 해설을 **7개 출처 기록 / 17개 증거 단위**로 연결하였다.

- **1529년 마르부르크:** GHDI 독일어 전사 제15조에서 `gaistliche niessung`(영적 참여), `leiblich im Brot und wein`(빵과 포도주 안의 육체적 임재 문제), `dißer Zeit nit vergleicht`(당시 미합의)를 구별했다. 제15조는 공통 선언과 미합의 양쪽을 모두 담고 있다. GHDI는 WA 30/III(1910), 160–171쪽 전사에 근거하며 원물 지면과 필사본을 직접 대조한 것은 아니다.
- **1531년:** Gruber 46 라틴어 신앙고백·변증서(`Witebergae: Georgium Rhau, MDXXXI`), Gruber 7 독일어본 1531년 11월 종결기록을 분리했다. 독립적인 에모리 Pitts 도록은 비텐베르크의 1531년 독일어판 **VD16 C4736**을 식별한다.
- **1540년:** Gruber 28 및 Pitts Variata는 1540년 라틴어 수정판으로 기록된다. Pitts 도록에서 **VD16 C4713**을 확인했다. 이는 **Gruber의 무번호 1540년 비Variata** 항목을 식별하는 번호가 아니다.
- **새로운 문법 경고:** 표제 `Addita est Apologia Confessionis diligenter recognita`의 `recognita`는 `Apologia`(변증서)를 수식한다. 표제 자체를 신앙고백 수정 판정의 유일한 근거로 사용하면 안 된다.
- **제10조 한정 대조:** 후대 연구의 라틴어 병렬 전사는 `vere adsint et distribuantur` 대 `cum pane et vino vere exhibeantur`를 보여준다. 하지만 16세기 실물 인쇄본의 완전 교감이나 저작자 의도 확정은 아니다.
- **마르부르크 당대 인쇄본:** 같은 에모리 도록에서 1529년 마르부르크 조항의 **VD16 W2117**을 별도 식별했다. 본문 원문·GHDI 편집판 사이의 인쇄 지면 교감은 미실시.
- **상태 유지:** 고위험 주장 **10건 중 10건에 1개 이상 근거 연결**, 그러나 **역사학자 승인 0명, 독자 실측 0명, 실제 AI Studio 통합 0건**. 근거를 붙였다고 논쟁적인 학술 해석이 확정된 것은 아니다.

**전문 검토 문서:** [V4.58 한국어 증거 대조 보고서](./V458_SOURCE_CRITICAL_EXPERT_EVIDENCE_DOSSIER_KO.md)

**연구 데이터:** `research/data/ATLAS_V458_HIGH_RISK_TEXTUAL_BIBLIOGRAPHIC_EVIDENCE_MATRIX.json`  
**감사 기록:** `research/data/ATLAS_V458_ORIGINAL_TEXT_AND_EDITION_AUDIT.json`  
**자동검증:** `v458-evidence-contract.test.mjs` (V8에 Node 파일 읽기/테스트 호출만 대체한 5개 검사 PASS; GitHub Actions 실제 실행 성공은 확인되지 않음). CI 연구 계약 작업에 추가함.

**다음 우선순위:** Gruber 무번호 1540 비Variata 실물 식별 및 독일어/라틴어 실제 인쇄 지면 교감. 각 문장 원전 대조에 따라 전문가 2인의 독립 판정 후 역사 콘텐츠 승격 결정.

**릴리스 제한:** `can_ship=false` / `can_merge_main=false` / `can_import_ai_studio=false`. `main`·Google AI Studio 운영 앱·원래 연구 원고 수정 없음.

## V4.59 — 사본 계통의 중요한 발견: 취리히 Z와 헤센 K는 본문이 완전히 같지 않음

이번 연구에서는 실제 Google AI Studio 운영 앱의 기능을 늘리지 않고 **사료의 '개체' 자체를 분리하는 정보구조**를 강화했다.

- **필사 원본 2종:** `StAZH E I 3.1 Nr.54`(취리히 Z)와 `HStAM Best.3 Nr.245`(헤센 K). 취리히 공식 보관소 목록은 **Z의 제7·13·15조 추가 문장이 K에 없다는 사실**을 명시한다. 두 문서를 하나의 고정된 원본으로 합치지 않는다.
- **원본 사진 실제 열람:** 헤센 주립문서보관소의 `archivnachrichten 17/1 (2017)` 인쇄 10쪽(PDF 0기준 9쪽)에서 **앞부분과 서명 사진을 화면으로 확인**. 제15조의 필사 원문 전체를 독해한 것은 아니다.
- **1529년 인쇄판 4종:** Worms `VD16 W2117`, Zürich `W2118` 및 `W2119`, Basel `W2108`의 실물 서지/디지털화 경로를 서로 분리했다. 어느 인쇄본이 Z 또는 K의 제15조를 그대로 따르는지는 아직 **HOLD**.
- **1531년 원문 비교 준비:** 바이에른 주립도서관의 1531년 **라틴어 `VD16 C4734`, `bsb11411960`(288스캔)**과 **독일어 `C4736`, `bsb10160424`(506스캔)** 디지털 개체를 분리해 식별했다. 각 제10조 인쇄 지면을 실제로 읽고 대조한 것은 아니다.
- **1540년 판본 구분:** Pitts `VD16 C4713` Variata와 Gruber의 번호 미확정 1540 비Variata를 혼동하지 않는다. 1540년 Google Books 스캔 개체는 발견했으나 서지판 동일성을 단정하지 않았다.
- **초안의 정확도 표시:** Z의 제15조 추가 문구가 '생자·사자 타인을 위한 미사의 은총 획득'과 관련 있다는 후대 영어 번역 단서는 있으나 **독일어 원본 문구로 직접 확인되지 않았다**. 이를 확정된 원어 인용으로 승격하지 않는다.
- **검증:** 사본/인쇄본 10건, 이문 3건의 데이터 정합성 검사 **5/5 PASS**(V8에서 GitHub 원본 테스트를 Node 파일 읽기 방식만 대체해 실행; `node --test`와 실제 CI는 미확인). 연구 CI에도 추가.

**한국어 논문형 대조 보고서:** [V4.59 필사·인쇄본 계통 연구](./V459_MANUSCRIPT_EDITION_STEMMA_RESEARCH_KO.md)  
**서지 개체 데이터:** `research/data/ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json`  
**검증 기록:** `research/data/ATLAS_V459_WITNESS_PROVENANCE_AND_UNCOLLATED_TEXT_AUDIT.json`  
**검증 코드:** `v459-witness-contract.test.mjs`.

**핵심 결론:** 제15조에 관한 앱 화면에는 '마르부르크 조항'이라는 단일 텍스트 레이블뿐 아니라 **사본(K/Z), 인쇄본(VD16), 후대 편집 전사(WA/GHDI)** 중 무엇을 근거로 해석하는지 밝혀야 한다. 실물 원전 문장 교감과 역사학자 승인까지 `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false` 유지. `main`/AI Studio 운영 앱 미변경.

## V4.60 — 라틴어 제10조의 실제 비판판 인쇄 지면·K/Z 원문 편집 근거 확보

**이번 증거의 정확한 수준:** 1858년 `Corpus Reformatorum` 제26권 **실제 인쇄 357쪽(PDF 0기준 5쪽)·주석 34번을 화면에서 직접 확인**하여 1531년판 계통과 1540년판 계통의 제10조 라틴어 비교를 실제 비판 장치에 연결했다. 16세기 해당 인쇄본 2종의 지면을 각각 열었다고 주장하지 않는다.

- **1531 Ed.1/2:** `vere adsint et distribuantur`.
- **1540 Ed.3/4:** `cum pane et vino vere exhibeantur`.
- **편집사 추가 확인:** `CR26`은 1531년 4절판(Ed1), 1531년 별도 수정 8절판(Ed2), 1540년 4절판(Ed3), 1541–42년 8절판(Ed4)을 구분한다. **1531 Ed2에 이미 수정의 역사가 있다는 편집사적 사실**과 오늘날 고유명사처럼 사용되는 `1540 Variata`를 동형으로 동일시하지 않는다.
- **마르부르크 K/Z 검토 인용문헌 확보:** 취리히 공식 문서보관소 기록은 2014년 루터교 계열의 K 기반 판본, `Reformierte Bekenntnisschriften` Z 기반 판본, `MBW Texte 3 no.825`(K에 Z 이문 병기), Usteri 1883 취리히본 팩시밀리를 구체적 페이지까지 소개한다.
- **실증 한계:** 1529년 K/Z 제15조의 직접 필사본 글자 대조 및 1531/1540 원본 제10조 지면은 아직 **HOLD**. Gruber 무번호 비Variata는 `VD16 C4713`으로 추정하지 않는다.
- **기계적 정합성:** `v460-critical-apparatus-contract.test.mjs`의 **5개 검사 GitHub 소스 V8 검증 PASS**. Node test runner와 GitHub Actions 실행 로그의 성공은 확인하지 못했으며, 연구 CI에는 검사용 경로만 추가.

**전문 검토 문서:** [V4.60 라틴어 제10조와 마르부르크 K/Z 본문 계통](./V460_CR26_ARTICLE10_AND_MARBURG_KZ_CRITICAL_DOSSIER_KO.md)

**연구 JSON:** `research/data/ATLAS_V460_CR26_ARTICLE_X_APPARATUS_AND_MARBURG_BASES.json`  
**검증 JSON:** `research/data/ATLAS_V460_CR26_PRINT_PAGE_REVIEW_AUDIT.json`

**승격 제한:** `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`. 실제 독자 평가 0명 / 역사학자 승인 0명. `main`, 기존 역사 본문, AI Studio 앱 변경 없음.

**V4.61 권장:** 추가 주장·버전보다 K/Z 15조 원문 잎과 VD16 C4734/C4713의 10조 원문 잎을 실제로 열고 비판판과 **텍스트 라인 단위 비교**를 완성한다.

## V4.61 — 서명본 K/Z 차이의 현대 번역 혼입과 제10조 OCR 경고

**역사적 실무 리스크 확인:** HAPuls 현대 독일어 번역 페이지의 하단에는 헤센본 `HStAM PA Nr.245`가 표기되지만 번역 내용은 **제7조 수도원 서원, 제13조 사제 혼인, 제15조 타인의 은총 획득을 위한 미사**에 관한 문장을 포함한다. 취리히 주립문서보관소의 공식 목록은 이 문장들이 속한 제7·13·15조의 추가 구절은 **Z에 존재하고 K에는 없다고 명시**한다. 따라서 `shelfmark=K`만 보고 화면의 편집 번역문을 K의 글자 그대로의 전사로 둔갑시킬 수 없다.

- GHDI WA 기반 역사 독일어 전사와 HAPuls 현대 독일어 번역을 조항별로 나란히 읽어 **3개 추가 구절의 존재**를 확인. 다만 Z/K 서명본 실제 해당 잎은 **두 개 모두 읽지 못함**.
- 헤센 교육 포털의 `/node/1472`에 원본 전체 디지털화 전용 페이지가 있다는 점을 확인. 현재 실제 제15조 이미지 직접 판독 **0건**.
- 튀빙겐 대학 OpenDigi가 우스테리의 **1883년 취리히본 팩시밀리 409–413쪽**이 실린 권호를 디지털화하여 공개함을 발견. PDF 응답 시간 초과로 해당 지면 직접 대조 **미완료**.
- 1858년 `Corpus Reformatorum` 26권 인쇄 357쪽 제10조는 PDF 추출과 이미지/독립 역사 전사 간 `exhibeatur` / `exhibeantur`의 **추출·판독 차이**가 존재. **16세기 원전 이문이 검증됐다는 주장으로 승격하지 않음**.
- 실제 사용자 화면 개선 제안: `archivalShelfmark`, `editorialTextSource`, `selectedReadingFamily`, `sourceInspectionLevel`을 분리해 표기.

**근거/검토 문서:** [V4.61 서명본-번역 저본 혼동 방지 보고서](./V461_MARBURG_KZ_SOURCE_BASE_CONFLICT_AND_ARTICLE10_OCR_RESEARCH_KO.md)  
**대조 데이터:** `research/data/ATLAS_V461_KZ_ARTICLES_7_13_15_EDITORIAL_ALIGNMENT_AND_CR26_TEXT_DIFF.json`  
**감사 기록:** `research/data/ATLAS_V461_SOURCE_BASE_AND_OCR_AUDIT.json`  
**테스트:** `v461-manuscript-edition-source-contract.test.mjs` GitHub 원본 테스트 본문을 V8에서 Node 파일 로드만 적응하여 실행한 **5/5 PASS**. GitHub Actions 실제 성공은 미확인.

**출시 차단:** `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`. 역사 원고, main 및 실제 AI Studio 운영 앱 변경하지 않음.

## V4.62 — 원본 지면 4개 직접 판독 확보 게이트와 기록

- **원본 대상 4개 정리:** 1529 마르부르크 K·Z 각각 제15조, 1531 라틴어 `VD16 C4734`과 1540 Variata `VD16 C4713` 각각 제10조. **정확한 16세기 원문 지면 직접 판독 성공 0/4**, 이미지 체크섬 0건, 외교적 전사 0건으로 정확히 기록한다.
- **Hessen Arcinsys 뷰어 구체적 확인:** `HStAM 3 Nr.245` 공식 열람기에 진입하여 `digitalMediaViewer.action?archivalDescriptionId=5447099`를 확인했고, JPG 디지털 복본 정보의 `representationId=14439026`을 식별했다. 현재 텍스트 도구에서는 로딩 이미지뿐이어서 제15조 직접 판독 실패.
- **취리히/1883년:** 튀빙겐 OpenDigi 제56권(1883) 및 Usteri 파크시밀리 409–413쪽의 출처는 확인됐으나 PDF 다운로드 **시간 초과**. Z 문서의 실제 제15조 사진은 미확인.
- **1531/1540년:** 바이에른 주립도서관 C4734의 288개 스캔은 서지 메타데이터로 확인했지만 실제 제10조 잎은 뷰어 접근 제한. Pitts 2017 도록 34쪽 및 독립 1540년 Google Books 책은 **표제지·서지 단계**이며 **Google 책이 Pitts C4713과 동일 판본인지 확인하지 않았다.**
- **잎 번호의 별도 확인 필요:** HAPuls의 K `Bl.60–63`와 취리히 목록에 나온 K `fol.60r–64v`는 표기가 다르며 실제 지면과 목록 관습 대조 없이 누락·오기라고 단정하지 않는다.
- **새 fail-closed 검증 코드:** `primary-source-evidence-gate.mjs`는 원문 사진 실제 열람, 원본 SHA256, 정확한 스캔/잎 번호, 독일어·라틴어 외교적 전사, 사람 QC를 모두 요구한다. 하나라도 미충족이면 '원문 직접 검증됨'으로 승격하지 않는다. 연구용 합성 데이터로 준비 조건을 시험해도 **릴리스 게이트는 항상 false**.
- **검증:** 원본 GitHub 소스를 이용한 V8 적응 실행에서 5개 검증 그룹 **5/5 PASS**; `node --test` 및 실제 GitHub Actions 성공은 미확인. 연구 CI에는 테스트 경로를 추가했다.

**작업 프로토콜:** [V4.62 원본 지면 확보·증거 승인](./V462_FOUR_ORIGINAL_FOLIO_ACQUISITION_AND_QC_PROTOCOL_KO.md)  
**지면 4개·기관 접근 기록:** `research/data/ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json`  
**증거 판정:** `primary-source-evidence-gate.mjs`  
**감사:** `research/data/ATLAS_V462_FOUR_FOLIOS_EVIDENCE_GATE_AUDIT.json`

**차기 우선:** 화면 기능 확장이 아니라 **해당 지면 4개를 대학/기록관 원본 뷰어에서 실제 확보·전사**하여 1529 K/Z와 1531/1540 라틴어를 병렬 교감. 전문가 승인·독자 파일럿 이전에는 `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`. `main`과 실제 Google AI Studio 앱·역사 원고는 변경하지 않음.

## V4.63 — 최초로 당대 1529년 **인쇄 원본 본문** 제15조 직접 확인

이전 버전의 서지 정보·후대 전사와 달리, **취리히 중앙도서관(Zentralbibliothek Zürich) 소장 1529년 프로샤우어 인쇄본 `VD16 W2119`의 실제 지면 사진**을 e-rara 원본 PDF에서 열어 확인했다.

- **1529년 W2119 원간:** 제목 `Wie sich D. Martin Luter ... und Huldrich Zvingli ...`, Zürich, Christoffel Froschauer, 소장번호 `5.174,5`. 원본 PDF `https://www.e-rara.ch/zuz/download/pdf/170052`, DOI `https://doi.org/10.3931/e-rara-597`, e-rara 표제면에서 **Public Domain Mark** 확인.
- **PDF 0부터 6쪽:** 제15조 제목 `Von Sacrament des lybs und blüts Christi` 아래 미사는 살아 있거나 죽은 다른 사람을 위해 은총을 획득하는 일이 아니라는 문장이 **실제 1529년 활자로 인쇄**되어 있음을 확인. 또한 성찬에 관한 공통 진술과 그리스도의 몸/피의 신체적 임재 방식 미합의가 함께 인쇄돼 있다.
- **PDF 0부터 5쪽:** 제13조의 사제 혼인을 금지하는 가르침에 반대하는 문장을 당대 인쇄면에서 확인. 제7조 추가 문구는 이번에 정확하게 확인했다고 표시하지 않는다.
- **학술적 의미:** 취리히 기록관이 서명본 **Z에 제7·13·15조 추가문장 존재**를 기록한 사실과, W2119 당대 인쇄본에서 제13·15조의 대응 문구를 직접 확인한 사실을 연결했다. 이것이 **W2119 전체가 Z 서명본과 글자 단위로 동일하다는 증명은 아니다**.
- **실물 지면 증거 수준:** 웹 PDF 사진에 있는 인쇄 본문을 직접 읽었으며, 주석·인쇄 오탈자 포함 전체 외교적 전사, 원문 이미지 해시, K/Z 필사원본 대조, 역사학자 QC는 미완료. 원본 이미지 파일은 로컬에 직접 다운로드하지 못하여 GitHub에 재업로드하지 않았다.
- **V4.62와의 엄격한 구분:** 네 목표 지면인 K와 Z 서명본 각각의 제15조 및 1531·1540 초기 라틴어 인쇄본 각각의 제10조 **완료 0/4 유지**. W2119은 **그와 별개의 1529년 실제 인쇄판 원전 증인**이다.
- **정합성 회귀:** W2119 사료 ID·페이지 위치·직접 읽은 활자 대 ‘미확보 필사 원본’ 구분을 **5개 V8 적응 검증에서 PASS**. Node 실행 및 GitHub Actions 실동작 성공은 확인되지 않았고, CI 설정에 테스트 경로를 추가했다.

**원전 직접 판독 보고서:** [V4.63 취리히 W2119 제13·15조 인쇄 본문 판독](./V463_ZURICH_W2119_1529_ART13_ART15_ACTUAL_PRINT_EVIDENCE_KO.md)

**증거 기록:** `research/data/ATLAS_V463_W2119_1529_PRINT_ART13_ART15_DIRECT_SCAN_EVIDENCE.json`  
**검증 기록:** `research/data/ATLAS_V463_1529_PRIMARY_PRINT_VISUAL_INSPECTION_AUDIT.json`  
**회귀 코드:** `v463-original-print-witness-contract.test.mjs`.

**이어갈 원전 작업:** W2118 제15조 인쇄면과 W2119을 먼저 직접 비교하고, 이어 서명본 Z/K 지면과 대조. 별도로 1531 C4734·1540 C4713 제10조 인쇄면 확보. `main`, 실제 AI Studio 운영 앱·기존 24장 원고 미변경. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`.

## V4.64 — 1529년 취리히 W2119와 바젤 W2108 **인쇄 원본 두 판본 직접 대조**

이번에는 사료를 하나 더 '목록에만 등록'하지 않고 **취리히와 바젤이라는 다른 지역에서 1529년에 인쇄된 두 실제 원본 PDF의 관련 페이지를 열어 비교**했다.

- **취리히 W2119:** `ZB Zürich 5.174,5`, Froschauer, [1529]. [원본 PDF](https://www.e-rara.ch/zuz/download/pdf/170052) **0기준 p4(제7조), p5(제13조), p6(제15조)**를 실제 사진으로 확인.
- **바젤 W2108:** `UB Basel Falk 2950:5`, Thomas Wolff, [1529]. [원본 PDF](https://www.e-rara.ch/bau_1/download/pdf/1643132) **0기준 p8(제7조), p10(제13조·제15조 시작), p11(제15조 끝 및 인쇄 서명자)**를 실제 사진으로 확인.
- **역사적 성과:** 제7조의 수도원 생활과 서원을 의 획득 수단으로 보는 견해 거부, 제13조의 사제 결혼 금지 교리 비판, 제15조의 미사를 타인을 위한 은총 획득 행위로 보는 견해 거부라는 **세 문구의 내용이 서로 다른 두 지역의 1529년 인쇄본에서 모두 확인**된다. 제15조의 성찬 공통진술과 육체적 임재 방식 미합의도 두 인쇄본에 존재.
- **전승 계통 주의:** 취리히 보관소의 'Z에만 있고 K에는 없다'는 **서명 필사본 두 부의 차이**를 가리킨다. **그 문장이 취리히시 인쇄본에서만 유통되었다는 뜻이 아니며**, 바젤 W2108에도 나타난다. 단, W2108이 Z를 직접 저본으로 삼았는지는 불명.
- **W2118의 한계:** 공식 기록의 `VD16 W2118 / Vischer C162`, e-rara 검색목록의 `Zwingli MvK A 81,8` 소장본 확인. DOI `https://doi.org/10.3931/e-rara-1085` 리다이렉트가 현 환경에서 접근되지 않아 제15조 지면 **미확인**. 이를 W2119와 직접 교감했다고 표시하지 않는다.
- **글자 단위 미완료:** 같은 의미를 확인한 것이지 2개 인쇄판의 **완전한 독일어 외교적 전사·철자/구두점 교감·사본 계통·PDF 파일 해시 확보**가 아니다. K/Z 실제 서명 원본 제15조와 1531/1540 라틴어 제10조 원본 지면도 여전히 미완료.
- **검증:** V4.64 신규 5개 및 기존 V4.63 회귀 5개를 GitHub 소스 기반 **V8 Node 로더 적응 실행**으로 **10/10 PASS**. Native `node --test` 및 GitHub Actions 실동작 성공은 아직 검증하지 않았다.

**원전 대조 보고서:** [V4.64 취리히·바젤 인쇄본 대조](./V464_ZURICH_BASEL_1529_PRINT_PARALLEL_REVIEW_KO.md)  
**본문 지면별 연구 데이터:** `research/data/ATLAS_V464_W2119_W2108_EARLY_PRINT_PARALLEL_ARTICLES_7_13_15.json`  
**감사 기록:** `research/data/ATLAS_V464_ZURICH_BASEL_DIRECT_ORIGINAL_PRINT_AUDIT.json`  
**계통표 실제 개정:** `research/data/ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json`  
**테스트:** `v464-early-print-parallel-contract.test.mjs`, 기존 `v463-original-print-witness-contract.test.mjs`.

**다음 핵심 연구:** W2118 원본 열람 및 동일 조항 대조를 먼저 시도하고, K·Z 서명 필사본 원문 15조와 1529년 인쇄계통이 어떻게 연결되는지 확정한다. `main`, AI Studio 운영 앱, 기존 통합 역사 원고 미변경, `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false` 유지.

## V4.65 — 취리히 W2118 직접 원본 판독: W2119와 인쇄자 콜로폰 차이 확인

V4.64에서 DOI 리다이렉트 오류로 **서지만 확인됐던 1529년 취리히 W2118**을 e-rara의 **실제 레코드 `291747`**로 찾아냈다.

- 원본 서지: **[e-rara W2118](https://www.e-rara.ch/zuz/content/titleinfo/291747)**, `VD16 W2118`, Vischer C162, `Zwingli MvK A 81,8`. **[원본 9쪽 PDF](https://www.e-rara.ch/zuz/download/pdf/291747)**, [IIIF manifest](https://www.e-rara.ch/i3f/v20/291747/manifest). e-rara 표제정보의 **Public Domain Mark**와 출처 표기 요청 확인.
- **W2118 실제 원본 인쇄 지면 판독:** PDF 0기준 p3–4 제7조, p5 제13조, p6 제15조, p7 서명자 목록. 제7·13·15조의 취리히 Z 추가문구에 대응하는 내용이 인쇄돼 있고 제15조는 성찬에 관한 공통 진술과 신체적 임재 방식의 미합의를 함께 기록한다.
- **W2119와 비교:** [기존 원본](https://www.e-rara.ch/zuz/download/pdf/170052), PDF p4 제7조, p5 제13조, p6 제15조, p7 서명면. **마지막 인쇄면의 콜로폰에 차이가 있다.** W2118 p7에는 인쇄된 서명자 명단 아래 인쇄자 표시가 없지만 W2119 p7에는 **취리히/크리스토프 프로샤우어 인쇄자 표시가 추가되어 있다.**
- **추론 범위:** 두 취리히 인쇄판의 **명제 내용 대응**과 **말미 인쇄표시 차이**는 실제 인쇄 지면으로 확인했다. 그 차이만으로 **인쇄 선후, 별도의 전체 조판, 공통 저본, 필사 Z/K와 동일성**은 확정할 수 없다. W2119에는 수기 라틴어 주석이 존재하나 그 내용과 작성자는 검증하지 않았다.
- **문헌 계통 실제 수정:** `ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json`의 W2118을 카탈로그 전용에서 **당대 인쇄 본문 직접 확인**으로 승격, W2119 콜로폰 정보도 별도로 추가. 과거 V4.64 당시 W2118 미열람 상태를 기록한 이력 데이터는 역사적 스냅샷으로 보존한다.
- **증거 상태:** 원본 PDF의 해당 지면은 화면으로 판독했으나 원본 파일을 저장하거나 SHA256을 확보하지 못했고, 정확한 활자·철자 전체 전사·전승 계보는 미완료. **K/Z 두 서명 필사본 제15조 및 1531/1540 라틴어 두 제10조 지면 = 여전히 0/4**.
- **회귀검증:** GitHub 원본 코드를 V8에서 Node 모듈 로드/파일 읽기만 대체한 적응 실행으로 V4.65 **5/5**, V4.64 **5/5**, V4.63 **5/5**, 합계 **15/15 통과**. **실제 `node --test`, GitHub Actions 및 역사 전문가 승인 성공은 확인되지 않았음**. 연구 CI에 별도 계약 테스트 추가.

**한국어 판본 대조 연구:** [V4.65 W2118·W2119 제15조와 콜로폰](./V465_W2118_W2119_ORIGINAL_1529_PRINT_COLOPHON_AND_ART15_KO.md)  
**지면별 구조화 근거:** `research/data/ATLAS_V465_ZURICH_W2118_W2119_DIRECT_ARTICLES_AND_COLOPHON_COMPARISON.json`  
**감사 기록:** `research/data/ATLAS_V465_W2118_W2119_ACTUAL_PRINT_VISUAL_INSPECTION_AUDIT.json`  
**회귀검사:** `v465-zurich-original-print-colophon-contract.test.mjs`

**다음 작업:** 인쇄본 세 종을 더 늘리기보다는 W2118/W2119의 실제 활자 배열 대조 → 서명본 **Z·K의 제15조 직접 교감**으로 집중한다. 별도로 1531 C4734/1540 C4713의 라틴어 제10조 직접 인쇄면을 확보한다. 전문가 서명·독자 실측·AI Studio 반영 전까지 `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`. `main`, 실제 운영 앱과 기존 역사 원고는 변경하지 않았다.

## V4.66 — W2118/W2119 인쇄 조판 **판정 보류** 및 학술판 저본 관계 정정

1529년 취리히 인쇄판 2종의 **서지상 독립성, V4.65에서 확인한 말미 콜로폰 차이**, 후대 학술판의 **정확한 저본(copy-text)**을 분리하였다.

- **새로 확정된 학술 자료 계통:** 취리히 주립문서보관소에 따르면 **『츠빙글리 저작집』 6/2권 제146번은 서명 필사본 Z가 아니라 인쇄판 `VD16 W2119`를 저본으로 사용**한다(`nach dem Druck VD16 W 2119`). 이에 비해 **2014년 루터교 자료집 43–46쪽은 K**, **개혁파 신앙고백집 1/1권 11번은 Z**, **MBW Texte 3, 825번은 K+Z 이문**을 사용한다. 앱용 저본 식별에서는 `EDITION_SOURCE`와 `AUTOGRAPH_MANUSCRIPT`를 자동 동일시하지 않는다.
- **현재 실행의 직접 원본:** W2119의 1529년 PDF 0기준 **6쪽 제15조, 7쪽 서명자·인쇄자 표시**를 다시 눈으로 확인. W2118의 PDF `291747`과 IIIF 리소스는 이번 실행에서 접근 실패해 **V4.65 관찰 내용으로만 이어받았음**. 따라서 W2118 지면을 V4.66에서 재판독한 것처럼 표시하지 않는다.
- **확인 수준 구별:** W2119에 프로샤우어 콜로폰이 있고 V4.65의 W2118 해당 지면에는 없는 **말미 인쇄 사항 차이**는 기록돼 있지만, 이를 **본문 전체가 별도로 조판됨 / 같은 활자판 사용 / 어느 인쇄가 먼저인지**의 증명으로 확장하지 않는다.
- **실제 텍스트 교감의 필요조건:** 두 판본의 이미지 바이트·SHA256, 정확한 활자 배열, 행끝 글자, 특이 조판 오류, 장의 서명표, 인쇄자 사항을 함께 비교해야 한다. 현재 원문 **줄·철자 완전 교감 0건**.
- **연구 방향 전환:** 이 단계 이후 1529 인쇄본 목록의 단순 확장을 중단하고, **서명 필사본 K/Z의 제15조 실제 이문 확보**를 우선한다. 이후 1531·1540년 아우크스부르크 신앙고백의 **제10조 실제 라틴어 인쇄 지면**을 대조한다.
- **검증:** `v466-print-setting-provenance-contract.test.mjs` 신규 6건의 GitHub 소스 기반 V8 실행 **6/6 PASS**. 이는 역사적 조판 차이를 완전 확정했다는 뜻이 아니며 GitHub Actions 원격 실행 결과도 아니다. 연구용 CI 설정에 동일 테스트를 추가했다.

**역사 연구보고서:** [V4.66 인쇄 조판 및 저본 판단](./V466_PRINT_SETTING_AND_CRITICAL_EDITIONS_COPYTEXT_KO.md)  
**기계 판정·출처 연결:** `research/data/ATLAS_V466_ZURICH_1529_PRINT_SETTING_AND_EDITION_COPYTEXT_GATES.json`  
**감사 기록:** `research/data/ATLAS_V466_PRINT_SETTING_AND_COPYTEXT_AUDIT.json`  
**계통표 실제 개정:** `research/data/ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json`

**릴리스:** `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`. 원고·main·실제 AI Studio 운영 앱 미변경. 역사학자 승인 및 실제 독자 파일럿 0건.

## V4.67 — 서명 원본 K/Z **공식 복제 확보 준비**와 실제 전사 승격 규칙

이 단계에서는 동일 시대 인쇄판을 계속 더 수집하는 대신, **1529년 두 서명 필사본 K·Z의 제15조 실물 확보를 위한 공식 연구 절차**를 문서화했다. 소장목록에 따른 Z 추가 문구 3건은 역사적으로 중요한 증거이나, 서명 필사본의 정확한 문자를 직접 읽은 것으로 기록하지 않는다.

- **원본 K:** `HStAM Best. 3 Nr. 245`, 헤센 주립문서보관소. [공식 연락처](https://landesarchiv.hessen.de/ueber-uns/hessisches-staatsarchiv-marburg) **marburg@hla.hessen.de**를 현재 안내에서 확인. HAPuls의 `Bl.60–63`와 취리히 서지의 `fol.60r–64v` 표기가 다른 문제를 보관소에 묻도록 했다. **Heinrich Heppe 1854**의 원본 파크시밀리 간행이 [Google Play](https://play.google.com/store/books/details/Heinrich_Heppe_Die_f%C3%BCnfzehn_Marburger_Artikel_vom?id=L2b7YTiIyLwC)에 무료 23쪽으로 등재된 사실도 확인했지만 해당 제15조 이미지를 직접 열지는 못했다.
- **원본 Z:** `StAZH E I 3.1 Nr.54`, 취리히 주립문서보관소. [공식 복제 신청](https://www.zh.ch/de/politik-staat/recherche-im-staatsarchiv/reproduktionen-bestellen.html)은 **서명된 신청서, 정확한 소장번호, 이용/비용 확인**을 요구하며, **staatsarchivzh@ji.zh.ch**를 안내한다. 우스테리 **1883년 파크시밀리 409–413쪽** 및 Z 저본의 개혁파 신앙고백 비판판 정보를 재연결했다.
- **새로 확인한 교감 참고서:** Wolf-Friedrich Schäufele 편, `Die Marburger Artikel als Zeugnis der Einheit`(Leipzig, 2012), **13–29쪽**에 'Faksimile–Transkription–Übertragung' 장이 존재함을 ETH 도서관 [목차](https://toc.library.ethz.ch/objects/pdf/z01_978-3-374-03080-4_01.pdf)에서 확인했다. **해당 장 전문을 판독한 것은 아님**.
- **실제 실행 가능한 산출물:** 원본 K/Z 보존소에 보내는 **독일어 연구 문의서 초안 2건**, 신청·비용·저작권·지면 요구사항을 갖춘 구조화 소장·확보 데이터, 기존 V4.62의 4개 원본 확보 게이트와 연동.
- **검증:** 신규 `v467-kz-autograph-acquisition-contract.test.mjs` 6개 + 기존 `v462-primary-source-evidence-contract.test.mjs` 5개를 GitHub 원본의 V8 적응 실행으로 **11/11 PASS**. 네 원본 직접 판독 지면 0/4, 그중 K/Z 서명본 0/2, 기관 메일 발송 0건. Native `node --test`/실제 GitHub Actions 성공은 별도 확인되지 않음.
- **안전 경계:** 서명받은 신청서·개인 연락처·기관 제공 이미지/회신을 **공개 GitHub에 자동 업로드하지 않음**. 이미지 재사용 조건과 비용은 기관 협의, 유료 복제 주문은 명시적 승인 후만 진행.

**독일어 공식문의 초안 및 한국어 연구 프로토콜:** [V4.67 K·Z 원본 확보 실행 패키지](./V467_KZ_AUTOGRAPH_SOURCE_ACQUISITION_AND_GERMAN_REQUESTS_KO.md)  
**자료·문의 구조화 데이터:** `research/data/ATLAS_V467_KZ_AUTOGRAPH_ARCHIVE_ACQUISITION_AND_SOURCE_GATES.json`  
**기존 원본 확보 게이트 연결:** `research/data/ATLAS_V462_FOUR_PRIMARY_FOLIO_IMAGE_ACQUISITION_REGISTER.json`  
**감사:** `research/data/ATLAS_V467_KZ_ARCHIVE_SOURCE_ACQUISITION_QA_AUDIT.json`

**다음 실질 단계:** K와 Z 각각의 **제15조 원본 사진 또는 신뢰할 만한 파크시밀리 원문 지면을 직접 확보**, 실제 필사 문장을 독립적으로 전사·교감한 뒤 전문가 검토. 별도 1531·1540 라틴어 제10조 인쇄면 연구도 미완료. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`; `main`, 기존 역사 원고 및 AI Studio 운영 앱 미변경.

## V4.68 — K/Z 원본 연구 문의 **Gmail 저장 확인** 및 헤페 출판연도 검증 보류

- **실제 Gmail 작업 완료:** 헤센 `HStAM 3 Nr245`와 취리히 `StAZH E I 3.1 Nr54`의 **1529년 서명본 K/Z 제15조** 촬영·디지털 열람·복제비·재사용 조건을 묻는 독일어 메일 2건을 연결된 Gmail **임시보관함에 저장**했고, 목록 조회로 **두 건 모두 존재함을 확인**했다. **메일 발송 0건, 유료 복제 주문 0건, 기관 회신 0건**.
- **개인정보 제한:** 공개 GitHub에는 공식 기관 수신 주소와 요청 상태만 기록하며 Gmail 개인 계정, 임시보관 메일 ID, 발신인 이름, 메시지 내부 개인 연락처는 저장하지 않는다. **사용자가 검토·승인하기 전에는 발송하지 않음**.
- **공개 파크시밀리 재조사:** 헤페의 `Die fünfzehn Marburger Artikel` Google Play 무료 전자책은 **1854년, 23쪽**으로 표시된다. 그런데 **1847년 당시 `Leipziger Repertorium`의 목록 198번은 Kassel Fischer, 20쪽+석판 4장**의 헤페 파크시밀리를 기록한다. 이 두 연도의 서지 연결은 표제지/실물을 직접 열지 않았으므로 **동일 판본·재판·오기 어느 것도 확정하지 않는다**. 1847년 PDF 이미지 캡처는 대용량·응답 시간 초과로 실패했으며 문헌목록의 검색 가능한 텍스트를 단서로만 사용한다.
- **실제 필사본 판독 상태:** K/Z **원본 제15조 0/2건**, Usteri 1883 취리히 파크시밀리 409–413쪽 실제 지면 미열람. 헤센 Arcinsys 뷰어의 제15조 이미지도 미판독. 기존 당대 인쇄본 W2118/W2119/W2108의 본문 확인과 구별.
- **검증과 상태:** 신규 `v468-kz-gmail-draft-and-early-facsimile-contract.test.mjs`의 GitHub 원본 자바스크립트 검증 조건 **5/5 PASS**(V8의 Node 로더 적응 실행). 실제 `node --test` 또는 GitHub Actions 성공은 아직 확인하지 못했다. 연구 CI에 V4.68 JSON/검사 경로 연결.

**한국어 실행보고서:** [V4.68 기관 문의 초안 저장·파크시밀리 서지 점검](./V468_KZ_ARCHIVAL_GMAIL_DRAFTS_AND_FACSIMILE_EDITION_YEAR_AUDIT_KO.md)  
**구조화 작업 감사:** `research/data/ATLAS_V468_KZ_GMAIL_DRAFTS_AND_ORIGINAL_FACSIMILE_ACCESS_AUDIT.json`  
**회귀 검사:** `v468-kz-gmail-draft-and-early-facsimile-contract.test.mjs`.

**다음 필수 절차:** 사용자가 Gmail의 두 독일어 초안을 검토하고 명시적으로 발송 승인하면 기관에 문의할 수 있다. 또는 제공받은 **K·Z 제15조 실제 필사 스캔/허가된 팩시밀리**가 있다면 먼저 직접 판독한다. 받은 적 없는 원본 이미지는 만들어 내지 않고, 승인받지 않은 유료 복제는 주문하지 않는다.

**릴리스 차단:** `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`; `main`, 기존 역사 통합 원고, 실제 AI Studio 운영 앱 미변경.

## V4.69 — 헤페 1847/1854 출판연도 충돌·1909년 교감 논쟁 연구사 보강

- 1847년 *Leipziger Repertorium* No.198, 당대 출판 광고, *Serapeum* 8(1847) 제81항의 **문헌 텍스트를 추가 대조**하여 헤페 마르부르크 조항 파크시밀리의 **1847년 존재 기록**을 여러 출처로 보강했다. 그러나 원본 책 표제면은 미확인, 대용량·시간 초과로 PDF **이미지 직접 판독 실패**.
- Google Play 1854년·23쪽 기록은 **별도 카탈로그 정보**로 보존. 1847 Kassel/Fischer의 20쪽·석판 4면 기술과 **동일판·재판·목록오류 여부 미확정**.
- Hans von Schubert의 1909년 연구(361쪽)는 K 결락을 근거로 추가 구절을 비진정하게 본 헤페 해석에 대해 Z 원본의 추기 사실로 반박한다. 이 주장은 **후대 역사학자의 해석**이지 연구자의 K/Z 서명본 직접 판독이 아니다.
- 헤센·취리히 Gmail 문의 2건은 **계속 미발송**. 사용자 명시 승인, 원본 사진, 역사학자 승인, 독자 실증 없음.
- 신규 연구 JSON·본문·5개 회귀 테스트 추가. **테스트 코드 신규 실행 결과는 별도 확인 전까지 미확인**. `main`, 역사 원고, 실제 AI Studio 앱 변경 없음.

**연구 보고서:** [V4.69 헤페 서지 충돌과 마르부르크 교감 연구사](./V469_HEPPE_1847_1854_BIBLIOGRAPHY_AND_KZ_INTERPRETATION_KO.md)  
**JSON:** `research/data/ATLAS_V469_HEPPE_BIBLIOGRAPHY_AND_MARBURG_VARIANT_HISTORIOGRAPHY.json`  
**회귀 코드:** `v469-heppe-bibliography-and-textual-history-contract.test.mjs`

**다음 우선:** 검토된 K·Z 문서보관소 초안에 대해 명시적 발송 승인 여부 결정 또는 합법적으로 이용 가능한 원본 스캔/파크시밀리 확보 후 실제 제15조 전사. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`.

## V4.70 — 1529년 W2119 실물 인쇄 제15조와 GHDI 영어 번역의 저본 차이를 활용한 L0/L1 연구 원고

- W2119 **1529년 취리히 인쇄 원본 PDF p6·p7을 이번 세션에서 직접 화면으로 재확인**했다. 제15조의 **미사-타인 은총 관련 문장**, 성찬에 관한 공동진술·현존 방식 미합의와 p7 **프로샤우어 콜로폰**을 구별해 기록했다.
- GHDI 편집 영어 번역 **제15조에는 해당 미사 구절이 나타나지 않음**을 원문 영어 본문과 비교했다. GHDI는 **WA 30 III (1910), pp160–171**을 저본으로 명시. 이것만으로 K/Z의 필사본 계통이나 추가문구 작성 시기를 **확정하지 않는다**.
- Philip Schaff의 역사 문헌목록은 헤페 파크시밀리의 **1847년 출판 + 1854년 제2판**을 명시. 그러나 두 책의 **실제 표제지/판권면 미검증**이라는 제한을 남긴다.
- 연구용 **L0 독자 개요 + L1 심화 해설 + 사료 카드 6종 + 검토 주장 6건 + 독자 질문 3건**을 새 문서와 JSON으로 작성했다. 실제 역사 본문이나 Google AI Studio에 승격하지 않았다.
- 사용자가 승인하지 않은 Gmail 발송 **0건**. K/Z 원본 직접 교감 미완료, 역사학자 승인 0, 실제 독자 평가 0. **추가 검증 코드 5개**를 연구 CI에 연결한다.

**[V4.70 실질적 독자용 L0/L1 역사 원고 후보](./V470_MARBURG_1529_READER_COPYTEXT_DIFFERENCES_KO.md)**  
데이터: `research/data/ATLAS_V470_W2119_ART15_TRANSLATION_GAP_AND_HEPPE_EDITION_CANDIDATE.json`  
검사: `v470-reader-copytext-and-bibliographic-contract.test.mjs`.  
**계속 보류:** `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`.  
**다음:** V4.71의 주장별 근거-문장 검토 및 실제 전문가/독자 평가 준비. K/Z 두 기관 메일은 사용자 검토·승인 없이는 발송하지 않는다.

## V4.71 — V4.70 L0/L1 29문장 출처·전문가 검토 연결, 독자 파일럿 자료 정비

- V4.70 **L0 8문장 + L1 21문장 = 29문장**을 원문 그대로 분리해 각 문장에 실제 선행 사료 카드 및 V4.57/V4.70 주장 ID를 연결했다. 연구용 JSON에서 사료별 증거 수준과 전문가 판단 미완료 상태를 보존한다.
- 즉시 수정 제안은 **4문장**(주관적 난도, '널리 읽히는' 근거 과잉, 번역 저본 인과 추론, 인쇄/필사 구별의 시대착오적 비유). V4.70 자체와 역사 원고는 **수정하지 않고** 후보만 생성했다.
- 기존 **3과제·9문항**과 오프라인 채점 기준을 그대로 유지하고, 정답 없는 참가자용 안내지 및 **비채점 추가 확인 질문 3건**을 준비했다. 공개 저장소의 기존 평가 JSON에 정답이 있다는 점을 명시하여 실제 블라인드 평가로 과장하지 않는다.
- 역사학자 0명, 독자 0명, 문의 발송 0건; **전문가 검토 요청과 독자 모집은 실행하지 않았다.**

**[V4.71 연구·전문가 검토 패키지](./V471_HISTORIAN_SENTENCE_LEVEL_REVIEW_PACKAGE_KO.md)**  
**[독자 참여 안내지(정답 제외)](./V471_READER_PARTICIPANT_HANDOUT_KO.md)**  
데이터: `research/data/ATLAS_V471_SENTENCE_PROVENANCE_AND_REVIEW_KIT.json`  
테스트: `v471-sentence-provenance-and-review-contract.test.mjs`.  
**출시 상태:** `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`.

**V4.72 권장:** 검토대상 4문장을 포함한 **별도 역사 해설 개정 후보**를 편집하고, 출처 대조와 전문 검토 기록이 축적되기 전에는 공개 앱으로 승격하지 않는다.

## V4.72 — 제4권 마르부르크 독자용 L0/L1 역사 해설 개정본(연구 초안)

- 이전 V4.70 원고·V4.71 문장별 검토 원장을 **그대로 보존**하고, 새 L0 3문단과 L1 6절을 실질적으로 편집하였다. V4.71에서 우선 표시한 4개 과잉표현은 수정하고 정치·신학·문헌 저본·서지·후속 연관성 등 **5개 해설 구조 보강**을 수행했다.
- GHDI 합의문과 루터교 측 오시안더 목격담, W2119 인쇄 원본 제15조, Z/K 보관소 목록, Schaff의 서지 진술, Gruber 소장목록을 각기 다른 사료 유형으로 연결했다. **원전 미검증 지면을 직접 판독했다고 승격시키지 않는다**.
- 검토용 L0/L1 연구 본문에 명확한 사료 ID[GA/GE/WP/ZA/SC/GR]를 부착했다. 구판의 판본 연도·본문 차이 등은 증거 한계를 포함한 새 문장으로 통합.
- **새 연구 JSON**: `research/data/ATLAS_V472_MARBURG_REVISED_READER_CANDIDATE_AND_REDLINES.json`; **5개 Native Node 시험 정의**: `integrations/atlas-flagship-phase1/v472-editorial-revision-evidence-contract.test.mjs` (실제 실행 결과는 별도 확인 필요).
- 역사학자 0명·독자 0명·K/Z 직접 대조 미완료·메일 발송 0건·운영 AI Studio 앱 변경 없음. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`.

**[V4.72 L0·L1 전체 수정 원고](./V472_MARBURG_1529_L0_L1_REVISED_READER_CANDIDATE_KO.md)**  
**[V4.72 수정 대조 및 전문가 검토 의제](./V472_EDITORIAL_REDLINES_AND_EVIDENCE_DECISION_KO.md)**

**다음 V4.73:** 별도의 연구용 미리보기에서 이 개정본과 사료 카드 연결을 평가하고, 실제 역사학자·독자 검토의 결과를 수집하기 전에는 배포하지 않는다.

## V4.73 — V4.72 실제 읽기 화면 연결 및 CI 실패 원인 진단·복구

- [**V4.73 독립형 연구 HTML**](./preview-v473-1529-1540.html): V4.72 **L0 3문단 / L1 6절 전체를 실제 표시**, 연표 4개, 사료 6개, **W2119-GHDI-K/Z 3행 증거 비교** 제공. 기존 원고·구형 시범 HTML 및 운영 AI Studio 앱은 불변.
- 기존 [Actions #44724441589](https://github.com/worldinyj/REFORMATION-ATLAS/actions/runs/44724441589) 실제 로그에서 **81/82 연구 계약 테스트 통과(오래된 W2118 URL assertion 1개 실패)**, 두 브라우저는 **Ubuntu 26.04/Playwright 비호환으로 실행 전 실패** 확인.
- V459 회귀검사에 공식 e-rara **291747 서지 URL + DOI permalink + 실제 PDF**를 분리 검증, Actions 러너 **ubuntu-24.04** 고정.
- 신규 **V473 Node 계약 5건 + Chromium/WebKit 각 320/375/768/1440px 브라우저 시나리오** 연결. 실제 CI 성공 여부는 실행 결과 확인 전에는 미확인.
- **[검증·진단 보고서](./V473_REVISED_READER_PREVIEW_AND_CI_RECOVERY_KO.md)**, JSON `research/data/ATLAS_V473_PREVIEW_SOURCE_BRIDGE_AND_CI_TRIAGE.json`; 출시 관련 모든 게이트는 닫힘.

## V4.74 — 기존 React 연구 컴포넌트에 V4.72 전체 L0/L1 + 사료 증거 카드 연결

- [**V4.74 React 연구 화면 통합 보고서**](./V474_REACT_READER_AND_BROWSER_INTEGRATION_KO.md): V4.73 정적 HTML에서 이미 표시했던 **V4.72의 L0 전체·L1 6절과 사료 6종**을 이제 `AtlasFlagship1529Panel.jsx`에서도 전달받아 실제 화면에 표시할 수 있다.
- 기존 `readerPack=null` 호환을 유지하면서, 유효한 `readerPack`을 받은 경우에만 **3행 W2119/GHDI/K·Z 비교표, 각 사료 카드의 유형·한계·공식 링크, 근거 ID 링크**를 보인다. 공개 저장소 파일은 비공개 서버 접근제어가 아님을 명시.
- 데이터: `research/data/ATLAS_V474_REACT_READER_PACK.json`. 기존 판본/역사 원문 수정 없이 V4.73 원고 정확성 연결을 검증하는 **5개 계약 테스트** 추가.
- **실제 React DOM**은 `esbuild`+ `react-dom`으로 구축한 검사용 fixture와 Playwright Chromium/WebKit·320/375/768/1440px로 검증하고, 접근 미승인/연구패키지 변조 시 차단하는 음성 테스트를 수행한다.
- 실제 CI 성공 여부는 신규 커밋 후 확인. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`. 인간 전문가 승인 0, 독자 0, 실제 운영 앱 미반영.

## V4.75 — 전문가·독자 검토 패키지 및 8권 공통 콘텐츠 계약

- V4.74의 기술 검증된 제4권 화면을 기반으로 **L0/L1 전체·4사건·6사료·3문헌 증거 비교·14 역사 주장·3과제·9문항**을 하나의 [공통 검토 데이터셋](../../research/data/ATLAS_V475_CROSS_VOLUME_REVIEW_BUNDLE.json)으로 통합했다. HIGH 역사 주장 10건은 독립 2인 검토를 요구하며 현재는 모두 미승인.
- [**역사학자 검토 자료집**](./V475_HISTORIAN_SOURCE_REVIEW_DOSSIER_KO.md)에는 출처 유형·한계, 14개 주장 목록, HIGH 10건, 필사본 K/Z 미확정, 판본/서지 쟁점, 실제 전문가 검토용 빈 판정 기록을 담았다.
- [**독자용 A4 인쇄 HTML (정답 없음)**](./V475_READER_PILOT_WORKSHEET.html)에는 기존 3과제·9문항 전체와 비채점 질문 3건, 자발적 참여 안내를 포함. 사료 카드 2개를 전제로 했던 Q09를 현재 6종에 맞게 수정했다. **키/응답/스크립트/전송/추적 없음**. 구형 공개 V4.57 파일에 정답이 있어 진정한 블라인드 평가가 보장되지 않는 위험을 표시했다.
- [**다른 권 재사용 표준**](./V475_CROSS_VOLUME_CONTENT_REVIEW_STANDARD_KO.md)에서 ID, L0/L1, 사료, 이본, 주장, 전문가/독자 평가, 출시 게이트를 정의. `atlas-review-bundle-contract.mjs` 검증 모듈 및 Node 계약 10개+ 실제 브라우저 새 시나리오 추가(테스트 성패는 Actions 결과 참조).
- [**V4.75 종합 보고서**](./V475_EXPERT_READER_REVIEW_READY_REPORT_KO.md). 인간 역사학자 검토/독자 평가/기관 이메일 발송/운영 앱 배포 **0건**. `can_ship=false` · `can_merge_main=false` · `can_import_ai_studio=false`.
