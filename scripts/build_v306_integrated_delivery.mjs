#!/usr/bin/env node
/** V3.06 deterministic exporter; does not mutate existing research files. */
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {assembleMediumDelivery} from '../integrations/medium-atlas-v306/assemble.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const manifest=JSON.parse(read('integrations/medium-atlas-v306/manifest.json'));
const inputs=manifest.inputs.map(item=>{
 const data=read(item.path);
 if(item.sha256)assert.equal(createHash('sha256').update(data).digest('hex'),item.sha256,'SHA256 drift '+item.path);
 if(item.gitBlobSha1){const payload=Buffer.concat([Buffer.from('blob '+data.length+'\0'),data]);assert.equal(createHash('sha1').update(payload).digest('hex'),item.gitBlobSha1,'blob identity drift '+item.path);}
 return JSON.parse(data.toString('utf8'));
});
const {delivery,crosswalk}=assembleMediumDelivery(...inputs);
assert.deepEqual([delivery.readers.length,delivery.metrics.sections,delivery.sources.length,delivery.reading_paths.length],[495,1485,697,27]);
assert.deepEqual(crosswalk.entries.reduce((a,r)=>(a[r.mapping_status]=(a[r.mapping_status]||0)+1,a),{}),{DIRECT_TOPIC:64,PARTIAL_COVERAGE:14,BACKGROUND_ONLY:1,NO_MATCH:18});
assert.equal(delivery.metrics.body_characters,inputs[0].metrics.body_characters+9897);
const i=process.argv.indexOf('--export');
if(i>=0){
 const dir=process.argv[i+1];assert.ok(dir&&!dir.startsWith('--'),'specify --export directory');mkdirSync(dir,{recursive:true});
 for(const [name,obj] of [['atlas_v306_integrated_495_medium_delivery.json',delivery],['atlas_v306_overview_medium_reading_crosswalk.json',crosswalk]]){
 const raw=JSON.stringify(obj,null,2)+'\n';writeFileSync(join(dir,name),raw);console.log(name,createHash('sha256').update(raw).digest('hex'));}
}
console.log('V3.06 CHECK: 495 readers / 1485 sections / 697 source records / 27 paths / 97 overview entries; HOLD');
