# V1.24 실제 GitHub 데이터 구조 QA 기록

2026-10-30, 연구 브랜치 저장 후 GitHub 연결로 4개 JSON 파일을 재열람하고 별도의 JavaScript 검사 8개를 실제 실행함.

| 구조검사 | 결과 |
|---|---|
| 모든 문헌·주장 자료의 공개 게이트 닫힘 | PASS |
| 출처 ID 8건의 유일성 | PASS |
| Egerton 617·618에 Genesis/Exodus 없음 | PASS |
| Manchester MS 89 혼합 판본 상태 | PASS |
| 세 비교 후보의 실물 판면 검증 미완료 표시 | PASS |
| 6월 심문과 7월 선고의 사건 장르 분리 | PASS |
| 8개 주장 중 2개 오류 주장 기각 표시 | PASS |
| 주요 source_ids의 출처 객체 참조 무결성 | PASS |

**8/8 PASS**. 이는 GitHub JSON 내용에 대한 실제 구조 검증 결과이며, 저장된 Python 단위 테스트의 실행 결과가 아님. 필사본/판본 직접 판독, 역사적 사실 전면 재검증, 외부 웹앱 배포 검증은 포함하지 않음.
