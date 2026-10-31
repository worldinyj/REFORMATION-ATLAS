# V1.54 — 60편 종교개혁 심화 역사학습 패키지

**2026-10-31 · 연구용 초안 · main과 AI Studio 코드 별도**

V1.53의 12개 제3권 모듈을 넘어서 이번에는 **여섯 영역, 총 60개 독자용 미니 해설**을 추가했다. 각 항목은 질문, 역사적 설명, 참고 출처 링크, 원문 직접 교감 미완료 상태를 포함한다.

## 구성
- A. 중세 말의 배경 — 10편
- B. 위클리프와 후스 — 10편
- C. 루터와 초기 독일 종교개혁 — 10편
- D. 스위스와 제네바 — 10편
- E. 신학 개념 비교 — 10편
- F. 문헌과 후대의 유산 — 10편

## 편집 원칙
1. 위클리프의 14세기 『교회론』 `WRK-V03-WYCLIFFE-DE-ECCLESIA`와 후스의 1413년 문헌 `OV-D-005`는 다르다.
2. 루터의 1517년 논쟁을 1530년 신앙고백의 완성된 교리로 소급하지 않는다.
3. 칼뱅 1536년 초판과 1559년 최종판은 서로 다른 판본으로 추적한다.
4. 루터·츠빙글리의 성만찬 의견 차이를 ‘실재 대 상징’의 양극단으로 조롱하거나 단순화하지 않는다.
5. 1530년 아우크스부르크 제출, 1531년 인쇄, 1540년 수정판을 분리한다.
6. 60편의 설명은 **연구용 초안**이다. 학술 개설·서지 등에서 확인된 사실을 바탕으로 작성했으나 원전 직접 대조·전면 전문가 감수는 아직 없다.

## 웹앱 접속 계획
`data/contracts/atlas_v154_60_module_outline.json`을 전체 목차로 쓰고, `data/deep/atlas_v154_group_[a-f].json`에서 각 해설과 질문을 가져온다. 모바일 UI에서는 여섯 주제별 탭 또는 카드 목록을 배치하고 상세 화면에 설명과 출처를 나란히 제공한다. **자동 배포는 허용하지 않으며 리뷰 후 반입**한다.

## 출처 시작점
- Stanford Encyclopedia of Philosophy, Wyclif: https://plato.stanford.edu/entries/wyclif/
- Masaryk University, Hus catalogue: https://digiscripta.phil.muni.cz/cs/node/12908
- Encyclopaedia Britannica, Luther: https://www.britannica.com/biography/Martin-Luther
- Britannica, Zwingli: https://www.britannica.com/biography/Huldrych-Zwingli
- Britannica, Calvin: https://www.britannica.com/biography/John-Calvin
- Britannica, Augsburg Confession: https://www.britannica.com/topic/Augsburg-Confession
- Britannica, Council of Trent: https://www.britannica.com/event/Council-of-Trent

## 검증 명령
`python3 scripts/validate_atlas_v154.py`. 항목 60개 수·제목 중복·주제 설명·출처·직접 교감 미완료·공개 보류를 확인한다. 이것이 역사적 사실 전반을 검증한다는 의미는 아니다.
