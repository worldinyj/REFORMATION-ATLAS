# V3.36 — 1573년 파브리키우스 문헌집의 신앙고백·반박문 전승 분리

> **MEDIUM · DRAFT · 출판 HOLD.** 1573년 원본 내부 인쇄면 직접 판독은 여전히 **0쪽**이다. 이번에는 하인리히 보른캄의 1956년 문헌비평 논문(1980년 변화 없는 재판) **인쇄 10·14·15쪽을 실제 화면으로 판독**하고, 1573년 *Confessio Augustana* 전승과 *Confutatio* 전승을 분리했다.

## 1. 이번 연구의 결정적 발견

**1573년 파브리키우스의 『Harmonia Confessionis Augustanae』에는 서로 다른 전승의 두 문헌이 공존한다.** 첫째는 1530년 루터파 신앙고백 자체를 재현한 라틴어 텍스트이고, 둘째는 가톨릭 신학자들이 그 신앙고백에 응답한 *Confutatio*다. 원래 신앙고백은 후대 『Corpus Reformatorum』 **제26권(1858)**의 교감 대상이며, 반박문은 **제27권(1859)**의 교감 대상이다. 이 둘을 뒤섞으면 1573년 책에서 누구의 목소리가 어느 문장에 나타나는지 역사적으로 구별할 수 없다.

보른캄은 파브리키우스가 수록한 **신앙고백의 라틴어 본문**을 다른 사본들과 구별되는 **독립적인 문헌 증인**으로 평가했지만, 편집적 순서 변경과 오류 때문에 다른 원고 계열보다 신뢰도를 낮게 평가한다. 이는 파브리키우스 문헌집 전체를 진본이라고 확정한 판단이나, 그 안의 *Confutatio*가 1530년 낭독문 그대로라고 주장한 판단이 아니다.

## 2. 1530년 신앙고백 텍스트의 전승

| 증인 ID | 연도 | 정확한 문헌 역할 |
|---|---:|---|
| `V336-N01` | 1530 | **AUGUSTANA_LATIN_SUBMITTED_ORIGINAL** — Original submitted Confession copy once in Brussels imperial archive; per 1956 Bornkamm no longer extant/located. |
| `V336-N02` | 1566 | **BRUSSELS_AUTHENTICATED_LATIN_TRANSCRIPT_CHAIN** — Vatican transcript certified 1566 Brussels, 1568 Vienna, transmitted to Rome. Witness V derivative. |
| `V336-N03` | 1596 | **CANISIUS_HUENFELD_COPY** — Hü manuscript associated with Canisius; copy through intermediate document, dated inscription 1596. |
| `V336-N04` | 1530 | **BISHOP_MANUSCRIPT_KRSW_GROUP** — Karlsruhe, Regensburg, Salzburg, Würzburg manuscripts, common intermediate exemplar identified through shared mistakes. |
| `V336-N05` | 1573 | **FABRICIUS_PRINTED_AUGUSTANA** — Fabricius included a Latin version of the *Augsburg Confession*, distinct independent textual family with unsystematic rearrangements and unknown exact exemplar. |
| `V336-N06` | 1573 | **FABRICIUS_FIRST_FULL_LATIN_CONFUTATIO_PUBLICATION** — Schaff identifies Roman Confutatio first full Latin print in same 1573 Harmonia volume; exact internal folio unseen. |
| `V336-N07` | 1577 | **COELESTIN_REPRINT_OF_FABRICIUS_AUGUSTANA** — Bornkamm printed p10 note22 says Georg Coelestin in *Historia comitiorum* (1577) reprinted Fabricius's *Augsburg Confession* text. |
| `V336-N08` | 1587 | **FABRICIUS_SECOND_EXPANDED_EDITION** — Second 1587 edition of Harmonia, separate collation and exact Latin paragraphs unexamined. |
| `V336-N09` | 1597 | **COELESTIN_LATER_BOOK_POSSIBLE_DEPENDENCE** — Older ADB comments Coelestin 1597 text and Fabricius, but source's identity and exact relationship unverified, not 1577 book. |
| `V336-N10` | 1858 | **CR26_LATIN_AUGUSTANA_COLLATION_1858** — CR XXVI (1858) printed cols226ff and 263ff cited by Bornkamm for Latin Augsburg Confession source comparison. University editorial derivative text online; actual 1858 printed scan not read. |
| `V336-N11` | 1859 | **CR27_LATIN_CONFUTATIO_CRITICAL_TEXT** — CR XXVII Latin Roman Confutatio col96,102–105 directly checked in V3.34; distinct from CR XXVI. |

바티칸 V와 휜펠트 Hü 사본, KRSW라는 네 주교 소장 필사본 그룹, 파브리키우스의 라틴어 신앙고백 텍스트가 독립적인 가치가 있다는 것은 **같은 종교개혁 문헌을 복원할 때 각 증언의 계보와 품질을 구분해야 한다**는 뜻이다. KRSW의 네 사본에 공통된 오류가 있다면 네 개의 독립적인 정확한 증인으로 모두 계산하지 않는다.

## 3. 출처·관계 그래프

| 관계 | 문헌 출발 → 도착 | 역사적 연결의 수준 |
|---|---|---|
| `IMPERIAL_CONFESSION_COPY_CHAIN` | `V336-N01` → `V336-N02` | Evidence of 1566 certified archival transcript, by Bornkamm, not surviving Brussels original scan |
| `DISTINCT_IMPERIAL_CONFESSION_COPY_CHAIN` | `V336-N01` → `V336-N03` | Hünfeld associated Canisius copy via intermediate source, 1596 note, not lineally identical with Vatican copy |
| `COMMON_INTERMEDIATE_BISHOPS_GROUP` | `V336-N01` → `V336-N04` | KRSW share characteristic errors by intermediate exemplar rather than four independent exact lines from emperor original |
| `INDEPENDENT_CONFESSION_PRINT_WITNESS_PROVENANCE_UNKNOWN` | `V336-N01` → `V336-N05` | Bornkamm judges 1573 Fabricius Confession text an independent family; possible Brussels-line copy but source unknown and not direct original |
| `REPRINT_OF_FABRICIUS_CONFESSION_TEXT` | `V336-N05` → `V336-N07` | Bornkamm footnote p10 says Coelestin 1577 reprinted Fabricius 1573 Confession text, not proven first full Latin Confutatio reprint |
| `BIBLIOGRAPHIC_FIRST_FULL_LATIN_CONFUTATIO_PUBLICATION` | `V336-N06` → `V336-N11` | Schaff reports 1573 first Latin full Confutatio; 1859 is later critical print of Confutatio, no original Latin sentence pair compared |
| `CR26_CONFESSION_COLLATION_REFERENCE` | `V336-N05` → `V336-N10` | CR XXVI (1858) col226ff and263ff are Latin *Augsburg Confession* variant collations, NOT CR XXVII (1859) Catholic Confutatio |
| `UNVERIFIED_LATER_COELESTIN_RELATION` | `V336-N05` → `V336-N09` | Older ADB 1597 relation is distinct from Bornkamm 1577 precise reprint; provenance unresolved, not first edition witness |
| `REVISED_COLLECTION_1587` | `V336-N05` → `V336-N08` | 1587 printed second Harmonia edition follows 1573, edition is expanded per title, exact content variation uncollated |
| `SAME_VOLUME_DIFFERENT_WORKS` | `V336-N05` → `V336-N06` | 1573 *Augsburg Confession* copy and *Roman Confutatio* response belong to same Fabricius collection, but separate authorships/textual histories and should never merge |

### 1577년과 1597년의 구별

보른캄의 **인쇄 10쪽 각주 22**는 파브리키우스의 **신앙고백 본문**이 게오르크 쾰레스틴의 『Historia comitiorum』(1577)에 재수록되었다고 명시한다. 이전 V3.35가 추적한 **1597년판**에 관한 오래된 독일어 전기의 주장은 별도 역사 검토 과제다. 두 연도를 하나로 합치거나 1577년 재수록이 당연히 가톨릭 **반박문** 전문을 재출판한 사건이라고 기록하지 않는다.

## 4. 제26권(1858)과 제27권(1859)의 물리적 구별

| 문헌집 | 간행연도 | 텍스트 | 이번에 실제 접근한 범위 |
|---|---:|---|---|
| 『Corpus Reformatorum』 **XXVI** | **1858** | 루터파 『아우크스부르크 신앙고백』 라틴어 전승·비평 | SLUB 대학 도서관의 간행 서지와 CR26에 근거한 Bibliotheca Augustana의 현대 HTML 전사, **1858년 실제 인쇄 이미지 0쪽** |
| 『Corpus Reformatorum』 **XXVII** | **1859** | 가톨릭 『반박문』 라틴어 전승·비평 | V3.34에서 **1859년 인쇄 96·102~105열을 직접 이미지 판독**, 기존 연구에서 읽은 결과를 이번에 보존 |

보른캄 인쇄 10쪽 각주 22에는 제26권의 **226열 이후·263열 이후**에 파브리키우스 신앙고백 본문의 관련 이문을 대조할 수 있다는 지시가 있다. 이것은 제27권의 반박문 96·102~105열과 **전혀 다른 대상**이므로 원문 관계를 그릴 때 반드시 두 종류의 노드로 관리한다.

## 5. 디지털 전사본의 라틴어 품질 검사

현대 온라인 전사인 Bibliotheca Augustana는 제26권(1858) **263~336쪽**에 기초했다고 표기하며 신앙고백 제4·7·8조를 제공한다. 하지만 다음 글자 표기는 다른 라틴어 전사와 일치하지 않는다. **이번에는 원본 1858년 인쇄 이미지를 직접 보지 않았으므로, 역사적 이문인지 HTML 편집·입력 오류인지 아직 확정하지 않는다.**

| 조항 | 검토한 온라인 표기 | 다른 라틴어판에서 보이는 표기 | 판정 |
|---|---|---|---|
| IV | `gratis iustificenter` | `gratis iustificentur` | **원본 확인 대기** |
| VII | `consentiere` | `consentire` | **원본 확인 대기** |
| VIII | `malii / sentibant` | `mali / sentiebant` | **원본 확인 대기** |

이와 같은 오류 의심 사례를 바로 1530년 당대의 원어 차이로 기록하면 편집상의 실수가 역사적 사실로 바뀐다. ATLAS의 한국어 전문에 라틴어 한 글자를 인용할 때도 **어느 판본의 글자인지** 추적하도록 한다.

## 6. 근거 카드 15건

| 카드 | 주장 | 출처 |
|---|---|---|
| `V336-C01` | Bornkamm states submitted 1530 German/Latin Confession originals could not be located, and reconstructs via copies, not zero manuscript tradition. | V336-S01 |
| `V336-C02` | He describes a certified Brussels Confession copy (1566, later 1568 Vienna), whose witnessed oath text is quoted and page visually seen in modern paper. | V336-S02 |
| `V336-C03` | Hü copy linked to Canisius and note dated 1596, derivative chain not necessarily same scribe as Vatican V. | V336-S01, V336-S03 |
| `V336-C04` | KRSW bishop manuscript family has common intermediate exemplar and shared omissions, cannot count as four independent direct originals. | V336-S03 |
| `V336-C05` | Bornkamm print p14-15 identifies Fabricius's Latin Augsburg Confession text as independent from both Hü,V and KRSW but with many rearrangements and unknown provenance. | V336-S03 |
| `V336-C06` | Bornkamm gives greater evidentiary value to Hü and V than to Fabricius in reconstruction; not all independent witnesses have equal text-critical trust. | V336-S03 |
| `V336-C07` | Footnote22 printed p10 says 1573 Fabricius *Confession* text reprinted by Georg Coelestin 1577, not automatically Roman Confutatio reprint. | V336-S04 |
| `V336-C08` | Footnote22 points to CR 26 columns226ff and263ff for *Confession* readings; separately verified CR27 cols96/102-105 concern Catholic *Confutatio*. | V336-S04, V336-S08 |
| `V336-C09` | Bornkamm says Fabricius probably had Brussels-line 1530 Confession copy; this is his likelihood assessment, not direct traceable source chain. | V336-S01, V336-S03 |
| `V336-C10` | Schaff's 1573 first full Latin Confutatio is a retrospective bibliography of a different text domain; not the same as Bornkamm's claim about Fabricius's Latin Confession witness. | V336-S07, V336-S03 |
| `V336-C11` | Older German biography 1597 Coelestin derivative warning is a distinct later publication issue, not proof 1577 was 1597. | V336-S14, V336-S04 |
| `V336-C12` | Despite library 1573 bibliographic proof, direct 1573 internal page and 1573-vs-1859 original Latin collation remain zero. | V336-S05, V336-S06, V336-S11 |
| `V336-C13` | SLUB Dresden confirms CR XXVI printed in 1858 while CR XXVII printed in 1859. Do not assign 1859 to both volumes. | V336-S15 |
| `V336-C14` | Bibliotheca Augustana online AC IV,VII,VIII explicitly draws on CR XXVI 1858 pp263-336, but these online HTML texts are not direct images of the 1858 book. | V336-S16, V336-S17, V336-S18, V336-S19 |
| `V336-C15` | Online iustificenter/consentiere/malii/sentibant anomalies require comparison with CR26 1858 print before being classified as actual sixteenth-century textual variants. | V336-S17, V336-S18, V336-S19 |

## 7. 중간 깊이 역사 해설 — 3편·9절

### 1. 1530년 서명된 라틴어 신앙고백은 어떻게 전해졌는가

#### 찾을 수 없는 원고와 살아남은 간접 필사본

1530년 제국의회에 제출한 신앙고백의 독일어·라틴어 원본은 오랫동안 찾아지지 않았다. 1956년 하인리히 보른캄의 문헌비평 연구는 이를 이유로 황제 측과 가톨릭 측에 남았던 간접 필사본을 면밀히 검토했다. 원고가 실종되었다는 말은 당시 문장이 전혀 전승되지 않았다는 뜻은 아니다. 보른캄의 연구는 실물 원고의 현존 여부와 문장 재구성의 신뢰도를 구별한다.

#### 브뤼셀 황제 문서에서 바티칸과 휜펠트까지

보른캄은 황제의 브뤼셀 보관 문서에서 만들어진 여러 사본을 추적한다. 바티칸 계열 사본은 1566년 브뤼셀에서 공증된 사본과 1568년 빈에서의 인증을 거친 전승으로 소개된다. 다른 사본은 페트루스 카니시우스와 관계된 휜펠트 소장 계열이다. 이러한 사본은 하나의 분실된 원고에서 멀고 가깝게 파생했을 수 있지만, 같은 계열이라는 이유로 전부 같은 정확도와 독립성을 갖는 것은 아니다.

#### 주교 문서 KRSW와 공통된 필사 오류

카를스루에·레겐스부르크·잘츠부르크·뷔르츠부르크로 표시하는 KRSW 계열은 보른캄이 공통의 중간 사본에서 파생했다고 판단한 필사본 그룹이다. 여러 문서에 같은 누락이나 실수가 반복되는 경우 이를 서로 완전히 독립적인 증언으로 셈할 수 없다. 종교개혁사를 연구할 때 출처 수를 단순 합산하는 대신, 어떤 사본에서 어떤 사본으로 문장이 이동했는지 추적해야 하는 이유가 여기 있다.

### 2. 1573년 파브리키우스 신앙고백 원문이 지닌 양면적 가치

#### 뜻밖의 독립적인 인쇄 전승

파브리키우스는 1573년 『Harmonia Confessionis Augustanae』를 펴내면서 신앙고백의 라틴어 본문과 가톨릭 측 대응 문서를 함께 수록했다. 보른캄은 이 책에 수록된 신앙고백 본문을 다른 주교 필사본 계열과 바티칸·휜펠트 계열에서 직접 복제한 것이 아닌, 별도로 전승된 텍스트 증거로 다룬다. 이 판단은 파브리키우스의 편집본이 당대 신앙고백 원고의 역사에 관한 자료로서 가치를 지닐 수 있다는 뜻이다.

#### 독립성은 무오성을 보증하지 않는다

보른캄은 파브리키우스 텍스트에 여러 임의적 문장 위치 변경과 필사·인쇄상의 작은 오류가 있으며, 직접 어떤 문헌을 사용했는지는 알려져 있지 않다고 명확하게 설명한다. 따라서 출처가 독립적이라고 해서 황제에게 제출된 원고를 정확히 한 글자도 바꾸지 않고 옮긴 것이라고 결론 내릴 수 없다. 그는 신앙고백 본문의 재구성에서 이 자료보다 바티칸과 휜펠트 계열을 더 우선한다.

#### 1577년 재수록과 1597년 후대판을 섞지 않는다

보른캄의 10쪽 각주 22는 게오르크 쾰레스틴이 1577년 『Historia comitiorum』에 파브리키우스의 신앙고백 텍스트를 다시 수록했다고 기록한다. 앞선 V3.35에서 검토한 오래된 전기가 언급하는 1597년판은 별개의 책과 연구 주장으로 취급해야 한다. 1577년과 1597년을 하나의 날짜로 쓰거나, 재수록된 신앙고백을 가톨릭 반박문 전문이라고 잘못 부르면 전승 계보를 크게 왜곡한다.

### 3. 비평판 제26권과 제27권을 왜 따로 읽어야 하는가

#### 같은 1859년 문헌 집성, 다른 연구 대상

1858년에 간행된 『Corpus Reformatorum』 제26권의의 226열과 263열 이후 부분은 파브리키우스가 간행한 아우크스부르크 신앙고백의 라틴어 문장과 관련 판본의 차이를 검토할 수 있는 구역으로 소개된다. 반면 1859년에 간행된 제27권의 96열·102~105열은 가톨릭 신학자들의 반박문인 『Confutatio』에 속한다. 책의 시리즈 제목만 같다고 동일 문헌의 연속된 한 페이지로 처리할 수 없다.

#### 제4·7·8조 대조에서 구분할 두 종류의 원문

예를 들어 신앙고백 제8조는 악한 성직자가 집례했더라도 성례는 유효하다고 주장한다. 반박문 제8조는 바로 그 주장을 받아들인다. 그러나 1573년 파브리키우스 문헌집에는 신앙고백의 문장도 있고 그에 대응하는 가톨릭 반박문도 있으므로, 책에서 어느 쪽 구절을 읽었는지 식별하지 않으면 근거가 뒤바뀐다. 제26권 신앙고백 계열과 제27권 반박문 계열을 분리한 뒤에야 서로 같은 쟁점의 두 화자를 나란히 인용할 수 있다.

#### 원전 대조를 완성하기 위한 다음 기준

현재 1573년 책의 해당 내부 인쇄면은 접근하지 못했으므로 1573년과 1859년의 직접 문장 교감은 이루어지지 않았다. 실제로 원본을 확보하면 먼저 파브리키우스 책의 제목·목차·문단 시작에서 ‘신앙고백’과 ‘반박문’을 구별하고, 각 원전의 라틴어를 해당 1859년판의 바른 권·열과 연결해야 한다. 그 다음에야 작은 철자 차이와 의미 있는 문장 이문을 따로 평가할 수 있다. 인터넷 전사본에는 예를 들어 제4조의 iustificenter, 제7조의 consentiere, 제8조의 malii·sentibant와 같은 특이 표기가 확인된다. 그러나 원래 1858년 인쇄면과 대조하지 않은 웹 전사 표기를 역사적 원전 이문으로 세어서는 안 된다.

## 8. 조사 출처와 검증 등급

| ID | 출처 | 실제 접근·근거 등급 |
|---|---|---|
| `V336-S01` | [Heinrich Bornkamm: Der authentische lateinische Text der Confessio Augustana (1530)](https://www.mgh-bibliothek.de/dokumente/a/a022116.pdf) | `HISTORICAL_TEXT_CRITICISM_PDF_PRINT_PAGES_VISUALLY_INSPECTED` |
| `V336-S02` | [Bornkamm 1956 quoted original-archive transcript testimony](https://www.mgh-bibliothek.de/dokumente/a/a022116.pdf) | `MODERN_HISTORIAN_PRINTED_QUOTATION_FROM_1566_ARCHIVAL_COPY` |
| `V336-S03` | [Bornkamm 1956 four-source ranking](https://www.mgh-bibliothek.de/dokumente/a/a022116.pdf) | `MODERN_SCHOLAR_DIRECT_VISUAL_PRINT_P14_15` |
| `V336-S04` | [Bornkamm 1956 note22 on Fabricius and Coelestin 1577](https://www.mgh-bibliothek.de/dokumente/a/a022116.pdf) | `MODERN_SCHOLAR_DIRECT_VISUAL_PRINT_P10` |
| `V336-S05` | [BnF original 1573 Fabricius imprint](https://catalogue.bnf.fr/ark:/12148/cb304145207) | `NATIONAL_LIBRARY_CATALOGUE_ONLY` |
| `V336-S06` | [Braidense first print 1573 and second 1587](https://opac.bibliotecabraidense.org/opac_braidense/opaclib?db=solr_braidense&do_cmd=search_show_cmd&from=1&item%3A8006%3ATitolo_uniforme%3A%40frase%40=SBL0086576&nentries=10&resultForward=opac%2Fbraidense%2Fbrief.jsp&searchForm=opac%2Fbraidense%2Ferror.jsp) | `NATIONAL_LIBRARY_CATALOGUE_1573_1587_DISTINCT` |
| `V336-S07` | [Schaff history of first full Latin Roman Confutation print](https://www.ccel.org/s/schaff/history/7_ch09.htm) | `RETROSPECTIVE_BIBLIOGRAPHIC_ASSERTION` |
| `V336-S08` | [CR XXVII NYPL 1859 actual Roman Confutatio](https://commons.wikimedia.org/wiki/File:Corpus_reformatorum_(IA_corpusreformato25melagoog).pdf) | `DIRECT_1859_CR27_CONTRADOCUMENT_SCANNED_PRIOR_V334` |
| `V336-S09` | [CR XXVII 1859 original PDF mirror](https://upload.wikimedia.org/wikipedia/commons/5/56/Corpus_reformatorum_%28IA_corpusreformato25melagoog%29.pdf) | `INDEPENDENT_FILE_URL_NOT_INDEPENDENT_TEXT_WITNESS` |
| `V336-S10` | [CR XXVI historical textual collation attested by Bornkamm](https://www.mgh-bibliothek.de/dokumente/a/a022116.pdf) | `SCHOLARLY_FOOTNOTE_ONLY_ORIGINAL_CR26_NOT_READ` |
| `V336-S11` | [V3.35 allowed 1573 PDF retrieval probe](https://github.com/worldinyj/REFORMATION-ATLAS/actions/runs/42321490328) | `ACTUAL_NETWORK_PROBE_LEDGER` |
| `V336-S12` | [Blackwell B172 1573 folio seller catalogue](https://ilab.org/assets/catalogues/catalogs_files_1111_catalogue_b172.pdf) | `RARITY_SELLER_CATALOGUE_PAGE_PREVIOUSLY_SCREENED` |
| `V336-S13` | [Berkeley rare books 1587 enlarged second edition](https://lawcat.berkeley.edu/record/287858) | `UNIVERSITY_LIBRARY_SECOND_EDITION_CATALOGUE` |
| `V336-S14` | [Deutsche Biographie Coelestin older ADB page](https://www.deutsche-biographie.de/gnd122885589.html?language=en) | `OLDER_HISTORIOGRAPHY_CRITICAL_HYPOTHESIS` |
| `V336-S15` | [SLUB Dresden Corpus Reformatorum volume 26 publication date](https://katalog.slub-dresden.de/id/0-168762757) | `UNIVERSITY_LIBRARY_CR26_AND_CR27_DATE_RECORD` |
| `V336-S16` | [Bibliotheca Augustana based on CR26 1858 transcription index](https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca00.html) | `WEB_EDITORIAL_TRANSCRIPTION_CR26_WITH_EXACT_SOURCE` |
| `V336-S17` | [Bibliotheca Augustana CR26 Augsburg Confession Article IV online text](https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca04.html) | `DERIVATIVE_EDITORIAL_LATIN_WEB_TEXT` |
| `V336-S18` | [Bibliotheca Augustana CR26 Augsburg Confession Article VII online text](https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca07.html) | `DERIVATIVE_EDITORIAL_LATIN_WEB_TEXT` |
| `V336-S19` | [Bibliotheca Augustana CR26 Augsburg Confession Article VIII online text](https://www2.hs-augsburg.de/~harsch/Chronologia/Lspost16/Melanchthon/mel_ca08.html) | `DERIVATIVE_EDITORIAL_LATIN_WEB_TEXT` |

이 가운데 보른캄의 논문은 인쇄 10쪽(디지털 0기준 11), 14쪽(15), 15쪽(16)을 직접 이미지로 확인했다. SLUB 서지 및 Bibliotheca Augustana는 웹 텍스트로 읽었다. **CR26의 1858년 인쇄면·1573년 파브리키우스 책의 내부 본문·1577년 및 1597년 쾰레스틴 원본**은 직접 열람하지 않았다.

## 9. 후속 원전 대조 10건

- **P0 `V336-I01` — FABRICIUS_CONFUTATIO_1573_FOLIOS**: Obtain authorized original 1573 *Roman Confutatio* text for IV VII VIII, not the *Augsburg Confession* pages in same volume.

- **P0 `V336-I02` — FABRICIUS_CONFESSION_1573_FOLIOS**: Independently obtain original 1573 *Augsburg Confession* text and its own headings for IV VII VIII, compare to Bornkamm source families.

- **P0 `V336-I03` — CR26_1858_COL226_263_ORIGINAL**: Visually check 1859 CR XXVI printed columns226ff and263ff for Fabricius *Confession* variants. Do NOT cite as Confutatio.

- **P0 `V336-I04` — CR27_1859_CRITICAL_APPARATUS**: Transcribe CR XXVII printed col96/102-105 footnotes and identify which refer to 1573 Fabricius editions, if any.

- **P1 `V336-I05` — HUNFELD_VATICAN_COPY_STEMMA**: Consult 1956 Bornkamm bibliography for V/Hü manuscript descriptions, differentiating manuscript authenticity and scholarly inference.

- **P1 `V336-I06` — KRSW_INDEPENDENCE**: Investigate common KRSW intermediate exemplar and provenance, verify conditional scholarly classification.

- **P1 `V336-I07` — COELESTIN_1577_FIRST_REPRINT**: Confirm 1577 original title, page image and exact object reprinted. Do not silently substitute 1597.

- **P1 `V336-I08` — COELESTIN_1597_DISTINCT_BOOK**: Verify older ADB 1597 claim via direct original book and modern bibliography; don't recategorize 1577 source.

- **P1 `V336-I09` — 1573_VS_1587_CRITICAL_DIFFERENCES**: Find original signed 1573 and 1587 first/second edition book scans and align distinct Confession vs Confutatio loci.

- **P1 `V336-I10` — 1530_ORIGINAL_AFTER_1956**: Check modern post-1956 scholars on lost 1530 submitted originals, avoid treating 1956 status as 2026 discovery guarantee.

## 10. 오독 방지 규칙

- Do not mistake independent Fabricius 1573 AUGSBURG CONFESSION text for the CATHOLIC CONFUTATIO in the same volume

- Do not use 1859 CR26 Confession variant columns as if they were the directly checked 1859 CR27 Confutatio printed columns

- Do not count Hu, V, KRSW (4 manuscripts), Fabricius as seven entirely independent textual witnesses; KRSW shares a common exemplar

- Do not treat Fabricius 1573 independent witness as autograph or textually superior; provenance unknown, rearrangements noted

- Do not treat the 1956 Bornkamm claim of no surviving submitted original as a full current-2026 archival search result

- Do not confuse Coelestin 1577 reprint attested by Bornkamm with later 1597 printing discussed in older ADB

- Do not assume the Latin first full Confutatio 1573 publication date equals date of 1530 public oral German reading

- Do not claim any 1573 original inner folio was directly read or a 1573/1859 exact passage collation accomplished

- Do not promote Bornkamm's notes on Hünfeld manuscript variant spellings to Fabricius-specific original variants

- Do not interpret Schaff, Bornkamm, or ADB independent bibliographic summaries as multiple first-print original images

- Do not label CR XXVI as printed in 1859; university catalogue dates it 1858 while CR XXVII dates to 1859

- Do not promote modern Latin HTML transcription oddities iustificenter, consentiere, malii or sentibant to historical CR26 original-print variants without page-image verification.

## 11. 기존 콘텐츠 유지 및 배포 통제

V3.35 데이터의 Git SHA를 잠금 검사 대상으로 하고, 기존 독자 원고 **513편·1,539절·근거 723건·개요 97개**, `main`, Google AI Studio 앱을 변경하지 않는다. 이번은 역사 해설의 **중간 깊이 연구 DRAFT**이며 최종 전문 감수와 공개 승인 없이 연구용 JSON만 생성한다.
