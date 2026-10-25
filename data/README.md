# REFORMATION ATLAS — Foundation Data (DRAFT)
이 디렉터리는 웹사이트에 연결 가능한 초기 콘텐츠 시범 데이터입니다.

- `people.json` — 인물 PER
- `events.json` — 사건 EVT
- `relations.json` — 인물 관계 REL
- `locations.json` — 현재 지명 및 역사 지명 연결 LOC

ID는 영속적으로 유지하며 중복 사용하지 않습니다. 관계의 `from_id`/`to_id`는 인물 ID를 가리킵니다. 사건의 `person_ids`/`location_ids`도 동일하게 참조합니다. 이 시범 데이터는 법적 저작권과 역사 사료 검증을 위한 콘텐츠 **초안**으로, 배포 승인되지 않았습니다.

- `date_precision`은 사건 날짜의 정확도. 불확실한 연대에 가짜 정밀도를 부여하지 않습니다. 현재 EVT-0001의 ISO 날짜는 정렬 편의용 임시 값이며 실제 연·일을 확정한 것이 아닙니다. **UI에서는 임의의 월·일을 표시하지 말 것.**
- 시기별 국경 및 좌표는 검증 후 별도 데이터로 저장할 것. 현재 지도용 좌표 없음.
- `publication_status`는 사람의 공개 승인 상태, `certainty`는 주장 사실성 정도.
- JSON을 수정한 후 참조 무결성·출처 ID 검증을 실시할 것.
