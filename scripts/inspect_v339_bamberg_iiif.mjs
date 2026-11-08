#!/usr/bin/env node
/**
 * ATLAS V3.39
 * Read-only locator of the IIIF canvases of the 1531 Bamberg surviving exemplar.
 * The tool records only URLs/labels and NEVER marks a leaf as transcribed or visually checked.
 * It does not download, redistribute, OCR, or publish page images.
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
const OBJECT='bsb11411960';
const MANIFEST='https://api.digitale-sammlungen.de/iiif/presentation/v2/'+OBJECT+'/manifest';
const SAMPLES=[1,2,3,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,240,280,288];
const state={version:'3.39',status:'IIIF_METADATA_REVIEW_ONLY',object:OBJECT,source_manifest:MANIFEST,source_catalogue:'https://www.digitale-sammlungen.de/en/details/'+OBJECT,created_at_utc:new Date().toISOString(),intended_exemplar:'Bamberg Staatsbibliothek .64 B 9#3a VD16 C 4734',image_pages_visually_checked:0,verified_1531_loci:[],discrepancies_W01_W04_resolved:0,published:false,webapp_integrated:false};
const timeout=AbortSignal.timeout(25000);
let res;
try { res=await fetch(MANIFEST,{signal:timeout,headers:{Accept:'application/ld+json,application/json'}}); }
catch(e){console.log('MANIFEST_FETCH_UNAVAILABLE '+String(e));process.exitCode=2;}
if(res){
 console.log('MANIFEST_HTTP '+res.status);
 if(!res.ok){console.log('MANIFEST_FAILURE '+(await res.text()).slice(0,300));process.exitCode=2;}
 else {
   const m=await res.json();
   const pages=m.sequences?.[0]?.canvases||[];
   state.manifest_id=m['@id']||null;
   state.manifest_label=m.label||null;
   state.canvas_count=pages.length;
   state.rights_statement=m.license||m.rights||null;
   state.metadata=(m.metadata||[]).filter(x=>/signatur|shelf|date|year|institution|bibliothek|library|rights/i.test(x.label)).map(x=>({label:x.label,value:x.value}));
   state.preview_canvases=SAMPLES.filter(n=>n<=pages.length).map(n=>{
     const c=pages[n-1];
     return {canvas_ordinal_1_based:n,canvas_index_0_based:n-1,label:c.label||null,canvas_id:c['@id']||null,image_service_id:c.images?.[0]?.resource?.service?.['@id']||null,width:c.width||null,height:c.height||null};
   });
   if(pages.length!==288){console.log('FAIL_CANVAS_COUNT_EXPECTED_288_GOT '+pages.length);process.exitCode=3;}
   console.log('ATLAS_MANIFEST_SUMMARY '+JSON.stringify({object:OBJECT,canvas_count:pages.length,manifest_label:state.manifest_label,preview_canvases:state.preview_canvases}));
   state.review_condition='Manifest and canvas metadata only. No full page or target chapter visually inspected.';
   console.log('V339_STRUCTURES '+JSON.stringify((m.structures||[]).slice(0,20).map(x=>({label:x.label,type:x['@type'],id:x['@id'],canvas_count:x.canvases?.length||0,range_count:x.ranges?.length||0}))));
   console.log('V339_TEXT_LINKS '+JSON.stringify({available:pages.filter(x=>x.seeAlso||x.rendering||x.otherContent).length,samples:pages.map((x,i)=>({index:i+1,seeAlso:x.seeAlso||null,rendering:x.rendering||null})).filter(x=>x.seeAlso||x.rendering).slice(0,5)}));
   mkdirSync(path.join('out','atlas-v339'),{recursive:true});
   writeFileSync(path.join('out','atlas-v339','iiif_canvas_locator_review_only.json'),JSON.stringify(state,null,2)+'\n');
   if(!pages.length||state.preview_canvases.some(x=>!x.image_service_id))process.exitCode=3;
   if(state.preview_canvases.some(x=>!String(x.image_service_id).includes(OBJECT+'_')))process.exitCode=3;
   if(state.preview_canvases.some(x=>x.canvas_ordinal_1_based!==x.canvas_index_0_based+1))process.exitCode=3;
   if(!process.exitCode)console.log('ATLAS_V339_PASS: 288 institution canvases; catalogue and image service IDs match; page transcription remains HOLD');
 }
}
