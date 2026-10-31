# V1.51 — 위클리프 1886년판 직접 판면 확인 게이트

**2026-10-31 · RESEARCH_ONLY · 공개 보류**

## 이번 접근 결과
Open Library의 1886년판 서지와 Internet Archive 자료 항목은 다시 확인했다. 전체 자료는 John Wycliffe의 *Tractatus de ecclesia*, Johann Loserth 편집, 1886년 London, 전면 로마숫자 xxxii쪽 + 본문 600쪽으로 식별된다.

실제 PDF URL (`https://archive.org/download/tractatusdeeccl00wycl/tractatusdeeccl00wycl.pdf`) 요청은 Internet Archive의 별도 보관 서버 `dn760001.eu.archive.org`로 이동했고, 현재 웹 열람 환경은 해당 외부 리다이렉트 대상에 접근하지 못했다. 이 실패를 원문 열람 성공으로 바꾸지 않는다.

## 원문 대조 후보의 진위 상태
| 인쇄본 위치 | 학술논문에서 보고한 편집본 참조 | 학술논문에서 보고한 필사본 참조 | 판면 직접 확인 |
|---|---|---|---|
| 257쪽 1행 | 20장 | 22장 | 아니오 |
| 467쪽 29행 | 27장 | 25장 | 아니오 |

각 지점은 연구 논문이 알려준 검증 후보이며, 내가 판면을 직접 읽어 확정한 이문이 아니다. 특히 인쇄본 257쪽을 스캔의 257번째 이미지로 취급하면 로마숫자 서문·표지 등 때문에 엉뚱한 페이지를 열게 될 수 있다.

## 편집자 서문
1886년판의 서문은 로마숫자 xxxii쪽 범위가 있으나, 이번 환경에서 서문을 직접 판독하지 못했다. 그러므로 Loserth가 사용한 세 완본의 sigla와 소장처·서가번호는 여전히 **미확인**이다.

## 다음 실질적 대조 방법
1. Open Library의 Read 화면 또는 SIEPM 검색 가능 판본으로 진입하여 **화면에 표시되는 인쇄쪽수**를 기준으로 257·467쪽 확인.
2. 판본 메타데이터가 일치하는 다른 디지털 스캔 `johanniswycliftr1401wycl`을 교차 확인하되, 제목만으로 동일한 책이라고 가정하지 않기.
3. Loserth 서문의 전반 32쪽에서 sigla·소장처·원고 비교 방법을 먼저 수집.
4. 판면·서문 직접 확인 완료 후에만 `facsimile_verified` 및 `manuscript_sigla_extracted` 값 변경.
5. 요약·문장 인용은 원문 직인용인지 후대 연구의 설명인지 별도로 표시.

## 출처
- [Open Library](https://openlibrary.org/books/OL24355600M/Tractatus_de_ecclesia)
- [Internet Archive](https://archive.org/details/tractatusdeeccl00wycl)
- [SIEPM 검색 가능 판본](https://siepm-digitalresources.bc.edu/books/)
- [Google Books 배포본](https://play.google.com/store/books/details/Johannes_Wyclif_Johannis_Wyclif_tractatus_de_eccle?id=JAad-LddLx8C)

## 웹앱 반입 주의
연구 상태를 `CATALOG_CONFIRMED_SCAN_UNREAD`로 유지하며, 원고 이미지와 전체 현대 텍스트를 자동으로 배포하지 않는다. `main` 및 Google AI Studio 앱은 수정하지 않았다.
