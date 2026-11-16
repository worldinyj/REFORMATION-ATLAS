# REFORMATION-ATLAS V3.81 — Kalliope 식별번호 정정 및 장크트갈렌 원고 추적

- 연구 기준일: **2026-11-16**
- 범위: 1536년 7월 부처(Martin Bucer) → 바디안(Joachim Vadian) 서신
- 연구 브랜치: `research/atlas-v381-catalog-id-correction-and-findingaid`
- 배포 상태: **RESEARCH_DRAFT / NOT PUBLISHED**
- 중요: 이전 단계의 GitHub 연구 브랜치는 그대로 두고, 이 브랜치에서는 V3.77–V3.80 파일의 오류를 정정함.

## 1. Kalliope 목록 직접 항목 분리 (V3.81 신규 정정)

취리히 중앙도서관의 Kalliope 통합목록에서 목록의 `eadCH-...` 식별번호는 **해당 번호 다음에 시작하는 서신 표제**에 속한다. 기존 연구에서는 다음 항목의 식별번호를 부처→바디안 서신에 잘못 연결하였다.

| ID | 목록의 실제 표제 | 목록 날짜 | 원고 청구기호 | 판단 |
|---|---|---|---|---|
| `CH-002121-2-991170608445805501` | **Martin Bucer → Joachim Vadian** | **1536-07-25** | Zürich ZB `Ms S 41, Nr. 33` | **올바른 후보 기록 ID** |
| `CH-002121-2-991170609317505501` | **Heinrich Bullinger → Ambrosius Blarer** | **1547-08-24** | Zürich ZB `Ms F 43 (133)` | 기존 부처 기록에 잘못 연결된 ID |

목록 출처: https://nachlassdatenbank.de/findingaid?fa.id=CH-002121-2-881170715577605501&fq=ead.pers.index%3A%28%22Albert-Durade%2C+...+d%27%22%29&htmlFull=false&lang=de&lastparam=true

**확인한 범위:** 공개 목록의 식별번호·표제·기재 날짜·서명. **확인하지 않은 범위:** 원본 날짜 행, 봉인·수신인, 필체, 전체 편지 내용. 날짜가 원본에 어떤 형식으로 적혀 있는지는 미확인.

## 2. 장크트갈렌 Vadianische Briefsammlung 디지털 원고목록 추적경로 신규 확보

이번 단계에서 장크트갈렌의 **원고 컬렉션 자체에 대한 Kalliope finding aid**도 확인하였다.

- Finding aid: https://kalliope-verbund.info/gnd/findingaid?fa.enum=1&fa.id=CH-002121-2-991170432739305501
- 전체 컬렉션 서명: `VadSlg Ms 30–41a`
- 목록 전체 **3,790개 항목** 표시
- 해당 목록 인명 색인: https://kalliope-verbund.info/gnd/findingaid_index?fa.enum=1&fa.id=CH-002121-2-991170432739305501&lastparam=true
- 인명 색인: **Bucer, Martin (1491–1551) (49)** 표시

**주의:** 49는 색인 히트 수이지 1536년 부처→바디안 편지가 49통 존재한다는 증거가 아니다. 7월 23일 서신의 원고 목록 항목도 아직 식별하지 못했다.

장크트갈렌 소장기관 설명: https://www.stadtarchiv.ch/forschungsprojekte/vadianische-briefsammlung/

## 3. 아직 해소되지 않은 날짜 쟁점

| 후보 | 날짜 | 현재 증거 | 역사 콘텐츠 게시 |
|---|---|---|---|
| A | **1536-07-23** | V3.74에서 전승된 `WA Br 7 Nr.3048` 편집주 경유 인용, `Vadian BW V p.339` | **차단** |
| B | **1536-07-25** | 취리히 중앙도서관 Kalliope 목록 `Ms S 41, Nr.33`, 이번 버전 정정 ID | 연구자 검토 전용 |
| C | **1536-08-06** | HBBW 875 불링거→바디안, `Vadian BW V pp.341–343` | 비평판 출처를 명시하는 해설 후보 |

A=B라는 결론은 여전히 근거 부족이다. HBBW 875의 편집주가 `Vadian BW V p.339`를 인용한다는 사실도 1536년 7월 25일 취리히 기록과의 동일성 확증은 아니다.

## 4. 근거 복원과 GitHub 작업

- 새 브랜치의 V3.77, V3.78, V3.79, V3.80 JSON 파일에서 **올바른 취리히 식별번호로 정정**함.
- 기존 독일어 문의문에도 **올바른 식별번호를 반영**함.
- V3.80 검증 스크립트의 해당 식별번호 검사도 업데이트함.
- 정정 이력 `catalog_id_amendment` 필드를 추가하여 잘못 기록한 번호와 그 실제 귀속 문서를 보존함.
- 별도 정정 원장: `research/data/V3_81_CATALOG_ID_CORRECTION_AND_ARCHIVE_LEAD.json`
- 재발 방지 검사: `research/scripts/validate_v381_kalliope_ids.mjs`
- **중요:** 이전 버전의 원래 GitHub 커밋(과거 연구 상태)은 삭제하거나 다시 쓰지 않았음.

## 5. 소장기관 문의 시 추가할 독일어 보충 질문 (미발송)

### Zürich: corrected catalog id
> Für unsere Anfrage zur Handschrift **Ms S 41, Nr. 33**, Martin Bucer an Joachim Vadian, **25. Juli 1536**, verwenden wir nach erneuter Prüfung des Kalliope-Findbuchs die korrekte Datensatzkennung **CH-002121-2-991170608445805501**. Die zuvor von uns notierte Kennung **CH-002121-2-991170609317505501** gehört zu einem anderen Stück (Bullinger an Ambrosius Blarer, 24. August 1547). Können Sie bitte die handschriftliche Datumszeile, die Dokumentart (Original/Abschrift) und einen Digitalisatlink bestätigen?

### St Gallen: finding aid
> Im Kalliope-Findbuch **Vadianische Briefsammlung** (Bestand **VadSlg Ms 30–41a**, Findbuchkennung **CH-002121-2-991170432739305501**) konnten wir die Gesamtüberlieferung und den Personenindex zu **Martin Bucer** lokalisieren, aber den konkreten Brief zu *Vadianische Briefsammlung* V, S. 339, noch nicht eindeutig bestimmen. Könnten Sie die dortige vollständige Editionsüberschrift, das Briefdatum und eine gegebenenfalls vorhandene Originalsignatur mitteilen?

## 6. V3.82 최우선 실증 과제

1. **장크트갈렌 색인 내부의 부처 관련 항목을 날짜로 필터링**하고, 1536년 7월 개별 소장기록의 표제·청구기호·URL을 확보한다.
2. 취리히 `Ms S 41, Nr.33`의 원문 날짜 판독을 확보한다.
3. 인쇄본 V권 338–343쪽 실제 이미지와 `WA Br 7 Nr.3048`의 서지 문구를 비교한다.
4. 이 세 증거가 충족되기 전까지 **날짜 동일성 강제 병합 및 공개 연표 삽입 금지**.

**기관에 실제 이메일을 보내지 않았으며**, `main`·기존 역사 원고·AI Studio 웹앱은 수정하지 않았다.
