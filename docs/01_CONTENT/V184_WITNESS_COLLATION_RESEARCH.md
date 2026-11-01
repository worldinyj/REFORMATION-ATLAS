# V1.84 연구 작업: 사료 대조를 위한 판본·사본 비교 패킷

## 검토 결과
1. 아우크스부르크 제4조는 1531년 인쇄 라틴어 본문과 1540년 Variata 본문을 나란히 확인해야 하며, Schaff의 역사적 편집 자료는 수정이 있었다고 설명한다. **실제 전체 라틴어 문장은 아직 입력하지 않았다.**
2. 아우크스부르크 제10조에서는 편집 비교 자료가 `vere adsint / distribuantur vescentibus`와 `cum pane et vino / vere exhibeantur`를 각각 기록한다. 이는 16세기 원판의 직접 대조가 아니라 후대 편집 전승에 근거한 구별이다.
3. 아우크스부르크 제11·12조의 고해/회개 조항은 1530과 1540에서 순서가 뒤집히므로 주제 기반 대응이 필요하다.
4. 마르부르크의 Z(취리히)·K(헤센) 소장번호와 참고 교감판 3종을 기록했다. 제7·13·15조의 추가 문구는 소장기관에서 존재를 설명하지만 **직접 전사하지 않았으므로 null**로 둔다.
5. 칼뱅 1536→1539→1543→1550→1559의 판본 구조는 연결했으나 장절별 동일 논증 대응은 검증되지 않았으므로 null로 보존한다.

## 기존 대비 실제 개선
V1.83의 '소장처·편집본 후보'를 **5개 별도 문헌/이문 대조 단위**로 분리하여 예상 증인(witness), 위치, 변화 성격, 미확인 전사 부분을 명시했다. 이 데이터는 연구자의 대조 작업 입력물이며 학술적 이문 대조의 완성 결과가 아니다.

## 출처
- Augsburg 1530/1540 비교: https://www.augsburg1540.com/1530-1540-comparison-text.html
- Schaff 1531 라틴어 인쇄본 설명: https://www.uecf.net/books/collected-works/chapter1488.html
- Schaff 1540 변경 분석: https://www.uecf.net/books/collected-works/chapter1319.html
- Zürich archival catalogue: https://suche.staatsarchiv.djiktzh.ch/detail.aspx?ID=618165
- Anthony N. S. Lane, *A Reader's Guide to Calvin's Institutes* 발췌: https://cdn-static.supadu.com/baker-academic-us/pdf/Excerpt_9780801037313.pdf

## 후속 실질 작업
- 원판 또는 신뢰할 수 있는 외교적(diplomatic) 전사 자료 확보 및 정확한 라틴어/독일어 문장 필드 입력
- Z/K 제7·13·15조 단락별 대조 및 번역, 판본 의존관계 기록
- 칼뱅 중간판 본문 확보 후 '동일·이동·확장·삭제·새로 추가' 분류
- 전문 검토를 통과한 원고만 웹앱 투입 검토

연구 브랜치 전용이며 `main`·Google AI Studio 앱에는 반영하지 않음.
