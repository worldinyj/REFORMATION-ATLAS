# V1.16 읽기 전용 변환기 및 대표 표본 회귀검증

**DRAFT_RESEARCH_NOT_PUBLIC** · 2026-10-30 · V1.15 후속

## 확인된 저장소 데이터
GitHub 연결을 통해 V1.15 규격 및 실제 세 JSON 파일을 읽어 구조를 점검했다. `data/overview/events_documents_v01.json`에는 사건 34개, `data/deep/vol04_luther_v01.json`에는 심화 문서 블록 1개, `data/deep/vol05_education_map_timeline_v114.json`에는 사건 4개가 있다. 이 39개에서 내부 ID 중복 0, 출처 배열 누락 0, 명시적 공개 승인 0을 확인하였다. 연결된 외부 문헌의 실재·주장 정확성을 이 검사만으로 검증할 수는 없다.

## 구현
- `scripts/atlas_readonly_adapter_v116.py`: V1.15 계약에 따른 JSON 표준화 결과를 **표준출력**으로만 표시하거나 `--check` 검사 수행. 파일 쓰기 없음.
- `tests/test_atlas_readonly_adapter_v116.py`: ID, 출처, 사적 상태, 날짜 구분을 점검하는 7개 단위 테스트.
- 기존 source JSON·main·Google AI Studio 미수정.
- 예외 발생 시 부분 결과를 공개하거나 출력하지 않음.

## 실행
```bash
python3 scripts/atlas_readonly_adapter_v116.py --check
python3 -m unittest discover -s tests -p 'test_atlas_readonly_adapter_v116.py' -v
python3 scripts/atlas_readonly_adapter_v116.py > /tmp/atlas_v116_private_preview.json
```

마지막 명령은 사용자가 직접 지정한 임시 경로에 저장하는 예시로 **프로그램 자체는 원본 파일을 수정하지 않는다.** 임시 결과물을 공개 서비스에 업로드하지 말 것.

## 한계
- 현재 읽기 전용 어댑터는 **대표 3종 데이터**로 범위를 제한했다. 1~5권 전체 파일을 모두 변환했다고 주장하지 않는다.
- V1.15 계약의 일부 `volume_ids`가 문자열이므로 출력에서는 배열로 래핑하지만 정본을 고치지 않는다.
- DATE의 `period`는 기존 개요 데이터에 등장하므로 호환 유지.
- 제5권 이벤트의 `type` 기술명은 임시 표시 제목이다. 사람에게 노출될 한국어 문장으로 승격하지 않는다.
- 해당 Python 테스트는 GitHub 브랜치에 저장하는 코드이며, **CI 실행 결과와 구분**한다.
- 후속 V1.17은 누락된 권별 인물·문헌·판본 계열을 추가 투영하고 각 출처 ID 유효성을 교차 검증하는 단계다.
