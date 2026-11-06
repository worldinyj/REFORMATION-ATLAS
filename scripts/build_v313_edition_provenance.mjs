#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV313} from '../integrations/medium-atlas-v313/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const manifest=JSON.parse(read('integrations/medium-atlas-v313/manifest.json'));
const load=i=>{
 const b=read(i.path);
 if(i.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),i.sha256,'source hash '+i.path);
 if(i.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),i.gitBlobSha1,'blob hash '+i.path);
 return JSON.parse(b.toString('utf8'));
};
const inputs=manifest.inputs.map(load),audits=manifest.auditInputs.map(load);
const edition=load(manifest.editionInput),addon=load(manifest.addendumInput),latin=load(manifest.latinInput);
const {delivery,crosswalk}=assembleV313(inputs,...audits,addon,latin,edition);
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.source_verification.selected_claims.length,crosswalk.entries.length],[513,723,22,97]);
const x=manifest.expectedEdition;
assert.deepEqual({
 studies:edition.studies.length,sections:edition.studies.reduce((a,s)=>a+s.sections.length,0),
 sources:edition.sources.length,edges:edition.relations.length,claims:edition.provenance_claims.length,
 characters:edition.metrics.body_characters,originalPagesInspected:edition.metrics.original_pages_collated,
 variantsProven:edition.metrics.verified_textual_variants},x);
assert.equal(delivery.publication_gate.published,false);
const at=process.argv.indexOf('--export');
if(at>=0){
 const dir=process.argv[at+1];assert.ok(dir&&!dir.startsWith('--'),'--export needs directory');
 mkdirSync(resolve(dir),{recursive:true});
 for(const [name,data] of [
  ['atlas_v313_513_editorial_provenance_bundle.json',delivery],
  ['atlas_v313_source_catalogue.json',edition.sources],
  ['atlas_v313_edition_relationships.json',edition.relations],
  ['atlas_v313_source_claims.json',edition.provenance_claims]
 ]) {
 const text=JSON.stringify(data,null,2)+'\n';
 writeFileSync(join(resolve(dir),name),text);
 console.log(name,createHash('sha256').update(text).digest('hex'));
 }
}
console.log('V3.13 PASS: 513 immutable manuscripts / 723 sources / 97 overview / 11 edition records / 8 relations / 9 provenance cards / 2 reading notes / HOLD');
