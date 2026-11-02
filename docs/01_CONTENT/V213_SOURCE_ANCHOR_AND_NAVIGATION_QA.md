# V2.13 · 원고 ID 연결·출처 수준·읽기 경로 테스트

기존 독자 원고 10편을 참조하는 4개 탐색 경로, 19개 학습 단계 및 15개 전환을 별도 연구 객체로 생성했다.

## 검사 규칙
- 모든 경로 단계가 V2.11의 고유 section, paragraph, sentence ID에 정확히 대응하며 본문 코드포인트 범위를 일치시키는지 검사
- V2.12의 관계 ID가 존재하는 경우 두 단계의 chapter key가 실제 연결의 양쪽에 있는지 검사
- 관계가 없는 전환은 `PARALLEL_EDITORIAL_COMPARISON_NO_DIRECT_RECEPTION_ASSERTED`로 기록해 인과관계를 주장하지 않음
- 출처 레코드가 URL/등급/접근 상태를 가지되 개별 문장 원문 검증 필드를 false로 고정
- 발행 가능, 원전 직접 교감, 전문가 승인, 웹앱 통합 플래그 모두 false로 고정

## 주제별 경로와 편집 범위
- PATH-V213-AUTHORITY 누가 교회를 대표하는가?: 5개 단계 — WYCLIFFE → HUS → LUTHER1521 → ZWINGLI → TRENT; 각 단계에 서술형 해설·오해 방지 문장·연결된 원고 위치 포함
- PATH-V213-EUCHARIST 같은 성찬, 왜 다른 결론에 이르렀나?: 5개 단계 — WYCLIFFE → ZWINGLI → MARBURG → AUGSBURG → TRENT; 각 단계에 서술형 해설·오해 방지 문장·연결된 원고 위치 포함
- PATH-V213-EDITIONS 같은 책의 다른 판본을 읽는 법: 5개 단계 — HUS → LUTHER1517 → AUGSBURG → CALVIN1536 → CALVIN1559; 각 단계에 서술형 해설·오해 방지 문장·연결된 원고 위치 포함
- PATH-V213-IMPLEMENTATION 개혁은 선언 뒤에 누가 실행했나?: 4개 단계 — LUTHER1521 → ZWINGLI → AUGSBURG → TRENT; 각 단계에 서술형 해설·오해 방지 문장·연결된 원고 위치 포함

## 다음 조사 우선순위
문헌학 검증이 빠른 단서: Bridwell 1531년 소장 카탈로그, GHDI 마르부르크 제15조, St Andrews 트리엔트 회기. 더 어려운 교감은 위클리프·후스의 필사본, 1529 마르부르크 Z/K, 1540 Variata 라틴어 원본 판본. 목록을 열람한 것과 고판본 직접 판독은 별개다.

**기존 출판 보류와 별개 웹앱 병렬 개발은 그대로 유지한다.**