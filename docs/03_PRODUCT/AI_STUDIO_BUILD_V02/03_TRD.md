# 03 · TRD V0.2 — Google AI Studio Build 중심 기술 설계

> 2026-10-25 · DRAFT · [PROJECT PLAN](01_PROJECT_PLAN.md) · [PRD](02_PRD.md) · [공식 Build 문서](https://ai.google.dev/gemini-api/docs/aistudio-build-mode)

## 1. 구현 전제
**Google AI Studio Build의 웹앱**을 사용한다. 공식 기본 프런트엔드는 React이고, 필요 시 Node.js 서버 런타임을 이용할 수 있다. **React + TypeScript**로 앱 코드를 생성하도록 프롬프트에 명시하며, 실제 생성물의 번들러·Node 버전·패키지 및 의존성은 **생성 후 확인**한다. AI Studio 기본 구성을 무조건 Vite라고 단정하지 않는다.

MVP는 **읽기 중심의 정적 콘텐츠 탐색**이다. Firebase Authentication/Firestore, 유료 지도, Gemini API 실시간 호출, 사용자 계정, 결제, AI 채팅 기능은 필요하지 않다. 이를 AI Studio가 자동 생성하면 제거 또는 P1 별도 제안하도록 한다.

### 1.1 선택 기술
| 계층 | 제안 | 이유 | 조건 |
|---|---|---|---|
| UI | React + TypeScript(strict) | Google AI Studio 기본 웹 빌더와 일치 | 생성물 검증 후 고정 |
| CSS | CSS custom properties / Tailwind 중 1개 선택 | 미니멀 디자인 일관성, 최소 의존 | 04의 토큰 소스 단일화 |
| Routing | React Router 또는 생성환경과 호환되는 동등 라우터 | 딥링크·뒤로가기·탐색 안정성 | 직접 URL 접근 회귀 테스트 |
| Content | Git 관리 JSON/Markdown 읽기 전용 어댑터 | 8권/127객체/32관계 원본 보존 | 입력 스키마 검증 |
| Search | 허가된 로컬 콘텐츠에 대한 간단한 클라이언트 색인 | 초기 데이터 소규모 | 한글/영문 별칭 규칙 |
| Server | Node.js 사용은 선택 | API가 없는 단계에 서버 상주 불필요 | 비밀키·API를 추가할 때만 |
| Database | 초기 불필요 | 편집은 Git PR 기반 | 다중 편집/실시간 저장 필요 시 재검토 |
| GitHub | 개발용 독립 브랜치 + PR | 이전 연구 문서 보호 | Build 연결/충돌 해소는 사용자 작업 |
| Deploy | Google AI Studio 내부 미리보기 우선 | 디자인과 기능 QA | Share/Publish/Cloud Run은 별도 승인 |

## 2. 데이터 계약 (개요 → 심층 확장)
입력 정본:
- data/overview/volumes_and_people_v01.json — 권 8 / 인물 33
- data/overview/events_documents_v01.json — 사건 34 / 문헌 20
- data/overview/places_v01.json — 장소 22 (실제 역사 좌표 미고증)
- data/overview/relationships_and_themes_v01.json — 관계 32 / 주제 10
- data/overview/source_register_v01.json — 출처 ID 23 (독립 출처로 중복 집계하지 않을 별칭 2)
- data/overview/legacy_person_crosswalk_v01.json — 발도·위클리프·후스 임시/정본 ID 대응표

앱 내부 UI 모델은 다음과 같이 **정규화된 읽기 모델**로 투영한다. 원본에 필드가 없는데 있다고 가정하지 말고 어댑터에서 계약에 맞춰 변환할 것.

| 모델 | 주요 필드 | 핵심 제약 |
|---|---|---|
| Volume | id, title, summary, period, category | VOL-08 = cross-topic archive |
| Person | canonicalId, aliases, nameKo/nameEn, summary, volumeIds, sourceIds, depthBlocks | 기존 PER/OV-P 같은 인물 중복 금지 |
| Event | id, title, dateLabel, datePrecision, sortYear, summary, related | 근사 연도를 정확한 월일로 위조 금지 |
| Document | id, title, originalTitle, period, sourceIds, witnessKind, fullTextIncluded | 원저술·후대번역·편집본·연구 구별 |
| Place | id, modernPlace, summary, historicalSiteConfirmed, geolocationStatus | P0는 실제 지도 마커 금지 |
| Topic | id, title, summary, relatedVolumeIds | 제8권 주제 허브 |
| Relation | id, fromId, toId, type, sourceIds, explanation | textual_influence ≠ direct_contact |
| ContentBlock | entityId, depth(OVERVIEW/DEEP_RESEARCH/PRIMARY_WITNESS), revision, sourceIds, publicationStatus | 심층 추가 시 기존 URL·ID 보존 |
| Source | id, url, publisher, accessType, reviewStatus, aliasOf | 출처 11건만 이번 링크·범위 검토 완료 |
| Media | id, origin, sha256, altText, rightsStatus, authenticityStatus, approvalStatus | 미승인 AI 이미지 빌드 제외 |

**식별자 규칙:** 최초 33명 중 기존 제3권 3명은 \`legacy_person_crosswalk_v01.json\`을 기반으로 단일 역사 인물로 해석한다. 원본 OV-P와 PER 레코드를 병합/개명하지 않는다. 화면 링크 생성용 해석기에서만 안정적 canonicalId를 사용하며 별칭 URL → 단일 페이지로 이동한다.

**콘텐츠 깊이:** 지금은 OVERVIEW만 제공. 나중에 후스·루터 등의 DEEP_RESEARCH 블록을 데이터에 추가할 수 있어야 하지만 승인된 새 블록 이외에는 공용 빌드에 들어가지 않는다.

## 3. 제안 파일 구조 (구현 시 생성; 현재 없음)
\`\`\`text
apps/web/
  package.json
  src/
    app/                 # Router, application shell, providers
    components/
      layout/            # Header, Footer, Breadcrumb, PageContainer
      discovery/         # VolumeTile, PersonRow, FilterBar, SourceRef
      content/           # RichText, RelatedItems, DepthSection
      states/            # EmptyState, LoadingState, NotFound
    pages/
      Home, Volumes, VolumeDetail, People, PersonDetail,
      Timeline, EventDetail, Documents, DocumentDetail,
      Places, Topics, TopicDetail, Search, About
    data/
      adapters/          # typed source loader, no fabricated fields
      selectors/         # source-aware filtering and relationship joins
      schemas/           # runtime type validation
    content/
      snapshots/         # REVIEW_ONLY vs approved-only PUBLIC
    styles/              # design tokens + typography + responsive
    test/
  public/
    approved/            # allowlisted assets only
\`\`\`

**AI Studio 앱 가져오기 경고:** 역사 콘텐츠만 가득한 저장소 전체를 가져오면 AI Studio가 루트 폴더를 임의 앱 구조로 바꿀 위험이 있다. **처음에는 06_MASTER_BUILD_PROMPT.md의 지시문으로 새 앱을 생성**하고, 생긴 파일을 검토한 후 독립 개발 브랜치의 \`apps/web/\`에 합치는 방식이 안전하다. GitHub Import/2-way sync를 사용한다면 변경 파일 범위를 사전 점검하고 \`main\` 직접 푸시는 하지 않는다.

## 4. 프리뷰/공개 콘텐츠 경계 (중요)
현재 연구 개요 전체는 DRAFT. **AI Studio 내부 미리보기와 공개 사이트는 다른 환경**이다.

- \`REVIEW_ONLY\`: 소유자 로컬 또는 AI Studio의 접근 제한된 개발 미리보기. 미검토 개요 127객체를 표시할 수 있으나 명확히 **검토용**으로 표시. 공유/게시 링크를 생성하지 않는다.
- \`PUBLIC\`: 콘텐츠별 명시적인 editorial_approved + publication_approved가 존재하는 **allowlist 스냅샷만** 사이트 HTML/JS/JSON/검색색인에 포함. 승인 0개일 때 연구 상세 0개가 공개된다.
- 단순히 \`robots noindex\`, CSS 숨김 또는 \`import.meta.env\`의 클라이언트 boolean 체크만으로 데이터를 보호하지 않는다. 공개용 빌드는 **빌드 단계에서 승인된 스냅샷만 읽어야** 한다.
- 이미지의 권리/역사 고증은 콘텐츠 본문 승인과 독립: \`rights_cleared && historical_media_reviewed && publication_approved\`일 때만 공용 public 자산에 포함.
- GitHub 저장소가 public이라면 원본 저장소의 가시성은 이미 공개인 셈이므로, URL 노출/클라이언트 번들 문제와 구분해 판단한다.
- Cloud Run 배포와 Build 앱 공유는 별도 UI 작업 및 비용·접근권한 확인이 필요하다.

### 4.1 빌드 실패 규칙
1. 공개 빌드에 review_status=DRAFT 또는 publish=false 자료가 포함될 경우 FAIL.
2. \`/assets/illustrations/**/candidates/\`, 승인되지 않은 이미지 바이너리, 원고 전문 파일이 PUBLIC 산출물에 복사되면 FAIL.
3. 공개 검색색인에 출처/권리 미승인 레코드가 있으면 FAIL.
4. 미확인 장소 좌표로 만든 지도 마커가 있으면 FAIL.
5. 문헌 전문 저작권·라이선스가 미확인인데 클라이언트에 전문이 포함되면 FAIL.

## 5. UI 라우트(14화면)
\`\`\`text
/
 /volumes
 /volumes/:volumeId
 /people
 /people/:personId
 /timeline
 /events/:eventId
 /documents
 /documents/:documentId
 /places
 /topics
 /topics/:topicId
 /search
 /about
\`\`\`
라우트의 식별자는 slug에 의존하지 않는 안정 ID를 사용. 번역·정본 ID 병합 시 과거 링크를 깨뜨리지 않는다. 모바일 뒤로가기/브레드크럼/스크롤 복원 테스트.

## 6. 상호작용·검색·연대표
- 검색: 로컬에서 한국어/영문/원어 별칭, 공백·대소문자 정규화. \`루터\`, \`Martin Luther\`, \`후스\`, \`Hus\`, \`1517\`, \`성찬론\` 회귀 사례.
- 인물 탐색: 인물의 연관 권·사건·문헌·주제를 클릭하여 2~3단계 이동, 관계에는 유형 표시.
- 연대표: \`year_start\`는 정렬, \`date_label\`은 화면 표시. day/year/range/period/approximate_year/approximate_period 보존.
- 특정 1436년 7월 5일 공적 선포와 7월 6일 문안 낭독을 하나의 날짜로 합치지 않는다(기존 제3권 연구 문서 참고).
- 장소: 도시 목록은 가능하지만 실제 역사 행사 건축물의 고증된 위치는 0건. 지도 렌더러/실제 핀은 P1.
- 콘텐츠 부족: 억지로 외부 이미지를 임포트하지 않고 **텍스트 기반 깊이감 있는 UI**와 ‘심층 연구 준비 중’을 사용한다.

## 7. 검증 계약
| Test ID | 대상 | 기대 결과 |
|---|---|---|
| TC-01 | 8권 IA | 8/8 카드를 보고 VOL-08은 자료실 |
| TC-02 | 33명 인물 | 목록/상세 및 3명 ID 교차표 |
| TC-03 | 사건 34 | 정밀도 보존/정렬, 임의 정확 날짜 없음 |
| TC-04 | 문헌 20 | 요약/원전·번역·편집본 구분 |
| TC-05 | 주제 10 | 관련 시대 이동 |
| TC-06 | 장소 22 | 현대 지명 목록, 지도 핀 0 |
| TC-07 | 관계 32 | 고아 ID 0, 영향/수용/직접접촉 구별 |
| TC-08 | 검색 | 6개 회귀 질의 + 없는 결과 |
| TC-09 | 공개 분리 | 승인 0건에서 public 상세·색인 0건 |
| TC-10 | 반응형 | 320/375/768/1024/1440px 오버플로 없음 |
| TC-11 | 접근성 | 키보드/스크린리더/대비/포커스 및 reduced-motion |
| TC-12 | 업데이트 | 후스/루터에 깊이 블록 추가해도 같은 ID·URL |
| TC-13 | 빌드 보안 | 패키지에 후보 이미지/비밀키/미승인 문헌 전문 0 |
| TC-14 | Git 연동 | AI Studio에서 변경한 파일 diff 확인, 연구 원본 불변 |

**보안:** API 키 필요 없는 MVP에 GEMINI_API_KEY 연결/브라우저 노출 금지. 미래 AI 기능은 Node 서버 Secret에서만 호출. 프로젝트 소스와 서드파티 종속성은 실제 설치 후 감사.

## 8. 구현 승인 전 미확정
- AI Studio가 생성하는 실제 React 앱 구조/컴포넌트 빌드 시스템과 lockfile.
- Router, 스타일 도구, 테스트 러너의 정확한 패키지/버전.
- GitHub 연결 권한과 브랜치·충돌 해결.
- 배포 대상(Cloud Run 등) 및 공유/유료 사용 승인.

**현재:** TRD_DRAFT_READY / WEB_CODE_NOT_CREATED / HUMAN_APPROVAL_PENDING / PUBLICATION_BLOCKED.
