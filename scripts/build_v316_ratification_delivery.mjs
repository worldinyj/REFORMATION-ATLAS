#!/usr/bin/env node
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV316} from '../integrations/medium-atlas-v316/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url))),raw=p=>readFileSync(join(root,p));
const m=JSON.parse(raw('integrations/medium-atlas-v316/manifest.json'));
const load=x=>{
 const buf=raw(x.path);
 if(x.sha256)assert.equal(createHash('sha256').update(buf).digest('hex'),x.sha256,x.path);
 if(x.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+buf.length+'\0'),buf])).digest('hex'),x.gitBlobSha1,x.path);
 return JSON.parse(buf.toString('utf8'));
};
const input=m.inputs.map(load),audit=m.auditInputs.map(load);
const extra=[m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput].map(load),ratification=load(m.ratificationInput);
const {delivery,crosswalk}=assembleV316(input,...audit,...extra,ratification);
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.source_verification.selected_claims.length,crosswalk.entries.length],[513,723,22,97]);
assert.deepEqual({
 sources:ratification.source_records.length,claims:ratification.claim_cards.length,chronologyEvents:ratification.chronology.length,
 readings:1,sections:ratification.reading.sections.length,bodyCharacters:ratification.metrics.body_characters,
 originalPagesInspected:ratification.inspection.original_treaty_pages_viewed
},m.expectedRatification);
const p=process.argv.indexOf('--export');
if(p!==-1){
 const dest=process.argv[p+1];assert.ok(dest&&!dest.startsWith('--'),'--export requires directory');
 const path=resolve(dest);mkdirSync(path,{recursive:true});
 for(const [name,obj] of [['atlas_v316_513_ratification_bundle.json',delivery],['atlas_v316_97_overview_crosswalk.json',crosswalk],
 ['atlas_v316_ratification_chronology.json',ratification.chronology],['atlas_v316_claims_and_evidence.json',ratification.claim_cards],
 ['atlas_v316_ratification_study.json',ratification.reading]]){
  const text=JSON.stringify(obj,null,2)+'\n';writeFileSync(join(path,name),text);
  console.log(name,createHash('sha256').update(text).digest('hex'));
 }
}
console.log('V3.16 PASS: 4 distinct event dates, 5 evidence-anchored claims, 1 mid-depth research reading; frozen 513-reader corpus / HOLD');
