import test from 'node:test';
import assert from 'node:assert/strict';
import {loadStudy,validateV336,reviewOnly} from '../../scripts/build_v336_bornkamm_two_text_stemma.mjs';
const copy=x=>structuredClone(x);
test('V3.35 immutable, V3.36 19 sources, 11 witnesses, 10 edges, 15 claims, 9 reading sections',()=>{
 const d=loadStudy();
 assert.deepEqual(validateV336(d),{sources:19,edition_and_manuscript_nodes:11,relations:10,claims:15,readings:3,sections:9,web_transcription_flags:3,open_issues:10});
});
test('1573 Fabricius Augsburg Confession and Roman Confutatio are two different textual domains',()=>{
 const d=loadStudy();
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V336-N05').document_domain,'CONFESSION_IN_EDITORIAL_COLLECTION');
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V336-N06').document_domain,'CATHOLIC_REBUTTAL_DISTINCT_WORK');
 const bad=copy(d);bad.contract.relations.find(x=>x.id==='V336-L10').type='SAME_ORIGINAL_AUTOGRAPH';
 assert.throws(()=>validateV336(bad));
});
test('CR XXVI was printed in 1858 and is Confession, CR XXVII 1859 is Confutatio',()=>{
 const d=loadStudy();
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V336-N10').year,1858);
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V336-N11').year,1859);
 assert.equal(d.contract.relations.find(x=>x.id==='V336-L07').type,'CR26_CONFESSION_COLLATION_REFERENCE');
 const bad=copy(d);bad.contract.witness_nodes.find(x=>x.id==='V336-N10').year=1859;
 assert.throws(()=>validateV336(bad));
});
test('Bornkamm p10 note22 locates 1577 Coelestin reproduction, not 1597 and not Confutatio',()=>{
 const d=loadStudy();validateV336(d);
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V336-N07').year,1577);
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V336-N09').year,1597);
 assert.equal(d.contract.relations.find(x=>x.id==='V336-L05').type,'REPRINT_OF_FABRICIUS_CONFESSION_TEXT');
 const bad=copy(d);bad.contract.relations.find(x=>x.id==='V336-L05').to='V336-N09';
 assert.throws(()=>validateV336(bad));
});
test('independent Fabricius Latin confession witness does not mean primary 1530 autograph or superior witness',()=>{
 const d=loadStudy();
 const p=d.contract.relations.find(x=>x.id==='V336-L04');
 assert.equal(p.type,'INDEPENDENT_CONFESSION_PRINT_WITNESS_PROVENANCE_UNKNOWN');
 assert.equal(d.contract.evidence_ledger.original_Fabricius_1573_book_interior_pages_read,0);
 const bad=copy(d);bad.contract.evidence_ledger.original_Fabricius_1573_book_interior_pages_read=1;
 assert.throws(()=>validateV336(bad));
});
test('Digital Latin transcript spellings are not certified historical original-print variants',()=>{
 const d=loadStudy();const f=d.contract.digital_latin_transcription_flags;
 assert.deepEqual(f.map(x=>x.article),['IV','VII','VIII']);
 assert.equal(f[0].transcribed,'gratis iustificenter');
 assert.equal(f[1].transcribed,'consentiere');
 assert.equal(f[2].transcribed,'malii / sentibant');
 const bad=copy(d);bad.contract.digital_latin_transcription_flags[0].original_1858_print_checked=true;
 assert.throws(()=>validateV336(bad));
});
test('New Bornkamm academic article screenshots are not actual 16th century folios',()=>{
 const d=loadStudy();
 assert.deepEqual(d.contract.evidence_ledger.bornkamm_modern_print_pages_visually_seen,[10,14,15]);
 assert.equal(d.contract.evidence_ledger.original_Coelestin_1577_pages_read,0);
 assert.equal(d.contract.evidence_ledger.CR26_1858_original_print_folios_read,0);
 const bad=copy(d);bad.contract.evidence_ledger.CR26_1858_original_print_folios_read=2;
 assert.throws(()=>validateV336(bad));
});
test('V3.34 CR XXVII original witness state survives V3.36; outputs remain three unpublished JSONs',()=>{
 const d=loadStudy();validateV336(d);const o=reviewOnly(d);
 assert.deepEqual(Object.keys(o),[
 'v336_two_text_augustana_confutatio_stemma.json',
 'v336_bornkamm_source_grade_claims.json',
 'v336_cr26_1858_web_transcription_followups.json'
 ]);
 assert.deepEqual(Object.values(o).map(x=>x.count),[11,15,10]);
 assert.deepEqual(d.contract.evidence_ledger.CR27_1859_original_confutatio_pages_prior_V334,[70,73,74,75]);
 assert.ok(Object.values(o).every(x=>x.published===false&&!x.webapp_integrated&&x.first_1573_interior_print_folios_seen===0));
});
