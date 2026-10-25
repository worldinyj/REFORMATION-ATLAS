# 아틀라스 8권 개요 콘텐츠 QA 절차
> 2026-10-25 / 콘텐츠 준비 단계 / 비공개

## 테스트
- `python3 scripts/validate_atlas_overview_v01.py`: GitHub 연결된 현행 JSON만 읽고 파일은 수정하지 않는다.
- 데이터 수량·ID/출처·관계 종단점·연대 정밀도·VOL-08 주제형 구조·문헌 전문 비수록·현대 도시 지명과 고증된 좌표의 구분을 검사한다.
- `data/overview/legacy_person_crosswalk_v01.json`으로 제3권 기존 인물 원형 3명과 대조한다.
- 8개 권별 개요 원고가 존재하는지 검사하며 웹사이트 코드 배포나 PRD/TRD 작성을 실행하지 않는다.
- `.github/workflows/atlas-overview-qa.yml`에 저장해 개요 브랜치에 푸시될 때 자동 실행한다.

## PASS가 의미하지 않는 사항
- 모든 23건 출처 전문을 검토한 것은 아니다. 11개 직접 링크·대상 확인, 나머지는 참고문헌 확인 대기.
- 학술 전문가의 사실관계·성경 번역·고대 교회사 감수 또는 저작권·AI 이미지 공개 승인이 아니다.
- PRD/TRD/UX/UI/TASKLIST 확정이나 사이트 빌드·배포를 수행했다는 뜻이 아니다.

## 게이트
- `CONTENT_INVENTORY_READY_FOR_PROJECT_PLAN_DRAFT`는 가능한 상태.
- `READY_FOR_PUBLIC_WEB`과 `FINAL_SCHOLARLY_APPROVED`는 **보류**.
- `main` 병합과 웹 공개는 별도로 승인받는다.
