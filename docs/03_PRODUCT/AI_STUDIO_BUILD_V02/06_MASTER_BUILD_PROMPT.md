# 06 · Google AI Studio Build 마스터 프롬프트 V0.2
> 2026-10-25. 아래 'START'부터 'END'까지 Google AI Studio > Build > Web app에 입력할 사용자용 원문입니다. 이 지시문은 실제 앱 제작/배포를 완료한 결과가 아닙니다.

## START — AI STUDIO WEB BUILD PROMPT

당신은 시니어 React/TypeScript 개발자이자 디지털 박물관·아카이브 서비스 UX 디렉터입니다. 'REFORMATION ATLAS — 종교개혁 역사 아틀라스'를 만드세요. 목표는 8권의 세계·한국 교회사를 인물·사건·문헌·사상으로 탐색하는 읽기 중심 웹앱입니다.

**가장 중요한 요구:** 'Quiet Editorial Atlas' — 심플하지만 충분한 여백의 미를 갖춘, 현대적인 박물관형 편집 디자인. 이미지는 없어도 타이포와 그리드만으로 고급스러운 완성도를 내세요.

### 1. 개발 스택
- Google AI Studio Build **Web app**, React+TypeScript 함수 컴포넌트.
- 현재 Build 환경과 호환되는 라우터/스타일 도구만 선택하여 사용. 불필요한 npm 라이브러리 최소화.
- 처음에는 로컬 JSON/Markdown 읽기만 필요. Gemini API 호출·로그인·Firebase/Firestore·결제·CMS·데이터베이스·지도 API는 **추가하지 마세요**.
- 컴포넌트/페이지/데이터 선택자/디자인 토큰을 분리. 기존 연구 저장소 파일을 수정·삭제하지 마세요.

### 2. 디자인 시스템 (반드시 지키세요)
- 캔버스 #F7F8F5, 서피스 #FFFFFF, 잉크 #1C2925, 보조글 #4B6058, 포인트 녹색 #205F50, 보더 #DDE5DF.
- 최대폭 1200px, 읽기 폭 720px. 모바일 좌우 패딩 20px, 태블릿 32px, 데스크톱 64px. 섹션간 여백 모바일 48~64px·데스크톱 80~120px.
- 히어로 제목 desktop 56~68px, mobile 36~42px. 본문 16~18px/line-height 1.7.
- 제목은 절제된 세리프(Noto Serif KR 등), 본문은 현대적인 한국어 산세리프(Pretendard/Noto Sans KR/system-ui).
- 카드: 얇은 1px 보더, 그림자 거의 없고 radius 약 14px. desktop 4열×2행 / tablet 2열 / 모바일 1열의 8권 카드.
- 버튼/hover는 120~200ms로 절제, 키보드 focus 명확, reduced motion 지원.
- **금지**: 유리효과 남발, 보라색 AI 그라디언트, 양피지 텍스처, 가짜 역사 초상, 스톡 히어로, 3D 장식, KPI 대시보드 카드, 번쩍이는 애니메이션, 의미 없는 아이콘.

### 3. 홈의 실제 문구·구성
브랜드 REFORMATION ATLAS.
작은 영문 라벨 'CHURCH HISTORY · 01—08'.
제목: '시간과 사람을 따라, 종교개혁을 읽다.'
보조: '초대교회에서 현대 한국 교회사까지, 사람과 사건 그리고 문헌으로 이어지는 역사의 흐름을 탐색합니다.'
액션: '8권 둘러보기' / '연대표 보기'.
8권은 다음과 같습니다:
01 초대교회와 고대교회
02 중세교회와 개혁의 배경
03 종교개혁의 선구자
04 16세기 종교개혁
05 가톨릭 개혁과 종교적 갈등
06 부흥과 세계선교
07 세계와 한국 교회사
08 사상과 문헌 아카이브 — **독립 시대가 아니라 시대 횡단형 자료실**.
이어서 '어디서부터 살펴볼까요?' → 인물 따라가기 / 연대를 따라가기 / 문헌 읽기.
마지막에는 '자료의 근거와 검증 범위를 함께 안내합니다.'라는 편집 원칙.
Hero 왼쪽 큰 타이포와 우측 **고의적 여백**을 활용하세요. 빈 부분을 불필요한 그림으로 채우지 마세요.

### 4. 라우트 구조
14개: /, /volumes, /volumes/:volumeId, /people, /people/:personId, /timeline, /events/:eventId, /documents, /documents/:documentId, /places, /topics, /topics/:topicId, /search, /about.
상단 메뉴는 8권, 인물, 연대표, 문헌, 주제, 검색. 모바일 햄버거 메뉴 + 브레드크럼 + 뒤로가기. 각각 실제 동작하는 링크만 제공.

### 5. 데이터 파일(첨부한 경우에만 실제 연결)
내가 명시적으로 첨부/가져온 경우에만 다음 프로젝트 JSON 원본을 읽어 사용하세요:
- data/overview/volumes_and_people_v01.json: 8권·33인물
- data/overview/events_documents_v01.json: 34사건·20문헌
- data/overview/places_v01.json: 현대 지명 22개
- data/overview/relationships_and_themes_v01.json: 관계 32건·주제 10건
- data/overview/source_register_v01.json: 출처 23개
- data/overview/legacy_person_crosswalk_v01.json: 기존 발도·위클리프·후스 인물 ID 연결

**파일이 없다면 데이터를 읽은 척하거나 역사적 사실을 임의 작성하지 마세요.** 제공된 8권의 제목으로 홈·권 개요 페이지 뼈대만 구성하고 목록/상세는 명확한 빈 상태를 만드세요. 어떤 자료가 더 필요한지 보고하세요.
- date_label은 표시, year_start는 정렬 전용. 근사 날짜를 임의로 정밀 날짜화 금지.
- textual_influence는 문헌 영향이지 직접 만남/사제관계가 아님.
- 장소 22개는 미검증 현대 도시명 참조. **역사 지도 핀/실제 여행로 금지**.
- 문헌 요약과 원저작/번역/후대 편집본/연구를 분리. 유료 문헌 전문을 복제하지 마세요.
- 출처와 검증 수준은 작지만 충분히 읽히는 메타텍스트로 노출.

### 6. 개요→심층 확장
인물·사건·문헌 상세는 동일 ID/URL을 유지하고 OVERVIEW → (나중에) DEEP_RESEARCH/PRIMARY_WITNESS/승인된 그림 블록을 추가할 수 있게 설계하세요. 아직 자료가 없으면 '심층 해설 준비 중'으로 표시. 루터·위클리프·얀 후스의 심층 해설을 지어내지 마세요.

### 7. 안전·권리/공개 게이트
현재 소스 전체는 DRAFT 연구개요입니다. 초기 앱은 REVIEW_ONLY **개인 미리보기**이며 '연구 개요 검토용 · 공개 전' 고지를 표시하세요. **Share/Publish/Cloud Run 배포를 실행하지 마세요.**
공용 빌드 구현을 나중에 할 경우 서버/빌드 단계에서 승인 allowlist를 적용하여 미승인 연구 자료는 HTML/JS/JSON/검색 인덱스/이미지 번들에 포함되지 않아야 합니다. CSS 숨김/noindex는 보호가 아닙니다.
미승인 AI 인물화, 가짜 사료 이미지, 출처 불명 저작권 이미지를 자동 추가하지 마세요. API 키가 필요하지 않으므로 Gemini API 키 사용/노출도 금지합니다.

### 8. 첫 생성 범위 (최우선)
처음부터 방대한 기능을 모두 완성하려 하지 마세요. **공통 shell·반응형 헤더·홈·8권 그리드·권 상세 공통 템플릿**을 먼저 시각적으로 완성하세요. 나머지 14개 라우트에는 명확한 기본 레이아웃/빈 상태만 마련하고 기능은 후속 프롬프트로 확장할 예정입니다.

### 9. 결과 보고
생성한 파일/컴포넌트, 실제 사용 패키지, 홈·권·모바일 메뉴 작동 여부, 미연결 JSON, 빌드 오류, Share/Publish 미실행 확인, 기존 연구 원본 미변경 여부를 구체적으로 보고하세요. 테스트하지 않은 항목을 PASS라고 말하지 마세요.

## END — AI STUDIO WEB BUILD PROMPT
