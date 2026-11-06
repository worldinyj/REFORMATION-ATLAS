#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV309} from '../integrations/medium-atlas-v309/overlay.mjs';
import {createMediumAtlas} from '../integrations/medium-atlas-v308/adapter.mjs';
import {createOverviewReadingBridge} from '../integrations/medium-atlas-v308/bridge.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const manifest=JSON.parse(read('integrations/medium-atlas-v308/manifest.json'));
const inputs=manifest.inputs.map(o=>{
 const b=read(o.path);
 if(o.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),o.sha256,'source SHA256 '+o.path);
 if(o.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),o.gitBlobSha1,'source blob '+o.path);
 return JSON.parse(b.toString('utf8'));
});
const audit=JSON.parse(read('data/contracts/atlas_v309_source_evidence_audit.json'));
const {delivery,crosswalk}=assembleV309(inputs,audit);
const atlas=createMediumAtlas(delivery),bridge=createOverviewReadingBridge(crosswalk,atlas);
assert.deepEqual(atlas.counts,manifest.expectedCounts);
assert.deepEqual(bridge.coverage,{total:97,direct:78,partial:18,background:1,missing:0});
const source=atlas.getSource('V307-S08');
assert.equal(source.url,'https://www.bskorea.or.kr/bbs/content.php?co_id=subpage2_3_3_1_1');
assert.equal(source.access.status,'NOT_CHECKED');
const idx=process.argv.indexOf('--export');
if(idx>=0){
 const dir=process.argv[idx+1];assert.ok(dir&&!dir.startsWith('--'),'--export directory required');
 mkdirSync(resolve(dir),{recursive:true});
 for(const [filename,data] of [['atlas_v309_source_audited_513_medium_delivery.json',delivery],['atlas_v309_source_audited_overview_crosswalk.json',crosswalk]]){
  const content=JSON.stringify(data,null,2)+'\n';writeFileSync(join(resolve(dir),filename),content);
  console.log(filename,createHash('sha256').update(content).digest('hex'));
 }
}
console.log('V3.09 PASS: 513 bodies preserved / 1 verified institutional link correction / 723 source records / HOLD');
