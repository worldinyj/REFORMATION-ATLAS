# V1.44 실측 CI 장애 원인 분석 및 활동 오류 분리

2026-10-30 · RESEARCH_ONLY · main / AI Studio 미수정

## 1. 실제 CI 실행
GitHub Actions 실행 41027644559 (2026-10-30 UTC 08:37)에서 V1.43 검사기는 JSON 117개를 전부 파싱했다. 정본 엔터티 집계는 인물 33, 문서 20, 사건 34였으며 잘못된 위클리프–후스 『교회론』 연결 형태를 3건 검출하여 exit 1로 실패 처리했다.

## 2. 실제 문제 2건과 기존 감사 기록 1건 구분
- **실제 데이터 결함 A**: data/contracts/atlas_person_document_witness_crosswalk_v119.json 의 links[0]는 위클리프 OV-P-009를 OV-D-005와 관련시킨다. 정본 문서 OV-D-005는 후스의 1413년 De ecclesia.
- **실제 데이터 결함 B**: data/deep/vol03_wycliffe_hus_primary_witness_audit_v120.json 의 records[0]은 위클리프 Tractatus de ecclesia 1886년 로저스? 아니며 실제 편집자 Johann Loserth 판본을 설명하면서 문서 ID OV-D-005를 사용한다. 위클리프 저작의 별도 정본 ID가 필요하다. 기록의 1886년 판본과 14세기 저작도 서로 구분해야 한다.
- **오류의 재인용**: data/contracts/atlas_v141_identity_audit.json findings[0]은 예전 잘못된 관계를 **문제 기록**으로 기술하고 있으므로 또 다른 현재 연결 오류로 세면 안 된다.

따라서 '실제 데이터 내 위클리프/후스 ID 충돌 지점 2개 + 감사 문서의 재인용 1개'로 분리한다. 구조 검사를 통과한다 해도 문헌 동정과 원문 대조가 끝났음을 뜻하지 않는다.

## 3. 새로운 검사기
scripts/audit_atlas_identity_triage_v144.py 는 data 내 JSON 전체를 파싱하지만 충돌 규칙을 실제 관계 운영 파일에 한정한다. 과거 감사 보고서는 증거로 존치한다. 원본 데이터를 강제로 삭제·변경하지 않았다.

실행:
```bash
python3 scripts/audit_atlas_identity_triage_v144.py --root . --output atlas-v144-audit.json
```

검출된 실제 충돌이 해결되기 전에는 검사기가 비정상 종료하도록 의도했다. 기존 V1.43 검사 결과와 동일한 실행 계열의 구분 규칙을 반영한 것으로, **V1.44 CI의 전체 실행 결과는 별도 확인 전까지 미확정**이다.

## 4. 역사 콘텐츠 작업
원전 비교 콘텐츠에서 같은 라틴어 제목을 가진 후스(1413)와 위클리프(14세기)의 저작을 혼용하지 않는다. 위클리프판 1886년 Loserth 편집본과 후스 저작을 각기 독립 식별자로 다루어야 한다. 문헌의 개별 서지 및 사본 영인은 추가 대조가 필요하다.
