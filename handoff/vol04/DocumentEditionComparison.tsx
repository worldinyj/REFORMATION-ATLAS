import React, { useRef, useState } from 'react';
import { getApprovedDocumentEdition } from './approvedEditions';
import { validatedPublicPayload, type ComparisonKind } from './editionPolicy';

const tabs: ReadonlyArray<{ id: ComparisonKind; label: string }> = [
  { id: 'structure', label: '구성 변화' },
  { id: 'textual_wording', label: '본문 차이' },
  { id: 'iconography', label: '삽화 차이' },
];
const EMPTY = '승인된 판본 비교 자료가 없습니다.';

/** Add to existing DocumentDetailPage only. No research data is loaded here. */
export default function DocumentEditionComparison({ documentId }: { documentId: string }) {
  const [active, setActive] = useState<ComparisonKind>('structure');
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const payload = validatedPublicPayload(getApprovedDocumentEdition(documentId), documentId);

  function selectByKeyboard(event: React.KeyboardEvent<HTMLButtonElement>, index: number) {
    let next: number;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else return;
    event.preventDefault();
    setActive(tabs[next].id);
    refs.current[next]?.focus();
  }

  if (!payload) return (
    <section aria-labelledby="edition-comparison-heading" className="edition-comparison">
      <h2 id="edition-comparison-heading">판본 비교</h2>
      <p role="status" className="edition-comparison__empty">{EMPTY}</p>
    </section>
  );

  const selected = payload.comparisons.filter(item => item.kind === active);
  return (
    <section aria-labelledby="edition-comparison-heading" className="edition-comparison">
      <h2 id="edition-comparison-heading">판본 비교</h2>
      <ol aria-label="판본 연대표" className="edition-comparison__timeline">
        {payload.editions.map(edition => (
          <li key={edition.id}>
            <strong>{edition.yearLabel}</strong> — {edition.label}
            <span> · {edition.language} · {edition.materialKind}</span>
          </li>
        ))}
      </ol>
      <div role="tablist" aria-label="판본 비교 유형" className="edition-comparison__tabs">
        {tabs.map((tab, index) => (
          <button type="button" role="tab" key={tab.id} id={`edition-tab-${tab.id}`}
            aria-controls={`edition-panel-${tab.id}`} aria-selected={active === tab.id}
            tabIndex={active === tab.id ? 0 : -1}
            ref={el => { refs.current[index] = el; }}
            onClick={() => setActive(tab.id)}
            onKeyDown={event => selectByKeyboard(event, index)}>{tab.label}</button>
        ))}
      </div>
      {tabs.map(tab => (
        <div role="tabpanel" key={tab.id} id={`edition-panel-${tab.id}`}
          aria-labelledby={`edition-tab-${tab.id}`}
          hidden={active !== tab.id} tabIndex={active === tab.id ? 0 : -1}>
          {active === tab.id && (selected.length === 0 ? <p>{EMPTY}</p> :
            selected.map(item => <article key={item.id}>
              <p>{item.observationKo}</p>
              {item.interpretationKo && <p><strong>역사적 해석:</strong> {item.interpretationKo}</p>}
              <p><strong>검토된 출처:</strong> {item.sourceLabels.join(' · ')}</p>
            </article>))}
        </div>
      ))}
    </section>
  );
}
