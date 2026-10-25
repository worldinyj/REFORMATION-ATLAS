# VOL-03 V1.1 R2C01 · 후보 미디어 파일 및 Word QA
> 2026-10-25 · DRAFT · 시안 제작·렌더 확인. 역사 고증 최종 승인/공개가 아니다.

## 대화 산출물
| 파일 | 내부 품질 | GitHub 반영 범위 |
|---|---|---|
| `REFORMATION_ATLAS_VOL03_V11_CANDIDATES.zip` | 16개 파일, CRC PASS; SHA256 `8ae5c9e1a96fa0813ed157eab2ad57fdaaddcb02d0dee787ed0ef0ff3c9e6930` | 미디어 파일 미업로드. 해시/설명만 |
| `REFORMATION_ATLAS_VOL03_V11_Visual_Revision_Review.docx` | **A4 5쪽** 렌더 5/5, 그림·표 배치 육안 점검. a11y high=0, medium=0, low=0. SHA256 `0d89f8cadad1a76b3f69a8d9efcd4cae3626196c5f77551724c53ea4a5294cc2` | Word 바이너리 미업로드 |

## 이미지/지도 세부
- 인물화 수정 후보 PNG/WebP 4쌍, 원본 신형 마스터 1점, 원본 대비 비교 시트 1점.
- 지도 후보 2종, 1500×900 SVG 및 PNG 각각 1점. SVG XML 파싱 및 PNG 렌더 통과.
- 이전 지도 ZIP과 현 GitHub 정본 SVG 사이의 주석 차이를 발견했으므로 후보 SVG는 여전히 **로컬 후보 ZIP 전용**. 버전 기준을 확정하기 전 GitHub SVG를 무조건 덮어쓰지 않음.
- 원래 자산의 `assets/asset_manifest.json`과 `ILLUSTRATION_STAGE.json`은 수정하지 않음.
- 사건 삽화 `ILL-V03-01/02`의 신규 그림은 **없음**. 생성기의 무관한 인포그래픽 결과 2점은 불채택하여 산출물에서 제외.

## 상태
- R2C01 후보 6점은 '제작 완료 / 고증 승인 대기'이다. 고위험 원본 7점 중 5점에 후보가 있고 2점은 미제작.
- 외부 전문가 이미지 고증 및 사용자 승인 없음. Draft PR #2, `main` 미병합.
- 정식 배포 플래그 `approved=false`, `can_ship=false`.
- 원전 검증·사료 전문 열람·역사 사실 승인과 파일 기술 QA는 별개의 작업이다.
