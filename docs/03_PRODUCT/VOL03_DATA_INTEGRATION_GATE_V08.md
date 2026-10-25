# VOL-03 · 5순위 통합 그래프와 6순위 Word 검토본 (V0.8)
> 2026-10-25 · DRAFT. 정식 사이트 데이터베이스 설계 또는 최종 승인본이 아닙니다.

## 1. 이번에 저장한 통합 색인
`data/vol03_integrated_catalog_v08.json`은 기존 자료를 옮겨 놓은 **읽기 전용 연결 모델**입니다. 원본 JSON은 변경하지 않았으며 그 데이터가 기준입니다.

- 항목: **182개 노드** (기초 출처 SRC-0001~0010과 VOL03 출처 V03-S01~53 포함).
- 관계: **365개 연결선**. 인물·운동·사건·장소·관계 기록·문서판본·주장·신학 쟁점·이미지·지도·독자 화면을 연결.
- 연구 주장과 검증문헌은 별개 노드. `grounded_in` 에지로 실제 연구 출처 연결.
- 기존 SVG의 `REL-` 관계 ID는 별도 노드로 유지하여 도식 참조 무결성을 보존.
- 지도 4점은 GitHub 원본 SVG 존재 / DRAFT; 인물화 4점 + 사건 삽화 2점은 **메타데이터만** GitHub 존재 / 바이너리 로컬 설치 대기.
- 배포 상태 `approved=false`, `can_ship=false`.

## 2. 주요 관계 속성
| 연결 종류 | 의미 | 제한 |
|---|---|---|
| `grounded_in` | 문헌·판본·연구출처와 연결 | 출처 간 증거력 차이를 없애지 않음 |
| `relation_origin/target` | 원래 역사 관계 ID의 출발·도착 | 개인의 직접 사제관계를 임의 추론하지 않음 |
| `claim_about` | 주장이 다루는 인물·사건 | 주장 자체의 확실성은 `certainty`로 별도 관리 |
| `associated_place` | 운동·사건의 관련 도시 | 중세 건물·전장·이동로 좌표 아님 |
| `staged_portrait` | 인물 페이지의 AI 시각자료 후보 | 바이너리 미설치, 노출·배포 불가 |
| `imagines` | AI 삽화의 상상 재현 대상 | 동시대 실제 초상·현장 복원 아님 |

## 3. 설치 및 테스트
```bash
# 로컬 동기화 후 원전·연구 데이터·SVG 검증
python3 scripts/validate_content.py
python3 scripts/validate_vol03.py
python3 scripts/validate_vol03_catalog.py

# 별도 ZIP 다운로드 후, 소유자가 명시적으로 설치할 때만
python3 scripts/install_vol03_illustrations.py \
  ~/Downloads/REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip
python3 scripts/install_vol03_illustrations.py \
  ~/Downloads/REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip --install
```

로컬 설치 이후에도 이미지와 역사 문헌은 **DRAFT**이며 배포 게이트를 변경하지 않습니다.

## 4. Word 도록 포함 V0.8 (별도 대화 파일)
파일명: `REFORMATION_ATLAS_VOL03_Illustrated_Research_Review_V08.docx`.
- 기존 V0.5 연구·신학 해설 본문 유지.
- 지도 4점은 가로형 페이지에 한 점씩 수록.
- 발도·위클리프·후스·지슈카 이미지 4점과 설교·협상 삽화 2점, 캡션·고증 주의.
- 편집 QA 표와 승인 게이트를 마지막에 수록.
- **전체 32페이지 렌더링 및 시각 검사** (A4 세로 본문, 가로 도록, 세로 QA).
- GitHub에는 이 바이너리 Word나 PNG/WebP 원본을 업로드하지 않았습니다. 대화 아티팩트로 제공합니다.

## 5. 남은 게이트
- 라틴/체코어 원전 전면 교감, 학술 외부 감수.
- AI 인물화의 시대착오 여부와 장면의 건축·복식 검토; 필요 시 재제작.
- ZIP을 사용한 추후 로컬 이미지 설치, 코멘트 반영.
- 최종 Word의 사용자 승인과 권리 확인, `main` 병합.
- 개발기획 문서(PRD/TRD/UX/UI/TASKLIST)는 8권 연구 구조·공통 데이터 계약 승인 후 착수.

GitHub 연결로 참조 관계는 독립 점검했으나 GitHub Actions와 실제 로컬 전체 테스트를 **실행했다고 주장하지 않습니다**.

## 6. 아티팩트 품질 및 해시 기록 (2026-10-25)
- Word: `REFORMATION_ATLAS_VOL03_Illustrated_Research_Review_V08.docx`, **32페이지**, SHA256 `5a9f0f211bee97aad47d33697ac6b1b78b0ec27e0dbb86eca403980454275989`.
- 검토 묶음: `REFORMATION_ATLAS_VOL03_V08_REVIEW_BUNDLE.zip`, SHA256 `1abed4eadba035ddc827bd9fbc955a78d741d79e71cff5497d6141f9660d75c6`. Word 1점, 지도 SVG 4점, 지도 PNG 4점, 기존 AI 이미지 ZIP 1점, 검토 시트 2점, 체크섬 목록·안내 포함.
- ZIP 무결성 및 각 항목 SHA256 교차 검증 통과. 이미지 ZIP은 해시 변형 없이 중첩 포함.
- Word 편집: A4 세로 본문→A4 가로 도록→A4 세로 QA, **전체 32쪽 렌더링 후 육안 검토**. 지도 첫머리의 불필요한 분리 페이지를 수정하고 다시 렌더링.
- 문서·아트 ZIP은 ChatGPT 대화 아티팩트로만 전달. GitHub 바이너리 업로드/로컬 Git 동기화는 미실시.
