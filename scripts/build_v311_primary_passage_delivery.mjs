#!/usr/bin/env node
/** V3.11 deterministic source-critical export from frozen inputs; never publishes. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV311} from '../integrations/medium-atlas-v311/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const manifest=JSON.parse(read('integrations/medium-atlas-v311/manifest.json'));
const load=o=>{
 const b=read(o.path);
 if(o.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),o.sha256,'SHA256 drift: '+o.path);
 if(o.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),o.gitBlobSha1,'Git blob drift: '+o.path);
 return JSON.parse(b.toString('utf8'));
};
const inputs=manifest.inputs.map(load),audit=manifest.auditInputs.map(load),addon=load(manifest.addendumInput);
const {delivery,crosswalk}=assembleV311(inputs,...audit,addon);
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.source_verification.selected_claims.length,crosswalk.entries.length],[513,723,22,97]);
assert.deepEqual([delivery.primary_passage_addenda.length,delivery.primary_passage_claims.length,delivery.primary_passage_source_records.length],[4,12,10]);
assert.equal(delivery.editorial_audit.v311_source_critical.new_body_characters,4435);
assert.equal(delivery.publication_gate.published,false);
const i=process.argv.indexOf('--export');
if(i>=0){
 const dir=process.argv[i+1];assert.ok(dir&&!dir.startsWith('--'),'--export requires directory');
 const out=resolve(dir);mkdirSync(out,{recursive:true});
 for(const [name,obj] of [
  ['atlas_v311_source_critical_513_medium_delivery.json',delivery],
  ['atlas_v311_overview_97_quality_crosswalk.json',crosswalk],
  ['atlas_v311_source_passage_claim_cards.json',addon.claim_cards],
  ['atlas_v311_source_reading_addenda.json',addon.addenda]
 ]){
  const str=JSON.stringify(obj,null,2)+'\n';writeFileSync(join(out,name),str);
  console.log(name,createHash('sha256').update(str).digest('hex'));
 }
}
console.log('V3.11 PASS: 513 original readers, 723 original sources and 22 claims preserved; 4 addenda / 12 sections / 12 located claims / 10 tiered source records; HOLD');
