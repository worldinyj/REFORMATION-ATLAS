import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,verifyV328,reviewOnlyOutputs} from '../../scripts/build_v328_methodist_rules_witness.mjs';
const clone=x=>structuredClone(x);
test('frozen V3.27 and V3.28 evidence-only data scope',()=>{
 const x=loadInputs();
 assert.deepEqual(verifyV328(x),{sources:11,editions:6,claims:12,readings:3,sections:9,issues:8});
 assert.equal(x.contract.publication_gate.webapp_integrated,false);
});
test('cannot falsely promote 1785 indexed scholarly Q16 as direct photographed Cist folio',()=>{
 const x=loadInputs(),a=clone(x);a.contract.topic_evidence.find(x=>x.id==='V328-E-1785-AMERICA').proof='DIRECT_PRINT_VISUAL';
 assert.throws(()=>verifyV328(a),/Expected values to be strictly equal/);
 const b=clone(x);b.contract.witness_ledger.american_1785_Q16_Q17_original_pages=1;
 assert.throws(()=>verifyV328(b),/Expected values to be strictly equal/);
});
test('1789 6 months and 1789 full General Rules section are distinct editorial changes',()=>{
 const x=loadInputs();verifyV328(x);
 const a=x.contract.topic_evidence.find(x=>x.id==='V328-E-1789-AMERICA');
 const b=x.contract.topic_evidence.find(x=>x.id==='V328-E-1789-GENERAL-RULES');
 assert.equal(a.months,6);assert.equal(b.months,null);
 assert.notEqual(a.proof,b.proof);
 const c=clone(x);c.contract.topic_evidence.find(x=>x.id==='V328-E-1789-GENERAL-RULES').months=6;
 assert.throws(()=>verifyV328(c),/Expected values to be strictly equal/);
});
test('historical secondary dating cannot be promoted to visual original witness',()=>{
 const x=loadInputs();
 const a=clone(x);a.contract.topic_evidence.find(x=>x.id==='V328-E-1789-AMERICA').direct_year_edition_body_page_read=true;
 assert.throws(()=>verifyV328(a),/Expected values to be strictly deep-equal/);
 const b=clone(x);b.contract.witness_ledger.american_1789_general_rules_original_pages=1;
 assert.throws(()=>verifyV328(b),/Expected values to be strictly equal/);
});
test('1798 six months text cannot become exact paragraph screenshot while original unavailable',()=>{
 const x=loadInputs();const changed=clone(x);
 changed.contract.topic_evidence.find(x=>x.id==='V328-E-1798-AMERICA').proof='DIRECT_PRINT_VISUAL';
 assert.throws(()=>verifyV328(changed),/Expected values to be strictly equal/);
});
test('1785 Q17 answer and antislavery text must remain source qualified',()=>{
 const x=loadInputs();verifyV328(x);
 assert.ok(x.contract.claim_cards.find(x=>x.id==='V328-C03').claim.includes('answer not read'));
 assert.ok(x.contract.claim_cards.find(x=>x.id==='V328-C10').claim.includes('not identical'));
 assert.ok(x.contract.open_issues.some(x=>x.topic==='1785_Q16_Q17_PAGE'));
 assert.ok(x.contract.open_issues.some(x=>x.topic==='1785_Q42_ORIGINAL'));
});
test('review-only data exports never signal publication or merge',()=>{
 const x=loadInputs();verifyV328(x);
 const out=reviewOnlyOutputs(x);
 assert.deepEqual(Object.keys(out),['v328_methodist_1785_1789_claims.json','v328_methodist_edition_events.json','v328_primary_source_research_gaps.json']);
 assert.deepEqual(Object.values(out).map(x=>x.count),[12,6,8]);
 assert.ok(Object.values(out).every(x=>x.publication_ready===false&&x.webapp_integrated===false&&x.original_1785_to_1789_same_text_pairs===0));
});
