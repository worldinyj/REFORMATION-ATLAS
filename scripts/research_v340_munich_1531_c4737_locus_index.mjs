#!/usr/bin/env node
/**
 * V3.40.1 Find structural leaf candidates for the newly recovered Munich BSB 1531 copy.
 * Institution's pre-existing OCR is read for navigation, not re-OCRed, not treated as an eyewitness reading.
 * No images, no full texts, no publication or app changes.
 */
import assert from 'node:assert/strict';
import {mkdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
const OBJECT='bsb00103368';
const manifest='https://api.digitale-sammlungen.de/iiif/presentation/v2/'+OBJECT+'/manifest';
const get=async(url)=>{
 const r=await fetch(url,{signal:AbortSignal.timeout(25000)});
 return {status:r.status,body:r.ok?await r.text():''};
};
const M=await get(manifest);
assert.equal(M.status,200,'BSB Munich manifest must be online');
const meta=JSON.parse(M.body);
const pages=meta.sequences?.[0]?.canvases||[];
assert.ok(pages.length>=25&&pages.length<=2000,'Unexpected number of pages');
const labels=(meta.metadata||[]).map(x=>({label:typeof x.label==='string'?x.label:JSON.stringify(x.label),value:typeof x.value==='string'?x.value:JSON.stringify(x.value)}));
const sampleIds=[...Array.from({length:24},(_,i)=>i+1),30,35,40,50,60,80,100,120,160,200,250,300].filter(n=>n<=pages.length);
const normalize=x=>x.replace(/<[^>]*>/g,' ').replace(/&(?:nbsp|amp|lt|gt);/g,' ').replace(/\s+/g,' ').trim();
const queue=[...sampleIds],samples=[];
const worker=async()=>{while(queue.length){
 const i=queue.shift();
 try{
  const r=await get('https://api.digitale-sammlungen.de/ocr/'+OBJECT+'/'+i);
  const t=normalize(r.body);
  const found={confession:/(confessio|confeſsio|confefſio|confef[sſ]io)/i.test(t),
   apology:/(apologia|apologiam|apologi[aæ])/i.test(t),
   article:/(artic[vul]{2,}|articuli)/i.test(t),
   justification:/(iu[ſsft]tific|justific|iuſtici)/i.test(t),
   church:/(eccle[ſsfi]{1,3}i|ecclesi)/i.test(t)};
  samples.push({ordinal:i,canvas_id:pages[i-1]['@id'],image_service:pages[i-1].images?.[0]?.resource?.service?.['@id'],
    status:r.status,ocr_length:r.body.length,start:t.slice(0,260),topic_flags:found});
 }catch(e){samples.push({ordinal:i,status:0,error:String(e),topic_flags:{}});}
}};
await Promise.all(Array.from({length:4},worker));
samples.sort((a,b)=>a.ordinal-b.ordinal);
const report={version:'3.40.1',status:'METADATA_OCR_NAVIGATION_ONLY',object:OBJECT,manifest,
 title:meta.label,metadata:labels.slice(0,25),canvas_count:pages.length,
 sampling:{requested:sampleIds.length,successful:samples.filter(x=>x.status===200).length,results:samples},
 verified_print_1531_image_pages:0,verified_1531_latin_confessio_articles:0,
 W01_W04_resolved:0,published:false,webapp_integrated:false};
const out=path.join('out','atlas-v340');mkdirSync(out,{recursive:true});
writeFileSync(path.join(out,'munich_1531_c4737_existing_ocr_locus_index.json'),JSON.stringify(report,null,2)+'\n');
console.log('V340_MUNICH_C4737_IDENTITY '+JSON.stringify({object:OBJECT,canvas_count:pages.length,source:meta.label,metadata:labels.filter(x=>/Call number|Signatur|Date|Zeit|Date|VD|Erschienen|Published|Holding institution|Besitzende/i.test(x.label)).slice(0,12)}));
console.log('V340_MUNICH_C4737_SAMPLES '+JSON.stringify(samples.map(x=>({ordinal:x.ordinal,start:x.start,status:x.status,topic_flags:x.topic_flags}))));
if(samples.filter(x=>x.status===200).length<Math.ceil(sampleIds.length*.7))process.exitCode=2;
else console.log('V340_MUNICH_LOCATOR_PASS: source identified; actual print reading still HOLD');

// Focused excerpts around four previously unresolved transcription strings.
// These are FIRST-PASS excerpts of institution-provided OCR, not print-letter readings.
const targets=[
 {code:'W01',article:'IV',rx:/(gratis.{0,30}(?:iu[ſsft]tific\w*|justific\w*))/gi},
 {code:'W02',article:'VII',rx:/(con[ſs]entier[e]?|consentiere|con[ſs]entire|consentire)/gi},
 {code:'W03',article:'VIII',rx:/(malii|mali\b|ma[ſs]i\b)/gi},
 {code:'W04',article:'VIII',rx:/(sentibant|sentiebant|ſentiebant|ſentibant|fentiebant|fentibant)/gi}
];
const focused=[];
for (const n of [14,15,16,17]){
 const resp=await get('https://api.digitale-sammlungen.de/ocr/'+OBJECT+'/'+n);
 const txt=normalize(resp.body);const matches=[];
 for(const t of targets){
   t.rx.lastIndex=0;const m=t.rx.exec(txt);
   if(m)matches.push({id:t.code,locus:m[0],surrounding:txt.slice(Math.max(0,m.index-135),Math.min(txt.length,m.index+170))});
 }
 focused.push({object:OBJECT,canvas_ordinal:n,status:resp.status,opening:txt.slice(0,440),matches,excerpt_type:'INSTITUTION_EXISTING_OCR_ONLY'});
}
console.log('V340_MUNICH_TARGETED_W01_W04 '+JSON.stringify(focused));
