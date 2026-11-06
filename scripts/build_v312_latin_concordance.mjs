#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV312} from '../integrations/medium-atlas-v312/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const manifest=JSON.parse(read('integrations/medium-atlas-v312/manifest.json'));
const load=i=>{
 const data=read(i.path);
 if(i.sha256)assert.equal(createHash('sha256').update(data).digest('hex'),i.sha256,i.path);
 if(i.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+data.length+'\0'),data])).digest('hex'),i.gitBlobSha1,i.path);
 return JSON.parse(data.toString('utf8'));
};
const base=manifest.inputs.map(load),audits=manifest.auditInputs.map(load);
const v311=load(manifest.addendumInput),latin=load(manifest.latinInput);
const {delivery,crosswalk}=assembleV312(base,...audits,v311,latin);
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.primary_passage_addenda.length,delivery.primary_passage_claims.length,crosswalk.entries.length],[513,723,4,12,97]);
assert.deepEqual({notes:latin.medium_readings.length,sections:latin.medium_readings.reduce((n,r)=>n+r.sections.length,0),
 pairs:latin.concordance_cards.length,sources:latin.source_records.length,characters:latin.metrics.new_body_characters,
 archivalCollations:latin.metrics.original_archival_witness_collations},manifest.expectedLatin);
const i=process.argv.indexOf('--export');
if(i!==-1){
 const dir=process.argv[i+1];assert.ok(dir&&!dir.startsWith('--'),'--export requires target directory');
 mkdirSync(resolve(dir),{recursive:true});
 for(const [name,obj] of [['atlas_v312_latin_scoped_513_medium_delivery.json',delivery],
 ['atlas_v312_latin_compared_claims.json',latin.concordance_cards],
 ['atlas_v312_latin_reading_notes.json',latin.medium_readings]]){
  const s=JSON.stringify(obj,null,2)+'\n';writeFileSync(join(resolve(dir),name),s);
  console.log(name,createHash('sha256').update(s).digest('hex'));
 }
}
console.log('V3.12 PASS: two Latin source-critical notes, six sections, four paired claims, five scoped records; 513 prior readers and 723 sources preserved; HOLD');
