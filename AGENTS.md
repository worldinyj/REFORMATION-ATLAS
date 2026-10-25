# REFORMATION ATLAS — contributor / AI coding agent boundaries

This is the **canonical research and historical-content repository**, not yet a runnable React app. Google AI Studio Build is intended to generate the web app separately, with a carefully reviewed import/sync step.

## Immediate priorities
1. Preserve the existing research dataset (`data/`), documentary apparatus (`docs/01_CONTENT/`), historical media staging (`assets/`), and validators (`scripts/`).
2. Use the current [AI Studio V0.2 design package](docs/03_PRODUCT/AI_STUDIO_BUILD_V02/README.md), with `06_MASTER_BUILD_PROMPT.md` as the **canonical Korean initial build prompt**.
3. In the initial AI Studio app, use a spacious, restrained "Quiet Editorial Atlas" look; React+TypeScript, no invented historical biographies, no maps or historical images without approval.
4. Implement **OVERVIEW first**, then add separately approved `DEEP_RESEARCH` blocks under stable canonical IDs/URLs.
5. Distinguish historical certainty, source access/edition, editorial review, image rights, and website publication approvals.

## GitHub scope
- **Do not push to main.** This instruction alone does not technically prevent pushes; users must enable repository Rulesets in GitHub Settings.
- Do not rewrite or delete `data/`, `docs/01_CONTENT/`, `assets/`, `scripts/`, `.github/` while importing app code.
- For the preferred setup, generate a new AI Studio app and connect it to a **separate web-app GitHub repository**, then deliberately import reviewed content through a versioned projection.
- If keeping a monorepo, do app work exclusively on a user-approved feature branch, isolating code beneath `apps/web/`, and review changes before synchronization. AI Studio's support for arbitrary workspace/branch layouts must be tested first rather than assumed.
- Respect `.env` and local secrets; no Google API key needed for an archive-only MVP.
- Do not use `Share`, `Publish`, Cloud Run, or public GitHub export without explicit publication approval.

## Current state
- 8 volumes; 33 people; 34 events; 20 documents; 22 unverified place references; 10 topics; 32 typed relations.
- All historical overview content remains DRAFT, and no AI historical portraits are approved for website publication.
- No React app or npm manifest has been created as of this preflight; do not claim an existing app imported into AI Studio.
- Read [setup and preflight guidance](docs/03_PRODUCT/AI_STUDIO_BUILD_V02/09_GITHUB_CONNECTION_SETUP.md).

## Verification
```bash
python3 scripts/validate_ai_studio_repo_preflight.py
python3 scripts/validate_ai_studio_design_v02.py
python3 scripts/validate_atlas_overview_v01.py
```
After adding an app, run `python3 scripts/check_ai_studio_sync_paths.py --base <the-reviewed-base-ref>` to check changed files before any push or merge.

**Passing structural checks is not historical verification or authorization to publish.**
