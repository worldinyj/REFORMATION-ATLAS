# AI Studio B2 — 문헌 상세 판본 비교 컴포넌트 인수 (2026-10-26)

**상태: HANDOFF ONLY / NOT SYNCED OR DEPLOYED**

## 이미 확인한 실제 AI Studio 앱
https://aistudio.google.com/apps/2bfbd3e6-8a9f-4e09-a34e-1abf17aca711

브라우저에서 보이는 앱의 파일 트리: `src/pages/DocumentDetailPage.tsx`, `src/lib/atlasSelectors.ts`, `src/lib/publicBuildGate.ts`, `src/components/ContentBlockRenderer.tsx`, `src/types/atlas.ts`, `package.json`. AI Studio의 실 파일 내용은 GitHub에 아직 내보내지지 않았으므로 기존 내용에 대한 변경·동기화·테스트를 했다고 주장하지 않는다.

## 작업 목표
1. 기존 정본 `/documents/:documentId` 및 20개 OVERVIEW 문헌을 유지한다.
2. `handoff/vol04/DocumentEditionComparison.tsx`를 **참고 소스**로 활용해 실제 앱의 `src/components/DocumentEditionComparison.tsx`에 추가한다. 기존 파일을 덮어쓰지 말고 기존 디자인 시스템과 타입에 맞게 조정한다.
3. `src/pages/DocumentDetailPage.tsx`의 DEEP_RESEARCH 슬롯 아래에 `<DocumentEditionComparison documentId={document.id} />`를 삽입한다. **승인된 별도 공개 스냅샷이 없으므로 현재는 empty state만 출력한다.** `data/deep/vol04_*` 연구 JSON을 앱에 import하지 않는다.
4. 접근성 검증: 탭은 키보드 화살표 탐색 또는 명확한 버튼 인터랙션 및 tab focus를 보장하고, 모든 판본은 텍스트 연표도 제공한다. 기본 여백, 모바일 320px부터 가로 스크롤 없음.
5. `src/lib/publicBuildGate.ts`와 별도 검사에서 `VOL04-CMP-`, `CMP-SRC-PROP-`, `WORK-PROP-V04-`, `EDN-PROP-V04-`, `DOC-PROP-V04-` 등 연구 키/연구 JSON이 공개 번들로 포함되면 실패하도록 한다. **주의:** 참고용 TSX 코드 자체도 정규식에 이들 토큰이 포함되어 있으므로 정적 문자열 번들 검사와 충돌하지 않게 검사 설계를 조정한다. 가능하면 연구용 파일을 아예 빌드 input으로 사용하지 않고 번들 검사는 생성 파일에서 실행한다.
6. 승인 manifest, 문헌/판본/출처/권리/사람 승인 없이 공개용 payload 생성 절대 금지. 연구 브랜치와 합치거나 `main` 병합하지 않는다.

## 앱 적용용 지시문 (Google AI Studio Build 채팅에 입력)
```
현재 REFORMATION ATLAS 앱 코드를 유지하면서, 문헌 상세 화면에 제4권 판본 비교 영역을 추가하세요. 기존 DocumentDetailPage.tsx, ContentBlockRenderer.tsx, atlasSelectors.ts, publicBuildGate.ts를 먼저 읽고 설계 충돌을 확인하세요. 이미 존재하는 React/TypeScript 구현을 수정하되 14개 라우트, 기존 20개 문헌 ID, 출처와 DEEP_RESEARCH 섹션을 보존하세요.

참고 코드 경로: GitHub worldinyj/REFORMATION-ATLAS, feat/vol04-document-ui-handoff-v01, handoff/vol04/DocumentEditionComparison.tsx. 접근할 수 없다면 해당 소스를 읽었다고 주장하지 말고 현재 앱 타입에 맞춘 독립 컴포넌트를 구성하세요.

판본 비교 섹션에는 제목과 '승인된 판본 비교 자료가 없습니다.'라는 빈 상태만 기본 표시하세요. 승인된 출판 manifest가 없으므로 연구 브랜치의 17개 후보, 10개 임시 판본, 3개 비교 사례, 이미지 원전·연구 텍스트를 앱에 절대 가져오지 마세요. 기존 정식 저작 ID /documents/:documentId를 유지하고 -PROP-, VOL04-CMP, CMP-SRC-PROP 등의 키로 새 라우트를 만들지 마세요.

미래의 승인본용 타입만 정의하되 기본적으로 null을 전달하세요. 판본 연표, 구성/본문/삽화 탭은 승인된 데이터에서만 렌더링하세요. 본문 비교에는 원전 대조가 완료된 경우에만 표시 허용. 최소 구현, 접근성, 모바일 반응형, 키보드, publicBuildGate 관련 단위 테스트와 Build를 수행하고 diff·결과를 보고하세요.

Share, Publish, Cloud Run, GitHub main push는 하지 마세요.
```

## 후속 인수 게이트
- Google AI Studio에서 소스를 GitHub 개발 브랜치로 export/commit한 뒤 해당 커밋을 기준으로 실제 TypeScript 컴파일, 유닛 테스트, 모바일 화면, 공개 번들 비포함을 확인한다.
- 연구 전용 `research/vol04-bibliography-editions-v02`는 변경 없이 유지.
- 적용 완료 전 상태는 `AI_STUDIO_INTEGRATION_NOT_VERIFIED`.

## 확인 범위
- 현재 GitHub의 `feat/atlas-web-overview-mvp` 및 `plan/atlas-ai-studio-build-v02`에서는 UI `src/`와 package.json이 발견되지 않았다.
- AI Studio 브라우저 탭에서 React 앱 소스 파일 목록과 Built 로그는 확인했지만 실 파일 내용은 확보·변경하지 않았다.

## V0.2 안전성·재현 검사 업데이트 (2026-10-26)

V0.1의 참고 TSX는 다음과 같이 보완되었다.
- `handoff/vol04/editionPolicy.ts`: 승인 상태, 정식 ID 문법, 문헌 일치, 각 판본의 승인 상태, 비교 근거 존재, **본문 원전 대조와 이미지 권리 조건** 검사. 브라우저 검사는 서명 검증/편집 승인의 대체가 아님.
- `handoff/vol04/approvedEditions.ts`: `Object.freeze({})`로 고정된 **빈 승인본 공급원**. 현재 자료 0건이 정상.
- `handoff/vol04/DocumentEditionComparison.tsx`: 외부에서 임의 payload를 받는 방식을 폐기하고, 전용 승인 공급원만 조회. 탭은 ArrowLeft/ArrowRight/Home/End 및 스크린리더 상태 지원.
- `handoff/vol04/DocumentEditionComparison.css`: Quiet Editorial Atlas 팔레트·모바일 터치 목표·focus-visible·줄바꿈·reduced-motion.
- `handoff/vol04/package.json` 및 `tests/policy.test.cjs`: 독립 React/TS 설정과 양성·음성 회귀 테스트.

**앱 파일 적용 순서**: 기존 앱 소스가 GitHub로 export된 후 세 TS/TSX 파일을 `src/components/vol04/`에 넣고 CSS를 기존 글로벌 스타일에 import한다. `DocumentDetailPage.tsx`에 `<DocumentEditionComparison documentId={document.id} />`를 추가하되 문헌 객체 ID 필드 이름이 다른 경우 실제 타입에 맞춘다. 14개 라우트를 새로 만들지 않는다.

**개발 검사**: `cd handoff/vol04 && npm install --no-audit --no-fund && npm test`. 제공한 source와 순수 정책 로직은 로컬 `tsc -p tsconfig.policy.json` 및 Node test 6건 통과. 별도의 GitHub Actions 워크플로 `.github/workflows/vol04-ui-handoff-qa.yml`을 구성해 JSX 타입검사를 요청했다. GitHub CI 결과는 실행된 경우에만 PASS로 보고한다.

**출판 검사**: 이 컴포넌트의 런타임 타입 검사만으로 퍼블릭 승인이 성립하지 않는다. 향후 독립된 사람 승인 릴리스 매니페스트에서만 `approvedEditions.ts`의 공급원을 빌드 시 생성해야 하며, 미승인 research JSON, 미검증 이미지, 원전 본문을 앱 import·번들에 넣지 않는다.

**현재 상태**: HANDOFF_IMPLEMENTED / REACT_APP_INTEGRATION_PENDING / PUBLIC_RELEASE_BLOCKED.
