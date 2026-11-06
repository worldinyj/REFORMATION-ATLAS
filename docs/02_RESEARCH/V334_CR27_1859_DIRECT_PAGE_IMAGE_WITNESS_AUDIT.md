# 종교개혁 ATLAS — V3.34 1859년 『Corpus Reformatorum』 제27권 실제 인쇄면 대조

> **MEDIUM · DRAFT · 출판 HOLD.** V3.33의 학술 주석을 통한 라틴어 부분 인용을 실제 1859년 비평판 인쇄면으로 확인한 단계. **1530년 독일어 낭독 원고 및 1573년 라틴어 초판을 직접 판독한 것은 아니다.**

## 1. 핵심 판정

뉴욕공공도서관 소장본을 구글이 디지털화한 **1859년 『Corpus Reformatorum』 XXVII**의 공개 PDF(360쪽)를 GitHub Actions 실행 환경에서 받아 SHA-256을 검증한 뒤 이미지로 렌더링하여 판독했다. **제4조는 인쇄 96열(PDF 70쪽), 제7조는 102~104열(PDF 73·74쪽), 제8조는 105열(PDF 75쪽**에 위치한다. 기존 V3.33의 ‘제4조 99쪽’이라는 기록은 **실제 인쇄 96열로 정정**한다.

1859년 학술 편집본의 직접 판독으로 증거 수준이 한 단계 높아졌다. 그러나 이는 **1859년의 비평판 인쇄면 직접 판독**이지 1530년 원고 또는 1573년 최초 라틴어 출판물의 직접 검증이 아니다. 각주에 나타난 판본 이문은 이번에 일부 확인했지만 전체 독립 사본의 문자 단위 교감은 진행하지 않았다.

## 2. 파일 무결성과 재현 가능한 디지털 원본

| 속성 | 실제 확인된 값 |
|---|---|
| 소장·디지털화 | 뉴욕공공도서관 소장본, Google 디지털화, Internet Archive ID `corpusreformato25melagoog` |
| 원본 디지털 파일 | [Wikimedia Commons PDF](https://upload.wikimedia.org/wikipedia/commons/5/56/Corpus_reformatorum_%28IA_corpusreformato25melagoog%29.pdf) |
| PDF | 360면, 30,637,982바이트 |
| SHA-256 | `ba1995d5587375a13f5298001e7a6c42d68f1c6b161ae86335471a1c4f30b29d` |
| 실물 인쇄연도 | 1859년, 『Corpus Reformatorum』 XXVII |
| GitHub 검증 기록 | `42232566430`, `42232790784`, `42232985301` |
| 별도 소장본 | 바이에른 주립도서관의 342스캔 사본은 별개 디지털 증거이며 이 사본과 직접 화면 교감을 하지 않음 |

## 3. PDF 페이지와 원본 인쇄 열 번호의 대응표

| PDF 1부터 센 페이지 | PDF 0부터 센 번호 | 실제 책 왼쪽 열 | 실제 책 오른쪽 열 |
|---:|---:|---:|---:|
| 69 | 68 | 93 | 94 |
| 70 | 69 | 95 | 96 |
| 71 | 70 | 97 | 98 |
| 72 | 71 | 99 | 100 |
| 73 | 72 | 101 | 102 |
| 74 | 73 | 103 | 104 |
| 75 | 74 | 105 | 106 |
| 76 | 75 | 107 | 108 |

**인용 규칙:** 독자에게 역사 서적의 위치를 제공할 때는 **'1859년 제27권 인쇄 열 번호'**를 먼저 제시하고 PDF 쪽 번호는 뒤에 병기한다. Google Books의 검색 인용에서 표시한 숫자를 직접 서적의 열 번호로 취급하지 않는다.

## 4. 실제 인쇄면에서 확인한 라틴어 구절

| 기록 | 신앙고백 조항 | 라틴어 핵심 구절 | 인쇄본 위치 | 검증 등급 |
|---|---|---|---|---|
| `V334-F1` | IV | *Gratia Dei praevenit voluntatem* | 제27권 96열 · PDF 70쪽 | `1859_CR27_PRINT_DIRECT` |
| `V334-F2` | VII | *non potest citra fidei praeiudicium admitti* | 제27권 102열 · PDF 73쪽 | `1859_CR27_PRINT_DIRECT_CONTINUES_COL103` |
| `V334-F3` | VII | *rituum varietatem non dissecare fidei unitatem* | 제27권 104열 · PDF 74쪽 | `1859_CR27_PRINT_DIRECT` |
| `V334-F4` | VIII | *acceptatur cum sancta romana ecclesia* | 제27권 105열 · PDF 75쪽 | `1859_CR27_PRINT_DIRECT` |

### 본문 해석의 주의 사항

제4조의 ‘하나님의 은총이 의지에 앞선다’는 말은 가톨릭 반박문에서도 **은총의 주도적 역할을 인정**한다는 직접적인 근거다. 제7조는 반대 문구가 **102열 말미에서 103열 첫머리로 연결**되고, 조건을 잘라내면 교회론의 입장을 왜곡한다. 제8조의 *acceptatur*라는 긍정 동사는 수용을 뜻하며, 성례 효력에 관한 가톨릭의 동의점을 명시한다.

## 5. 기존 V3.33의 정정 이력 — 원본 보존

| 정정 카드 | 이전 내용 | 실제 검증 후 표기 | 처리 |
|---|---|---|---|
| `V334-C1` | CR XXVII (1859) printed p99 / Google Books popular passage | CR XXVII (1859) printed column 96 / NYPL PDF 1-based page 70 | `CORRECT_FALSE_PRINTED_PAGE_LOCATOR` |
| `V334-C2` | CR XXVII col102 quoted by 2026 commentary | CR XXVII col102 with sentence continuing across col103 / PDF pages 73–74 | `ADD_REQUIRED_CROSS_COLUMN_CONDITION` |
| `V334-C3` | CR XXVII col104 mediated by CPH scholarly footnote | CR XXVII col104 / NYPL 1859 scan PDF page 74 | `UPGRADE_TO_1859_PRINT_VISUAL` |
| `V334-C4` | CR XXVII col105 mediated by CPH scholarly footnote | CR XXVII col105 / NYPL 1859 scan PDF page 75 | `UPGRADE_TO_1859_PRINT_VISUAL` |
| `V334-C5` | 1859 CR27 directly seen historical pages: zero | 1859 direct visibly inspected claim-supporting PDF pages 70,73,74,75 (4); 1530/1573 pages remain zero | `SUPERSEDE_WITNESS_LEVEL_NOT_MUTATE_PARENT` |

V3.33의 JSON/보고서를 조용히 수정하거나 삭제하지 않고, V3.34에서 **이전 근거와 바뀐 판단의 대응관계**를 명시했다. 특히 V3.33의 직접 인쇄면 판독 0건은 당시에는 사실이었으며, 이를 소급해서 허위로 바꾸지 않는다. 이번에 새로 읽은 인쇄면을 V3.34의 별도 근거로 기록했다.

## 6. 직접 판독의 해석상 발견 7건

- **`V334-O01` — `CORRECT_GRACE_LOCATOR`**: Google Books shows Page 99 but historical 1859 print locates Article IV grace passage on printed column 96 / PDF page 70. (PDF 70쪽)

- **`V334-O02` — `VII_CROSS_COLUMN_CONDITION`**: The Article VII refusal begins printed column 102 and crucial 'if bad or sinful people are excluded' continuation appears at start of column 103. (PDF 73, 74쪽)

- **`V334-O03` — `VII_PARTICULAR_AND_GENERAL_RITES`**: Printed col104 commends diversity in particular local rites, but disagrees with extending this claim to universal rites. (PDF 74쪽)

- **`V334-O04` — `VIII_AFFIRMATIVE_ACCEPTANCE`**: Printed col105 positively accepts Article VIII despite a minister's personal wickedness. (PDF 75쪽)

- **`V334-O05` — `HUSS_WYCLIFFE_POLEMIC`**: Col105 attributes errors to Wycliffe and Hus: a claim made by the Confutatio authors, NOT an independently supported modern historical classification. (PDF 75쪽)

- **`V334-O06` — `EDITION_VARIANT_FOOTNOTES`**: The 1859 historical text has numerous critical manuscript/edition footnotes, directly visible but NOT exhaustively transcribed or evaluated. (PDF 70, 73, 74, 75쪽)

- **`V334-O07` — `NOT_FIRST_PRINT_SOURCE`**: Directly seen folios belong to a scholarly 1859 edition, not the 1530 German public reading or 1573 first Latin printing. (PDF 70, 73, 74, 75쪽)

## 7. 중간 깊이 역사 해설 4편·12절

### 1. 제4조의 은총과 행위: 96열에서 확인한 논쟁

#### 반박문이 인정한 은총의 선행성

『Corpus Reformatorum』 제27권 1859년 인쇄 96열의 실제 이미지를 확인하면 가톨릭 반박문은 은총이 인간 의지에 앞서며 의지를 움직이고 완성한다고 설명한다. 이를 통해 선행이 하나님 앞에서 가치와 공로를 지닐 수 있다는 논리를 전개한다. 가톨릭 측이 은총 없이 자기 힘으로 구원받는다는 주장을 가르쳤다고 단순화하면 이 인쇄된 주장과 충돌한다.

#### 그리스도를 믿는 믿음과 선행의 공로 사이

같은 96열은 믿음과 그리스도의 역할을 인정하면서도 성경이 선한 행위에 대한 상급을 말한다는 점을 강조한다. 따라서 양측의 차이는 선행의 필요성 자체보다는 은총으로 이루어지는 행위가 칭의 또는 영생의 공로와 어떤 관계를 맺는지에 있다. 종교개혁 이후에 만들어진 구호를 그대로 끼워 맞추기보다 당시 저자의 논거를 먼저 읽어야 한다.

#### 99라는 웹 표시와 96이라는 인쇄 열 번호

V3.33의 Google Books 검색은 이 문장을 ‘Page 99’에 배치하는 것처럼 보였다. 하지만 이번 뉴욕공공도서관/구글 디지털화 인쇄본의 PDF 70번째 화면에는 좌우 인쇄 번호 95와 96이 명시되어 있고, 은총 관련 문장은 오른쪽 96열에 있다. 따라서 V3.33의 위치 표시는 별도 정정 카드로 수정하며 과거 계약 데이터를 몰래 변경하지 않는다.

### 2. 제7조 교회: 조건절은 열 경계를 넘는다

#### 102열의 거부 문구만 인용하면 생기는 오해

1530년 반박문의 제7조가 교회를 성도들의 모임으로 규정한 표현에 이의를 제기하는 사실은 1859년 인쇄본 102열에서 확인된다. 그러나 문장의 핵심 조건은 다음 화면의 103열 첫 부분에 이어진다. 악인과 죄인을 외적인 교회 공동체에서 분리한다는 뜻이라면 받아들일 수 없다는 조건이 붙는 것이다. 열 경계를 무시하면 조건부 반대가 전체 교회 정의에 대한 절대적 반대로 바뀐다.

#### 눈에 보이는 교회와 악인·위선자의 존재

반박문 제7조는 가시적인 교회 조직 안에도 선한 사람과 악한 사람이 함께 있을 수 있다는 성경적 비유를 전개한다. 이것은 당시 가톨릭 신학자들이 교회와 성례의 현실적 조건을 어떻게 이해했는지를 보여 준다. 반면 멜란히톤의 변증서는 참된 영적 교회와 외적인 공동체를 구별해 자기 측 표현을 해명한다. 두 문헌은 같은 단어를 사용하면서 그 외적 범위에서 다투었다.

#### 104열의 한정된 예식 다양성

1859년 인쇄 104열은 지역별 특별한 예식의 다양성이 신앙의 일치를 무너뜨리지는 않는다는 판단을 긍정적으로 논의한다. 그러나 이 논리를 모든 교회가 지켜야 하는 보편적 예식까지 무제한 적용하는 것은 반대한다. 이 지점을 통해 교회 일치의 기준을 한 문장으로만 설명할 수 없고, 특수한 의식과 보편적 관행이라는 구별을 함께 보여 주어야 함을 확인한다.

### 3. 제8조 수용과 비난의 언어를 분리한다

#### 105열에서 확인되는 명시적인 수용

1859년 편집본 제8조의 시작 부분인 105열은 악한 성직자의 죄 때문에 그가 집례하는 말씀과 성례의 효력이 사라진다는 생각을 받아들이지 않으며, 신앙고백 제8조의 해당 주장 자체를 가톨릭 측이 수용한다는 동사를 쓴다. 이는 단지 현대 영어 번역이나 스페인어 주석만의 해석이 아니라, 이번에는 원어 인쇄 문맥에서 직접 확인된 사실이다.

#### 위클리프와 후스에 대한 평가는 반박문의 논쟁적 비난

제8조의 이어지는 문장에서 가톨릭 반박문 저자들은 도나투스파의 오류를 비난하면서 위클리프·후스 등의 이름을 거론한다. 이 표현은 저자가 자신의 논적을 분류하려고 사용한 공격적 규정이다. 오늘날 역사 연구의 공인된 판정으로 옮겨 쓰면 출처를 오독하게 된다. 독자용 글에는 반드시 ‘당시 반박문은 그들을 그렇게 비난했다’라는 주체를 밝혀야 한다.

#### 편집 각주와 본문은 같지 않다

1859년 비평판 105열 하단에는 여러 역사 원고 또는 이전 간행본 사이의 차이를 제시하는 편집 각주가 존재한다. 이것은 본문의 독립성과 문헌 전승의 복잡성을 보여 주지만, 현재 확인한 것은 각주가 있다는 사실과 일부 항목의 분리뿐이다. 전체 이문을 단어별로 대조한 것도 아니고 1530년 독일어 낭독문의 완전한 재구성을 마친 것도 아니다.

### 4. 사료 판독의 등급: 1859년 실물 스캔과 1530년 낭독 원고

#### 이번에 새롭게 직접 판독한 자료의 정체

이번 작업은 1859년 『Corpus Reformatorum』 제27권의 공개 디지털 사본을 직접 내려받아 정확한 파일 해시를 기록하고 이미지로 펼쳐 읽는 방법을 사용했다. 360쪽짜리 PDF 안에서 인쇄된 열 번호를 확인하여 96·102·103·104·105열을 재현할 수 있는 위치에 고정했다. 이전에는 학술 주석에서 간접 확인하던 핵심 라틴어 표현을 1859년 학술 편집본의 실제 인쇄면에서 확인했다는 점에서 검증 수준이 개선됐다.

#### 1859년 비평판이 1530년 낭독문 자체인 것은 아니다

당대 가톨릭 반박문은 1530년 제국의회에서 독일어로 낭독되었으나 라틴어 전문의 첫 간행은 역사 연구에 따르면 1573년이었다. 1859년 제27권은 훨씬 뒤에 여러 자료를 대조하고 비평적 각주를 붙여 출판된 책이다. 그러므로 1859년의 라틴어 문장을 직접 읽었다는 사실과 1530년 낭독 현장의 실제 독일어 단어를 직접 확인했다는 주장은 분명히 다르다.

#### 검증을 이어갈 차기 문헌 관계

다음 단계에서는 1573년 최초 라틴어 인쇄본과 1859년 편집본의 제4·7·8조 문장을 대조할 필요가 있다. 그리고 가능하면 1530년 독일어 공적 낭독의 자료 전승을 별도로 확인해야 한다. 1859년 각주에 표시된 문헌 약칭을 해독하면 변증서 편찬 과정에서 누가 어떤 문장을 접했을지를 더 세밀하게 추적할 수 있을 것이다. 그런 후 성인 공경 제21조와 미사 제24조도 같은 기준으로 확장한다.

## 8. 출처 및 근거 수준

| 출처 | 사용 방법 |
|---|---|
| [V334-S-NYPL1859](https://commons.wikimedia.org/wiki/File:Corpus_reformatorum_(IA_corpusreformato25melagoog).pdf) | `DIGITIZED_1859_PRINT_DIRECTLY_SEEN` — 1859 edited CR27 printed columns visibly read in NYPL/Google scanned book |
| [V334-S-NYPLPDF](https://upload.wikimedia.org/wikipedia/commons/5/56/Corpus_reformatorum_%28IA_corpusreformato25melagoog%29.pdf) | `HASH_VERIFIED_1859_PRINT_PDF` — 360-page 30,637,982-byte PDF; SHA256 verified with GitHub Actions |
| [V334-S-BSB](https://www.digitale-sammlungen.de/de/details/bsb10360389) | `INDEPENDENT_COPY_CATALOGUE_ONLY` — 1859 CR27 Bavarian library 342 images; different digitization, not directly examined |
| [V334-S-GOOGLE](https://books.google.com/books/about/Philippi_Melanthonis_Opera_quae_supersun.html?id=TMjLpAOy2zYC) | `GOOGLE_BOOKS_INDEXED_QUOTE` — Internet popular passage marked page 99, differing from original printed column 96 |
| [V334-S-CPH](https://bookofconcord.cph.org/es/apologia-confesion-augsburgo/articulos-vii-y-viii-la-iglesia/) | `MODERN_EDITORIAL_NOTES` — Footnotes 169/181/184/189 cite CR27 102,104,105; independently crosschecked on 1859 image |
| [V334-S-REUIV](https://thebookofconcord.org/roman-confutation/article-iv/) | `MODERN_ENGLISH_TRANSLATION` — Article IV rendering and context, not original manuscript |
| [V334-S-REUVII](https://thebookofconcord.org/roman-confutation/article-vii/) | `MODERN_ENGLISH_TRANSLATION` — Article VII English witness, not original manuscript |
| [V334-S-REUVIII](https://thebookofconcord.org/roman-confutation/article-viii/) | `MODERN_ENGLISH_TRANSLATION` — Article VIII English witness, not original manuscript |
| [V334-S-SCHAFF](https://www.ccel.org/ccel/schaff/hcc7/hcc7.ii.ix.iv.html) | `LATER_EDITION_BIBLIOGRAPHY` — 1573 first Latin full printing reported by historical scholar |

## 9. 후속 원본 검증 대기 목록

- **P0 · `V334-I1` · 1573_FABRICIUS_FIRST_LATIN**: Identify the actual 1573 full Latin Confutatio book and directly check IV VII VIII alongside 1859 print

- **P0 · `V334-I2` · 1530_GERMAN_READING_WITNESS**: Locate attested German manuscript sources of imperial oral reading and publication genealogy

- **P0 · `V334-I3` · CR27_APPARATUS_COMPLETE**: Transcribe and classify the variant notes for 1859 printed columns96,102-105

- **P1 · `V334-I4` · BSB_INDEPENDENT_COPY**: Compare BSB 342-scan digital witness independently of NYPL PDF 360 pages

- **P1 · `V334-I5` · MELANCHTHON_APOLOGY_1531**: Read early 1531 Latin Apology text responding to IV VII VIII

- **P1 · `V334-I6` · CONFUTATIO_SAINTS_XXI**: Extend direct Latin printed column check to 1530 Confutatio XXI

- **P1 · `V334-I7` · CONFUTATIO_MASS_XXIV**: Extend direct Latin printed column check to 1530 Confutatio XXIV

- **P1 · `V334-I8` · AUGSBURG_CONFESSION_DUAL_LANGUAGE**: Separate 1530 Augsburg German/Latin submissions and later editings

- **P1 · `V334-I9` · LATIN_KOREAN_LINE_BY_LINE**: Review exact Korean translation of short Latin fragments with qualified philologist

## 10. 근거 과장 방지와 배포 경계

- Google Books 99 was the printed location of Article IV grace phrase

- 1859 printed CR27 is the 1530 German public-reading manuscript

- The 1573 full Latin first printing has been visually compared to CR27

- Article VII rejected the entire church definition without any conditional clause

- Article VII permitted all universally required liturgical rites to vary freely

- Article VIII rejected the wicked-minister sacrament-validity article

- Confutatio polemical claims about Hus and Wycliffe are independently verified historical facts

- 1859 editorial apparatus was exhaustively collated

**이번 개선은 출판 승인과 다르다.** 기존 종교개혁 ATLAS의 513편·1,539절 및 원래 근거 723건·개요 97건을 변경하지 않았고, `main` 또는 별도로 개발하는 Google AI Studio 웹앱에 병합·탑재하지 않았다. 연구 자료는 V3.34 Draft PR에서만 관리한다.
