# 제4권 저작·판본 정식 ID 이관 계약 V0.2

> **DESIGN CONTRACT / NOT A MIGRATION** (2026-10-25). 연구 브랜치의 [17개 서지 데이터](../../../data/deep/vol04_witness_bibliography_v02.json)를 읽는 웹/데이터 개발자를 위한 명시적 경계.

## ID 모델
```text
Canonical PERSON (OV-P-013…016) -- unchanged
  │
  ├── Work identity (existing OV-D-011 Augsburg / OV-D-012 Institutes)
  │        ├── Edition (EDN-V04-XXXX)       [reviewed historical edition only]
  │        ├── Translation (TRN-V04-XXXX)   [reviewed translation derived from specified edition]
  │        └── Witness (WIT-V04-XXXX)       [reviewed manuscript/print individual copy]
  │
  └── New independent Work (DOC-V04-XXXX)   [only after editorial approval]
```

`DOC-PROP-V04-*` / `EDN-PROP-V04-*` / `WORK-PROP-V04-*`는 **정식 ID가 아니다**. 심층 사건 `DEEP-V04-*` 역시 정식 사건 ID가 아니며, 이미 존재하는 `OV-E-*`와 중복 발급하면 안 된다.

## 필수 필드와 인수 전 검사

| 계층 | 필수 | 금지 |
|---|---|---|
| Work | ID·저자/공동 저자·원어 표제·문헌 분류·기존 정본/신규 여부 | 회담 목격보고와 공동합의문을 한 저작으로 병합 |
| Edition | work ID·연도/정밀도·언어·출판지·인쇄자 또는 미확인 상태·대표 판본 근거 | 1530 제출본=1540 Variata, 1536 칼뱅=1559 칼뱅 |
| Translation | 번역 대상 판본 ID·번역자/저자 자신의 개역 여부·언어·간행년 | 현대 번역본을 16세기 원본으로 오기 |
| Witness | 소장 기관·소장번호 또는 명시적 결측·필사/실물/디지털 재현 구분 | 링크 존재만으로 전체 사료 직접 대조 완료 주장 |
| 연구 Claim | 문장·원전/후대 해설 출처 ID·불확실성·편집 상태·출판 승인 | source ID 없는 주장, 학술 초록만으로 전문 읽었다는 주장 |
| 역사 Media | provenance·권리·AI 상상 재현 표기·지리/복장 고증·human approval | AI 초상/개념도를 당대 진본 이미지로 표시 |

## 승인 전 자동 차단
- 문헌·사건·이미지의 `approved=false` 또는 `publication_approved=false`는 **build exclusion**.
- 자산 미승인 여부를 CSS 숨김/noindex/클라이언트 조건문으로 처리하지 않는다.
- 새로 가져올 자료는 현재 연구 정본 파일이 아니라 **명시적 인간 승인으로 생성된 별도의 퍼블릭 스냅샷**이어야 한다.
- 키 충돌이나 언어별 문헌 분리 미완료가 있으면 전체 마이그레이션 중단; 기존 `OV-D`와 `OV-P`는 변하지 않는다.
- 웹앱은 Google AI Studio Build에서 개요 뼈대를 계속 개발하고, 이 연구 브랜치를 런타임 직접 데이터 URL로 연결하지 않는다.

## 이관 준비 판정
`BIBLIOGRAPHY_DRAFT_PREPARED` · `CAN_MINT_CANONICAL_IDS=false` · `CAN_PUBLISH=false`. 정식 ID로의 이관은 5개 분리/판본·법적 권리·내용 승인 뒤 별도 PR을 통해 수행.
