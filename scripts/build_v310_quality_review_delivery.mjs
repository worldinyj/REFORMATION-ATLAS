#!/usr/bin/env node
/** V3.10: input-locked scoped research and 97-entry overview correction. */
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV310} from '../integrations/medium-atlas-v310/overlay.mjs';
import {createMediumAtlas} from '../integrations/medium-atlas-v310/adapter.mjs';
import {createOverviewReadingBridge} from '../integrations/medium-atlas-v310/bridge.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const manifest=JSON.parse(readFileSync(join(root,'integrations/medium-atlas-v310/manifest.json')));
const readInput=p=>readFileSync(join(root,p));
const verified=input=>{
 const bytes=readInput(input.path);
 if(input.sha256)assert.equal(createHash('sha256').update(bytes).digest('hex'),input.sha256,'source SHA256 mismatch '+input.path);
 if(input.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+bytes.length+'\0'),bytes])).digest('hex'),input.gitBlobSha1,'source Git blob drift '+input.path);
 return JSON.parse(bytes.toString('utf8'));
};
const inputs=manifest.inputs.map(verified),[v309,v310]=manifest.auditInputs.map(verified);
const {delivery,crosswalk}=assembleV310(inputs,v309,v310);
const atlas=createMediumAtlas(delivery);
const bridge=createOverviewReadingBridge(crosswalk,atlas);
assert.deepEqual(atlas.counts,manifest.expectedCounts);
assert.deepEqual(bridge.coverage,manifest.expectedCoverage);
assert.equal(delivery.readers.length,513);
assert.equal(delivery.sources.length,723);
assert.equal(delivery.source_reading_dossiers_v310.length,6);
assert.equal(crosswalk.entries.find(e=>e.overview_id==='TOP-08').mapping_status,'PARTIAL_COVERAGE');
assert.equal(atlas.canPublish,false);
assert.equal(delivery.publication_gate.published,false);
const i=process.argv.indexOf('--export');
if(i!==-1){
 const destination=process.argv[i+1];assert.ok(destination&&!destination.startsWith('--'),'--export expects directory');
 const dir=resolve(destination);mkdirSync(dir,{recursive:true});
 for(const [name,data] of [
   ['atlas_v310_quality_review_513_medium_delivery.json',delivery],
   ['atlas_v310_reviewed_97_overview_crosswalk.json',crosswalk],
   ['atlas_v310_source_dossiers.json',v310.source_reading_dossiers]
 ]){
  const text=JSON.stringify(data,null,2)+'\n';writeFileSync(join(dir,name),text);
  console.log(name,createHash('sha256').update(text).digest('hex'));
 }
}
console.log('V3.10 PASS: 513 bodies frozen / 723 source records / 19 audited limited entries / 10 scoped navigation patches / 6 source reading dossiers / overview 78 direct + 19 partial / HOLD');
