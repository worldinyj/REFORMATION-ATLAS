# VOL-03 · 이미지 스테이징(아직 GitHub 바이너리 미포함)

6개 신규 AI 역사 재현 이미지의 바이너리는 대화에서 제공한 `REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip`에만 들어 있습니다. 로컬 동기화 전까지 GitHub에는 **원본을 업로드한 것으로 간주하지 마세요**.

현재 GitHub에 있는 자산은 다음과 같습니다.

- [ILLUSTRATION_STAGE.json](ILLUSTRATION_STAGE.json): 각 WebP 이름, SHA-256, 인물/사건 관계, 출처, 역사적 위험, DRAFT 상태.
- [고증·시각 기준](../../../docs/02_MEDIA/VOL03_ORIGINAL_ARTWORK_V01.md)
- [QC 체크리스트](../../../docs/02_MEDIA/VOL03_ART_QA_GATE_V01.md)
- [로컬 설치 스크립트](../../../scripts/install_vol03_illustrations.py)

## 이후 로컬에서 진행할 명령
```bash
# 이 브랜치를 로컬에 받은 상태에서 실행
python3 scripts/install_vol03_illustrations.py \
  ~/Downloads/REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip

# 검사 성공한 경우에만 설치 (WebP 6점 + 자산 등록)
python3 scripts/install_vol03_illustrations.py \
  ~/Downloads/REFORMATION_ATLAS_VOL03_ILLUSTRATIONS_V01.zip --install

python3 scripts/validate_vol03.py
git status --short
```

경로 `~/Downloads`는 예시이므로 실제 ZIP 위치에 맞게 변경하세요. 설치 이후에도 사람의 고증·최종 승인 전까지 DRAFT를 유지합니다.
