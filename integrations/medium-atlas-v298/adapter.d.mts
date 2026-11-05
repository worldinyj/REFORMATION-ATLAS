export const CONTRACT_VERSION: '2.98';
export type PathAxis = 'REGION' | 'CHRONOLOGY' | 'ISSUE';
export interface ReaderSummary { id: string; title: string; lead: string; type: string }
export interface SourceView {
  id: string; title: string; url: string; sourceKind: string;
  access: {status: 'PAGE_RETURNED' | 'PARTIAL_PAGE_THEN_TIMEOUT' | 'ACCESS_FAILED' | 'NOT_CHECKED'; label: string; checkedOn: string | null; note: string};
  historicalAccessRecord: {access: unknown; accessStatus: unknown; scope: unknown}; expertApproved: false;
}
export interface ClaimView {
  id: string; reader_id: string; section_index: number; exact_text_span: string;
  source_ids: string[]; source_locator: string; evidence_summary: string;
  status: 'SUPPORTED_IN_INSPECTED_MODERN_SOURCE_WITH_STATED_SCOPE' | 'PARTIAL_SUPPORT_FURTHER_PASSAGE_NEEDED';
  expert_approved: false; original_witness_collated: false; label: string; sources: SourceView[];
}
export interface Caution { id: string; source_ids: string[]; reader_ids: string[]; note: string }
export interface SourceGuide {
  id: string; title: string; readingGuide: string; verificationNote: string;
  sources: SourceView[]; preferredSourceIds: string[]; claims: ClaimView[]; cautions: Caution[];
}
export interface ReaderDetail extends ReaderSummary {
  sections: {heading: string; body: string}[]; readingQuestion: string;
  relatedReaders: ReaderSummary[]; sources: SourceView[]; sourceGuide: SourceGuide | null;
  editorialStatus: '편집 초안'; expertApproved: false;
}
export interface ReadingPath { id: string; title: string; reader_ids: string[]; reading_question: string; interpretive_limit: string; axis?: PathAxis; status?: string }
export interface ReaderGroup { id: string; title: string; reader_ids: string[] }
export interface Comparison { id: string; title: string; lead: string; rows: ({reader_id: string} & Record<string, unknown>)[]; interpretive_limit: string; reading_question: string }
export interface FAQ { id: string; question: string; answer: string; related_readers: string[]; basis: unknown }
export interface AtlasConsumer {
  readonly contractVersion: '2.98'; readonly mode: 'EDITORIAL_PREVIEW_ONLY'; readonly canPublish: false;
  readonly counts: Readonly<{readers: number; sections: number; sources: number; guides: number; claims: number; paths: number}>;
  listReaders(): ReaderSummary[]; getReader(id: string): ReaderDetail | null;
  getSource(id: string): SourceView | null; getSourceGuide(readerId: string): SourceGuide | null;
  getClaim(id: string): ClaimView | null;
  search(query: string, options?: {limit?: number; offset?: number; type?: string | null}): {total: number; items: (ReaderSummary & {score: number})[]};
  listGroups(): ReaderGroup[];
  listReadingPaths(options?: {axis?: PathAxis | null; includeLegacy?: boolean}): ReadingPath[];
  getReadingPath(id: string): ReadingPath | null;
  listComparisons(): Comparison[]; listFAQ(): FAQ[];
  getResearchBasis(id: string): Record<string, unknown> | null;
}
/** Throws on unsupported, incomplete or internally inconsistent input. No network access. */
export function createMediumAtlas(input: unknown): AtlasConsumer;
