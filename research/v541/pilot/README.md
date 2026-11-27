# V5.41 — 첫 이식 후보: 마르부르크·아우크스부르크

**RESEARCH ONLY.** 실제 AI Studio 호스트 소스/라우터/권한 미확인. can_ship=false, can_import_ai_studio=false, can_merge_main=false. 기존 앱에 적용하거나 배포하지 않았다.

## 사용 계약
- `pilot_content.json`: V5.39에서 그대로 추출한 L448-04-02 전체 원고, 역사 사례 3개, 신학 해설 3개, 기존 화면 후보 4개.
- `pilot_panel.mjs`: 프레임워크 독립형, 전용 DOM 요소에 추가 영역만 삽입. `destroy()`는 해당 영역만 제거. React 등 호스트에서는 승인 이후 전용 ref 및 effect 정리 단계와 연결한다.
- `pilot_panel.css`: `.atlas-pilot-v541` 범위에 한정. 실제 호스트의 상속 스타일 및 레이아웃 충돌은 별도 검증.
- `augsburg.svg`: V5.39 원본과 동일 Git blob.
- 깊이별 원문은 안전한 텍스트 노드로 표시. Markdown은 문자 그대로 표시하므로 최종 UI에서는 호스트의 안전한 Markdown 렌더러를 검토해야 한다.
- `node research/v541/pilot/test_pilot.mjs`: 모의 DOM 시험 재현. 연결 환경에서 함수 실행 20/20; Node 명령 자체나 실제 브라우저 실행은 미검증.

## 승인 이후에만 적용할 계약 예시
```js
import {mountPilot} from './pilot_panel.mjs';
// hostRecord는 실제 기존 앱이 로드한 원본 객체여야 함.
// pack은 접근 제어가 적용된 연구 환경에서만 전달.
const handle = mountPilot(dedicatedElement, {
  pack, hostNamespace: 'ATLAS_OVERVIEW_V01',
  kind: 'event', hostRecord,
  reviewEnabled: authorizedReviewMode,
  diagramPath: verifiedHostAssetPath
});
// 페이지 전환 또는 컴포넌트 해제 시
handle.destroy();
```
`reviewEnabled`는 보안 인증이 아니라 UI 표시 조건. 전체 연구 JSON을 미승인 공개 앱 번들에 넣지 않는다. 연구 저장소는 공개 상태이다. 호스트 접근권한 및 연구 자료 취급 정책을 별도로 확인한다.

## 실제 앱 이식 전 인수 기준
1. 실제 앱의 OV-E-018 및 제목, 라우터, 소스 및 인증 경계를 확인.
2. 호스트의 기존 상세 화면과 뒤로 가기, 링크, 레이아웃 및 기존 데이터 보존.
3. 첫 화면 OV-E-018만 시범 연결하고 나머지 세 후보는 후속 검토.
4. 개요·중간·심층 전환, 문헌 SVG 및 출처 표시 확인.
5. 모바일 360px/768px, 데스크톱 1440px, 키보드 및 실제 브라우저 오류 검사.
6. 1531·1540 제10조 원판 직접 교감 미완료 등 연구 한계 유지. 전문가 검토 이후 별도 승인.
7. 운영 앱 배포, main 병합, 공유 금지.

## 남은 차단 조건
실제 AI Studio 앱의 연결 저장소/브랜치 또는 비밀키 제거된 소스 내보내기 필요. 소스 없이 기존 앱에 자동 적용했다고 표시하지 않는다.
