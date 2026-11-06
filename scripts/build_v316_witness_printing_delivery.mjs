#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV316} from '../integrations/medium-atlas-v316/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const m=JSON.parse(read('integrations/medium-atlas-v316/manifest.json'));
const load=i=>{
 const b=read(i.path);
 if(i.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),i.sha256,i.path);
 if(i.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),i.gitBlobSha1,i.path);
 return JSON.parse(b.toString('utf8'));
};
const base=m.inputs.map(load),audits=m.auditInputs.map(load);
const [a,b,c,d,e,f]=[m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput,m.witnessInput].map(load);
const {delivery,crosswalk}=assembleV316(base,...audits,a,b,c,d,e,f);
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.source_verification.selected_claims.length,crosswalk.entries.length],[513,723,22,97]);
assert.deepEqual({sources:f.source_records.length,studies:f.studies.length,
 sections:f.studies.flatMap(x=>x.sections).length,claims:f.claim_cards.length,
 unresolvedIssues:f.issues.length,characters:f.metrics.body_characters,
 originalPagesRead:f.inspection.original_print_pages_collated+f.inspection.original_diplomatic_pages_collated,
 variantsProven:f.inspection.new_textual_variants_proven},m.expectedWitness);
assert.equal(delivery.publication_gate.published,false);
const p=process.argv.indexOf('--export');
if(p>=0){
 const dir=process.argv[p+1];assert.ok(dir&&!dir.startsWith('--'),'missing export directory');
 mkdirSync(resolve(dir),{recursive:true});
 for(const [name,obj] of [
  ['atlas_v316_513_source_scoped_delivery.json',delivery],
  ['atlas_v316_97_overview_crosswalk.json',crosswalk],
  ['atlas_v316_seven_printing_and_archive_sources.json',f.source_records],
  ['atlas_v316_ten_claim_provenance_cards.json',f.claim_cards],
  ['atlas_v316_four_open_verification_issues.json',f.issues]
 ]){
  const text=JSON.stringify(obj,null,2)+'\n';
  writeFileSync(join(resolve(dir),name),text);
  console.log(name,createHash('sha256').update(text).digest('hex'));
 }
}
console.log('V3.16 PASS: 513 frozen manuscripts, 723 sources, 97 overview rows and V3.11–15 supplements intact; 3 studies, 9 sections, 10 evidence cards, 4 unresolved; publication HOLD');
