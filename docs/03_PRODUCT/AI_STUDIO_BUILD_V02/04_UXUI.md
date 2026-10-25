# 04 · UX/UI V0.2 — Quiet Editorial Atlas
> 사용자 요구: **심플하고 여백의 미가 있으며 최신 감각의 현대적 웹 디자인**.
> 상태: DRAFT, Google AI Studio 코드 생성용 화면/디자인 명세 (실제 배포 화면 아님)

## 1. 디자인 철학
고대 문헌·교회사라는 주제를 다루되 **빈티지 양피지로 꾸미지 않는다**. 학술 출판물의 정돈된 편집 미감에 현대 디지털 프로덕트의 사용성을 결합한다. 첫 화면에 박물관처럼 느긋한 공기를 만들고, 세부 페이지는 읽기에 집중한다.

Design words: spacious / editorial / precise / modern / calm / humane.

절제된 서체 대비와 아주 얇은 경계선, 긴 호흡의 수직 간격, 1개 강조 색상만 사용. 유사 중세 표식·금박·그림자·보라색 AI 그라디언트·거대한 가짜 역사 초상·과도한 장식형 대시보드를 피한다.

## 2. 토큰
| 영역 | 제안 |
|---|---|
| canvas | #F7F8F5 |
| card/surface | #FFFFFF |
| primary text | #1C2925 |
| secondary text | #4B6058 |
| accent | #205F50 |
| separator | #DDE5DF |
| H1 | 데스크톱 56–68px / 모바일 36–42px |
| 본문 | 16–18px, line-height 1.7 |
| 사이트 폭 | max 1200px / 본문 max 720px |
| 가로 여백 | mobile 20 / tablet 32 / desktop 64px 이상 |
| 섹션 상하 | desktop 80–120 / mobile 48–64px |
| 그리드 | 4열 desktop / 2열 tablet / 1열 mobile |
| border/radius | 1px / 14px |
| micro-interaction | 120–200ms, prefers-reduced-motion 준수 |

권장 바디 폰트 Pretendard/Noto Sans KR/system-ui. 디스플레이에만 Noto Serif KR 선택적 사용(무작정 폰트 다운로드/파일 배포 금지). 캔버스 대비 본문색 약 14.14:1, 보조색 약 6.33:1, 포인트색 약 7.00:1 — 실제 화면 전체 WCAG 검증은 별도.

## 3. 사이트맵
- HOME / : 브랜드·큰 제목·8권 목차·시간 흐름 프리뷰·자료의 신뢰성 고지
- VOLUMES /volumes, VOLUME /volumes/:id : 권 목록/개관 및 연결
- PEOPLE /people, PERSON /people/:id : 인물 검색·상세/심층 확장 자리
- TIMELINE /timeline, EVENT /events/:id : 연대·사건 상세
- DOCUMENTS /documents, DOCUMENT /documents/:id : 저술·번역·판본/해설
- PLACES /places : 현대 지명 목록, 미검증 지도 핀은 없음
- TOPICS /topics, TOPIC /topics/:id : VOL-08 시대 횡단 테마
- SEARCH /search : 한국어·원어 별칭 통합 결과
- ABOUT /about : 연구 방식·출처·권리·AI 상상화 고지

## 4. 홈 — Desktop 구성
[1] Nav 72px: RA / REFORMATION ATLAS | 8권 | 인물 | 연대표 | 문헌 | 주제 | 검색

[2] Hero 320~450px: 위 작은 영어 Kicker, 왼쪽에 큰 한국어 H1 **시간을 따라, 사상을 건너, 사람을 만나다.** 2줄 설명. 오른쪽은 주로 **빈 여백**. 주요 CTA ‘8권 살펴보기’, 보조 링크 ‘연대표 보기’.

[3] Section separator: 1px hairline. Title: ‘8권으로 읽는 교회사’. 01~08 4×2 카드. 각 카드 번호·제목·2줄 개요와 작은 인터랙션. VOL-08은 아카이브라고 설명.

[4] 탐색 경로: 인물 / 연대표 / 문헌 — 타이포그래픽 링크 세 개. 이미지는 없음.

[5] Timeline teaser: 니케아(325), 후스(1415), 루터(1517), 조선 천주교(1784) 등 근거 있는 짧은 사건 표본. 자세한 연대표로 이동.

[6] Footer: 출처/편집 정책/저작권·AI 생성물 고지, 저장소 링크(원한다면).

## 5. 모바일 홈 375px
- 헤더 60px: RA Atlas / 검색 / 모바일 메뉴.
- 넓은 위아래 여백 뒤 H1 36–42px, 가독성 있는 3~4행.
- CTA를 세로로 쌓음.
- 8권 목록은 1열, 긴 이름은 2행 허용. 이미지를 억지로 배치하지 않음.
- 검색과 사상/문헌/연대표 진입 경로를 쉽게 찾음. 메뉴 열기/닫기와 ESC/포커스 복귀 지원.

## 6. 상세 화면 구성
**권 상세:** Breadcrumb → 권 번호/연도/큰 제목 → 2~3개 문단 시대 개관 → 관련 인물 → 핵심 사건 타임라인 → 대표 문헌 → 시대 간 주제 링크 → 출처.

**인물 상세:** Breadcrumb → 생애 연도/한글·영문 이름 → 3~5문장 개요 → 사건·문헌·관계 탭 → 심층 연구가 오면 같은 URL에 추가되는 DEEP_RESEARCH 블록. 미승인 초상 대신 큰 제목과 대표 연도를 사용.

**연대표:** 가벼운 세로선+연도+사건 본문. 반응형이고 자료 label을 정확히 표시(1420년 전후는 1420-01-01 아님). 필터는 한 줄.

**문헌:** 저자/연대/원어명/후대 판본·번역·서평/출처/접근 범위 → 본문 자체 요약. 전문 미열람을 원문 검증 완료로 표시하지 않음.

**주제:** 성찬론/칭의/교회론 등 → 여러 권의 인물/문헌 연결. 동일 학설이나 실제 직접 관계를 암시하지 않는 분명한 연결 설명.

**장소:** 현대 지명 카드/목록 + 역사 맥락. 좌표 고증 전 지도 컴포넌트 미생성.

**검색:** 하나의 큰 입력창 → 유형 필터 → 깔끔한 결과 리스트. 정상 결과/0건/기다리는 자료/권한 없는 자료 상태 구분.

## 7. 컴포넌트
- SiteHeader, MobileMenu, Breadcrumbs, Footer
- HeroTitle, VolumeCard, PersonCard, TimelineEntry
- DocumentRow, TopicCard, SourceCitation
- EvidenceNotice, ReviewStatusText, EmptyState
- SearchField, FilterChips(과도한 배지 대신 절제된 탭)
- DeepContentSection (후속 작업을 위한 빈 슬롯)

## 8. 상호작용과 접근성
- 키보드 탭/포커스, Skip to content, 본문 의미 구조, aria-label, 검색·필터의 label.
- 320/375/768/1024/1440px 시각 QA, 화면 가로 스크롤 0.
- hover뿐 아니라 focus-visible, disabled 상태. 터치 영역 44px 목표.
- 문맥 없는 '자세히' 링크 반복을 피하고 이름이 드러나는 링크 텍스트 사용.
- 출처·자료 상태는 작은 **일반 텍스트**로 표현, 색만으로 판단하지 않게 한다.
- 컨텐츠 승인 전 비공개 개인 미리보기에서만 DRAFT 안내. 공개 사이트에는 비승인 정보를 넣지 않는다.

## 9. 디자인 수용 기준
- 첫 화면에서 8권 개관이 자연스럽게 읽힘.
- 다섯 화면(홈, 권, 인물, 연대표, 문헌)이 같은 토큰과 여백 규칙으로 구성됨.
- 이미지 없이도 텍스트/그리드만으로 화면이 완성된 느낌.
- VOL-08은 8번째 시대가 아니라 주제·문헌 아카이브.
- 모바일에서 1열 목록과 메뉴를 잘 읽고 조작 가능.
- 나중에 위클리프·후스·루터 심층 블록을 넣어도 전체 디자인 개편 없이 수용.

상태: UX/UI 초안 완료, 코드·실제 시각 사용자 승인 대기.
