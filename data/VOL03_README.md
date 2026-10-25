# VOL-03 구조화 데이터 초안 V0.1
- `vol03_extension.json`: 6명 추가 인물 + 4개 운동, 새 위치 7개, 사건 14건, 관계 7개.
- 이미 존재하는 `PER-0001` 위클리프, `PER-0002` 후스, `PER-0003` 루터 및 `LOC-0001~0005`는 부모 브랜치의 기존 데이터에 있다.
- **주의**: 이 파일은 별도 심화 연구 초안이며 아직 `data/people.json` 등 배포 스키마로 통합되지 않았다. `APPROVED` 상태로 취급하지 않는다.
- 날짜 `year_start`는 역사 연표 정렬을 위한 값이다. `date_precision=approximate_period`가 붙은 항목의 연도는 대표 연도이지 확정된 발생연도가 아니다. 사용자에게는 `date_label`을 표시한다.
- 소스 `V03-S01~S18`은 `docs/01_CONTENT/VOL03/05_SOURCE_REGISTER.md`에 연결된다.
- 링크가 표현하는 의미를 표시하지 않은 채 한 줄 계보도로 내보내지 않는다.
