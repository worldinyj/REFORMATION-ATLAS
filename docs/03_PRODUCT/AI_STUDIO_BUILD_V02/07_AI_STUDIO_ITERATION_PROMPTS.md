# 07 · Google AI Studio Build — 단계별 수정 프롬프트
> 06 마스터 프롬프트의 B1 코드가 실제 생성·확인된 뒤, 아래 프롬프트를 **하나씩** 입력한다.
> 한 단계씩 빌드 결과와 실패 로그를 확인하고 다음 프롬프트로 이동. 이 문서는 코드 실행 결과가 아니다.

## B1-FIX — 디자인 점검 (필요할 때)
PROMPT:
> Keep the existing React/TypeScript app and all routes. Refine only the design to strictly follow Quiet Editorial Atlas: more generous whitespace, Korean editorial typography, warm off-white #F7F8F5 canvas, ink #1C2925, muted #4B6058, forest accent #205F50, 1200px max layout, ~720px reading width, 4/2/1 responsive volume cards. Remove heavy shadows, unnecessary gradients, giant images and any fake historical portraits. Verify at 375px and 1440px. Summarize what you changed.

검사: 헤더/히어로/8권 카드/권 상세가 같은 디자인 토큰 사용. 메뉴 기능 정상.

## B2-DATA — 원본 JSON 데이터 연결
PROMPT:
> Preserve the current approved UI components and tokens. Implement a read-only typed data adapter for the actual GitHub project source files: data/overview/volumes_and_people_v01.json; data/overview/events_documents_v01.json; data/overview/places_v01.json; data/overview/relationships_and_themes_v01.json; data/overview/source_register_v01.json; data/overview/legacy_person_crosswalk_v01.json. Do not fabricate missing data or modify historical source files. First check which source files are actually available in this AI Studio project and report counts. Expected inventory: 8 volumes, 33 people, 34 events, 20 documents, 22 modern place names, 10 topics, 32 relationships, 23 source IDs. If files are unavailable, stop the import and show DEMO state instead of claiming success. Preserve OV-P to PER mappings for Valdes/Wyclif/Hus, source types and date precision. No images, maps, Gemini inference, database or public deployment.

검사: import 진단에 전체 개수·누락 항목·ID 고아 관계 기록. 원래 JSON 수정 없음.

## B2-GATE — 데이터 공개 방지/승인 경계
PROMPT:
> Implement explicit publication-deny-by-default architecture. DRAFT source records must not be placed in any public deployment build's HTML, JS, JSON, source map, static assets or search index unless individually approved. The current research has zero approved public records. Personal development preview may show a DRAFT watermark, but merely hiding DOM content with CSS is not security. Add tests proving that unapproved research images, historic-coordinate claims and manuscripts cannot leak to a public build. Never press Publish or Share; do not add noindex as a substitute for access control. Do not copy GitHub source research to a public hosting service.

검사: 공개 스냅샷 0건인 상태에서 출력 허용 데이터 0건, 후보 WebP/SVG 노출 0.

## B3-PAGES — 세부 화면 연결
PROMPT:
> Keep the exact same Quiet Editorial Atlas design and real imported source IDs. Build /people, /people/:id, /timeline, /events/:id, /documents, /documents/:id, /topics, /topics/:id and /places with React components. People detail starts with short OVERVIEW and has a DEEP_RESEARCH extension slot for future approved content. Timeline must render date_label as written (do not invent precise dates from year_start). Documents must distinguish historical original, later edition, translation and academic review. Places are text-only; 22 places have no verified coordinates, so no map pins. VOL-08 is a cross-era archive. Add source references and typed related-content links. Do not invent historical materials or mark research as approved.

검사: 인물·사건·문헌·주제·장소 목록과 상세, 관계 의미, 정확/근사 날짜.

## B3-SEARCH — 검색과 탐색
PROMPT:
> Add a single calm, accessible search interface with Korean/English aliases, content-type filters and explicit empty states. Test 루터/Martin Luther, 후스/Hus, 1517 and 성찬론. Search only data actually imported for the internal review, and use publication-allowlisted data for any exportable public search index. Keep keyboard and mobile navigation usable. Never show a fake historical quotation or 'verified' label just because a search result exists.

검사: 검색어·필터·결과 없음/준비 중/404, URL 직접 진입, 접근성.

## B4-ACCESSIBILITY — 화면 검수
PROMPT:
> Audit the app at 320, 375, 768, 1024 and 1440 px. Fix overflow, typography, grid and header spacing. Ensure skip link, semantic headings, keyboard focus, mobile menu ESC/focus handling, accessible inputs and reasonable touch targets. Honor prefers-reduced-motion. Keep the spacious Quiet Editorial look rather than compressing everything into crowded cards. Report specific issues fixed; don't claim WCAG certified unless actually tested with tools and manual checks.

검사: 실제 브라우저 미리보기·키보드·모바일 검증 증거.

## B4-GITHUB — 코드 정리와 안전 동기화
PROMPT:
> Run the available build and type checks, inspect Git diff, and prepare only the generated app code and relevant design documentation for a new GitHub feature branch. Do not change or overwrite research files or the protected main branch. Check for secrets in client-side bundles, drafts/assets accidentally copied into public output, missing links and dependency versions. Show the list of changed files and the exact verification result; do not claim tests that were not executed. Do NOT deploy or publish.

검사: 빌드 성공, diff 검토, 브랜치 확인, 실제 테스트 증거.

## P1-DEPTH — 나중의 심층 콘텐츠 추가
PROMPT:
> Without recreating the page template or changing its canonical entity ID and permalink, add an approved DEEP_RESEARCH content block for the supplied person or event. Keep the original overview above it. Include citation, edition/translation access tier, confidence and revision history. Do not copy paywalled source text or use unapproved historical portraits. If approval metadata is absent, store as DRAFT for private review and exclude from any public output.

검사: 동일 URL/기존 링크, 판본·출처, 사용자 승인 및 공개 별도.

## 오류 처리 지시문
PROMPT:
> Before making more changes, inspect the actual files and build errors. Explain the minimal cause and fix only the failing step. Preserve existing working routes and design tokens. Do not reset the project or invent source records. Re-run the failed validation and report exact result.

## 중요
Google AI Studio는 개발·미리보기·코드 동기화 도구이다. **역사적 사료를 검증하는 전문가를 자동으로 대신하지 않으며**, 생성 UI가 멋지게 보인다는 이유만으로 자료 출판 승인이 되는 것은 아니다.
