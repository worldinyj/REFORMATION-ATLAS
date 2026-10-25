# 시각 디자인·원본 제작 지침 V0.1

## 시각적 일관성
- 아카이브/박물관형, 과장된 중세 판타지가 아니라 차분하고 현대적이며 신뢰감 있는 역사 편집 디자인.
- 인물화: 같은 비율·광원·배경·색조의 비실사형 해설 일러스트. 작품 아래 “AI 생성 역사 재현 이미지” 명시.
- 역사 사건: 확인된 장소·행위의 핵심만 시각화하고 불확실한 세부는 배제한다.
- 대표 지도: SVG를 원본으로 보관하고 PNG는 프리뷰. 시대와 지명이 불명확한 지도는 제작·공개 보류.
- 관계도: 영향/후대 수용/별도 발전/논쟁 관계를 선 모양과 레이블로 명확히 구별. 화살표 하나로 직접 계보를 단정하지 않는다.
- 접근성: alt-text, 캡션, 적절한 대비, 모바일 레이아웃 고려.

## 파일 메타데이터 (asset manifest)
`asset_id`, `type`, `title_ko`, `linked_entity_ids`, `creator_method`, `tool`, `created_date`, `historical_accuracy_note`, `rights_status`, `ai_disclosure`, `review_status`, `source_links`, `alt_ko`, `relative_path`.
권장 파일명 `AST-0001_relation_english-bohemian-reformation.svg`.

## 제작/검증 워크플로
1. 텍스트 사실 검증 → 2. 이미지 제작 명세 → 3. 생성/직접 제작 → 4. 시대·장소·표현 검수 → 5. 자산 대장 연결 → 6. 편집·배포 승인.

역사적 실물·고문서의 자체 제작 모조품은 실제 사료로 보이지 않도록 편집 일러스트로 분류한다.
