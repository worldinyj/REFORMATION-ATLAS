# V5.35 인물화 2차 — 등록 준비

기존 AI 창작 2분할 삽화에서 두 개의 887×887 WebP를 분리한 패키지. 역사적 외모의 증거가 아니며 기존 상징 카드를 대체하지 않는다. ZIP과 각 파일의 SHA256은 portrait_manifest.json에 고정했다. **이 커밋에는 WebP 자체가 포함되어 있지 않다.** 현재 연결된 GitHub 텍스트 작업 환경과 로컬 파일 사이의 바이너리 전송 제한으로 사용자 다운로드 패키지와 저장소 등록 도구를 분리했다.

## 등록 방법
연구 브랜치를 최신 상태로 동기화한 로컬 저장소에서 실행:
```sh
python3 research/v535/visual/people_v2/import_portraits.py /path/to/ATLAS_V535_portrait_pilots.zip
git status --short
```
스크립트는 해시와 브랜치를 확인한 후 파일만 복사한다. 자동 커밋·푸시는 하지 않는다. 검토 후 별도 커밋하고 상태를 갱신한다. 현재 can_ship=false.

## 통합 자산 색인
visual_integration_candidate.json: 8 지도, 5 연표·문헌 도해, 10 상징 카드. 이전 감사 기록 확인. 전 파일 재검사, 브라우저 QA, 실제 웹앱 적용은 미완료.
