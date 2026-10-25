# VOL-03 V1.2 · 사건 삽화·지도 수정 후보 QA
> 2026-10-25 · DRAFT. 사용자 아티팩트 및 GitHub 연결 데이터 검증. 역사학·원전 인증 아님.

## 실제 확인
- 두 신규 장면은 ImageGen 복합 시트에서 크롭한 교육용 상상화다. 특정 설교 장소/회의 일시의 독립 역사 재현으로 주장하지 않는다.
- 2점 PNG/WebP 모두 **1280×720** 디코딩 확인; 독립 파일 SHA256은 `data/vol03_visual_candidates_v12.json`에 기록.
- ZIP `REFORMATION_ATLAS_VOL03_V12_SCENE_CANDIDATES.zip` (7개 파일), CRC PASS, SHA256 `6a1f27c8fc998e1961e15324f550702ca74287009f24468e95f5b8189dbc42d3`.
- R3C01 SVG 2종은 **현재 GitHub 원본 파일에서 설명 문구만 수정한 새 파일**이다. 연결된 GitHub 트리에서 두 후보 모두 존재 확인. 정확한 두 SVG의 로컬 픽셀 렌더 QA는 **추후 로컬 체크아웃**에서 수행할 것.
- GitHub 스냅샷 비교: 기존 통합 그래프, 주장, 자산 매니페스트, 이미지 스테이징, 페이지 공개 설정 및 정식 지도 2종의 Git blob SHA **7/7 불변**.
- 182노드·365관계, 주장 14개, 웹 노출 매체 0건, 공개 게이트 `approved=false, can_ship=false`.

## Word 보고서 QA
- `REFORMATION_ATLAS_VOL03_V12_Visual_And_Scene_Review.docx`
- V1.1 5쪽 Word를 보존하고 신규 장면·지도 게이트 2쪽을 부록으로 덧붙인 **A4 총 7쪽**, 인라인 그림 6개, 표 3개.
- 렌더 7/7쪽 및 전체 페이지 시각 점검 완료. 초기 표 헤더 접근성 중간 위험 1건을 수정한 뒤 **high=0, medium=0, low=0**.
- SHA256 `9edd11d7d8c552e22c2191dca6c89b0c0a7f0b16150ba19d468eed5faf0c3f12`.
- Word·씬 바이너리는 **대화 아티팩트**로만 제공, GitHub에는 QA 문서/후보 SVG/메타데이터만 저장.

## 자동 검증 경계
- `scripts/validate_vol03_v12_candidates.py`는 연구 브랜치 체크아웃에서 `python3 scripts/validate_vol03_v12_candidates.py`로 실행. 선택적으로 `--scene-zip <ZIP 경로>`를 전달하면 원본 ZIP CRC와 두 PNG/WebP의 해시를 검사한다.
- GitHub Actions 워크플로를 연구 브랜치에 추가해 실제 실행을 확인했으며, 그 결과는 아래 실행 기록에서 구분한다.
- 역사학 전문가 및 사람 승인·미디어 정식 원본 승격 전 `DRAFT` 유지.

## 실제 GitHub Actions 체크아웃 검증 (실행 확인)
- 첫 실행 `40178049479`은 실패. 원인: `scripts/validate_content.py`가 관계 레코드에 존재하지 않는 `name_ko`를 요구하여 2건 오류. 실제 관계 스키마의 `summary_ko`를 검사하도록 검증기를 수정한 후 재실행.
- `80a6362b3be877d6ce5deeb96a0da408f859c925` 커밋의 GitHub Actions 실행 **40178144052, completed / success**. 확인 URL: https://github.com/worldinyj/REFORMATION-ATLAS/actions/runs/40178144052
- 동일 실행 로그에서 `validate_content.py`, `validate_vol03.py`, `validate_vol03_catalog.py`, `validate_vol03_v09_batch.py`, `validate_vol03_v12_candidates.py` 총 **5개 검증 명령을 모두 실행·통과**. V0.9-P3 `issues=0` 및 V1.2 `issues=0` 확인.
- 해당 CI 작업은 ZIP을 포함하지 않은 저장소 검사. 실제 V1.2 ZIP SHA256/CRC·WebP PNG 파일 검사 및 Word 7쪽 렌더·접근성 QA는 **별도의 현재 대화 로컬 파일 확인** 결과다.
- 이 QA 기록 갱신 커밋의 워크플로는 별도 실행으로 표시된다. 위 성공을 아직 실행되지 않은 미래 커밋의 성공으로 치환하지 않는다.

**남은 제한:** 중세 사료의 전문 교감과 복식·건축·지슈카 도상의 전문가 고증은 여전히 미완료. `approved=false`, `can_ship=false`.
