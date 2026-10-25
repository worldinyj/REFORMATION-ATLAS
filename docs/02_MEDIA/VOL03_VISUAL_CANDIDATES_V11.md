# 제3권 V1.1 · 고위험 역사 시각자료 수정 후보 R2C01
> 2026-10-25 · DRAFT. 공개 승인·역사 미술 고증 완료 아님.

## 이번에 실제로 제작한 파일
- 별도 ZIP **`REFORMATION_ATLAS_VOL03_V11_CANDIDATES.zip`** (SHA256 `8ae5c9e1a96fa0813ed157eab2ad57fdaaddcb02d0dee787ed0ef0ff3c9e6930`).
- 인물화 신규 **4점**(발도·위클리프·후스·지슈카): 765×508 독립 PNG/WebP 각각 한 점. 공통 회화적 제작 마스터 1점 포함.
- 교육 지도 개선안 **2종**(옥스퍼드–프라하와 왈도파 교류망): 1500×900 SVG/PNG. 문헌/사상 관계 점선을 실물 이동로로 오인하지 않도록 수정.
- **사건 삽화 2점은 생성 미완료.** 두 번의 잘못 생성된 정보 대시보드 이미지를 역사 이미지로 사용하지 않고 ZIP에서도 제외.
- 원본 인물화 4점과 신규 후보 4점의 전후 비교 시트를 ZIP에 수록.

## 고위험 검토표
| 대상 | 개선 취지 | 남은 고증 위험 |
|---|---|---|
| 발도(평신도 설교자) | 고딕 대성당 실경·성직자 인상 축소 | 실제 얼굴·중세 거리·책과 복장 |
| 위클리프 | 옥스퍼드 탑 등 후대 건축 배경 제거 | 필사본·서재·복식의 14세기 정확성 |
| 후스 | 후대 도상과 특정 베들레헴 예배당 내부로의 오인 감소 | 외모·설교대·당대 청중 등 |
| 지슈카 | 얼굴과 어느 눈을 잃었는지를 단정하지 않는 뒷모습 구도 | 군사 복식·전투 장소·장비 |
| 옥스퍼드–프라하 | '저술 영향'과 '사람 여행' 구분 | 당시 필사본 전파 경로의 실증 |
| 왈도파 네트워크 | '신학적 교류'와 '방문 여정' 구분 | 문헌별 도시·시기의 정확한 경계 |

## 검증 가능한 근거
- [American Waldensian Society — Waldo](https://www.waldensian.org/history/waldo/) : 초기 왈도파 지도자의 평신도 성격.
- [American Waldensian Society — Myths](https://www.waldensian.org/history/myths-surrounding-the-waldensian-story/) : 'Peter'라는 호칭의 후대 귀속.
- [Czech Academy of Sciences — Jan Žižka](https://www.avcr.cz/cs/veda-a-vyzkum/biologicko-ekologicke-vedy/Pred-600-lety-zemrel-husitsky-vojevudce-Jan-Zizka.-Jeho-pribeh-dodnes-budi-vasne/) : 지슈카 생전 초상 부재 및 부상 눈의 방향 미확정.
- [Czech Academy institutes' statement](https://www.arup.cas.cz/en/statement-aru-arub/) : 현대 얼굴 복원 주장의 과학적 한계.
- [Prague City Tourism — Bethlehem Chapel](https://prague.eu/en/objevujte/bethlehem-chapel-betlemska-kaple/) : 설교 장소의 20세기 재건 사실.

## 중요한 버전 관리 차이
과거 대화의 지도 ZIP(`REFORMATION_ATLAS_VOL03_MAPS_V01_SVG_PNG.zip`)과 이번에 GitHub에서 재조회한 정식 SVG 원본에 **설명 문구 차이**가 있다. 따라서 이번 후보 SVG의 해시를 **현재 GitHub 원본에 직접 적용한 결과**로 잘못 기술하지 않는다. 두 후보 SVG는 **대화 ZIP에만 제공**하고, 후속 로컬 동기화 시 두 정본을 비교·조정한 뒤에만 새 브랜치 자산으로 등록한다.

## 기계적 QA
- 후보 ZIP 내부 CRC PASS, WebP 4종·SVG 2종 PNG 렌더 완료, 해시 기록.
- 고위험 7점 중 **5점에 대해 수정 후보만** 존재(인물 3 + 지도 2). 사건 삽화 2점은 여전히 미완료. 후스 인물화는 중위험이었지만 일관성 확보를 위해 함께 제작.
- 시각자료 '완료'는 **제작 단계에만 해당**; 인간 고증·권리·역사학 검증·공개 전환은 아님.
- 게시 `approved=false`, `can_ship=false`, 기존 `assets/asset_manifest.json`과 `ILLUSTRATION_STAGE.json` 불변.

## 다음 권장 작업
1. 기존 GitHub 지도와 후보 지도 간 SVG 텍스트 차이를 비교한 뒤 **기존 GitHub를 기준으로 재생성**.
2. 사건 장면 두 개는 독립 이미지로 제작(인포그래픽 제외), 연대·회의장 허구의 확정 재현 금지.
3. 후보 ZIP 수동 검수 후 선택한 산출물만 별도 승인·해시 기록으로 승격.
