# REFORMATION ATLAS — 실제 앱 연계 Phase 0 점검 결과 및 첫 적용 설계

> 2026-11-18 · GitHub 소스 직접 확인 / 실제 AI Studio 앱 미접속 · **비공개 스테이징 설계안일 뿐 운영 앱 수정 아님** · `can_ship=false`

## 1. 출발점 — 어디까지 실제로 있는가?

| 구분 | GitHub에서 확인한 사실 | 판단 |
|---|---|---|
| **저장소 기본 상태** | 저장소 `worldinyj/REFORMATION-ATLAS`는 **Public**. 기본 `main` 브랜치에는 `README.md` 1개뿐 | 연구 브랜치와 별도 실제 앱의 빌드·배포 체계를 하나로 생각하면 안 됨 |
| **실제 AI Studio 앱** | 이 저장소에서 실제 Google AI Studio Build 앱의 프로젝트 ID·라우터·소스 전체 및 런타임을 확인하지 못함. V4.31 README도 해당 앱의 소스가 없다고 명시 | 실제 앱 설치·수정·화면 검증 **미실시** |
| **기존 앱 연계 후보** | `integrations/atlas-l0-v430/bridge.mjs` 읽기 전용 브리지와 `integrations/atlas-l0-v431/AtlasL0Panel.jsx` React 후보 존재 | 교체 대상이 아니라 활용할 후보 |
| **이미 확보한 화면** | V4.51 한 파일짜리 L0↔L1 HTML (8권·24장·16문항) | 독립 시범본. 실제 AI Studio 앱의 UI는 아님 |
| **L0 앱 계약** | V4.29: 8권, 6주제, 42개의 논리적 연결, 입문 6장, `publicationState=BLOCKED` | 안정된 ID 계약 기준으로 보존 |
| **연구 심화 내용** | V4.47 L0 8권, V4.50 L1 24장 / 본문 15,031자 | 모두 연구 초안. 역사 전문가 승인 없음 |
| **지도** | `assets/maps/`에서 제3권의 편집 가능한 자체 제작 SVG 4종과 후보 2종 확인 | 현대 참조 좌표는 `coordinates_verified=false`이므로 공개 역사 지도로 승격 불가 |

### 실제로 발견한 가장 큰 연계 문제 — V4.29와 V4.47은 같은 원고가 아니다

두 데이터셋은 `VOL-01`부터 `VOL-08`까지 동일한 **권 ID**를 사용하지만, **8권 모두 제목과 본문이 다르다.** V4.29은 L0 스테이징 패키지이고, V4.47은 새로 집필·개정한 연구 원고다. 이 때문에 기존 앱의 `getVolume("VOL-04")`가 가리키는 문장을 V4.47 새 문장으로 자동 대체하면 **편집 승인이 없는 콘텐츠 업데이트**가 된다.

1. 지금 쓰는 앱의 공개·비공개 경로와 실제 버전을 먼저 확인한다.
2. ID와 구조만 연결해 두되, **V4.29 본문은 잠금**으로 취급한다.
3. V4.47 L0과 V4.50 L1은 별도 **연구용 읽기 계층**에서만 표시한다.
4. 편집·역사 검토를 마친 항목만 해당 앱의 비공개 테스트 대상으로 승격한다.
5. 실제 앱 호스트의 접근 제어를 검증하지 않았다면 원고 JSON을 일반 공개 JS 번들에 넣지 않는다.

참고: `can_ship=false`는 UI와 데이터의 출시 승인 상태일 뿐 **GitHub 공개 권한을 차단하는 기능이 아니다.** 현재 Public 저장소의 모든 공개 브랜치에 있는 연구 텍스트는 외부에서 열람할 수 있다. 비공개가 필요한 자료를 계속 다룬다면 별도의 private 저장소 또는 접근 제어를 갖춘 스테이징 환경이 우선이다. 권한 설정은 이번 작업에서 변경하지 않았다.

## 2. 이번에 실제로 만든 연계 산출물

| 파일 | 목적 |
|---|---|
| `research/data/ATLAS_PHASE0_APP_GITHUB_STATUS_AND_VERSION_GAP_20261118.json` | 실제 GitHub 자산·버전 차이·접근 위험을 확인한 원천별 점검표 |
| `integrations/atlas-l1-phase0/bridge.mjs` | V4.29·V4.47·V4.50을 **내용 동기화 없이** 묶는 읽기 전용 L0/L1 연구 어댑터 |
| `integrations/atlas-l1-phase0/bridge.test.mjs` | 8권/24장/6주제/42연결/6입문·비공개 모드·부정 사례 단위시험 7종 |
| `research/data/ATLAS_PHASE0_FLAGSHIP_SCENE_1529_1540_PRIVATE_MODEL.json` | 마르부르크 1529 → 아우크스부르크 1530·1531·1540의 사건·판본·자료 카드 **첫 종단형 학습 장면 모델** |

읽기 전용 어댑터는 원고를 재작성하지 않고 정확한 ID로 접근한다. `getVolume`, `getChapter`, `getTheme`, `getIntroChapter`, `resolve`, `search`를 제공한다. 로컬 연구 모드 외에는 생성 자체를 거부하고, 모든 반환 데이터에 `canShip=false`를 유지한다. 이 플래그가 사용자 인증을 구현한다는 뜻은 아니다.

사용 예시:

```js
import { createAtlasResearchReadOnlyBridge } from "./integrations/atlas-l1-phase0/bridge.mjs";

// 입력 자료는 외부 접근 통제가 끝난 개인 검토 환경에서만 전달한다.
// 브라우저에서 공개 GitHub 원본을 자동 fetch 하지 않는다.
const bridge = createAtlasResearchReadOnlyBridge({
  frozenStagingPackage: v429,
  researchOverview: v447,
  researchIntermediate: v450
}, {mode:"LOCAL_RESEARCH_PREVIEW"});

const overview = bridge.getVolume("VOL-04");     // V4.47의 연구용 개요
const deeper = bridge.getChapter("L448-04-02");  // V4.50 심화 장
const documentTheme = bridge.getTheme("T415-03");
const hits = bridge.search("마르부르크");

// 세 계층의 출처 버전과 본문이 달라진 사실은 메타데이터로 구분.
// 실제 AI Studio로의 import는 이 코드만으로 이루어지지 않는다.
```

**보안 주의:** 위 코드는 자료 조회를 돕는 데이터 계층이다. 호스트 애플리케이션의 사용자 로그인·서버측 접근 제한이 없으면 JSON 내용을 공개하고 있다고 간주해야 한다.

## 3. 첫 번째 종단형 대표 사례 — 1529~1540년 문헌 탐색

### 독자 동선

`제4권 L0 개요` → `L1 제4권 제2장` → `1529~1540 연표` → `마르부르크 15개 조항·신앙고백 판본 카드` → `사료 종류와 미해결 부분 비교`

| 구간 | 사실·문헌의 층위 | 사료 출처 |
|---|---|---|
| **1529 · 마르부르크** | 앞선 공통 조항과 성찬의 남은 이견을 함께 설명 | [German History Documents: Marburg Articles](https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/the-marburg-colloquy-the-marburg-articles-1529) |
| **1530 · 아우크스부르크** | 제국회의에서 제출한 신앙고백과 인쇄 출판물 분리 | [Gruber Rare Books](https://gruber.lstc.edu/confessions/augs_apol.php) |
| **1531 · 인쇄본** | 신앙고백·변증서 및 편집판의 별도 서지 | 같은 희귀본 소장목록 |
| **1540 · 수정 이본** | Variata와 같은 해 비Variata 인쇄물을 구별 | 같은 희귀본 소장목록 |

장면에는 **정확 지도를 가장한 역사적 이동 경로와 국경선은 넣지 않았다**. 마르부르크·아우크스부르크라는 장소 이름과 연도까지만 표시하며, 장소별 좌표·당시 영토 경계·실물 책 이미지 권리 확인은 후속 연구 항목으로 유지한다. 이벤트/문헌 모델은 연구 전용 데이터이며 실제 앱에 설치하지 않았다.

## 4. 현재 앱을 연결할 때 필요한 검증 순서

**A. 실제 앱 구조 파악:** Google AI Studio Build의 실제 앱 소스 또는 연결된 별도 저장소를 확인해 React 버전, 라우팅, 콘텐츠 로더, 인증, 렌더링 방식, 기존 지도/검색 기능을 확인한다. 이 정보 없이 `App.tsx` 같은 경로를 상상해 수정하지 않는다.

**B. 비공개 미리보기 구성:** 현재 앱의 디자인을 유지하고, 기존 V4.31 컴포넌트를 교체하지 않은 상태로 새로운 L1 읽기 탭을 연계한다. 단, 실제로 접근제어된 환경을 먼저 확보해야 한다. V4.29를 삭제하거나 V4.47을 자동 대체하지 않는다.

**C. 첫 세로 통합:** 제4권 1529~1540년의 **하나의 사례**에서 L0→L1→연표→문헌 근거 카드가 연결되는지 검증한다. 기존 8/6/42/6 ID 계약은 불변으로 유지한다.

**D. 기능 수락:** 실제 앱에서 데스크톱/모바일의 탐색·검색·서지 링크·뒤로 가기, 검증보류 표시, 외부 미인가 사용자의 콘텐츠 차단을 확인한다. 정확한 위치 정보가 확보되지 않은 지도는 지도처럼 표현하지 않는다.

**E. 독자·전문 검토:** 역사 전문가 서면 검토와 실제 독자 관찰이 완료된 해당 콘텐츠 단위만 따로 승인 판단한다. 고위험 `C417-11`, `C417-12`, `C417-18`, `TAMIL-1719` 보류는 계속 유지한다.

## 5. 완료 기준 및 다음 대규모 작업

Phase 0의 성과는 **앱과 연구 원고가 동일한 것이 아님을 실제 소스 기준으로 식별하고, 그 차이를 무시하지 않는 읽기 전용 연결 모델을 만든 것**이다.

다음 실제 제품 작업은 **현재 별도 AI Studio Build 앱의 소스/기능 조사**와 **제4권 첫 역사 장면을 비공개 UI에 붙여 동작 테스트**하는 것이다. 실제 앱 소스가 연결되기 전에는 GitHub 연구 후보를 운영 앱에 적용했다고 주장하지 않는다.

**현재 상태: 연구용 어댑터 작성·검증 / 실제 앱 수정 0 / 실제 사용자 테스트 0 / 외부 역사학자 승인 0 / `can_ship=false`.**
