# VOL-03 · 편집 가능한 SVG 역사 지도 4종
> V0.1 · DRAFT · 2026-10-25

| 자산 ID | 범위 | SVG 파일 | 해설 |
|---|---|---|---|
| MAP-V03-01 | 리옹의 12세기 청빈·설교 운동과 후대 앙그로냐 비교 | [지도01](MAP-V03-01_waldensians_lyon.svg) | 12세기 직접 여행경로를 주장하지 않음 |
| MAP-V03-02 | 위클리프 저술: 옥스퍼드 → 프라하의 선택적 수용 | [지도02](MAP-V03-02_oxford_prague.svg) | 점선은 실제 필사본 이동노선 아님 |
| MAP-V03-03 | 프라하·타보르·쿠트나호라·리파니·이흘라바 | [지도03](MAP-V03-03_bohemia_hussite.svg) | 옛 국경·군사 작전·전투 대형 미복원 |
| MAP-V03-04 | 앙그로냐·바젤·슈트라스부르·베른·뇌샤텔 | [지도04](MAP-V03-04_waldensian_reform_network.svg) | 1530~32 교류망이지 실제 출발/방문 순서가 아님 |

각 지도는 직접 작성한 독립적인 SVG 파일이며 텍스트·핀·곡선·패널을 별도 편집할 수 있습니다. 한국어 본문은 `Noto Sans CJK KR` 글꼴 대체 순서를 지정했습니다. 글꼴 파일 자체는 저장소에 포함하지 않습니다.

## 좌표와 편집
- [좌표 및 지도별 핀 데이터](../../data/vol03_map_points.json): 13개 근현대 도시/전장 인근 참조점과 4개 지도에 대한 연결.
- 도시 위치는 **근현대 지도 기준 대략적인 중심점**입니다. 역사적 정확 좌표·국경·동시대 도로망에 대한 감수를 완료하지 않았습니다.
- 좌표값은 `coordinates_verified=false`로 보수적으로 기록했습니다. 상세 출처가 확인된 지점도 성당·전투터·합의 장소의 정확 위치를 의미하지 않습니다.
- 그림에 표시한 '리파니'는 특정 전장의 고고학적 경계가 아니라 전투터 *인근*의 지리상 위치입니다.
- 지도가 비율을 정확하게 나타내는 현장 측량도, 공식 역사 지도, 실제 군사 배치도를 뜻하지 않습니다.
- 지도04의 개혁자 방문은 1530년 모렐과 동료들의 외교·서신·대화와 연관된 **여러 도시**를 보인 도식입니다. 선의 방향이 개인별 확정 여행 경로라는 뜻이 아닙니다.
- 마커 색: 주요 해설 대상=초록, 비교/참조 지점=갈색. 점선=문헌/교류 개념 관계.

## 2차 근거
- **Oxford 학술 연구**, Ralph Hanna, “Oxford to Prague: Orthodox Insular Texts in Bohemia,” *The Library* 24(3), 2023. https://academic.oup.com/library/article/24/3/302/7280415. 옥스퍼드→프라하의 필사 문화 연구; 실제 도로 및 정확 운반 경로를 제공하지 않음.
- **American Waldensian Society**, “Encounters with the Reformation in the 1530s.” https://www.waldensian.org/history/encounters-with-the-reformation-in-the-1530s/ . 모렐의 1530년 교류, 1532년 앙그로냐 관련 기록 설명.
- **Musée protestant**, “A History of the Waldensians.” https://museeprotestant.org/en/notice/a-history-of-the-waldensians/ . 16세기 개혁자들과의 여러 도시 교류 확인.
- **Geographic sanity check**, Italian locality Angrogna https://www.italiamappata.it/piemonte/35-angrogna/ ; Czech state geodetic stations https://czepos.cuzk.gov.cz/_souradnice.aspx . 관측소 좌표와 지도상의 도시 중심점은 동일하지 않음.
- 관련 본문 학술 출처 IDs: V03-S01, S02, S05, S09, S11, S14, S26, S27, S34, S42. 역사학 감수 전 공개용 증거 지도라고 호칭하지 않습니다.

## 제작·저작권
- SVG는 **자체 제작 원본**이며 상용·유료 지리 베이스맵이나 타사 이미지 파일을 트레이싱하지 않았습니다.
- 지도 내 핀/곡선/텍스트의 의미는 문헌학적 연결과 역사 연대표, 대략적인 도시 위치에 근거한 것만 허용합니다.
- 로컬 생성 및 검토용 PNG와 SVG ZIP은 본 대화에 별도 파일로 제공하되, 이 저장소에는 SVG 원본과 메타데이터를 기준 자산으로 보관합니다.
- 사람의 지도/콘텐츠 검토 후 상태를 DRAFT에서 REVIEWED로 승격할 수 있습니다. 자동으로 공개 승인하지 않습니다.
