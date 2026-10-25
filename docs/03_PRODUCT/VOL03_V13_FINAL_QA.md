# VOL-03 V1.3 · 필수 작업 진행 최종 기술 QA
> 2026-10-25 · DRAFT / HISTORIAN REVIEW PENDING / NOT PUBLISHABLE

## 실제 완료한 편집
- 제3권 본문 5개 장: 발도, 위클리프, 얀 후스, 후스파, 프라하 4개조·콤팍타타의 원전·도상·건축 유의 문단 편집.
- 06 연대표: 1432년 체브, 1433년 프라하, 1435년 브르노, 1436년 이흘라바, 1437년 바젤의 분리와 1435년 특정 문서의 편집자 추정 날짜 구분.
- 07 사실검증표: 베들레헴 예배당 현대 복원, 지슈카의 현대 얼굴 복원과 문장(紋章)·복식의 역사적 불확실성, 교류 지도 범례.
- 시각자료 8점의 편집 검토 결정 기록: 7점 REVIEW_PENDING + 협상 삽화 ILL-V03-02-R2C01 1점 REVISE_HIGH. 모두 승인/공개 0건.

## 로컬 이미지 설치용 패키지 기술 QA
- REFORMATION_ATLAS_VOL03_V13_INSTALL_PACKAGE.zip.
- SHA256: b29df503033edc4f77b9c98a5154edb1549b8d1e48687b241eea64368d37bce7.
- WebP 6점의 SHA256/파일 크기/헤더와 ZIP CRC 검사 PASS.
- 설치 스크립트 테스트: 검증만 6/6 PASS, 격리 모형 저장소 후보 스테이징 복사 6/6 PASS, 두 번째 설치 0개 변경, 다른 내용의 기존 파일 덮어쓰기 거부 PASS.
- 사용자의 Mac 저장소 및 GitHub에 이미지 바이너리를 설치한 것은 아니다. 원래 자산 매니페스트와 게시 플래그를 변경하지 않음.
- 후보의 로컬 설치 유무에 따라 검사기 V1.3은 미설치 또는 6점 전부의 해시가 일치할 때만 수용하도록 보완했다.

## 11쪽 Word 통합 검토본
- REFORMATION_ATLAS_VOL03_V13_Integrated_Editorial_Review.docx.
- 기존 V1.2 7쪽에 V1.3 심사 결론·본문 수정·설치/검증·승인 기준을 추가한 총 11쪽.
- SHA256: be7ba7b84baffdd083b1eeed7bc981e780186fc7b129c44d85a6c70383e4cc71.
- DOCX 전체 11쪽 PNG 렌더 검토, 접근성 감사 high=0 medium=0 low=0.
- Word/ZIP은 ChatGPT 다운로드 산출물이며 GitHub 바이너리로 저장하지 않음.

## 실제 GitHub Actions
- V1.3 추가검증을 포함한 브랜치 실행번호 **40179437252**: completed, success.
- 결과: https://github.com/worldinyj/REFORMATION-ATLAS/actions/runs/40179437252
- 실행 대상: 기존 5개 표준 라이브러리 Python 검증 + scripts/validate_vol03_v13_editorial.py. 역사적 진실성을 보증하는 테스트가 아니라 저장소의 참조/게시/파일게이트 기술 검사다.
- 앞서 기존 자료 182 노드·365 관계·14 주장, 원본 자산 파일을 보존하였고 새 이미지 후보는 공개 0건.

## 남은 필수 게이트
1. 중세 원전의 전문·판면/필사본 교감 및 2019년 Šmahel 비평판 라틴 문서 10건 검토.
2. 8점 후보의 외부 역사미술사/건축/복식/문장 전문가 판단; 특히 협상 이미지의 붉은 예복·문장 수정.
3. 사용자 PC의 실제 미디어 후보 파일 설치·로컬 회귀검증.
4. 사용자의 후보별 채택/재제작/제외 결정 및 승인 기록.
5. 이후에만 원본 이미지 승격, 공개 매니페스트 반영, main 병합·사이트 배포 검토.

**상태: EDITORIAL_REVISED · TECHNICAL_QA_PASS · HISTORICAL_APPROVAL_PENDING.**
