# 제3권 V1.3 역사 시각자료 고증 판정표
> 2026-10-25 / DRAFT / 전문가 학술 승인 또는 게시 승인 아님.

## 기술 검증과 역사적 고증은 별개
- 연구용 이미지 ZIP SHA-256: `b29df503033edc4f77b9c98a5154edb1549b8d1e48687b241eea64368d37bce7`.
- 이 환경에서 ZIP CRC, 6점 WebP 개별 체크섬을 확인. 읽기 전용 검증 PASS.
- **격리된 임시 저장소**의 설치 시험: 첫 실행 6개 복사, 두 번째 재실행 0개 복사. 실제 사용자 맥북 저장소에는 설치하지 않음.
- 이 테스트는 역사 고증, 인물의 생전 초상, 웹 게시·사용자 승인 완료가 아니다.
- 변경 대상은 후보 6장(인물 4, 사건 2)이고, 지도 후보 2종은 이미 GitHub 정본으로부터 분기된 DRAFT SVG. 원본 전부 보존.

| 후보 | 기존 위험도 | 명시해야 할 한계 |
|---|---|---|
| PRT-V03-01-R2C01 | HIGH | 발도의 실제 외모·거리·복식은 확인되지 않았다. 평신도 설교를 묘사한 상상화다. |
| PRT-V03-02-R2C01 | HIGH | 위클리프의 실재 얼굴과 14세기 서재·필사본의 모습은 미확인이다. |
| PRT-V03-03-R2C01 | MEDIUM | 얀 후스의 상상 초상이며 설교 배경은 당시 예배당 실측 복원이 아니다. |
| PRT-V03-04-R2C01 | HIGH | 지슈카의 실제 얼굴·눈 부상 방향·당시 장비는 확정할 수 없다. |
| ILL-V03-01-R2C01 | HIGH | 프라하 설교 분위기의 AI 상상 장면. 베들레헴 예배당 내부 복원 아님. |
| ILL-V03-02-R2C01 | HIGH | 공의회·보헤미아 협상의 일반적 상상 장면. 1433/1435/1436의 특정 회의 재현 아님. |
| MAP-V03-02-R3C01 | HIGH | 저술 영향의 개념적 연결. 직접 여행로나 직접 사제관계 아님. |
| MAP-V03-04-R3C01 | HIGH | 문헌·신학 교류의 개념적 연결. 실제 방문 순서·여정 아님. |

## 출처 교차검증
- [EXT-V03-01] 발도의 Peter 호칭 후대 귀속: https://www.waldensian.org/history/myths-surrounding-the-waldensian-story/
- [EXT-V03-02] 지슈카의 얼굴·눈 부상 복원 한계: https://www.arup.cas.cz/en/statement-aru-arub/
- [EXT-V03-03] 베들레헴 예배당 재건 내부 원형과 다름: https://www.cvut.cz/en/the-bethlehem-chapel
- [EXT-V03-04] 후스 설교기 1402~1413: https://prague.eu/en/objevujte/bethlehem-chapel-betlemska-kaple/
- [EXT-V03-05] Pálka 2019: 1436년 7월 5일 콤팍타타 선포: https://cms.flu.cas.cz/wp-content/uploads/2022/03/SMB_11_177-212-0a0.pdf
- [EXT-V03-06] 1436년 7월 6일 옛 체코어 문안 낭독: https://dbs.herder-institut.de/digitale-angebote/dokumente-und-materialien/themenmodule/quelle/3255/details/4733.html
- [EXT-V03-07] 브르노 1435년 7월 편집자 추정·원문 무날짜: https://www.rbmonline.cz/portal/book/1199?lpage=445
- [EXT-V03-08] 1433 합의와 2019 비평판 10문서 구별: https://scholarworks.iu.edu/journals/index.php/tmr/article/view/31313

## 문헌학적 수정사항
- 브르노 교섭문 초안은 원문에 특정 날짜가 없고 후대 편집자가 **1435년 7월**로 추정한 텍스트다.
- Pálka(2019)의 역사 연구는 콤팍타타의 **1436년 7월 5일 이흘라바 공적 선포**를 서술한다.
- Herder-Institut의 문헌 해설은 **7월 6일 이흘라바 성 야고보 교회에서 옛 체코어 번역 집행문서 낭독**을 따로 설명한다.
- 1433 합의의 핵심 3문서와 2019년 비평판 관련 10문서는 다른 문서군이다. 비평판 라틴 원문 전문은 미열람.

## 외부 전문가·사람 승인까지 보류
- [ ] 12~15세기 복식·설교대·책·갑옷·문장에 대한 전문가 검토
- [ ] 이미지별 출처/생성 이력/제3자 유사성 및 권리 확인
- [ ] 라틴·체코어 필사본/근대 편집판의 문장 교감
- [ ] 사용자 시각적 수용 판정
- [ ] 승인 자료만 공개/교체하는 별도 PR 및 게시 QA

모든 레코드의 `review_status=DRAFT`, `public_visible=false`, `approved=false`, `can_ship=false`. 정식 이미지 설치는 사용자가 로컬 저장소를 동기화한 후 별도 수행.
