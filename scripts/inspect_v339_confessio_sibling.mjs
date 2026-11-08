#!/usr/bin/env node
/** Institution-only catalogue/manifest check for sibling historical unit.
 * NO image requests, no OCR, no page-reading claims.
 */
import assert from 'node:assert/strict';
const ID='bsb11411959';
const url='https://api.digitale-sammlungen.de/iiif/presentation/v2/'+ID+'/manifest';
const response=await fetch(url,{signal:AbortSignal.timeout(25000),headers:{Accept:'application/json'}});
assert.equal(response.status,200,'BSB sibling manifest unavailable');
const m=await response.json();
const canvases=m.sequences?.[0]?.canvases||[];
assert.ok(canvases.length>15,'unexpectedly short sibling object');
const pick=(x,i)=>({ordinal:i+1,label:x.label||null,canvas:x['@id']||null,image_service:x.images?.[0]?.resource?.service?.['@id']||null,ocr_available:Boolean(x.seeAlso)});
console.log('ATLAS_CONFESSIO_SIBLING '+JSON.stringify({
 id:ID,manifest_label:m.label||null,manifest_metadata:m.metadata||[],
 canvas_count:canvases.length,first:canvases.slice(0,4).map(pick),
 last:canvases.slice(-2).map((x,i)=>pick(x,canvases.length-2+i)),
 existing_ocr_link_count:canvases.filter(x=>x.seeAlso).length,
 provenance_status:'CATALOGUE_AND_CANVAS_ONLY_NOT_TEXT_VERIFIED',
 assertion:'Object differs from bsb11411960; require historical date and actual article images before promotion'
}));
console.log('V339_SIBLING_METADATA_PASS');
