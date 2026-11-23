# 종교개혁 ATLAS V5.23 — 사건·저자·인쇄·영인의 시간 구분

> 2026-11-23 · 연구 브랜치 `research/atlas-v523-authorship-print-facsimile-evidence-pathways` · 운영 AI Studio 및 main 미변경

## 이번 단계에서 실제 완성한 것

- 제2·4·5·6·7권의 다섯 역사 장에 **6개 증거 경로, 20개 사건·문헌·인쇄·현대 전승 단계**를 추가
- 제5권 소르 후아나의 **1691년 집필 / 1700년 첫 인쇄 / 1701년 별도 재판 / 2026년 현대 영인**을 분리
- 몬테레이 공과대학교 2026년 4월 27일 공식 자료의 **1701년판 기반 현대 영인본 첫 면 사진**을 확인. 사진은 2026년 현대의 복제물에 관한 자료이지 1701년 원판 활자 지면 직접 교감이 아님을 명시
- 해당 제5권 역사 본문 477자 보강, 다른 23개 장의 역사 원문 완전 보존
- 24개 참고자료 목록 가운데 제5권에 공식 출처 1건 추가(총 152건, 고유 132개)
- 기존 52개 사례, 독자용 요약 24편, 중간 해설 9편, 제8권 6개 주제, 기존 판본 주의사항 모두 보존
- 독자판 및 심화 원고에 6개 증거 경로의 내부 연결 반영
- 45개 무결성 검사 전부 통과(출처 URL의 개별 사실 귀속·UI 클릭 시험·사람 독자 평가는 별도)

## 결과물

- [V5.23 8권·24장 통합 원고](../../docs/01_CONTENT/INTEGRATED/V523_EIGHT_VOLUME_SOURCE_LAYERS_MASTER_KO.md)
- [V5.23 독자용 역사 이야기](../../docs/01_CONTENT/READER/V523_24_CHAPTER_SOURCE_LAYERS_READER_KO.md)
- [6개 증거의 시간 경로 안내](./SIX_SOURCE_TIMEPATHS_READER_GUIDE_KO.md)
- [현대 영인본 사진 출처와 20개 단계 구조화 데이터](./evidence_timepaths_registry.json)
- [24장 사료 한계·현대 복제물 주의사항](./RESEARCH_BOUNDARIES_24_CHAPTERS_KO.md)
- [전체 8권 구조화 콘텐츠 JSON](../data/V523_EIGHT_VOLUME_SOURCE_LAYERS_CANDIDATE.json)
- [V5.23 최종 검증](./v523_integrity_and_source_provenance_audit.json)

## 다음 V5.24 권장

새 원전 확보를 계속 무리하게 반복하기보다 전체 8권을 대상으로 **독자에게 필요한 세 가지 읽기 모드(짧은 이야기·중간 깊이·출처 연구)**의 범위와 잔여 결함을 평가하고, 근거 등급과 논쟁 상태를 앱이 오해 없이 표시할 수 있는 공통 콘텐츠 계약(JSON 스키마)을 정리한다. 실제 Google AI Studio 앱 적용은 별도 단계로 구분한다.

**검증 보류:** 1700·1701년 같은 줄 원판 대조 0, 역사학자 서명 0, 독자 시험 0, 앱 E2E 0. `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`.
