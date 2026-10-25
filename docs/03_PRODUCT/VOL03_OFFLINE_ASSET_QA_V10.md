# 제3권 V1.0 · 로컬 매체 파일 기술 재검증
> 2026-10-25 · 연구 시점 로컬 대화 아티팩트 검사. GitHub 전체 체크아웃 또는 GitHub Actions 수행 결과가 아님.

## 실제 수행
- `REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip`: SHA256 `571d80c7ee3f0722bc07c76e5760aeac2795d67c4bc96d000d699bda65ac35a3` 기록과 **일치**, ZIP CRC PASS.
- 원래 WebP 6점: 각 파일과 `ILLUSTRATION_STAGE.json` 기록의 SHA256 모두 **6/6 일치**, 이미지 디코더 확인 **6/6 통과**.
- 지도 `MAP-V03-01~04`: 편집 가능한 SVG 4개의 XML 파싱 **4/4 PASS**, 각각 SVG `viewBox=0 0 1500 900`.
- Word `REFORMATION_ATLAS_VOL03_V09R2_Research_and_G4_Review.docx`: SHA256 `35f7c9943e5126466b0d9f29686d96e1d64bb601ef635969d1a50450fd9ca3ef` 기록과 **일치**, DOCX 내부 CRC PASS, 매체 10점, 기존 렌더 PNG 15점 확인.
- 읽기 전용 로컬 QA 상세 JSON 별도 대화 아티팩트: `REFORMATION_ATLAS_VOL03_LOCAL_MEDIA_QA_R3.json`.

## 수행하지 못한 검증
- GitHub API로 원본 콘텐츠 JSON/참조 검사를 하는 이전 P3 결과는 유효하게 보존하지만, `scripts/validate_vol03_v09_batch.py` 및 다른 세 개 저장소 Python 스크립트를 **실제 전체 체크아웃에 대해 실행하지 못함**.
- 이유: 이 실행 환경의 shell에서 GitHub 도메인의 DNS 조회가 실패해 `git clone` 불가. GitHub 커넥터는 브랜치 파일을 별도로 읽고 쓸 수 있어 연구 브랜치 내용은 관리 가능.
- Word에서 확인된 15개 PNG는 **기존 세션이 생성한 렌더 이미지 개수 확인**이며 이번 작업에서 Word 렌더 프로그램을 새로 실행했다고 주장하지 않음.
- 로컬 백업 시뮬레이션과 GitHub Actions는 실행하지 않음.

## 로컬 동기화 후 사용자가 실행할 명령
```bash
git fetch origin
git switch docs/vol03-deep-research-v0-1
git pull --ff-only
python3 scripts/validate_content.py
python3 scripts/validate_vol03.py
python3 scripts/validate_vol03_catalog.py
python3 scripts/validate_vol03_v09_batch.py
python3 scripts/validate_vol03_v09_batch.py --illustrations-zip ~/Downloads/REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip
```
- 이 명령은 **이미지 설치가 안 된 상태**를 전제로 하며 ZIP 경로는 다운로드 실제 위치에 맞게 변경해야 한다.
- ZIP 이미지는 승인 전 설치되지 않으므로 게시·미디어 스테이징 게이트는 계속 닫아 둔다.
