# 종교개혁 ATLAS V4.35 — 고위험 주장 5건의 편집 판정 및 원본 보호

> 2026-11-18 · 연구용 · 원전 전체 교감/외부 전문가 교열/앱 반영 **미실시** · `can_ship=false`

## 이번 단계의 실질적 결과

V4.34에서 추린 다섯 건의 수정 후보는 **제3·4·6·7권의 정확한 원고 위치**에 대응한다. V4.32 8권을 독립적으로 재구성한 결과 **5/5 변경 앵커가 유일**, **8/8 변환 결과가 일치**, **4권은 원문 불변**이었다. 앱용 V4.29 JSON은 Git blob `64c27c0dfe05394acbb049807e4c4384d58908b9`로 확인했고 변경하지 않았다.

| 쟁점 | 편집 판단 | 출판 승인 |
|---|---|---|
| 아우크스부르크 1530/1531/1540 | 1530 비공식 인쇄, 1531 멜란히톤 관여판, 1540 Variata의 개념 구분은 정당화되는 **조건부 후보**. 1540 비-Variata 판본도 소장 목록에 별도로 언급됨 | 아니오 |
| 타밀어 1714/1715/1719 | 1715년까지 나머지 신약서가 인쇄됐다는 전문 기관 연구의 구체적 증언을 추가 확보. 다만 인도성서공회의 1719 전권 간행 서술과 충돌하여 **완결 연도 보류** | 아니오 |
| 한국어 성경 1882/1887/1911 | 개별 복음서/신약전서/신·구약 전서 구분 및 정확한 표제 보강 후보. 1911년 4권 구성 소장본의 세부 표제 정보는 L1 주석 대상 | 아니오 |
| 한국 천주교 1779/1784 | 강학 모임과 세례·공동체 형성은 다른 사건. 역사학적 관점의 차이를 유지하는 조건부 후보 | 아니오 |
| 위클리프·후스 성찬론 | remanence와 transubstantiation는 구별되지만 신학 원문 대조 전 세부 해석 확정 불가 | 아니오 |

## V4.33 판정 보정

V4.33의 `CL433-21=SOURCE_SUPPORTED`를 '1715년 신약전서 **전권의 무조건적인 최초 출판 확정**'으로 해석하지 않는다. `CONFLICT_HOLD_FOR_COMPLETION_YEAR`로 **후속 재판정**한다. V4.33 자체는 변경하지 않으며 누적 판정서에 명시적인 이력과 이유를 남긴다.

## 새로 특정한 근거

1. [WLB Stuttgart 전문 연구 자료](https://journals.wlb-stuttgart.de/index.php/wlbf/article/download/296/298/772): 첫 부분 1713말~1714여름 인쇄, 작은 글자로 나머지 부분 1715년까지 인쇄
2. [Bible Society of India 소장관](https://www.bsind.org/bsi-archives/): 1714년 부분 및 1719년 전체 신약 설명 — 타 기관과 충돌
3. [WLB 소장 목록](https://www.wlb-stuttgart.de/fileadmin/user_upload/sammlungen/bibeln/Missionsbibeln/Missionsbibel_Stationen.pdf): `Ba Indien 1715 01`, 타밀어 신약, 2단 인쇄, 이중언어 헌정 서문
4. [LSTC Gruber 목록](https://gruber.lstc.edu/confessions/augs_apol.php): 1530년 독일어 인쇄본, 1531년 판본, 1540년 Variata와 비-Variata 소장 사실
5. [대한성서공회 성서학도서관](https://lib.bskorea.or.kr/$/10110/contents/7502442): 1911년 『셩경젼셔』 4권의 서지 정보와 권별 표제면·구성

## 다음 실증 작업

**V4.36**: 타밀어 신약 1714년 첫 부분의 [Francke Halle 디지털화 소장본](https://digital.francke-halle.de/fsaad/content/titleinfo/162120)과 WLB 1715년 소장본의 **표제지·수록 책·권별 페이지 구분**을 비교하는 독립 검토표 작성. 아우크스부르크 신앙고백은 1530/1531/1540 판본의 동일성에 대한 좁은 확인 항목으로 분리한다.

## 변경 금지 게이트

`HISTORIAN_SIGNOFF=0` · `READER_PILOT=0` · `AI_STUDIO_APP_CHANGE=0` · `can_ship=false` · `can_merge_main=false`.

V4.29 앱 배포본·V4.32 원고·V4.34 증거 원본은 건드리지 않으며, 현재 데이터는 모두 **비공개 연구용 후보**다.
