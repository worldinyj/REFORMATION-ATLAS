#!/usr/bin/env node
/** V3.42.1: source-linked 1531/1858/Bibliotheca Augustana collation QC. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const d=JSON.parse(readFileSync(path.join(root,'data/contracts/atlas_v342_cr26_1858_direct_print_collation.json'),'utf8'));
assert.equal(d.schema,'atlas.research.v342.cr26_1858_direct_print_collation.v1');
assert.equal(d.version,'3.42.1');
assert.equal(d.status,'RESEARCH_DRAFT_HOLD');
assert.equal(d.publication_allowed,false);
assert.equal(d.webapp_integrated,false);
assert.deepEqual(d.historical_witnesses.map(x=>x.id),['V342-1531-MUNICH','V342-1858-CR26','V342-BA','V342-SCHAFF']);
assert.equal(d.historical_witnesses[0].digital_id,'bsb00103368');
assert.equal(d.historical_witnesses[0].vd16,'C 4737');
assert.equal(d.historical_witnesses[1].scan,'IA corpusreformato09melagoog / NYPL / Google digitization');
assert.deepEqual(d.historical_witnesses[1].book_print_pages_read,[275,276,277,278]);
assert.deepEqual(d.print_pdf_page_map.map(x=>x.pdf_page_1based),[162,163]);
assert.deepEqual(d.print_pdf_page_map.map(x=>x.printed_left),[275,277]);
assert.ok(d.print_pdf_page_map.every(x=>x.pdf_zero_based===x.pdf_page_1based-1));
assert.ok(d.print_pdf_page_map.every(x=>x.image.startsWith('https://thumb.wikimedia.org/')));
assert.equal(d.word_collations.length,4);
assert.deepEqual(d.word_collations.map(x=>x.id),['W01','W02','W03','W04']);
assert.deepEqual(d.word_collations.map(x=>x.article),['IV','VII','VIII','VIII']);
assert.deepEqual(d.word_collations.map(x=>x.cr26_print_page),[275,277,277,277]);
assert.deepEqual(d.word_collations.map(x=>x.cr26_pdf_page_1based),[162,163,163,163]);
assert.deepEqual(d.word_collations.map(x=>x.cr26_1858_print_normalized),
 ['iustificentur','consentire','mali','sentiebant']);
assert.deepEqual(d.word_collations.map(x=>x.ba_web),
 ['iustificenter','consentiere','malii','sentibant']);
for(const w of d.word_collations){
 assert.equal(w.first1531_print_normalized,w.cr26_1858_print_normalized,'independent historic witnesses differ');
 assert.notEqual(w.cr26_1858_print_normalized,w.ba_web,'BA web not a discrepant witness');
 assert.equal(w.status,'PRINT_1531_AND_1858_MATCH_BA_WEB_DIFFERS');
 assert.ok(w.conclusion_ko.length>30);
}
assert.equal(d.word_collations[3].first1531_print_as_typeset,'ſentie- / bant');
assert.equal(d.evidence_procedure.initial_validation_run_id,42537437470);
assert.equal(d.evidence_procedure.focused_validation_run_id,42537586479);
assert.equal(d.evidence_procedure.source_1858_print_visually_read,true);
assert.equal(d.evidence_procedure.same_1531_all_exemplars_confirmed,false);
assert.equal(d.outcome.readings_in_1531_exemplar_directly_verified,4);
assert.equal(d.outcome.readings_in_1858_cr26_directly_verified,4);
assert.equal(d.outcome.ba_transcription_discrepancies_established,4);
assert.equal(d.outcome.exact_process_that_created_ba_errors_established,0);
assert.equal(d.outcome.original_513_essays_changed,0);
assert.equal(d.outcome.publication_approved,false);
assert.ok(d.release_gates.some(x=>x.includes('Do not auto-patch')));
console.log('ATLAS V3.42.1 PASS: CR26 print 275/277 + 1531 print 4 matching; BA online differs 4; publication HOLD');
