#!/usr/bin/env node
/**
 * Scan institution-supplied IIIF structural metadata only.
 * Strictly read-only: no OCR, no image download, no persisted images.
 */
import assert from 'node:assert/strict';
const ID='bsb11411960';
const URL='https://api.digitale-sammlungen.de/iiif/presentation/v2/'+ID+'/manifest';
const r=await fetch(URL,{signal:AbortSignal.timeout(25000),headers:{Accept:'application/json'}});
assert.equal(r.status,200,'institution IIIF manifest must respond 200');
const d=await r.json();
const pages=d.sequences?.[0]?.canvases||[];
assert.equal(pages.length,288,'MDZ record has 288 canvases');
const structures=d.structures||[];
const flatten=(a,depth=0)=>a.map(x=>({depth,label:x.label||null,id:x['@id']||null,type:x['@type']||null,canvases:x.canvases?.length||0,ranges:x.ranges?.length||0,subrange:x.ranges?.slice(0,12)||[]})).slice(0,120);
console.log('V339_STRUCTURE '+JSON.stringify(flatten(structures)));
const withSeeAlso=pages.map((p,i)=>({n:i+1,label:p.label,seeAlso:p.seeAlso||null,rendering:p.rendering||null,otherContent:p.otherContent?.length||0})).filter(x=>x.seeAlso||x.rendering||x.otherContent);
console.log('V339_CANVAS_EXTRA '+JSON.stringify({total:withSeeAlso.length,first:withSeeAlso.slice(0,12)}));
console.log('V339_OBJECT_SUMMARY '+JSON.stringify({id:d['@id'],label:d.label,description:String(d.description||'').slice(0,350),metadata:d.metadata?.slice(0,12),canvas_count:pages.length,structure_count:structures.length,rendering:d.rendering||null}));
console.log('V339_STRUCTURE_PASS');
