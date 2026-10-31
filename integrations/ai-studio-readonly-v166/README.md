# V1.66 · AI Studio 연계용 읽기 전용 데이터 어댑터

이 모듈은 **Google AI Studio의 실제 앱을 수정하지 않습니다.** 연구 데이터의 서로 다른 JSON 규격을 단일 미리보기 데이터로 조합하는 순수 JavaScript 모듈입니다. 현재 앱의 TypeScript·프레임워크 구조가 확인되지 않았으므로 특정 앱에 바로 삽입 가능한 완성 통합코드라고 주장하지 않습니다.

## 입력

`buildAtlasPreview({manifest,narratives,cities,geoLinks,editions,evidence,navigation})`

각 입력은 순서대로 V1.65 통합 매니페스트, V1.56 심층 해설, V1.57 도시 좌표 및 연결, V1.61 판본, V1.63 증거 카드, V1.64 증거 탐색 JSON을 직접 import한 **객체**입니다. 네트워크 요청·데이터베이스 쓰기·브라우저 저장소 호출 없음.

## 출력
`{contractVersion,mode,canPublish,readerCards,mapPins,datedLinks,editionCards,claimCards,mediaPolicy}`

- `canPublish=false` — 모든 미리보기 자료는 정식 게시 불가
- `isVerifiedPrimary=false`, `originalVerified=false` — 원문 미교감 명시
- `canPublishImage=false` — 원작·영인 이미지 권리 승인 전 미표시
- `accuracy=CITY_APPROXIMATE` — 역사적 건물 정밀 위치로 사용 금지

## 앱 적용 시 순서
1. AI Studio의 실제 데이터 스키마를 별도로 확인한다.
2. 로컬 개발 환경에서 기존 JSON을 읽기 전용 import로 연결한다.
3. 미리보기 페이지에서만 호출하고 반환값을 기존 UI 컴포넌트의 props로 변환한다.
4. 학술 감수·이미지 권리·정본 ID·앱 스키마를 모두 승인하기 전 공개 경로에는 연결하지 않는다.

## 검증
`python3 scripts/validate_atlas_v166.py`는 입력 수와 보안 기본조건을 확인한다. Node를 사용할 수 있다면 별도 `node --test integrations/ai-studio-readonly-v166/adapter.test.mjs`에서도 실제 변환 경로를 검사한다.
