# 종교개혁 ATLAS V3.49.1 — 비텐베르크 일치 1536년: CR III(1836) 75–78단 원 인쇄 직접 판독과 1540 CA-X 교감

**작성:** 2026-11-09 · **상태:** `RESEARCH_DRAFT_HOLD` · **부모:** V3.48  
**대상:** 1836년 편집·출판된 `Corpus Reformatorum` Vol. III, No. 1429 `Formula Concordiae`, **인쇄 열(column) 번호 75–78**.  
**중요:** 이 단계에서 직접 확인한 것은 **1836년 간행본의 실제 인쇄 이미지**이다. **1536년 당시 필사 원문 이미지가 아니다.**

## 1. 원전 수록 좌표 — 쪽수/단수/스캔 번호 분리

Princeton Theological Commons [1836년 CR 제3권 서지](https://commons.ptsem.edu/id/philippimelantho03mela)는 `Philippi Melanthonis Opera quae supersunt omnia`, 제3권, Halle: Schwetschke, 1836, **674쪽 디지털 원본**을 표시한다. Amy Nelson Burnett(2016)은 합의문 원문 수록 위치를 CR III **75–77**로 인용한다. 이를 조사하면서 핵심적인 서지 구분을 확인했다.

실제 인쇄본의 같은 한 페이지는 **좌·우 두 개의 번호가 매겨진 단(column)**으로 구성되어 있다. 즉 **75–76단이 하나의 스캔**, **77–78단이 다음 스캔**이다. 서지의 '75–77'을 단순한 PDF/IIIF 이미지 인덱스 `75–77`이라고 읽거나 인쇄 75~77면이라고 단정해서는 안 된다.

| 인쇄 단 | 1836년 인쇄면 이미지 | 해당 구간에서 직접 확인한 사실 |
|---|---|---|
| **75 (왼쪽)** | [IA IIIF scan 62](https://iiif.archive.org/image/iiif/3/philippimelantho03mela%2Fphilippimelantho03mela_jp2.zip%2Fphilippimelantho03mela_jp2%2Fphilippimelantho03mela_0062.jp2/full/1400,/0/default.jpg) | `No. 1429`, `29. Maii`, `Formula Concordiae`, 제목, I항과 II항 |
| **76 (오른쪽)** | 동일 scan 62 | III항, 서명 요구와 서명자 명단 시작 |
| **77 (왼쪽)** | [IA IIIF scan 63](https://iiif.archive.org/image/iiif/3/philippimelantho03mela%2Fphilippimelantho03mela_jp2.zip%2Fphilippimelantho03mela_jp2%2Fphilippimelantho03mela_0063.jp2/full/1400,/0/default.jpg) | Martin Luther, Philipp Melanchthon 등 이름, `De Baptismo` |
| **78 (오른쪽)** | 동일 scan 63 | `De Absolutione`, `Actum et finitum ... 29. Maii Anno 1536`, `Buceri exhortatio ad Collegas`의 시작 |

해당 CR III의 이미지 IA 객체: `philippimelantho03mela`; [공식 IIIF v3 Manifest](https://iiif.archive.org/iiif/philippimelantho03mela/manifest.json), **674 canvases**. **스캔 62/63은 1-based 파일 순번**, 원본 manifest의 **0-based index 61/62**에 대응한다.

### 파일 무결성: 받았던 이미지 바이트의 원 SHA-256

| scan | 원 JPEG 바이트 | 이미지 반환 크기 | 수신 파일 SHA-256 |
|---|---:|---|---|
| 62 | 647,000 | 1401×1729 | `0fb1c09b458f0ded51354c2675e4f93ac545845e94af8b58a43ce29655e94f6a` |
| 63 | 667,997 | 1401×1729 | `9b513c04c6e97b54b0b1f82cb29cbb7edd201f240608991d35574a6a906d39c0` |

GitHub Actions **run `42570853740`**, job **`129007626603`**, IA 원 인쇄 JPEG 두 장 HTTP 200 수신. 실제 이미지 두 장의 인쇄 숫자·본문·표제·연속 구간을 시각 검토하였다. SHA-256은 서버에서 수신한 **1400px 이미지 JPEG 원 바이트**의 해시이며, 검토용 재인코딩 축소 이미지의 해시와 다르다. 원본 전체 책이나 1536 원문 필사본을 저장소에 복제하지 않았다.

## 2. 인쇄 본문 직접 판독: 성찬 합의의 핵심 논점

아래는 1836년에 인쇄된 라틴어 조항의 **짧은 검증 표식**으로, 1836년 고전 인쇄본은 저작권 제한 자료가 아니나 불필요한 전체 원문 재게시를 피한다.

**I항 (75단)** — 이레네우스의 성찬 이해를 끌어오고, 빵과 포도주와 함께 실제 임재·제공·수찬을 고백한다.

- 인쇄 표식 `Confitentur iuxta verba Irenaei`, `Eucharistiam duabus rebus, terrena et coelesti`.
- 핵심 짧은 읽기: `cum pane et vino vere et substantialiter adesse, exhiberi et sumi`.
- 제2요소: `corpus Christi et sanguinem`으로 표현.

**II항 (75단→76단)** — 성례의 결합을 표현하면서 국소적·영구적 봉입과 구별한다.

- `negant fieri transsubstantiationem`.
- `nec sentiunt fieri localem inclusionem in pane`.
- `concedunt sacramentali unione panem esse corpus Christi`.
- `porrecto pane simul adesse et vere exhiberi corpus Christi`.
- 성례 사용 이외의 보관·행렬에서 현존함을 주장하지 않는 문맥이 이어진다.

**III항 (76단)** — 성례는 집례자·수찬자의 개인적 합당함에만 의존하지 않으며, 합당하지 않은 사람도 수찬하되 심판을 받는다는 논의.

- `nec pendere ex dignitate ministri aut sumentis`.
- `etiam indignos manducare`, `porrigi vere corpus et sanguinem Domini etiam indignis`.
- `Sed tales sumunt ad iudicium`.

**III항 다음:** 76단은 합의가 다른 설교자·상급자에게 전달될 필요가 있다고 말한다. 이는 **1536년 현장 합의의 서명만으로 독일/스위스의 모든 개혁 교회가 즉시 동의했다**고 단정하는 해석을 막는 근거다. 76·77단의 서명자 명단에는 Capito, Bucer, Luther, Justus Jonas, Melanchthon 등이 포함된다.

## 3. 원 인쇄본에 명시된 날짜: 5월 29일

- 75단의 문헌 번호 `No. 1429.` 바로 오른쪽에 **`29. Maii.`**가 분명히 인쇄돼 있다.
- 78단 사죄(Absolution) 항목의 끝은 **`Actum et finitum secunda feria post Exaudi, 29. Maii Anno 1536`**로 되어 있다.
- 앞 단계에서 [MBW 1744](https://melanchthon.hadw-bw.de/regest.html?reg_nr=1744)의 1536-05-29을 우선 날짜로 택한 근거를 **1836년 CR 원 인쇄판의 내부 표시와 독립 교차확인**했다.
- BDS 6/1(1988) 항목의 표제는 이전 단계에서 28일로 확인되었고, MBW는 이를 잘못된 날짜로 지적한다. **어느 편집자가 어떠한 원사본에 근거해 28일로 기재했는지**까지 이번 두 원 인쇄면만으로 해결한 것은 아니다.
- BDS 비평 장치에 전하는 특정 사본 표제의 `XXiii May`(23일) 같은 다른 날짜 표현은 회의 과정·특정 문서의 날짜일 수 있다. 이를 29일의 완료 일자와 **동일한 사건 기준으로 치환하지 않는다**.

**원전 경계:** 이 날짜들은 1836년 판의 실제 인쇄판에 존재하는 **편집된 날짜 증언**이다. **1536년 서명·날짜 기재 필사본 자체를 직접 본 것은 아니다.**

## 4. BDS 1988 편집 전사 / 1836 CR 원 인쇄 / 1540 당대 신앙고백

| 논점 | 1836 CR III 원 인쇄에서 직접 본 위치 | 1988 BDS 6/1 온라인 편집 전사 (V3.48) | 1540 Variata CA X 실제 원 인쇄 (V3.46.1) |
|---|---|---|---|
| 성찬의 두 요소 | 75단 `terrena et coelesti` | p.120 | 제10조에는 설명 없음 |
| 빵·포도주와 함께 | 75단 `cum pane et vino` | p.120 | **같은 어휘 있음** |
| 실제 임재·제공 | 75단 `vere et substantialiter adesse, exhiberi et sumi` | p.120 | `vere exhibeantur` (짧게 표현) |
| 성례적 결합 | 75단 `sacramentali unione` | p.122 | 제10조 단문에 상세 논증 없음 |
| 국소적 봉입·지속 결합 | 75–76단에서 구분 | p.122 | 제10조 단문에 상세 논증 없음 |
| 불합당한 수찬자 | 76단 `etiam indignis`, `ad iudicium` | p.124 | 제10조 단문에 명시적 상세 논증 없음 |
| 서명·날짜 | 76–78단 목록 및 29 May | 비평 서지의 28/29일 충돌 | 1540 제10조의 인쇄 연도만 확인 |

이 대조는 **1836 원 인쇄와 1988 비평 편집 전사의 핵심 논점이 대체로 부합한다**는 범위의 판정이다. 전사 문장 전체의 글자 단위 일치, 16세기 필사본의 교감, 1540 저자의 내면 동기까지 인증한 것은 아니다.

## 5. 웹앱용 중(中) 수준 해설 초안 — 공개하지 않음

### 1536년 합의와 1540년 고백, 같은 말은 같은 뜻일까요?

1536년 비텐베르크에서 여러 개신교 신학자는 성찬을 어떻게 설명할지 논의했습니다. 이들은 그리스도의 몸과 피가 빵과 포도주와 함께 참으로 주어진다는 표현을 사용했습니다. 그러나 단지 한 문장만 정한 것은 아닙니다. 성례와 집례자, 성찬에 참여하는 사람의 문제도 함께 논의했습니다.

우리가 직접 확인한 1836년 학술판은 이 합의문을 세 조항으로 기록하며, 서명자의 명단도 보여줍니다. 나중에 1540년 개정된 아우크스부르크 신앙고백 제10조는 여기서 사용하는 중요한 표현 일부를 짧게 사용합니다. 이 점은 두 문헌의 역사적 연결을 설명할 근거가 됩니다.

다만 여러 조항으로 된 합의를 한 문장에 요약했다고 해서, 합의문의 다른 논점이 모두 사라졌거나 부정되었다고 단정할 수는 없습니다. 또한 실제 판본이 달라진 사실과 후대 편집자의 해석도 서로 구별해야 합니다.

**독자 탐색 질문:** 교회의 일치를 위해 공통 문장을 선택할 때, 어떤 내용을 그대로 담고 어떤 논점은 설명을 줄이게 될까요?

## 6. 재현성·보호 게이트

- [x] 1836 CR III **단수 75–78 / IIIF scan 62–63**의 일대일 좌표 직접 확인. 두 단이 한 페이지라는 구조 증명.
- [x] `No. 1429`, `Formula Concordiae`, 29 Maii, I·II·III, 서명자 및 세례/사죄 논점 경계 직접 판독.
- [x] 인용 핵심 6개 어휘를 1988 BDS 6/1 온라인 편집 전사와 대조.
- [x] V3.46.1의 1540 CA X 직접 원 인쇄 3개 소장본 교감과 연결.
- [ ] CR III 본문과 BDS 6/1의 **모든 원문 문자·비평 이문**을 정밀 교감한 것은 아님.
- [ ] **1536년 필사 원본 한 점 이상** 직접 이미지 판독 및 날짜/서명 사료 검증은 미완료.
- [ ] 현장 수용사·지역별 승인 과정의 독립 문서 심사 및 출판 심사 미완료.
- [ ] 출판 승인 전 **513편 원고·main·Google AI Studio 웹앱·외부 배포 변경 금지**.

**최종:** `CR_1836_PRINT_COLUMNS_75_78_DIRECT_VISUAL_CONFIRMED`, `1536_AUTOGRAPH_NOT_READ`, `BDS_SELECTED_TERMS_CORROBORATED`, `PUBLICATION_HOLD`.
