/**
 * V4.62 — conservative original-folio evidence gate.
 * Only validates recorded provenance. It cannot itself prove source authenticity
 * or replace a historian's inspection. No network, no file writes, no UI import.
 */
export const REQUIRED_PRIMARY_TARGETS = [
  "T462-K-ART15", "T462-Z-ART15", "T462-L1531-ARTX", "T462-L1540-ARTX"
];
const SHA256 = /^[a-f0-9]{64}$/;
const filled = value => typeof value === "string" && value.trim().length > 0;

export function checkOriginalFolio(target) {
  if (!target || typeof target !== "object") throw Error("invalid target");
  const missing = [];
  if (target.directOriginalLeafViewed !== true) missing.push("DIRECT_ORIGINAL_PAGE_NOT_INSPECTED");
  if (!SHA256.test(target.originalImageSha256 ?? "")) missing.push("ORIGINAL_IMAGE_SHA256_MISSING");
  if (!filled(target.leafOrCanvas)) missing.push("EXACT_PAGE_OR_CANVAS_MISSING");
  const transcription = target.diplomaticGermanText ?? target.diplomaticLatinText;
  if (!filled(transcription)) missing.push("DIPLOMATIC_TRANSCRIPTION_MISSING");
  if (target.transcriptionReview !== "HUMAN_QC_PASS") missing.push("TRANSCRIPTION_HUMAN_QC_MISSING");
  if (target.id === "T462-L1540-ARTX" && target.selectedSourceKind === "GOOGLE_ALTERNATE"
      && target.copyIdentityGoogleVsPitts !== "VERIFIED_SAME_EDITION")
    missing.push("PRINT_EDITION_IDENTITY_UNVERIFIED");
  return {id: target.id, directlyCitable: missing.length === 0, blockers: missing};
}

export function evaluateFourFolios(registry) {
  if (!registry || !Array.isArray(registry.targets)) throw Error("invalid registry");
  const ids = registry.targets.map(t=>t.id);
  if (new Set(ids).size !== ids.length || REQUIRED_PRIMARY_TARGETS.length !== ids.length
      || REQUIRED_PRIMARY_TARGETS.some(id=>!ids.includes(id)))
    throw Error("four distinct required folio targets must be present");
  const checks = registry.targets.map(checkOriginalFolio);
  const find = id => checks.find(c=>c.id === id);
  const article15PairedReady = find("T462-K-ART15").directlyCitable
    && find("T462-Z-ART15").directlyCitable;
  const articleXPairedReady = find("T462-L1531-ARTX").directlyCitable
    && find("T462-L1540-ARTX").directlyCitable;
  return {
    directFolioCount: checks.filter(c=>c.directlyCitable).length,
    targetsExpected: 4,
    article15PairedReady,
    articleXPairedReady,
    checks,
    originalPageTextComparisonReady: article15PairedReady && articleXPairedReady,
    historicalApprovalCount: registry.historianApprovals ?? 0,
    canShip: false, canMergeMain: false, canImportAIStudio: false
  };
}
