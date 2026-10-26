/** Browser-side shape check only. Publication authority belongs to a separate reviewed build manifest. */
export type ComparisonKind = 'structure' | 'textual_wording' | 'iconography';
export interface ApprovedEdition {
  id: string; label: string; yearLabel: string; language: string; materialKind: string;
  approved: true; publicationApproved: true;
}
export interface ApprovedComparison {
  id: string; kind: ComparisonKind; observationKo: string; interpretationKo?: string;
  sourceLabels: string[]; approved: true; publicationApproved: true;
  textCollated: boolean; mediaRightsApproved: boolean;
}
export interface ApprovedDocumentEditionPayload {
  workId: string; releaseManifestRef: string; editorialApprovalRef: string;
  releaseApproved: true; workApproved: true; sourceEvidenceApproved: true; rightsApproved: true;
  editions: ApprovedEdition[]; comparisons: ApprovedComparison[];
}
const isNonempty = (value: unknown): value is string =>
  typeof value === 'string' && value.trim().length > 0;
const isObject = (value: unknown): value is Record<string, unknown> =>
  value !== null && typeof value === 'object' && !Array.isArray(value);
const WORK_ID = /^OV-D-\d{3}$/;
const EDITION_ID = /^(?:EDN|TRN|WIT)-V04-\d{4}$/;
const COMPARISON_ID = /^COM-V04-\d{4}$/;
const TYPES: ComparisonKind[] = ['structure', 'textual_wording', 'iconography'];

/** Validates a *preapproved* projection. This does not authenticate signatures or grant release. */
export function validatedPublicPayload(value: unknown, documentId: string): ApprovedDocumentEditionPayload | null {
  if (!isNonempty(documentId) || !WORK_ID.test(documentId) || !isObject(value)) return null;
  if (value.workId !== documentId || value.releaseApproved !== true || value.workApproved !== true ||
      value.sourceEvidenceApproved !== true || value.rightsApproved !== true ||
      !isNonempty(value.releaseManifestRef) || !isNonempty(value.editorialApprovalRef)) return null;
  if (!Array.isArray(value.editions) || !Array.isArray(value.comparisons) || value.editions.length === 0) return null;
  const editionIds = new Set<string>();
  for (const item of value.editions) {
    if (!isObject(item) || !isNonempty(item.id) || !EDITION_ID.test(item.id) ||
        editionIds.has(item.id) || !isNonempty(item.label) || !isNonempty(item.yearLabel) ||
        !isNonempty(item.language) || !isNonempty(item.materialKind) ||
        item.approved !== true || item.publicationApproved !== true) return null;
    editionIds.add(item.id);
  }
  const compareIds = new Set<string>();
  for (const item of value.comparisons) {
    if (!isObject(item) || !isNonempty(item.id) || !COMPARISON_ID.test(item.id) ||
        compareIds.has(item.id) || !TYPES.includes(item.kind as ComparisonKind) ||
        !isNonempty(item.observationKo) || !Array.isArray(item.sourceLabels) ||
        item.sourceLabels.length === 0 || !item.sourceLabels.every(isNonempty) ||
        item.approved !== true || item.publicationApproved !== true ||
        (item.kind === 'textual_wording' && item.textCollated !== true) ||
        (item.kind === 'iconography' && item.mediaRightsApproved !== true)) return null;
    compareIds.add(item.id);
  }
  return value as unknown as ApprovedDocumentEditionPayload;
}
