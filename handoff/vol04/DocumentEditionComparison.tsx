import React, { useState } from "react";

/** PUBLIC APPROVED DATA ONLY. Do not import data/deep or research projections. */
export type ApprovedEdition = Readonly<{
  id: string;
  label: string;
  yearLabel: string;
  language: string;
  materialKind: string;
  approved: true;
  publicationApproved: true;
}>;
export type ApprovedEditionComparison = Readonly<{
  id: string;
  kind: "structure" | "textual_wording" | "iconography";
  observationKo: string;
  interpretationKo?: string;
  sourceLabels: readonly string[];
  approved: true;
  publicationApproved: true;
  textCollated: boolean;
}>;
export type ApprovedDocumentEditionPayload = Readonly<{
  workId: string;
  releaseManifestId: string;
  releaseApproved: true;
  editions: readonly ApprovedEdition[];
  comparisons: readonly ApprovedEditionComparison[];
}>;
type Props = Readonly<{
  documentId: string;
  /** Supply only from a separately generated, signed-off public snapshot. */
  approvedPayload?: ApprovedDocumentEditionPayload | null;
}>;
const TABS = [
  { id: "structure", label: "구성 변화" },
  { id: "textual_wording", label: "본문 차이" },
  { id: "iconography", label: "삽화 차이" },
] as const;
const EMPTY = "승인된 판본 비교 자료가 없습니다.";

function isSafe(payload: ApprovedDocumentEditionPayload | null | undefined, documentId: string): payload is ApprovedDocumentEditionPayload {
  if (!payload || payload.workId !== documentId || payload.releaseApproved !== true ||
      !payload.releaseManifestId || !Array.isArray(payload.editions) || !Array.isArray(payload.comparisons)) return false;
  // REVIEW-ONLY identifiers must never be public route identifiers.
  if (/(?:-PROP-|VOL04-CMP-|CMP-SRC-PROP-)/.test(payload.workId)) return false;
  if (!payload.editions.every(e => e.approved === true && e.publicationApproved === true &&
      !!e.id && !!e.yearLabel && !!e.language)) return false;
  if (!payload.comparisons.every(c => c.approved === true && c.publicationApproved === true &&
      !!c.id && !!c.observationKo && Array.isArray(c.sourceLabels) &&
      (c.kind !== "textual_wording" || c.textCollated === true))) return false;
  return true;
}

/** Non-public template: deliberately renders empty state until an approved payload is provided. */
export default function DocumentEditionComparison({ documentId, approvedPayload }: Props) {
  const [active, setActive] = useState<(typeof TABS)[number]["id"]>("structure");
  const safe = isSafe(approvedPayload, documentId);
  if (!safe) return (
    <section aria-labelledby="editions-heading" className="edition-comparison">
      <h2 id="editions-heading">판본 비교</h2>
      <p role="status">{EMPTY}</p>
    </section>
  );
  const comparisons = approvedPayload.comparisons.filter(c => c.kind === active);
  return (
    <section aria-labelledby="editions-heading" className="edition-comparison">
      <h2 id="editions-heading">판본 비교</h2>
      <ol aria-label="승인된 판본 연표" className="edition-timeline">
        {approvedPayload.editions.map(e => (
          <li key={e.id}>
            <strong>{e.yearLabel}</strong> — {e.label}
            <span> · {e.language} · {e.materialKind}</span>
          </li>
        ))}
      </ol>
      <div role="tablist" aria-label="판본 비교 유형">
        {TABS.map(t => <button key={t.id} role="tab" type="button"
          aria-selected={active === t.id} id={"edition-tab-"+t.id}
          aria-controls={"edition-panel-"+t.id}
          onClick={() => setActive(t.id)}>{t.label}</button>)}
      </div>
      <div role="tabpanel" id={"edition-panel-"+active}
        aria-labelledby={"edition-tab-"+active} tabIndex={0}>
        {comparisons.length === 0 ? <p>{EMPTY}</p> :
          comparisons.map(c => <article key={c.id}>
            <p>{c.observationKo}</p>
            {c.interpretationKo && <p><strong>해석:</strong> {c.interpretationKo}</p>}
            <p><strong>검토된 출처:</strong> {c.sourceLabels.join(" · ")}</p>
          </article>)}
      </div>
    </section>
  );
}
