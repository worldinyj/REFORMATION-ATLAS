# 종교개혁 ATLAS — V5.14 시대 정렬과 독자 서사 통합

> 2026-11-23 · 연구 브랜치: research/atlas-v514-chronological-case-rehoming-reader-architecture

## 완료한 편집 작업

- **역사 사례 2건 실제 이동:** 과만 포마(약 1615년) 제7권 → 제5권; 태평양 여성(1820년) 제5권 → 제6권. 기존 위치에는 교차 참조 유지.
- 8권의 도입부·맺음말 **총 16곳 집필 개정**. 기존 약 999자 → 4,242자.
- 8권 24장 독자용 연대기 지도 및 문서·현지 행위자별 2개 독서 경로 추가.
- 기존 21개 장 본문 정확히 유지, 이동에 관련된 3개 장만 수정.
- 본문 글자 수 52,812자 → 53,081자. 데이터↔Markdown 24장 전부 일치.
- 이전 URL 삭제 0, 기존 출처를 새로운 장에 5건 재연결. 새 문헌 원본 교감·역사학자 승인·앱 E2E 없음.

## 문서

- [전체 8권·24장 통합 연구 원고](../../docs/01_CONTENT/INTEGRATED/V514_EIGHT_VOLUME_CHRONOLOGICAL_READER_MASTER_KO.md)
- [독자용 8권 흐름·질문 지도](./READER_NAVIGATION_AND_CHRONOLOGY_KO.md)
- [시대권 재배열 편집 보고](./CASE_REHOMING_EDITORIAL_REPORT_KO.md)
- [사례 이동 레지스트리](./case_relocation_manifest.json)
- [24장·8권 편집 감사](./integrity_reader_flow_audit.json)
- [구조화 콘텐츠 JSON](../data/V514_EIGHT_VOLUME_CHRONOLOGICALLY_REHOMED_CANDIDATE.json)

## 다음 V5.15

8권·24장 역사서의 일반 독자용 **짧은 장 서두(150~250자)**와 연구자용 상세 사료층을 구분하는 독서 판본 설계. 본문 역사 사실은 추가 고증 없이 단정하지 않는다.

`can_ship=false` · `can_merge_main=false` · `can_import_ai_studio=false`. GitHub main·운영 AI Studio 앱 미변경.
