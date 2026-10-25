# 03 · TRD V0.2 — Google AI Studio Build 기술 설계
> 2026-10-25 · DRAFT / 생성 플랫폼: Google AI Studio Build(Web).
> 참고: https://ai.google.dev/gemini-api/docs/aistudio-build-mode?hl=ko

## 1. 기술적 방향 전환
| 항목 | 기존 V0.1 | 이번 V0.2 |
|---|---|---|
| 웹 프런트 | Astro 권장 | React + TypeScript (AI Studio 기본 React와 정합) |
| 서버 | 정적 우선 | 필요시 Node.js 서버 런타임/Secrets |
| 데이터베이스 | 후속 검토 | P0에서 불필요, Git JSON·Markdown 원본 |
| 사이트 생성 | 직접 구현 가정 | AI Studio Build 프롬프트로 점진적 생성 |
| 배포 | Cloudflare 후보 | AI Studio 미리보기, 추후 Cloud Run은 별도 승인 |
| 디자인 | 개념 정의 | Quiet Editorial Atlas 토큰 구현 |

## 2. 원칙과 실제 구현 대상
AI Studio가 처음 생성한 프로젝트의 빌드/패키지 도구를 존중한다. TypeScript strict, React 함수 컴포넌트, 라우트, 재사용 컴포넌트, 콘텐츠 어댑터 및 검사 코드가 필요하다. AI Studio의 npm/Node 기능은 지원되지만 첫 앱에서 DB·Gemini API·로그인은 필수 기능이 아니다. GitHub 연동은 공식적으로 가능하나 브랜치/권한 충돌과 미승인 파일 공개에 주의한다.

제안 폴더 구조(코드를 아직 생성하지 않음):
- src/app: App, Router, RootLayout
- src/pages: Home, Volumes, VolumeDetail, People, PersonDetail, Timeline, EventDetail, Documents, DocumentDetail, Places, Topics, TopicDetail, Search, About
- src/components/layout: Header, MobileNav, Breadcrumb, Footer
- src/components/editorial: VolumeCard, PersonCard, TimelineEvent, DocumentRow, TopicCard
- src/components/trust: SourceLink, EvidenceStatus, ReviewNotice, EmptyState
- src/lib/content: read-only data adapter, alias/crosswalk, publication allowlist, deep-content extension
- src/lib/search: alias-aware type-filtered search
- src/styles: design tokens, global CSS, reduced motion
- src/tests: data integrity, routing, publication gate, accessibility smoke tests
- assets: **승인된 파일만**, 외부 연구용 후보 미디어는 복사 금지

## 3. 콘텐츠 데이터 계약
| 대상 | 필수 입력 | 독자 표시/금지 |
|---|---|---|
| Volume | id, title, summary, type | VOL-08은 시대가 아닌 횡단 자료실 |
| Person | canonical_id, nameKo/nameEn, years, summary, sourceIds | 동일 인물 ID/URL 유지 |
| Event | dateLabel, precision, yearStart(sort only), references | '1420년 전후'를 정확한 날짜로 바꾸지 않음 |
| Document | originalTitle, editionKind, summary, sourceIds | 유료판 원문 전문 자동 수록 금지 |
| Place | modernPlace, evidenceStatus, coordinates(optional) | 22개 미검증 장소에 지도 핀 금지 |
| Topic | id, relatedVolumes, sourceIds | 1~7권 문헌·사상을 연결 |
| Relation | fromId, toId, relationType, sources | 문헌 영향과 직접 여행/사제관계 혼동 금지 |
| ContentBlock | entityId, depth, revision, sourceIds, status | 개요 이후 심층 내용만 증분 추가 |
| Media | sha, origin, alt, rights, historicalReview, publishState | 미승인 AI 그림은 공개 차단 |

초기 데이터 정본: data/overview 내 JSON, docs/01_CONTENT/OVERVIEW의 여덟 Markdown. 기본 개요 127객체 + 32관계, 출처 23개(별칭 2개). 3명의 인물(발도·위클리프·후스)은 legacy_person_crosswalk_v01.json에서 기존 제3권 PER ID로 연결하며 원본 OV-P 관계를 파괴하지 않는다.

**정밀 날짜 값:** day/year/range/period/approximate_year/approximate_period. 날짜 label을 우선 표시하고 정렬 연도를 정확한 날짜처럼 화면에 내보내지 않는다.

## 4. 게시 허용 규칙: deny by default
- 연구 데이터는 모두 DRAFT. 내부 사용자 시연에서만 DRAFT임을 명확히 표시.
- 외부 공개 빌드에서는 편집 승인 + 게시 승인 + 매체/문헌 권리 확인을 함께 요구한다. 미확인 권리(null 포함)는 공개 불가.
- 공개 페이지의 HTML/JS/JSON/검색 인덱스/소스맵/미디어 파일에 미승인 텍스트·파일이 있으면 FAIL.
- 보안은 CSS로 숨기는 것이 아니라 **빌드 입력과 서버 응답 단계에서 차단**해야 한다.
- GitHub가 공개 저장소일 경우 저장소 자체 자료는 공개될 수 있다. 앱 프리뷰를 비공개로 둔다고 저장소가 비공개가 되지 않는다.
- noindex/추측 어려운 URL은 인증이나 접근제어가 아니다. 개인 AI Studio 미리보기를 우선 사용하고 공유/Cloud Run Publish는 별도 승인을 받는다.
- P0는 Gemini API 호출/키를 사용하지 않는다. 추후 AI 기능을 추가한다면 Google AI Studio Server Secrets로 키를 보관하고 클라이언트 번들에 넣지 않는다.

## 5. 14개 라우트
/ · /volumes · /volumes/:id · /people · /people/:id · /timeline · /events/:id · /documents · /documents/:id · /places · /topics · /topics/:id · /search · /about

React Router 또는 AI Studio가 생성한 동등한 라우팅을 이용한다. 새로고침, 직접 링크, 뒤로가기, 존재하지 않는 ID, 빈 콘텐츠를 모두 테스트한다. 라우트는 UI 검토 뒤 최종 결정한다.

## 6. 검색·연대표·깊이 확장
- 한국어/영문/원어별칭: 루터/Luther, 후스/Hus, 성찬론, 1517 등을 검색.
- 유형별 필터(인물/사건/문헌/주제)와 0건 상태. 승인된 콘텐츠만 공개 검색 인덱스에 포함.
- 타임라인은 34개 이벤트의 label을 보존한 세로 리스트. 정확·근사 연대 차이를 보이는 소형 텍스트 설명 제공.
- 심층 블록: 동일 ID와 링크를 보존하고 APPROVED된 DEEP_RESEARCH 섹션만 공개 데이터에 추가. 수정 이력과 판본/출처 기록.
- 위치 데이터는 현 단계 ‘현대 지명 설명’만. 검증된 역사 좌표와 경로 기능은 P1으로 연기.

## 7. 시각적 구현 규칙
디자인 토큰은 DESIGN_TOKENS.json을 단일 기준으로 사용: canvas #F7F8F5 / ink #1C2925 / muted #4B6058 / forest #205F50. 콘텐츠 1200px 최대 폭, 읽기 720px, 충분한 섹션 간격, 저자극 transition, reduced-motion 지원. 모바일 320px 이상, 키보드 내비게이션, WCAG 2.2 AA 목표. 초기에 시각 이미지가 없다면 큰 편집형 타이포와 숫자/연대만으로 완성도 유지.

## 8. Google AI Studio 생성 순서와 검사
A. 첫 프롬프트: 레이아웃/토큰/홈/8권 구조 → 미리보기
B. 데이터 연결: 기존 JSON 실제 import 및 인벤토리 개수 진단 → 검증
C. 화면 연결: 인물/사건·타임라인/문헌/주제/장소/검색
D. 신뢰·게이트: 출처/상태/비공개/별칭/404/빈 결과 검사
E. 품질: 모바일·접근성·자동 빌드 테스트 → 기능 브랜치 GitHub 동기화
F. 배포: **사용자 승인 후에만**.

처음부터 모든 18개 요구사항을 한 프롬프트에 몰지 말고 06 마스터 프롬프트로 골격을 만든 후 07 반복 프롬프트를 순서대로 사용한다.

## 9. 테스트 및 인수 조건
- 8권·127 객체·32 관계의 유일 ID, 고아 참조 0.
- 데이터 실제 연결 전에는 DEMO를 명시. 실제 파일을 읽지 않았는데 127개를 임포트했다고 보고하지 않음.
- DRAFT 자료 공개 0, 미승인 AI 그림/지도 핀 0.
- 인물 교차 ID 3건, event precision 보존, 문헌 접근 범위 구분.
- 14 라우트, WCAG 2.2 AA 목표, 320/375/768/1440px 시각 검증.
- React 앱 실제 설치/실행/테스트는 **설계서 이후의 개발 단계**.

현재 상태: TRD DRAFT / React 기반 개발환경 설계 / 웹 코드 미생성 / 승인 미완료.
