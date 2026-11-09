# 종교개혁 ATLAS V3.46.1 — 1540년 Variata 성찬 제10조: 독립 소장본 두 권의 인쇄면 직접 교감

**기록일:** 2026-11-09 · **상태:** `RESEARCH_DRAFT_HOLD` · **선행:** V3.45 / V3.44.1  
**이번 회차 결론:** 레겐스부르크와 밤베르크에 별도로 보존된 **1540년 비텐베르크 Georg Rhau판(VD16 C4713)**의 성찬 제10조를 원 인쇄 이미지로 직접 판독했다. 두 판독은 일치하며, 앞서 검수한 시카고 Gruber 28의 제10조 사진과도 일치한다. 원본 그림은 저장소에 복제하지 않고 **기관 링크·인쇄면·사진 식별·SHA-256·검토 로그**만 보존한다.

## 1. 자료 식별 — 판본과 물리적 소장본을 분리

| 소장처 | 청구기호 | BSB/MDZ 디지털 ID | Canvas | 판독한 원 책 인쇄면 | 이미지 |
|---|---|---|---:|---:|---|
| Regensburg, Staatliche Bibliothek | `999/4Theol.syst.33` | `bsb11069754` | **17** | **9쪽** | https://api.digitale-sammlungen.de/iiif/image/v2/bsb11069754_00017/full/1800,/0/default.jpg |
| Bamberg, Staatsbibliothek | `.10 D 14` | `bsb11399533` | **21** | **9쪽** | https://api.digitale-sammlungen.de/iiif/image/v2/bsb11399533_00021/full/1800,/0/default.jpg |
| Lutheran School of Theology at Chicago, Gruber Collection | `Gruber 28` | 기관 사진 | 제10조 크롭 | 쪽번호 불명 | https://gruber.lstc.edu/confessions/images/gruber28var.jpg |

공식 IIIF Manifest는 두 BSB 객체에서 HTTP 200 확인:
- Regensburg (396 Canvas): https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11069754/manifest
- Bamberg (372 Canvas): https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11399533/manifest

두 BSB 자료의 기관 메타데이터에 **1540**, **Vitebergae: Rhau**, **라틴어**, **44+137장**, **VD16 C4713**이 확인된다. SLUB 카탈로그는 두 URL을 **서로 다른 소장처·청구기호**로 연결했다. 공통 BSB 서지 식별자 `991096256859707356`은 공유 서지이지 동일 물리적 책이라는 뜻이 아니다. 독립 소장본을 서로 다른 **판본**으로 계산하지 않는다.

직접 원전 위치 찾기 과정: SLUB 공개 링크 → 기관 IIIF Manifest → 기관 기성 OCR에서 제10조가 실린 Canvas를 탐색(**기계 OCR은 위치 확인 전용**) → **실제 판면 JPEG 두 장을 불러와 글자를 직접 시각 판독**. 도서관 OCR만으로 본문 확정을 하지 않았다.

## 2. 실제 이미지 판독 및 파일 검증 장부

| 증거 ID | 페이지 헤더 | 이미지 원 크기 | JPEG 원 바이트 | SHA-256 |
|---|---|---|---:|---|
| `V346-R-17` | `PRAECIPVI. 9.` | 1800×2783 | 576,483 | `efdeee37020baa9e456069c142777002e6d7cc45c6362834123a4fb27a622b18` |
| `V346-B-21` | `PRAECIPVI. 9.` | 1800×2452 | 597,147 | `684f7a2ff38f482303b3cfe933bf84dac99059ef3e3a3b1e5877985562585460` |

**증거 실행:** GitHub Actions `42548638567`, `historical print` job `128939028846` (이미지 각 1회 직접 HTTP 200 획득 및 시각 판독용 일시 표시). 해시값은 **API에서 수신한 원 JPEG 바이트** 기준이다. 전송 중 화면 확인용으로 축소·재인코딩한 판독 이미지의 해시와 혼동하지 않는다.

두 실제 원본 모두 제9조 세례 문단 아래에서 **로마 숫자 `X.`**, 제10조 전체, 이어지는 **`XI.`**를 한 화면으로 보여 준다. 앞뒤 조항까지 확인한 것이 OCR에서 비슷한 표현이 나오는 다른 페이지를 오인하지 않았다는 근거이다.

### 제10조 라틴어 원문 읽기

두 인쇄본 모두 눈으로 확인한 표기는 현대 라틴 문자로 정규화하면 다음과 같다.

> De Coena Domini docent, quod cum pane et vino vere exhibeantur corpus et sanguis Christi, vescentibus in Coena Domini.

인쇄판에는 줄바꿈 `ves- / centibus`, 긴 `ſ`, `&`, `œ` 등의 16세기 조판 형태가 있고, 정규화 시 의미에 영향을 주지 않는 그래픽 차이를 별도로 처리했다.

**직접 교감 결과:** Regensburg·Bamberg의 제10조 인쇄된 문장과 어순이 일치한다. 특히 두 책 모두:
1. `cum pane & vino`를 포함한다.
2. `vere exhibeantur corpus & sanguis Christi`를 포함한다.
3. 제10조 끝에 `improbant secus docentes`가 **없고**, 바로 XI조가 시작한다.

이는 V3.44.1에서 직접 판독한 시카고 **Gruber 28**의 크롭 사진(421×113)의 내용과도 일치한다. 따라서 **1540년판 제10조에 대해 직접 본 개별 소장본 3권의 정규화 인쇄문구가 일치**한다고 말할 수 있다. 다만 전수 판본·인쇄 상태 교감 완료나 모든 소장본의 동일성까지 입증한 것은 아니다.

### 밤베르크 소장본에서 새로 구분해야 할 사항

Bamberg Canvas 21에는 IX·X·XI 조항 번호 옆 **손글씨 주제 표기**와 파손·변색이 보인다. 이것은 한 권의 소장·사용 이력과 관련된 **필사적 흔적/물리적 상태**로 분류한다. Regensburg의 같은 쪽 인쇄 본문과 달라진 **조판 본문 이문**으로 잘못 집계하지 않는다. 주석의 필기자·작성연대는 아직 확인되지 않았다.

## 3. 1531과 1540 사이의 역사적 개정은 별도 비교

**1531 원 인쇄 직접 증거:** Bayerische Staatsbibliothek München, `4 H.ref. 205 b`, `bsb00103368` **Canvas 17**, Wittenberg Rhau 1531. V3.44.1의 실제 이미지에서 제10조 `vere adsint, et distribuantur`와 `improbant secus docentes`를 읽었다.  
**1540 인쇄 직접 증거:** Regensburg Canvas 17 / Bamberg Canvas 21 / Chicago Gruber 28의 제10조에서 `cum pane et vino vere exhibeantur` 및 배격 문구 생략을 읽었다.  
**1858 비평판:** *Corpus Reformatorum* XXVI **인쇄 357쪽 각주 34**의 1531/1540 교감 기록과 양쪽 당대 판독이 부합한다. 이것은 후대 편집자의 참고 증언이며 16세기 두 당대 판독과 별도 자료 층위다.

**판정:** (a) 1531→1540 제10조 표현 변경 = 역사적 판본 개정, (b) V3.42.1의 BA 웹 표기 불일치 W01~W04 = 현대 전사 불일치. 두 문제를 서로 교체하지 않는다.

신학적 의도를 단일한 원인으로 단정하지 않는다. 1534년 카셀 협의·1536년 비텐베르크 일치·1540년 대화 정치의 연결은 V3.45의 학술 연구 자료와 별도 해석 등급으로만 설명한다.

## 4. V3.46의 실패·우회하지 않은 접근 경로

- **Google Books Augsburg `HmpoAAAAcAAJ`**, `Th S 276`: 메타데이터 및 초기 작은 인쇄 이미지가 HTTP200, 그러나 그 샘플은 제10조가 아니라 서문. `PA30`/`PA40`/`PA50`/`PA60`의 고배율 HTTP200은 전부 동일한 “image not available” 플레이스홀더(9,103바이트); 원문 읽기로 계산하지 않음. 전자책 텍스트 링크 HTTP403.
- **Halle ULB `Pon Vg 3008 a (2)`**, URN `urn:nbn:de:gbv:3:1-143262`: 현대 저장소 주소로 이동하지만 anti-bot 접근 제한을 관찰; 우회하지 않았고 제10조 미판독.
- **Pitts Theology Library `1540 CONF`**: 1540판 서지·표제 증거. 제10조 원본 인쇄면 미판독.
- **Paderborn `VD16 C4714`**: 1542년판. 다른 판본이므로 제2의 1540년 소장본으로 집계하지 않는다.

이번 성공은 제10조의 **다른 공식 기관 소장 디지털 원본 2개를 확보한 것**으로 이 자료 접근의 어려움을 실질적으로 해결했지만, Google Books/Halle 접근 실패 기록은 동일하게 남긴다.

## 5. 정량 성과·제약·후속 과제

| 판정 대상 | 수치·단계 |
|---|---|
| 이번 회차 새로운 1540 실물 소장본 제10조 직접 이미지 판독 | **2/2** (Regensburg, Bamberg) |
| 앞선 V3.44에서 직접 읽은 1540 Gruber 28 | **1** |
| 실제 본문 비교에 사용할 수 있는 서로 다른 1540년 소장본의 제10조 | **3** |
| 1540 제10조 인쇄 내용의 이번 두 신증거간 본문 불일치 | **0** |
| 이전 1531 Rhau 제10조 직접 판독 | **1** (Munich BSB 단일 소장본) |
| 모든 1540 원본·전체 조항에 대한 전수 교감 | **미실시** |
| 513편 통합 원고, 1,539절, 723개 출처 변경 | **0** |
| `main`/Google AI Studio/출판 상태 | **변경 없음 / HOLD** |

후속 과제는 (i) 1540년 세 사본의 다른 조항이나 표제·종이·인쇄상태를 비교해 **press-state** 여부 탐색, (ii) 밤베르크 필기 주석의 독립 연대·소장 이력 검토, (iii) 1536년 비텐베르크 일치 당대 원문과 학술 연구의 구분 강화, (iv) 문헌·신학 검토위원 승인 후 앱 이관 심사다.

**Publication HOLD / Draft PR 유지.** 제10조의 직접 이미지 판독은 완료됐으나 기존 코퍼스나 웹앱의 자동 교정·출판을 승인한 것은 아니다.
