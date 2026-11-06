#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV317} from '../integrations/medium-atlas-v317/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const manifest=JSON.parse(read('integrations/medium-atlas-v317/manifest.json'));
const load=s=>{
 const b=read(s.path);
 if(s.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),s.sha256,'source SHA256 '+s.path);
 if(s.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),s.gitBlobSha1,'source Git blob '+s.path);
 return JSON.parse(b.toString('utf8'));
};
const originals=manifest.inputs.map(load),audits=manifest.auditInputs.map(load);
const [v311,v312,v313,v314,v315,v316,v317]=[
 manifest.addendumInput,manifest.latinInput,manifest.editionInput,manifest.authInput,
 manifest.wordingInput,manifest.ratificationInput,manifest.witnessPrintInput].map(load);
const {delivery,crosswalk}=assembleV317(originals,...audits,v311,v312,v313,v314,v315,v316,v317);
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.source_verification.selected_claims.length,crosswalk.entries.length],[513,723,22,97]);
assert.equal(delivery.ratification_event_v316.chronology.length,4);
const exp=manifest.expectedWitnessPrint;
assert.deepEqual({sources:v317.source_records.length,readings:v317.studies.length,
 sections:v317.studies.reduce((n,r)=>n+r.sections.length,0),claims:v317.claim_cards.length,
 unresolvedIssues:v317.issues.length,bodyCharacters:v317.metrics.body_characters,
 archivalPagesCollated:v317.inspection.original_print_pages_collated+v317.inspection.original_diplomatic_pages_collated,
 variantsVerified:v317.inspection.new_textual_variants_proven},exp);
assert.equal(delivery.publication_gate.published,false);
const i=process.argv.indexOf('--export');
if(i!==-1){
 const target=process.argv[i+1];assert.ok(target&&!target.startsWith('--'),'--export requires directory');
 const dir=resolve(target);mkdirSync(dir,{recursive:true});
 for(const [name,value] of [
  ['atlas_v317_513_frozen_early_print_delivery.json',delivery],
  ['atlas_v317_97_overview_crosswalk.json',crosswalk],
  ['atlas_v317_early_print_source_records.json',v317.source_records],
  ['atlas_v317_print_witness_claims.json',v317.claim_cards],
  ['atlas_v317_open_questions.json',v317.issues]
 ]){
  const s=JSON.stringify(value,null,2)+'\n';
  writeFileSync(join(dir,name),s);
  console.log(name,createHash('sha256').update(s).digest('hex'));
 }
}
console.log('V3.17 PASS: 513 frozen readers / 723 sources / V3.16 ratification retained; 3 early print studies / 10 claims / 4 open questions; original collation 0 / HOLD');
