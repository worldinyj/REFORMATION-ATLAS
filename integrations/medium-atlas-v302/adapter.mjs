/** V3.02: consumer for the integrated 455-reader editorial delivery.
 * No fetch, DOM rendering, state writes or publication operation.
 */
export const CONTRACT_VERSION = '3.02';
const fail = message => { throw new Error(`Atlas import: ${message}`); };
const copy = value => structuredClone(value);
const array = (value, label) => { if (!Array.isArray(value)) fail(`${label} must be an array`); return value; };
const string = (value, label) => { if (typeof value !== 'string' || !value.trim()) fail(`${label} must be non-empty text`); return value; };
const map = (items, label) => {
  const out = new Map();
  for (const item of array(items, label)) {
    if (!item || typeof item !== 'object') fail(`${label} entry must be an object`);
    string(item.id, `${label}.id`);
    if (out.has(item.id)) fail(`duplicate ${label} ID: ${item.id}`);
    out.set(item.id, item);
  }
  return out;
};
const refs = (items, index, label) => {
  for (const id of array(items, label)) if (typeof id !== 'string' || !index.has(id)) fail(`unresolved ${label}: ${String(id)}`);
};
const normalize = value => value.normalize('NFKC').toLocaleLowerCase('ko-KR').replace(/\s+/gu, ' ').trim();
const compact = value => normalize(value).replace(/\s/gu, '');
const accessLabels = {
  PAGE_RETURNED: '자료 페이지 확인',
  PARTIAL_PAGE_THEN_TIMEOUT: '일부 접근·후속 확인 제한',
  ACCESS_FAILED: '이번 확인에서 접근 실패',
  NOT_CHECKED: '이번 확인 대상 아님',
};
const claimLabels = {
  SUPPORTED_IN_INSPECTED_MODERN_SOURCE_WITH_STATED_SCOPE: '지정한 현대 자료 범위에서 뒷받침',
  PARTIAL_SUPPORT_FURTHER_PASSAGE_NEEDED: '부분 뒷받침·추가 확인 필요',
};

export function createMediumAtlas(input) {
  if (!input || typeof input !== 'object') fail('missing bundle');
  // Snapshot the JSON data; neither later input edits nor returned objects alter the index.
  const b = copy(input);
  if (b.version !== '3.02' || b.status !== 'DRAFT' || b.depth !== 'MEDIUM') fail('unsupported bundle version or editorial state');
  for (const key of ['published', 'main_changed', 'webapp_integrated', 'historian_approved']) {
    if (b.publication_gate?.[key] !== false) fail(`missing editorial hold: ${key}`);
  }
  const readers = map(b.readers, 'reader'), sources = map(b.sources, 'source');
  const guides = map(b.reader_source_cards, 'guide'), basis = map(b.research_basis, 'research basis');
  const groups = map(b.reader_groups, 'group');
  const paths = map(b.reading_paths, 'path'), legacyPaths = map(b.legacy_reading_paths, 'legacy path');
  const comparisons = map(b.comparisons, 'comparison'), faq = map(b.faq, 'faq');
  const claims = map(b.source_verification?.selected_claims, 'claim');
  const checks = map(b.source_verification?.access_checks, 'access check');
  const cautions = map(b.source_verification?.source_cautions, 'caution');
  if (readers.size !== 455 || sources.size !== 650 || guides.size !== 11 || claims.size !== 22 || paths.size !== 21) fail('incomplete V3.02 snapshot');
  for (const s of sources.values()) {
    string(s.title, 'source title');
    let url; try { url = new URL(s.url); } catch { fail(`invalid source URL: ${s.id}`); }
    if (url.protocol !== 'https:' || url.username || url.password) fail(`unsafe source URL: ${s.id}`);
    const current = s.verification_v297;
    if (current && !Object.hasOwn(accessLabels, current.access_result)) fail(`unknown access status: ${s.id}`);
  }
  for (const c of readers.values()) {
    for (const key of ['title', 'lead', 'reading_question']) string(c[key], `${c.id}.${key}`);
    if (array(c.sections, 'sections').length !== 3) fail(`expected three sections: ${c.id}`);
    for (const s of c.sections) { string(s.heading, 'section heading'); string(s.body, 'section body'); }
    refs(c.sources, sources, 'reader sources');
    if (!c.sources.length) fail(`missing reader source references: ${c.id}`);
    refs(c.related_readers, readers, 'related readers');
    if (c.related_readers.includes(c.id)) fail(`self-related reader: ${c.id}`);
    refs(c.research_basis_ids, basis, 'reader research basis');
    if (c.source_card_id && !guides.has(c.source_card_id)) fail(`unresolved guide: ${c.id}`);
    if (c.selected_claim_ids) refs(c.selected_claim_ids, claims, 'reader selected claims');
  }
  for (const c of claims.values()) {
    if (!readers.has(c.reader_id) || !Number.isInteger(c.section_index)) fail(`invalid claim reader/index: ${c.id}`);
    const section = readers.get(c.reader_id).sections[c.section_index];
    string(c.exact_text_span, 'claim text span');
    if (!section || !section.body.includes(c.exact_text_span)) fail(`claim text drift: ${c.id}`);
    refs(c.source_ids, sources, 'claim sources');
    if (!c.source_ids.length) fail(`missing claim sources: ${c.id}`);
    if (!Object.hasOwn(claimLabels, c.status) || c.expert_approved !== false || c.original_witness_collated !== false) fail(`invalid claim scope: ${c.id}`);
    for (const sid of c.source_ids) if (sources.get(sid).verification_v297?.access_result !== 'PAGE_RETURNED') fail(`claim source unavailable: ${sid}`);
  }
  for (const a of checks.values()) {
    if (!sources.has(a.source_id) || sources.get(a.source_id).url !== a.url || !Object.hasOwn(accessLabels, a.access_result)) fail(`invalid access check: ${a.id}`);
  }
  for (const w of cautions.values()) { refs(w.source_ids, sources, 'caution sources'); refs(w.reader_ids, readers, 'caution readers'); }
  for (const g of guides.values()) {
    if (!readers.has(g.reader_id) || readers.get(g.reader_id).source_card_id !== g.id) fail(`guide reader mismatch: ${g.id}`);
    refs(g.source_ids, sources, 'guide sources'); refs(g.research_basis_ids, basis, 'guide research basis');
    refs(g.selected_claim_ids, claims, 'guide claims'); refs(g.access_check_ids, checks, 'guide access'); refs(g.warning_ids, cautions, 'guide cautions');
    refs(g.preferred_source_ids, sources, 'preferred sources');
    for (const id of g.selected_claim_ids) if (claims.get(id).reader_id !== g.reader_id) fail(`claim guide mismatch: ${g.id}`);
    for (const id of g.warning_ids) if (!cautions.get(id).reader_ids.includes(g.reader_id)) fail(`caution guide mismatch: ${g.id}`);
    for (const id of g.preferred_source_ids) if (!g.source_ids.includes(id)) fail(`preferred source outside guide: ${g.id}`);
  }
  for (const collection of [groups, paths, legacyPaths]) for (const p of collection.values()) refs(p.reader_ids, readers, 'navigation');
  const grouped = [...groups.values()].flatMap(g => g.reader_ids);
  if (grouped.length !== readers.size || new Set(grouped).size !== readers.size) fail('groups must partition all readers');
  for (const p of paths.values()) if (!['REGION', 'CHRONOLOGY', 'ISSUE'].includes(p.axis)) fail(`unknown path axis: ${p.id}`);
  for (const c of comparisons.values()) refs(array(c.rows, 'comparison rows').map(row => row.reader_id), readers, 'comparison readers');
  for (const q of faq.values()) refs(q.related_readers, readers, 'faq readers');
  if (b.metrics?.readers !== readers.size || b.metrics?.sections !== 1365 || b.metrics?.source_records !== sources.size) fail('bundle metrics mismatch');

  const summary = c => ({id: c.id, title: c.title, lead: c.lead, type: c.reader_type});
  const get = (index, id) => index.has(id) ? copy(index.get(id)) : null;
  const getSource = id => {
    if (!sources.has(id)) return null;
    const s = sources.get(id), current = s.verification_v297;
    const status = current?.access_result ?? 'NOT_CHECKED';
    return {id: s.id, title: s.title, url: s.url,
      sourceKind: s.source_class ?? s.scope ?? s.access ?? 'UNSPECIFIED',
      access: {status, label: accessLabels[status], checkedOn: current?.checked_on ?? null,
        note: current?.note ?? '접근 여부와 내용의 정확성을 이번에 확인하지 않았습니다.'},
      historicalAccessRecord: copy({access: s.access ?? null, accessStatus: s.access_status ?? null, scope: s.scope ?? null}),
      priorInspection: s.inspection_note ? copy({checkedOn: s.checked_on, scope: s.scope, note: s.inspection_note, inheritedFrom: s.provenance?.dataset, recheckedThisVersion: false}) : null,
      expertApproved: false};
  };
  const getClaim = id => {
    const c = get(claims, id);
    return c ? {...c, label: claimLabels[c.status], sources: c.source_ids.map(getSource)} : null;
  };
  const getSourceGuide = readerId => {
    const c = readers.get(readerId); if (!c?.source_card_id) return null;
    const g = guides.get(c.source_card_id);
    return {id: g.id, title: g.title, readingGuide: g.reading_guide, verificationNote: g.verification_note,
      sources: g.source_ids.map(getSource), preferredSourceIds: [...g.preferred_source_ids],
      claims: g.selected_claim_ids.map(getClaim), cautions: g.warning_ids.map(id => get(cautions, id))};
  };
  const getReader = id => {
    if (!readers.has(id)) return null;
    const c = readers.get(id);
    return {...summary(c), sections: copy(c.sections), readingQuestion: c.reading_question,
      relatedReaders: c.related_readers.map(id => summary(readers.get(id))), sources: c.sources.map(getSource),
      sourceGuide: getSourceGuide(id), editorialStatus: '편집 초안', expertApproved: false};
  };
  const searchIndex = [...readers.values()].map(c => ({c, title: compact(c.title), lead: compact(c.lead),
    all: compact([c.title, c.lead, ...c.sections.flatMap(s => [s.heading, s.body])].join(' '))}));
  const search = (query, {limit = 30, offset = 0, type = null} = {}) => {
    if (typeof query !== 'string') throw new TypeError('query must be a string');
    if (!Number.isInteger(limit) || limit < 1 || limit > 100 || !Number.isInteger(offset) || offset < 0) throw new RangeError('invalid search pagination');
    const terms = normalize(query).split(' ').filter(Boolean).map(compact);
    if (!terms.length) return {total: 0, items: []};
    const matches = searchIndex.filter(x => (!type || x.c.reader_type === type) && terms.every(t => x.all.includes(t)))
      .map(x => ({...summary(x.c), score: terms.reduce((score, t) => score + (x.title.includes(t) ? 8 : x.lead.includes(t) ? 3 : 1), 0)}))
      .sort((a, z) => z.score - a.score || a.id.localeCompare(z.id));
    return {total: matches.length, items: matches.slice(offset, offset + limit)};
  };
  return Object.freeze({contractVersion: CONTRACT_VERSION,
    mode: 'EDITORIAL_PREVIEW_ONLY', canPublish: false,
    counts: Object.freeze({readers: readers.size, sections: 1365, sources: sources.size, guides: guides.size, claims: claims.size, paths: paths.size}),
    listReaders: () => [...readers.values()].map(summary), getReader, getSource, getSourceGuide, getClaim, search,
    listGroups: () => copy([...groups.values()]),
    listReadingPaths: ({axis = null, includeLegacy = false} = {}) => copy([
      ...[...paths.values()].filter(p => !axis || p.axis === axis), ...(includeLegacy && !axis ? [...legacyPaths.values()] : [])]),
    getReadingPath: id => get(paths, id) ?? get(legacyPaths, id),
    listComparisons: () => copy([...comparisons.values()]),
    listFAQ: () => copy([...faq.values()]),
    getResearchBasis: id => get(basis, id),
  });
}
