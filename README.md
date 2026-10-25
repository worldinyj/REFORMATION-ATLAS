# REFORMATION ATLAS
**세계 교회사·종교개혁 디지털 역사 아카이브 | Foundation V0.1**

사도 시대부터 중세 교회 개혁, 16세기 유럽 종교개혁, 현대의 세계 기독교까지 인물·사상·사건·장소·문헌을 서로 연결하는 한국어 중심 역사 프로젝트입니다.

> **현재 상태: 자료 구조와 시범 원고 작성 단계(DRAFT).** 웹사이트 개발, 역사 콘텐츠 공개 승인, 인물화 제작 및 Word 8권 완성 상태가 아닙니다. 모든 파일은 작업 브랜치에서 검토 중이며 `main`은 안정된 기준선으로 유지합니다.

## 둘러보기
- [프로젝트 헌장](docs/00_GOVERNANCE/PROJECT_CHARTER.md)
- [로드맵과 게이트](docs/00_GOVERNANCE/ROADMAP_AND_GATES.md)
- [저작권·편집·AI 생성 매체 정책](docs/00_GOVERNANCE/EDITORIAL_RIGHTS_POLICY.md)
- [8권 편찬 계획](docs/01_CONTENT/CONTENT_VOLUMES.md)
- [첫 시범 원고: 위클리프·후스·루터](docs/01_CONTENT/PILOT_WYCLIFFE_HUS_LUTHER.md)
- [출처 대장](docs/01_CONTENT/RESEARCH_SOURCES.md)
- [시각 제작 지침](docs/02_MEDIA/ART_DIRECTION.md)
- [시범 데이터](data/README.md)
- [직접 제작 관계도 SVG](assets/diagrams/AST-0001_wycliffe-hus-luther-relations.svg)
- [기획서→PRD→TRD→UXUI→TASKLIST](docs/03_PRODUCT/PLANNING_PIPELINE.md)

## 초기 시범
- 인물 3명: `PER-0001` 위클리프, `PER-0002` 후스, `PER-0003` 루터
- 사건 4건 / 사상 관계 2건 / 지명 5건
- 자체 제작 관계도 SVG 1점, 출처 10건
- 모든 콘텐츠·매체는 `DRAFT`, 공개 승인을 의미하지 않음

## 개발 준비
Python 3 환경에서 `python3 scripts/validate_content.py`로 JSON 참조, 출처 ID와 SVG 구문을 점검합니다. 별도 외부 패키지나 GitHub Actions는 사용하지 않습니다.

## 역사와 권리의 기본 원칙
- 초대교회와 16세기의 프로테스탄트 종교개혁을 역사적으로 구별합니다.
- 위클리프에서 후스로의 문헌 영향, 후스에서 루터 시대로의 후대 수용을 구분합니다.
- AI 재현 인물화는 사료 사진이나 실존 인물의 확정적 생김새로 표시하지 않습니다.
- 유료 출판물 전문을 복제하지 않고, 공개적으로 확인 가능한 내용과 적법하게 확인한 연구를 독자적으로 요약·해설합니다.
- 교단별 관점과 역사적 논쟁은 출처 및 불확실성을 병기합니다.

## AI Studio GitHub 연결 준비 (2026-10-25)
Google AI Studio Build로 **웹사이트 뼈대를 먼저 만들고**, 이 저장소의 8권 역사 개요를 검증 후 연결합니다.

- [GitHub 연결/동기화 실행 안내](docs/03_PRODUCT/AI_STUDIO_BUILD_V02/09_GITHUB_CONNECTION_SETUP.md)
- [AI Studio용 설계 패키지](docs/03_PRODUCT/AI_STUDIO_BUILD_V02/README.md) 및 [첫 Build 프롬프트](docs/03_PRODUCT/AI_STUDIO_BUILD_V02/06_MASTER_BUILD_PROMPT.md)
- [저장소 사전 점검 스크립트](scripts/validate_ai_studio_repo_preflight.py): `python3 scripts/validate_ai_studio_repo_preflight.py`
- [웹 코드 동기화 전 변경 경로 검사](scripts/check_ai_studio_sync_paths.py): 앱 코드가 생긴 뒤 사용

**중요:** 이 GitHub 저장소는 역사 원본 중심의 **public 자료 저장소이며 아직 React 앱은 없습니다.** AI Studio에서는 새 앱을 생성하고 **별도 웹앱 저장소(예: REFORMATION-ATLAS-WEB)**에 연결하는 방식을 권장합니다. 기존 저장소를 바로 Import하면 앱 루트가 없고 역사 자료가 섞여 있어 충돌 위험이 있습니다.

`main`은 2026-10-25 점검 당시 GitHub API에서 **protected=false**로 확인됐습니다. 웹앱 양방향 Sync를 시작하기 전에 [GitHub Ruleset/브랜치 보호 설정](docs/03_PRODUCT/AI_STUDIO_BUILD_V02/09_GITHUB_CONNECTION_SETUP.md#3-깃허브에서-사람이-직접-해야-하는-보호-설정)을 직접 완료해야 합니다. 이 문서와 QA 준비만으로 브랜치 보호가 설정되지는 않습니다.
