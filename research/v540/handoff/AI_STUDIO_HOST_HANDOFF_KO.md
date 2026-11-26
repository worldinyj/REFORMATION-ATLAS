# V5.40 — 기존 AI Studio 앱 연결 준비

## 확인된 범위
- 연구 저장소 main: README만 존재. 초기 설계 브랜치 chore/ai-studio-github-readiness-v01의 SCREEN_CONTRACT.json과 개요 JSON을 기준으로 작성.
- 과거 integration/atlas-phase1-browser-qa-v452의 AtlasCrossVolumeResearchPanel.jsx는 연구 후보 패널이며 실제 호스트 앱이 아님. README도 실제 호스트 코드 미확보를 명시한다.
- worldinyj/REFORMATION-ATLAS-WEB 후보 조회 404: 해당 이름의 접근 가능한 저장소를 찾지 못했을 뿐, 다른 위치의 앱 존재 여부는 판단하지 않는다.
- 기존 개요 127개 중 관련 연구 읽기 83개, 미연결 44개. 인물 동일성 3개만 명시, 신규 인물 7명은 자동 병합하지 않음. 32개 기존 관계 수정 없음. 관련 읽기는 인물/사건/문헌 동일성이나 인과의 근거가 아니다.

## 파일과 사용 계약
legacy_crosswalk.json: 기존 ID와 표시명, 연결 유형, 새 자료 ID, 출처 blob SHA.
research_adapter.mjs: 명시적 검토 모드 및 호스트 네임스페이스를 요구하는 읽기 전용 어댑터. getSupplement(kind,hostRecord)는 실제 호스트 ID와 정확한 한국어 표시명 또는 제목이 일치할 때만 관련 자료를 반환. 미확정이면 null. 반환 필드 chapters, cases, people, theology_units, global_units, assets. 기존 데이터와 URL을 수정하지 않음. listNewPeople는 자동 통합 목록이 아닌 검토 후보.
test_adapter.mjs: 로컬 재현용 Node 스크립트; node research/v540/handoff/test_adapter.mjs. 이 파일 자체의 Node 실행은 하지 않았으며 어댑터 함수 실행 시험은 연결된 JS 환경에서 수행함.
atlas_preview.json: research/v539/site/에 존재. asset.preview_path는 해당 패키지 상대경로이며 호스트 공개 URL로 가정하지 않는다.

## 다음 단계: 실제 호스트 앱 인벤토리 확보
AI Studio에서 실제 앱을 열고 Code 소스 내보내기 또는 연결 GitHub 저장소/브랜치를 제공한다. API 키, .env, 사용자 데이터 제외. 확인 대상은 package.json/lockfile, 라우터, 개요 데이터 로더 및 실제 ID, 상세 페이지 컴포넌트, 인증/접근 제어, CSS 또는 디자인 토큰, 기존 빌드/테스트 명령.
앱 코드가 확보되면 실제 데이터를 원본 127개 ID 및 표시명과 대조하고 차이를 검토한다. 일치하지 않는 레코드는 자동 연결하지 않는다.

## 승인 이후 AI Studio에서 사용할 읽기 전용 사전점검 프롬프트
현재 앱을 수정하지 말고 라우트, 상세 페이지 컴포넌트, 데이터 로더와 실제 객체 ID, 표시명, 인증 경계를 조사해 파일 경로와 근거를 보고하라. V5.40 legacy_crosswalk.json의 기존 ID와 비교하여 동일, 변경, 누락, 신규를 구분하라. 기존 데이터/기능/라우트/CSS를 덮어쓰거나 연구 JSON을 클라이언트 공개 번들에 넣지 마라. 배포·공유·main 변경·자동 동기화를 하지 마라. 이 사전점검을 검토한 뒤에만 통합 계획을 확정한다.

## 판정
첫 이식 후보: 기존 VOL-04 상세 또는 OV-E-018 마르부르크 회담 화면에 L448-04-02의 읽기 자료를 추가하는 별도 검토 블록. 실제 라우터와 인증 확인 후에만 실행한다. 기존 개요와 연구 심화의 차이를 명시하고 직접 원전 교감 미완료 사항을 보존한다.
현재 can_ship=false, can_import_ai_studio=false, main 병합 없음. 실제 운영 앱 호환성/브라우저 QA/전문가 검토 미완료. 연구 저장소는 공개이며 플래그/어댑터 UI 차단은 실제 접근 제어가 아니다. 비공개 자료는 권한이 통제되는 환경에서만 취급해야 한다.
