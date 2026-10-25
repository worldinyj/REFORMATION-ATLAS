## 변경 목적
<!-- 어떤 앱/데이터/설계를 왜 변경했나요? -->

## 변경 영역
- [ ] AI Studio 웹앱 코드 (독립 저장소 또는 승인된 기능 브랜치)
- [ ] 8권 개요 데이터/출처
- [ ] 제3권 심층 연구·시각자료
- [ ] 설계/운영 문서
- [ ] 검증 스크립트/CI

## 검증
- [ ] 변경 대상과 브랜치를 확인했고 `main` 직접 Push가 아니다.
- [ ] `python3 scripts/validate_ai_studio_repo_preflight.py` 확인 (연구 저장소 PR인 경우).
- [ ] `python3 scripts/validate_ai_studio_design_v02.py` 확인 (설계 변경 시).
- [ ] `python3 scripts/validate_atlas_overview_v01.py` 확인 (개요 데이터 변경 시).
- [ ] 신규 웹앱 코드가 있으면 `npm run build` / `typecheck` 결과 기록.
- [ ] `data/`, `docs/01_CONTENT/`, `assets/`에 의도하지 않은 변경 없음.
- [ ] 환경변수·API 키·OAuth 토큰·미승인 후보 이미지/유료 문헌 전문 미포함.
- [ ] DRAFT 개요가 공개 페이지의 HTML/JS/JSON/검색색인에 들어가지 않는다.
- [ ] 모바일/키보드 접근성과 직접 라우트가 확인됐다(앱 변경 시).
- [ ] `Share`, `Publish`, Cloud Run, `main` 병합을 승인 없이 하지 않았다.

## 위험/남은 작업
<!-- CI 통과는 역사적 승인·공개 허가가 아닙니다. -->
