# VOL-03 · 종교개혁의 선구자 | Deep Research V0.8
**상태: DRAFT** (기초 공개 학술자료를 토대로 한 심화 연구 초안, 사람의 역사학 감수 전)

## 읽는 순서
1. [00_VOLUME_EDITORIAL.md](00_VOLUME_EDITORIAL.md): 연구 대상, 용어, 편집 범위
2. [01_WALDENSIANS.md](01_WALDENSIANS.md): 발도·왈도파와 1532년 개혁파 연결
3. [02_WYCLIF_LOLLARDS.md](02_WYCLIF_LOLLARDS.md): 위클리프·영어 성경·롤라드파
4. [03_HUS_AND_PRAGUE.md](03_HUS_AND_PRAGUE.md): 후스와 프라하의 개혁
5. [04_HUSSITE_MOVEMENTS.md](04_HUSSITE_MOVEMENTS.md): 후스파 전쟁·프라하 4개조·형제단
6. [05_SYNTHESIS_AND_PITFALLS.md](05_SYNTHESIS_AND_PITFALLS.md): 계보·신학 차이·후대 수용
7. [08_THEOLOGY_EUCHARIST_COMPARE.md](08_THEOLOGY_EUCHARIST_COMPARE.md): 위클리프·후스·야쿠베크 성찬론 비교
8. [09_PRAGUE_ARTICLES_AND_COMPACTATA.md](09_PRAGUE_ARTICLES_AND_COMPACTATA.md): 1420~1437 협상의 역사
9. [10_WALDENSIAN_MEMORY_AND_SOURCES.md](10_WALDENSIAN_MEMORY_AND_SOURCES.md): 1532년과 후대 역사 기억
10. [06_TIMELINE.md](06_TIMELINE.md): 날짜 정확도를 함께 표시한 연대표
11. [07_FACTCHECK_MATRIX.md](07_FACTCHECK_MATRIX.md): 단정 금지와 검증 과제
12. [05_SOURCE_REGISTER.md](05_SOURCE_REGISTER.md): 학술·전시 출처 48건과 실제 접근 범위

## 연결 산출물
- [볼륨 3 구조화 확장 데이터](../../../data/vol03_extension.json): 추가 인물 6명, 운동 4개, 위치 8곳, 사건 16건, 관계 7개
- [자체 제작 편집 가능한 SVG 관계도](../../../assets/diagrams/AST-0002_vol03_movement-pathways.svg)
- [원본 매체 관리대장](../../../assets/asset_manifest.json)
- [VOL-03 검증 스크립트](../../../scripts/validate_vol03.py)

- [검증 수준별 주장 카드](../../../data/vol03_primary_claims.json): V0.3 원전 검증 11건, DRAFT
- [주장 카드 스키마 해설](12_CLAIM_DATA_GUIDE.md): 서지·번역·원문 접근 수준 구분

## 스코프와 권한
- 이 저장소에는 **원고 Markdown과 JSON/SVG가 기준 자산**이다.
- Word V0.2 검토본 및 갱신된 V0.3 원전 검증 증보본은 대화에서 별도 다운로드로 제공되며, 현재 GitHub의 바이너리 자산으로 커밋되지 않았다.
- 기존 `docs/foundation-v0-1` 브랜치를 기반으로 한 후속 작업이다. `main`은 변하지 않았다.
- `PR`을 `DRAFT`로 유지한다. 검토 완료 전 발표·공개 승인 금지.

## 후속 내용 검토 순서
- [ ] 공인된 원전 판본을 통한 후스 『교회에 관하여』 및 위클리프 성찬론 심화 검증
- [ ] 프라하 4개조·1436년 콤팍타타 원문 및 번역의 차이 검토
- [ ] 왈도파 여성 설교 참여, 1532년 찬포랑 세부 경과 교차 검증
- [ ] 개신교/가톨릭/체코 지역사 관점의 교차 감수
- [ ] 검증된 좌표·시점별 경계에 근거한 실제 역사 지도 별도 제작
- [ ] AI 생성 역사 재현 인물화의 정확성·표현 검수 및 승인
- [ ] 이후 16세기 종교개혁(VOL-04)과 교차 링크

## 원전 대조 V0.3
- [11_PRIMARY_SOURCE_AUDIT_V03.md](11_PRIMARY_SOURCE_AUDIT_V03.md): 직접 확인한 판본·장·쪽수·편집본 제한을 구분한 사료 검증 기록.
- 다음 원문 검증의 미완료 항목(후스 라틴어 비평판 및 콤팍타타 공식 문서 전문)은 **미확인** 상태 유지.

## V0.3 내용 교정 노트
- **1433년 핵심 문안 3개와 2019 비평판 수록 문서 10개**를 분리하여 설명(원문 전문 직접 대조는 미완료).
- 후스와 루터 활동 시기 차이를 '한 세대 이상'에서 '약 100년'으로 표현 교정.
- 신규 원전 검증 항목은 [11_PRIMARY_SOURCE_AUDIT_V03.md](11_PRIMARY_SOURCE_AUDIT_V03.md)에 연결.

## V0.4 문헌 판본 및 사료 계보
- [13_DOCUMENT_PROVENANCE_AND_EDITION_V04.md](13_DOCUMENT_PROVENANCE_AND_EDITION_V04.md): 프라하 4개조 1844/1937 편집본 구분 및 콤팍타타 1433 핵심 3문안/2019 학술판 10문서 구분.
- [문헌-판본 JSON](../../../data/vol03_document_witnesses.json): 8개 역사 문헌 및 온라인 전사/현대 학술판 객체.
- [역사 주장 카드](../../../data/vol03_primary_claims.json): 기존 11건에서 14건으로 확장.
- 1433-11-30의 잠정 합의와 1437-12-23의 후속 조치를 사건 ID EVT-0019·0020으로 추가하되, 원전 미대조임을 명시.
- 1436년 이흘라바 선포와 1433년 프라하 합의는 서로 다른 사건.

## V0.5 — 2순위 신학·역사 해설 보강
- [15 신학 7축 비교](15_THEOLOGICAL_COMPARISON_V05.md): 성경·설교·교회론·재산·성찬·양형성찬·강제력.
- [16 인과 사례 5건](16_CAUSAL_CASE_STUDIES_V05.md): 리옹·옥스퍼드/프라하·후스·후스파·왈도파 연대.
- [17 교단과 지역사의 관점](17_HISTORIOGRAPHY_PERSPECTIVES_V05.md): 가톨릭·개신교·체코 지역사, 실제 콤팍타타 해석 논쟁.
- [18 용어집과 학습문항](18_GLOSSARY_AND_LEARNING_V05.md): 역사 용어 20개, 독자 질문 10개.
- [쟁점/인과 JSON](../../../data/vol03_theology_causality.json): 7개 신학 축/5개 인과 사례, DRAFT.
- 제3권 지역 출처 `V03-S01~S47` 47건. 1순위 원전 심층 검증의 남은 과제는 미완료로 유지한다.
- 정식 인물화·역사 지도와 PRD·TRD 본격 개발은 다음 게이트. `main` 미병합.

## V0.6 — 3순위 편집형 역사 지도 SVG 4종
- [MAP-V03-01 · 리옹의 초기 왈도파](../../../assets/maps/MAP-V03-01_waldensians_lyon.svg)
- [MAP-V03-02 · 옥스퍼드–프라하 문헌 영향](../../../assets/maps/MAP-V03-02_oxford_prague.svg)
- [MAP-V03-03 · 1414~1436년 보헤미아 도시와 사건](../../../assets/maps/MAP-V03-03_bohemia_hussite.svg)
- [MAP-V03-04 · 1530~1532년 왈도파–개혁자 교류망](../../../assets/maps/MAP-V03-04_waldensian_reform_network.svg)
- [좌표 근거 및 역사적 정확성 한계](../../02_MEDIA/VOL03_MAP_SOURCES_V01.md) · [좌표 데이터](../../../data/vol03_map_points.json)
- 자체 제작 16:9 SVG, 텍스트·도형 편집 가능. 현대 도시 좌표를 사용한 역사 교육 개념도이며 **중세 국경·실제 여정·군사 이동 복원 아님**.
- 제3권 출처 `V03-S01~48` 등. 3순위 SVG 초안 완료, 역사 지리학 전문가 감수 및 정확한 옛 국경 지도는 별도 게이트.

## V0.6 — 3순위 역사 지도 4종(시각 검토본)
- [4종 원본 SVG 및 지도 사용법](../../../assets/maps/README.md)
- [좌표·지도 핀 데이터](../../../data/vol03_map_points.json): 지도당 현대 도시 중심 참조점과 링크의 역사적 의미를 별도 구분.
- [지도 QA 기록](../../02_MEDIA/VOL03_MAP_QA_GATE_V01.md): 한국어 글꼴 렌더 문제 수정, 4종 위치·역사 지도의 한계, 권리 관리, 남은 감수 과제.
- 각 SVG 파일은 `assets/asset_manifest.json`에서 `MAP-V03-01`부터 `MAP-V03-04`까지 등록.
- PNG 미리보기와 SVG ZIP은 대화 첨부로 제공됨; GitHub에는 **SVG 편집 원본과 메타데이터**가 관리되는 기준본.
- 현대 좌표 개념도이며 실재 중세 국경·단일 인물의 정확 이동경로를 나타내지 않음. 모든 지도 **DRAFT**.
- 다음 4순위는 역사 재현 인물화와 사건 삽화 제작이며, 1순위 문헌 대조 및 최종 지도 전문가 검수는 남음.

## V0.7 — 4순위 인물화 4종·사건 삽화 2종
- [제작 고증·화풍 기준](../../02_MEDIA/VOL03_ORIGINAL_ARTWORK_V01.md) · [6점 QC 게이트](../../02_MEDIA/VOL03_ART_QA_GATE_V01.md).
- [바이너리 스테이징 해시 대장](../../../assets/illustrations/vol03/ILLUSTRATION_STAGE.json) · [추후 로컬 설치 명령](../../../assets/illustrations/vol03/README.md).
- **대화 ZIP에 PNG 6점 + WebP 6점 + 원본 마스터 2점 + 검토 시트·메타데이터를 포함**. 실제 이미지의 GitHub 바이너리 커밋은 아직 미완료.
- 새 인물·도상 근거 V03-S49~53을 포함해 출처 대장 총 53건. 고증·최종 공개 승인 대기, `main` 미병합.
- 로컬 동기화 전에는 위 스테이징 JSON만 GitHub에 있으며 웹사이트 경로에 이미지가 설치된 것으로 표시하지 않는다.

## V0.7 — 5순위 콘텐츠 데이터 연결 시범
- [웹 콘텐츠 색인 JSON](../../../data/vol03_presentation_index.json): 인물 페이지 4건, 역사 장면 2건, SVG 지도 뷰 4건, 심화 연구 뷰 4건.
- [안전한 웹 연결·접근성·미디어 게시 제약](../../02_MEDIA/VOL03_WEB_PRESENTATION_BRIDGE_V01.md).
- 이미지 6점은 아직 GitHub 실물 바이너리가 없으므로 `media_safe_to_display=false`, 모든 게시 상태는 `DRAFT` 및 `can_ship=false` 유지.
- 검증 스크립트가 각 인물·장소·원고·출처·이미지 스테이지를 검토. 이 자료는 정식 PRD/TRD/UX/UI 승인이 아니며 향후 프로젝트 기획 문서 작성의 근거가 된다.

## V0.8 — 5순위 통합 데이터 모델 + 6순위 도록 포함 Word
- [통합 연구 그래프 182항목/365관계](../../../data/vol03_integrated_catalog_v08.json): 기초 SRC 10건·제3권 V03-S 53건도 독립 소스 노드로 포함.
- [통합 데이터 모델 검증 도구](../../../scripts/validate_vol03_catalog.py): 그래프·출처·GitHub 자산 경로·미설치 이미지·배포 금지 게이트 검사.
- [검수/설계 경계 기록](../../03_PRODUCT/VOL03_DATA_INTEGRATION_GATE_V08.md): 5순위 통합 초안과 6순위 Word 제작 범위·남은 연구 과제.
- 외부 다운로드 전용 Word: `REFORMATION_ATLAS_VOL03_Illustrated_Research_Review_V08.docx` · **32쪽, SHA256 `5a9f0f211bee97aad47d33697ac6b1b78b0ec27e0dbb86eca403980454275989`**.
- 지도 4 SVG/PNG·역사 재현 AI 이미지 6 PNG/WebP·Word 포함 검토 패키지: `REFORMATION_ATLAS_VOL03_V08_REVIEW_BUNDLE.zip`, **SHA256 `1abed4eadba035ddc827bd9fbc955a78d741d79e71cff5497d6141f9660d75c6`**.
- Word 32쪽 전체 렌더 검사 및 역사 재현 표시. 패키지 내부 파일 SHA256 검사·ZIP CRC 통과. **바이너리 Word/PNG/WebP는 GitHub에 미커밋**.
- `main` 병합·전문가 검수·역사적 승인·사이트 공개는 보류. 

## V0.9-P1 — 원전·판본 심층 재검증 (2026-10-25)
- [20_PRIMARY_TEXT_REAUDIT_V09_P1.md](20_PRIMARY_TEXT_REAUDIT_V09_P1.md): 위클리프·후스·프라하 4개조·바젤 콤팍타타의 **원전/후대 편집/번역/서평** 근거 등급을 분리한 검토 보고서.
- [증거 등급 JSON](../../../data/vol03_source_audit_v09_p1.json): 신규 감사 레코드 10건, 기존 주장 CLM-V03-001~014 전체를 참조하며 기존 주장 14건 및 통합 그래프 182/365의 원본은 변경하지 않음.
- [QA 기록](../../03_PRODUCT/VOL03_SOURCE_REAUDIT_QA_V09P1.md): 고아 출처/주장 ID 0건 및 Word 검토본 렌더·접근성 결과.
- 독립 Word 검토본: `REFORMATION_ATLAS_VOL03_Source_Audit_V09P1.docx` (8쪽, SHA256 `eafde01842216663576731791227ba863cdc2ad645d7f00a72f5936527492f0a`). ChatGPT 대화 아티팩트만 제공, GitHub 바이너리 미수록.
- **DRAFT / 미출판.** 라틴어 필사본 교감·1844/1937 비교·2019 비평판 전문·인간 학술감수 미완료. Draft PR #2 유지, `main` 미병합.

## V0.9-P1 A~D · V0.9-P2 시각자료 및 P3 데이터 연결 (2026-10-25)
- [P1A 위클리프 원전·OCR 대조](21_WYCLIF_TEXT_COLLATION_V09_P1A.md): 1892년 Loserth OCR Ch IV/V, Trialogus 저작 귀속 구분; 원판 이미지와 중세 필사본 직접 교감 미완료.
- [P1B 후스 라틴-영어 대조 게이트](22_HUS_LATIN_TRANSLATION_GATE_V09_P1B.md): Schaff 1915 영어 번역 확인, 라틴어판 장·절 직접 비교 HOLD.
- [P1C 프라하 4개조 1844/1937 비교](23_PRAGUE_1844_1937_TEXT_LAYERS_V09_P1C.md): Archiv český III pp.213–216 온라인 OCR과 1937 전사 비교. 인접한 1421 다른 다섯 요구 문서를 1420 프라하 4개조로 오인하지 않음.
- [P1D 콤팍타타 문서·승인 연대](24_COMPACTATA_DOCUMENT_GATES_V09_P1D.md): 1433 3개 원 문안 / 2019 10개 비평 문서 / 24개 필사본 구분, 법적 효력 교감 미완료.
- [P1A-D 근거 등급 JSON](../../../data/vol03_batch_source_review_v09.json): 4개 검토 레코드와 기존 14개 CLM 전체 연결.
- [P2 이미지·지도 10점 검수 기록](../../02_MEDIA/VOL03_VISUAL_QA_V09_P2.md): 원본 그림 6점과 지도 4종, 7점 HIGH·3점 MEDIUM. [기계 판정용 JSON](../../../data/vol03_visual_review_v09_p2.json).
- [P3 저장소 관계/게시 게이트 QA](../../03_PRODUCT/VOL03_BATCH_QA_V09_P3.md): 182노드·365에지·14개 주장·10시각자료, 누락 ID 0건. [독립 검증 스크립트](../../../scripts/validate_vol03_v09_batch.py).
- 과거 바이너리·기존 본문·원래 182/365 통합색인은 불변, Draft PR #2 유지, `main` 미병합 및 공개 승인 금지.

- V0.9 사용자용 Word `REFORMATION_ATLAS_VOL03_V09_BATCH_REVIEW.docx` (12쪽, SHA256 `44467b08b3e6a4263fd2a3e68c2561c0d858c37f5444679b0529e3689b2860c5`), 교육 지도·기존 AI 그림 ZIP이 함께 포함된 `REFORMATION_ATLAS_VOL03_V09_BATCH_REVIEW_BUNDLE.zip` (SHA256 `c730b1d1db34828b37b64398e41319515a1a982b4dfb5417b40c84e31e6a68b2`). 대화 다운로드 전용, GitHub 바이너리 미수록.

## V0.9-P4 — 독자 표시·안전 캡션과 데이터 연결 (2026-10-25)
- [25_READER_DISPLAY_AND_CAPTION_V09_P4.md](25_READER_DISPLAY_AND_CAPTION_V09_P4.md): AI 인물화 4·사건 장면 2·SVG 지도 4의 역사 고증 문구, 독자용 설명, 대체 텍스트, 실제 이동 경로 오인 방지.
- [10점 미디어/14개 역사 주장 연결 오버레이](../../../data/vol03_editorial_overlay_v09_p4.json): 출처/대상 누락 0건, `show_in_public=false` 및 승인 대기 유지. 기존 Markdown·통합 그래프·이미지 바이너리 수정 없음.
- [G4 8권 공통 데이터 계약 연구용 초안](../../03_PRODUCT/G4_ATLAS_DATA_CONTRACT_V01.md) · [계약 JSON](../../../data/contracts/atlas_contract_v01.json) · [검증 상태](../../03_PRODUCT/G4_DATA_READINESS_V01.md). 글로벌 ID를 재활용하고 원전/편집본/번역, 역사 확실성/공개 승인을 서로 구분. **정식 G4 및 G5 승인 아님**.
- 원전 원문 교감·7개 HIGH 시각자료의 전문가 고증, 사용자 승인과 로컬 전체 Python 테스트는 여전히 별도 게이트.
