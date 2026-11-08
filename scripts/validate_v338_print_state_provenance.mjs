#!/usr/bin/env node
/** Read-only V3.38 edition/exemplar provenance contract guard. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(readFileSync(path.join(root,'data/contracts/atlas_v338_1531_print_state_source_matrix.json'),'utf8'));
const unique=(items,label)=>assert.equal(new Set(items).size,items.length,`duplicate ${label}`);
assert.equal(data.schema,'atlas.research.v338.print_state_provenance.v1');
assert.equal(data.version,'3.38');
assert.equal(data.parent_version,'3.37.1');
assert.equal(data.status,'RESEARCH_DRAFT_HOLD');
assert.equal(data.published,false);
assert.equal(data.webapp_integrated,false);
assert.equal(data.sources.length,7);
assert.equal(data.nodes.length,10);
assert.equal(data.relations.length,7);
assert.equal(data.claims.length,8);
unique(data.sources.map(x=>x.id),'source IDs');
unique(data.nodes.map(x=>x.id),'node IDs');
unique(data.claims.map(x=>x.id),'claim IDs');
const nodes=new Map(data.nodes.map(x=>[x.id,x]));
const sources=new Map(data.sources.map(x=>[x.id,x]));
const exemplarNodes=data.nodes.filter(x=>x.level==='exemplar');
assert.equal(exemplarNodes.length,3);
assert.ok(exemplarNodes.every(x=>x.edition_id==='V338-N02'));
assert.ok(exemplarNodes.every(x=>x.leaf_spreads_seen===0));
assert.equal(nodes.get('V338-N04').bsb_object_id,'bsb11411960');
assert.equal(nodes.get('V338-N04').catalogue_id,'VD16 C 4734');
assert.equal(sources.get('V338-S01').holding,'Staatsbibliothek Bamberg');
assert.equal(sources.get('V338-S01').digitized_by,'Bayerische Staatsbibliothek/MDZ');
assert.equal(sources.get('V338-S01').image_pages_inspected,0);
assert.equal(sources.get('V338-S06').same_copy_as_V338_S01,false);
assert.equal(sources.get('V338-S03').year,2025);
assert.deepEqual(sources.get('V338-S03').direct_print_pages_seen,[10,11,12]);
assert.equal(sources.get('V338-S03').access,'FIRST_29_PDF_PAGES_OPEN_PREVIEW');
for (const relation of data.relations){
 assert.ok(nodes.has(relation.from)&&nodes.has(relation.to), 'relation node absent');
 assert.ok(sources.has(relation.source_id), 'relation source absent');
}
for (const claim of data.claims) {
 assert.ok(sources.has(claim.source_id),`claim source absent: ${claim.id}`);
 assert.ok(claim.assertion.length>40,`claim too short: ${claim.id}`);
 assert.ok(claim.scope.length>15,`claim scope missing: ${claim.id}`);
}
assert.deepEqual(data.variant_classification,[
 'AUTHORIAL_REVISION_BETWEEN_EDITIONS',
 'PRESS_CORRECTION_WITHIN_PRINT_RUN',
 'EXEMPLAR_STATE_DIFFERENCE',
 'CRITICAL_EDITOR_ALTERATION',
 'DIGITAL_TRANSCRIPTION_ERROR',
 'ORTHOGRAPHIC_NORMALIZATION',
 'UNRESOLVED'
]);
assert.deepEqual(data.unresolved_transcriptions.map(x=>x.id),['W01','W02','W03','W04']);
assert.ok(data.unresolved_transcriptions.every(x=>x.class==='UNRESOLVED'&&x.verified_1531_direct===false));
assert.ok(data.unresolved_transcriptions.every(x=>x.required_images.length>=2));
assert.equal(data.metrics.print_1531_direct_pages_seen,0);
assert.equal(data.metrics.cr26_ed1_direct_pages_seen,0);
assert.equal(data.metrics.unresolved_transcription_flags,4);
assert.equal(data.metrics.existing_corpus_changes,0);
assert.equal(data.metrics.publication_allowed,false);
assert.equal(Object.keys(data.editorial_gates).length,7);
console.log('V3.38 PASS: 7 sources / 10 nodes / 3 exemplar copies / 8 claims / 4 unresolved readings; HOLD');
