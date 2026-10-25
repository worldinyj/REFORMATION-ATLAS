# VOL-04 심층 연구 트랙 — 웹앱과 독립적인 콘텐츠 확장
> 2026-10-25 · **DRAFT / 웹앱 자동 게시 없음**

## 현재 산출물
- **기존 권 개요:** [VOL-04 개요](../OVERVIEW/VOL-04_OVERVIEW_V01.md). 8권 앱의 개요 데이터는 절대 수정하지 않음.
- **루터 심화 V0.1:** [LUTHER_DEEP_RESEARCH_V01.md](LUTHER_DEEP_RESEARCH_V01.md).
- **구조화된 출처·주장·연대표:** [vol04_luther_v01.json](../../../data/deep/vol04_luther_v01.json) · 17 출처 / 16 주장 / 11 시간 앵커.
- **검증·게이트:** [LUTHER_V01_RESEARCH_QA.md](LUTHER_V01_RESEARCH_QA.md).
- **Python validator:** [validate_vol04_luther_deep_v01.py](../../../scripts/validate_vol04_luther_deep_v01.py).

## 웹앱팀을 위한 인수 계약
| 항목 | 고정 값 |
|---|---|
| canonical person | \`OV-P-013\` Martin Luther |
| volume | \`VOL-04\` |
| depth block | \`DEPTH-V04-P013-001\` |
| depth kind | \`DEEP_RESEARCH\` |
| current review status | \`DRAFT_RESEARCH_NOT_PUBLIC\` |
| release approval | \`approved=false\`, \`can_ship=false\` |
| web/app code changes | **없음** |
| original overview JSON changes | **없음** |

- Google AI Studio에서 생성 중인 웹앱의 인물 상세 구조는 **OVERVIEW 위에 승인된 DEEP_RESEARCH 블록을 추가할 수 있도록** 설계되어 있다.
- 여기서 만든 새로운 사건 앵커 \`DEEP-V04-E-*\`는 이미 있는 \`OV-E-*\` 정본과 통합된 사건이 아니다. 이벤트 중복 검토 전에는 공개 타임라인에 넣지 말 것.
- 이번 루터 연구 JSON은 **Draft PR의 연구용 추가 데이터**이지, 공개 React 앱에서 직접 import할 파일이 아니다.
- 역사적 고증·원전 판본·저작권 검토 → 문장별 상태 갱신 → 별도의 public snapshot 승인 → 웹 앱 타입/라우트/검색 QA → 배포 승인이 필요하다.

## 다음 심층 연구의 순서
1. **루터 V0.2** — 1518 하이델베르크 논제, 1521 보름스 발언의 사료 계열, 1525 농민전쟁 당대 사료 대조.
2. **츠빙글리 V0.1** — 취리히 예배 개혁과 성찬론, 1529 마르부르크를 루터·츠빙글리 양측 증언으로 교차 연결.
3. **멜란히톤 V0.1** — 1530 아우크스부르크 신앙고백 작성·교육개혁, 루터와의 협력/차이.
4. **칼뱅 V0.1** — 1536/1559 『기독교강요』의 판본 차이, 제네바 정치·교회 구조·성찬론.
5. **VOL-03 ↔ VOL-04 교차 비교** — 위클리프·후스·루터 사이의 실제 문헌·수용 관계를 검증.

순서대로 원고/출처·주장 JSON/검증 자료를 추가하며 **웹 디자인/React 코드 변경 없이 콘텐츠 연구를 계속한다**.

## 제4권 네 인물 심층 연구 및 문헌·판본 단계 업데이트 (2026-10-25)
- [루터](LUTHER_DEEP_RESEARCH_V01.md), [츠빙글리](ZWINGLI_DEEP_RESEARCH_V01.md), [멜란히톤](MELANCHTHON_DEEP_RESEARCH_V01.md), [칼뱅](CALVIN_DEEP_RESEARCH_V01.md) 심층 초안이 모두 DRAFT로 준비됨.
- [4인 비교 검토](REFORMERS_CROSS_REVIEW_V01.md) → [61 주장/43 사건 대응표](FOUR_REFORMERS_EVIDENCE_CROSSWALK_V01.md) → [17개 판본·원전 서지 V0.2](WITNESS_EDITION_BIBLIOGRAPHY_V02.md) → [정본 ID 이관 계약](EDITION_ID_MIGRATION_CONTRACT_V02.md).
- [기계판독 서지](../../../data/deep/vol04_witness_bibliography_v02.json), [자동검증](../../../scripts/validate_vol04_witness_bibliography_v02.py).
- 17개 후보 중 **5개가 복합 문헌이므로 분리 필요**, 정식 ID 발급·원전 전문 대조·이미지 권리 승인 **미완료**.
- 이전 '다음 연구' 목록은 당시 계획으로 남겨 두었으며, 이번 이력에 따라 루터/츠빙글리/멜란히톤/칼뱅 V0.1을 추가 작업 완료로 기록함.

## 판본 상세 화면 데이터 연결 V0.2 (2026-10-25)
- [설계 및 검증 가이드](../../03_PRODUCT/VOL04_DOCUMENT_EDITION_UI_PROJECTION_V02.md) · [기계판독 계약](../../../data/contracts/vol04_document_edition_ui_v02.json).
- [읽기 전용 변환 스크립트](../../../scripts/build_vol04_edition_ui_review_v02.py): 기존 서지 17개·임시 하위 구분 10개·비교 사례 3개를 검토. 기본 실행은 파일 생성하지 않음.
- [부정 경로 검증](../../../scripts/validate_vol04_edition_ui_projection_v02.py): 기존 저작 연결/연도/언어/승인 차단을 점검.
- **공개 건수 0건**; 연구 시안은 Google AI Studio 앱에서 직접 import하거나 퍼블릭 파일로 배포하지 않음. 이미지 권리·사료 고증·사람 승인이 끝난 별도 릴리스 생성기 필요.

