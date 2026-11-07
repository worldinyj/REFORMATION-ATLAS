import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,verifyV337,reviewOnly} from '../../scripts/build_v337_cr26_cr27_print_qa.mjs';
const clone=x=>structuredClone(x);
test('V3.36 parent hash, V3.37 physical source audit and all historical counts',()=>{
 const x=loadInputs();assert.deepEqual(verifyV337(x),{sources:10,cr26_pages:7,cr27_pages:4,online_corrections:4,editorial_notes:6,essays:3,sections:9,open_issues:7});
 assert.equal(x.contract.publication_gate.published,false);
});
test('1858 CR26 Confession distinct from 1859 CR27 Catholic Confutation',()=>{
 const x=loadInputs();
 assert.equal(x.contract.print_provenance.cr26.work,'CONFESSIO_AUGUSTANA');
 assert.equal(x.contract.print_provenance.cr27.work,'ROMAN_CONFUTATIO');
 assert.equal(x.contract.print_provenance.cr26.pdf_page_count,420);
 assert.equal(x.contract.print_provenance.cr27.pdf_page_count,360);
 const bad=clone(x);bad.contract.print_provenance.cr26.year=1859;
 assert.throws(()=>verifyV337(bad));
});
test('printed physical page to PDF mapping: 1858 original p275->162 and p277->163',()=>{
 const x=loadInputs();verifyV337(x);
 assert.deepEqual(x.contract.print_page_map_cr26.filter(p=>[162,163].includes(p.pdf_page)).map(p=>[p.pdf_page,p.left_printed_page]),[[162,275],[163,277]]);
 const bad=clone(x);bad.contract.print_page_map_cr26.find(p=>p.pdf_page===163).left_printed_page=278;
 assert.throws(()=>verifyV337(bad));
});
test('AC IV: 1858 actual iustificentur rather than online iustificenter',()=>{
 const x=loadInputs();
 assert.equal(x.contract.online_latin_qa[0].printed,'iustificentur');
 const bad=clone(x);bad.contract.online_latin_qa[0].printed='iustificenter';
 assert.throws(()=>verifyV337(bad));
});
test('AC VII: 1858 actual consentire, AC VIII: mali and sentiebant',()=>{
 const x=loadInputs();
 assert.deepEqual(x.contract.online_latin_qa.slice(1).map(z=>z.printed),['consentire','mali','sentiebant']);
 const bad=clone(x);bad.contract.online_latin_qa[3].printed='sentibant';
 assert.throws(()=>verifyV337(bad));
});
test('CR27 critical Fabr. notes are original 1859 reports, not direct 1573 pages',()=>{
 const x=loadInputs();
 assert.equal(x.contract.edition_apparatus_notes.find(z=>z.id==='V337-N6').printed_location,105);
 assert.equal(x.contract.witness_ledger.fabricius1573_original_interior_pages,0);
 const bad=clone(x);bad.contract.witness_ledger.fabricius1573_original_interior_pages=1;
 assert.throws(()=>verifyV337(bad));
});
test('do not promote unreviewed manuscript variants, original oral texts or public publication',()=>{
 const x=loadInputs();
 const bad=clone(x);bad.contract.witness_ledger.all_manuscript_variants_verified=true;
 assert.throws(()=>verifyV337(bad));
 const bad2=clone(x);bad2.contract.publication_gate.webapp_integrated=true;
 assert.throws(()=>verifyV337(bad2));
});
test('the three source-grade review JSON artifacts are not public app data',()=>{
 const x=loadInputs();verifyV337(x);const out=reviewOnly(x);
 assert.deepEqual(Object.values(out).map(o=>o.count),[11,4,6]);
 assert.ok(Object.values(out).every(o=>o.published===false&&o.webapp_updated===false&&o.direct_1573_to_1859_original_pairs===0));
});
