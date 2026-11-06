#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV315} from '../integrations/medium-atlas-v315/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const m=JSON.parse(read('integrations/medium-atlas-v315/manifest.json'));
const load=x=>{
 const b=read(x.path);
 if(x.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),x.sha256,x.path);
 if(x.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),x.gitBlobSha1,x.path);
 return JSON.parse(b.toString('utf8'));
};
const originals=m.inputs.map(load),audits=m.auditInputs.map(load);
const [a,b,c,d,e]=[m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput].map(load);
const {delivery,crosswalk}=assembleV315(originals,...audits,a,b,c,d,e);
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.source_verification.selected_claims.length,crosswalk.entries.length],[513,723,22,97]);
assert.deepEqual({readings:e.reading_notes.length,sections:e.reading_notes.reduce((n,x)=>n+x.sections.length,0),
 sources:e.source_records.length,claims:e.claim_cards.length,
 latinFragments:e.claim_cards.filter(x=>x.latin_fragment!==null).length,characters:e.metrics.body_characters,
 originalPageCollations:e.inspection.original_museum_pages+e.inspection.original_treaty_pages},m.expectedWording);
const i=process.argv.indexOf('--export');
if(i!==-1){
 const dest=process.argv[i+1];assert.ok(dest&&!dest.startsWith('--'),'--export requires directory');
 const dir=resolve(dest);mkdirSync(dir,{recursive:true});
 for(const [name,value] of [
  ['atlas_v315_513_frozen_critical_wording_delivery.json',delivery],
  ['atlas_v315_97_overview_crosswalk.json',crosswalk],
  ['atlas_v315_eight_claim_anchors.json',e.claim_cards],
  ['atlas_v315_two_medium_readings.json',e.reading_notes]
 ]) {
  const output=JSON.stringify(value,null,2)+'\n';
  writeFileSync(join(dir,name),output);
  console.log(name,createHash('sha256').update(output).digest('hex'));
 }
}
console.log('V3.15 PASS: original 513 readers / 723 sources unchanged; 2 microreadings, 6 sections, 8 claims, 4 museum-transcribed Latin fragments; HOLD');
