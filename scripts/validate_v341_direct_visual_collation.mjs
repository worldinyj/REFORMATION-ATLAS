#!/usr/bin/env node
/**
 * ATLAS V3.41.1 direct 1531 facsimile evidence guard.
 * Read-only; proof of specific Munich 1531 exemplar, NOT 1858 CR26 nor 1530 submission.
 */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const f=JSON.parse(readFileSync(path.join(root,'data/contracts/atlas_v341_1531_rhau_direct_visual_collation.json'),'utf8'));
assert.equal(f.schema,'atlas.research.v341.facsimile_direct_reading.v1');
assert.equal(f.version,'3.41.1');
assert.equal(f.status,'RESEARCH_DRAFT_HOLD');
assert.equal(f.publication_allowed,false);
assert.equal(f.webapp_integrated,false);
assert.equal(f.responsible_witness.digitized_object,'bsb00103368');
assert.equal(f.responsible_witness.vd16,'C 4737');
assert.equal(f.responsible_witness.shelfmark,'4 H.ref. 205 b');
assert.equal(f.responsible_witness.date,1531);
assert.deepEqual(f.responsible_witness.visual_read_canvases,[15,16]);
assert.equal(f.responsible_witness.direct_read_original_1531_surviving_print_pages,2);
assert.equal(f.evidence_runs.length,3);
assert.deepEqual(f.evidence_runs.map(x=>x.run_id),[42536205697,42536298524,42536364300]);
assert.deepEqual(f.readings.map(x=>x.id),['W01','W02','W03','W04']);
assert.deepEqual(f.readings.map(x=>x.normalized_reading),['iustificentur','consentire','mali','sentiebant']);
assert.deepEqual(f.readings.map(x=>x.rejected_BA_web_spelling),['iustificenter','consentiere','malii','sentibant']);
assert.ok(f.readings.every(x=>x.status.startsWith('DIRECT_PRINT_EXEMPLAR_READING_VERIFIED')));
assert.ok(f.readings.every(x=>x.canvas_zero_index===x.canvas_ordinal_1based-1));
assert.ok(f.readings.every(x=>x.source_image.includes('bsb00103368_')));
assert.equal(f.readings[3].physical_print_reading,'ſentie- / bant');
assert.ok(f.readings.every(x=>x.ocr_locator_bbox.length===4));
assert.ok(f.blocked_overclaims.some(x=>x.includes('1858 CR XXVI 263')));
assert.equal(f.metrics.original_1531_exemplar_scanned_pages_visually_read,2);
assert.equal(f.metrics.witnesses_directly_visually_read,1);
assert.equal(f.metrics.words_directly_verified,4);
assert.equal(f.metrics.other_1531_exemplar_collations,0);
assert.equal(f.metrics.cr26_1858_263_336_original_pages_directly_read,0);
assert.equal(f.metrics.corpus_updates,0);
assert.equal(f.metrics.published,false);
console.log('V3.41.1 PASS: 1531 Munich facsimile W01-W04 4/4 visually read; 1858/other copies UNCOLLATED; publication HOLD');
