import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {createMediumAtlas} from './adapter.mjs';
const manifest = JSON.parse(readFileSync(new URL('./manifest.json', import.meta.url), 'utf8'));
const raw = readFileSync(new URL('../../' + manifest.input.path, import.meta.url), 'utf8');
const bundle = JSON.parse(raw);
const atlas = createMediumAtlas(bundle);
const mutate = change => { const x = structuredClone(bundle); change(x); return x; };

test('frozen input identity and consumer counts match the manifest', () => {
  assert.equal(createHash('sha256').update(raw).digest('hex'), manifest.input.sha256);
  assert.deepEqual(atlas.counts, manifest.expectedCounts);
  assert.equal(atlas.canPublish, false);
  assert.equal(atlas.mode, 'EDITORIAL_PREVIEW_ONLY');
});
test('all 455 details preserve original text, questions and source references', () => {
  for (const c of bundle.readers) {
    const detail = atlas.getReader(c.id);
    assert.equal(detail.title, c.title); assert.equal(detail.lead, c.lead);
    assert.deepEqual(detail.sections, c.sections); assert.equal(detail.readingQuestion, c.reading_question);
    assert.deepEqual(detail.sources.map(s => s.id), c.sources);
    assert.deepEqual(detail.relatedReaders.map(c => c.id), c.related_readers);
    assert.equal(detail.expertApproved, false);
  }
  assert.equal(atlas.listReaders().length, 455);
});
test('all source guides, selected claims and warnings resolve with their scope intact', () => {
  for (const g of bundle.reader_source_cards) {
    const out = atlas.getSourceGuide(g.reader_id);
    assert.equal(out.verificationNote, g.verification_note);
    assert.equal(out.claims.length, 2);
    assert.deepEqual(out.preferredSourceIds, g.preferred_source_ids);
    assert.deepEqual(out.cautions.map(w => w.id), g.warning_ids);
  }
  for (const c of bundle.source_verification.selected_claims) {
    const out = atlas.getClaim(c.id);
    assert.equal(out.exact_text_span, c.exact_text_span);
    assert.equal(out.status, c.status);
    assert.equal(out.expert_approved, false); assert.equal(out.original_witness_collated, false);
  }
  assert.equal(atlas.getClaim('CLAIM-V297-17').label, '부분 뒷받침·추가 확인 필요');
});
test('current failed/partial access is distinct from historical access and from unreviewed sources', () => {
  assert.equal(atlas.getSource('V296-LEGACY-02').access.status, 'ACCESS_FAILED');
  assert.equal(atlas.getSource('SRC-V205-MARB-ARCH').access.status, 'PARTIAL_PAGE_THEN_TIMEOUT');
  assert.equal(atlas.getSource('SRC-V205-MARB-ARCH').historicalAccessRecord.accessStatus, 'SEARCH_RESULT_EXCERPT_ONLY');
  assert.equal(atlas.getSource('SRC-V205-WORMS').access.status, 'PAGE_RETURNED');
  const untouched = bundle.sources.find(s => !s.verification_v297);
  assert.equal(atlas.getSource(untouched.id).access.status, 'NOT_CHECKED');
  assert.equal(atlas.getSource(untouched.id).access.checkedOn, null);
});
test('search finds Korean whitespace variants, body-only facts and normalized Latin text', () => {
  for (const [query, expected] of [
    ['카를 5세', 'MEDIUM-LUTHER1521'], ['루터 1517', 'MEDIUM-LUTHER1517'],
    ['구드브란두르', 'DOCUMENT-GUDBRANDUR_BIBLE1584'],
    ['말뫼', 'PERSON-HANS_TAUSEN'], ['Ｂｉｂｌｉａ', 'DOCUMENT-SKARYNA_BIBLE1517'],
  ]) assert.ok(atlas.search(query, {limit: 100}).items.some(c => c.id === expected), query);
  assert.deepEqual(atlas.search('  '), {total: 0, items: []});
  assert.equal(atlas.search('존재하지않는검색어XYZ').total, 0);
});
test('search supports type filters, stable ordering and non-overlapping pagination', () => {
  const result = atlas.search('성경', {limit: 100});
  assert.ok(result.total > 5);
  assert.deepEqual(atlas.search('성경', {limit: 2}).items, result.items.slice(0, 2));
  assert.deepEqual(atlas.search('성경', {limit: 2, offset: 2}).items, result.items.slice(2, 4));
  assert.ok(atlas.search('성경', {type: 'DOCUMENT'}).items.every(c => c.type === 'DOCUMENT'));
  assert.throws(() => atlas.search('성경', {limit: 0}), RangeError);
  assert.throws(() => atlas.search('성경', {offset: -1}), RangeError);
  assert.throws(() => atlas.search(null), TypeError);
});
test('all groups, 21 paths plus six legacy paths, comparisons and FAQ resolve', () => {
  const groups = atlas.listGroups();
  assert.equal(new Set(groups.flatMap(g => g.reader_ids)).size, 455);
  assert.equal(atlas.listReadingPaths().length, 21);
  assert.equal(atlas.listReadingPaths({includeLegacy: true}).length, 27);
  for (const axis of ['REGION', 'CHRONOLOGY', 'ISSUE']) assert.equal(atlas.listReadingPaths({axis}).length, 7);
  for (const p of atlas.listReadingPaths({includeLegacy: true})) {
    assert.equal(atlas.getReadingPath(p.id).id, p.id);
    assert.ok(p.reader_ids.every(id => atlas.getReader(id)));
  }
  assert.equal(atlas.listComparisons().length, 6); assert.equal(atlas.listFAQ().length, 12);
});
test('missing lookups return null; all 10 inherited research chapters remain available', () => {
  for (const getter of [atlas.getReader, atlas.getSource, atlas.getSourceGuide, atlas.getClaim, atlas.getReadingPath, atlas.getResearchBasis]) assert.equal(getter('missing'), null);
  for (const b of bundle.research_basis) assert.equal(atlas.getResearchBasis(b.id).chapter.body, b.chapter.body);
});
test('caller input and returned objects cannot mutate the internal snapshot', () => {
  const input = structuredClone(bundle), before = JSON.stringify(input), client = createMediumAtlas(input);
  assert.equal(JSON.stringify(input), before);
  input.readers[0].sections[0].body = 'changed';
  const detail = client.getReader(bundle.readers[0].id); detail.sections[0].body = 'changed again';
  client.getSource('SRC-V205-WORMS').access.status = 'wrong';
  client.listReadingPaths()[0].reader_ids.push('bad');
  assert.equal(client.getReader(bundle.readers[0].id).sections[0].body, bundle.readers[0].sections[0].body);
  assert.equal(client.getSource('SRC-V205-WORMS').access.status, 'PAGE_RETURNED');
  assert.ok(!client.listReadingPaths()[0].reader_ids.includes('bad'));
});
const corruptions = [
  ['version', x => { x.version = '2.99'; }],
  ['status', x => { x.status = 'APPROVED'; }],
  ['missing hold', x => { delete x.publication_gate; }],
  ['publication', x => { x.publication_gate.published = true; }],
  ['historian approval', x => { x.publication_gate.historian_approved = true; }],
  ['missing reader', x => x.readers.pop()],
  ['duplicate reader', x => { x.readers[1].id = x.readers[0].id; }],
  ['missing source', x => x.sources.pop()],
  ['duplicate source', x => { x.sources[1].id = x.sources[0].id; }],
  ['blank body', x => { x.readers[0].sections[0].body = ''; }],
  ['missing section', x => x.readers[0].sections.pop()],
  ['dangling source', x => x.readers[0].sources.push('missing')],
  ['empty source list', x => { x.readers[0].sources = []; }],
  ['dangling related', x => x.readers[0].related_readers.push('missing')],
  ['self reference', x => x.readers[0].related_readers.push(x.readers[0].id)],
  ['source script URL', x => { x.sources[0].url = 'javascript:alert(1)'; }],
  ['URL credentials', x => { x.sources[0].url = 'https://user:pass@example.com/'; }],
  ['claim text drift', x => { x.source_verification.selected_claims[0].exact_text_span = 'absent text'; }],
  ['claim expert flag', x => { x.source_verification.selected_claims[0].expert_approved = true; }],
  ['claim status upgrade', x => { x.source_verification.selected_claims[0].status = 'PROVEN'; }],
  ['guide mismatch', x => { x.reader_source_cards[0].reader_id = x.readers[1].id; }],
  ['path unresolved', x => x.reading_paths[0].reader_ids.push('missing')],
  ['group incomplete', x => x.reader_groups[0].reader_ids.pop()],
  ['comparison unresolved', x => { x.comparisons[0].rows[0].reader_id = 'missing'; }],
  ['FAQ unresolved', x => x.faq[0].related_readers.push('missing')],
  ['metric mismatch', x => { x.metrics.readers = 434; }],
];
for (const [name, change] of corruptions) test(`reject inconsistent import: ${name}`, () => assert.throws(() => createMediumAtlas(mutate(change))));
