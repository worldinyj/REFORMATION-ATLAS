# 제5권 V1.12 — 1651년 여학생 100명 이상 근거 및 콘텐츠 연결 데이터 검증

**DRAFT_RESEARCH_NOT_PUBLIC** · 2026-10-29

## 검증 결과

**확인:** Karl Hengst 편, *Westfälisches Klosterbuch*, Teil 2, Aschendorff 1994, 2024년 디지털 발행, 뮌스터 항목 인쇄 111쪽(디지털 PDF 0-based page 113), §2.4.2는 1651년 교육수녀회가 여학생 100명 이상에게 읽기, 쓰기, 계산, 수공교육을 무료로 제공했다고 기술한다. PDF 텍스트 위치: line 4160–4166, 특히 4161–4163. 해당 문헌은 1994년 연구서의 디지털판이며 **1651년 당시의 학교 장부 원본이 아니다**. PDF 화면 캡처는 도구 시간 초과로 확인하지 못했으므로 이미지 판독은 여전히 미완료.

**추가 사실:** §2.3.1에서 뮌스터 수도회의 자매 수도원으로 Essen(1652)과 Paderborn(1658)을 거론한다. §2.4.2에는 1750년경 무료학교 약 200명, 1809년 학교 여학생 170명이라는 별개 시점도 기록되어 있다. 서로 다른 시점의 통계를 합산하지 않는다.

**서지 정확성:** 2024년은 연구서의 최초 간행연도가 아니다. PDF 앞부분에 원판 1994년, 온라인판 2024년을 분리 표기한다. PDF 판권의 CC BY-SA-ND 3.0 DE 및 재사용 제한을 확인했으므로 원본 페이지 이미지를 웹앱에 임의로 복제하지 않는다.

## 근거 상태

| Claim | 판정 | 직접 미확인 요소 |
|---|---|---|
| 1651년 100명 초과 교육 | 후대 학술자료 본문 확인 | 당시 수녀회 학교장부/시의회 원사료 |
| 읽기·쓰기·계산·수공교육 무료 제공 | 동일 학술자료 본문 확인 | 1651년 교육과정 원본 문서 |
| Essen 1652 / Paderborn 1658 네트워크 | 동일 학술자료 본문 확인 | 각 재단 설립문서 |
| 1649년 2월·3월 시의회 논의 | Jakobi 연구를 통한 간접 확인 | 의사록 folio 및 APW 원문 |

## JSON 연결 데이터 초안
경로: `data/deep/vol05_muenster_education_claim_graph_v112.json`

- entities: 기관 및 장소.
- sources: 학술 문헌/시 역사자료의 구별, 서지연도 및 PDF 페이지.
- claims: 시점, 진술, 출처, evidence_level, 원사료 검증 여부.
- events: 사건과 해당 근거를 연결.
- publication_gate: `approved=false`, `can_ship=false`.

특히 정량 데이터 100명은 정확한 학생 수가 아니라 **100명 초과라는 하한 표현**이다. 표현상 100명으로 반올림하거나 1649년으로 당겨 기재하면 안 된다.

## 후속 QA
1. claim의 참조 ID 유효성, 연도, 출처 없는 내용의 금지.
2. 원사료 미검증 항목의 공개 승격 거절.
3. 문헌의 저작권/사용조건을 이미지·전문과 해설별로 따로 판단.
4. 본 연구 브랜치만 유지; main/AI Studio 앱 배포 0.

## 출처
- https://www.lwl.org/hiko-download/HiKo-Reihe_044_Band_2_Teil_2_%282024%29.pdf
- https://www.presse-service.de/data.aspx/static/592334.html
- https://www.lwl.org/westfaelische-geschichte/portal/Internet/drucken.php?ID=445&tab=tex
