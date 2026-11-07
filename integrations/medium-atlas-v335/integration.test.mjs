import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,validateV335,reviewOnly} from '../../scripts/build_v335_fabricius_edition_graph.mjs';
const clone=x=>structuredClone(x);
test('V3.34 parent locked, V3.35 real catalogues and original-page limits',()=>{
 const d=loadInputs();assert.deepEqual(validateV335(d),{sources:15,witnesses:8,relations:8,needed_loci:4,probe_results:4,warnings:10,readings:3,sections:9,gaps:10});
 assert.equal(d.contract.publication_gate.published,false);
});
test('actual first 1573 Fabricius Cologne Maternus Cholinus title and 574-page first print preserved',()=>{
 const d=loadInputs();validateV335(d);
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V335-E04').year,1573);
 assert.ok(d.contract.source_records.find(x=>x.id==='V335-S01').note.includes('574'));
 assert.ok(d.contract.witness_nodes.find(x=>x.id==='V335-E04').source_ids.includes('V335-S15'));
 const fake=clone(d);fake.contract.witness_nodes.find(x=>x.id==='V335-E04').year=1587;
 assert.throws(()=>validateV335(fake));
});
test('1587 augmented second edition is not 1573 first edition',()=>{
 const d=loadInputs();
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V335-E05').year,1587);
 assert.ok(d.contract.source_records.find(x=>x.id==='V335-S05').note.includes('515'));
 assert.equal(d.contract.typed_relations.find(x=>x.id==='V335-R02').type,'SEPARATE_REVISED_SECOND_EDITION');
 const fake=clone(d);fake.contract.typed_relations.find(x=>x.id==='V335-R02').type='IDENTICAL_EDITION';
 assert.throws(()=>validateV335(fake));
});
test('1573 Catholic Confutatio and reused Augsburg Confession are different document domains',()=>{
 const d=loadInputs();
 assert.equal(d.contract.typed_relations.find(x=>x.id==='V335-R06').type,'DIFFERENT_TEXT_DOMAIN_WITHIN_SAME_COLLECTION');
 assert.ok(d.contract.source_records.find(x=>x.id==='V335-S15').note.includes('Confutatio'));
 assert.ok(d.contract.warnings.some(x=>x.code==='BOOK_COMPOSITE_CONFUTATIO_VS_CONFESSION'));
 const fake=clone(d);fake.contract.typed_relations.find(x=>x.id==='V335-R06').type='ORIGINAL_1530_CONFESSION_AUTOGRAPH';
 assert.throws(()=>validateV335(fake));
});
test('1597 Coelestin derivative warning is retrospective and not newly verified original',()=>{
 const d=loadInputs();
 assert.equal(d.contract.witness_nodes.find(x=>x.id==='V335-E06').year,1597);
 assert.equal(d.contract.provenance_ledger.original_1597_Coelestin_book_folios_directly_read,0);
 assert.ok(d.contract.warnings.some(x=>x.code==='COELESTIN_1597_AUTHENTICITY_WARNING'));
 const fake=clone(d);fake.contract.provenance_ledger.original_1597_Coelestin_book_folios_directly_read=1;
 assert.throws(()=>validateV335(fake));
});
test('Google Books access HTTP 200 is HTML, and PDF HTTP 403 is not page verification',()=>{
 const d=loadInputs();
 assert.deepEqual(d.contract.digital_access_probes.map(x=>x.http_status),[200,403,200,403]);
 assert.ok(d.contract.digital_access_probes.every(x=>!x.pdf_directly_available&&!x.original_print_folio_visually_read));
 const bad=clone(d);bad.contract.digital_access_probes[1].pdf_directly_available=true;
 assert.throws(()=>validateV335(bad));
});
test('1859 directly verified latin print columns remain verified, yet 1573 exact pairs are zero',()=>{
 const d=loadInputs();
 assert.deepEqual(d.contract.chapter_comparison_requests.map(x=>x.cr27_print_column),[96,102,104,105]);
 assert.equal(d.contract.provenance_ledger.parallel_1573_vs_1859_original_latin_lemma_pairs,0);
 const bad=clone(d);bad.contract.chapter_comparison_requests[3].original_pair_collated=true;
 assert.throws(()=>validateV335(bad));
 const bad2=clone(d);bad2.contract.provenance_ledger.parallel_1573_vs_1859_original_latin_lemma_pairs=1;
 assert.throws(()=>validateV335(bad2));
});
test('Blackwell 1573 book cover/catalogue is evidence of existence, not direct original internal pages',()=>{
 const d=loadInputs();
 const s=d.contract.source_records.find(x=>x.id==='V335-S15');
 assert.equal(s.grade,'RARE_BOOK_DEALER_CATALOGUE_PAGE_VISUALLY_SCREENED');
 assert.equal(s.direct_1573_folio_seen,false);
 const bad=clone(d);bad.contract.source_records.find(x=>x.id==='V335-S15').direct_1573_folio_seen=true;
 assert.throws(()=>validateV335(bad));
});
test('research exports are three review-only JSONs and not published to webapp',()=>{
 const d=loadInputs();validateV335(d);const x=reviewOnly(d);
 assert.deepEqual(Object.keys(x),[
 'v335_1573_1587_edition_graph.json',
 'v335_fabricius_access_and_reading_provenance.json',
 'v335_1573_1859_original_print_comparison_queue.json'
 ]);
 assert.deepEqual(Object.values(x).map(t=>t.count),[8,4,10]);
 assert.ok(Object.values(x).every(t=>t.publication_ready===false&&t.webapp_integrated===false&&t.original_1573_print_pages_seen===0));
});
