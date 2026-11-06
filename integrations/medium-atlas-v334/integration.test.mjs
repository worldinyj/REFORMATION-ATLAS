import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,validateV334,reviewOnly} from '../../scripts/build_v334_cr27_direct_folio_audit.mjs';
const clone=x=>structuredClone(x);
test('V3.33 frozen; V3.34 has four directly read 1859 article clauses and historical evidence bounds',()=>{
 const d=loadInputs();
 assert.deepEqual(validateV334(d),{sources:9,printed_page_pairs:8,latin_clauses:4,findings:7,corrections:5,essays:4,sections:12,open_issues:9});
 assert.equal(d.contract.publication_gate.published,false);
 assert.equal(d.contract.metrics.original_reader_mutations,0);
});
test('1859 PDF file hash and printed-column to PDF page mapping match verified original',()=>{
 const d=loadInputs();
 assert.equal(d.contract.source_pdf.pdf_sha256,'ba1995d5587375a13f5298001e7a6c42d68f1c6b161ae86335471a1c4f30b29d');
 assert.equal(d.contract.source_pdf.pdf_page_count,360);
 const bad=clone(d);bad.contract.print_page_map.find(x=>x.pdf_page_1based===73).printed_right_col=103;
 assert.throws(()=>validateV334(bad),/Expected values to be strictly equal/);
});
test('V3.33 Google Books p99 localization is corrected to printed CR27 col96 PDF page70',()=>{
 const d=loadInputs();
 assert.equal(d.contract.latin_fragments.find(x=>x.id==='V334-F1').printed_col,96);
 assert.ok(d.contract.corrections.find(x=>x.id==='V334-C01').replacement.includes('column 96'));
 const bad=clone(d);bad.contract.corrections.find(x=>x.id==='V334-C01').replacement='printed p99';
 assert.throws(()=>validateV334(bad),/The expression evaluated to a falsy value/);
});
test('the Article VII rejection condition crosses col102 and col103; neither may be silently omitted',()=>{
 const d=loadInputs();validateV334(d);
 const x=d.contract.latin_fragments.find(x=>x.id==='V334-F2');
 assert.equal(x.pdf_page_1based,73);
 assert.ok(x.translation_and_context.includes('103열'));
 const bad=clone(d);bad.contract.latin_fragments.find(x=>x.id==='V334-F2').translation_and_context='All articles rejected unconditionally';
 assert.throws(()=>validateV334(bad),/The expression evaluated to a falsy value/);
});
test('Confutatio VIII 1859 col105 positive acceptatur must remain affirmative',()=>{
 const d=loadInputs();const clause=d.contract.latin_fragments.find(x=>x.id==='V334-F4');
 assert.equal(clause.latin,'acceptatur cum sancta romana ecclesia');
 assert.equal(clause.article,'VIII');
 const bad=clone(d);bad.contract.latin_fragments.find(x=>x.id==='V334-F4').latin='reiectatur cum sancta romana ecclesia';
 assert.throws(()=>validateV334(bad),/Expected values to be strictly equal/);
});
test('direct 1859 edition inspection does not assert 1530 spoken manuscript or 1573 first Latin print checked',()=>{
 const d=loadInputs();validateV334(d);
 assert.equal(d.contract.source_scope.original_1530_german_manuscript_pages_visually_read,0);
 assert.equal(d.contract.source_scope.original_1573_first_latin_print_pages_visually_read,0);
 assert.equal(d.contract.source_scope.full_1859_variant_apparatus_collated,false);
 const bad=clone(d);bad.contract.source_scope.original_1573_first_latin_print_pages_visually_read=1;
 assert.throws(()=>validateV334(bad),/Expected values to be strictly equal/);
});
test('editorial criticism of Hus and Wycliffe must not be transformed into established history',()=>{
 const d=loadInputs();
 assert.equal(d.contract.observations.find(x=>x.id==='V334-O05').type,'HUSS_WYCLIFFE_POLEMIC');
 assert.ok(d.contract.blocked_claims.some(x=>x.includes('Hus and Wycliffe')));
 const bad=clone(d);bad.contract.observations.find(x=>x.id==='V334-O05').type='HISTORICALLY_PROVEN_HERESY';
 assert.throws(()=>validateV334(bad),/Expected values to be strictly equal/);
});
test('review files count 4 5 9 and are not approved for release or webapp use',()=>{
 const d=loadInputs();validateV334(d);const output=reviewOnly(d);
 assert.deepEqual(Object.keys(output),[
  'v334_1859_folio_lemma_evidence.json',
  'v334_v333_locator_and_evidence_corrections.json',
  'v334_1573_1530_original_witness_queue.json'
 ]);
 assert.deepEqual(Object.values(output).map(x=>x.count),[4,5,9]);
 assert.ok(Object.values(output).every(x=>x.release_approved===false&&x.google_ai_studio_integrated===false&&x.original_1530_or_1573_direct_folios===0));
});
