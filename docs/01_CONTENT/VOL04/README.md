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
