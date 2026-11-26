# V5.37 — 검토용 통합 콘텐츠 패키지

V5.34 역사 원고와 V5.36 연결 색인, 구조 검사된 23개 SVG를 기준으로 통합 데이터와 검색 색인을 생성했다. 현재 연구 브랜치에는 원본 SVG가 상위 연구 폴더에 존재하며 이 디렉터리는 자산 해시와 경로를 참조한다. ZIP은 아직 생성하거나 실행 검증하지 않았다. 로컬에서 build_preview_package.py를 실행하면 원본과 일치하는 자산을 ZIP으로 복사한다.

- atlas_preview.json: 8권 24장, 52개 사례, 36개 좌표, 10명, 5개 신학·6개 지역 해설.
- search_index.json: 24개 장의 검색 텍스트.
- asset_manifest.json: 활성 SVG 23개, Git blob SHA 고정.
- package_qa.json: 데이터 및 참조 검사 결과.
- DATA_CONTRACT.md: 필드 및 자산 해석 규칙.
- AI_STUDIO_REVIEW_GUIDE_KO.md: 향후 승인 이후 적용 프롬프트와 시험 계획.
- build_preview_package.py: 검토용 ZIP 생성 스크립트.

시범 WebP 2개 제외, 상징형 카드 유지. 앱 적용이나 배포 없음. can_ship=false, can_merge_main=false, can_import_ai_studio=false.
