import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,validateV329,reviewOnly} from '../../scripts/build_v329_general_rules_correction.mjs';
const copy=structuredClone;
test('V3.28 frozen and V3.29 12 sources, 7 witnesses, 4 corrections, 9 new research sections',()=>{
 const x=loadInputs();const r=validateV329(x);
 assert.deepEqual(r,{sources:12,witnesses:7,links:6,corrections:4,readings:3,sections:9,issues:8});
 assert.equal(x.contract.publication_gate.published,false);
});
test('1788 Rules separate appendix overturns V3.28 first-1789 simplification',()=>{
 const x=loadInputs(),c=x.contract;
 assert.equal(c.witness_nodes.find(w=>w.id==='V329-W03').year,1788);
 assert.equal(c.relations.find(r=>r.id==='V329-REL01').type,'HISTORIAN_ATTESTED_SEPARATE_ANNEX');
 assert.equal(c.supersession_cards.find(r=>r.id==='V329-CORR01').status,'SUPERSEDED_OVERBROAD');
 const f=copy(x);f.contract.supersession_cards.find(r=>r.id==='V329-CORR01').status='UNCHANGED';
 assert.throws(()=>validateV329(f));
});
test('1787 Rules internal date is not 1788 Kollock imprint year',()=>{
 const x=loadInputs(),w=x.contract.witness_nodes;
 assert.equal(w.find(a=>a.id==='V329-W04').year,1787);
 assert.equal(w.find(a=>a.id==='V329-W03').year,1788);
 const f=copy(x);f.contract.witness_nodes.find(a=>a.id==='V329-W04').year=1788;
 assert.throws(()=>validateV329(f));
});
test('1898 historiography was scanned, not the 1788 or 1789 first print itself',()=>{
 const x=loadInputs();
 assert.equal(x.contract.source_scope.historical_1898_printed_pages_visually_read,2);
 assert.equal(x.contract.source_scope.original_1788_general_rules_pages_visually_read,0);
 const f=copy(x);f.contract.source_scope.original_1788_general_rules_pages_visually_read=2;
 assert.throws(()=>validateV329(f));
 const g=copy(x);g.contract.source_scope.direct_1788_1789_page_pairs_collated=1;
 assert.throws(()=>validateV329(g));
});
test('Emory not-found is not edition nonexistence: Vanderbilt 1788 holding retained',()=>{
 const x=loadInputs();
 assert.ok(x.contract.sources.some(s=>s.id==='V329-S-VANDERBILT1788'));
 assert.ok(x.contract.sources.some(s=>s.id==='V329-S-EMORY'));
 assert.ok(x.contract.supersession_cards.some(c=>c.id==='V329-CORR04'&&c.status==='SCOPE_CLARIFICATION'));
 const f=copy(x);f.contract.sources.find(s=>s.id==='V329-S-VANDERBILT1788').level='NO_1788_EDITION';
 assert.throws(()=>validateV329(f));
});
test('historical 1789 fifth, 1790 sixth, and 1992 facsimile are not same text pair evidence',()=>{
 const x=loadInputs(),w=x.contract.witness_nodes;
 assert.equal(w.find(z=>z.id==='V329-W05').year,1789);
 assert.equal(w.find(z=>z.id==='V329-W06').year,1790);
 assert.ok(w.some(z=>z.id==='V329-W07'));
 assert.ok(x.contract.open_issues.some(z=>z.id==='V329-I-FACSIMILE_OMISSION'));
 const f=copy(x);f.contract.relations.find(z=>z.id==='V329-REL03').exact_original_page_comparison=true;
 assert.throws(()=>validateV329(f));
});
test('three generated review-only exports cannot expose disputed first-1789 or imply publication',()=>{
 const x=loadInputs();validateV329(x);
 const o=reviewOnly(x);
 assert.deepEqual(Object.keys(o),[
 'v329_explicit_supersession_ledger.json',
 'v329_1787_1790_rules_edition_graph.json',
 'v329_original_witness_followup_queue.json'
 ]);
 assert.deepEqual(Object.values(o).map(x=>x.count),[4,6,8]);
 assert.ok(Object.values(o).every(x=>x.publication_ready===false&&x.webapp_integrated===false&&x.original_1788_1789_aligned_page_pairs===0));
});
