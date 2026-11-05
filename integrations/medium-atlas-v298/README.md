# V2.98 심화정보 앱 연결 모듈

현재 V2.97의 435편 전달본을 **독립 검토 환경에서 읽는 실행 가능한 모듈**이다. 실제 Google AI Studio 앱의 최신 소스는 이 연구 저장소에서 확인되지 않았다. 따라서 이 모듈의 실행과 실제 앱에 반영된 상태를 구분한다. main·기존 원고·실제 앱을 수정하지 않는다.

## 이번에 완성한 범위

- 435편 목록·상세, 한국어·본문 검색, 분야 필터와 페이지 나눔
- 관련 해설 이동, 8개 분야 목록, 지역·연대·쟁점별 읽기 경로 18개
- 기존 읽기 경로 6개·비교표 6개·FAQ 12개
- 출처 626건, 독자용 안내 11개, 선택 주장 22건과 원고 내 위치
- 현재 접근 실패·부분 접근·확인 대상 아님과 과거 접근 기록의 구별
- 부분 뒷받침과 전문 감수 미완료 표시, 자료 사용 주의사항
- 입력 오류 검출, 입력·출력 객체의 변경이 내부 인덱스에 미치는 영향 차단

외부 패키지는 필요 없다. `adapter.mjs`는 fetch·DOM·저장 기능 없이 전달된 JSON 객체를 읽는다. 테스트는 Node의 내장 테스트 도구를 사용한다. 선언 파일 `adapter.d.mts`는 편집기의 TypeScript 타입 안내용이다. 이번 환경에는 TypeScript 컴파일러가 없어 별도 tsc 검사는 수행하지 않았다.

## 기존 구조와의 대조

| 항목 | 저장소의 이전 V1.66 어댑터 | 이번 V2.98 모듈 |
|---|---|---|
| 입력 | manifest·narratives·cities 등 7개 객체 | V2.97 전달본 객체 1개 |
| 본문 | `narratives.pages[].segments[].text` | `readers[].sections[].body` |
| 읽기 규모 | 시범 10편 | 중간 깊이 435편 |
| 출처 | 단순 URL 배열 | 자료 ID·성격·날짜별 접근 상태·확인 범위 |
| 탐색 | 시범 지도·문헌·근거 카드 | 목록·상세·검색·분야·읽기 경로·비교·FAQ |
| 지리·정밀 연대 | 근사 도시 좌표와 별도 연결 | 제공하지 않음. 읽기 경로에서 좌표나 날짜를 추출하지 않음 |
| 공개 | 연구 검토 전용 | 편집 검토 전용 |

구형 `buildAtlasPreview()`의 인수를 그대로 바꾸어 넣는 방식으로 호환되지 않는다. 기존 모듈을 덮어쓰지 말고, 별도 검토 화면에서 새 API를 호출한다. 실제 앱의 overview ID·라우트·컴포넌트 구조는 별도 확인 대상이다. `MEDIUM-*`, `PERSON-*` 같은 이 전달본의 ID를 앱의 기존 `OV-*` ID와 자동으로 같다고 취급하지 않는다.

## 입력 파일과 고정 버전

`manifest.json`은 입력 경로·커밋·SHA256과 기대 수량을 기록한다. 입력은 다음 한 파일이다.

`data/deep/atlas_v297_source_checked_medium_content_delivery_bundle.json`

이전 35개 회차의 원고 파일을 앱에서 순서대로 읽을 필요가 없다. 입력 버전이 바뀌면 재검토 후 계약과 manifest를 갱신한다. 어댑터는 현재 2.97 편집 초안만 수용한다. 해시 검증은 테스트에서 수행하고, 모듈은 전달받은 객체의 구조와 내부 연결을 검사한다. 임의로 변경한 객체가 원래 파일과 바이트 단위로 같다는 것을 구조 검사만으로 보장하지 않는다.

## 실행 예시

저장소 루트에서:

```bash
node --test integrations/medium-atlas-v298/adapter.test.mjs
```

Node에서 읽기:

```js
import {readFileSync} from 'node:fs';
import {createMediumAtlas} from './integrations/medium-atlas-v298/adapter.mjs';

const bundle = JSON.parse(readFileSync(
  'data/deep/atlas_v297_source_checked_medium_content_delivery_bundle.json', 'utf8'
));
const atlas = createMediumAtlas(bundle);
const results = atlas.search('카를 5세', {limit: 10});
const detail = atlas.getReader('MEDIUM-LUTHER1521');
const paths = atlas.listReadingPaths({axis: 'REGION'});
const guide = atlas.getSourceGuide('MEDIUM-LUTHER1521');
```

브라우저 검토 코드에서도 같은 함수를 사용한다. 호스트가 이미 읽은 JSON 객체를 인수로 전달하면 된다. 이 모듈은 네트워크에서 자료를 찾거나 임의의 최신 파일로 대체하지 않는다. 실제 앱의 공개 경로에 연구 JSON을 복사하는 단계는 이번 작업에 포함되지 않는다.

## 화면에서 사용하는 반환값

| 기능 | API | 주요 반환값 |
|---|---|---|
| 전체 목록 | `listReaders()` | ID·제목·도입·분야 |
| 상세 | `getReader(id)` | 본문 세 절·질문·관련 해설·출처·출처 읽기 안내 |
| 검색 | `search(query, options)` | 전체 결과 수·현재 페이지 결과 |
| 분야 | `listGroups()` | 분야 이름·해설 ID 목록 |
| 읽기 경로 | `listReadingPaths({axis})` | 이름·순서·질문·해석의 범위 |
| 경로 상세 | `getReadingPath(id)` | 새 경로 또는 기존 경로 |
| 출처 | `getSource(id)` | 링크·자료 성격·현재 접근 결과·과거 기록 |
| 출처 읽기 안내 | `getSourceGuide(readerId)` | 읽기 안내·선택 주장·우선 자료·주의사항 |
| 주장 위치 | `getClaim(id)` | 원고 ID·절 번호·정확한 구간·근거 위치·판정 |
| 비교·FAQ | `listComparisons()`, `listFAQ()` | 기존 자료와 해설 ID |
| 이전 핵심 연구 | `getResearchBasis(id)` | 기존 연구 원고와 사료 주석 |

없는 ID의 조회는 `null`이다. 검색은 공백으로 나눈 모든 검색어를 포함하는 결과를 반환한다. 한국어 띄어쓰기 차이와 영문 대소문자·전각 문자를 정규화하며, 제목·도입을 우선 정렬한다. 본문과 절 제목도 검색한다. 오타 교정·형태소 분석·동의어 확장은 제공하지 않는다. 정확한 연대·위치·영향 관계를 검색 결과에서 추론하지 않는다.

페이지 나눔은 `offset`과 `limit`을 사용하며 limit은 1~100이다. `type`에는 `MEDIUM`, `THEME`, `REGION`, `GLOBAL`, `PERSON`, `DOCUMENT`, `CITY`, `EVENT`를 사용한다.

## 출처와 확인 상태 표시

현재 접근 결과는 `source.access`에서 읽고 과거 열람 기록은 `historicalAccessRecord`로 구분한다. `NOT_CHECKED`는 이번 점검 대상이 아니라는 뜻이다. `PAGE_RETURNED`는 페이지가 반환되었다는 뜻이며 원고 전체의 사실 검증이나 전문가 승인이 아니다.

출처 읽기 안내의 `verificationNote`, 주장의 `label`·`evidence_summary`·`source_locator`, 자료의 `access.note`를 함께 보존한다. 선택 주장 중 부분 뒷받침 1건을 완전 검증으로 표시하지 않는다. 모든 원고와 출처의 `expertApproved`는 false이며, 이는 그 내용이 거짓이라는 뜻이 아니라 전문 감수 완료를 주장하지 않는다는 뜻이다.

문자열은 React의 텍스트 자식이나 `textContent`로 출력한다. `innerHTML` 또는 HTML 문자열 템플릿으로 해석하지 않는다. 출처 링크는 새 탭을 쓸 경우 `rel="noopener noreferrer"`를 함께 지정한다. 어댑터 자체는 HTML이나 이미지를 생성하지 않는다.

## 검증 결과와 실앱에 남은 작업

새 GitHub 워크플로 `Medium Atlas V2.98 Consumer QA`에서도 같은 내장 테스트를 실행한다. 추가 패키지 설치는 없다.

35개 테스트로 435편의 본문·질문·출처·관련 연결, 검색과 페이지 나눔, 11개 안내와 22개 주장, 전체 탐색 경로, 객체 변경 격리를 검사한다. 버전·공개 상태·중복 ID·누락 자료·잘못된 참조·위험 URL·주장 구간 변경 등 26개 오류 입력도 검사에 포함된다. 테스트 수는 내용이나 역사적 사실의 개수가 아니다.

다음 항목은 **실제 앱에서 확인하지 않았다**.

1. 최신 앱의 자료 로딩 방식과 기존 개요 ID에 대한 연결표
2. 컴포넌트에 목록·상세·출처·경로를 배치한 결과
3. 검색 후 상세 진입·뒤로 가기·없는 ID 처리
4. 키보드 탐색·스크린리더·모바일 화면과 실사용 성능
5. 공개를 위한 별도 승인 자료와 실제 배포 결과

실앱 검토 시에는 이 모듈을 사용하는 별도 검토 화면에서 연결을 먼저 확인한다. 이 모듈의 테스트 통과를 실제 앱 E2E·모바일 검수·공개 완료로 보고하지 않는다.
