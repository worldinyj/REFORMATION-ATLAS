# V5.15 — 8권 24장 독자·연구자 2층 콘텐츠 연결 규격

> 이 파일은 **문서·데이터 설계**다. AI Studio 앱의 기능 구현이나 화면 E2E 완료 보고가 아니다.

## 기본 원칙

**독자층(Reader):** 장 제목 + 기간 + 150~250자 역사 이야기 + 한 가지 독자 질문을 보여 준다. 어려운 교감학 문제를 처음부터 전부 읽게 하지 않는다.

**연구층(Research):** 독자가 심화를 선택하면 기존 역사 본문 전체와 '자료와 해석을 구별하기', 장별 출처 URL, 완료되지 않은 원전 검증을 보여 준다.

**근거 보존:** Reader는 V5.14 내용의 편집 요약이므로 Research에 없는 사실을 추가하거나 원본 미열람을 숨기지 않는다.

## 데이터 연결

| 계층 | JSON 필드 | 포함 정보 |
|---|---|---|
| 공통 식별자 | `chapters[].id`, `title`, `period`, `volume_id` | 24장 연결의 기준 |
| 독자용 | `chapters[].readerLayerV515.reader_summary` | 150~250자 요약 |
| 독자용 | `chapters[].readerLayerV515.reader_question` | 장별 사고 질문 |
| 독자용 | `chapters[].readerLayerV515.summary_characters` | 분량 검증 지표 |
| 연구용 | `chapters[].bodyMarkdown` | V5.14 기존 심화 역사 본문 전체, 무변경 |
| 연구용 | `chapters[].researchLayerV515.evidence_boundary` | 사료·해석 구분 주의 문구 원문 |
| 연구용 | `chapters[].sourceLinks` | 기존 참고자료 URL 배열, 무변경 |
| 상태 | 최상위 `can_ship`, `can_import_ai_studio` | 인간 검증 전까지 false |

## UI에서 추후 적용할 수 있는 흐름

1. 먼저 권·장 카드에 요약과 질문을 표시한다.
2. 독자가 '자세히 읽기'를 선택하면 같은 `chapter.id`의 `bodyMarkdown`을 가져온다.
3. 전문가용 '사료 근거'에서 `sourceLinks`와 `evidence_boundary`를 추가로 보여준다.
4. 해당 자료가 초판 직접 교감인지, 소장서지·현대 번역·후대 교감판인지 설명하고 미확정 부분을 경고한다.
5. '다음 장'은 기존 장 순서를 그대로 이용한다. 비교 사례가 다른 권으로 이동했다면 V5.14의 `volume_navigation_v514.relocations`를 읽는다.

**구현 주의:** 위 내용은 향후 운영 AI Studio 앱에 반영할 때 사용할 설계이며, 실제 동작하는 버튼·접기 패널·네비게이션 링크를 앱에 추가하지 않았다.

## 참조 파일

- [독자용 24장](../../docs/01_CONTENT/READER/V515_24_CHAPTER_PLAIN_LANGUAGE_READER_KO.md)
- [2층 통합 원고](../../docs/01_CONTENT/INTEGRATED/V515_EIGHT_VOLUME_TWO_LAYER_MASTER_KO.md)
- [24장 원전 주의사항](./RESEARCH_BOUNDARIES_24_CHAPTERS_KO.md)
- [V5.15 데이터셋](../data/V515_EIGHT_VOLUME_TWO_LAYER_READER_CANDIDATE.json)
- [원문·출처 불변성 검사](./two_layer_integrity_audit.json)
