# 종교개혁 ATLAS V3.55 — 1536년 비텐베르크 일치협약의 지역 수용과 전승

- 작성: 2026-11-10
- 이전 버전: V3.54 (`research/atlas-v354-wittenberg-1530-1540-lemma-collation`)
- 연구 브랜치: `research/atlas-v355-concord-reception-city-matrix`
- 승인: RESEARCH_ONLY / DRAFT / NOT_APPROVED / CAN_SHIP=false
- 변경 금지: `main`, 공개 역사 원고 513편, Google AI Studio 앱, 기존 사료파일

## 1. 연구 질문과 이번에 해결된 쟁점

**비텐베르크에서 체결한 1536년 협약을 여러 도시는 실제로 언제, 누구를 통해, 어떤 권한으로 수용했는가?**

연구상 가장 중요한 구분은 다음 다섯 단계다.

1. `participant_assent`: 비텐베르크 현장 참가자의 합의·서명.
2. `report_or_explanation`: 귀향길 또는 귀향 후의 합의 내용 보고·설명.
3. `clergy_or_church_assent`: 해당 도시 목회자, 교구대표, 교회 지도부의 동의.
4. `magistrate_ratification`: 해당 도시의 시의회/당국 공식 승인.
5. `regional_reception_or_rejection`: 다른 도시가 수용·유보·거절하거나 후속 교섭을 진행한 상태.

**단일 도시를 단순한 `accepted=true/false`로 모델링하지 않는다.** 시점과 승인 주체가 서로 다르기 때문이다.

## 2. 날짜 검증과 시작 조건

MBW 1744는 협약을 1536년 5월 29일로 표기하며, 1988년 BDS 6/1 목차의 28일을 보충 주석에서 잘못된 날짜로 지적한다. BDS 6/3의 「Chronologia Bucerana」에서도 5월 29일을 협의 종결, 문서 낭독, 합의 조항 서명 일자로 분명하게 제시한다. 다만 별도의 `De magistratu`는 비텐베르크 측만 서명했다는 점을 같은 연표가 구분한다.

참조: [MBW 1744](https://melanchthon.hadw-bw.de/regest.html?reg_nr=1744), [BDS 6/3 /0016, p.12](https://digi.hadw-bw.de/view/bds6_3/0016).

## 3. 실증 연표: 설명에서 승인까지

| 날짜 | 지역·인물 | 자료가 보증하는 사건 | 판정 |
|---|---|---|---|
| 1536-05-29 | 비텐베르크 | 참석자 협상 마무리·공통 조항 서명 | `participant_assent` / MBW regest + BDS 연표 |
| 1536-06-02~05 | 프랑크푸르트 | 귀환 참가자들이 각 도시 당국에 제출할 공동 보고서를 정리. 부처와 카피토는 뒤에 추가 체류 | `report_drafted` / BDS 6/1 pp.135–174 + 2014 Capito correspondence headnote |
| 1536-06-22 | 부처와 동료들 | 참석하지 못한 동료들이 서명하도록 설명·권고한 문헌 | `explanation_written` / BDS 6/1 pp.175–202 |
| 1536-06-29 | 스트라스부르 | 부처의 합의 경위 설명 문헌. 편집자 주석에 목회자·교구 관리인들의 수용 언급 | `church_local_assent` / BDS 6/1 pp.203–208. **시의회 최종 비준과 혼동 금지** |
| ca. 1536-07-02 또는 이후 | 스트라스부르 | `Dem volck solle man verkunden` 설교대 발표 문서. 비평판 목차는 약 6/29지만 편집자 해설은 6/29 발표 이후 첫 주일인 7/2를 가능한 발표일로 지목 | `draft_for_public_proclamation` / BDS p.207. 실제 낭독일 확정하지 않음 |
| 1536-07-05 | 스트라스부르 | `Declaratio articulorum germanica` 독일어 해설 문헌 | `text_explanation` / BDS 6/1 pp.209–216 |
| 1536-07-17 | 스트라스부르 | 도시 설교자들이 비텐베르크 조항을 해설한 문헌. 네 필사본 계열의 대부분 차이는 정서법 문제라는 비평판 설명 | `clergy_interpretation` / BDS 6/1 pp.217–226 |
| 1536-07-22 | 부처 → 루터 | 부처는 프랑크푸르트·보름스·란다우·바이센부르크·에슬링겐·아우크스부르크·멤밍겐·켐프텐·스트라스부르가 조항에 동의했다고 보고. **정식 비준은 아직 필요** | `reported_acceptance_pending_ratification` / WA Br 7:471–473, Ep.3050, cited by Capito correspondence headnote |
| 1536-07-23 | 아우크스부르크 설교자 → 루터 | 신중한 검토 후 협약 서명 사실 보고 | `clergy_subscription_reported` / WA Br 7:474–476, Ep.3051 (Capito correspondence headnote) |
| 1536-08-26 | 스트라스부르 시의회 | 시의회가 공식적으로 협약을 승인했다고 서신집 연구 해설 기재 | `magistrate_ratification_reported` / *Correspondence of Wolfgang Capito*, Ep.612 headnote; cites Eells 207 |
| 1536-09-03 | 에슬링겐 | 협약 비준일로 언급(11/2 츠비크 보고를 인용한 현대 편집자 주석) | `city_ratification_reported` / HBBW 6 Ep.908 cited via Capito correspondence |
| 1536-09-13 | 로이틀링겐 | 협약 비준일로 언급 | `city_ratification_reported` / same |
| 1536-09-16 | 멤밍겐·켐프텐 | 두 도시의 협약 비준일로 언급 | `city_ratification_reported` / same |
| 1536-10-30 | 울름 시의회 | 협약 수용을 공포하고 비텐베르크에 통보 | `magistrate_ratification` / Ulm Stadtarchiv, *Kirchen und religiöses Leben*, p.41 |
| 1536-11 (day unverified) | 콘스탄츠 | 수용하지 않음. 부처·스트라스부르 설교자들이 11월 23일 콘스탄츠에 보낸 서신은 BDS 6/1 pp.258–270에 수록 | `city_rejection_reported` / Capito correspondence headnote and BDS TOC |
| 1537-01-27 | 취리히·스위스 | 부처의 스위스 교회 대상 후속 서신 | `outreach_continues` / BDS 6/1 pp.271–273 |
| 1537-04-01 | 스위스 연맹 | 부처가 연맹 측에 자신의 보고를 전달하는 문헌 | `outreach_continues` / BDS 6/1 pp.274–293 |
| 1538-01-14 | 카피토·부처 → 바젤 | 루터의 1537년 12월 1일 스위스 도시 대상 편지를 전달하고 여전한 이해 차이를 언급 | `negotiations_unresolved` / BDS 16 (2013), pp.277–295 |

**실증 한계:** 7/22, 9월의 도시별 비준 정보는 당시 서신을 *현대 학술 편집자의 주석을 통해* 확인한 것이며, 이 단계에서 각각의 시의회 원부 또는 해당 서신의 실물 이미지를 직접 판독하지 않았다. 8/26 스트라스부르 비준도 Eells가 인용된 학술 해설이다. 울름 10/30은 시립문서관 자체의 역사 해설이 독립적으로 보강한다.

## 4. 지역별 수용 판정 (2026-11-10 연구 단계)

| 지역 | 가장 강한 현재 근거 | 판정 방식 |
|---|---|---|
| 비텐베르크 | MBW + BDS 연표 | 현장 참가자 동의; 도시 전체의 독립 비준과 구별 |
| 스트라스부르 | BDS 6/1 6/29, 7/17 및 Capito correspondence의 8/26 | `church_assent` → `council_ratification_reported` |
| 프랑크푸르트 | 6/2–5 보고 초안, 7/22 부처의 동의 보고 | `reported_acceptance_formal_ratification_unverified` |
| 아우크스부르크 | 7/23 도시 설교자들이 루터에게 보낸 동의 보고 | `clergy_signed`; 의회 비준 별도 검증 |
| 에슬링겐 | 9/3 수용으로 서신집 해설에 전함 | `ratified_reported_secondary_to_letter` |
| 로이틀링겐 | 9/13 수용으로 전함 | 동일 |
| 멤밍겐·켐프텐 | 9/16 수용으로 전함 | 동일 |
| 울름 | 울름 시립문서관, 10/30 | `city_council_acceptance_supported` |
| 콘스탄츠 | 서신집 해설: 11월 거부, BDS 11/23 서신 | `rejected`, 결정문 직접 판독 미완료 |
| 취리히·베른·바젤 등 | 1536 회담 불참, 1537–38 후속 교섭 | 단일 `swiss_rejection` 불가: 개별 도시·신학자별 입장 별도 관리 |

### 특히 중요: '독일 도시들 모두 수용'이라는 문구 금지
부처의 7월 22일 보고는 수용 전망과 조항 동의 사실을 알려주지만, 공식 비준 자체가 남았다고 명시한다. 프랑크푸르트, 보름스, 란다우 등은 **보고 단계의 동의**로만 적는다.

### 스위스와 콘스탄츠를 합쳐 한 진영으로 취급하지 않음
1536년 5월 1일 스위스 대표들은 회담에 불참했다. 루터는 1537년 말에도 스위스 도시들의 동의를 설득했고, 1538년 1월 전달된 부처·카피토의 설명에는 아직 신학적 견해 차이가 남아 있었다. 시민당국, 설교자, 지역 대표자의 서명/수용을 독립적으로 다룰 것.

## 5. 자료 비평: '6월 29일 설교'라는 오해 바로잡기

BDS 6/1 p.207의 편집자는 `Dem volck solle man verkunden` 원고를 설명하면서 **시의회 대상 설명보다 먼저 설교가 행해지지는 않았을 것**이라고 말한다. 해당 시의회 관련 설명은 6월 29일로 기록되어 있고, 다음 주일인 7월 2일이 공개 선포의 가능한 날짜라고 제시한다.

따라서 목차의 `ca. 29. Juni 1536`만을 보고 '6월 29일 주일설교'라고 확정하는 것은 피해야 한다. 원고 작성·문서 표제상의 날짜·실제 대중 전달 일자는 별개 필드로 둔다. 문헌에 `Productum dem samstag den 29 Junij Anno 1536`과 같은 기록이 있더라도, 요일·날짜의 내부 일치성도 함께 점검한다.

## 6. 수용의 신학적 내용 — 일반 독자용 해설 초안

### 협약은 서명했지만, 도시는 아직 답하지 않았다

1536년 5월 말, 비텐베르크의 협의가 끝났을 때 남독일과 작센의 신학자들은 성찬에 관한 공동 표현을 마련했다. 그러나 그 문서에 서명한 신학자들이 각 도시 전체를 대신하여 즉시 최종 결정을 내린 것은 아니었다. 아직 자리에 참석하지 못한 목회자들과 시 당국의 동의가 필요했다.

부처와 카피토가 돌아오는 길에 프랑크푸르트에서 여러 도시의 대표들과 결과를 설명할 보고문을 준비한 것은 그 때문이다. 스트라스부르에서는 부처의 설명문, 목회자들의 해설, 대중에게 전할 설교문이 잇따랐다. 여러 사람에게 서로 다른 방식으로 협약을 설명해야 했다는 사실은, 신학적 화해를 공동체의 새로운 관행으로 옮기는 일이 하나의 서명보다 훨씬 복잡했음을 보여준다.

흥미롭게도 대중에게 전하기 위해 작성한 해설문은 그리스도의 몸과 피가 성찬에서 참으로 주어지고 받아들여진다고 설명하면서, 빵과 포도주가 물질적으로 바뀌거나 그리스도의 몸이 공간적으로 갇힌다는 해석은 경계했다. 그래서 신학자들의 라틴어 표현은 도시 사람들에게 전할 독일어 설교의 언어로 다시 설명되어야 했다.

스트라스부르는 8월 26일 시의회의 공식 동의에 이르렀고, 울름은 몇 달을 더 논의하다 10월 30일에야 협약을 받아들였다. 콘스탄츠는 같은 해 11월 협약을 받아들이지 않았다. 부처는 스위스 도시들과의 대화를 포기하지 않았으며, 협의는 1538년에도 계속되었다.

이 과정은 종교개혁이 유명한 신학자 몇 사람의 논쟁만으로 끝나지 않았다는 사실을 드러낸다. 설교자와 시의회, 도시 주민, 지역 교회가 서로 다른 속도로 결정을 내렸고, '교리적으로 합의했다'와 '그 합의를 교회가 실제로 받아들였다'는 서로 다른 사건이었다.

**독자 질문:** 한 도시의 설교자가 찬성했는데 시의회가 아직 승인하지 않았다면, 그 도시는 이미 협약을 수용한 것일까?

*공개 금지: 이 문장은 DRAFT이며 출처 판정과 전문가 교열이 끝나지 않았다.*

## 7. 구조화 스키마 및 지도·인물 연동

`event_id`, `date_value`, `date_precision`, `place_id`, `city`, `source_document_id`, `source_page`, `source_access`, `actors`, `authority_level`, `reception_status`, `direct_council_minute_checked`, `claim_strength`, `source_urls`, `publication_gate`.

허용 상태:
- `participant_assent`
- `report_drafted`
- `explanation_written`
- `church_local_assent`
- `text_explanation`
- `reported_acceptance_pending_ratification`
- `clergy_subscription_reported`
- `magistrate_ratification_reported`
- `city_council_acceptance_supported`
- `city_rejection_reported`
- `outreach_continues`
- `negotiations_unresolved`

위 상태는 단일 수용 여부 Boolean으로 변환하지 않는다.

`place_id`는 도시명+역사명칭+오늘날 국가를 포함하지만, 현 도시 중심점에 대한 임의의 상세 GPS 좌표를 연구원문 근거처럼 쓰지 않는다. 독자용 역사 지도에서는 회담 개최지, 문서 작성지, 결과 수용지의 마커를 별개로 설명해야 한다.

인물 연결: 루터·멜란히톤(비텐베르크); 부처·카피토(스트라스부르); 마르틴 프레히트(울름); 요하네스 베른하르디(프랑크푸르트); 요하네스 츠비크(콘스탄츠); 하인리히 불링거(취리히). 관련 인물이 도시의 입장을 언제나 대표한 것으로 자동 추정하지 않는다.

## 8. 16세기 시각 자료 — 권리·시점 구분을 위한 후보만 등록

- **1572년 비텐베르크 도시 목판화**, 세바스티안 뮌스터의 *Cosmographia*에 실림, 에모리 대학교 Pitts Theology Library가 원자료/온라인 버전을 미국 내 퍼블릭 도메인으로 표기.
- 원문 링크: https://digital.pitts.emory.edu/s/digital-collections/item/5649
- 현재는 **이미지 파일을 복사·다운로드·수정·배포하지 않음**. 향후 웹앱 적용 시 현지 관할권 및 기관 요구 인용/이용 정책 재검토.
- 1572년 지도를 **1536년 일치협약 당시 도시의 정확한 현황 사진**이라고 기재하지 않음.

## 9. 검증 결과와 다음 순서

### 완료
- [x] 5월 29일 종결 날짜와 근거 유형 재확인.
- [x] 프랑크푸르트 6월 초 보고문, 스트라스부르의 6월·7월 설교·설명·승인 단계를 분리.
- [x] 7월 22일 부처의 '보고된 동의'와 공식 비준 차이 명시.
- [x] 스트라스부르 8월 26일, 울름 10월 30일, 콘스탄츠 11월 입장 차이 조사.
- [x] 공개 설교문 날짜의 편집상 불확실성 별도 등록.
- [x] 1537–38년 스위스 접촉을 이행 후속 사건으로 연결.
- [x] 한국어 독자용 심화 문단 초안 및 공개 보류.
### 미완료
- [ ] 각 도시 시의회 의사록 및 개별 1536년 서신 원본 이미지 확인.
- [ ] 7월 22일 서신 WA Br 7 Ep.3050 실물 직접 판독.
- [ ] 1536년 11월 콘스탄츠 회신 문서 원본 검토.
- [ ] 스위스 각 도시별 1536~1538년 개별 수용 단계 재검증.
- [ ] 학술 전문가 검토, 라이선스 점검, 대중 공개 승인.

## 10. 출처별 접근 유형

1. MBW 1744 — **학술 서신목록 regest**: https://melanchthon.hadw-bw.de/regest.html?reg_nr=1744
2. BDS 6/3, 연표 p.12 — **1987년판 온라인 OCR**: https://digi.hadw-bw.de/view/bds6_3/0016
3. BDS 6/1, 목차 및 각 작품 — **1988년판 웹 OCR 및 목차**: https://digi.hadw-bw.de/view/bds6_1/0207 ; https://digi.hadw-bw.de/view/bds6_1/0211 ; https://digi.hadw-bw.de/view/bds6_1/0222
4. BDS 6/1 p.208, 대중 설교문 성찬 해설 — **비평판 OCR**: https://digi.hadw-bw.de/view/bds6_1/0212
5. *The Correspondence of Wolfgang Capito*, English edition, Letter 612 headnote (printed 437–438) — **PDF 추출 텍스트**; 이미지 스크린샷 시도했으나 403 접근 차단. 편집자의 요약과 재인용은 1차 서한 직접 판독으로 표현하지 않는다: https://uplopen.com/books/579/files/ee9e764a-bac4-4b38-a467-6cf85785e09f.pdf
6. 울름 시립문서관 역사 설명 (p.41) — **공공 기록기관의 현대 해설/검색 텍스트**: https://stadtarchiv.ulm.de/-/media/archiv/downloads/ugin/kirchen/reformation.pdf
7. *BDS* 16 (2013), p.277, 1538년 스위스 대상 서신 서문 — **현대 비평판 웹 OCR**: https://digi.hadw-bw.de/view/bds16/0281
8. Emory Pitts Theology Library 1572 목판화 — **디지털 수장품의 권리·출처 메타데이터**: https://digital.pitts.emory.edu/s/digital-collections/item/5649
9. 1536년 울름 관련 비교 연구 — **교회사 연구소 해설**, 프레히트와 슈벵크펠트 긴장 맥락: https://www.wkgo.de/cms/article/print/266

**최종 판정: DRAFT. 발표·병합·기존 원고 반영 없음.**
