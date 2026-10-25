# VOL-03 V1.3 | 6점 연구용 미디어 로컬 설치 가이드
> 설치 패키지는 ChatGPT 산출물로 제공. GitHub에는 텍스트 검증 계약만 커밋; 이미지 6개 바이너리는 아직 없음.

## 사전 조건
1. REFORMATION-ATLAS 저장소가 로컬에 있고 docs/vol03-deep-research-v0-1 연구 브랜치를 사용 중인지 확인.
2. REFORMATION_ATLAS_VOL03_V13_INSTALL_PACKAGE.zip 파일을 다운로드.
3. ZIP을 임의의 새 폴더에 압축 해제. 안전한 기본값은 검증만 수행하는 것.

## 명령
패키지를 푼 디렉터리에서 다음을 실행한다.

    python3 install_candidates.py --bundle REFORMATION_ATLAS_VOL03_V13_INSTALL_PACKAGE.zip

실제 로컬 체크아웃에 후보 이미지 파일만 설치하려면 해당 저장소의 절대 경로를 지정한다.

    python3 install_candidates.py --bundle REFORMATION_ATLAS_VOL03_V13_INSTALL_PACKAGE.zip --repo /path/to/REFORMATION-ATLAS --install

실행 시 후보 6개를 assets/illustrations/vol03/candidates/에만 쓰고 승인/기존 이미지/공개 매니페스트는 건드리지 않는다. ZIP 패키지의 install_candidates.py는 텍스트와 해시 검증이 가능하다. 패키지 SHA256: b29df503033edc4f77b9c98a5154edb1549b8d1e48687b241eea64368d37bce7.

## 테스트 내역
- DRY RUN 6/6 SHA256, WebP 헤더, CRC PASS.
- 임시 repo 스테이징 설치 6/6 PASS.
- 동일 패키지 재설치 파일변경 0건 PASS.
- 대상 파일이 다른 내용으로 변조된 경우 덮어쓰기 거부 PASS.

## 남은 단계
실제 사용자 PC 설치·동기화 확인, 후보 수동 검수, 시대별 복식·건축·상징 전문가 검수, Human Approver 승인, 정식 아카이브 등록·사이트 배포는 별개 작업이다. 이 문서는 이를 자동 승인하지 않는다.

## 경로와 검증기 주의
- ZIP을 압축 해제한 폴더 안에서 실행할 경우 --bundle 인수는 **압축파일의 실제 경로**를 지정한다. ZIP이 한 단계 상위 폴더에 있다면 ../REFORMATION_ATLAS_VOL03_V13_INSTALL_PACKAGE.zip 형태로 입력한다.
- 실제 설치 뒤에는 python3 scripts/validate_vol03_v13_editorial.py를 실행한다. 스크립트는 후보 디렉터리가 없거나 6점 전체가 있는 경우를 허용하고, 설치된 파일을 등록 SHA256으로 검증한다.
- 원래 자산 매니페스트나 사이트 게시 상태는 변경되지 않는다.
