# VOL-03 · V1.2 사건 삽화·정본 기반 지도 후보 R3C01
> 2026-10-25 | DRAFT 연구용 | 기존 게시 승인과 원본 파일 불변

## 완료한 후보
1. **ILL-V03-01-R2C01** (설교): PNG/WebP 1280×720, 현대 AI 역사 상상화. 생성 시트에서 **설교 장면만 크롭**했으며 역사적 원본 이미지는 아니다. 베들레헴 예배당 실제 실내·후스 생전 초상의 정확한 복원을 주장하지 않는다.
2. **ILL-V03-02-R2C01** (협상): PNG/WebP 1280×720, 현대 AI 역사 상상화. 생성 시트의 회의 장면 일부를 **크롭**했다. 1433 프라하·1435 브르노·1436 이흘라바·1437 바젤 후속 조치 중 특정 하나를 시각적으로 인증하지 않는다.
3. **MAP-V03-02-R3C01**: 지금 GitHub 연구 브랜치의 `MAP-V03-02_oxford_prague.svg`을 **기준으로 다시 작성**한 별도 SVG. 본문의 도시점·선·전반 레이아웃을 수정하지 않고 *저술 영향 ≠ 실제 여행·사제 관계* 범례만 수정.
4. **MAP-V03-04-R3C01**: 지금 GitHub 연구 브랜치의 `MAP-V03-04_waldensian_reform_network.svg`을 기준으로 다시 작성한 별도 SVG. *문헌·신학적 교류 ≠ 방문 순서·이동로* 범례만 수정.

## 새 사건 이미지 파일 및 무결성
- 다운로드 파일 `REFORMATION_ATLAS_VOL03_V12_SCENE_CANDIDATES.zip`.
- SHA256: `6a1f27c8fc998e1961e15324f550702ca74287009f24468e95f5b8189dbc42d3`.
- PNG/WebP 2쌍과 출처 크롭 좌표/원본 마스터 파일명을 기계 판독 가능한 `MANIFEST.json`에 기록.
- ZIP CRC PASS, 파일 이미지 디코딩 PASS, 16:9 1280×720 확인.
- 잘못 생성된 인포그래픽 결과들은 **인포그래픽을 역사 화폭으로 사용하지 않으며** 장면 일부만 독립 후보로 추출. 크롭/업스케일링의 원본 패널보다 역사 고증이 더 높아지는 것은 아니다.

## 지도 기준 차이 해결
- 이전 V1.1 후보 지도는 **이전 대화 ZIP 자산**에서 시작해 GitHub 정본 SVG와 설명 문구가 일부 달랐다.
- 이번 새 R3C01 후보는 **연결된 GitHub SVG 원본을 다시 가져온 후** 설명 문자열 세 군데만 변경하는 방식으로 작성했다. 이전 ZIP 수정안을 그대로 복사해 정본이라 부르지 않는다.
- 신설 GitHub 후보 경로: `assets/maps/candidates/MAP-V03-02-R3C01_oxford_prague_research_links.svg`, `assets/maps/candidates/MAP-V03-04-R3C01_waldensian_exchange.svg`.
- 원래 `assets/maps/MAP-V03-02_oxford_prague.svg` 및 `MAP-V03-04_waldensian_reform_network.svg` 파일은 변함없음. 후보 SVG는 공개 자산 대장에 등록하지 않음.

## 고증 근거
- 프라하 관광기관의 베들레헴 예배당 안내는 1391년 설립·1402~1413년 후스의 설교·20세기 재건 사실을 보여준다. https://prague.eu/en/objevujte/bethlehem-chapel-betlemska-kaple/
- 체코 공과대학은 현재 복원된 내부가 15세기 본모습의 완전한 복제는 아니라고 설명한다. https://www.cvut.cz/en/the-bethlehem-chapel
- Fudge 2020 Šmahel 비평판 서평은 1433년 프라하 3개 핵심 합의·1435 브르노 협상·1436 이흘라바 선포·1437 후속 조치를 구분한다. https://scholarworks.iu.edu/journals/index.php/tmr/article/view/31313
- 정확한 장소·날짜·실제 인물·복식·문장(紋章)·책의 글씨·건물 표현은 사람 검증 이전까지 미확정.

## 수용 게이트 (현재 미승인)
- **기술:** 역사 장면 2개 후보 PNG/WebP 디코딩·해시 정상. R3C01 SVG 두 파일의 기술적 텍스트 변환 성공. GitHub SVG 픽셀 렌더/외부 실측 고증은 별도 확인.
- **내용:** 각 자산의 이미지 문맥·연도·건축·문장·복식은 역사학자 검수 필요.
- **게시:** 원본 182노드·365관계, 14개 주장, 기존 `ILLUSTRATION_STAGE.json`과 `asset_manifest.json`, 웹 `media_safe_to_display=false` 전부 그대로. `approved=false`, `can_ship=false`.
- **사람 최종 결정:** 별도 사용자 판정과 외부 전문가 감수 없이 ACCEPTED/LOCKED/PUBLISHED 상태로 옮기지 않음.
