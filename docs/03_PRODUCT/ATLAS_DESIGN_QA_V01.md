# 종교개혁 아틀라스 · 5대 설계 문서 교차검증 V0.1

> 2026-10-25 · **DRAFT / 사용자 승인 대기**. GitHub 원본 JSON·파일 트리를 직접 읽어 비교한 검증 기록.

## 구조·관계 검증: 15/15 PASS
- [x] 18 PRD requirements all traced in TRD
- [x] 14 UX screens match PRD paths
- [x] 6 journeys use existing screens
- [x] 10 acceptance suites
- [x] 30 tasks all NOT_STARTED
- [x] Tasks cover all 18 requirements
- [x] Task dependency references valid
- [x] Task graph acyclic
- [x] Implementation gated by explicit design approval
- [x] 127 initial overview objects, 32 relationships
- [x] 22 places not falsely geocoded
- [x] Source review limits explicit
- [x] All web/publishing release gates closed
- [x] Five design docs stored
- [x] No web app code generated yet

이 검증은 요구/화면/작업 관계의 데이터 무결성 검사이며 **웹사이트 기능 테스트·학술 전문가 검증·실제 배포 승인**이 아니다.

## 전체 설계 산출물
1. [ATLAS_PROJECT_PLAN_V01.md](./ATLAS_PROJECT_PLAN_V01.md)
2. [ATLAS_PRD_V01.md](./ATLAS_PRD_V01.md)
3. [ATLAS_TRD_V01.md](./ATLAS_TRD_V01.md)
4. [ATLAS_UXUI_V01.md](./ATLAS_UXUI_V01.md)
5. [ATLAS_TASKLIST_V01.md](./ATLAS_TASKLIST_V01.md)

## 핵심 통계
- PRD 요구사항 **18건**, TRD 추적 18/18, UX/UI 화면 **14개**, 사용자 여정 **6개**, 수용시험 묶음 **10개**.
- 개발 TASKLIST **30개**(P0 26, P1 4); 구현 작업은 모두 `NOT_STARTED`.
- 검토용 개요 데이터 8권·인물 33·사건 34·문헌 20·장소 22·주제 10 = **127객체**, 관계 **32건**.
- 등록 출처 23건 중 직접 링크/범위 검토 11건, 같은 URL의 별칭 2건. 역사 좌표 검증 장소 0건.
- 웹 애플리케이션 코드 없음. 승인되지 않은 미디어는 계속 연구자료 상태.

## 필수 안전 게이트
- `TSK-030` 설계 승인 완료 전 `TSK-003` 앱 스캐폴딩을 시작하지 않는다. TASK 번호는 작성 순서이며 집행은 DAG 의존성을 따른다.
- 초기 데이터 `DRAFT`를 공개 JS·HTML·JSON·검색 색인·이미지에 복사하지 않는다. 로컬 비공개 시범을 우선.
- Astro+TypeScript / Cloudflare Pages는 **TRD의 권장 후보**, 아직 기술 확정·클라우드 배포 없음.
- `main` 병합/외부 공개와 8권 콘텐츠 학술적 승인 모두 별도 사람 판정이 필요.
