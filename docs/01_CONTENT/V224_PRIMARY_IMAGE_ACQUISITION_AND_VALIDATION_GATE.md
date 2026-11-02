# 종교개혁 ATLAS V2.24 — 1529년 원본 영상 수집 검증 게이트

> **연구 전용 · 공개 보류**. 부모 커밋 `17b549ad755fd9d8a865f1342487736bb2af2310`. V2.19 원고 10편/74절/128문단/543문장/35,102코드포인트, 핵심 주장 30건, 탐색 연결 30건 변경 없음.

## 1. 왜 이번 단계가 달라졌나

V2.20~V2.23은 필사본 Z·K와 1529년 동시대 인쇄본 W2119의 **존재, 보존처, 연구 대조 범위, 후대 편집 전사의 차이**를 분명히 했다. 그러나 직접 판독 가능한 원본 이미지가 실제로 수집되지는 않았다. 따라서 V2.24에서는 **공식 보존기관의 디지털 이미지/전체 PDF 접근 규칙을 기계적으로 검증하는 재현 가능한 절차**를 연구 자료로 추가한다.

e-rara 공식 [인터페이스 문서](https://www.e-rara.ch/wiki/apiinfo)는 표제 단위 PDF의 경로 패턴 `/download/pdf/{VLID}.pdf`를 공개한다. [취리히 중앙도서관 e-rara 서지](https://www.e-rara.ch/zuz/content/titleinfo/170052)는 ZB Zürich **5.174,5 = VD16 W2119**, **1529년 프로샤우어(Froschauer) 인쇄본**, [4]매, 영구식별자 **e-rara-597**, Public Domain Mark를 확인한다. 따라서 표제 ID **170052**를 이용하여 공식 문서에 따른 다음 두 주소를 **수집 대상으로 산출할 수 있다**.

- **공식 PDF URL (공식 경로 규칙으로 조합한 요청 대상):** https://www.e-rara.ch/download/pdf/170052.pdf
- **공식 IIIF v2 Manifest (서지에 표시된 주소):** https://www.e-rara.ch/i3f/v20/170052/manifest

두 URL의 응답을 이번 실행 환경에서 실제로 가져오지는 못했다. 자동 생성한 URL을 '수집 성공'이라고 부르지 않는다. 로컬 테스트에서도 네트워크 연결이 실패했다.

## 2. 실행 가능한 검증 프로그램

파일: `scripts/fetch_atlas_v224_primary_facsimile.py`

별도의 외부 Python 패키지 설치 없이 Python 표준 라이브러리를 이용한다. **기본 실행 모드는 오프라인 preview**이며, 실제 네트워크 접근에는 명시적 `--mode fetch`가 필요하다. 원본 이미지와 PDF는 Git 저장소 바깥 폴더에만 기록하고, 기존 파일을 덮어쓰지 않는다.

```bash
# 저장소의 연구 브랜치를 로컬에서 체크아웃한 뒤 실행
python3 scripts/fetch_atlas_v224_primary_facsimile.py --mode self-test
python3 scripts/fetch_atlas_v224_primary_facsimile.py --target w2119-pdf --mode preview

# 네트워크 가능한 환경에서 원본 PDF 취득을 명시적으로 요청
python3 scripts/fetch_atlas_v224_primary_facsimile.py --target w2119-pdf --mode fetch

# PDF 실패 시 IIIF 매니페스트 요청
python3 scripts/fetch_atlas_v224_primary_facsimile.py --target w2119-iiif --mode fetch
```

기본 파일 저장 위치: `~/Downloads/REFORMATION_ATLAS_V224_SOURCES/` (스크립트 내부 기본값).

성공 조건은 실제 응답을 받은 뒤 **PDF 헤더 `%PDF-` 및 끝 마커 확인**, 또는 **유효한 IIIF Presentation API v2 JSON과 canvas 목록 확인**, 파일 크기 상한, SHA-256 산출, 파일 보존이다. **이것은 파일 검증이지 판독 검증이 아니다.** HTML 차단 페이지를 PDF로 오인하지 않고, PDF/IIIF에 직접 접근할 수 없다면 실패를 출력하며 연구 데이터의 원본 판독 상태를 올리지 않는다.

## 3. 1529년 증인별 원문 검증 큐

| 대상 | 확보 경로 | 문헌학적 판독 목표 | 상태 |
|---|---|---|---|
| 취리히 W2119 | e-rara 공식 PDF/IIIF | 제7·13·15조 원래 인쇄 표기 및 판면 위치 | 응답 파일 검증 **미완료** |
| 헤센 K | [HAPuls 원본 갤러리](https://www.hapuls.de/node/1472) 및 DigiRef 소장 기록 | Best.3 Nr.245 fol.60r–64v에서 제7·13·15조 위치 | 원본 이미지 **미확보** |
| 취리히 Z | [문서관 E I 3.1 Nr.54](https://suche.staatsarchiv.djiktzh.ch/detail.aspx?ID=618165) | 제7·13·15조에 있다는 추가 부분의 원래 판독 | 원본 이미지 **미확보** |

HAPuls의 `PA Nr245, Bl.60–63` 및 학술·문서관의 `Best.3 Nr245, fol.60r–64v` 표기는 원본의 식별표와 면 구획을 확인할 때까지 별도 기록한다. 취리히 Z의 세 추가 문구를 W2119 인쇄본에서 **반드시** 발견할 것이라고 전제하지 않는다.

원문 대조표의 `z_original_reading`, `k_original_reading`, `w2119_original_print_reading`, 세 증인의 정확한 면·행 번호는 모두 **null**로 보존한다.

## 4. 편집사가 다른 날짜를 보존하는 이유

[MBW 825](https://melanchthon.hadw-bw.de/regest.html?reg_nr=825)는 마르부르크 조항의 날짜를 **`3.[4.] Oktober 1529`**라고 기록한다. 취리히 보존목록·W2119 인쇄본 표제는 **3일**, DigiRef 학술 메타데이터는 **4일**이다. MBW의 표기는 이 차이를 텍스트 비평상 설명할 수 있는 직접적인 학술 신호이므로, 연구 데이터에서는 단일 확정 날짜를 만들어 덮어쓰지 않았다. 원본 서명본 종결부와 연구자 설명을 확인할 때까지 잠정 상태로 유지한다.

## 5. 두 번째 원본 복제 경로와 서지 이견

원본 필사본과 별도로 **Heinrich Heppe의 19세기 서명본 파크시밀리**가 대체 검증 경로가 될 수 있다. [Google Books의 목록](https://play.google.com/store/books/details/Heinrich_Heppe_Die_f%C3%BCnfzehn_Marburger_Artikel_vom?id=L2b7YTiIyLwC)은 이를 1854년 출판물로 기록하며, [19세기 Meyers 전기 목록](https://de.wikisource.org/wiki/MKL1888%3AHeppe)은 1847년으로 기재한다. **판본·재간행·디지털 카탈로그의 날짜 중 무엇이 원인인지 미확인**이므로 1847과 1854를 합치지 않는다. 해당 파크시밀리의 실제 판면을 직접 읽을 때까지 `BIB-V224-HEPPE-DATES`를 미해결로 둔다.

## 6. 진행 판정과 다음 실제 조사

- **완료:** e-rara 표준 수집 패턴 문서화, W2119의 정확한 ID에 연결, 오프라인 자기검증 및 실제 네트워크 요청을 구분하는 수집 프로그램, 원본 판독·저작권·출판 보류 데이터.
- **미완료:** W2119 PDF 또는 IIIF의 실제 파일 응답 확보·페이지 시각 검수, K/Z 원본 사진 판독, 삽입 문구의 증인별 교감, 전문가 감수.
- **개발 경계:** `main`·웹앱 미변경, 다운로드 원본·영인은 Git에 추가하지 않음, 보고서와 데이터는 연구 브랜치에서만 관리.

**연구 데이터:** `data/deep/atlas_v224_primary_facsimile_retrieval_gate.json`  
**오프라인/연결 정합성 검사:** `scripts/validate_atlas_v224.py`  
**이미지 확보 및 해시 검증 도구:** `scripts/fetch_atlas_v224_primary_facsimile.py`

다음 V2.25의 진행 판정은 **실제 파일 취득 성공 여부**부터 시작해야 한다. 취득 실패만 반복된다면 소장기관 제공 원본·기존 파크시밀리의 영상 확보를 대체 경로로 검토하고, 연구 원고에서 확인하지 못한 인용을 추가하지 않는다.
