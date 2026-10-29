# VOL05 V0.7 | 1648 이후 지역 원자료 확인 경로 — 연구 인수 문서

> **DRAFT_RESEARCH_NOT_PUBLIC**, 2026-10-29. 연구 브랜치 research/vol05-v35-primary-archive-leads-v07. 기존 정본/Google AI Studio/main 변경 0.

## 연구 신규 발견

- **1649 Augsburg St Servatius**: 시 역사사전은 이 병원의 종파별 공동 운영 시작을 1649년으로 명시한다. **IPO V §3 맥락의 기관 관리**, 개별 환자에 대한 **V §35 집행 사건이 아님**.
- **1648 vs 1712/1757 archives**: 시 공문헌은 1648 이후 종파별 행정기록 분화를 언급한다. Augsburg 신 디지털 열람실 안내는 Evangelisches Wesensarchiv(1712)와 Katholisches Wesensarchiv(1757)의 별도 정식 수립 연도를 제시한다. 행정업무 분화와 기관의 설립 날짜를 혼동하면 안 된다.
- **Münster A II Nr. 20**: 시의회 212권이 온라인 디지털화됐지만 **1648년의 연도별 권은 결락**한다. 1649~1655년의 색인/청원에서 장례·길드·종교 권리를 조사할 수 있다.
- **Münster Judicialprotokolle / Acta Judicialia**: 약 65권(1548~1661)의 민사 법정 등록부와 약 1,161건의 사건 문서 자료군을 별도로 확인. 대량의 사건 기록이 존재한다는 사실은 §35의 특정 종교재판이 발견됐다는 뜻이 아님.
- **2024 scholarly review**: Ulrike Ludwig와 Philip Hoffmann-Rehnitz 편집 Münster nach dem Dreißigjährigen Krieg (1648–1655), 217쪽. 출판사/대학 개요만 확인했고 전체 저작과 구체 장례 사건은 미확인.
- **Visual candidate**: bavarikon의 1742년 Augsburg Hl.-Geist-Spital 판화는 St. Servatius 1649년의 현장 그림이 아님. 기관이 PDM/CC0 라벨을 제공하지만 이 연구 브랜치에서는 이미지 파일을 수집하거나 공개하지 않았다.

## 산출물

1. docs/01_CONTENT/VOL05/IPO_V35_AUGSBURG_ST_SERVATIUS_1649_V07.md
2. docs/01_CONTENT/VOL05/IPO_V35_MUENSTER_DIGITAL_COUNCIL_COURT_V07.md
3. data/deep/vol05_ipo_v35_primary_archive_leads_v07.json (14 source records / 5 findings / 4 archive target series / 0 verified V35 trial)
4. scripts/validate_vol05_v35_primary_archives_v07.py
5. scripts/test_vol05_v35_primary_archives_negative_v07.py (**30 false mutations rejected**)
6. .github/workflows/vol05-v35-primary-archives-qa.yml

### 다음 조사

아우크스부르크의 1648~1652 성 세르바티우스 시설 관리 기록을 찾고, 뮌스터 1649~1655년 A II Nr 20 의사록 색인과 해당 법정문서가 교차하는 실제 사건을 찾아야 한다. 반드시 **인물·날짜·신앙고백·§35 원문 또는 다른 법률 근거·판결 결과·보존번호**를 확인해야 법적 적용 사례로 승격할 수 있다.

기존 IPO 온라인 라틴어 전사·원본 오스트리아 이미지 미열람·APW 비평판 직접 미대조 한계는 그대로 유지. 원문, 현대 사진, PDF를 저장소에 무단 복제하거나 공개하지 않는다.
