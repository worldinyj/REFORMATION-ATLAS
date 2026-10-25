# VOL-03 · 역사 지도 4종 제작 근거 및 품질 기준 (V0.1)
> 2026-10-25 · 상태 DRAFT / 시각적 미리보기 검수 완료 · 역사 지리 전문가 감수 전

## 현 단계에서 만드는 것은 무엇인가
- 출처로 확인되는 **현대 지명 대표 좌표**를 지도 평면에 정렬한 역사 교육용 **위치 개념도**다.
- 실제 12~16세기 경계선, 도로, 국경, 경로 또는 군대의 진로를 복원한 정밀한 역사 지도는 아니다.
- 날짜·역사 관계는 연구 출처에 근거하고 위치는 현대 지명 좌표를 사용하므로, **역사적 발생 장소의 정확한 건물·경계와 다를 수 있다**.
- 어떠한 웹 지도 타일, 역사 지도 사진, 스톡 일러스트도 복사·트레이싱하지 않았다. 지도 구성·도형·문구·레이아웃을 독립 제작한 원본 SVG다.
- `assets/maps/`의 SVG는 텍스트, 원, 선, 레이어가 편집 가능하다. 16:9 (1500×900).
- 사용자용 ZIP은 SVG 4종으로 제공. PNG 미리보기는 검수 및 공유 편의 용도다.

## 지도별 사실관계
### MAP-V03-01 · 리옹의 왈도파
초기 운동은 1170년대 리옹에서 등장했다. 청빈보다 **인가받지 않은 공적 설교의 문제**가 갈등의 핵심 중 하나였다. 앙그로냐 핀은 1532년 후대 장을 독자적으로 비교하기 위한 것으로, 12세기부터 확정된 특정 여행 경로를 뜻하지 않는다. [V03-S01,S02,S26]
- 학술 논문: https://academic.oup.com/fh/article/32/3/327/5091977
- Angrogna 대표 좌표: https://www.tuttitalia.it/piemonte/39-angrogna/
- Lyon 대표 좌표: https://www.coordmap.com/cities/lyon

### MAP-V03-02 · 옥스퍼드–프라하
위클리프 저술의 프라하 수용은 **필사본·학자들의 교류**를 통해 설명한다. 그러나 구체적 전달 메커니즘과 물리적 노선은 여전히 연구 중이다. 점선은 영향의 도식일 뿐, 실제 중세 책 운반 경로를 트레이싱한 것이 아니다. 콘스탄츠는 후스의 1415년 처형 장소로 별도 표시한다. [V03-S05,S09]
- Ralph Hanna, 'Oxford to Prague: Orthodox Insular Texts in Bohemia', *The Library* (2023), https://academic.oup.com/library/article/24/3/302/7280415
- Marcela K. Perett, *Church History* (2015) 공개 초록: https://www.cambridge.org/core/journals/church-history/article/abs/neglected-eucharistic-controversy-the-afterlife-of-john-wyclifs-eucharistic-thought-in-bohemia-in-the-early-fifteenth-century/75573F8B29830575C3DE4322D3FA07F3

### MAP-V03-03 · 보헤미아의 주요 도시
프라하(설교·4개조), 타보르(1420년 후스파 거점), 쿠트나호라(역사적 도시/전쟁 맥락), 리파니 전투터(1434년), 이흘라바(1436년 공적 선포)를 현대 도시·전장 인근 좌표로 표기했다.
- 타보르: https://mapcarta.com/T%C3%A1bor
- 리파니 전투터: https://mapcarta.com/N7391917196
- 쿠트나호라: https://mapcarta.com/Kutn%C3%A1_Hora
- 이흘라바: https://mapcarta.com/Jihlava
- 콤팍타타 서지/서평: https://scholarworks.iu.edu/journals/index.php/tmr/article/view/31313

### MAP-V03-04 · 1530~1532년 대화망
모렐 등 왈도파 설교자가 개혁자들과 대화를 진행한 사실은 확인된다. 앙그로냐와 바젤·슈트라스부르·베른·뇌샤텔의 점선은 **교류 네트워크의 요약**이며 실제 방문 순서, 누구의 여행 일지, 교리 통합 완료 시점을 나타내지 않는다. 교단 자료의 후대 해석과 독립적인 1차 서신 대조는 추후 필요하다. [V03-S26,S27,S42]
- https://www.waldensian.org/history/encounters-with-the-reformation-in-the-1530s/
- https://museeprotestant.org/en/notice/a-history-of-the-waldensians/

## 좌표 관리
모든 점은 `data/vol03_map_points.json`에 **현대 대표 좌표**와 원문 URL을 함께 저장한다. 지도에 표기된 좌표가 정확한 15세기 시장·예배당이나 전쟁 당시 진영을 의미하지 않는다.

## 저작권·파일 구조
- 출처 웹사이트의 이미지는 **시각 참고만** 했다. 배경 영상·지도 타일·기존 지도 경계선·타인의 벡터 작업을 반영하거나 직접 복제하지 않았다.
- 라이선스 분류: `original_project_asset`. 다만 외부 지리좌표 데이터의 제공처별 출처는 위 링크와 JSON에 표기한다.
- Mac/Windows SVG 편집기에서 글꼴이 없으면 `NanumSquare, Noto Sans CJK KR, Arial` 등 대체 폰트로 표현한다. 글꼴 파일은 포함하지 않는다.
- 이미지 생성형 AI 인물 재현이 아니라 코드 기반 SVG 설명도이므로 `ai_disclosure = not_applicable_data_diagram`.

## 검증 기록 및 남은 작업
- PNG로 렌더링 후 제목, 지도 격자, 지도점 위치, 한국어 레이블, 주의 문구를 육안 검토.
- 위도/경도와 지도 투영은 등각도표(equirectangular) 단순 위치 변환이다. 동서/남북 거리의 실제 길이 비율을 주장하지 않으므로 **축척 막대 및 이동 거리 표기 생략**.
- 후속 고증: 당대 정치 경계, 고대 도시 구역, 실제 필사본 전달과 관련한 문헌 증거, 왈도파 회합의 자세한 위치, 리파니 전투 정확 현장 배치.
- 현재 지도는 `DRAFT`이며 승인받은 역사 경계 지도라고 소개하지 않는다.
