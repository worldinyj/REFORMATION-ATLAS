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
