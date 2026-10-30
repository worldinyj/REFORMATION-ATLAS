# V1.45 — 동명 저작 ID 분리 및 CI 회귀 수정

2026-10-30 · 연구 브랜치 · 공개 불허

## 실제 수정
- `data/contracts/atlas_person_document_witness_crosswalk_v119.json`: 위클리프 `OV-P-009`의 `document_id`를 임시 `WRK-V03-WYCLIFFE-DE-ECCLESIA`로 분리.
- `data/deep/vol03_wycliffe_hus_primary_witness_audit_v120.json`: 1886년 Loserth 편집본의 저작 식별자를 동일 임시 ID로 교체.
- 기존 `OV-D-005`는 후스의 1413년 『교회론』 정본 ID로 유지.
- `scripts/audit_atlas_all_json_v143.py`: 감사 기록의 과거 오류 인용은 현재 운영 중인 오류로 집계하지 않도록 위클리프·후스 충돌 검사 범위를 실제 두 파일로 제한.

임시 ID는 정본 발행이 아니며 원문/사본 교감과 역사 편집자의 최종 확인이 남아 있다.

## 자동검사 관찰
V1.44 검증 GitHub Actions는 실제 두 데이터 수정 후 **성공**(run 41035878766)했다. 이보다 오래된 V1.43 검사기의 실패는 V1.41 감사문서 속 인용을 여전히 오류로 센 데 따른 것이다. V1.43 검사기 수정 커밋 f5d54b24에 대한 신규 실행은 별도 확인해야 한다. **이 문서는 실행 완료 전 성공을 예단하지 않는다.**

## 이후 연구
동명의 저작에 독립 증인·판본 ID를 설계하고, 후스의 1413년 『교회론』과 위클리프의 14세기 저작을 각각 독립 원문과 문헌 계보로 대조할 것.
