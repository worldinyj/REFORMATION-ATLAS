# VOL-03 · 원전·판본 재검증 V0.9-P1
> 2026-10-25 | 연구 초안 DRAFT | 기존 제3권 V0.8R1 이후 첫 번째 역사 검증 게이트
> **중요:** 공개 웹에 접근하여 확인한 범위의 재검증이다. 라틴어 필사본 실물 교감, 2019년 유료 비평판 전문 열람, 체코어 필사본 대조 또는 외부 역사학자 심사를 완료했다는 뜻이 아니다.

## 1. 작업 대상과 검증 방법
- 기준 브랜치: `docs/vol03-deep-research-v0-1`; 원본 자료 `data/vol03_primary_claims.json`의 14개 주장은 **덮어쓰지 않는다**.
- 이번 증분: `data/vol03_source_audit_v09_p1.json`에 출처 접근 방식, 연결된 기존 주장 ID, 근거와 제한 사항, 후속 전문 검증 작업을 기록한다.
- 레벨: **T1** 현존 중세 필사본/원본을 직접 대조, **T2** 공개 역사 인쇄판/원전 전사 직접 확인, **T3** 역사 번역판 직접 확인, **S1** 학술 비평판 출판기관 설명, **S2** 전문 학술서평/학술백과, **HOLD** 판본·번역·이문 교감 보류. T2/T3는 T1과 같지 않다.
- 실제 접근: Internet Archive 역사 라틴 인쇄판 OCR, Fordham 대학 온라인 원전 발췌, 1915년 영어 번역 온라인 전사, 체코어 1937년판 전사, 2019년 비평판의 기관 소개, 2020년 학술서평, Stanford Encyclopedia of Philosophy 2025년 개정판.
- 각 출처의 접근 범위는 문서가 말하는 '이벤트', '역사적 원문', '후대 편집', '연구자의 해석' 가운데 어느 것인지 지정한다.

## 2. 핵심 판정 A — 위클리프 성찬론
**대상 주장:** CLM-V03-001, CLM-V03-002.

- John Wyclif의 `De eucharistia`는 Johann Loserth가 편집한 1892년 인쇄판과 그 OCR 전사에서 접근한다. 이전 조사 기록에 제시된 Ch. IV~V, pp.108–109, 141의 문장·문맥은 전문 라틴어 판면 대조가 완료되지 않았으므로 **검증 등급을 올리지 않는다**. 새 조사에서는 판본 서두가 비엔나·프라하 도서관의 관련 필사본들을 열거한다는 점까지 확인했으나 그 필사본들을 직접 보지는 못했다. [V03-S29]
- 2025년 개정 Stanford Encyclopedia of Philosophy §4.3은 위클리프가 축성 뒤 빵의 실체 존속과 그리스도의 현존을 동시에 논한다는 해설을 제시한다. 따라서 위클리프가 '현존을 무조건 부정했다'거나 오늘날의 '순수 기념설'을 그대로 가르쳤다는 단정은 피한다. **이 대목은 현대 학술 해설이지 인쇄판 판면 교감의 대체물이 아니다.** [V03-S19]
- Fordham Medieval Sourcebook의 제목이 `On the Sacrament of Communion`인 글은 페이지 서두와 출처 표기상 `Trialogus`에서 뽑은 발췌이다. `De eucharistia`의 번역문으로 출처를 재지정하면 안 된다. [V03-S30]
- **미완료:** 1892년 인쇄판 페이지 이미지 대 OCR 오류 교정, Ch. IV의 반론/자기 견해 문맥 분리, 관련 필사본 이문 분석.

## 3. 핵심 판정 B — 후스 『De ecclesia』
**대상 주장:** CLM-V03-003, CLM-V03-004.

- David S. Schaff의 1915년 영어 번역 전사에서 Ch. IV는 '그리스도만이 보편교회의 머리'라는 핵심 결론을 직접 제시한다. 이는 **역사 번역본에서의 확인(T3)** 이며 라틴어 원문 대조(T1/T2)가 아니다. [V03-S31]
- Ch. I은 '교회'라는 표현의 복수 의미를 논하고, Ch. XVII은 순종과 교회 권위에 관해 논쟁한다. 이를 '모든 제도적 교회가 무가치하다'거나 '모든 성직자에게 순종할 필요 없다'로 과장하지 않는다.
- 후스의 `De ecclesia`에서 그리스도를 머리로 강조하는 것과 그가 위클리프의 성찬론을 전면 수용했다는 명제는 다른 문제다. 현 단계에서는 후스의 성찬론 저술 및 학술 교차 대조를 별도 게이트로 둔다. [V03-S21,V03-S22]
- **미완료:** 라틴어 비평판 장·절·페이지와 Schaff 번역문의 대응표, 번역자의 해설·주석 분리.

## 4. 핵심 판정 C — 프라하 4개조의 네 조항
**대상 주장:** CLM-V03-005, CLM-V03-006, CLM-V03-007, CLM-V03-012.

체코 Wikizdroje에 공개된 글은 서지상 Palacký–Tschorn 1937년판 제3권 225쪽 계열의 **후대 편집본을 다시 전사한 글**이다. 1420년 작성된 유일한 자필 원본이라고 부르지 않는다. [V03-S32]

| 조항 | 온라인 전사에서 확인되는 특징 | 한국어 서술 지침 |
|---|---|---|
| I 말씀 선포 | `od křesťanských kněží` — 기독교 사제·성직자 | '누구든 무제한 설교' 대신 당시 특정 설교 주체를 표시 |
| II 양형성찬 | `jimž hřiech smrtelný nepřekážie` — 중대한 죄에 관한 제한 | '아무 조건 없이 전체 주민에게 성찬'이라는 단정 금지 |
| III 성직자 재산·권력 | 세속적 지배와 부당한 재산을 둘러싼 문제 | 모든 교회 재산의 예외 없는 폐지를 선언했다고 과장 금지 |
| IV 공개적인 죄의 교정 | `jenž úřad k tomu mají` — 해당 직무 권한을 지닌 자 | 임의의 개인에게 무제한 처벌권을 부여했다고 설명 금지 |

1844년 `Archiv český` 편집계열과 1937년 출판계열은 별개 판본으로 유지한다. 둘 사이의 실제 이문이 무엇인지는 두 인쇄판의 **판면을 나란히 확보하기 전까지 미확인**이다. [V03-S23,V03-S32]

## 5. 핵심 판정 D — 바젤 콤팍타타: 시간·문서 세트 분리
**대상 주장:** CLM-V03-008, 009, 010, 013, 014.

- **1432 Cheb(Eger):** 바젤 공의회 논쟁에 사용할 심판 기준을 두고 협상. 학술서평은 1432년 5월 18일 협의에 대해 언급한다. 해당 의정서 자체의 원문 직접 열람은 아니다. [V03-S34]
- **1433년 11월 30일 Prague:** Fudge의 2020년 학술서평은 원래 합의의 핵심이 당사자들이 확인한 **3개 문안**임을 전한다. 원문 3점/인장 실물은 직접 조사하지 않았다. [V03-S34]
- **1433년 12월 11일 관련 서술:** 같은 서평은 최종 문안이 이 날짜 이후 달라지지 않았다는 Šmahel의 해석을 소개한다. 이를 11월 30일의 '3개 문안'과 혼합해 **같은 단일 사건/동일 날짜**로 병합하지 않는다. [V03-S34]
- **1436년 7월 Jihlava(Iglau):** 기관 출판 안내와 서평은 후속 협상 끝에 콤팍타타가 공적으로 선포되었다고 설명한다. 이 시점은 최초 문안 작성일과 다르다. [V03-S33,V03-S34]
- **1437년 12월 23일 Basel:** 공의회 `Ut lucidius videatur` 후속 교령에 대해 서평은 평신도가 잔을 반드시 받아야 한다는 의무를 인정하지 않았다고 정리한다. 원전 문장과 법적 효력은 미대조다. [V03-S34]
- **문서 수의 차이:** Šmahel의 2019년판에 포함된 관련 라틴어 문서는 **10건**이고, 서평에 따르면 **24개 필사본**에 근거했다. 이 숫자는 1433년 프라하에서 확인한 **3개 핵심 원 합의 문안**의 숫자와 동일한 범주가 아니다. 책의 실제 라틴어 편집 텍스트(pp.165–218)는 직접 열람하지 않았다. [V03-S33,V03-S34]
- **미완료:** 2019 비평판 문서 10건별 외교문서 유형·서명·인장·법적 발효 시점, 1437년 교령 본문 교감, 콤팍타타의 가톨릭·우트라크비스트 해석 차이를 전문으로 검토.

## 6. 주장 관리 게이트 (V0.9-P1)
1. 기존 14개 CLM 기록·182 노드·365 에지는 수정 없이 **읽기 전용 기준**으로 유지. 이 보충 조사 때문에 기존 관계 그래프의 수량을 자동 갱신하지 않는다.
2. 새 JSON의 각 `claim_ids`와 `source_ids`는 기존 주장/출처를 참조한다. 이는 **근거 추적성**이지 원전 검증 완료나 게시 승인을 뜻하지 않는다.
3. 모든 항목 `review_status=DRAFT`, `publication_gate.approved=false`, `can_ship=false`.
4. 고증 및 공개 승인 전 Word·SVG·AI 그림에 정식 학술 인증·복원 완료 문구를 붙이지 않는다.

## 7. 우선 후속 실무 과제
- **P1-A:** Loserth (1892) 실제 인쇄면의 Ch. IV/V 문장 대 OCR을 대조하고 문장별 필사본 이문을 검토.
- **P1-B:** Hus `De ecclesia` 라틴어 정본 확보 후 1915 영어 번역의 Ch. I/IV/VII/XVII 문장 대조.
- **P1-C:** Palacký (1844)와 Palacký/Tschorn (1937) 인쇄면의 네 조항을 좌우 대조해 현대 체코어 전문 감수.
- **P1-D:** Šmahel (2019) pp.165–218 접근권한 확보 후 10건 문헌 목록과 1433년 3개 핵심 텍스트 관계를 확인.
- **P1-E:** 역사학자/라틴어학자/체코어 연구자에 의한 독립 검증 결과가 있을 때만 항목별 `REVIEWED` 승격.

## 8. 출처 및 접근범위 (재확인일 2026-10-25)
- [V03-S19] Stanford Encyclopedia of Philosophy, *John Wyclif*, §4.3, 2025-05-06 revision. **S2 학술백과**: https://plato.stanford.edu/entries/wyclif/
- [V03-S29] Loserth ed., *Iohannis Wyclif De eucharistia tractatus maior* (1892), Internet Archive OCR. **T2 편집본 OCR**: https://archive.org/stream/latinworks13wycl/latinworks13wycl_djvu.txt
- [V03-S30] Fordham Medieval Sourcebook, *Wyclif: On the Sacrament of Communion*, from *Trialogus*. **T3 번역 발췌**: https://sourcebooks.web.fordham.edu/source/wyclif-euch.asp
- [V03-S31] Jan Hus, *De Ecclesia. The Church*, Schaff 1915 English translation. **T3 역사 번역**: https://en.wikisource.org/wiki/De_Ecclesia._The_Church
- [V03-S32] *Čtyři artikuly pražské*, 1937 edited-text transcription. **T2 후대 편집 전사**: https://cs.wikisource.org/wiki/%C4%8Cty%C5%99i_artikuly_pra%C5%BEsk%C3%A9
- [V03-S33] Centre for Medieval Studies, Czech Academy of Sciences, Šmahel 2019 publication notice. **S1 출판 안내**: https://cms.flu.cas.cz/en/publications/monographs/die-basler-kompaktaten-mit-den-hussiten-1436.html
- [V03-S34] Thomas A. Fudge (2020), Šmahel 2019 review, *The Medieval Review*. **S2 전문 서평**: https://scholarworks.iu.edu/journals/index.php/tmr/article/view/31313
- [V03-S21,V03-S22] 후스 성찬론의 선택적 수용과 위클리프 비교에 관한 학술 초록·서지. **S2 초록만 접근**, 전문 검토 미완료.

**결론:** 서지·전사·후대 학술해설은 여러 건 재확인했다. 그러나 이 단계의 완료란 **검증 근거와 보류 지점을 명확하게 정리했다**는 뜻이며, 역사학 전문 인증이나 본문 공개 승인이 아니다.
