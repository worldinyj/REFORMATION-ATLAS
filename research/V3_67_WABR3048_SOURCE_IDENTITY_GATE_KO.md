# 종교개혁 ATLAS V3.67 — WA Br 7 제3048호 서지 정체성 및 원문 접근 게이트

- 기준일: 2026-11-11
- 부모: `research/atlas-v366-capito-618-619-print-collation`
- 현재: `research/atlas-v367-wabr3048-source-identity-gate`
- 상태: RESEARCH_ONLY · DRAFT · NOT_APPROVED · CAN_SHIP=false
- 범위 제한: 연구 파일 추가만. main, 기존 역사 원고 513편, AI Studio 웹앱과 기존 사료 파일은 변경하지 않는다.

## 1. 대상 문헌 식별

**역사 문서:** 1536년 7월 20일 Wolfgang Capito → Martin Luther, Strasbourg.

**현대 편집 요약:** *The Correspondence of Wolfgang Capito*, vol.3 (2015), Ep.619 (앞선 V3.66에서는 인쇄 p.455 확인).

**원전 비평판 출전:** *D. Martin Luthers Werke. Kritische Gesamtausgabe*, Abt. 4, Briefwechsel, Bd.7 (Weimar, 1937), pp.466–468, Nr.3048.

- SLUB Dresden 서지목록: https://katalog.slub-dresden.de/id/0-1072308576
- 독일어 Wikisource의 WA Br 7 인터넷 아카이브 간접 링크 목록: https://de.wikisource.org/wiki/Martin_Luther
- 카피토 2015년 현대판 PDF: https://tile.loc.gov/storage-services/master/gdc/gdcebookspublic/20/20/71/95/37/2020719537/2020719537.pdf
- 카피토 서신집 개방 PDF 검색: https://uplopen.com/books/579/files/ee9e764a-bac4-4b38-a467-6cf85785e09f.pdf

## 2. 이번 조사로 달성한 것과 미완료 사항

- [x] WA Br 7의 1937년 서지·1534–1536년 수록 범위를 기관 목록으로 확인.
- [x] WA Br 7 인터넷 아카이브 복제본의 **목록 경로**를 확인.
- [x] Capito III Ep.619 ↔ WA Br 7 Nr.3048 pp.466–468 연결을 이전 V3.66의 인쇄판 검증 기록과 결합.
- [ ] WA Br 7 466–468쪽의 인쇄 원판 PDF 지면 직접 시각 검수.
- [ ] 원어 편지 전체 판독, 행별 번역, 각주 및 사본 목록 검토.
- [ ] 7월 19일 HBBW 866 라틴어 원문 직접 대조.

현재 등급은 `BIBLIOGRAPHIC_LOCATOR_VERIFIED`이며 `ORIGINAL_TEXT_VERIFIED`가 아니다. 인쇄 지면 미확보 상태에서 문장이나 문구를 창작해 원전 인용으로 제시하지 않는다.

## 3. 번호 충돌 주의 — 서로 다른 프로젝트의 제3048호

작센학술원 종교개혁 정치서신 온라인판의 `Nr.3048`은 [1525-11-12 이후] 요한 선제후 관련 **다른** 서신이다:
https://bakfj.saw-leipzig.de/doc/2361

이는 `WA.Br 3, S.619f., Nr.948`를 자체 서지출전으로 가진다. 따라서 `WA Br 7, Nr.3048`과 동일한 문서가 **아니다**.

ATLAS 문헌 ID는 단순 숫자가 아니라 다음과 같이 생성해야 한다.

`WA_BR:7:3048` = Capito→Luther, 1536-07-20, pp.466–468

`BAKFJ:3048` = 정치서신 온라인판 번호 3048, [1525-11-12 이후], 자체 편집출전 WA.Br 3 Nr.948

권고 JSON 스키마:
```json
{
  "stable_document_id": "WA_BR:7:3048",
  "edition_series": "WA.Br",
  "volume": "7",
  "editorial_number": "3048",
  "pages": "466-468",
  "historical_date": "1536-07-20",
  "sender": "Wolfgang Capito",
  "recipient": "Martin Luther",
  "evidence_access": "bibliographic_locator_only",
  "original_print_image_seen": false,
  "full_original_text_seen": false,
  "derived_summary": "CAPITO_CORRESPONDENCE:3:619",
  "can_publish": false
}
```

## 4. 해석 및 시간축 제약

2015년 편집 요약을 통해 바젤의 대표단 방문과 수용 설득을 카피토가 루터에게 보고했다는 *편집자 기술*을 확인했다(V3.66 계승). 1536-07-19 HBBW 866의 미코니우스 서신은 별도의 편집본 및 목록으로만 확인되었다.

아직 다음과 같이 주장할 수 없다.
- 카피토의 원어 편지에서 구체적으로 어떤 표현으로 바젤의 입장을 묘사했는지
- 7월 19일과 20일 당사자들의 신학적 태도가 정확히 어떻게 달랐는지
- 7월 17일이 대표단 파견일, 협의 종결일, 문서 작성일 중 무엇인지

**해석 원칙:** '현대 편집자 요약', '1937 비평판 원문', '1536 원필사본', '서신 메타데이터'를 별도 자산으로 구분한다.

## 5. V3.68 우선작업

1. WA Br 7 제3048호 pp.466–468을 실제 페이지 이미지로 확보해 내용·각주·원어를 교감.
2. HBBW VI Nr.866의 원어 본문 확보 및 7월 19일 `Argentinae` 관련 표현 대조.
3. 두 서신의 발신·수신·작성 일시·대표단 위치를 사건표로 연결하되 확인된 것만 직접 증거로 승격.
4. 1536-08-02 바젤 목회자 및 08-05 시의회 수용 판단의 당대 원천 자료 추적.
5. 공개 게이트 `CAN_SHIP=false` 지속.

## 6. 출처 및 QA

- SLUB: https://katalog.slub-dresden.de/id/0-1072308576
- 독일어 Wikisource WA Br 목록: https://de.wikisource.org/wiki/Martin_Luther
- Capito 제3권: https://tile.loc.gov/storage-services/master/gdc/gdcebookspublic/20/20/71/95/37/2020719537/2020719537.pdf
- 작센학술원 번호 충돌 반례: https://bakfj.saw-leipzig.de/doc/2361

연구 산출물 외 변경 없음. 전문가 심사 전 공개 금지.
