# REFORMATION ATLAS · UX/UI 구조 및 와이어프레임 V0.1
> 2026-10-25 · **DRAFT / 화면 설계 초안** · 상위 [PRD](ATLAS_PRD_V01.md), [TRD](ATLAS_TRD_V01.md)
> 와이어프레임은 **텍스트 구조도**이며 실제 HTML 페이지·디자인 시안·배포 화면이 아니다.

## 1. 정보 구조(IA)
```text
홈
├── 8권 둘러보기
│   ├── 1권 초대교회/고대교회 ─┐
│   ├── 2권 중세 교회       │
│   ├── 3권 선구자          │
│   ├── 4권 16세기 개혁     ├─ 개관 → 인물 → 사건 → 문헌 → 출처
│   ├── 5권 가톨릭 개혁     │                    └─ 관련 장소/사상
│   ├── 6권 부흥·세계선교   │
│   ├── 7권 세계·한국 교회사┘
│   └── 8권 사상·문헌 아카이브 → 주제 → 시대 횡단 자료 링크
├── 인물(한국어/원어/별칭)
├── 연대표(시간 정확도 구분)
├── 문헌(저술/판본/번역/연구 분리)
├── 사상·주제(10개)
├── 장소(현대 지명 목록 / 미검증 좌표 없음)
├── 통합 검색
└── 프로젝트 소개·출처·제작/검수 방법
```

## 2. 화면 원칙
- 공통: 상단 브랜드/검색, 1차 내비게이션, 위치 표시(브레드크럼), 콘텐츠 제목, 현재 데이터 종류와 기간, 출처·검토 한계, 관련 기록.
- 역사는 ‘화려한 포스터’보다 **읽기 쉬운 글과 연결 관계**를 우선. 그림은 승인된 경우에만 보조적 활용.
- 검증 상태를 색깔만으로 표현하지 않고 **'개요', '심층', '근거 확인', '추가 검토 중' 등 명확한 텍스트**로 표시. 공개 자료와 내부 검토의 UI를 혼동하지 않는다.
- 키보드 순서: Skip link → 브랜드/검색/메뉴 → 본문 H1 → 필터 → 카드 → 출처/부가 콘텐츠.
- 인물/문헌명은 한국어 기본+영문/라틴어 보조. 날짜는 `date_label`을 사람에게 그대로 표시.

## 3. 주요 화면 와이어프레임

### A. 홈 / (모바일 및 데스크톱)
```text
┌────────────────────────────────────────────────┐
│ REFORMATION ATLAS         8권  인물  연대표  🔎  │
├────────────────────────────────────────────────┤
│ [교회사와 종교개혁의 큰 흐름을 탐색하세요]       │
│ [역사적 시기/주제를 검색]                        │
│                                                │
│  [01 초대교회] [02 중세교회] [03 선구자] [04 개혁]│
│  [05 가톨릭]   [06 부흥]     [07 세계·한국]       │
│  [08 사상·문헌 자료실 : 시대를 가로지릅니다]    │
│                                                │
│  주요 사건의 흐름 → 인물 탐색 → 문헌과 근거 확인  │
│  [출처·역사 재현 고지]                           │
└────────────────────────────────────────────────┘
```
모바일에서는 8권 카드 한 열, 검색은 첫 화면 위쪽, 글로벌 메뉴는 한 개의 열림/닫힘 컨트롤. 대형 이미지·지도 대신 제목·간결한 텍스트가 우선.

### B. 권 상세 /volumes/:volumeId
```text
[홈 / 4권]
4권 · 16세기 종교개혁
시대 · 핵심 질문 · 4~8줄 개관
[인물] [사건] [문헌] [주제] [관련 장소]
인물 카드(대표 인물) → 인물 상세
연대순 사건(날짜 근사성 명시)
주제간 연결(다른 권으로 이동)
출처 · 더 깊이 읽기(준비중)
```

### C. 인물 상세 /people/:personId
```text
[홈 / 4권 / 인물 / 마르틴 루터]
마르틴 루터 | Martin Luther
1483~1546 · 종교개혁 (시대 개요)
[개요] [관련 사건] [주요 문헌] [사상과 관계]
인물 개관 / 역사적 논점 / 검토 근거
1517 면벌부 논쟁 → 1521 보름스 → 관련 문헌
+ 심층 블록 (승인 전에는 공용 페이지에 추가하지 않음)
[작성/검토 상태] [출처·자료 한계]
```
**한 페이지를 지속적으로 깊게 만드는 방식**을 전제한다. `OVERVIEW` 개요를 삭제하고 새 페이지를 만드는 것이 아니라 같은 안정적인 ID 아래 `DEEP_RESEARCH` 블록을 추가한다.

### D. 연대표 /timeline
```text
[전체 시대] [권 필터] [주제 필터] [연도 범위]
325년            니케아 공의회
1420년 전후      프라하 4개조 (근사 연대)
1435년 7월 추정  브르노 문안 (편집자의 추정)
1436-07-05       이흘라바 공적 선포
1436-07-06       옛 체코어 문안 낭독
1517년           95개조 논제
...
```
정렬 숫자는 이용자에게 정확한 날짜로 보이지 않음. 중요한 두 사건이 같은 근처에 위치하더라도 데이터에 없는 인과를 자동 생성하지 않음.

### E. 문헌 상세 /documents/:documentId
```text
[문헌 제목] · [원어 제목]
시대/작성 맥락 · 판본/번역/서평 종류
짧은 해설 (자체 저술 요약)
[원저술 존재] [직접 확인 범위] [번역 종류]
주요 연결 인물·사건·주제
[외부 출처 열기] → 새 사이트
미열람/유료 원문 전문 미수록 고지
```

### F. 통합 검색 /search
```text
[검색어 입력: 루터 / Luther / 성찬론 ...] 🔍
[전체] [인물] [사건] [문헌] [주제] [권]
결과 건수
- [인물] 마르틴 루터 · 1483~1546
- [사건] 1517년 95개조 논쟁
- [문헌] 95개조 논제 · 1517
[자료 없음 / 검증 대기 상태]
```
검색결과는 **인가된 배포물 기준의 인덱스만** 사용. DRAFT 내용이 검색어 자동완성·색인용 JS에 섞여 누출되지 않도록 함.

### G. 장소 /places (P0)
현대 지명 22곳을 텍스트 목록으로 보여주며 권/사건 필터만 사용. 지도 핀은 **0건 고증**이므로 지도 자체를 억지로 노출하지 않는다. 후속 P1에서 출처 근거가 있는 위치만 지도 UI를 추가한다.

### H. 8권 아카이브
VOL-08은 연대표/지역 시대 카드가 아니라 **성경·교회권위·성찬·은총·문헌 번역 등 주제 카드**를 중심으로 여러 권을 연결한다.

## 4. 14개 화면의 구성 요소·빈 상태
| 화면 ID | 제안 경로 | 목적 | 핵심 영역 | 상태 |
|---|---|---|---|---|
| SC-01 | `/` | 8권 개요와 시작할 탐색 경로 | HeroIntro, VolumeGrid, FeaturedTimeline, SourceMethodNote | DESIGN_DRAFT |
| SC-02 | `/volumes` | 8권 전체 구조 및 제8권의 자료실 성격 | VolumeGrid, VolumeSearch, PeriodVsArchiveLabels | DESIGN_DRAFT |
| SC-03 | `/volumes/:volumeId` | 권별 개요·관련 인물·사건·문헌·주제 | Breadcrumb, VolumeHeading, OverviewText, LinkedEntityTabs, Sources | DESIGN_DRAFT |
| SC-04 | `/people` | 인물 카드 검색·권별 필터 | SearchField, VolumeFilter, PersonCardGrid, PaginationIfNeeded | DESIGN_DRAFT |
| SC-05 | `/people/:personId` | 인물 개요, 관련 사건·문헌 및 심층 확장 공간 | Breadcrumb, PersonHeader, TimelineSnippet, RelatedDocuments, DepthSections, Provenance | DESIGN_DRAFT |
| SC-06 | `/timeline` | 사건 정렬·권 필터, 연대 정확성 안내 | EraFilter, DatePrecisionLegend, EventTimeline, SourceDrawer | DESIGN_DRAFT |
| SC-07 | `/events/:eventId` | 사건 상세 개요·관련 인물/문헌 | EventDateAndPrecision, EventNarrative, RelatedEntities, Provenance | DESIGN_DRAFT |
| SC-08 | `/documents` | 문헌 제목/판본/저술연대 기준 탐색 | DocumentFilter, WitnessTypeLegend, DocumentList | DESIGN_DRAFT |
| SC-09 | `/documents/:documentId` | 저술·편집판·번역/요약 출처를 정확히 구별 | BibliographyHeader, WitnessLayers, Summary, AccessLink, Provenance | DESIGN_DRAFT |
| SC-10 | `/places` | 현대 도시 지명과 역사적 맥락의 텍스트 목록 | PlaceList, VolumeFilter, GeolocationDisclaimer | DESIGN_DRAFT |
| SC-11 | `/topics` | 10개 시대 횡단 핵심 주제 | TopicGrid, CrossVolumeLabels, SourceNote | DESIGN_DRAFT |
| SC-12 | `/topics/:topicId` | 관련 권·인물·사건·문헌으로 가는 주제 허브 | TopicIntro, ComparisonSummary, RelatedEntities, SourceNotes | DESIGN_DRAFT |
| SC-13 | `/search` | 한국어·영문·라틴어 별칭 통합 검색 | QueryInput, TypeFilters, SearchResults, ZeroResults | DESIGN_DRAFT |
| SC-14 | `/about` | 프로젝트 범위·출처·역사학/AI 이미지 고지 | Methodology, EditorialStatus, VersionNotice, ContactLater | DESIGN_DRAFT |

**빈 상태:** '해당 필터에 결과 없음'·'아직 자료 미준비'·'승인된 자료 없음'을 구분. 존재하지 않는 사건/문헌을 AI로 생성하거나 외부 승인 없는 이미지를 임시로 노출하지 않는다.

## 5. 모바일/태블릿/데스크톱
| 구간 | 임시 기준 | 동작 |
|---|---|---|
| 작은 모바일 | 320px~767px | 카드 1열, 전체 너비 입력, 햄버거 메뉴, 표는 가로 스크롤/대체 리스트 |
| 태블릿 | 768px~1199px | 권 카드 2~3열, 필터는 접을 수 있음 |
| 데스크톱 | 1200px 이상 | 권 카드 4열, 페이지 최대 폭 제한, 본문 좌·연관 링크 우 |
| 구현 검사 지점 | 320/375/768/1024/1440px | 줄바꿈·접근성·출처 링크 위치 검사 |

폭 숫자는 설계 후보이며 시각 점검 후 확정한다. 읽기 본문 최대 폭 약 46rem, 정보 카드 격자 약 76rem을 후보로 제안한다.

## 6. 디자인 시스템 초안
- **톤:** 깨끗한 편집형 아카이브. 과한 장식이나 유사 중세 장식 배경은 피함. 8권에 일관된 텍스트 계층.
- **컬러:** 종이색에 가까운 중립 배경·진한 본문 잉크·절제된 하나의 포인트 색상. 실제 HEX·AA 대비는 시각 시안/구현 이후 결정.
- **타이포:** 한국어 본문은 화면에서 읽기 좋은 산세리프. 헤더는 선택적으로 절제된 세리프 활용. 역사 고유명사/라틴어 가독성 검사.
- **간격:** 4/8px 기반 후보, 카드 높이는 고정하지 않아 긴 인물명·한글/영문 혼합을 지원.
- **컴포넌트:** Header, Breadcrumb, SourceLink, ProvenanceTag, VolumeCard, PersonCard, TimelineEvent, WitnessLayer, EmptyState, MobileNav, TopicConnector.
- **접근성:** WCAG 2.2 AA 지향. 일반 본문 대비 4.5:1 이상, 큰 글자 3:1 이상, 포커스·오류 텍스트 명확성. 터치 영역은 실사용성 차원에서 여유 있는 44~48px를 권장하되 WCAG 2.2의 기본 최소 요구와 혼동하지 않음. 링크는 색상 외 밑줄/텍스트 표시.

## 7. 출처/사실성 표시 패턴
| 상황 | 권장 표시 | 피해야 할 표시 |
|---|---|---|
| 개요 서술 | “시대 개요 · 출처 확인 범위” | “원전 전체 사실 검증 완료” |
| 특정 역사 해석 | “학자/전통 A는 ~로 해석” | 한 전통의 해석을 절대적 사실로 단정 |
| 1435 브르노 | “1435년 7월 추정(무날짜 원문)” | 날짜 확정 또는 1436과 합침 |
| AI 인물화 | “현대 AI 상상 재현” + alt + 검토/권리 | 생전 실사·당대 초상으로 오인 |
| 현대 지명 | “오늘날의 도시명 · 관련 역사” | 중세 사건의 정확한 지도 좌표 |
| 문헌 접근 | “후대 번역/편집본, 요약 제공” | 전문 미열람 상태에서 ‘원문 대조 완료’ |

## 8. 사용자 흐름
- **FLOW-01: 처음 방문 → 인물** — home → volumes → volume → person → events → document; 수용시험: 권→인물→사건→문헌으로 탐색
- **FLOW-02: 검색 → 역사 주제** — search → topics → topic → person; 수용시험: 루터, Luther, 성찬론 별칭
- **FLOW-03: 연대의 불확실성 이해** — timeline → events → document; 수용시험: 1420년 전후/1436-07-05/06 구분
- **FLOW-04: 한국인 초기 신앙사** — volumes → volume → timeline → people; 수용시험: VOL-07의 1784/1880년대 차이
- **FLOW-05: 문헌 판본 한계 알기** — documents → document → about; 수용시험: 원저작/번역/서평 구별
- **FLOW-06: 개요에서 심층 확장** — people → person → document; 수용시험: 깊이 블록 추가 시 URL·ID 유지

## 9. 다음 단계로 전달할 기준
- **Tasklist에는** 모든 14화면의 UI 상태(데스크톱/모바일), 컴포넌트, 출처 표시, 검색 0건, 콘텐츠 승인 0건 테스트가 포함돼야 함.
- 트리 메뉴/와이어프레임은 실제 UI가 아니며 사용성 테스트·시각 승인 이후 코드로 옮긴다.
- 권별 카드/연대표/관계 링크는 승인된 데이터만 공개. 초기 전체 자료는 내부 검토에서 이용자에게 DRAFT 경고.
- 웹/이미지·지도·설교 공간의 역사 재현 학술 승인은 별개로 유지.

**최종 게이트:** `UXUI_DRAFT_READY`, `HUMAN_VISUAL_APPROVAL=false`, `WEBSITE_NOT_BUILT`, `can_ship=false`.
