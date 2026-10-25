# G4-A · 제3권의 8권 공통 읽기 전용 데이터 프로젝션
> 2026-10-25 · V0.2 실험 / 비공개 / 원본 JSON 변경 금지

## 목적
제3권의 통합 색인 **182개 항목·365개 관계**를 원본 스키마의 손상 없이 G4 8권 공통 읽기 모델로 변환하는 최소 실행 구현이다.

`python3 scripts/build_vol03_g4_projection.py`는 실제 원본 데이터와 공통 계약을 읽고 **검증만 실행**, 파일은 생성하지 않는다.

`python3 scripts/build_vol03_g4_projection.py --output /tmp/vol03_g4_review.json` 는 **승인받지 않은 로컬 검토용 파생본**을 저장하며 원래 원전·도상 자료를 수정하거나 GitHub에 자동 커밋하지 않는다.

## 주요 계약
- 182개 노드의 원본 `id`, `type`, `title`, `source_ids` 보존. 표준화된 `title_ko`, `volume_ids=[VOL-03]`, `review_status`, `public_visible=false`만 읽기 모델에 제공.
- 365개 에지는 **기존 `type`과 방향**을 변경 없이 유지. `textual_influence`를 사람 여행 또는 직계 제자관계로 재해석하지 않는다.
- 역사 사건은 원래 `data/events.json` 또는 `vol03_extension.json`의 `date_display/date_label/date_start/date_precision`을 복사한다. **날짜가 모호할 때 정확 월일을 새로 만들지 않는다**.
- 주장은 `claim_ko` 정본으로 연결하고 evidence tier와 certainty를 다른 축으로 보존한다. 배포 승인 여부와 역사적 확실성은 별개다.
- 이미지/지도 노드는 `REVIEW_PENDING` 권리 상태와 `requires_human_approval=true`, `public_visible=false`로 유지한다. WebP가 로컬에 존재해도 공개 승격하지 않는다.

## 범위 제한
- 실제 데이터베이스 이관, 검색 API, 지도 타일, 상용 서비스 화면 구현 없음.
- 제3권 이외 7권은 공통 키 규약만 존재하며 전체 콘텐츠나 연대표가 자동 생성되는 것은 아니다.
- 원전 필사본·역사 복식·문장 전문 심사 또는 사람 최종 승인 대체하지 않음.

## 검증
CI에서 `python3 scripts/build_vol03_g4_projection.py` 호출. 노드/관계 수, 모든 에지 종단점, 날짜 정밀도, 주장 14건 커버리지, 검토/미공개 플래그를 확인한다. **CI 성공 여부는 실제 실행 후에만 기록한다.**

## CI 수정 메모
기존 확장 사건 데이터의 EVT-0008/0013/0017은 `date_precision=approximate_year`이다. 최초 G4 V0.1의 허용값 목록에 해당 항목이 누락되어 CI 실패가 발생했으므로 **원본 데이터를 변경하지 않고 계약 enum만 확장**했다. 검증기의 엄격한 타입 검사와 사건의 고유 날짜 레이블은 유지한다.
