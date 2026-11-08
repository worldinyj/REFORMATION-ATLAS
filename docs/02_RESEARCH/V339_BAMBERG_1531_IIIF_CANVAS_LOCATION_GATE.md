# V3.39 — 1531년 바믐베르크 소장본 IIIF 판면 탐색 및 교감 게이트

- 상태: **RESEARCH_DRAFT_HOLD**; publication=false; webapp_integrated=false.
- 부모: V3.38 (1530 제출 사건/1531 판본/개별 소장본/19세기 비평판 분리).
- 작성일: 2026-11-09.
- 대상: Bamberg Staatsbibliothek `.64 B 9#3a`, VD16 C 4734, `bsb11411960`. **뮌헨 BSB의 별도 소장본 `4 H.ref. 205 b`와 혼동 금지**.

## 확인된 공개 기관 근거

- BSB/MDZ [공식 디지털 목록](https://www.digitale-sammlungen.de/en/details/bsb11411960)은 `Confessio Fidei ...` (Wittenberg, Georg Rhau, 1531, 라틴어), Bamberg 소장번호 `.64 B 9#3a`, VD16 C 4734 및 **288 scans**를 표시한다. 목록의 스캔 숫자는 **각 조항의 실제 이미지 판독 완료 건수**가 아니다.
- BSB/MDZ의 [공식 IIIF 인터페이스 설명](https://www.digitale-sammlungen.de/en/interfaces)은 `https://api.digitale-sammlungen.de/iiif/presentation/v2/{object_id}/manifest`를 제공하며, `.sequences[0].canvases`에서 **각 페이지의 label, canvas, image 서비스**를 조회할 수 있다고 명시한다.
- 정확한 대상 endpoint: `https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11411960/manifest`.
- 기관 목록의 권리 표시: `No Copyright - Non-Commercial Use Only`. **이미지를 공개 GitHub 저장소에 복제·재배포하지 말고 소장기관 링크만 사용**.

## 현재 탐색 상태

- 채팅 환경에서 MDZ 원격 manifest를 직접 열어 읽는 동작은 제한되어, **각 Canvas의 label/서비스 URL을 그 자리에서 확정할 수 없었다**.
- 재현 가능한 Node 22 리드온리 탐색 스크립트 `scripts/inspect_v339_bamberg_iiif.mjs`를 추가했다. 이 스크립트는 PDF 전체나 288면 이미지 자체를 내려받지 않고 **기관 manifest의 페이지 메타데이터**만 가져온다.
- GitHub Actions `.github/workflows/atlas-v339-bamberg-iiif-probe.yml`는 연구 브랜치에서 요청된 manifest를 조회하고 **review-only JSON**을 단기 아티팩트로 저장하도록 했다. 실제 Actions 성공 여부와 canvas 개수 일치는 **실행 결과를 조회한 뒤에만 인증 가능**.
- 1531 원판의 제4·7·8조 실물 이미지 직접 판독: **0쪽**.
- 1858년 CR XXVI 제26권의 제4·7·8조 초판 계열 본문 263–336쪽 직접 판독: **0쪽**.
- 기존 1540 Variata 1858년 비평판 발췌 351–356쪽은 V3.37.1의 한정된 판독 실적으로 유지. 대상 자료를 바꿔치기하지 않는다.

## 다음 교감 절차

1. 자동검증 로그에서 `canvas_count`가 기관 목록의 288과 일치하는지 검증한다. 일치하지 않으면 객체 식별자/manifest 구성부터 재확인하고 이미지 페이지를 추정하지 않는다.
2. Canvas label, 1-based ordinal, 0-based index와 이미지 서비스 URL을 기록한다. `page=N`과 인쇄면/책장 번호가 같다고 가정하지 않는다.
3. 먼저 표제면과 Confessio 본문 시작 지점을 **실물 이미지**로 검토한 다음 제4조 `De iustificatione`, 제7조 `De ecclesia`, 제8조 `Quid sit ecclesia`의 실제 이미지 위치를 지정한다.
4. 각 표기를 `1531_exemplar_reading`, `1858_CR26_edition_reading`, `BA_web_transcription`, `Schaff_edited_reading`으로 독립 등록한다. 1531 다른 소장본을 비교하기 전 인쇄 중 교정 상태라고 확정하지 않는다.
5. 네 전사 의심 표기 W01–W04는 모두 `UNRESOLVED` 유지. 원전 판독 없이 유추한 값은 NULL.
6. 독자용 중 수준 해설은 자료의 층위를 설명하는 초안까지만 작성. `main`, 기존 513편 본문, Google AI Studio 앱, 배포물의 자동 치환 금지.

## 판독 테이블 (미확정 템플릿)

| ID | 조항 | 웹상 충돌 표기 | 1531 Bamberg 실물 읽기 | CR XXVI 1858 초판 계열 읽기 | 판정 |
|---|---|---|---|---|---|
| W01 | IV | iustificenter / justificentur | 미열람 | 미열람 | OPEN |
| W02 | VII | consentiere / consentire | 미열람 | 미열람 | OPEN |
| W03 | VIII | malii / mali | 미열람 | 미열람 | OPEN |
| W04 | VIII | sentibant / sentiebant | 미열람 | 미열람 | OPEN |

**승격 금지:** 공식 IIIF endpoint를 찾은 것 자체는 특정 라틴어 철자를 시각 판독했음을 의미하지 않는다. 검토되지 않은 페이지 링크를 '원본 대조 완료'로 표시하면 안 된다.


## 2026-11-09 실제 GitHub Actions 조회 결과 (추가 확인)

**실제 실행 확인:** GitHub Actions run `42531249348` / job `128885709649` / result `success`. 다른 기존 VOL03 Draft Consistency QA도 동시 성공. 다음 항목은 로컬 추측이 아니라 **원격 실행 로그의 실측 값**이다.

- `MANIFEST_HTTP 200`
- `object=bsb11411960`, `canvas_count=288`
- `manifest_label=Confessio Fidei exhibita invictiss. Imp. Carolo V. Caesari Aug. in Comiciis Augustae, Anno MDXXX`
- `canvas_ordinal_1_based=1` → `canvas_index_0_based=0` → `label=(0001)` → `image_service_id=https://api.digitale-sammlungen.de/iiif/image/v2/bsb11411960_00001`.
- `canvas_ordinal_1_based=50` → `canvas_index_0_based=49` → `label=(0050)` → `image_service_id=https://api.digitale-sammlungen.de/iiif/image/v2/bsb11411960_00050`.
- `canvas_ordinal_1_based=288` → `canvas_index_0_based=287` → `label=(0288)` → `image_service_id=https://api.digitale-sammlungen.de/iiif/image/v2/bsb11411960_00288`.
- 소장기관의 디지털 목록 288 scans와 실물 이미지 Canvas 메타데이터 수 288이 **정확하게 일치**한다. 대표 샘플 21개 Canvas에서 ID와 이미지 서비스 경로가 식별된다.
- **중요:** 각 서비스 URL의 **실제 이미지 바이트/문자를 이번 회차에서는 열어 판독하지 않았다**. 따라서 CA IV/VII/VIII 실제 페이지 위치는 미확정이며 W01–W04는 모두 OPEN 상태이다.

실행 검토 후 스크립트에 **288개 수 불일치/기관 객체 ID 불일치/0-based 번호 불일치 시 실패 처리**를 추가했다. 따라서 향후 자동검증에서 링크 교체·권차 혼동을 조기 검출할 수 있다.

### 다음 작업 게이트

1. Canvas 1–288 사이에서 **실제 표제·목차·조항 머리말을 이미지로 확인**하고 제4·7·8조 좌표를 확정.
2. 해당 면에서 글자 이미지를 판독하여 `W01–W04`와 연결하고, 똑같이 1858 CR XXVI 263–336쪽 1531 계열 본문을 확인.
3. 독립 소장본의 인쇄 상태 차이를 주장하려면 두 개별 실물을 별도로 대조한다.
4. **공개 보류:** 독자 원문 자동수정, 대량 이미지 재배포, main 변경, 웹앱 배포 금지.
