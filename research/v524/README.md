# 종교개혁 ATLAS V5.24 — 3단계 읽기 준비도 평가 및 콘텐츠 계약

> 2026-11-24 · 기준 V5.23 · 연구 브랜치 `research/atlas-v524-three-level-24-chapter-readiness-contract`

## 무엇을 완료했는가

- 24장 L1 짧은 이야기, 9장 L2 중간 해설, 24장 L3 전문 연구 원고의 실제 존재 여부와 연결 위치를 전수 점검
- L2 미작성 15장과 역사·판본 검증 우선 5장의 편집·연구 우선순위를 명시
- 8권별 출처 URL 수·글자수·중간 해설 공백과 24장 개별 진단표 작성
- 앱이 결여된 중간 해설을 생성된 것으로 취급하지 않고, 원전 직접 확인과 현대 영인을 혼동하지 못하도록 연구용 JSON 계약과 JSON Schema 작성
- 자동 구조 검사 18/18 통과; V5.23 기준 원고, 52개 사례, 6개 증거 경로, 152개 URL 항목 유지

## 자료

- [24장 3단계 읽기 진단표](./THREE_LEVEL_READINESS_AND_GAPS_24_CHAPTERS_KO.md)
- [콘텐츠 계약 데이터](./three_level_display_contract.json)
- [콘텐츠 계약 JSON Schema](./three_level_display_contract.schema.json)
- [자동 검증](./v524_integrity_audit.json)

## 다음 V5.25 권장

제5권 05-03, 제4권 04-01, 제8권 08-01의 L2 중간 서사 3편을 먼저 보강해 9/24→12/24로 진전. 판본의 미확정 사항은 별도 경고로 유지. 먼저 연구 브랜치 원고로 작성하고, 전문가·독자·앱 검증은 이후 단계에서 별도 수행.

**승인·배포 보류:** `can_ship=false`, `can_merge_main=false`, `can_import_ai_studio=false`. 전문가 검토 0·사람 독자 시험 0·운영 앱 E2E 0.
