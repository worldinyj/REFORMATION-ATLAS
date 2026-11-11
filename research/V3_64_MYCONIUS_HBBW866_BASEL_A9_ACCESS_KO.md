# 종교개혁 ATLAS V3.64 — HBBW 866 및 미코니우스 서신 교차목록·바젤 A9 접근 감사

- 연구일: 2026-11-11
- 계승: research/atlas-v363-bds-title-apparatus-correction
- 연구 브랜치: research/atlas-v364-myconius-letters-basel-a9-access
- 상태: RESEARCH_ONLY / DRAFT / NOT_APPROVED / CAN_SHIP=false
- 변경 범위: 신규 연구문서만. 기존 513편, main, 앱, 원전 파일 불변.

## 1. HBBW 6 / Nr. 866 공식 편집목록

취리히대학교 종교개혁사연구소 공식 편집 서신목록은 다음을 명시한다.

> Nr. 866: Oswald Myconius an Bullinger, Theodor Bibliander und Konrad Pellikan, Basel, 19. Juli 1536

- https://www.irg.uzh.ch/de/publikationen/bullinger/edition-briefwechsel/briefverzeichnis.html
- 확인 가능: 편집번호, 발신자, 수신자, 날짜, 편집본의 제목식 목록.
- 확인 불가: 편지의 전체 라틴어 원문, 편집 각주, 문장별 판독, 필사본 이미지. **LETTER_BODY_NOT_SEEN**.

취리히대학교 공식 전자판 소개: https://www.irg.uzh.ch/de/publikationen/bullinger/e-ausgabe.html
전자판 연결 https://teoirgsed.uzh.ch/ 는 이번 조사에서 타임아웃. 접근 실패를 원문 부재의 증거로 오인하지 않는다.

## 2. 독립 사료목록 — 바젤대학교 Oswald Myconius Briefdatenbank

- 출처: https://www.myconius.unibas.ch/briefdb.html
- 이 데이터베이스는 공개된 날짜·발신·수신·소장지·판본 목록이며 편지 전문이 아니다.
- 1536-07-15: Myconius → Bullinger 및 Bullinger → Myconius 목록 존재.
- `Die Lucae [eher: 18. 7.?] 1536`: Martin Bucer → Oswald Myconius, Strasbourg StadtA, 편집 참고문헌 'Barge, Karlstadt'. 날짜는 재구성·추정으로 기록. **이 레코드는 HBBW 866이 아닌 별도 문서이며, 실제 날짜 7월 18일 확정 금지.**
- 1536-07-18: Bullinger → Myconius, Zürich StA.
- 1536-07-19: Myconius → Bullinger, [Bibliander], Pellikan, Zürich StA, Bullinger BW.
- 1536-07-28: Bullinger → Myconius, Zürich StA.
- 1536-07-31: Myconius → Bullinger, Zürich StA.
- 1536-08-02: Bibliander → Myconius, Zürich StA.

### 독립 교차검증의 정확한 의미
두 학술 데이터베이스에 7월 19일 편지의 서지 정보가 나타난다. 이로써 '그 날짜·발신·수신의 편지가 편집·목록에 실림'을 교차 확인했으나, **개별 라틴어 문장과 대표단 위치는 아직 검증한 것이 아니다.**

## 3. 날짜 문제를 다루는 수정된 이벤트 테이블

| 날짜 | 관찰·문헌 | 날짜 확실성 | 사건 유형 판정 |
|---|---|---|---|
| 1536-07-17 | BDS p.217의 16세기 후기 기재에 등장 | 기재값 | 협의 종료/문서 작성/파견일 중 어느 것인지 미확정 |
| 1536-07-18? | 부처→미코니우스 `Die Lucae` | 현대 데이터베이스의 날짜 추정 | 편지의 원문·본문 날짜 미확인 |
| 1536-07-19 | 미코니우스→불링거·비블리안더·펠리칸 | 공식 편집 목록 | 대표단이 실제 어디에 있었는지 본문 검수 전 미확정 |
| 1536-07-29 | 카를슈타트→불링거 HBBW 870 | 공식 편집 목록 | 편지 내용 재교감 필요 |

**검증 제한:** V3.63에서 인용했던 BDS p.218의 라틴어 `Et iam sunt Argentinae. Nos expectamus, quid referant`는 편집판의 인용을 경유한 것으로서 이번 연구에서 HBBW 866의 전체 라틴 원문을 직접 읽어 독립 검증하지 못했다. 그 구절을 현대 목록의 메타데이터만으로 확인했다고 표시하지 않는다.

## 4. Basel Staatsarchiv의 실제 최신 검색 경로

바젤슈타트 주 정부의 공식 2022-11-15 안내에 따르면, 2022-11-24부터 디지털 열람실(Digitaler Lesesaal) https://dls.staatsarchiv.bs.ch 가 기존 query.staatsarchiv.bs.ch 대신 운영됨.

- 공식 안내: https://www.bs.ch/news/2022-umstellung-archivkatalog
- 검색 대상: 기존 문헌에서 언급한 `Kirchenakten A9`, `Bl.405–410` 및 1536년 바젤 성찬 협의.
- **현행 문서 식별자 확인: NOT_FOUND_IN_ACCESSIBLE_PUBLIC_RESULTS**.
- **해당 면의 디지털 이미지 접근: NOT_VERIFIED**.
- 자료 위치를 확인하지 못했다는 것이 사본이 없다는 증거가 아니다.

## 5. 다음 우선 연구

1. HBBW 전자판의 대체 접근 경로(공식 출판사·도서관)을 통해 Nr.866의 서신 본문과 각주를 직접 열람하고, 1536-07-19 현재 대표단의 위치 및 `Argentinae` 문구 해석 확인.
2. 바젤대학교 서신 목록의 `Die Lucae [eher 18.7.?]` 부처→미코니우스 서신을 Barge 1905의 인용문·소장 정보와 대조하여 왜 날짜가 추정인지 확인.
3. 바젤 국가문서보관소 디지털 열람실에서 A9 405–410의 현행 서가번호·디지털 자료 유무 확인.
4. 실제 원전 지면을 확보하여 Barge 부록 50 Q1~Q4와 BDS 6/1 A–D의 문장 단위 교감.
5. 전문 검토 후에만 원고 513편 개정 여부를 판단.

## 6. 연구 QA

- PASS: HBBW 편집목록의 Nr.866 발신·수신·날짜 확인.
- PASS: Basel Myconius 서신 목록에서 동시대 교환 및 ‘Die Lucae’ 기록 확인.
- PASS: 국가문서보관소의 **현행** 검색 시스템 식별.
- PENDING: HBBW 866 전문/원본 이미지.
- PENDING: A9 405–410 현행 식별자와 해당 문장 결여 확인.
- PENDING: 전체 교감·전문가 검토.
- CAN_SHIP=false.

## 참고 원문 경로
- https://www.irg.uzh.ch/de/publikationen/bullinger/edition-briefwechsel/briefverzeichnis.html
- https://www.irg.uzh.ch/de/publikationen/bullinger/e-ausgabe.html
- https://www.myconius.unibas.ch/briefdb.html
- https://www.bs.ch/news/2022-umstellung-archivkatalog
- https://dls.staatsarchiv.bs.ch
