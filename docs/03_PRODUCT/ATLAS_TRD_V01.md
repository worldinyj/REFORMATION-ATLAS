# REFORMATION ATLAS · 기술 요구 및 아키텍처 설계서 (TRD) V0.1
> 2026-10-25 · **DRAFT — 기술 제안서, 미구현** · 상위 [PROJECT PLAN](ATLAS_PROJECT_PLAN_V01.md) 및 [PRD](ATLAS_PRD_V01.md)
> 결정 사항은 사용자의 설계 검수 전까지 확정 아님. 웹 코드·호스팅·운영 배포를 실행하지 않는다.

## 1. 기술 목표와 설계 범위
첫 번째 구현은 8권 개요(127 데이터 객체, 32 관계)를 **빠르고 읽기 쉬운 탐색형 사이트**로 표현하는 것이다. 이후 깊이 `OVERVIEW`→`DEEP_RESEARCH`/문헌 이문/고증된 그림이 추가되어도 URL·ID·기본 화면 구조는 안정적으로 유지되어야 한다.

### 기술 목표
- 정적 페이지 중심으로 검색엔진·모바일 접근성·저용량 출력을 우선.
- Git의 Markdown/JSON을 정보 정본으로 보존하여 나중에 DB나 CMS로 이전 가능.
- 8권 가운데 VOL-08은 ‘8번째 시대’가 아닌 **문헌/사상 교차 인덱스**.
- 콘텐츠 승인(편집/학술/권리/게시)을 **기술 빌드/QA와 분리**.
- 미승인 이미지나 문헌, 역사 좌표를 공개 산출물에 복사하지 않는다.

## 2. 기술 스택 의사결정(승인 전 추천)
| 선택지 | 장점 | 비용/우려 | 판정 |
|---|---|---|---|
| **Astro + TypeScript + 빌드 시 JSON/Markdown 어댑터** | 콘텐츠·정적 페이지 중심, 필요시에만 클라이언트 인터랙션, 본문·URL·SEO/빠른 로딩에 적합 | 초반 자료 스키마 통합·검색 인덱스 어댑터 작성 필요 | **권장 후보** |
| Next.js + React + 정적/서버 하이브리드 | 동적 인증·관리/검색 확장이 쉬움 | 지금의 127개 개요에 SSR/서버 비용과 운영 복잡성 증가 | P1 서버 요구 발생 시 비교 |
| Django + HTMX/템플릿 | Python 중심 편집 도구·관리자에 적합 | 콘텐츠 정적 사이트에 초기 서버·DB/세션 부담 | CMS/편집자용 백엔드 요구 시 재평가 |

**권장안은 고정 결정이 아닌 TRD V0.1 기술 제안**이다. 프레임워크 최신 버전은 실제 구현 시작 시 호환성/안전 업데이트와 lockfile로 확정한다.

공식 문서: Astro content collections https://docs.astro.build/en/guides/content-collections/ ; Cloudflare Pages Astro 배포 안내 https://developers.cloudflare.com/pages/framework-guides/deploy-an-astro-site/ ; W3C WCAG 2.2 https://www.w3.org/TR/wcag/ .

## 3. 제안 디렉터리/아키텍처 (미생성)
```text
repo/
  data/overview/                  # 기존 정보 정본 (수정하지 않고 소비)
  docs/01_CONTENT/OVERVIEW/       # 8권 원고
  docs/03_PRODUCT/                # 계획/PRD/TRD/UXUI/TASKLIST
  apps/web/                        # 웹 구현 단계에서만 생성
    src/
      pages/                       # Astro route
      layouts/                     # 공통 헤더/사이드바/접근성 영역
      components/                  # VolumeCard, PersonCard, Timeline, SourceBadge ...
      lib/content/                 # 임포트, ID 통합, 승인 게이트
      lib/search/                  # 승인 콘텐츠만 담는 빌드 타임 색인
      styles/                      # design tokens
    public/                        # 승인된 정적 파일만
    tests/
  scripts/                         # 기존 Python 데이터 QA는 보존
```
패키지 관리자 및 Monorepo 여부는 구현 착수 시 확정한다.

**처리 흐름:** Markdown/JSON → 스키마 검사 → 출처/ID 대응표 적용(가상 읽기 뷰) → 공개/비공개 선택 → Astro 렌더링/검색색인 → 승인된 배포물만 포함. **원본 데이터를 수정하는 자동 마이그레이션 금지**.

## 4. 개요 데이터 계층과 글로벌 ID
초기 입력: 권 8, 인물 33, 사건 34, 문헌 20, 현대 지명 장소 22, 주제 10, 관계 32, 출처 등록 23(독립 근거로 중복 계산하면 안 되는 별칭 2개).

### 데이터 모델 및 향후 콘텐츠 깊이
| 엔터티 | 주요 필드 | 규칙 |
|---|---|---|
| Volume | `id`, `title`, `summary`, `order`/유형 | VOL-08은 theme_archive |
| Person | `id`, `canonical_person_id`, `name_ko`, `name_en`, `volume_ids`, `summary`, `depths` | 기존 제3권 PER- ID 우선 보존; `OV-P`는 alias |
| Event | `id`, `date_label`, `date_precision`, `year_start/end`, `summary` | `year_start`는 정렬에만 사용 |
| Document | `id`, `original_title`, `witness_kind`, `source_ids`, `rights_status` | 원저작/필사본/판본/번역/서평 혼합 금지 |
| Place | `id`, `modern_place`, `historical_site_verified`, `coordinates`(옵션) | 현재 22건 `coordinates=null`; map pin 금지 |
| Topic | `id`, `related_volumes`, `summary` | 제8권 중심의 공통 태그 |
| Relation | `id`, `from_id`, `to_id`, `type`, `source_ids` | 문헌 영향 ≠ 직접 여행/사제 관계 |
| ContentBlock | `parent_id`, `depth`, `body_ref`, `evidence`, `edition`/version, `review_status`, `publish_state` | 동일 URL 아래 점진적으로 추가 |
| Media | `id`, `asset_sha256`, `origin`, `alt_ko`, `rights_status`, `historical_review`, `publish_state` | 미승인 생성 이미지는 빌드 입력에서 차단 |

**반드시 TRD 구현 시험:** `data/overview/legacy_person_crosswalk_v01.json`의 발도·위클리프·후스 대응표는 읽기 전용으로 해석한다. 기존 `OV-R` 관계가 가리키는 ID를 조용히 다시 써서 원본을 손상시키면 안 된다. UI 링크 생성 시 우선 정본 ID로 해석하고 리디렉트/별칭 계약 테스트를 둔다.

### 표시 계층과 출처
- `source_ids`는 실제 서지 레코드에 매핑, 온라인 확인 수준 `WEB_CHECKED`와 `REFERENCE_ONLY_NOT_RECHECKED`를 구분.
- 역사적 확실성(확정/추정/논쟁적), 원전 직접 접근 등급(T1/T2/T3/S1/S2/HOLD 등), 편집 상태, 저작권, 공개 여부는 **각각 독립 필드**.
- 문헌 장문은 원문/판본 저작권을 확인한 경우에만. 유료 비평판은 자체 내용 요약과 출처 링크만.

## 5. 콘텐츠 승인/공개 보안 계약
모든 현재 개요는 DRAFT이며 기존 제3권 연구에도 별도 `approved=false`, `can_ship=false` 게이트가 있다.

```text
source item
  ├─ source reference exists? ─ no → reject
  ├─ editorial approval recorded? ─ no → exclude from public snapshot
  ├─ media rights & historical presentation cleared? ─ no → exclude media
  ├─ publication approval recorded? ─ no → exclude from public snapshot
  └─ yes → include in public build manifest → render/search/static assets
```

**핵심:** `DRAFT`를 화면에서 숨기는 CSS/JS만으로 보호해서는 안 된다. 공개 사이트 번들, JSON, HTML, 검색색인·소스맵·정적 이미지 디렉터리에 미승인 원고를 복사하지 않는다. 내부 검토는 로컬 환경을 우선 사용한다. 인터넷 프리뷰를 배포한다면 **실제 인증·접근 제어**가 필요하며 `robots noindex`는 보안 수단이 아니다. GitHub 저장소 자체가 공개인지 여부도 확인/승인받아야 한다. **연구 브랜치에 있는 자료는 웹 비공개와 별개로 저장소 가시성을 검토해야 한다.**

### 보안 테스트
- 최초 공개 승인 레코드 0개 → 빌드 public sitemap/detail route/search index에 승인되지 않은 정보 0개.
- 승인 없는 이미지 해시와 `assets/illustrations/**/candidates/` 파일이 `dist`에 있으면 빌드 FAIL.
- ID/관계 고아·날짜 정밀도 위조·누락된 출처가 있으면 빌드 FAIL.
- 복원/롤백: Git 커밋 및 승인된 manifest snapshot 기반 이전 버전 재생성 가능.

## 6. 페이지/라우팅 계약
- `/` — 홈
- `/volumes` — 8권 탐색
- `/volumes/:volumeId` — 권 상세
- `/people` — 인물 목록
- `/people/:personId` — 인물 상세
- `/timeline` — 연대표
- `/events/:eventId` — 사건 상세
- `/documents` — 문헌 목록
- `/documents/:documentId` — 문헌 상세
- `/places` — 장소 목록
- `/topics` — 주제 목록
- `/topics/:topicId` — 주제 상세
- `/search` — 통합 검색
- `/about` — 자료·출처 안내

페이지 경로는 **PRD의 제안 경로**이며 세부 permalink/alias 규칙은 UX/UI 승인 후 확정. 대부분 정적 사전 생성. 경로가 존재해도 승인된 상세 데이터가 없으면 임의 원문이나 허위 사건을 표시하지 않고 비공개/준비중 상태로 처리한다.

## 7. 검색, 타임라인, 지역
### 검색
P0은 승인된 데이터로부터 빌드 시 가벼운 클라이언트 색인을 제작. 정규화 키: 한글 표시명/라틴·영문 별칭, 유형, 권 ID, 주요 사건/문헌 제목. 루터/Martin Luther, 후스/Hus, 1517, 성찬론을 기본 회귀 시나리오로 제시. 형태소 분석·대규모 검색 서버/클라우드는 일단 도입하지 않음.

### 연대
라벨 `1420년 전후`와 내부 정렬 숫자 `1420`는 별개다. `day`, `year`, `range`, `period`, `approximate_year`, `approximate_period`를 버전 명시된 enum으로 보존. 불확실한 정확 월·일을 자동 생성하지 않는다.

### 장소
22개 장소는 문자열 지명일 뿐 현대 도시의 정확 좌표도 역사 사건 지점도 검증하지 않았다. P0는 **리스트/인물·사건 관계 텍스트**만 제공. 지도 엔진/지도 타일/경로 애니메이션은 P1 및 좌표 고증 후 선택.

## 8. 심층 콘텐츠 증분 확장
예: `Martin Luther` 인물의 초기 개요 카드에는 활동 연대·주요 사건·대표 문헌·출처를 유지. 추후 원전 번역·논쟁 해설·역사적 지도·초상 권리를 확인하면 해당 사람의 `DEEP_RESEARCH` 블록을 추가한다. 이 때 `OVERVIEW`는 삭제하지 않고 별도 개정 이력으로 남기며, 새 심층 내용도 승인된 블록만 공개한다.

각 변경은 `content_revision_id`, `source_ids`, `review_status`, `approved_at/by`(승인된 경우), `valid_from` 등이 추후 필요. 웹 코드의 구조 변경 없이 데이터+빌드로 재발행 가능하도록 한다.

## 9. 테스트/CI 및 품질
| 종류 | 기술 테스트 |
|---|---|
| 입력 계약 | 기존 `scripts/validate_atlas_overview_v01.py` 통과 및 필드 스키마 테스트 |
| ID | 사람 3건 정본 대응, 기타 ID 중복/누락 0 |
| 출처 | 모든 공개 카드의 출처/범위/출판 등급 유효, 2개 alias 중복 근거 계산 금지 |
| 날짜 | 34 사건의 정밀도 보존, 근사 날짜 월/일 변환 금지 |
| 이미지/지도 | 미승인 바이너리 및 비고증 지도 좌표가 `dist`에 포함되지 않음 |
| 공개 안전 | 0개 승인 레코드 조건에서 0개 공개 상세/검색 결과 |
| 기능 | 8권/33인물/34사건/20문헌/10주제/22장소 텍스트 접근 (내부 검토 모드) |
| 접근성 | WCAG 2.2 AA 지향, 키보드·스크린리더·텍스트 대비·라벨 |
| 반응성 | 320px·768px·1440px 주요 경로 점검 |
| 성능 | PRD 목표 검색 600ms/LCP 2.5초 (측정 환경 구현 시 정함) |
| 운영 | 승인 스냅샷 재현, 실패 시 롤백 및 콘텐츠 상태 감사 |

### FR 전체 추적
| PRD 요구 | 데이터 영역 | 경로/컴포넌트 | 기술 시험 ID |
|---|---|---|---|
| FR-001 | DOM-VOLUME | ROUTE-VOLUME | TEST-VOLUMES |
| FR-002 | DOM-VOLUME | ROUTE-VOLUME-DETAIL | TEST-VOLUME-DETAIL |
| FR-003 | DOM-PERSON | ROUTE-PERSON | TEST-PERSON |
| FR-004 | DOM-EVENT | ROUTE-TIMELINE | TEST-DATE |
| FR-005 | DOM-DOCUMENT | ROUTE-DOC | TEST-WITNESS |
| FR-006 | DOM-TOPIC | ROUTE-TOPIC | TEST-TOPICS |
| FR-007 | DOM-PLACE | ROUTE-PLACES | TEST-UNVERIFIED-PLACE |
| FR-008 | DOM-SEARCH | ROUTE-SEARCH | TEST-SEARCH |
| FR-009 | DOM-RELATION | ROUTE-DETAIL-LINK | TEST-RELATION |
| FR-010 | DOM-SOURCE | UI-PROVENANCE | TEST-SOURCE |
| FR-011 | DOM-APPROVAL | BUILD-PUBLIC | TEST-NONPUBLIC |
| FR-012 | DOM-ACCESS | UI-RESPONSIVE | TEST-A11Y |
| FR-013 | DOM-EMPTY | UI-EMPTY | TEST-EMPTY |
| FR-014 | DOM-VERSION | PIPELINE-CONTENT | TEST-REPLACE |
| FR-015 | DOM-ROUTE | UI-NAVIGATION | TEST-NAV |
| FR-016 | DOM-GEO | FUTURE-MAP | TEST-NO-COORDINATES |
| FR-017 | DOM-DEPTH | FUTURE-DEEP | TEST-OVERVIEW-DEPTH |
| FR-018 | DOM-EDGES | FUTURE-VISUAL | TEST-TYPED-RELATION |

## 10. 구축 단계·비용과 주요 트레이드오프
1. 데이터 스키마/게이트 변환기 → 2. 권/상세 공통 템플릿 → 3. 목록/필터/검색 → 4. 연대표/문헌/주제 → 5. 접근성/프리뷰 QA → 6. 사용자 검토 후 선택적 공개.
2. 초기 P0에서 별도 인증 서버/DB를 만들지 않는 대신 **내부 검토는 로컬**을 기본으로 한다. 편집자 여러 명의 원격 협업·실시간 업로드가 필요해지면 서버·CMS/인증 요구를 재검토.
3. 빌드/정적 배포는 Cloudflare Pages가 후보지만, 승인 전 실제 서비스 생성/Deploy는 금지.

## 11. 미해결 의사결정 및 다음 단계
- 프레임워크 Astro 추천안 채택/변경.
- 향후 운영자가 Git 기반 편집을 지속할지, Django·관리형 CMS를 둘지.
- 영구 인물 ID 및 URL alias 정책의 구체 형식.
- 프리뷰의 접근 제어 방식, URL 도메인/호스팅 승인.
- 다언어 검색·지도·관계도 단계별 확장 순서.

**상태:** `TRD_DRAFT_READY`, `TECH_STACK_NOT_APPROVED`, `WEBSITE_NOT_BUILT`, `can_ship=false`.
