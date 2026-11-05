/** Explicit overview-to-reading navigation. No name matching, fetch or route writes. */
export function createOverviewReadingBridge(input, atlas) {
  const reject = message => { throw new Error(`Overview reading bridge: ${message}`); };
  if (!atlas || atlas.contractVersion !== '3.06' || atlas.canPublish !== false || atlas.counts?.readers !== 495) reject('unsupported consumer');
  const x = structuredClone(input);
  if (x?.version !== '3.06' || x.status !== 'DRAFT') reject('unsupported crosswalk');
  for (const key of ['published', 'main_changed', 'webapp_integrated']) if (x.publication_gate?.[key] !== false) reject('missing editorial hold');
  if (!Array.isArray(x.entries) || x.entries.length !== 97) reject('incomplete overview snapshot');
  const rows = new Map(), reverse = new Map();
  const counts = {DIRECT_TOPIC: 0, PARTIAL_COVERAGE: 0, BACKGROUND_ONLY: 0, NO_MATCH: 0};
  const labels = {DIRECT_TOPIC: '대응 주제 해설', PARTIAL_COVERAGE: '일부 범위 해설', BACKGROUND_ONLY: '배경 자료만', NO_MATCH: '직접 원고 없음'};
  for (const row of x.entries) {
    if (!/^(OV-[PED]-\d{3}|TOP-\d{2})$/.test(row.overview_id) || rows.has(row.overview_id)) reject('invalid or duplicate overview ID');
    if (!row.title || !row.scope || !Object.hasOwn(counts, row.mapping_status)) reject('missing reading scope');
    if (row.overview_record?.id !== row.overview_id || row.overview_record.public_visible !== false) reject('overview identity/state mismatch');
    if (!Array.isArray(row.reader_links)) reject('missing reader links');
    const targetIds = new Set();
    for (const link of row.reader_links) {
      if (!['PRIMARY', 'FOLLOWUP', 'BACKGROUND'].includes(link.role) || targetIds.has(link.reader_id)) reject('invalid or duplicate reading role');
      const target = atlas.getReader(link.reader_id);
      if (!target || target.title !== link.title) reject('unknown or renamed reader');
      targetIds.add(link.reader_id);
      if (!reverse.has(link.reader_id)) reverse.set(link.reader_id, []);
      reverse.get(link.reader_id).push({overviewId: row.overview_id, title: row.title, role: link.role, status: row.mapping_status, scope: row.scope});
    }
    if ((row.mapping_status === 'NO_MATCH') !== (row.reader_links.length === 0)) reject('empty reading state mismatch');
    if (row.mapping_status === 'BACKGROUND_ONLY' && row.reader_links.some(l => l.role !== 'BACKGROUND')) reject('background promoted to primary');
    if (['DIRECT_TOPIC', 'PARTIAL_COVERAGE'].includes(row.mapping_status) && !row.reader_links.some(l => l.role === 'PRIMARY')) reject('missing primary reading');
    counts[row.mapping_status]++; rows.set(row.overview_id, row);
  }
  if (!Array.isArray(x.exclusions) || x.exclusions.length !== 5) reject('missing false-match rules');
  for (const rule of x.exclusions) {
    const row = rows.get(rule.overview_id);
    if (!row || !Array.isArray(rule.forbidden_reader_ids)) reject('invalid false-match rule');
    if (row.reader_links.some(l => rule.forbidden_reader_ids.includes(l.reader_id))) reject('excluded false match');
  }
  const expected = {DIRECT_TOPIC: 64, PARTIAL_COVERAGE: 14, BACKGROUND_ONLY: 1, NO_MATCH: 18};
  for (const key of Object.keys(expected)) if (counts[key] !== expected[key]) reject('coverage mismatch');
  const resolve = (id, {includeRelated = false} = {}) => {
    if (!rows.has(id)) return null;
    const row = rows.get(id);
    const selected = row.reader_links.filter(l => l.role === 'PRIMARY' || includeRelated);
    return {overviewId: id, title: row.title, status: row.mapping_status, label: labels[row.mapping_status], scope: row.scope,
      hasPrimaryReading: row.reader_links.some(l => l.role === 'PRIMARY'),
      readers: selected.map(l => ({id: l.reader_id, title: l.title, lead: atlas.getReader(l.reader_id).lead, role: l.role})),
      message: row.mapping_status === 'NO_MATCH' ? '이 항목의 심화 원고는 아직 준비되지 않았습니다.' : row.mapping_status === 'BACKGROUND_ONLY' ? '직접 해설은 없으며 관련 배경 자료만 있습니다.' : row.scope,
      canPublish: false};
  };
  return Object.freeze({version: '3.06', canPublish: false,
    coverage: Object.freeze({total: 97, direct: 64, partial: 14, background: 1, missing: 18}),
    resolve,
    listOverview: ({status = null} = {}) => [...rows.values()].filter(r => !status || r.mapping_status === status).map(r => ({id: r.overview_id, title: r.title, category: r.category, status: r.mapping_status, scope: r.scope})),
    forReader: readerId => structuredClone(reverse.get(readerId) ?? []),
  });
}
