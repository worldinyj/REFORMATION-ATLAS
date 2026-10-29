# 제5권 V1.14 — Münster·Essen·Paderborn 통합 연표와 지도용 데이터

**DRAFT_RESEARCH_NOT_PUBLIC** | 2026-10-29 | V1.13에서 분기

## 연구 결론
1652년 뮌스터의 교육수녀 3명이 에센으로 이동한 사건, 1652년 10월 21일 파더보른 설립 승인문서, 1658년 3월 28일 뮌스터 출신 수녀 2명의 파더보른 도착·교육 개시를 서로 분리한다. 1669년 파더보른 내 건물 이전은 같은 도시 내 이동이며 뮌스터로부터 새로 이동한 사건이 아니다.

## 통합 사건 연표
| 연도·날짜 | 장소 | 사건 | 출처 수준 |
|---|---|---|---|
| 1652 | 뮌스터→에센 | 수녀 3명 이동, 학교 개설 | 에센 수도회 공식 연혁 |
| 1652-10-21 | 파더보른 | 설립 관련 주교 Gnadenbrief | 성 미카엘 학교 연혁 |
| 1658-03-28 | 뮌스터→파더보른 | 수녀 2명 도착, 무료학교 교육 개시 | 학교·수도원 연혁 |
| 1669-04 | 파더보른 | Meyer 가옥으로 이전 | 수도원 연혁 |

## 지도 설계
이벤트 이동선은 두 개다: Münster→Essen (1652), Münster→Paderborn (1658). 지도의 점은 **현대 도시 중심의 근사 좌표**이며 17세기 학교/수도원 정확한 위치를 뜻하지 않는다. 지도상 직선은 관계를 시각화할 뿐 역사적 이동 경로를 재현한 것이 아니다. 1652년 파더보른 허가는 이동선이 아니라 장소에 귀속되는 행정 사건으로 표시한다.

## 공통 콘텐츠 규격 제안
- `entities`: person, institution, place, work, document 등 타입
- `events`: id, dates (precision과 uncertain 분리), agents, places, relations
- `claims`: assertion, evidence_sources, evidence_level, review_status
- `sources`: 서지, 판본, URL, 원전/2차문헌 유형, 열람 범위, 권리
- `media`: 제작자·판본·권리·시대재현 여부·출처
- `publication_gate`: claim별 및 콘텐츠 패키지별 human 승인 및 검증
제1~5권 전체로 확장하기 전 기존 데이터 규격과의 마이그레이션 매핑을 수행한다. 현재 규격은 **시범 초안**이다.

## 차기 검증
1. 실제 1652년 Essen Stiftung 문서와 1652 Paderborn Gnadenbrief 판독.
2. 도시 중심 점을 17세기 실제 지점으로 치환하려면 역사 지도와 원전 좌표 확인.
3. 저작권 있는 사진·문서의 앱 배포 금지.
4. `publication_gate.can_ship = false` 유지.

## 근거
- https://www.kloster-bmv.de/augustiner-chorfrauen/unsere-geschichte/
- https://www.michaelsschule.de/index.php/unsere-schule/neun-gute-gruende-2
- https://www.michaelskloster.de/michaelskloster/geschichte/
