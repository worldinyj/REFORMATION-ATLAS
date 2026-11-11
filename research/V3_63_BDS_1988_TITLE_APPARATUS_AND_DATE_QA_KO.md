# 종교개혁 ATLAS V3.63 — BDS 1988 pp.217–218 표제 장치·날짜 문맥 재검토

**연구 기준일** 2026-11-11  
**계승** `research/atlas-v362-basel-witness-chronology-qa`  
**브랜치** `research/atlas-v363-bds-title-apparatus-correction`  
**상태** RESEARCH_ONLY · DRAFT · NOT_APPROVED · CAN_SHIP=false

## 1. 직접 열람한 공개 자료와 접근 한계

- BDS 6/1 (1988), 인쇄 p.217, https://digi.hadw-bw.de/view/bds6_1/0221
- BDS 6/1 (1988), 인쇄 p.218, https://digi.hadw-bw.de/view/bds6_1/0222
- 본 차수에서 해당 웹페이지의 공개 **OCR 본문**을 직접 재검토했다. 인쇄 이미지 자체의 고해상도 육안 교감이나 16세기 필사본 원본 대조를 완료했다고 기록하지 않는다.

## 2. 표제 교감 — V3.61의 A/B 충돌 해소 범위

BDS 1988 인쇄 p.218에서 편집 본문에 표시된 기본 표제는 다음과 같다.

> Erlüterung der Witembergischen Articklen durch die predicanten von Straßburg gegeben

그 아래 각주 `a)—a)`에서 `B`는 기본 표제의 해당 범위를 생략한 것으로 표시되고, `C`와 `D`에는 서로 다른 표제 읽기가 기재되어 있다.

- A(Leithandschrift): 위 문구가 기본 본문(lemma)의 읽기로 채택되어 있음. *필사본 표제를 이미지로 직접 재검증하지 않았으므로 이 사실만으로 A 표제의 전사 상태를 외교적 검증 완료로 처리하지 않는다.*
- B: `a)—a) B`라는 부호로 기본 표제 구절의 부재 표시.
- C: `Was Doctor Andreas Carolstadt Vnd M. Simon Grynaeüs by den Herren Predicanten zu Strasbürg gehandelt ...`로 시작하는 대체 표제.
- D: `Diß ist vnnser geliepten herren vnnd brüdern zü Straßburg gschrifftliche vßlegung ...`로 시작하는 대체 표제.

### 오류 정정 결정

- V3.61 한국어 Markdown의 'A = Erlüterung ...' 표기는 BDS의 기본 본문 읽기라는 점에서 **완전히 오류라고 할 수 없다**. 다만 A 원필사본 표제의 완전한 외교적 전사라고 주장하지 않는 보충 설명이 필요하다.
- V3.61 JSON `V361-V04`의 'B = Erlüterung ...'는 p.218의 각주 장치와 모순된다. **정정 후보: B의 해당 표제 = omitted**.
- JSON의 A에 적힌 `BDS editorial headword, not established manuscript title`는 지나치게 부정확하다. **정정 후보: BDS main-text lemma based on A (Leithandschrift), A facsimile heading not directly verified**.
- 기존 V3.61 원본 파일은 이 브랜치에서도 변경하지 않고, 별도의 정정 자료에 기록한다.

## 3. 사건 연대 재검토

BDS 인쇄 p.217 편집 서론은 바젤의 그뤼네우스·미코니우스가 작성한 견해에서 `unio naturalis` 문제를 제기했고, 그에 대한 설명을 얻으려고 바젤 대표들이 파견되었다고 서술한다. 이어 취리히 사료의 후기 문구를 인용하여 카를슈타트와 그뤼네우스가 스트라스부르의 카피토·부처와 8일간 회담을 하고 서면 설명을 얻었다는 내용 뒤에 `Julij 17 1536`이 있음을 전한다.

인쇄 p.218의 편집 서술은 1536-07-19 미코니우스의 불링거 서신에 당시 두 바젤 대표가 **아직 스트라스부르에 있었다**고 기술하며, 짧게 `Et iam sunt Argentinae. Nos expectamus, quid referant`라고 인용한다.

### 충돌/해석

- 7월 17일을 **실제 귀환 완료일**로 확정하는 것은 7월 19일 서신의 편집자 설명과 긴장 관계가 있다.
- 7월 17일을 **파견 시작일**로 확정하는 것 역시 후기 문구의 문장 배열(파견→8일 협의→서면 답변→날짜)만으로는 정당화하기 어렵다.
- `1536-07-17`은 **동시대 사료의 문맥에 포함된 날짜 기재**로 보존하고 사건 유형은 `UNRESOLVED`로 둔다.
- BDS에서 제시한 '1536년 7월 중순' 협의 범위와 '1536-07-19 아직 체류' 정보는 별도 데이터로 유지한다.
- 1537-08-02라는 C 사본의 날짜 기재는 여전히 사본에 적힌 기재값으로 보존하되 편집자 연대 정정과 구분한다.

## 4. 신학적 내용 연결

BDS p.217은 바젤 측 질문의 핵심 논점 중 하나로 자연적 결합(`unio naturalis`)을 명시한다. 이는 바르게 부록 제50호 Q1 '실재적 임재와 자연적 결합 구별'이라는 V3.61의 주제 대응을 **간접적으로 보강**한다. 다만 Q1의 정확한 독일어 본문과 A–D 사이의 모든 이문을 검증한 것으로 취급하지 않는다.

## 5. 검증 및 공개 게이트

| 검증 대상 | 결과 |
|---|---|
| BDS p.217–218 공개 OCR 원문 재열람 | PASS |
| 본문 기본 표제와 B의 생략 각주 구분 | PASS_OCR |
| C·D 표제 계열 구분 | PASS_OCR |
| V3.61 JSON 표제 B 오배정 발견 | PASS |
| A 원필사본의 표제 존재·필체·행 단위 검증 | PENDING |
| 1536-07-17의 정확한 사건 유형 | UNRESOLVED |
| HBBW 제866호 원문·문맥 직접 교감 | PENDING |
| 전문가 승인 | PENDING |
| 기존 513편 역사 콘텐츠 또는 웹앱 변경 | NONE |

**결론**: BDS p.218 표제의 A/B 혼동을 정정할 근거가 확인되었으나 OCR 기반 결과이므로 원판 이미지와 사본 대조는 남겨 둔다. 역사 콘텐츠 출판 상태는 `CAN_SHIP=false`를 유지한다.

## 6. 다음 연구 우선순위

1. BDS 1988 p.218 인쇄 이미지 또는 IIIF 타일에서 표제 및 `a)—a)`의 위치 확인.
2. HBBW 제866호(1536-07-19) 본문에 실린 발신·수신·날짜와 바젤 대표단 위치를 직접 확인.
3. Basel Staatsarchiv Kirchenakten A9 fol.405–410의 보존 기록·이미지 접근 여부 확인.
4. 바르게 1905 II 부록 50의 페이지 단위 인쇄 이미지와 Q1–Q4 대조.
