import test from 'node:test';
import assert from 'node:assert/strict';
import {loadStudy,validateV331,reviewOnly} from '../../scripts/build_v331_original_folio_access_matrix.mjs';
const clone=x=>structuredClone(x);
test('V3.30 frozen, V3.31 holds 14 sources and 9 original page requests',()=>{
 const d=loadStudy();
 assert.deepEqual(validateV331(d),{sources:14,targets:9,comparisons:10,readings:3,sections:9,issues:9});
 assert.equal(d.contract.publication_gate.published,false);
});
test('1788 Kollock and 1789 Ross book page targets are edition-specific',()=>{
 const d=loadStudy();validateV331(d);
 const x=d.contract.original_page_requests;
 assert.equal(x.find(t=>t.id==='V331-T01').edition,'KOLLOCK_BOOK_TITLE');
 assert.equal(x.find(t=>t.id==='V331-T04').edition,'ROSS_FIFTH_TITLE');
 assert.equal(x.find(t=>t.id==='V331-T03').target_type,'PRINTED_P41');
 const incorrect=clone(d);incorrect.contract.original_page_requests.find(t=>t.id==='V331-T04').year=1788;
 assert.throws(()=>validateV331(incorrect),/Expected values to be strictly equal/);
});
test('a catalogue hit cannot become a directly visually checked historical page',()=>{
 const d=loadStudy(),fake=clone(d);
 fake.contract.original_page_requests.find(t=>t.id==='V331-T03').original_leaf_visual_check_pass=true;
 assert.throws(()=>validateV331(fake),/missing original must not become visually verified/);
 const f2=clone(d);f2.contract.source_registry.find(s=>s.id==='V331-S02').contemporary_1788_1789_page_directly_seen=true;
 assert.throws(()=>validateV331(f2),/source evidence incorrectly upgraded/);
});
test('1898/1997 historical pages remain separate from 1788/1789 original collations',()=>{
 const d=loadStudy();validateV331(d);
 const l=d.contract.inspection_ledger;
 assert.equal(l.historical_Tigert_1898_print_pages_visual_previous_V329,2);
 assert.equal(l.scholarly_Ruth_1997_print_pages_visual_previous_V330,2);
 assert.equal(l.original_same_passage_pairs_aligned,0);
 const fake=clone(d);fake.contract.inspection_ledger.original_same_passage_pairs_aligned=1;
 assert.throws(()=>validateV331(fake),/Expected values to be strictly equal/);
});
test('1888 false-friend must never be substituted for original 1788 edition',()=>{
 const d=loadStudy();
 const s=d.contract.source_registry.find(s=>s.id==='V331-S10');
 assert.equal(s.evidence_type,'CHRONOLOGICAL_FALSE_FRIEND');
 assert.ok(s.what_verified.includes('one century newer'));
 const fake=clone(d);fake.contract.source_registry.find(s=>s.id==='V331-S10').evidence_type='1788_ORIGINAL_PRINT_SCAN';
 assert.throws(()=>validateV331(fake),/Expected values to be strictly equal/);
});
test('1787 Evans index viewer requires JS and is not direct original 1788 or 1789',()=>{
 const d=loadStudy();const src=d.contract.source_registry.find(s=>s.id==='V331-S09');
 assert.equal(src.evidence_type,'DIGITAL_TRANSCRIPTION_INDEX_JAVASCRIPT_GATE');
 assert.equal(d.contract.original_page_requests.find(t=>t.id==='V331-T08').access_status,'INDEX_ONLY');
 const fake=clone(d);fake.contract.original_page_requests.find(t=>t.id==='V331-T08').access_status='NO_DIRECT_IMAGE';
 assert.throws(()=>validateV331(fake),/Expected values to be strictly equal/);
});
test('Bangs temperance quotation stays a later historian quotation, not 1789 first-print scan',()=>{
 const d=loadStudy();const x=d.contract.comparison_cards.find(x=>x.id==='V331-X04');
 assert.equal(x.primary_source_id,'V331-S06');
 assert.equal(x.original_pages_compared,0);
 const fake=clone(d);fake.contract.comparison_cards.find(x=>x.id==='V331-X04').original_pages_compared=1;
 assert.throws(()=>validateV331(fake),/Expected values to be strictly equal/);
});
test('all outputs remain review only and do not insert anything into webapp',()=>{
 const d=loadStudy();validateV331(d);const o=reviewOnly(d);
 assert.deepEqual(Object.keys(o),[
  'v331_original_folio_request_manifest.json',
  'v331_source_level_edition_claims.json',
  'v331_unresolved_original_access_flags.json'
 ]);
 assert.deepEqual(Object.values(o).map(x=>x.count),[9,10,9]);
 assert.ok(Object.values(o).every(x=>!x.public_release_approved&&!x.webapp_integrated&&x.original_1788_1789_print_page_pairs===0));
});
