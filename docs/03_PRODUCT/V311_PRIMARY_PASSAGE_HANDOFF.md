# V3.11 연구 전달본 — 원고 513편을 보존하는 원문 지정 위치 부록

상태: **DRAFT / MEDIA DEPTH / PUBLICATION HOLD**, 실제 Google AI Studio 앱 수정 없음.

V3.10 연구 원고 513편, 1,539절, 출처 723건, 기존 선택 주장 22건, 개요 직접78·부분19의 기존 읽기 연결을 **변경하지 않고**, 사료 중심 추가 해설 4개·12절·주장 위치 카드 12건·출처 구분 기록 10건을 독립적으로 연결한다.

- 트리엔트 1547년 제6회기 칭의교령과 1563년 제23회기 교육 개혁령: 번역 전사 지정 조항
- 베스트팔렌 1648년 오스나브뤼크와 뮌스터 조약: 선택 조항 발췌·율리우스/그레고리 날짜 차이
- 웨슬리 1743년 신앙회 일반 규칙: 현대 전사한 역사적 제2판 1~7항, 1738/1739/1743의 시점 구별
- WCC 1948년 총회와 1961년 Basis: 기관 공식 해설·보고서의 디지털 소장 서지. **보고서 본문 페이지와 투표 원장 미판독**

`data/deep/atlas_v311_primary_passage_medium_addenda.json`의 `addenda`는 위 부록의 별도 작성 원고이며 기존 513편에 포함되지 않는다. `claim_cards`는 이번에 확인한 번역/해설 단락의 위치를 나타내지만 기존 22개 선택 주장과 서로 다른 근거 계층이다. 자료의 원본 언어 판본·필사본/원본 이미지 직접 대조 또는 역사 전문가 서명은 없으며, 어떤 항목도 해당 완료로 승격하지 않았다.

## 재현

```bash
node --test integrations/medium-atlas-v311/source.test.mjs
node scripts/build_v311_primary_passage_delivery.mjs --check
node scripts/build_v311_primary_passage_delivery.mjs --export /tmp/atlas-v311-passages
```

검토 화면에 별도 부록을 표시하려면 `assembleV311(...)`가 반환하는 `getAddendaForReader(readerId)`를 사용한다. 유효한 기존 `readerId`에 대해서만 새로운 연구 부록을 반환하며, 기존 원고를 수정하거나 원전 증거를 자동 승격하지 않는다.

**남은 연구:** 트리엔트 라틴어 공식 판본, 베스트팔렌 두 조약 원어 전문, 웨슬리 브리스톨/뉴캐슬 판본 차이, WCC 첫 총회 인쇄 보고서 282쪽 실제 본문 및 1961년 표결 원장 대조.