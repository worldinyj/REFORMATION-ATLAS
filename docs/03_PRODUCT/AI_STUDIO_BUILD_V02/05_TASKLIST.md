# 05 · TASKLIST V0.2 — Google AI Studio Build용 실행 작업표

> 2026-10-25 · **DRAFT / 개발 미착수** · [PLAN](01_PROJECT_PLAN.md) · [PRD](02_PRD.md) · [TRD](03_TRD.md) · [UX/UI](04_UXUI.md)
> 1차 목표: AI Studio 내부에서 8권의 **현대적 미니멀 웹 골격** 생성·검증 → 제3권/루터 심층 콘텐츠는 추후 점진적으로 추가.
> 일괄 생성된 이 Tasklist의 모든 개발 Task는 `NOT_STARTED`이며, GitHub에 문서가 있다는 이유로 자동 완료하지 않는다.

## 0. 웹 개발 전에 먼저 수행해야 하는 공통 필수 작업
- **AT-001은 GitHub 실물 설계 자료 검토가 먼저**: [00 사전 감사](00_GITHUB_DESIGN_PREFLIGHT.md)로 PROJECT PLAN→PRD→TRD→UXUI→TASKLIST, 디자인 토큰, 한국어·영문 프롬프트, 입력 JSON 사이의 일관성·유기성·통일성을 확인한다. 작은 모순은 diff로 수정·재검증하고, GitHub에 접근 불가 또는 중대 모순이면 `PREBUILD_GATE=BLOCKED`로 앱 생성 금지.
- **AT-004 최초 앱 생성은 AT-001~003 완료 및 설계 범위 승인 후에만** 시작. 첫 앱은 역사 **OVERVIEW 개요**와 8권·공통 상세 뼈대, 이후 위클리프·얀 후스·루터 등 **DEEP_RESEARCH**가 준비되면 동일 ID/URL의 상세 섹션만 증분 추가.
- **AT-026/029 핵심 검수는 모바일 우선**: 320/360/375/390/430px + 태블릿 768/1024px + 데스크톱 1440px. 모바일 검색·연대표·문헌·출처·필터 등 기능 축소 금지. 실제 검증 전 PASS 처리하지 않는다.
- **작업 수량과 상태 불변**: 36개 Task(AT-001~036, P0 33/P1 3), 전부 `NOT_STARTED`이며 웹 코드/공개 배포 미실행. 이번 변경은 완료 기준을 강화한 설계 업데이트다.

## 1. 단계
- G0 **사람 검토/설계 결정**: 디자인·범위/AI Studio 연결·출판 게이트, 브랜치 고정
- G1 **AI Studio 첫 생성 + 데이터 정규화**: React TS, 토큰, ID/출처/권리 계약
- G2 **화면 구성**: 홈·8권·인물·연대표·문헌·사상/주제·장소
- G3 **정보 연결**: 검색·관계·출처 상태·빈 상태
- G4 **QA/버전 관리**: 모바일·접근성·비공개 데이터 격리·GitHub diff·수용
- P1 **심층 확장**: 고증된 지도·심층 원전·연결 관계 시각화

## 2. 전체 36개 Task
| ID | 단계 | 우선도 | 작업 | 선행 조건 | PRD |
|---|---|---|---|---|---|
| AT-001 | G0 | P0 | 설계/개발 범위 결정 기록 | — | FR-011, FR-015 |
| AT-002 | G0 | P0 | 원본 저장소/분기 정책 확정 | AT-001 | FR-014, FR-011 |
| AT-003 | G0 | P0 | AI Studio 연결·프리뷰 접근 안전 점검 | AT-001, AT-002 | FR-011 |
| AT-004 | G1 | P0 | Google AI Studio 초기 Build 프롬프트 적용 | AT-001, AT-002, AT-003 | FR-001, FR-012 |
| AT-005 | G1 | P0 | 디자인 토큰과 전역 CSS 단일화 | AT-004 | FR-012 |
| AT-006 | G1 | P0 | 공통 Header Footer BreadCrumb EmptyState | AT-004, AT-005 | FR-012, FR-015, FR-013 |
| AT-007 | G1 | P0 | JSON 소스 loader와 타입 검증 | AT-004 | FR-001, FR-002, FR-003 |
| AT-008 | G1 | P0 | OV-P↔PER 글로벌 인물 ID alias 해석 | AT-007 | FR-003, FR-014 |
| AT-009 | G1 | P0 | 개요/심층 콘텐츠 DepthBlock 스키마 | AT-007, AT-008 | FR-014, FR-017 |
| AT-010 | G1 | P0 | 승인 별도 PUBLIC snapshot 빌더 | AT-003, AT-007 | FR-011 |
| AT-011 | G1 | P0 | 자료 출처/판본/권리 Badge 아닌 메타텍스트 계약 | AT-007 | FR-010, FR-005 |
| AT-012 | G2 | P0 | 홈 히어로·8권 카드 | AT-005, AT-006, AT-007, AT-010 | FR-001 |
| AT-013 | G2 | P0 | 권 전체 목록과 권별 상세 화면 | AT-012 | FR-002 |
| AT-014 | G2 | P0 | 인물 목록·권/이름 필터 | AT-006, AT-007, AT-008, AT-013 | FR-003 |
| AT-015 | G2 | P0 | 인물 상세 공통 템플릿 | AT-009, AT-011, AT-014 | FR-003, FR-009, FR-014 |
| AT-016 | G2 | P0 | 사건 목록·연대표 | AT-007, AT-013 | FR-004 |
| AT-017 | G2 | P0 | 사건 상세 및 관련 콘텐츠 | AT-016, AT-015 | FR-004, FR-009 |
| AT-018 | G2 | P0 | 문헌 목록·판본 필터 | AT-007, AT-011, AT-013 | FR-005 |
| AT-019 | G2 | P0 | 문헌 상세·사료 증거 수준 | AT-018, AT-015 | FR-005, FR-010 |
| AT-020 | G2 | P0 | VOL-08 및 주제 10건 목록·상세 | AT-013, AT-015 | FR-006 |
| AT-021 | G2 | P0 | 장소 22건 텍스트 목록 | AT-007, AT-013 | FR-007 |
| AT-022 | G3 | P0 | 관계 32건 링크 의미 시각적으로 표시 | AT-008, AT-015, AT-017, AT-019, AT-020 | FR-009 |
| AT-023 | G3 | P0 | 한국어/원어/영문 단순 검색 인덱스 | AT-007, AT-010, AT-014, AT-016, AT-018, AT-020 | FR-008 |
| AT-024 | G3 | P0 | 상태·출처·저작권 표시 UI 일괄 적용 | AT-011, AT-015, AT-017, AT-019, AT-022 | FR-010, FR-013 |
| AT-025 | G3 | P0 | 빈 데이터·없는 URL·검색 결과 없음 | AT-006, AT-023 | FR-013, FR-015 |
| AT-026 | G4 | P0 | 반응형·키보드 사용성·대비 검사 | AT-012, AT-013, AT-014, AT-015, AT-016, AT-018, AT-020, AT-021, AT-023, AT-024, AT-025 | FR-012 |
| AT-027 | G4 | P0 | PUBLIC 아티팩트 전체 비공개 누출 검사 | AT-010, AT-023, AT-024 | FR-011 |
| AT-028 | G4 | P0 | 문헌 원문·이미지 권리 점검 | AT-011, AT-019, AT-027 | FR-005, FR-011 |
| AT-029 | G4 | P0 | UI 밀도·여백·마이크로인터랙션 리뷰 | AT-026 | FR-012 |
| AT-030 | G4 | P0 | 전체 딥링크/라우팅/검색 회귀 QA | AT-015, AT-017, AT-019, AT-023, AT-025, AT-026 | FR-008, FR-015 |
| AT-031 | G4 | P0 | AI Studio→GitHub 동기화 diff 점검 | AT-002, AT-030 | FR-014 |
| AT-032 | G4 | P0 | 로컬 비공개 프리뷰 및 최종 수용 기록 | AT-026, AT-027, AT-028, AT-029, AT-030, AT-031 | FR-001, FR-011, FR-012 |
| AT-033 | G4 | P0 | 외부 배포 승인/호스팅 비용 검토 | AT-032 | FR-011 |
| AT-034 | P1 | P1 | 역사 지리 좌표 검증 후 지도 기능 | AT-021, AT-033 | FR-016 |
| AT-035 | P1 | P1 | 심층 연구 블록/주석 점진 추가 | AT-009, AT-015, AT-033 | FR-017 |
| AT-036 | P1 | P1 | 관계도/학습경로 | AT-022, AT-033 | FR-018 |

## 3. Task 완료 기준·검증
### AT-001 · 설계/개발 범위 결정 기록
- 상태: **NOT_STARTED** · G0/P0
- 선행: 없음
- 인수 조건: GitHub에서 5대 설계 문서·토큰·한국어/영문 생성 프롬프트·개요 JSON의 접근 여부와 일관성/유기성/통일성을 먼저 점검하고 FR18·화면14·Task36·ID·게이트·모바일 항목의 PREBUILD_GATE=PASS 감사표와 사용자의 설계 범위 승인 기록을 확보. 접근 불가/BLOCKER면 NO BUILD.
- QA: inspected branch/paths + consistency matrix(PASS/WARN/BLOCKER) + 최소 수정 diff + 실제 실행 QA + 사용자 승인; GitHub 미연결 시 STOP
- PRD 추적: FR-011, FR-015

### AT-002 · 원본 저장소/분기 정책 확정
- 상태: **NOT_STARTED** · G0/P0
- 선행: AT-001
- 인수 조건: GitHub 작업용 브랜치와 apps/web 경계, 충돌 해결 방식 확정
- QA: 원본 연구 8권·제3권 파일 diff 0
- PRD 추적: FR-014, FR-011

### AT-003 · AI Studio 연결·프리뷰 접근 안전 점검
- 상태: **NOT_STARTED** · G0/P0
- 선행: AT-001, AT-002
- 인수 조건: AI Studio 연결·권한 확인 및 모바일 핵심 경로의 테스트 장치/브라우저 조건(320/360/375/390/430/768/1024/1440, Safari/Chrome)을 기록하고 공유/Publish 미실행 확인
- QA: 브랜치·접근권한·비밀키·모바일 테스트 계획 및 Publish=0
- PRD 추적: FR-011

### AT-004 · Google AI Studio 초기 Build 프롬프트 적용
- 상태: **NOT_STARTED** · G1/P0
- 선행: AT-001, AT-002, AT-003
- 인수 조건: AT-001 PREBUILD_GATE=PASS/사용자 검토 후 Google AI Studio B1 React+TS 앱 골격 생성, OVERVIEW 기반 8권/상세 템플릿과 미래 DEEP_RESEARCH 슬롯·모바일 동등 UX 확보
- QA: 깃허브 감사 PASS 증거, 홈·권·모바일 320/375/390/430/데스크톱 1440 실측 또는 NOT TESTED, Git diff
- PRD 추적: FR-001, FR-012

### AT-005 · 디자인 토큰과 전역 CSS 단일화
- 상태: **NOT_STARTED** · G1/P0
- 선행: AT-004
- 인수 조건: 01~08권 전체 동일 색상·타이포·폭·간격
- QA: 320/375/768/1440px 확인
- PRD 추적: FR-012

### AT-006 · 공통 Header Footer BreadCrumb EmptyState
- 상태: **NOT_STARTED** · G1/P0
- 선행: AT-004, AT-005
- 인수 조건: 접근성 헤더·내비·페이지 컨테이너·404·빈 화면
- QA: keyboard tab order, skip link
- PRD 추적: FR-012, FR-015, FR-013

### AT-007 · JSON 소스 loader와 타입 검증
- 상태: **NOT_STARTED** · G1/P0
- 선행: AT-004
- 인수 조건: 기존 127개 JSON 항목·32관계 소스에서 읽기
- QA: count assertion + no source edits
- PRD 추적: FR-001, FR-002, FR-003

### AT-008 · OV-P↔PER 글로벌 인물 ID alias 해석
- 상태: **NOT_STARTED** · G1/P0
- 선행: AT-007
- 인수 조건: 발도·위클리프·후스 3인 동일 인물/안정된 URL
- QA: crosswalk 3/3, duplicate link 0
- PRD 추적: FR-003, FR-014

### AT-009 · 개요/심층 콘텐츠 DepthBlock 스키마
- 상태: **NOT_STARTED** · G1/P0
- 선행: AT-007, AT-008
- 인수 조건: OVERVIEW 콘텐츠를 유지한 동일 canonical ID/URL의 후속 DEEP_RESEARCH/PRIMARY_WITNESS 블록 및 승인·개정 이력 스키마
- QA: 후스/루터 샘플 fixture 추가 전후 URL·관계·개요 보존, 공개 승인 없는 블록 제외
- PRD 추적: FR-014, FR-017

### AT-010 · 승인 별도 PUBLIC snapshot 빌더
- 상태: **NOT_STARTED** · G1/P0
- 선행: AT-003, AT-007
- 인수 조건: 미승인 원고·이미지를 html/js/json/search에서 제외
- QA: 승인 0 → 공용 데이터 0 / 실패 시 block
- PRD 추적: FR-011

### AT-011 · 자료 출처/판본/권리 Badge 아닌 메타텍스트 계약
- 상태: **NOT_STARTED** · G1/P0
- 선행: AT-007
- 인수 조건: 출처 23, 별칭 2, 원본/번역/서평, DRAFT 표기
- QA: 11 rechecked vs others clearly labelled
- PRD 추적: FR-010, FR-005

### AT-012 · 홈 히어로·8권 카드
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-005, AT-006, AT-007, AT-010
- 인수 조건: 타이포 중심 미니멀 홈, 8권 4×2/2×4/1열
- QA: 권 카드 8/8 및 VOL-08 횡단 자료실
- PRD 추적: FR-001

### AT-013 · 권 전체 목록과 권별 상세 화면
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-012
- 인수 조건: 8권 개요, 핵심 인물·사건·문헌·주제 링크
- QA: 8 상세 직접 URL·필터
- PRD 추적: FR-002

### AT-014 · 인물 목록·권/이름 필터
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-006, AT-007, AT-008, AT-013
- 인수 조건: 33 인물, 한글/영어 이름, 사전 알파벳 결합 아닌 정렬
- QA: 33 entries local review, zero duplication
- PRD 추적: FR-003

### AT-015 · 인물 상세 공통 템플릿
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-009, AT-011, AT-014
- 인수 조건: 개요·활동·관련 사건·문헌·출처·심화 공간
- QA: 루터/후스/발도 상세 + empty depth
- PRD 추적: FR-003, FR-009, FR-014

### AT-016 · 사건 목록·연대표
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-007, AT-013
- 인수 조건: 34사건, dateLabel/datePrecision 유지
- QA: 1420 전후·1435 편집 추정 위조 금지
- PRD 추적: FR-004

### AT-017 · 사건 상세 및 관련 콘텐츠
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-016, AT-015
- 인수 조건: 연대·문헌·인물 연결, 출처 링크
- QA: deep URL/return navigation
- PRD 추적: FR-004, FR-009

### AT-018 · 문헌 목록·판본 필터
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-007, AT-011, AT-013
- 인수 조건: 20문헌, 원작/번역/편집과 자체 개요
- QA: 유료 문헌 본문 없음
- PRD 추적: FR-005

### AT-019 · 문헌 상세·사료 증거 수준
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-018, AT-015
- 인수 조건: 원어 제목·판본·접근 범위·외부 출처
- QA: 후스 1915 영어 번역=원어 원전 아님
- PRD 추적: FR-005, FR-010

### AT-020 · VOL-08 및 주제 10건 목록·상세
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-013, AT-015
- 인수 조건: 성경·교회론·성찬론 등 10개 cross-volume 탐색
- QA: VOL-08 not eighth chronological era
- PRD 추적: FR-006

### AT-021 · 장소 22건 텍스트 목록
- 상태: **NOT_STARTED** · G2/P0
- 선행: AT-007, AT-013
- 인수 조건: 현대 지명 기반 설명과 관련 사건, 고증 안된 지도 없음
- QA: 지도 핀/좌표 0
- PRD 추적: FR-007

### AT-022 · 관계 32건 링크 의미 시각적으로 표시
- 상태: **NOT_STARTED** · G3/P0
- 선행: AT-008, AT-015, AT-017, AT-019, AT-020
- 인수 조건: 문헌 영향/후대 수용/공동 활동 구별
- QA: textual_influence≠direct mentor
- PRD 추적: FR-009

### AT-023 · 한국어/원어/영문 단순 검색 인덱스
- 상태: **NOT_STARTED** · G3/P0
- 선행: AT-007, AT-010, AT-014, AT-016, AT-018, AT-020
- 인수 조건: 승인된 데이터만 PUBLIC 색인, 내부 프리뷰는 DRAFT 고지
- QA: 루터/Luther/Hus/후스/1517/성찬론
- PRD 추적: FR-008

### AT-024 · 상태·출처·저작권 표시 UI 일괄 적용
- 상태: **NOT_STARTED** · G3/P0
- 선행: AT-011, AT-015, AT-017, AT-019, AT-022
- 인수 조건: 페이지에 검증 한계·원전 층위·출처 링크
- QA: source links live, badges not overused
- PRD 추적: FR-010, FR-013

### AT-025 · 빈 데이터·없는 URL·검색 결과 없음
- 상태: **NOT_STARTED** · G3/P0
- 선행: AT-006, AT-023
- 인수 조건: 404/미검토/심층 준비중/0건 결과 구별
- QA: screen reader result summary
- PRD 추적: FR-013, FR-015

### AT-026 · 반응형·키보드 사용성·대비 검사
- 상태: **NOT_STARTED** · G4/P0
- 선행: AT-012, AT-013, AT-014, AT-015, AT-016, AT-018, AT-020, AT-021, AT-023, AT-024, AT-025
- 인수 조건: 모바일 320/360/375/390/430px과 태블릿 768/1024px, 데스크톱 1440px에서 홈·8권·인물·연대표·문헌·검색·출처의 동일 기능과 가독성, 키보드/터치/포커스/가로넘침 0 검증
- QA: 모바일 화면별 기록 및 iOS Safari/Android Chrome 실행 여부, 44px 터치 권장, 16px 본문·safe-area·메뉴 Escape/focus·reduced-motion
- PRD 추적: FR-012

### AT-027 · PUBLIC 아티팩트 전체 비공개 누출 검사
- 상태: **NOT_STARTED** · G4/P0
- 선행: AT-010, AT-023, AT-024
- 인수 조건: dist, json, JS, sitemap, assets에서 DRAFT/AI 이미지 제외
- QA: approved 0 → public records 0
- PRD 추적: FR-011

### AT-028 · 문헌 원문·이미지 권리 점검
- 상태: **NOT_STARTED** · G4/P0
- 선행: AT-011, AT-019, AT-027
- 인수 조건: 유료 전문 미복제, 미승인 역사화, 출처 종류 분리
- QA: 22 unverified place pins and candidate assets 0
- PRD 추적: FR-005, FR-011

### AT-029 · UI 밀도·여백·마이크로인터랙션 리뷰
- 상태: **NOT_STARTED** · G4/P0
- 선행: AT-026
- 인수 조건: Quiet Editorial Atlas의 모바일 20px 여백·단일 열·48~64px 섹션과 데스크톱 4열/최대1200px의 여백과 가독성 품질 동시 평가
- QA: 320/390/430/1440 스크린샷 비교, 사용성/접근성 미수행 항목 NOT TESTED
- PRD 추적: FR-012

### AT-030 · 전체 딥링크/라우팅/검색 회귀 QA
- 상태: **NOT_STARTED** · G4/P0
- 선행: AT-015, AT-017, AT-019, AT-023, AT-025, AT-026
- 인수 조건: 14개 화면 URL, 브레드크럼/뒤로가기, 검색 무결성
- QA: no broken routes
- PRD 추적: FR-008, FR-015

### AT-031 · AI Studio→GitHub 동기화 diff 점검
- 상태: **NOT_STARTED** · G4/P0
- 선행: AT-002, AT-030
- 인수 조건: apps/web 경로 중심, 연구 데이터 변경 없음
- QA: user approves push on isolated branch
- PRD 추적: FR-014

### AT-032 · 로컬 비공개 프리뷰 및 최종 수용 기록
- 상태: **NOT_STARTED** · G4/P0
- 선행: AT-026, AT-027, AT-028, AT-029, AT-030, AT-031
- 인수 조건: 14화면/6여정/10수용 항목 검토 기록
- QA: human review; no publish
- PRD 추적: FR-001, FR-011, FR-012

### AT-033 · 외부 배포 승인/호스팅 비용 검토
- 상태: **NOT_STARTED** · G4/P0
- 선행: AT-032
- 인수 조건: 별도 콘텐츠·권리·코드 게이트; Cloud Run 가능성 검토
- QA: 명시적 승인 전 Deploy=NO
- PRD 추적: FR-011

### AT-034 · 역사 지리 좌표 검증 후 지도 기능
- 상태: **NOT_STARTED** · P1/P1
- 선행: AT-021, AT-033
- 인수 조건: 실제 근거 있는 지점만 pin, 사상 관계는 경로 아님
- QA: 무증거 지명으로 지도 제작 0
- PRD 추적: FR-016

### AT-035 · 심층 연구 블록/주석 점진 추가
- 상태: **NOT_STARTED** · P1/P1
- 선행: AT-009, AT-015, AT-033
- 인수 조건: 위클리프·얀 후스·루터 등 인물/사건/문헌별 심층 연구가 준비될 때 같은 canonical ID/URL의 기존 OVERVIEW 아래 DEEP_RESEARCH 블록·원전 층위·개정·출처·승인 필드 추가
- QA: 심층 도착 전/후 같은 permalink와 관련 링크 유지, 개요 존재, 승인되지 않은 새 블록 공용 제외
- PRD 추적: FR-017

### AT-036 · 관계도/학습경로
- 상태: **NOT_STARTED** · P1/P1
- 선행: AT-022, AT-033
- 인수 조건: 교파별 이견, 직계/영향 구별, 접근성 있는 관계도
- QA: evidence labels + keyboard fallback
- PRD 추적: FR-018


## 4. AI Studio 실행 단위
- **입력 단위 0:** [06 마스터 프롬프트](06_MASTER_BUILD_PROMPT.md)를 AI Studio Build(웹앱)에 붙여넣고, 현재 디자인 문서·JSON 데이터 파일을 제공한다. 잘못 추측해서 데이터를 생성하지 않도록 한다.
- **입력 단위 1:** 홈·공통 레이아웃/디자인 시스템 (`AT-004~006,12`).
- **입력 단위 2:** 원본 데이터·ID/검증·출처 연결 (`AT-007~011`).
- **입력 단위 3:** 목록/상세/연대표/문헌/주제/검색 (`AT-013~025`).
- **입력 단위 4:** 모바일/접근성/공개 안전/동기화 (`AT-026~033`).
- **입력 단위 5:** 지도·심층 블록 등 P1 (`AT-034~036`). P1은 공개 승인 시점과 별개로 준비하며 미승인 고증 도상은 게시하지 않는다.

## 5. 최종 작업 인수 게이트
- FR-001~018 **18개 요구 모두 Task에 연결**, 의존 관계 순환/고아 없음.
- 수용 시험: 8권, 33인물, 34사건, 20문헌, 10주제, 22장소, 32관계.
- 검증된 좌표 0·미승인 AI 이미지 0. **데이터 원본의 DRAFT는 공개 승인 아님**.
- `AT-001~003` 설계/접근 범위 승인 전 Build 앱의 외부 공유·Publish를 하지 않는다.
- 사용자가 저장소를 연결하더라도 `main` 병합·자료 자동 승격·비밀키 추가를 독단적으로 하지 않는다.

**상태:** TASKLIST_V02_DRAFT_CREATED / TASKS_0_DONE / WEBSITE_NOT_BUILT / can_ship=false.
