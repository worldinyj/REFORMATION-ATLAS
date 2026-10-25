# VOL-03 V1.4 · G4-A adapter & image-generation rejection QA
> 2026-10-25 · DRAFT / NOT PUBLISHABLE

## 수행 내용
1. **시각자료 반려:** 기존 고위험 `ILL-V03-02-R2C01`을 실제로 대체할 16:9 한 장면 회화를 요청했으나, 출력 2건 모두 여러 사건/지도/연대표를 합친 포스터였다. 둘 다 불합격 처리, 교체 승인 0건.
2. **G4-A 프로그램 개발:** `scripts/build_vol03_g4_projection.py`를 추가해 기존 연구 그래프의 182개 노드/365개 에지, 14개 주장, 글로벌 ID, 원래 출처 링크, 사건 연대의 원문 정확도를 읽기 전용으로 보존하고 웹 공개는 0으로 고정.
3. **CI 1차 실패와 복구:** 3개 사건 `EVT-0008/0013/0017`은 `date_precision=approximate_year`인데 G4 계약 목록에 누락되어 첫 검증이 실패. 원래 날짜를 바꾸지 않고 계약에 `approximate_year`을 보완.
4. **실제 Actions 성공:** 수정 커밋 `fab65115aab96055b7293dd3e9566ccc36821a11`, 워크플로 실행번호 **40180354821** / status=completed / conclusion=success. https://github.com/worldinyj/REFORMATION-ATLAS/actions/runs/40180354821

## Word 검토본
- `REFORMATION_ATLAS_VOL03_V14_G4_and_Art_Gate_Review.docx`: A4 **3쪽**, 5개 표, 모든 페이지 PNG 렌더·접근성 검사 (high=0, medium=0, low=0).
- SHA-256: `5bb8c3d2ba02d9594d0cefee57d9a5734d2a85d781acc24af938f7a4427ec268`.
- 해당 Word는 사용자 대화 다운로드 산출물이며 저장소에는 바이너리를 업로드하지 않음.

## 안전·승인 상태
- 원래 182/365 통합 그래프·14개 주장·기존 정식 지도·인물화·사건화 바이너리 및 `asset_manifest.json`은 수정하지 않았다.
- 이미지 WebP 6점의 **사용자 Mac 실제 설치는 미실행**; ZIP은 보관/기술 검증만 완료한 자료다.
- 원전 전면 교감, 고위험 이미지 복식·문장·건축 전문가 판단, 사용자 수용 결재는 미완료.
- `publication_gate.approved=false`, `can_ship=false`; Draft PR #2 유지, `main` 미병합.
