#!/usr/bin/env node
/**
 * REFORMATION-ATLAS V3.40: targeted reading of PRE-EXISTING institution hOCR
 * as a page-finding index, never as a substitute for an image inspection.
 * Avoids newly running OCR; fetches hOCR already published per canvas by BSB.
 * No images, no full hOCR copies, no manuscript or app changes.
 */
import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const objects = [
 {id:'bsb11411959', work:'1530-era Confessio separate imprint / VD16 C4708', pages:Array.from({length:40},(_,i)=>i+1), expectedCanvasCount:40},
 {id:'bsb11411960', work:'1531 Rhau Bamberg object / VD16 C4734', pages:[1,2,3,4,6,8,10,12,15,20,26,30,40,50,60,80,100,120,160,200,240,280,288], expectedCanvasCount:288}
];
const topics=[
 {tag:'confession',regex:/(confessio|confe[ſs]sio|confesfio)/gi},
 {tag:'apology',regex:/(apologia|apologi[aæ])/gi},
 {tag:'justification',regex:/(iustific|justific|iu[ſs]tific|iuftific|iustici|iuftici)/gi},
 {tag:'church',regex:/(ecclesi|eccle[ſs]i|ecclefi)/gi},
 {tag:'article',regex:/(articul|articvl)/gi},
 {tag:'rhau',regex:/(rhau|wit[te]{1,2}ber|wittemberg)/gi}
];
const normalize = input=>input
 .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,' ')
 .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,' ')
 .replace(/<[^>]*>/g,' ')
 .replace(/&(?:amp|nbsp|quot|lt|gt);/g,' ')
 .replace(/\s+/g,' ').trim();
async function get(url){
 const ctrl=new AbortController();const timer=setTimeout(()=>ctrl.abort(),14000);
 try {const r=await fetch(url,{signal:ctrl.signal});return {status:r.status,body:r.ok?await r.text():''};}
 finally{clearTimeout(timer);}
}
async function worker(queue, output) {
 while(queue.length) {
   const job=queue.shift();
   try{
     const url='https://api.digitale-sammlungen.de/ocr/'+job.object+'/'+job.page;
     const {status,body}=await get(url);
     const txt=normalize(body);const matches={};let excerpt='';
     for(const t of topics){
       t.regex.lastIndex=0;
       const m=t.regex.exec(txt);
       if(m){matches[t.tag]=true;
         if(!excerpt&&['justification','church','article'].includes(t.tag))
           excerpt=txt.slice(Math.max(0,m.index-65),Math.min(txt.length,m.index+200));
       }
     }
     output.push({object:job.object,page:job.page,status,content_length:body.length,opening:txt.slice(0,140),matches,excerpt,reading_level:'INSTITUTION_PREEXISTING_OCR_FINDING_AID_ONLY'});
   }catch(e){output.push({object:job.object,page:job.page,status:0,error:String(e),matches:{},reading_level:'RETRIEVAL_FAILURE'});}
 }
}
for(const o of objects){
 const r=await fetch('https://api.digitale-sammlungen.de/iiif/presentation/v2/'+o.id+'/manifest',{signal:AbortSignal.timeout(20000)});
 assert.equal(r.status,200);
 const m=await r.json();
 assert.equal(m.sequences?.[0]?.canvases?.length,o.expectedCanvasCount);
}
const jobs=objects.flatMap(o=>o.pages.map(page=>({object:o.id,page})));
const output=[],queue=jobs.slice();await Promise.all(Array.from({length:4},()=>worker(queue,output)));
output.sort((a,b)=>a.object.localeCompare(b.object)||a.page-b.page);
const report={
 version:'3.40',status:'LOCATOR_ONLY',date:'2026-11-09',
 sample_total:jobs.length,attempted:output.length,
 object_summaries:objects.map(o=>({
  object:o.id,work:o.work,expected_canvas_count:o.expectedCanvasCount,
  sample_count:o.pages.length,success_count:output.filter(x=>x.object===o.id&&x.status===200).length,
  candidates:output.filter(x=>x.object===o.id&&['justification','church','article','apology'].some(k=>x.matches[k])).map(x=>({ordinal:x.page,topics:Object.keys(x.matches)}))
 })),
 samples:output,
 physical_page_images_visually_read:0, verified_actual_1531_ca_articles:0,
 W01_W04_primary_readings_resolved:0,published:false,webapp_integrated:false
};
assert.equal(report.attempted,report.sample_total);
console.log('V340_SUMMARY '+JSON.stringify(report.object_summaries));
console.log('V340_TOP_SAMPLES '+JSON.stringify(output.filter(x=>x.status===200&&(x.matches.justification||x.matches.church)).slice(0,26)));
console.log('V340_HTTP_ERRORS '+JSON.stringify(output.filter(x=>x.status!==200).slice(0,12)));
const out=path.join('out','atlas-v340');mkdirSync(out,{recursive:true});
writeFileSync(path.join(out,'institution_existing_ocr_page_locator.json'),JSON.stringify(report,null,2)+'\n');
if(report.object_summaries.some(x=>x.success_count<Math.floor(x.sample_count*0.7)))process.exitCode=2;
else console.log('V340_LOCATOR_PASS: institution OCR is finding aid; no historical readings promoted');
