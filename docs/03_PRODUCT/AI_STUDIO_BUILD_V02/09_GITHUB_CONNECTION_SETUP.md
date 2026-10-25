# 09 · AI Studio Build × GitHub 연결 준비와 안전 동기화
> 2026-10-25 · GITHUB_READINESS DRAFT · 기존 역사 연구 저장소는 그대로 보존
> 대상: `worldinyj/REFORMATION-ATLAS` / 현재 기준 `main`은 public, 보호되지 않음. 사용자 계정의 AI Studio 연결 상태는 이 문서만으로 확인할 수 없음.

## 1. 현 상태와 위험 판정
| 항목 | 실제 확인 상태 | 조치 |
|---|---|---|
| 원본 GitHub | `worldinyj/REFORMATION-ATLAS` · public | 개요·심층 연구의 정본으로 사용 |
| 기본 브랜치 | `main` · **protected=false** (2026-10-25 GitHub API 확인) | 사람 손으로 Rulesets 설정 필수 |
| 8권 콘텐츠 | 127개 객체/32개 관계, 원전 자료 DRAFT | 공개 승격 금지; 검토용 입력에만 사용 |
| 설계 패키지 | `docs/03_PRODUCT/AI_STUDIO_BUILD_V02/` | V0.2 PLAN/PRD/TRD/UXUI/TASKLIST |
| 실행 앱 코드 | `package.json`, React 앱 루트 없음 | **기존 웹앱으로 직접 Import할 준비는 아직 안 됨** |
| GitHub↔AI Studio 인증 | 확인할 수 없음 | 사용자가 AI Studio Settings에서 OAuth 연결 |
| AI Studio Build 앱 | 생성 여부 미확인 | 첫 마스터 프롬프트로 생성 후 내부 Preview |
| 실제 공개 승인 | false | Share/Publish/Cloud Run 금지 |

### 중요한 구별
이 저장소의 `data/`·`docs/`는 공개 GitHub 자체에서 접근할 수 있을 수 있다. '웹페이지에 보이지 않는다'가 '비밀 자료'라는 뜻은 아니다. **미공개 원고나 키가 비밀이라면 public GitHub에 올리지 않는다.**

## 2. 권장하는 GitHub 구조 — 웹앱과 연구 정본 분리
**가장 안전한 방식은 두 저장소다.**

```text
worldinyj/REFORMATION-ATLAS          [현재 저장소 · 연구/자료 정본]
  data/overview/                     8권 개요와 근거
  docs/01_CONTENT/                   문헌·역사 원고
  docs/03_PRODUCT/AI_STUDIO_BUILD_V02/  설계 문서와 실행 프롬프트
  assets/                             심사 대기 이미지
  scripts/                            데이터 품질 검사

worldinyj/REFORMATION-ATLAS-WEB      [권장 새 저장소 · 생성/연결은 사용자가 직접]
  package.json                        Google AI Studio Build가 실제 생성
  src/                                React/TypeScript
  public/                             승인된 미디어만
  tests/                              앱/출판 게이트 테스트
```

이렇게 하면 AI Studio가 웹앱 루트에 파일을 생성/푸시하더라도 연구 정본의 경로를 덮어쓸 위험이 작다. **새 웹앱 저장소를 생성했다고 기록하지 않음**. 생성 뒤에도 앱 저장소에 DRAFT 연구 본문/이미지를 무차별 복사하지 않고, 승인된 내용만 import 가능한 데이터 스냅샷으로 제공한다.

### 첫 연결 순서
1. [Google AI Studio](https://aistudio.google.com/)에 로그인 → **Build → Web app**.
2. 연결된 연구 브랜치가 실제로 보이는 경우 [00_GITHUB_DESIGN_PREFLIGHT.md](00_GITHUB_DESIGN_PREFLIGHT.md)의 **설계 사전 감사**를 먼저 수행. GitHub 접근이 안 된다면 이 단계가 통과했다고 가정하지 않는다. 이후 [06_MASTER_BUILD_PROMPT.md](06_MASTER_BUILD_PROMPT.md)의 최초 생성 지시문 입력. **홈·8권·공통 라우트 뼈대**만 생성.
3. Code/Preview에서 **실제로 생성된 `package.json`/코드/디자인 토큰**과 모바일 메뉴 동작 점검.
4. AI Studio **Settings → GitHub**에서 GitHub 계정 연결(최소 권한 검토) 후 **새 저장소 만들기** 또는 기존 앱용 별도 저장소 연결. 이름 후보 `REFORMATION-ATLAS-WEB`; 가능하면 Private로 시작. 저장소 소유자가 로그인한 `worldinyj` 계정인지 확인.
5. AI Studio가 처음 Push하려는 변경 파일·대상 저장소·브랜치를 검토한다. **연구 저장소 `main`이면 Push 중단**.
6. GitHub에서 첫 커밋을 확인하고, 앱 저장소의 README/패키지/잠금 파일/비밀키 누락 여부를 점검한다.
7. 역사 개요 JSON은 실제 검토 후 필요한 원본만 안전한 **로컬 내부 Preview**에 제공한다. 외부 Share/Publish는 별도 승인.
8. [07_ITERATION_PROMPTS.md](07_ITERATION_PROMPTS.md)의 단계별 지시문으로 인물·연표·문헌/검색을 구현.

### 대안 — 기존 저장소 하나만 사용할 때
현재 연구 저장소에는 앱 진입점이 없어 직접 Import로 시작하면 안 된다. 먼저 Google AI Studio에서 **새 앱을 생성**해 다운로드/내보내기를 확보한다. 그 다음 기능 브랜치 `feat/atlas-web-ai-studio-v01`에 `apps/web/` 코드를 수동 통합한다. AI Studio가 monorepo `apps/web/` 같은 하위 경로와 브랜치 push를 공식적으로 처리한다는 보장은 없으므로, **실제 Sync 실험 성공 전 자동 양방향 동기화를 사용하지 않는다**.

## 3. 깃허브에서 사람이 직접 해야 하는 보호 설정
이 단계는 현재 연결된 GitHub 도구가 직접 수정할 수 없으므로 **설정 완료를 주장하지 않는다**.

1. <https://github.com/worldinyj/REFORMATION-ATLAS/settings/rules> 열기 (GitHub 로그인).
2. **New ruleset → New branch ruleset** 선택. 이름 예: `Protect main - Reformation Atlas`.
3. 대상 브랜치 `main`을 지정하고 ruleset을 **Active**로 설정.
4. 기본적으로 **Require a pull request before merging**, **Block force pushes**, **Restrict deletions**을 적용. 필요 시 최소 승인 인원 1명 및 미해결 리뷰 대화 처리 조건을 설정.
5. CI가 성공적으로 작동하는 것을 확인한 뒤 필요한 검사(개요/AI Studio 설계/저장소 사전점검)를 Required status checks로 선택. 없는 체크를 미리 필수로 지정하지 않는다.
6. 규칙 적용 대상이 관리자에게도 해당할지, 본인 계정 예외(bypass)가 있는지 확인. **Ruleset이 실제로 Active인지 화면에서 확인**.
7. 새 `REFORMATION-ATLAS-WEB`를 만든 경우 그 저장소의 `main`에도 비슷한 보호 규칙 적용.

> GitHub 계정/플랜·규칙 지원 범위는 사용자 저장소 Settings에서 실제 확인해야 한다. `.github/CODEOWNERS`는 검토 담당자 안내이며 **Ruleset 없이 Push를 기술적으로 차단하지 않는다**.

## 4. GitHub 워크플로 검증
이 브랜치에는:
- `.github/CODEOWNERS` 및 `.github/pull_request_template.md`: 소스 변경 검토 책임과 PR 체크리스트
- `AGENTS.md`: AI Studio 생성 에이전트가 따라야 할 보존/편집/배포 지침
- `scripts/validate_ai_studio_repo_preflight.py`: 표준 라이브러리 기반 준비 상태 검사
- `scripts/check_ai_studio_sync_paths.py`: 앱 도입 후 diff를 검사해 연구 원본 변경에 STOP
- `.github/workflows/ai-studio-repo-preflight.yml`: 브랜치별 준비 검사 자동화
- `.gitignore`: React/Node 비밀키·빌드 산출물 기본 무시 규칙

**로컬 재현:**
```bash
git fetch origin
git switch chore/ai-studio-github-readiness-v01
python3 scripts/validate_ai_studio_repo_preflight.py
python3 scripts/validate_ai_studio_design_v02.py
python3 scripts/validate_atlas_overview_v01.py
```

## 5. Push/Pull 전 체크리스트
- [ ] AI Studio 앱이 실제로 생성되었고 내부 미리보기가 동작한다.
- [ ] 연결한 저장소가 **앱 전용 저장소**인지, 연구 저장소의 기능 브랜치인지 정확히 확인한다.
- [ ] `main` 보호 Ruleset을 실제로 활성화했다.
- [ ] 변경된 파일이 연구 원본을 수정하지 않았는지 diff와 [경로 검사](../../../scripts/check_ai_studio_sync_paths.py) 확인.
- [ ] GitHub에 `.env`, API 키, 비밀 토큰, 미승인 역사 원전/이미지가 추가되지 않았다.
- [ ] Cloud Run/Publish/Share 등 **외부 공개 실행 없음**.
- [ ] React UI 디자인이 Quiet Editorial Atlas와 일치하고 모바일 320~430px에서도 정상.
- [ ] 공개용 빌드에는 승인된 콘텐츠만 포함됨을 별도 검사한다.

## 6. 다음 단계 준비 판정
- **GITHUB_RESEARCH_REPO_PREFLIGHT_READY**: 연구 저장소 내 문서/검증/가이드 준비.
- **NOT_YET**: `main` Ruleset 활성화, AI Studio OAuth 연결, 앱 전용 저장소 생성·동기화, 실제 앱 CI/런타임 테스트.
- **대상:** AI Studio 첫 Build → 앱 코드/연구 데이터 격리 → 사람이 GitHub 링크/브랜치 확인 → 내부 Preview 검증 → 향후 공개 승인.
