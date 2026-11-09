# 종교개혁 ATLAS V3.47.1 — 1540년 Variata 제7·8조 복수 소장본 교감과 인쇄 상태 판정 한계

**작성:** 2026-11-09 · **상태:** `RESEARCH_DRAFT_HOLD` · **선행:** V3.46.1  
**이번 작업:** 제10조 이외의 독립 인쇄면에서 실제 판본 간 동일성의 국지적 검증. **제7조 전체 + 제8조 앞부분을 Regensburg와 Bamberg 2개 개별 소장본의 원 인쇄 이미지에서 직접 판독했다.** 다음 페이지에 계속되는 제8조 끝은 선행 V3.46.1 원본(각각 Canvas 17/21)을 근거로 이어 읽는다. 원고 513편, 1,539절, 723 출처, `main`, Google AI Studio 웹앱, 공개 배포 변경 없음.

## 1. 1540 원본 두 권 — 실제 판독 좌표와 물리적 특징

| 증거 ID | 기관 / 청구기호 | 디지털 객체 | 새 판독 Canvas | 수신 JPEG 해시 (SHA-256) |
|---|---|---|---:|---|
| V347-R-16 | Staatliche Bibliothek Regensburg, `999/4Theol.syst.33` | `bsb11069754` | **16** | `bc2f17e744abbe34e4b3ab4c963ce3f71f317005678e9e909bc4f5db7a34da9d` |
| V347-B-20 | Staatsbibliothek Bamberg, `.10 D 14` | `bsb11399533` | **20** | `19363b775afba5471638f3394659cf11983c20266e83012ea4ee095cf52025d1` |

- **R 이미지:** https://api.digitale-sammlungen.de/iiif/image/v2/bsb11069754_00016/full/1800,/0/default.jpg · HTTP 200 · 원 수신 1800×2726 JPEG / 611,789 bytes.
- **B 이미지:** https://api.digitale-sammlungen.de/iiif/image/v2/bsb11399533_00020/full/1800,/0/default.jpg · HTTP 200 · 원 수신 1800×2385 JPEG / 589,609 bytes.
- **출처·판본:** 둘 다 Wittenberg: Georg Rhau, 1540, 라틴어 `Confessio Augustana Variata`, **VD16 C4713**. 원 BSB/MDZ Manifest는 V3.46.1에 기록. 서로 다른 디지털 이미지와 청구기호는 **서로 다른 물리적 소장본**을 뜻하지만 **서로 다른 역사 판본**이라는 뜻은 아니다.
- **직접 시각 검토 증거:** GitHub Actions run `42556126783`, job `128962110742`, 본문 이미지 2매를 실제 그림으로 확인. 도서관이 제공한 OCR은 위치 찾기에만 사용했고, 이 판정에서 글자의 최종 근거는 인쇄 이미지다.
- **제8조 계속의 기존 직접 판독:** R Canvas **17** / B Canvas **21**, V3.46.1 run `42548638567`, job `128939028846`. 앞 페이지 아래의 `licere`가 다음 페이지 위쪽의 `populo`로 이어지는 행간 연속성 확인.

## 2. 제7조 — 인쇄본 두 권의 직접 교감 결과

두 원본의 `VII.`와 본문 전체, 그 아래 `VIII.` 표제를 같은 사진에서 판독한다. **다음은 비교 좌표(짧은 원문 표식)이며 원문 전체 재게시가 아니다.**

| 비교 구절 | Regensburg Canvas 16 | Bamberg Canvas 20 | 판정 |
|---|---|---|---|
| 교회 정의 | `congregatio membrorum Christi` | 동일 | 두 이미지 일치 |
| 신자와 현실의 혼재 | `multi mali & hypocritæ admixti sunt` | 동일 | 두 이미지 일치 |
| 말씀·성례의 표지 | `puram & sanam Evangelii doctrinam` / `rectum usum Sacramentorum` | 동일 | 두 이미지 일치 |
| 일치의 조건 | `satis est consentire de doctrina Evangelii, & administratione Sacramentorum` | 동일 | 두 이미지 일치 |
| 획일적 관습의 부정 | `Nec necesse est ubique similes esse traditiones humanas` | 동일 | 두 이미지 일치 |
| 끝부분 | `Unus Dominus, una fides, unum Baptisma` | 동일 | 두 이미지 일치 |

**조판 비교:** `con-/gregatio`, `Evan-/gelii`, `do-/ctrina`, `Bap-/tisma` 등 선택한 행말 분할 지점이 대응 판면에서 일치한다. 두 소장본의 이 **검토 구역**에서 확인되는 서술·행 바꿈의 대응은 동일한 조판 계열이라는 판단과 부합한다. **이것만으로 인쇄 중 교정의 전면 부재, 동일 인쇄 시기, 모든 낱말의 육안 교감, 개별 책의 생산순서는 확정할 수 없다.**

## 3. 제8조 — 조항 시작과 다음 면으로 이어지는 읽기

- R Canvas 16 / B Canvas 20의 `VIII.` 아래 같은 서두: `Cum autem in hac vita admixti sint Ecclesiae multi mali & hypocritae` — 교회 안에 악인과 위선자가 섞인 현실을 먼저 제기한다.
- `Sacramenta & verbum Dei propter ordinationem & mandatum Christi sunt efficacia` 및 `etiam si per malos exhibeantur` 문구가 두 인쇄면에서 함께 확인된다.
- 판면의 아래쪽 `Damnant Donatistas & similes, qui negabant` 이후 단어 `licere`와, 다음 Canvas(R17/B21)에서 이어지는 `populo uti ministerio malorum...`의 연결 관계는 V3.46.1 이미지와 부합한다.
- **판정:** 확인한 제8조 서두 및 행 연결에서 구체적인 1540 두 권의 이문은 식별하지 못했다. 전체 1540년 인쇄본의 모든 지점에 이문이 없다는 뜻은 아니다.
- **1531↔1540의 역사적 변경과 분리:** V3.37/V3.41/V3.43에서 1531 계열과 1540 Variata 간 제7·8조의 논리 배열·확장이라는 **판본 간 개정**을 별도로 조사했다. 이번에는 **1540년 같은 판본을 가진 개별 두 책 간의 인쇄 상태·필기 흔적**을 조사한다.

## 4. Bamberg 책에서 직접 본 필기: 텍스트 변이로 계수하지 않는다

Bamberg Canvas 20에는 Regensburg 대응 페이지에 없는 연필/잉크로 보이는 **손글씨 주제 표기 및 여백 참조**가 관찰된다.

- `VII.` 오른쪽에 교회/일치에 관한 라틴어 주제 표기.
- `VIII.` 오른쪽에 악한 집례자에 관한 주제 표기.
- 본문 왼쪽 여백에 성경 위치를 뜻하는 것으로 보이는 참조(예: `Gal.`, `Ephes.`, `Matt.` 계열).
- 세로 가장자리와 제7조 시작 인근 종이에 진한 얼룩·마모가 있다. 잉크/착색층의 정확한 재료·상태를 영상만으로 판별하지 않는다.

**이 관찰이 허용하는 결론:** 서로 다른 소장본의 **후대 혹은 출판 후에 더해진 것으로 보이는 손글씨 흔적**을 인쇄 본문과 분리할 수 있다. 단, 필기자·작성 연대·정확한 필기 내용·책의 소장 이력은 별도 물증이 없으면 **확정하지 않는다**. 손글씨는 `PRINT_VARIANT`가 아닌 `COPY_SPECIFIC_MANUSCRIPT_ANNOTATION`으로 기록한다.

## 5. Press-state(인쇄 중 교정) 판정 매트릭스

| 질문 | 이번까지의 증거 | 상태 |
|---|---|---|
| 같은 1540 Rhau/VD16 C4713의 별도 물리적 책인가? | 소장처·청구기호·IIIF 원본 2종 | **확인** |
| 제7조 전체의 핵심 인쇄 문자열이 같은가? | 두 Canvas 판독 6개 지점 | **일치 확인** |
| 제8조 시작 부분과 행 경계가 같은가? | 두 Canvas 및 선행 연속면 | **일치 확인** |
| 대응 행말/인쇄 배치가 같은가? | 관찰한 특정 분할과 표제 배치 | **일치 확인(표본 한정)** |
| 손글씨와 인쇄문자가 다른 층위인가? | Bamberg의 필기 및 Regensburg의 부재 | **구분 확인** |
| 전체 1540판에 press correction이 없나? | 모든 판면·타 소장본·쇄 교정 서명 미대조 | **미확정** |
| Bamberg 필기자와 연대를 특정했나? | 소장내역/필기분석 미실시 | **미확정** |

## 6. 웹앱용 중(中) 수준 해설 초안 (출판 미승인)

### 500년 전 인쇄된 같은 신앙고백, 왜 어떤 책에는 글씨가 더 있을까요?

1540년에 찍힌 아우크스부르크 신앙고백 두 권을 비교하면, 같은 문장이 같은 위치와 줄바꿈으로 인쇄된 부분을 발견할 수 있습니다. 제7조는 교회의 일치를 모든 지역의 관습을 똑같이 만드는 것과 구별하고, 복음의 가르침과 성례의 집례를 강조합니다. 제8조는 교회에 악한 사람이 섞여 있을 수 있더라도 말씀과 성례의 효력이 집례자의 도덕성만으로 결정되지 않는다고 설명합니다.

그런데 밤베르크에 보존된 책의 여백에는 누군가가 쓴 것으로 보이는 메모가 남아 있습니다. 이러한 메모는 1540년 인쇄소에서 활자로 찍은 원문과 다릅니다. 역사를 연구할 때는 **저자가 고친 문장, 인쇄소에서 조판한 글자, 후대 독자가 남긴 필기**를 따로 살펴야 합니다.

이번에 비교한 부분의 인쇄 글자는 서로 일치했지만, 그것으로 모든 1540년판이 한 글자까지 같다고 결론내리는 것은 아닙니다. 원전의 작은 차이를 검증하는 일은 종교개혁자들이 남긴 문서를 정확하게 이해하려는 과정입니다.

## 7. 보존 및 후속 게이트

- [x] **1540 두 개별 원 인쇄본 제7·8조 연속 구역 실제 이미지 직접 판독**.
- [x] 핵심 비교 읽기, 행바꿈, 표제 배치, 주변 성경 주석 흔적 분리.
- [x] V3.46.1의 제10조 1540년판 3개 개별 소장본 교감은 별도 검증 범위로 유지.
- [ ] 별도 인쇄본 3권 이상에서 인쇄된 다른 구역(제4/5조, 표제면, 정오표/인쇄사 표식) 비교로 press-state 탐색 확대.
- [ ] Bamberg 필기자를 특정할 근거와 소장 이력 문헌을 확보하면 별도 기록.
- [ ] 학술 편집자 인간 검수 및 출판 승인 전 기존 코퍼스 수정·웹앱 이관·main 병합 **금지**.
- [ ] 인쇄본 공개 URL만 인용하고 원본 이미지 전체 파일을 저장소에 재게시하지 않음.

**최종 판정:** `EXEMPLAR_SELECTED_TEXT_MATCH_NO_PRINT_VARIANT_IDENTIFIED`, `HANDWRITTEN_NOT_PRINT`, `PRESS_STATE_GLOBAL_UNDETERMINED`, `PUBLICATION_HOLD`.
