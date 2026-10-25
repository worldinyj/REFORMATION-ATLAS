# 05 · TASKLIST V0.2 — Google AI Studio Build 실행 작업
> 2026-10-25 · **일괄 작성 완료 / 실제 앱 구현은 미시작**.
> 디자인 기준: Quiet Editorial Atlas · 소스: [PROJECT PLAN](01_PROJECT_PLAN.md) / [PRD](02_PRD.md) / [TRD](03_TRD.md) / [UXUI](04_UXUI.md)
> 마스터 프롬프트는 [06](06_AI_STUDIO_MASTER_PROMPT.md), 단계별 증분 지시는 [07](07_AI_STUDIO_ITERATION_PROMPTS.md).

## 운영 방법
- B1(화면 뼈대) → B2(실제 데이터/출처) → B3(상세·탐색) → B4(품질/동기화) 순서로 **한 번에 한 기능군씩 Google AI Studio에게 생성 요청**.
- 각 단계에서 생성 코드를 확인하고 앱 미리보기/콘솔 빌드 오류를 수정한 다음 다음 프롬프트 실행.
- `T-001` 설계 검토와 `T-005` 공개/권리 경계가 준비되기 전 공유/배포 금지.
- 구현 작업 상태 전부 `NOT_STARTED`. 이 목록의 존재는 웹 구축 완료가 아니다.

## 작업 표 — 34개
| ID | 단계 | 우선순위 | 작업 | 선행 | PRD |
|---|---|---|---|---|---|
| T-001 | S0 | P0 | 설계 5문서/디자인 토큰과 사용 승인 범위 대조 | — | FR-011, FR-015 |
| T-002 | S0 | P0 | Google AI Studio Build Web 모드 및 프로젝트 생성 준비 | T-001 | FR-015 |
| T-003 | S0 | P0 | GitHub 기능 브랜치·동기화 방식 확인 | T-002 | FR-014 |
| T-004 | S0 | P0 | 개요 데이터 127건·관계 32건/출처 23건 실제 읽기 진단 | T-003 | FR-001, FR-010 |
| T-005 | S0 | P0 | DRAFT/시연용 데이터 경계·접근제어 계획 | T-001 | FR-011 |
| T-006 | B1_UI | P0 | 첫 Build 프롬프트로 React TypeScript 앱 골격 생성 | T-001, T-002, T-005 | FR-012, FR-015 |
| T-007 | B1_UI | P0 | 토큰/CSS/읽기 폭/헤더·모바일 메뉴 | T-006 | FR-012, FR-015 |
| T-008 | B1_UI | P0 | 홈 편집형 Hero/8권 카드·CTA | T-007 | FR-001 |
| T-009 | B1_UI | P0 | 권 목록·권 상세 기본 템플릿 | T-008 | FR-002 |
| T-010 | B1_UI | P0 | 로컬 데모 상태/404/빈 상태 | T-006, T-009 | FR-013, FR-015 |
| T-011 | B1_UI | P0 | 모바일 320/375/768/1440 디자인 1차 검수 | T-007, T-008, T-009 | FR-012 |
| T-012 | B2_DATA | P0 | Git JSON/Markdown read-only 어댑터·타입 검사 | T-004, T-006 | FR-001, FR-002, FR-014 |
| T-013 | B2_DATA | P0 | 인물 3건 OV-P ↔ PER 글로벌 ID 대응 | T-012 | FR-003, FR-014 |
| T-014 | B2_DATA | P0 | 문헌·출처 계층/URL·라이선스 분리 | T-012 | FR-005, FR-010 |
| T-015 | B2_DATA | P0 | 34개 사건 정밀도·정렬·연대표 어댑터 | T-012 | FR-004 |
| T-016 | B2_DATA | P0 | 출판 allowlist와 빌드 결과 누출 검사 | T-005, T-012 | FR-011 |
| T-017 | B3_PAGES | P0 | 인물 목록/상세/관련 항목 연결 | T-013, T-016, T-009 | FR-003, FR-009 |
| T-018 | B3_PAGES | P0 | 사건 상세·연대표 화면 | T-015, T-016, T-009 | FR-004, FR-009 |
| T-019 | B3_PAGES | P0 | 문헌 목록/상세·판본 상태 | T-014, T-016, T-009 | FR-005, FR-010 |
| T-020 | B3_PAGES | P0 | 주제 10개·VOL-08 횡단 자료실 | T-016, T-009 | FR-006, FR-009 |
| T-021 | B3_PAGES | P0 | 현대 지명 22곳 텍스트 목록 | T-016, T-009 | FR-007 |
| T-022 | B3_PAGES | P0 | 별칭 검색·유형 필터·빈 결과 | T-017, T-018, T-019, T-020 | FR-008, FR-013 |
| T-023 | B3_PAGES | P0 | 관계 타입·사실/해석·출처 UI | T-014, T-017, T-020 | FR-009, FR-010 |
| T-024 | B3_PAGES | P0 | 개요/심층 블록 확장과 수정 이력 모델 | T-013, T-017 | FR-014, FR-017 |
| T-025 | B4_QA | P0 | 14개 라우트/6개 대표 사용자 경로 회귀 검증 | T-017, T-018, T-019, T-020, T-021, T-022 | FR-015 |
| T-026 | B4_QA | P0 | 모바일·접근성·reduced-motion 전체 QA | T-025, T-011 | FR-012 |
| T-027 | B4_QA | P0 | 공개 권리/출처·역사 왜곡·미승인 미디어 자동검사 | T-016, T-023, T-025 | FR-010, FR-011 |
| T-028 | B4_QA | P0 | 프로젝트 빌드·성능·GitHub 기능 브랜치 동기화 | T-025, T-026, T-027 | FR-014, FR-015 |
| T-029 | B4_QA | P0 | 내부 시각검토·사용자 최종 수정 판정 | T-028 | FR-012, FR-015 |
| T-030 | B4_QA | P0 | 최초 공개 범위·접근 제어/배포별도 승인 | T-029 | FR-011 |
| T-031 | P1 | P1 | 심층 연구 블록 증분 추가(후스/위클리프/루터) | T-024, T-029 | FR-017 |
| T-032 | P1 | P1 | 지리학 고증 완료 좌표만 지도화 | T-021, T-030 | FR-016 |
| T-033 | P1 | P1 | 관계도·학습 흐름/동선 강화 | T-023, T-030 | FR-018 |
| T-034 | P1 | P1 | 새 권/신학 주제·참고 문헌 증분 갱신 루틴 | T-031, T-030 | FR-014, FR-017 |

## 마일스톤별 합격 기준
**S0 Preparation**
- AI Studio Build Web 앱 화면/계정/생성 방식 확인, GitHub 동기화 대상 브랜치 확인.
- 8권 데이터 원본을 AI Studio가 실제로 읽을 수 있는지 확인. 미연결 시 8권 표제만 포함한 **DEMO**로 시작.
- 원전 전문/비승인 그림/역사지도는 생성기가 임의로 만들거나 공개해서는 안 됨.

**B1 UI Skeleton**
- 타이포 중심 반응형 Hero, 8권 카드, 헤더, 모바일 메뉴, 전체 스타일 토큰.
- 빈 공간을 낭비가 아닌 의도적인 편집형 여백으로 사용.
- 320px에서도 H1/카드·메뉴가 잘림 없이 보이고 키보드 이동이 됨.

**B2 Data and Trust**
- 127개 개요 객체/32관계/23 출처를 실제 파일로부터 읽고 각 분류 개수를 보여주는 진단.
- OV-P 인물 3건 원형 매핑, source/status/permissions 분리.
- DRAFT의 외부 공개 0. 사용자 개인 시연과 외부 배포물 혼동 금지.

**B3 Content Journeys**
- 14개 제안 라우트/인물·연대표·문헌·주제·장소·검색.
- 한국어/원어 검색, 연대 정밀도·문헌 판본 구분, 기본 반응형.
- 깊이 블록 추가 시 같은 인물 ID·URL 유지.

**B4 Quality & Review**
- 실제 앱 빌드와 핵심 링크 회귀, 6개 탐색 경로, 접근성, 모바일 5폭.
- 비승인 AI 역사 인물화와 거짓 좌표 핀 0건.
- Cloud Run/공유/메인 병합은 사용자 별도 승인 없이 하지 않음.

## 작업별 완료 정의
### T-001 설계 5문서/디자인 토큰과 사용 승인 범위 대조
- **단계:** S0, P0; **상태:** NOT_STARTED
- **의존:** 없음
- **완료 기준:** 사용자 수정사항 및 구상 확정 기록
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-011, FR-015

### T-002 Google AI Studio Build Web 모드 및 프로젝트 생성 준비
- **단계:** S0, P0; **상태:** NOT_STARTED
- **의존:** T-001
- **완료 기준:** 계정/프로젝트/생성 모드 실제 확인, Publish 금지
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-015

### T-003 GitHub 기능 브랜치·동기화 방식 확인
- **단계:** S0, P0; **상태:** NOT_STARTED
- **의존:** T-002
- **완료 기준:** main 보호, 정본/생성 코드 충돌 계획과 diff 기록
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-014

### T-004 개요 데이터 127건·관계 32건/출처 23건 실제 읽기 진단
- **단계:** S0, P0; **상태:** NOT_STARTED
- **의존:** T-003
- **완료 기준:** 8/33/34/20/22/10/32/23 숫자 검증. 미조회 시 DEMO 명시
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-001, FR-010

### T-005 DRAFT/시연용 데이터 경계·접근제어 계획
- **단계:** S0, P0; **상태:** NOT_STARTED
- **의존:** T-001
- **완료 기준:** 허가 없는 외부 공유·배포·원전/AI 미디어 사용 금지
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-011

### T-006 첫 Build 프롬프트로 React TypeScript 앱 골격 생성
- **단계:** B1_UI, P0; **상태:** NOT_STARTED
- **의존:** T-001, T-002, T-005
- **완료 기준:** 실행 가능한 앱/코드 확인, 배포는 미실시
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-012, FR-015

### T-007 토큰/CSS/읽기 폭/헤더·모바일 메뉴
- **단계:** B1_UI, P0; **상태:** NOT_STARTED
- **의존:** T-006
- **완료 기준:** 배경/색/폰트/여백 일관, keyboard menu
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-012, FR-015

### T-008 홈 편집형 Hero/8권 카드·CTA
- **단계:** B1_UI, P0; **상태:** NOT_STARTED
- **의존:** T-007
- **완료 기준:** 8개 카드와 01~08 정확한 권명, 볼륨8 자료실 고지
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-001

### T-009 권 목록·권 상세 기본 템플릿
- **단계:** B1_UI, P0; **상태:** NOT_STARTED
- **의존:** T-008
- **완료 기준:** 8개 권 상세와 내부 경로 작동
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-002

### T-010 로컬 데모 상태/404/빈 상태
- **단계:** B1_UI, P0; **상태:** NOT_STARTED
- **의존:** T-006, T-009
- **완료 기준:** DEMO와 실제 연구 구분, 존재하지 않는 ID 안내
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-013, FR-015

### T-011 모바일 320/375/768/1440 디자인 1차 검수
- **단계:** B1_UI, P0; **상태:** NOT_STARTED
- **의존:** T-007, T-008, T-009
- **완료 기준:** 텍스트 오버플로 0, focus/hover/scroll 확인
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-012

### T-012 Git JSON/Markdown read-only 어댑터·타입 검사
- **단계:** B2_DATA, P0; **상태:** NOT_STARTED
- **의존:** T-004, T-006
- **완료 기준:** 정본 수정 없이 127객체+32관계 연결
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-001, FR-002, FR-014

### T-013 인물 3건 OV-P ↔ PER 글로벌 ID 대응
- **단계:** B2_DATA, P0; **상태:** NOT_STARTED
- **의존:** T-012
- **완료 기준:** 발도/위클리프/후스 동일 엔터티 매핑, 링크 안정
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-003, FR-014

### T-014 문헌·출처 계층/URL·라이선스 분리
- **단계:** B2_DATA, P0; **상태:** NOT_STARTED
- **의존:** T-012
- **완료 기준:** 번역/편집/서평 구분, 유료 원문 전문 미복제
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-005, FR-010

### T-015 34개 사건 정밀도·정렬·연대표 어댑터
- **단계:** B2_DATA, P0; **상태:** NOT_STARTED
- **의존:** T-012
- **완료 기준:** dateLabel 보존, approximate를 day로 바꾸지 않음
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-004

### T-016 출판 allowlist와 빌드 결과 누출 검사
- **단계:** B2_DATA, P0; **상태:** NOT_STARTED
- **의존:** T-005, T-012
- **완료 기준:** 미승인 원고/이미지/좌표 검색색인·HTML·JSON·dist 0
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-011

### T-017 인물 목록/상세/관련 항목 연결
- **단계:** B3_PAGES, P0; **상태:** NOT_STARTED
- **의존:** T-013, T-016, T-009
- **완료 기준:** 33명(내부 검토) 중 주요 인물 라우트
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-003, FR-009

### T-018 사건 상세·연대표 화면
- **단계:** B3_PAGES, P0; **상태:** NOT_STARTED
- **의존:** T-015, T-016, T-009
- **완료 기준:** 34사건 필터, 날짜 표시·관계 정확
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-004, FR-009

### T-019 문헌 목록/상세·판본 상태
- **단계:** B3_PAGES, P0; **상태:** NOT_STARTED
- **의존:** T-014, T-016, T-009
- **완료 기준:** 20문헌, 출처와 열람 한계
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-005, FR-010

### T-020 주제 10개·VOL-08 횡단 자료실
- **단계:** B3_PAGES, P0; **상태:** NOT_STARTED
- **의존:** T-016, T-009
- **완료 기준:** 아카이브의 시대 비종속성
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-006, FR-009

### T-021 현대 지명 22곳 텍스트 목록
- **단계:** B3_PAGES, P0; **상태:** NOT_STARTED
- **의존:** T-016, T-009
- **완료 기준:** 좌표 핀 0, 역사 현장 거짓 복원 0
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-007

### T-022 별칭 검색·유형 필터·빈 결과
- **단계:** B3_PAGES, P0; **상태:** NOT_STARTED
- **의존:** T-017, T-018, T-019, T-020
- **완료 기준:** 루터/Luther/후스/Hus/1517/성찬론 검색
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-008, FR-013

### T-023 관계 타입·사실/해석·출처 UI
- **단계:** B3_PAGES, P0; **상태:** NOT_STARTED
- **의존:** T-014, T-017, T-020
- **완료 기준:** 문헌 영향과 실제 직접 교류 분리
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-009, FR-010

### T-024 개요/심층 블록 확장과 수정 이력 모델
- **단계:** B3_PAGES, P0; **상태:** NOT_STARTED
- **의존:** T-013, T-017
- **완료 기준:** 같은 인물 URL 아래 새 연구 블록 삽입 가능
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-014, FR-017

### T-025 14개 라우트/6개 대표 사용자 경로 회귀 검증
- **단계:** B4_QA, P0; **상태:** NOT_STARTED
- **의존:** T-017, T-018, T-019, T-020, T-021, T-022
- **완료 기준:** 페이지 직접 접근, 뒤로가기, 404
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-015

### T-026 모바일·접근성·reduced-motion 전체 QA
- **단계:** B4_QA, P0; **상태:** NOT_STARTED
- **의존:** T-025, T-011
- **완료 기준:** 320/375/768/1024/1440 및 키보드·스크린리더
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-012

### T-027 공개 권리/출처·역사 왜곡·미승인 미디어 자동검사
- **단계:** B4_QA, P0; **상태:** NOT_STARTED
- **의존:** T-016, T-023, T-025
- **완료 기준:** 공개 가능 레코드 0이면 공개 데이터 0, 가짜 지도 0
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-010, FR-011

### T-028 프로젝트 빌드·성능·GitHub 기능 브랜치 동기화
- **단계:** B4_QA, P0; **상태:** NOT_STARTED
- **의존:** T-025, T-026, T-027
- **완료 기준:** 프로젝트 빌드 PASS, lockfile/커밋/재현 경로
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-014, FR-015

### T-029 내부 시각검토·사용자 최종 수정 판정
- **단계:** B4_QA, P0; **상태:** NOT_STARTED
- **의존:** T-028
- **완료 기준:** 승인/반려/추가 수정 결정, 외부 Deploy 없음
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-012, FR-015

### T-030 최초 공개 범위·접근 제어/배포별도 승인
- **단계:** B4_QA, P0; **상태:** NOT_STARTED
- **의존:** T-029
- **완료 기준:** 명시적 승인 없으면 Cloud Run Publish 금지
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-011

### T-031 심층 연구 블록 증분 추가(후스/위클리프/루터)
- **단계:** P1, P1; **상태:** NOT_STARTED
- **의존:** T-024, T-029
- **완료 기준:** ID/URL 유지, 사료/판본별 승인
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-017

### T-032 지리학 고증 완료 좌표만 지도화
- **단계:** P1, P1; **상태:** NOT_STARTED
- **의존:** T-021, T-030
- **완료 기준:** 근거 좌표 0이면 지도 핀 0
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-016

### T-033 관계도·학습 흐름/동선 강화
- **단계:** P1, P1; **상태:** NOT_STARTED
- **의존:** T-023, T-030
- **완료 기준:** 관계 의미/접근성 보존
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-018

### T-034 새 권/신학 주제·참고 문헌 증분 갱신 루틴
- **단계:** P1, P1; **상태:** NOT_STARTED
- **의존:** T-031, T-030
- **완료 기준:** 데이터만 바꾸고 기본 컴포넌트 재개발 불필요
- **검증:** AI Studio preview + repository diff + checklist evidence (stage-specific)
- **PRD:** FR-014, FR-017


## 추적성
- FR-001~FR-018 모두 최소 하나 이상의 Task에 연결.
- 관계는 명시적 선행 의존성으로 기록하고 순환 및 미존재 참조를 검사.
- P1 심층 연구/지도/관계도는 **초기 화면의 코드/도메인 ID를 변경하지 않고 추가**하도록 설계.
- Google AI Studio가 생성한 파일은 새 기능 브랜치에서 관리하고 원본 연구 자료를 자동 변경하지 않는다.

**상태:** TASKLIST_DRAFT / 작업 34개 모두 NOT_STARTED / 게시 승인 없음.
