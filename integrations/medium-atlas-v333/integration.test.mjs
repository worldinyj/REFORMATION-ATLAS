import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,validateV333,draftReviewOutputs} from '../../scripts/build_v333_confutatio_latin_witness.mjs';
const cp=x=>structuredClone(x);
test('frozen V3.32 and V3.33 exact scope: 12 sources 7 Latin fragments 4 cases 12 sections',()=>{
 const input=loadInputs();
 assert.deepEqual(validateV333(input),{sources:12,latin_lemmas:7,article_cases:4,publication_events:6,essays:4,sections:12,gaps:10});
 assert.equal(input.contract.publication_gate.published,false);
});
test('1530 German oral reading MUST differ from 1573 first full printed Latin edition',()=>{
 const d=loadInputs(),st=d.contract.publication_stages;
 const oral=st.find(x=>x.id==='V333-D02'),first=st.find(x=>x.id==='V333-D04');
 assert.equal(oral.date,'1530-08-03');assert.equal(oral.first_published_latin_full_text,false);
 assert.equal(first.date,'1573');assert.equal(first.first_published_latin_full_text,true);
 const fake=cp(d);fake.contract.publication_stages.find(x=>x.id==='V333-D02').first_published_latin_full_text=true;
 assert.throws(()=>validateV333(fake),/Expected values to be strictly deep-equal/);
 const fake2=cp(d);fake2.contract.publication_stages.find(x=>x.id==='V333-D04').date='1530';
 assert.throws(()=>validateV333(fake2),/Expected values to be strictly equal/);
});
test('1531 Cochlaeus is summary only and 1808 German archival print is distinct',()=>{
 const d=loadInputs(),st=d.contract.publication_stages;
 assert.equal(st.find(x=>x.id==='V333-D03').type,'COCHLAEUS_SUMMARY_NOT_FULL_CONFUTATIO');
 assert.equal(st.find(x=>x.id==='V333-D05').type,'GERMAN_ARCHIVAL_CRITICAL_PUBLICATION_MUELLER');
 const fake=cp(d);fake.contract.publication_stages.find(x=>x.id==='V333-D03').type='FULL_CONFUTATIO_PRINT';
 assert.throws(()=>validateV333(fake),/Expected values to be strictly equal/);
});
test('CR27 Latin VIII acceptatur expressly supports historical ACCEPTANCE not REJECTION',()=>{
 const d=loadInputs();const c=d.contract.article_claim_adjudications.find(x=>x.id==='V333-C04');
 const literal=d.contract.latin_clause_records.find(x=>x.id==='V333-L04');
 assert.equal(literal.lemma,'acceptatur cum sancta romana ecclesia');
 assert.equal(c.confutatio_stance,'EXPLICIT_ACCEPTANCE_OF_ARTICLE_VIII');
 assert.equal(literal.critical_reference,'CR XXVII (1859) col105, cited in CPH Spanish note 189');
 const fake=cp(d);fake.contract.article_claim_adjudications.find(x=>x.id==='V333-C04').confutatio_stance='REJECTION';
 assert.throws(()=>validateV333(fake),/Expected values to be strictly equal/);
});
test('Confutatio VII conditional non potest and regional rites endorsement remain different facts',()=>{
 const d=loadInputs();const cards=d.contract.article_claim_adjudications;
 assert.equal(cards.find(x=>x.id==='V333-C02').confutatio_stance,'CONDITIONAL_REJECTION_OF_CHURCH_DEFINITION');
 assert.equal(cards.find(x=>x.id==='V333-C03').confutatio_stance,'PRAISES_LOCAL_RITUAL_VARIETY_BUT_DISTINGUISHES_UNIVERSAL');
 const fake=cp(d);fake.contract.article_claim_adjudications.find(x=>x.id==='V333-C03').confutatio_stance='TOTAL_REJECTION_OF_LOCAL_RITUALS';
 assert.throws(()=>validateV333(fake),/Expected values to be strictly equal/);
});
test('Confutatio IV gracious initiative is CR27 excerpt not Augsburg Confession source',()=>{
 const d=loadInputs();
 assert.equal(d.contract.latin_clause_records.find(x=>x.id==='V333-L01').source_ids[0],'V333-S-CR27-GOOGLE');
 assert.equal(d.contract.latin_clause_records.find(x=>x.id==='V333-L05').level,'AUGUSTANA_LATIN_LATER_UNCOLLATED_TRANSCRIPTION');
 const fake=cp(d);fake.contract.latin_clause_records.find(x=>x.id==='V333-L05').level='1530_CONFUTATIO_LATIN_PRINT';
 assert.throws(()=>validateV333(fake),/Expected values to be strictly equal/);
});
test('no 1530 or 1573 contemporary direct leaf claims and no 1859 print screenshot claim',()=>{
 const d=loadInputs();const l=d.contract.witness_ledger;
 assert.equal(l.direct_1530_german_original_pages,0);
 assert.equal(l.direct_1573_fabricius_latin_print_pages,0);
 assert.equal(l.direct_1859_CR27_print_pages,0);
 const fake=cp(d);fake.contract.witness_ledger.direct_1859_CR27_print_pages=1;
 assert.throws(()=>validateV333(fake),/Expected values to be strictly equal/);
 const fake2=cp(d);fake2.contract.source_records.find(s=>s.id==='V333-S-CPH-ES').critical_1859_printed_leaf_visually_inspected=true;
 assert.throws(()=>validateV333(fake2),/no original witness leaf was seen/);
});
test('research outputs are three draft JSONs only, with 7 6 10 records and no webapp approval',()=>{
 const d=loadInputs();validateV333(d);const output=draftReviewOutputs(d);
 assert.deepEqual(Object.keys(output),[
 'v333_latin_clause_evidence_grade.json',
 'v333_1530_1573_1859_publication_genealogy.json',
 'v333_original_language_primary_witness_queue.json']);
 assert.deepEqual(Object.values(output).map(x=>x.count),[7,6,10]);
 assert.ok(Object.values(output).every(x=>x.published===false&&x.webapp_integrated===false&&x.actual_original_latin_folios_seen===0));
});
