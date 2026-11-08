# V3.39.2 — 두 바믐베르크 디지털 객체의 혼동 해소: 1530 신앙고백과 1531 변증서

**Research Draft / Publication HOLD · 작성일 2026-11-09**

## 1. 연구의 실질적 발견

기존 V3.39는 Bamberg `.64 B 9#3a` 소장본 (`bsb11411960`)의 IIIF 288개 Canvas 목록을 확보했지만, 이를 바탕으로 아우크스부르크 신앙고백 제4·7·8조를 특정하기에는 중요한 전제 검증이 빠져 있었다. 실제 기관 OCR 1면에는 `APOLOGIA CONFESSIONIS EMENDA`(변증서 정오), 제20면에는 `meritum congrui`, `meritum condigni` 등 변증서 제4조의 긴 칭의론에 부합하는 논의가 등장한다. 이는 해당 두 면을 **신앙고백 제4조의 원문**으로 사용하는 것이 위험하다는 직접적인 단서다. 해당 288면이 **전체적으로 변증서만 포함한다는 주장은 아직 입증되지 않았다.**

인접 객체 `bsb11411959`도 공식 IIIF manifest를 직접 조회했다. 이것은 `bsb11411960`과 같은 1531년 라우 인쇄본이 아니라, 기관 서지에서 **약 1530년 라틴어 신앙고백 별도 인쇄본**으로 분류한다. 40개 Canvas, VD16 C 4708, Bamberg 서가번호 `.64 B 9#3`이다. 기관은 발행지를 **[취리히]**, 인쇄자를 **[크리스토프 프로샤우어]**로 추정하나, 별도 견해로 **[비텐베르크: 라우, 1530]**도 함께 소개한다. 이견을 제거한 확정적 출판 정보로 표현하지 않는다.

**연구적으로 유의미한 점:** 서로 인접한 `bsb11411959`(c.1530 신앙고백)와 `bsb11411960`(1531 라우의 신앙고백/변증서 서지, 실제 표본 OCR은 변증서)의 관계를 '1531년 신앙고백의 두 디지털 조각'으로 가정하면 오류가 된다. **작품·판본·개별 소장본·문헌 단위를 먼저 식별해야만** 제4·7·8조의 철자를 비교할 수 있다.

## 2. 기관 원전과 재현 가능한 검증 로그

| 증거 | 식별자 | 기관 메타데이터 | 검증 상태 |
| --- | --- | --- | --- |
| 이른 라틴어 신앙고백 | `bsb11411959` | `Confessio Exhibita Caesari`; c.1530; VD16 C 4708; Bamberg `.64 B 9#3`; 40 scans | 공식 기관 IIIF HTTP 200, Canvas 40개, 각 Canvas에 OCR 링크 40개; 실제 인쇄 글자 미판독 |
| 1531 라우 계열 | `bsb11411960` | `Confessio Fidei ... Addita Apologia`; 1531; VD16 C 4734; Bamberg `.64 B 9#3a`; 288 scans | 공식 기관 IIIF HTTP 200, Canvas 288개; OCR Canvas 1·20의 **주제 확인만**; 원 인쇄 글자 미판독 |
| 1531 또 다른 인쇄본 후보 | BSB `4 H ref 206` | 『울름 1549년 도서목록 연구』의 1531 Rhau, VD16 C 4735 소장본 서지 | 현대 연구물 서지만 확인; 디지털 객체 ID 및 본문 인쇄면은 미확인 |

기록 근거:
- `https://www.digitale-sammlungen.de/en/details/bsb11411959`
- `https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11411959/manifest`
- `https://www.digitale-sammlungen.de/en/details/bsb11411960`
- `https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11411960/manifest`
- `https://stadtbibliothek.ulm.de/-/media/bibliothek/downloads/volltexte/der-erste-katalog-der-stadtbibliothek-ulm-von-1549.pdf` (BSB 4 H ref 206/VD16 C 4735 언급)

GitHub Actions 실증:
- `bsb11411960` manifest 조회 성공: 288개 Canvas, `bsb11411960_00001`–`_00288`
- 기관 제공 기존 OCR **Canvas 20**: `meritum congrui / meritum condigni` 등 확인. URL `https://api.digitale-sammlungen.de/ocr/bsb11411960/20`
- 기관 제공 기존 OCR **Canvas 1**: `APOLOGIA CONFESSIONIS EMENDA` 확인. URL `https://api.digitale-sammlungen.de/ocr/bsb11411960/1`
- `bsb11411959` manifest 조회 성공: 40 Canvas, 인쇄/연도/VD16/서가번호의 서지 이견도 원본 메타데이터에서 직접 확인. 초기 run `42532567817` (job `128889778874`).
- **이 모든 증거는 기관 메타데이터 또는 기관이 이전에 만들어 둔 OCR**이다. 이 회차의 육안 인쇄면 직접 판독은 **0쪽**.

## 3. 문헌학적 제한: 1530 인쇄본과 1530 제출본을 혼동하지 않기

1530년대 신앙고백의 역사는 단순한 '1530 원본 → 1531 초판 → 1540 개정'의 일직선 복사가 아니다. 1530년에 인쇄된 신앙고백이라 하더라도 황제에게 제출한 필사본과 같은 서술이라고 보장할 수 없다. 또한 1531년 저자 관여본이 포함하는 `Apologia`(가톨릭 반박문에 대한 개신교 측 변증)와 `Confessio`(신앙고백) 사이의 '제4조'도 문헌을 구분해야 한다.

따라서 V3.39은 모든 표기를 다음 필드와 연결해야 한다.
`work_id` / `printing_year_as_catalogued` / `printer_attribution_status` / `vd16` / `holding` / `shelfmark` / `bsb_object_id` / `canvas_id` / `physical_reading` / `evidence_level`.

## 4. 독자를 위한 해설 초안 — 중(中) 수준

### 제목이 비슷해도 서로 다른 책일 수 있습니다

1530년 아우크스부르크 제국회의에서 발표된 신앙고백은 곧 여러 경로로 필사되고 인쇄되었습니다. 그런데 인쇄된 책 가운데는 저자가 본문을 정리해 출판한 판본도 있고, 그보다 이른 시기에 별도로 인쇄된 판본도 있습니다. 따라서 출판 연도나 제목이 비슷하다는 이유로 같은 책이라고 볼 수 없습니다.

1531년에는 신앙고백과 함께 이에 대한 **변증서**가 출판되었습니다. 신앙고백 제4조는 사람이 어떻게 의롭다 하심을 얻는지를 간결하게 설명하는 반면, 변증서 제4조는 그 논증을 더 상세히 펼칩니다. 둘은 연결되는 문서지만 같은 본문은 아닙니다. 후대 학자들이 편찬한 비평판이나 현대 도서관의 OCR을 사용할 때도 이 문헌의 차이를 먼저 확인해야 합니다.

## 5. 미완료 조건 및 다음 단위

1. `bsb11411959`의 **40개 원 이미지** 중 실제 신앙고백 제4·7·8조 머리말과 본문 위치를 시각 확인. 해당 객체는 **c.1530 비저자 관여 인쇄 가능성이 있는 계열**이므로 1531 최초 공인 인쇄의 대체 증거로 취급하지 않는다.
2. `bsb11411960` 전체 페이지별 **작품 구획**을 확인해 1531 라틴어 신앙고백 본문이 288개 Canvas 안에 포함되는지 검증. OCR 샘플 1·20만으로 전체 결론 확정 금지.
3. 진정한 **1531 Rhau 라틴어 신앙고백** 소장본의 정확한 디지털 객체를 확보(추가 후보: BSB 4 H ref 206 / VD16 C 4735).
4. 1858 CR XXVI 263–336쪽 인쇄면에서 같은 문장의 실물 글자를 직접 확인.
5. 기존 W01–W04 (`iustificenter`, `consentiere`, `malii`, `sentibant`) 4건은 모두 미확정 유지. OCR나 추정 판본으로 자동 교정하지 않는다.

**출판/병합 보류:** 기존 513편 원고·main·AI Studio 웹앱 변경 없음. 외부 이미지 복제, 저작권 있는 현대 문헌 전문 공개 없음. 이 보고서의 구조화 데이터는 `data/contracts/atlas_v339_confessio_apologia_object_disambiguation.json`.
