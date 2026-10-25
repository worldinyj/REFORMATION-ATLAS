# 기술 설계 결정 목록 (ADR) V0.1
> PRD V0.1 기반 / 모두 제안 / 실제 구현 없음

| ID | 선택 제안 | 보류 가능한 대안 | 채택 전 확인 |
|---|---|---|---|
| ADR-001 | Astro + TypeScript, pre-render static-first | Django templates or Next.js runtime rendering | Small initial catalogue; pages and cross-links, low cost; no login/transaction in P0; future deep content remains Markdown/JSON |
| ADR-002 | Git-managed Markdown/JSON + build-time generated read model, no DB in P0 | Django/SQLite then Postgres; CMS | Current GitHub data and Python validators are ready; editorial traceability via Git; DB is warranted only for multi-author workflows/user data |
| ADR-003 | Static client-side index, deterministic Korean/Latin normalized title and aliases | Backend full-text API/hosted search | 127 introductory records, no need remote service; type-scoped queries; avoid leaking draft records in index |
| ADR-004 | Cloudflare Pages as optional static host only after release-gate decision | GitHub Pages / another static host | Candidate only. Preview deployments are public by default and must not contain draft data unless protected with Access |
| ADR-005 | Text-only places in P0; verified geodata and map provider P1 | Unverified geocoder pins | 22 places are unverified named locations and have zero confirmed coordinates. False historical precision is disallowed |
| ADR-006 | No unapproved historic portraits in P0 public build; optional verified licensed assets later | Immediate AI image upload | Old VOL03 historic study/candidate 8 visuals still require human scholarly and rights approval |

특히 Cloudflare Pages Preview는 기본적으로 공개 URL이다. Cloudflare Access로 보호하거나 로컬 프리뷰로 제한한 경우에만 DRAFT 기반 검토 화면을 외부에서 볼 수 있도록 한다. `noindex`는 보안 또는 비공개를 보장하지 않는다. [공식 문서](https://developers.cloudflare.com/pages/configuration/preview-deployments/)

실제 도입 여부는 기술 적합성·예산·유지보수 방식과 사용자의 최종 승인을 거쳐 정한다. 제품/역사 출판 승인과 별도다.
