# V5.36 — 통합 품질검사 및 적용 준비 판정

8권 24장, 52개 사례, 36개 좌표, 10명 인물과 활성 SVG 23개에 대한 구조 및 참조 연결 검사 완료. V5.34 원고 변경 없음. 2개 시범 WebP는 저장소 등록 대기 상태이므로 렌더 대상에서 제외.

- [content_qa.json](content_qa.json): 15/15
- [maps_qa.json](maps_qa.json): 8/8
- [diagrams_and_people_01_qa.json](diagrams_and_people_01_qa.json): 10/10
- [people_02_qa.json](people_02_qa.json): 5/5
- [link_qa.json](link_qa.json): 11/11

[콘텐츠-시각 자산 통합 색인](content_visual_link_index.json)

## 판정

검토용 통합 패키지 준비는 가능. 실제 웹앱 반영 및 배포는 보류. 구조 검사와 시각적 검수는 별개이다.

- QA-01: Browser and mobile visual QA: typography, marker overlaps, small islands, color contrast, accessibility — NOT_RUN
- QA-02: Two WebP pilot portraits not registered in repository; use SVG fallback — PENDING
- QA-03: Historical and theological specialist review, current source URL checks, independent geocoding — NOT_RUN
- QA-04: AI Studio data schema and end-to-end app acceptance — NOT_RUN

다음: V5.37 검토용 데이터·시각 자산 패키지 작성, 스키마 계약과 누락 자산 대체 처리, 브라우저 검수 및 앱 E2E 테스트 계획. 실제 앱 변경 없이 연구 브랜치 유지.
