# ATLAS V3.46 — 1540 Variata 복수 소장본 2차 원전 접근·판본 식별 장부

**날짜:** 2026-11-09 · **연구 단계:** RESEARCH_DRAFT_HOLD · **부모:** V3.45 / V3.44.1  
**금지:** 513편 코퍼스 원고 수정, main/Google AI Studio 반영, 출판, PDF/고해상도 원본 재배포.

## 1. 진전: 1540 Rhau 동일 서지 계열의 두 별도 소장본에 연결되는 공식 이미지 객체 확보

드레스덴 SLUB 카탈로그의 공개 디지털본 접속 링크를 확인하여 두 개의 정확한 MDZ 디지털 ID를 얻었다. 이는 단순 제목 검색이 아니라 **기관의 소장 표기와 연결된 디지털 객체 URL**이다.

| 소장처 | 청구기호 | BSB/MDZ 객체 | 기관 IIIF | 검증 |
|---|---|---|---|---|
| Regensburg, Staatliche Bibliothek | `999/4Theol.syst.33` | `bsb11069754` | https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11069754/manifest | HTTP 200, **396 Canvas**, Rhau Wittenberg **1540**, **VD16 C4713** |
| Bamberg, Staatsbibliothek | `.10 D 14` | `bsb11399533` | https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11399533/manifest | HTTP 200, **372 Canvas**, Rhau Wittenberg **1540**, **VD16 C4713** |

목록: https://katalog.slub-dresden.de/?tx_find_find%5Bq%5D%5Btopic%5D%5B0%5D=%22Confessio+Augustana%22+%22Theologie%22+  
동일한 역사 판본의 **별도 인쇄 소장본**으로 구조화한다. 서로 다른 디지털 객체가 **별도의 저작·판본**을 증명하는 것은 아니며, 표지·내지·인쇄 시 교정 상태의 동일성도 아직 검증하지 않았다. 공통 BSB 서지 ID(991096256859707356)와 VD16 C4713은 **판본 수준 메타데이터**이지 동일한 물리적 개별 책이라는 뜻이 아니다.

GitHub Actions `42547810355`에서 기관 IIIF Manifest 2개 직접 확보 및 소장 메타데이터 확인. 이후 `42547899192`, `42548030677`, `42548193448`에서 도서관 기존 OCR을 통해 해당 조항 위치 추적. **기성 OCR은 위치 찾기용이므로 글자 교감 근거로 승격 금지.**

## 2. Google Books Augsburg Th S276 경로 — HTTP 200 함정 발견

- 서지: 1540 Rhau, Augsburg Staats- und Stadtbibliothek **Th S 276**, Google Books `HmpoAAAAcAAJ`. https://books.google.com/books?id=HmpoAAAAcAAJ
- `books.google.com/books/content?id=HmpoAAAAcAAJ&pg=PA10&img=1&zoom=1` 등의 앞부분 샘플은 HTTP 200 및 실제 인쇄면 **작은 이미지** 반환. 그러나 해당 샘플은 서문(PRAEFATIO)이지 제10조가 아니다.
- `PA30`, `PA40`, `PA50`, `PA60`, `zoom=3` 모두 HTTP 200이었지만 **동일한 9,103바이트 “image not available” 대체 이미지**였다. 본문 인쇄면 판독으로 계산할 수 없다.
- Google Books 원문 텍스트 다운로드 경로는 HTTP 403. 접근 제한을 우회하거나 OCR을 원 인쇄의 직접 시각 판독이라고 주장하지 않는다.

## 3. Halle 경로 및 제2 소장본 근거 등급

- Halle ULB, `Pon Vg 3008 a (2)`, 영구 식별자 `urn:nbn:de:gbv:3:1-143262`. 과거 `digitale.bibliothek.uni-halle.de`의 URL은 기관 안내 사이트로 리디렉션.
- `https://nbn-resolving.de/urn:nbn:de:gbv:3:1-143262`는 `https://opendata2.uni-halle.de/handle/1516514412012/972`로 리디렉션하나 실제 본문은 anti-bot 검증 화면. 우회·자동시도하지 않음.
- Emory Pitts `1540 CONF`(VD16 C4713)는 서지·표지 사진 단계로 유지; Gruber 28은 V3.44.1에서 직접 제10조 부분 이미지 판독 완료.
- Regensburg/Bamberg는 이미 **IIIF Manifest와 기성 OCR에 접근 가능한 공식 스캔**이다. 다음 작업은 **제10조가 수록된 Canvas를 좁혀 실제 이미지 고해상도 육안 판독**하고, Gruber 28과 세 가지 변경축을 대조하는 것.

## 4. 기존 V3.44.1과 아직 구별해야 할 결과

V3.44.1에서 1531 BSB Canvas 17과 1540 Gruber 28의 당대 인쇄를 직접 확인하였다.

- 1531 `vere adsint et distribuantur` → 1540 `vere exhibeantur`.
- 1540 `cum pane et vino` 명시.
- 1531 `improbant secus docentes`는 1540년 제10조 사진에 없음.

**여기서 Regensburg/Bamberg 독립 1540 소장본의 제10조가 동일하다고 아직 판정하지 않음.** 서지 일치와 본문 일치의 검증 단계는 다르다.

## 5. 검증 게이트

1. 두 개 BSB/MDZ Manifest의 **출처·연도·소장 정보**가 일치할 것: PASS.
2. 기관 OCR의 라틴어 단어는 **위치 찾기**로만 활용할 것: PASS.
3. Google Books의 대체 이미지와 실제 인쇄 이미지는 분리할 것: PASS.
4. **Regensburg 또는 Bamberg 제10조의 실제 이미지 육안 판독**: 아직 OPEN.
5. 둘 중 하나의 독립 원전과 Gruber 28 간 문구 교감: 아직 OPEN.
6. 사람의 학술 편집 승인 전 출판·앱 이관: **HOLD**.

**범위 제한:** 출처 링크·연구 로그·서지 식별만 저장. 기관 소장 이미지·현대 저작권 문헌 원본은 저장소에 커밋하지 않는다.
