#!/usr/bin/env node
/** Deterministically export the V3.08 513-reader delivery and 97-item crosswalk. */
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {assembleV308} from '../integrations/medium-atlas-v308/assemble.mjs';
import {createMediumAtlas} from '../integrations/medium-atlas-v308/adapter.mjs';
import {createOverviewReadingBridge} from '../integrations/medium-atlas-v308/bridge.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const load=p=>readFileSync(join(root,p));
const manifest=JSON.parse(load('integrations/medium-atlas-v308/manifest.json'));
const inputs=manifest.inputs.map(input=>{
  const raw=load(input.path);
  if(input.sha256)assert.equal(createHash('sha256').update(raw).digest('hex'),input.sha256,'SHA256 mismatch: '+input.path);
  if(input.gitBlobSha1){const bytes=Buffer.concat([Buffer.from('blob '+raw.length+'\0'),raw]);
    assert.equal(createHash('sha1').update(bytes).digest('hex'),input.gitBlobSha1,'Git blob mismatch: '+input.path);}
  return JSON.parse(raw.toString('utf8'));
});
const {delivery,crosswalk}=assembleV308(...inputs);
const reader=createMediumAtlas(delivery),bridge=createOverviewReadingBridge(crosswalk,reader);
assert.deepEqual(reader.counts,manifest.expectedCounts);
assert.deepEqual(bridge.coverage,{total:97,direct:78,partial:18,background:1,missing:0});
assert.equal(delivery.metrics.body_characters,inputs[0].metrics.body_characters+inputs[1].metrics.new_body_characters+inputs[3].metrics.new_body_characters);
assert.equal(delivery.publication_gate.published,false);
const outputIndex=process.argv.indexOf('--export');
if(outputIndex!==-1){
  const arg=process.argv[outputIndex+1];assert.ok(arg&&!arg.startsWith('--'),'--export needs a target directory');
  const dir=resolve(arg);mkdirSync(dir,{recursive:true});
  for(const [filename,data] of [['atlas_v308_integrated_513_medium_delivery.json',delivery],['atlas_v308_overview_medium_reading_crosswalk.json',crosswalk]]){
    const text=JSON.stringify(data,null,2)+'\n';writeFileSync(join(dir,filename),text);
    console.log(filename,createHash('sha256').update(text).digest('hex'));
  }
}
console.log('V3.08 PASS: 513 readers / 1539 sections / 723 source records / 31 paths / overview 78 direct + 18 partial + 1 background / HOLD');
