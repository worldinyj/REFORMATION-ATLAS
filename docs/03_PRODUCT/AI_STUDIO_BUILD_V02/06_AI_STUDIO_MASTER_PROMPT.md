# 06 · Google AI Studio Build — FIRST MASTER PROMPT
> **영문 보조 프롬프트**. 기본안은 [한국어 마스터 지시문](06_MASTER_BUILD_PROMPT.md). 두 개를 한 번에 실행하지 않음.
> 이 아래 **PROMPT START~END**를 Google AI Studio > Build > Web 앱 입력창에 복사한다.
> 먼저 **B1 UI Skeleton만 생성**한다. 나머지 기능은 [07 단계별 프롬프트](07_AI_STUDIO_ITERATION_PROMPTS.md)로 수행.
> 사용자는 배포가 아니라 **개인 프리뷰용** 초기 앱을 원한다.

---

## PROMPT START

You are a senior React/TypeScript engineer and an award-winning editorial product designer. Build the FIRST MILESTONE of a modern Korean-language historical exploration web app called **REFORMATION ATLAS / 종교개혁 아틀라스**.

### Product vision
A calm, beautifully typeset, modern web atlas that helps Korean readers explore the history of Christianity and the Reformation across 8 thematic volumes. The first milestone is a **functional UI skeleton** with real navigation; subsequent milestones will connect source-verified content records and progressively add deeper research without changing entity URLs.

### Mandatory platform assumptions
- Google AI Studio Build Web app. Prefer React + TypeScript using the existing generated scaffolding and package manager; do not forcibly replace the toolchain.
- Do not add Firebase, Google sign-in, Firestore, payments, Gemini inference/API calls, Cloud Run deployment or external CMS. These are NOT needed in B1.
- Keep state local to the demo app. Use modular components and accessible semantic HTML.
- **No automatic publishing, no GitHub push to main, no secret keys or paid service activation.**

### Mandatory design direction: QUIET EDITORIAL ATLAS
Visually restrained, exceptionally spacious, a contemporary historical editorial/museum aesthetic — NOT a vintage parchment theme.
- Canvas #F7F8F5; cards #FFFFFF; ink #1C2925; muted text #4B6058; one forest-green accent #205F50; hairline borders #DDE5DF.
- Korean body typography: Pretendard or Noto Sans KR with system-ui fallback. Optional Noto Serif KR used sparingly for display headings, not for small UI labels.
- Desktop H1 56–68px, mobile H1 36–42px. Body 16–18px, line-height around 1.7.
- Wide breathing room: content max-width 1200px, reading column ~720px; desktop horizontal padding 64px, mobile 20px; desktop section spacing 80–120px, mobile 48–64px.
- Desktop volume grid 4 columns, tablet 2, mobile 1. Long Korean titles must wrap gracefully.
- Crisp responsive navigation, visible keyboard focus, subtle hover transitions of 120–200ms, reduced-motion support. WCAG 2.2 AA is the accessibility target.
- Do not include giant stock hero images, fake historical portraits, heraldic emblems, purple AI gradients, repetitive pills, glassmorphism, dashboard KPI cards, carousels, parallax or distracting animation.
- The beauty should come from typography, grid, whitespace, elegant spacing and careful content hierarchy.

### B1: generate only these pages and interactions
1. Home / : a large typography-led hero (Korean headline: **시간과 사람을 따라, 종교개혁을 읽다.**) and subheading (초대교회에서 현대 한국 교회사까지, 사람과 사건 그리고 문헌으로 이어지는 역사의 흐름을 탐색합니다.), a primary link '8권 살펴보기', and a secondary link '연대표 탐색'.
2. A full 8-volume grid with working clickable cards and correct Korean titles.
3. /volumes : eight-volume index.
4. /volumes/:id : one reusable volume detail template with title, concise description, placeholder sections for people/events/documents/topics.
5. Shared site header, mobile navigation, breadcrumbs, footer/about link.
6. Lightweight /timeline, /people, /documents, /topics, /search routes can show a clearly marked **DEMO / 콘텐츠 연결 준비 중** empty state. Do not pretend they are fully implemented.
7. /about should describe the project’s research/editing/rights limitations.
8. Not-found route/empty state and keyboard-operable navigation.

### Exactly eight volumes
VOL-01 초대교회와 고대교회
VOL-02 중세교회와 개혁의 배경
VOL-03 종교개혁의 선구자
VOL-04 16세기 종교개혁
VOL-05 가톨릭 개혁과 종교적 갈등
VOL-06 부흥과 세계선교
VOL-07 세계와 한국 교회사
VOL-08 사상과 문헌 아카이브

Important: VOL-08 is NOT another chronological historical era. It is a cross-period archive of ideas and primary documents.

### Content safety
- Existing research is DRAFT, not publication-approved. For this FIRST milestone, use only the above volume labels and clearly labeled illustrative DEMO placeholder paragraphs, unless the original files are actually imported and you can prove the file paths and counts.
- If the connected GitHub repository is imported, NEVER assume all files are visible. Inspect the actual files before claiming import; do not alter historical source JSON/Markdown.
- Do not invent biographies, quotations, original historical manuscripts, event dates, public source references or precision-mapped historical locations to make the page look complete.
- Do not import unapproved AI historical illustrations or maps.
- Internal AI Studio preview only. Do not call Publish, Share or Deploy.

### Architecture constraints
- Components must be modular and reusable: SiteHeader, MobileNav, HeroIntro, VolumeGrid, VolumeCard, VolumeDetail, Footer, EmptyState.
- Keep design tokens centralized in CSS custom properties or the existing framework’s theme configuration.
- Preserve stable volume IDs in route parameters for future entity/detail expansion.
- Add readable loading, empty and error states; do not make inert buttons that claim to navigate.

### Before you finish
1. Generate code files and show a working preview.
2. Verify the home, /volumes and /volumes/VOL-04 routes.
3. Verify viewport widths 375px and 1440px, and mobile navigation.
4. Provide a concise change summary: files created, routes implemented, which items are DEMO, known limitations.
5. Explicitly confirm: no external deployment; no Gemini inference; no images or unreviewed historical data exposed.
6. Stop after B1. Do NOT try to implement all features at once.

## PROMPT END

---

## 사용자 사용법
1. [Google AI Studio](https://aistudio.google.com/)를 열고 **Build → Web**을 선택한다.
2. 위 마스터 프롬프트만 입력. 필요하면 DESIGN_TOKENS.json, 01~05 설계 문서를 AI Studio에 참고 파일로 붙인다.
3. 초기 미리보기를 확인: 8권 / 헤더 / 카드 / 데모 상세 템플릿 / 모바일.
4. 수정은 07의 B1→B2→B3→B4 순서대로 지시한다.
5. GitHub 동기화는 저장소 브랜치 확인 후 진행. AI Studio의 GitHub 가져오기 메뉴가 특정 브랜치를 노출하지 않으면 **현재 화면에서 지원하는 가져오기·동기화 절차를 확인**하고 main에 푸시하지 않는다.
6. 빌드에 데이터가 부족하면 AI Studio에게 역사 내용을 임의로 생성하게 하지 말고 GitHub의 source JSON을 별도로 제공한다.
