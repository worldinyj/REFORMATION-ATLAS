# 종교개혁 ATLAS V4.30 — 비공개 L0 읽기 전용 런타임 브리지

> **실제 원고 8권 + 주제 6개 + 입문 6장면 + 연결 42개**를 소비하는 프레임워크 독립 ES 모듈. `canPublish=false`.
>
> **현재 상태:** GitHub 연구 브랜치의 실사용 가능한 모듈·단위 테스트. **Google AI Studio의 실제 앱에 연결하거나 배포한 것은 아니다.**

## 무엇이 새로 달라졌는가

기존 V1.66 읽기 전용 어댑터는 당시의 10개 심화 페이지·11개 도시·판본·증거 카드용이었다. V4.29의 새로운 **8권 L0 상위 역사 본문**은 구조가 달라 기존 어댑터를 그대로 재사용할 수 없다. V4.30은 V4.29 인계 JSON을 실제로 파싱하고, 앱이 호출할 수 있는 `getVolume`, `getTheme`, `getChapter`, `resolve`, `search`를 제공한다. 판본·이미지·지도는 호출하지 않는다.

| 구성 | 파일 | 역할 |
|---|---|---|
| 앱 데이터 | [V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json](../../handoff/V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json) | 원본 역사 원고 전문과 링크 |
| 읽기 전용 API | [bridge.mjs](./bridge.mjs) | 데이터 무결성·비공개 상태 검사 후 읽기 API 제공 |
| TypeScript 타입 | [bridge.d.ts](./bridge.d.ts) | 실제 앱에서 활용할 데이터 모델·라우트 타입 |
| 회귀 시험 | [bridge.test.mjs](./bridge.test.mjs) | 정상 콘텐츠·탐색·검색·부정/공개 시나리오 자동검사 |

이 브리지는 V4.28 시제품의 별도 HTML을 복제하지 않는다. **별도 AI Studio 앱이 기존 디자인을 유지하며 콘텐츠를 가져갈 수 있도록** 화면과 데이터를 분리했다.

## 기존 앱에서 사용하기

앱의 기존 소스 구조와 라우팅을 먼저 확인한다. 기존 앱 코드를 임의로 덮어쓰지 않고, 별도 비공개 개발 브랜치에 JSON·모듈 파일을 복사한다. 다음은 로컬 비공개 환경의 사용 예다.

```js
import content from "./V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json";
import { createAtlasL0ReadOnlyBridge } from "./bridge.mjs";

// 이 플래그는 실제 인증 검사를 수행하지 않는다.
// 앱이 로그인·권한을 독립적으로 검증한 뒤에만 선언해야 한다.
const atlas = createAtlasL0ReadOnlyBridge(content, {
  environment: "PRIVATE_STAGING",
  accessControlDeclared: true
});

// 화면과 분리된 읽기 API
const catalog = atlas.catalog;                        // 8권·6주제·6장면
const volume = atlas.getVolume("VOL-03");              // 실제 역사 원문
const theme = atlas.getTheme("T415-06");               // 실제 비교 원문과 시대권 7개 링크
const next = atlas.resolve({kind:"VOLUME",id:"VOL-07"}); // 존재하는 ID로만 이동
const hits = atlas.search("후스", {limit: 10});         // 전체 본문 검색
```

**주의:** 이 예제 코드의 `accessControlDeclared:true`는 실제 사용자 인증·접근제어를 대신하지 않는다. 테스트 스테이징도 **서버·호스팅 쪽에서 비인가 접근을 차단**해야 한다. 공개 JavaScript 번들에 JSON이 들어간다면 앱 경로의 비공개 표시만으로 원고 접근을 차단했다고 볼 수 없다.

앱의 마크다운 표시기는 **본문의 HTML을 안전하게 이스케이프/정화하고** 제목·단락·강조만 렌더링해야 한다. 본 모듈은 원문 마크다운을 반환할 뿐, 신뢰되지 않은 문자열을 직접 `innerHTML`에 주입하지 않는다.

## 읽기 모형과 ID 계약

제1~7권은 시간 순으로 진행되지만 **VOL-08은 별도의 시대가 아니라 주제 아카이브**다. 여섯 주제 `T415-01`~`T415-06`은 각각 일곱 역사권으로 연결되며, 42개 링크는 **논리적 ID**일 뿐 실제 심층 문헌 페이지 URL이 아니다. `getVolume/getTheme/getChapter`는 없는 ID에 대해 `null`을 반환하고, `resolve`도 존재하지 않는 경로를 만들지 않는다.

화면 소비자에게 반환되는 문장은 V4.29의 `bodyMarkdown`과 정확히 동일하다. 읽기 모형에는 전문가 검토 상태·비공개 채점 정답·보류된 주장 ID·외부 이미지 URL이 포함되지 않는다. 출처 연구 파일과 편집 메모는 별도 보존하고 원고에 대한 전문가 검토 없이 페이지를 공개하지 않는다.

## 실패 시 기본 차단 정책

모듈은 비공개 환경 선언 누락, `canShip=true`, 공개 색인 가능, 심사 완료 허위 표시, 권·주제 수량 누락, 중복 ID, 틀린 연결, 원문 내 임베드 이미지·액티브 HTML·독해 평가 정답 ID 등에서 **예외를 발생시킨다**. 통과할 때에도 반환하는 `canPublish`와 `canMergeMain`은 항상 `false`다.

브리지는 파일·네트워크·DB·쿠키·로컬 스토리지를 읽거나 쓰지 않는다. **실제 AI Studio 운영 라우터나 서버 인증을 직접 변경하지 않는다.**

## 재현 가능한 자동검증

저장소의 V4.30 연구 브랜치를 로컬에 받아 다음을 실행한다.

```bash
node --test integrations/atlas-l0-v430/bridge.test.mjs
node research/tests/v429_staging_import_contract.cjs
```

첫 시험은 **실제 V4.29 인계 JSON**을 로드하여 데이터 소비·검색·42개 연결·금지 상태에 대한 부정 테스트를 수행한다. 두 번째 시험은 20개 원문과 V4.23 원본이 바이트 단위로 같은지, V4.28의 Chromium/WebKit 실제 테스트 보고서가 236/236씩 통과했는지를 별도로 확인한다. 이 두 종류의 시험은 **AI Studio 앱의 실제 스테이징 테스트 결과가 아니다.**

GitHub Actions 워크플로는 이 연구 브랜치에서 실행 후 테스트 로그와 결과 JSON을 연구 아티팩트에 보존한다. 앱에 실제 연결된 뒤 별도의 인증·320/375px 화면·검색·접근성 E2E를 수행해야 한다.

## 다음 통합 단계 (승인 필요)

V4.30 브리지와 V4.29 JSON을 현재 Google AI Studio Build 앱의 **복제된 비공개 스테이징**에서 import하고, 현재 앱의 실제 라우터/데이터 구조에 매핑한다. 앱 소스·스테이징 URL이 이 저장소에 없으므로 이번 연구 브랜치에서 실제 사용자 앱을 수정했다고 주장하지 않는다.

**HISTORIAN_REVIEW=NOT_PERFORMED · READER_PILOT=NOT_PERFORMED · AI_STUDIO_DEPLOYMENT=NOT_APPLIED · RIGHTS=NOT_CLEARED · can_ship=false.**
