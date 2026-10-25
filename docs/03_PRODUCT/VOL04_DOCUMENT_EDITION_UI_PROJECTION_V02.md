# 제4권 문헌·판본 상세 UI — 읽기 전용 프로젝션 V0.2

> **개발 상태: 실행 가능한 연구용 어댑터 + 설계 계약. 정식 웹앱 미연동, 출판 차단.**

## V0.1에서 발전시킨 사항

기존의 [문헌 화면 설계 V0.1](VOL04_DOCUMENT_EDITION_UI_CONTRACT_V01.md)은 UI 구성과 일곱 개 게시 게이트를 정의한다. V0.2는 실제 연구 파일 3종을 읽고 **문헌 비교 3개를 연구자 검토 구조로 매핑**한다. 아직 웹앱에서 불러오거나 화면을 렌더링한 것은 아니다.

| 사례 | 저작 참조 | 화면 탭 | 연도·언어 구분 | 확인된 한계 |
|---|---|---|---|---|
| 칼뱅 1536/1539/1559 | `OV-D-012` | 구성 변화 | 라틴어 1536, 1539, 1559 | 1539년 별도 정식 판본 후보가 아직 없음 |
| 루터 1522 9월/12월 | `WORK-PROP-V04-LUTHER-NT` | 삽화 차이 | 독일어 1522-09, 1522-12 | 실물 이미지 사용권 미승인 |
| 아우크스부르크 1530/1540 | `OV-D-011` | 본문 차이 | 라틴어 제출 전승·Variata | 제출 원본 현존 여부와 교리적 해석 논쟁을 구별 |

## 날짜·식별자·출처 보존
- 연도만 확인한 판본의 날짜는 `1536`처럼 유지한다. 월이 있는 경우만 `1522-09`와 같이 기록한다.
- `WORK-PROP`, `EDN-PROP`, `*-S01`은 **연구용 키**이며 독자에게 제공할 URL의 ID가 아니다. 정식 ID를 생성하지 않는다.
- `OV-D-011/012`는 **기존 저작 참조**일 뿐, 연결된 하위 연구 비교까지 게시 승인되었다는 의미가 아니다.
- 구조 관찰과 교리적 해석, 삽화 수정과 본문 이문을 분리한다.
- 기관 전시의 링크 및 소장 정보는 직접 원문 대조 또는 이미지 재사용 허가로 승격하지 않는다.

## 실행 사용법
기본 모드는 실제 저장소 데이터를 검증하고 **파일을 생성하지 않는다**.

```bash
python3 scripts/build_vol04_edition_ui_review_v02.py
python3 scripts/validate_vol04_edition_ui_projection_v02.py
```

연구자 개인이 명시적으로 검토용 JSON을 만들 경우 저장소 **밖으로만** 저장한다.

```bash
python3 scripts/build_vol04_edition_ui_review_v02.py --review-output /tmp/vol04_edition_review_v02.json
```

생성된 JSON에는 `kind=RESEARCH_REVIEW_ONLY`, `web_import_allowed=false`, `public_visible=false`가 강제된다. 외부 저장 경로라도 웹앱 퍼블릭/정적 자산 폴더로 복사하면 안 된다.

## 공개 경로: 현재 구현하지 않음
`make_public_projection()`은 현재 0건만 반환하며, 이 스크립트는 공개 파일을 출력하는 옵션이 없다.

향후 사람 승인된 **별도 릴리스 매니페스트, 원문·판본별 검수, 출처 링크와 저작권 검토, 안전한 정식 ID 발급, 콘텐츠 해시 고정 및 재현 가능한 승인 로그**가 갖춰진 경우에만 새로운 공개 생성기/별도 PR이 필요하다. 현재 연구 데이터에서 `approved=true`로 바꾸는 것만으로는 게시가 허용되지 않는다.

## 재현 검증
`validate_vol04_edition_ui_projection_v02.py`는 17개 상위 후보, 분리 부모 5개, 임시 하위 10개, 비교 3개의 연결 관계를 검사한다. 테스트는 ID 무단 발급, 승인 플래그 조작, 판본 연도·언어·저작 연결 훼손, 저장소 내부로 연구 JSON 출력을 시도하는 경우 등을 차단해야 통과한다.

파일:
- `data/contracts/vol04_document_edition_ui_v02.json`
- `scripts/build_vol04_edition_ui_review_v02.py`
- `scripts/validate_vol04_edition_ui_projection_v02.py`

**의사결정:** Google AI Studio의 웹앱 구현 브랜치와 병합하지 않는다. 백엔드 API, 검색, 지도, 이미지 및 원문 전문은 여기서 제공하지 않는다.
