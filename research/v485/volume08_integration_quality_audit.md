# ATLAS V4.85 — Content integration quality audit

Date: 2026-11-21
Status: PARTIAL_INTEGRATION_RESEARCH_ONLY
can_ship: false
Base: research/atlas-v484-vol08-claims-and-integration-gates

## Files independently checked in working session
- V4.83 draft: SHA256 a7f8e60220c798ae7ec83a259d3393918ae546ca81d6b6530bf9afa88ea56498; 15 sections (A1-A7, B1-B8).
- V4.84 editorial research draft and JSON connection contract: 9 claims, 3 source entries, 5 reading paths.
- V4.84 research draft already embeds V4.83 complete draft **once**: do not append the same prose again.
- V4.82 10-section draft: only referenced by earlier conversation; FULL CONTENT AND SHA NOT RECOVERED. Do not mark merged.

## Machine validation outcomes
PASS: V4.83 actual file SHA matches the contract's expected hash.
PASS: 15 unique section IDs.
PASS: 9 unique claim IDs, 3 unique source IDs, 5 unique reading path IDs.
PASS: all claim->source and reading-path->claim references resolve.
PASS: all five reading paths refer to extant A/B sections.
PASS: V4.84 embeds V4.83 exactly once.
BLOCKED: V4.82 full text diff and integration.
NOT DONE: semantic duplicate review against V4.82, per-volume deep links, historian review, reader evaluation, app integration testing.

## Editorial protections
- 1530 Augsburg Confession / 1555 Religious Peace / 1648 Peace of Westphalia must not be collapsed into one legal-historical event.
- Do not conflate the 1530 presentation of the Augsburg Confession with its 1531 printed versions or the 1540 Variata.
- Do not treat the limited protection in 1555 as universal individual religious liberty.
- Tamil 1715/1719 publication/witness relationship: HOLD pending bibliographic verification.
- Claims status totals: supported=5, supported_interpretive=1, reject=1, hold=1, review=1.
- Cross-volume reading links are PROPOSALS ONLY pending verification of actual source-volume IDs and anchors.

## Next action
1. Find exact V4.82 path + commit + file SHA.
2. Recover source volumes I-VII to map actual anchors and separate historical sequence from causation.
3. Produce semantic duplicate and contradiction triage for the three Volume VIII themes.
4. Keep staging isolated and can_ship=false.

Local user-facing files in the session:
- REFORMATION_ATLAS_V485_통합품질검토.md
- REFORMATION_ATLAS_V485_통합계약_검증결과.json

These files are NOT represented by this tracker as fully committed file bodies. Only this audit summary is committed.
