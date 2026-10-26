# 제4권 문헌·판본 출처 그래프 / 웹앱 인수 V0.3

> 연구 브랜치 전용 (2026-10-26) · **본문 미대조 / 학술·법적 검수 미승인 / 공개 금지**

## 이번에 실제 구현된 것

- 제4권 기존 V0.2 어댑터를 재사용해 세 가지 문헌 판본 비교를 읽는다.
- V0.1 비교 사례에서 URL로만 존재하던 **7개 출처를 임시 `CMP-SRC-PROP-*` 키에 1:1 연결**한다. 기존 네 개 개혁자 데이터셋에 등록된 61개 출처 키와 충돌하거나 동일 출처라고 자동 판단하지 않는다.
- 출처의 분류(학술 초록, 기관 전시, 교파적 해설, 웹 비교 등)와 미대조/미승인 상태를 추적한다.
- 기존 `OV-P-013` 루터 / `OV-P-014` 멜란히톤 / `OV-P-016` 칼뱅과 관련 사건 `OV-E-019`·`OV-E-020`에 연구 관계를 연결하되 **직접 참석·모든 판본과 사건 동일성은 추론하지 않는다**.
- 새로운 정식 `DOC/EDN/TRN/WIT/SRC` 식별자, 퍼블릭 API, 퍼블릭 JSON, 이미지 파일은 생성하지 않는다.

## 연구용 비교 사례 연결

| 비교 키 | 저작 참조 | 근거 링크 수 | 인물 연결 | 사건 연결 / 범위 |
|---|---|---:|---|---|
| VOL04-CMP-001 | OV-D-012 기독교강요 | 3 | OV-P-016 칼뱅 | OV-E-020은 **1536 초판 한정** |
| VOL04-CMP-002 | WORK-PROP-V04-LUTHER-NT | 2 | OV-P-013 루터 | 해당 개요 사건 아직 확정하지 않음 |
| VOL04-CMP-003 | OV-D-011 아우크스부르크 | 2 | OV-P-014 멜란히톤 (기초 작성 맥락) | OV-E-019는 **1530 제출 한정** |

`OV-D`는 저작 레퍼런스일 뿐 해당 연구 내용의 웹 게시 권한이 아니다. `WORK-PROP`, `CMP-SRC-PROP`, `VOL04-CMP`는 정식 라우트/정식 문헌 ID가 아니다.

## 실행 및 검사

```sh
python3 scripts/build_vol04_edition_ui_review_v02.py
python3 scripts/build_vol04_provenance_graph_v03.py
python3 scripts/validate_vol04_provenance_graph_v03.py
```

기본 실행은 파일을 쓰지 않는다. 연구자 개인 검토용 결과만 저장소 **외부**에 작성할 수 있다.

```sh
python3 scripts/build_vol04_provenance_graph_v03.py --review-output /tmp/vol04_provenance_review_v03.json
```

이 파일을 실제 웹앱의 `public/`, `src/`, `dist/`, CDN, GitHub Pages, AI Studio Build 첨부 파일에 올려서는 안 된다.

## Google AI Studio Build 인수 계약

실제 웹앱 개발 브랜치와 본 연구 브랜치를 별도로 유지한다. 현재 웹앱 원본 프런트엔드 소스가 연구 저장소에 포함되지 않아 컴포넌트 통합·런타임 검증은 **아직 수행하지 않았다**.

1. 문헌 라우트 `/documents/:documentId`는 기존 안정 ID만 허용한다. 연구 키는 라우트로 사용하지 않는다.
2. 웹앱은 미래의 **사람 승인·출처·권리·판본별 승인 근거와 릴리스 매니페스트가 있는 별도 PUBLIC_PROJECTION**만 읽는다.
3. 승인본이 없을 때는 `승인된 판본 비교 자료가 없습니다.`라는 빈 상태를 표시한다. 연구 데이터 자동 fallback 및 브라우저 내부 필터링 금지.
4. 향후 컴포넌트 영역: 저작 머리말 → 판본 타임라인 → 구성/본문/삽화 탭 → 출처 유형 및 소장 정보 → 고증 한계·연결 인물과 사건. 탭 키보드 조작, 스크린리더용 타임라인 텍스트, 비색상적 상태 표시를 필수로 한다.
5. 승인된 이미지 없이 박물관 이미지·도상을 직접 불러오지 않는다. 링크 확인만으로 이미지 재사용권을 추론하지 않는다.
6. 프런트엔드 번들에 `data/deep/vol04_*`, `CMP-SRC-PROP`, `VOL04-CMP` 또는 연구용 그래프 JSON이 들어가면 빌드를 중단한다.

## QA와 남은 과제

- `validate_vol04_provenance_graph_v03.py`: URL 이탈·출처 누락·가짜 검증/승인·정식 ID 임의 발급·고아 관계 등 16개 변형 시험.
- 향후: 각 서지 링크 재접속·학술적 권위 검토, 1539년 칼뱅 판본의 실물 증인 후보 기록, 루터 9월판 소장번호, 아우크스부르크 Variata 제10조 원어 비교, 사람 승인용 별도 매니페스트.
- 현재는 **RESEARCH ONLY / PUBLIC 0건**. 공개 결과가 없다는 것은 빈 서비스 데이터가 정상이란 의미이며 누락 오류가 아니다.

관련 파일: `data/deep/vol04_comparison_provenance_crosswalk_v01.json`, `scripts/build_vol04_provenance_graph_v03.py`, `scripts/validate_vol04_provenance_graph_v03.py`.
