#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV314} from '../integrations/medium-atlas-v314/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const manifest=JSON.parse(read('integrations/medium-atlas-v314/manifest.json'));
const loaded=i=>{
 const b=read(i.path);
 if(i.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),i.sha256,i.path);
 if(i.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),i.gitBlobSha1,i.path);
 return JSON.parse(b.toString('utf8'));
};
const params=[...manifest.inputs.map(loaded),...manifest.auditInputs.map(loaded),loaded(manifest.addendumInput),
 loaded(manifest.latinInput),loaded(manifest.editionInput),loaded(manifest.authInput)];
const {delivery,crosswalk}=assembleV314(params.slice(0,4),...params.slice(4));
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.source_verification.selected_claims.length,
 crosswalk.entries.length],[513,723,22,97]);
assert.deepEqual({sources:delivery.source_attestation_v314.sources.length,
 claims:delivery.source_attestation_v314.claims.length,
 studies:delivery.source_attestation_v314.studies.length,
 sections:delivery.source_attestation_v314.studies.reduce((n,s)=>n+s.sections.length,0),
 characters:delivery.editorial_audit.v314_source_attestation.new_body_characters,
 fullArchivalCollations:delivery.editorial_audit.v314_source_attestation.physical_original_pages_read},manifest.expectedAuth);
assert.equal(delivery.publication_gate.published,false);
const i=process.argv.indexOf('--export');
if(i>=0){
 const p=process.argv[i+1];assert.ok(p&&!p.startsWith('--'),'--export destination required');
 const dir=resolve(p);mkdirSync(dir,{recursive:true});
 for(const [name,v] of [
  ['atlas_v314_513_preserved_editorial_bundle.json',delivery],
  ['atlas_v314_museum_archive_source_notes.json',delivery.source_attestation_v314.sources],
  ['atlas_v314_authentication_claims.json',delivery.source_attestation_v314.claims],
  ['atlas_v314_source_critical_readings.json',delivery.source_attestation_v314.studies]
 ]){
  const s=JSON.stringify(v,null,2)+'\n';writeFileSync(join(dir,name),s);
  console.log(name,createHash('sha256').update(s).digest('hex'));
 }
}
console.log('V3.14 PASS: six scoped institutional/archival sources, six protected claims, two readings, 513 frozen originals / HOLD');
