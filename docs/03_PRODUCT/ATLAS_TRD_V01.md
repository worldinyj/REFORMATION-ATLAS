# REFORMATION ATLAS — 기술 요구사항 정의서(TRD) V0.1
> 2026-10-25 · **DRAFT / 기술 선택은 제안 단계**
> **PROJECT PLAN → PRD → TRD → UX/UI → TASKLIST → 웹 MVP → 심층 역사 콘텐츠 증분**
> 코드 구현·배포는 이 문서에서 하지 않으며 기존 연구 자료를 수정하지 않는다.

## 1. 요구사항과 기술 목표
상위 PRD: [ATLAS_PRD_V01.md](ATLAS_PRD_V01.md), 기능 요구사항 18건(P0 15/P1 3), 페이지 유형 14종, 수용시험 그룹 10개.
MVP 목적은 먼저 8권·33인물·34사건·20문헌·22 현대 지명·10주제·32관계를 **개요 데이터로 탐색**하는 것. 고증자료가 늘어날 때 디자인을 다시 만들지 않고 **같은 페이지의 읽기 모델에 심층 블록을 추가**한다.

## 2. 우선 제안 아키텍처: 정적 우선, 콘텐츠와 화면 분리
```text
기존 GitHub 역사 연구 콘텐츠 (Markdown/JSON/출처)
       ├── VOL03 심층 연구 원본 (절대 덮어쓰기 금지)
       └── 8권 개요 data/overview/*  (현재 전부 DRAFT)
                       │
           ① Python 구조·근거·권리 검증
                       │
           ② 정규화된 read-only entity projection
                       │
           ③ 승인 상태별 공개/비공개 데이터 분리
                    ┌──┴──────────────────┐
              public builder         local/internal review builder
              승인 기록된 항목       DRAFT 명시, 권한 제한
              ★ 미승인 0개          ★ 외부 접근 통제
                    │                       │
           ④ Astro/TypeScript UI       동일 컴포넌트의 검토 렌더
                    │
              정적 HTML/검색 인덱스 + 원본 출처 링크
```
**Astro + TypeScript 정적 페이지**를 현재 가장 단순한 후보로 제안한다. CMS/API/Django 서버는 P0에 필수 요건이 없다. 추후 다중 편집자·인증 기능·동적 검색이 실제 필요해지면 Django/PostgreSQL 등으로 발전 가능하도록 계약을 독립적으로 둔다. 프레임워크/호스트는 인간의 기술 결정 뒤 TASKLIST에서 확정한다.

### 기술 의사결정 기록
| ADR | 주제 | 1차 권고 | 보류 조건 |
|---|---|---|---|
| ADR-001 | Web rendering | Astro + TypeScript, pre-render static-first | Small initial catalogue; pages and cross-links, low cost; no login/transaction in P0; future deep content remains Markdown/JSON |
| ADR-002 | Storage | Git-managed Markdown/JSON + build-time generated read model, no DB in P0 | Current GitHub data and Python validators are ready; editorial traceability via Git; DB is warranted only for multi-author workflows/user data |
| ADR-003 | Search | Static client-side index, deterministic Korean/Latin normalized title and aliases | 127 introductory records, no need remote service; type-scoped queries; avoid leaking draft records in index |
| ADR-004 | Hosting | Cloudflare Pages as optional static host only after release-gate decision | Candidate only. Preview deployments are public by default and must not contain draft data unless protected with Access |
| ADR-005 | Places and maps | Text-only places in P0; verified geodata and map provider P1 | 22 places are unverified named locations and have zero confirmed coordinates. False historical precision is disallowed |
| ADR-006 | Images | No unapproved historic portraits in P0 public build; optional verified licensed assets later | Old VOL03 historic study/candidate 8 visuals still require human scholarly and rights approval |

참고 문서: [Astro Content Collections](https://docs.astro.build/en/guides/content-collections/), [Cloudflare Pages Preview Access](https://developers.cloudflare.com/pages/configuration/preview-deployments/), [Cloudflare Pages Branch Controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/).

**중요:** Cloudflare Pages의 preview URL은 기본적으로 공개 접근 가능하다. 연구용 DRAFT 데이터를 프리뷰로 배포할 계획이라면 사전에 Cloudflare Access 등 보호 장치를 검증해야 하며, 기본 설정으로 임시 URL을 생성하지 않는다. `noindex`는 접근통제가 아니다. PRD/설계 브랜치가 호스팅 서비스에 자동 연결되어 있다면 그 빌드를 별도 통제해야 한다.

## 3. 데이터 모델과 ID 전략
### 3.1 엔터티 명세 (정규화된 읽기 모델, 원본 개정 금지)
| 엔터티 | 필수 | 주의 |
|---|---|---|
| Volume | `id,title_ko,period_or_scope,summary,source_ids,review_status` | VOL-08은 사상·문헌 횡단형 |
| Person | `global_id,name_ko,aliases,period,summary,volume_ids,source_ids` | 동일 역사 인물 한 번만 등록 |
| Event | `id,title_ko,date_label,date_precision,year_start,source_ids` | 정렬 연도는 정확 월일이 아님 |
| Document | `id,title_ko,original_title,period,witness_kind,source_ids,rights_status` | 원저작·필사본·인쇄판·번역·논문 구별 |
| Place | `id,name_ko,modern_place,geolocation_status,source_ids?` | 미고증 좌표는 NULL |
| Topic | `id,title_ko,related_volume_ids,source_ids` | 주제는 여러 권에 속함 |
| Relation | `id,from_id,to_id,type,source_ids,review_status` | 문헌 영향 ≠ 개인 여행 |
| SourceRef | `id,title,url,source_kind,access_tier,checked_scope` | 동일 URL 별칭은 독립 출처로 중복 계산 금지 |
| ContentBlock | `entity_id,depth,body_ref,version,source_ids,review_status,public_visible` | 개요/심층/쟁점/판본/이미지 블록 |

### 3.2 단일 인물 ID 계약
- 현재 개요의 `OV-P-*`는 **임시 식별자**다. 발도·위클리프·후스는 `data/overview/legacy_person_crosswalk_v01.json`의 `PER-0004/0001/0002`와 연결.
- TRD가 정식으로 승인되기 전 `OV-P`의 일괄 ID 재작성·기존 관계 FK 파괴를 금지한다.
- 변환 빌드 시 먼저 **immutable global ID**를 확정해 `OV-P` → `PER` 매핑을 적용한다. 미등록 30인물의 신규 PER ID는 변경되지 않는 방식으로 별도 배정하고 실제 배정 결과·충돌 검사를 기록해야 한다.
- 대외 URL은 인물의 원어/한글 표기 변경과 무관한 안정적 키(추천: `/people/<globalId>`)를 사용한다. 별명 slug는 리다이렉트로 관리.

### 3.3 콘텐츠 깊이와 원본 문헌 구별
```text
Entity(person PER-...) 
 ├── OVERVIEW          짧은 생애·시대·관련 사건·주요 문헌
 ├── DEEP_RESEARCH     연구주제·문맥·전통 간 해석과 반론
 ├── DOCUMENT_WITNESS  원문/인쇄판/번역/논문 (접근 허가 차등)
 └── MEDIA             AI 상상화/공개 소장 이미지/검증된 지도 (권리+고증 독립)
```
데이터 단위의 `review_status`와 `public_visible`은 별도 필드다. 성찬론이나 교회사 특정 해석의 `certainty`와 파일 `rights_status`도 따로 유지한다. 공개 승인 없이 `DRAFT` 내용을 SSG에 자동 수록하면 안 된다.

## 4. 승인된 콘텐츠만 빌드하는 경로
**필수 배포 게이트(제안):**
1. JSON/Markdown 형식·권역·ID·출처 고아·라이선스 필수 항목 검증.
2. 공용 데이터 집합은 **`review_status=APPROVED` 및 `public_visible=true`**를 모두 만족해야 한다. 별도 권리 상태 `rights_status=APPROVED`가 필요한 자산도 검사한다.
3. 배포 페이지·클라이언트 JS ·검색 인덱스·사이트맵·정적 `public/` 파일 어디에도 DRAFT 원문/미승인 그림 포함 금지. 단순히 화면에서 `display:none`으로 감추는 것으로는 부족하다.
4. 다만 코드가 포함된 **공개 GitHub 저장소 자체는 이미 접근 가능한 연구 자료를 포함**한다. 사이트가 게시하지 않는다는 것이 GitHub 원본의 기밀성을 의미하지 않으므로 진짜 비밀 자료는 애초에 공개 저장소에 넣지 않아야 한다.
5. 승인 자료가 0건이면 **독립된 비공개 UI 프리뷰 또는 빈 셸**이 안전한 결과다. 127개를 임의 공개 승인하는 것은 금지.

내부 프리뷰는 첫 단계에서 로컬 개발 서버로만 만들고, 외부 프리뷰가 필요하다면 조직인증/접근제어와 GitHub 브랜치 배포 제한을 **먼저 실제 시험**한다.

## 5. 정적 검색 설계
- 초기 공개 검색 인덱스는 승인된 `id, title_ko, aliases, summary, type, volume_ids` 필드만 포함.
- 한국어 공백/대소문자/영문 철자 표준화 및 원어별 별칭 사전 운영. 동음이의 인물은 `id`와 시대 병기.
- 최소 테스트어: `루터`, `Martin Luther`, `후스`, `Jan Hus`, `성찬`, `1517`, `번역`.
- 일차 단계에서 단순 부분문자열/전방 일치와 타입별 필터로 충분. 형태소 분석기/원격 검색 서비스는 정보 규모가 커진 뒤 도입을 비교.
- 검색 인덱스에도 `DRAFT`가 남지 않는 테스트를 릴리스 차단 검사로 지정.
- 검색/정렬이 자동으로 사상 관계를 만들어 내지 않도록 한다.

## 6. 연대표·장소·관계 엔진
### 날짜
`date_precision`: `day, year, range, period, approximate_year, approximate_period`. 검색과 정렬에 쓰는 `year_start`를 실제 날짜로 치환하지 않으며 UI에 `date_label` 우선 표시. 예: “1435년 7월 추정”과 “1436년 7월 5일 선포”를 같은 유형의 정확 일자로 오인시키지 않는다.

### 장소
현재 22곳의 `geolocation_status=UNMAPPED_MODERN_PLACE_ONLY`. P0에는 목록/연계 장소만 포함. P1 지도 핀은 `modern_coordinates`(현대 대표 좌표), `historical_site_evidence`, `coordinate_confidence`, `rights_status` 등의 독립 정보와 검토를 갖춘 경우에만 공개. 현재 근거 없는 특정 중세 건축·전투 지점 생성 금지.

### 관계
`textual_influence` `later_reception` `historical_participant` `associated_place` `collaborator_of` 등 기존 관계 유형을 보존. **`textual_influence`로부터 직접 만남·여행·교리 일치를 자동 도출하지 않는다.**

## 7. 페이지·라우팅 계약
| P0 UI | 경로 제안 | 데이터 |
|---|---|---|
| 홈 | `/` | approved-only catalog |
| 8권 탐색 | `/volumes` | approved-only catalog |
| 권 상세 | `/volumes/:volumeId` | Volume + cross references |
| 인물 목록 | `/people` | approved-only catalog |
| 인물 상세 | `/people/:personId` | Person + ContentBlocks + links |
| 연대표 | `/timeline` | Event[] ordered by year_start |
| 사건 상세 | `/events/:eventId` | approved-only catalog |
| 문헌 목록 | `/documents` | approved-only catalog |
| 문헌 상세 | `/documents/:documentId` | approved-only catalog |
| 장소 목록 | `/places` | Place[] name-only |
| 주제 목록 | `/topics` | approved-only catalog |
| 주제 상세 | `/topics/:topicId` | approved-only catalog |
| 통합 검색 | `/search` | approved-only catalog |
| 자료·출처 안내 | `/about` | approved-only catalog |

404/미승인 항목 응답: 공개 URL에 미승인 상세가 요청되면 **404 또는 검토 중인 일반 안내**로 처리하고 데이터는 응답 본문에 포함하지 않는다. 내부 프리뷰에서는 잠금 표시와 출처/검토 상태를 별도 제공한다.

## 8. 구현 경계와 검증 단계
```text
[1] Read original JSON/MD ──> [2] validate_atlas_overview_v01.py
        │                                     │
        ▼                                     ▼
   content-normalizer                       [3] ID & schema gates
        │
        ▼
   public-exporter (APPROVED only) / review-exporter (local only)
        │
        ▼
   Astro content model + typed components
        ├── volumes, people, timeline, events, docs, topics, places, search
        └── optional deep blocks / map P1 only
        │
        ▼
   links/a11y/performance/rights/security release checks
        │
        ▼
   manually approved deployment
```

검증은 **단위**(ID·검토·날짜·검색), **통합**(관계/라우트), **시각**(반응형/가독성/색 대비), **접근성**(키보드/스크린리더), **릴리스**(DRAFT 누출·저작권)의 층위로 분리한다.

### PRD 요구사항 → 기술 검증 추적표
| PRD ID | 책임 기능 | 읽기 계약 | 테스트 |
|---|---|---|---|
| FR-001 | SSR/static pages | volumes read model | volume enumeration/links |
| FR-002 | static volume route | cross referenced people/events/docs | foreign-key and empty states |
| FR-003 | person route | global Person + alias mapping | crosswalk and deep migration |
| FR-004 | timeline route | Event.date_label + date_precision | approximate labels vs sorting |
| FR-005 | document route | Document+witness access tier | no full copyrighted text leakage |
| FR-006 | theme route | Topic links and related volumes | VOL-08 thematic only |
| FR-007 | place route | text-only location reference | zero false map coordinates |
| FR-008 | client search | approved-only SearchDocument fields | Korean/English search and zero leaks |
| FR-009 | linked cards | Relation: from/to/type/evidence | no untyped personal contact |
| FR-010 | provenance | SourceRef + verification scope | metadata vs primary original |
| FR-011 | build-time visibility gate | approved public catalogue vs local review-only data | unapproved excluded from HTML/JS/JSON/media |
| FR-012 | responsive styles | semantic HTML + progressive enhancement | keyboard/mobile/a11y |
| FR-013 | empty and pending states | content status enum per record | no fabricated content |
| FR-014 | revision trail | Git SHA and content version fields | stable URL after increment |
| FR-015 | navigation | typed routes and breadcrumbs | direct link and back navigation |
| FR-016 | future map module | verified coordinates in geodata extension only | P1 no fake pins |
| FR-017 | deep content block adapter | same global identity and content-depth sections | no route rewrite |
| FR-018 | future graph visualization | typed, cited relations only | P1 do not infer travel |

## 9. 비기능 요건과 운영
- **접근성:** WCAG 2.2 AA 지향. 핵심 탐색은 모든 의미가 읽기 순서/텍스트로 전달되어야 한다.
- **성능 예산 가정:** 대표 페이지 LCP 2.5초, 검색 응답 600ms. 실제 빌드 후 기기/네트워크 기준을 정해 조정.
- **저작권:** 외부 이미지 무단 사용 금지. 자료는 원문/소장자 링크·자체 요약과 직접 제작 시각자료를 중심으로 전시.
- **버전:** 콘텐츠 변환 결과에 소스 커밋·데이터 버전 기록, 릴리스 명세/롤백 기록 보존.
- **보안:** 외부 스크립트 최소, 임의 HTML 삽입 통제, `rel=noopener noreferrer`, CSP/HTTP headers 후보, 종교·개인정보 수집 최소화(P0 사용자 계정 없음).
- **운영 효율:** 변환 및 검사 CI, 최종 배포는 승인 받은 릴리스 브랜치에서만 실행.

## 10. 웹 개발 전 결정할 항목
- ADR-001~006에 대한 기술·예산 적합성 최종 결정(Astro/정적/호스팅 추천은 현재 **잠정**).
- 인물 33명의 정식 글로벌 ID 할당 방식과 별칭 URL 유지 정책.
- 내부 검토용 데이터 접근 방식과 정적 배포 보호 여부.
- 편집자가 GitHub PR을 통한 배포 승인으로 충분한지 또는 운영 UI가 필요한지.
- 이미지 업로드·권리 기록/라이선스 검증과 역사학 전문가 감수 절차의 역할.
- URL/slugs와 콘텐츠 버전·배포 스냅샷 구조.

## 11. 다음 산출물
다음 순서: **UX/UI 정보구조·와이어프레임** → **TASKLIST 구현 단위** → **사람 승인 후 웹 MVP 코드** → **심층 콘텐츠 추가**.

**상태: `TRD_DRAFT_READY / USER_APPROVAL_PENDING / UXUI_NOT_STARTED / WEBSITE_NOT_BUILT / PUBLICATION_GATE_CLOSED`.**
