import test from 'node:test';
import assert from 'node:assert/strict';
import {loadResearch,validateV330,reviewOnly} from '../../scripts/build_v330_general_rules_relocation.mjs';
const clone=x=>structuredClone(x);

test('frozen V3.29 parent and 11 sources, 7 typed links, 14 claims, 9 reading sections',()=>{
 const input=loadResearch();
 assert.deepEqual(validateV330(input),{sources:11,nodes:7,links:7,claims:14,upgrades:4,readings:3,sections:9,issues:9});
 assert.equal(input.contract.publication_gate.published,false);
 assert.equal(input.contract.metrics.original_513_reader_mutations,0);
});
test('1788 annex to 1789 main body is evidenced by Baker but not primary print scan',()=>{
 const input=loadResearch(),rel=input.contract.typed_relations.find(r=>r.id==='V330-L02');
 assert.equal(rel.type,'ANNEX_TO_MAIN_BODY_REPOSITION');
 assert.equal(rel.proof_type,'ACADEMIC_HISTORICAL_SYNTHESIS');
 assert.equal(rel.direct_folio_comparison,false);
 const bad=clone(input);bad.contract.typed_relations.find(r=>r.id==='V330-L02').type='FIRST_PRINT_1789';
 assert.throws(()=>validateV330(bad),/Expected values to be strictly equal/);
});
test('1789 General Rules move is distinct from 1790 other doctrinal tract incorporation',()=>{
 const input=loadResearch(),rels=input.contract.typed_relations;
 assert.equal(rels.find(r=>r.id==='V330-L02').to,'V330-N04');
 assert.equal(rels.find(r=>r.id==='V330-L03').to,'V330-N05');
 const fake=clone(input);fake.contract.typed_relations.find(r=>r.id==='V330-L03').to='V330-N04';
 assert.throws(()=>validateV330(fake),/Expected values to be strictly equal/);
});
test('1997 Ruth academic article pages must never be promoted to 1788 Kollock original p41',()=>{
 const input=loadResearch();
 assert.equal(input.contract.witness_ledger.scholarly_1997_print_pages_visually_inspected,2);
 assert.equal(input.contract.witness_ledger.original_1788_1992_reprint_page41_visually_inspected,0);
 const fake=clone(input);fake.contract.witness_ledger.original_1788_1992_reprint_page41_visually_inspected=1;
 assert.throws(()=>validateV330(fake),/Expected values to be strictly equal/);
 const fake2=clone(input);fake2.contract.claim_cards.find(c=>c.id==='V330-C08').approved_for_publication=true;
 assert.throws(()=>validateV330(fake2),/Expected values to be strictly equal/);
});
test('Baker article PDF text is not a successfully rendered scanned image and original witness pairs are zero',()=>{
 const input=loadResearch();
 assert.equal(input.contract.witness_ledger.scholarly_Baker_exact_PDF_page_screenshots_read,0);
 assert.equal(input.contract.witness_ledger.scholarly_Baker_PDF_page_screenshot_error,'HTTP_403');
 const fake=clone(input);fake.contract.witness_ledger.scholarly_Baker_exact_PDF_page_screenshots_read=3;
 assert.throws(()=>validateV330(fake),/Expected values to be strictly equal/);
 const fake2=clone(input);fake2.contract.witness_ledger.aligned_1788_1789_original_print_page_pairs=1;
 assert.throws(()=>validateV330(fake2),/Expected values to be strictly equal/);
});
test('previous 1789-first-print error must remain blocked in the updated typed graph',()=>{
 const input=loadResearch();
 assert.ok(input.contract.blocked_overclaims.includes('1789 was first American publication of General Rules'));
 assert.ok(input.contract.blocked_overclaims.includes('1790 was first year General Rules moved inside main body'));
 assert.ok(input.contract.upgrades.some(x=>x.id==='V330-REV01'));
 assert.ok(input.contract.unresolved.some(x=>x.id==='V330-I01'));
 const fake=clone(input);fake.contract.document_nodes.find(n=>n.id==='V330-N03').status='FIRST_EVER_RULES_PRINT_1788';
 assert.throws(()=>validateV330(fake),/Expected values to be strictly equal/);
});
test('review export is three JSONs and none is published or integrated to webapp',()=>{
 const input=loadResearch();validateV330(input);
 const outputs=reviewOnly(input);
 assert.deepEqual(Object.keys(outputs),[
  'v330_1788_1789_edition_relocation_graph.json',
  'v330_claim_source_provenance.json',
  'v330_original_pages_to_inspect.json'
 ]);
 assert.deepEqual(Object.values(outputs).map(x=>x.count),[7,14,9]);
 assert.ok(Object.values(outputs).every(o=>o.publication_ready===false&&o.google_ai_studio_webapp_integrated===false&&o.direct_1788_1789_original_print_pairs===0));
});
