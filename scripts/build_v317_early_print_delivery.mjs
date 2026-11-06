#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV317} from '../integrations/medium-atlas-v317/overlay.mjs';

const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const raw=p=>readFileSync(join(root,p));
const manifest=JSON.parse(raw('integrations/medium-atlas-v317/manifest.json'));
const load=x=>{
 const b=raw(x.path);
 if(x.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),x.sha256,x.path);
 if(x.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),x.gitBlobSha1,x.path);
 return JSON.parse(b.toString('utf8'));
};
const base=manifest.inputs.map(load),audits=manifest.auditInputs.map(load);
const [v311,v312,v313,v314,v315,rat316,print317]=[
 manifest.addendumInput,manifest.latinInput,manifest.editionInput,manifest.authInput,
 manifest.wordingInput,manifest.ratificationInput,manifest.printingWitnessInput
].map(load);
const {delivery,crosswalk}=assembleV317(base,...audits,v311,v312,v313,v314,v315,rat316,print317);
assert.deepEqual([delivery.readers.length,delivery.sources.length,
 delivery.source_verification.selected_claims.length,crosswalk.entries.length],[513,723,22,97]);
const expected=manifest.expectedPrintingWitness, actual={
 sources:print317.source_records.length,studies:print317.studies.length,
 sections:print317.studies.reduce((n,s)=>n+s.sections.length,0),
 claims:print317.claim_cards.length,unresolvedIssues:print317.issues.length,
 characters:print317.metrics.body_characters,
 originalPagesRead:print317.inspection.original_print_pages_collated+
  print317.inspection.original_diplomatic_pages_collated,
 variantsProven:print317.inspection.new_textual_variants_proven
};
assert.deepEqual(actual,expected);
assert.equal(delivery.publication_gate.published,false);
const idx=process.argv.indexOf('--export');
if(idx!==-1){
 const destination=process.argv[idx+1];
 assert.ok(destination&&!destination.startsWith('--'),'--export needs destination');
 mkdirSync(resolve(destination),{recursive:true});
 for(const [name,item] of [
  ['atlas_v317_513_unchanged_editorial_delivery.json',delivery],
  ['atlas_v317_97_overview_crosswalk.json',crosswalk],
  ['atlas_v317_seven_printing_source_records.json',print317.source_records],
  ['atlas_v317_three_critical_medium_studies.json',print317.studies],
  ['atlas_v317_ten_claim_cards.json',print317.claim_cards],
  ['atlas_v317_four_open_bibliography_questions.json',print317.issues]
 ]){
  const s=JSON.stringify(item,null,2)+'\n';
  writeFileSync(join(resolve(destination),name),s);
  console.log(name,createHash('sha256').update(s).digest('hex'));
 }
}
console.log('V3.17 PASS: 513 readers, 723 base sources, 97 overview, frozen V3.16 ratification; 3 studies / 9 sections / 7 source records / 10 claims / 4 unresolved issues; HOLD');
