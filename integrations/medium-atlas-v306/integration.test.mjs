import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleMediumDelivery,pathSpecs} from './assemble.mjs';
const root=new URL('../../',import.meta.url);
const raw=p=>readFileSync(new URL(p,root));
const manifest=JSON.parse(raw('integrations/medium-atlas-v306/manifest.json'));
const [base,newData,cross]=manifest.inputs.map(i=>JSON.parse(raw(i.path)));
const {delivery:b,crosswalk:x}=assembleMediumDelivery(base,newData,cross);
test('pinned input identity',()=>{
 for(const input of manifest.inputs){const bytes=raw(input.path);
 if(input.sha256)assert.equal(createHash('sha256').update(bytes).digest('hex'),input.sha256);
 if(input.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+bytes.length+'\0'),bytes])).digest('hex'),input.gitBlobSha1);
 }
});
test('old content and source evidence are entirely preserved',()=>{
 assert.deepEqual(b.readers.slice(0,475),base.readers);
 assert.deepEqual(b.sources.slice(0,675),base.sources);
 assert.deepEqual(b.source_verification,base.source_verification);
 assert.equal(b.publication_gate.published,false);
});
test('new 20 original chapters and 22 source scopes are reproduced',()=>{
 for(const c of newData.chapters){const r=b.readers.find(r=>r.id===c.id);assert.deepEqual(r.sections,c.sections);assert.equal(r.reading_question,c.reading_question);
  assert.deepEqual(r.sources,c.sources.map(s=>'V305-'+s));}
 for(const s of b.sources.slice(675)){assert.equal(s.original_image_read,false);assert.equal(s.checked_on,'2026-11-06');assert.ok(s.inspection_note);}
});
test('three editorial paths cover all 20 additions exactly once',()=>{
 assert.equal(pathSpecs.length,3);assert.deepEqual(b.reading_paths.slice(0,24),base.reading_paths);
 const ids=b.reading_paths.slice(24).flatMap(p=>p.reader_ids);
 assert.equal(ids.length,20);assert.equal(new Set(ids).size,20);assert.deepEqual(new Set(ids),new Set(newData.chapters.map(c=>c.id)));
});
test('97 overview entries, 11 scoped upgrades, 18 remaining gaps',()=>{
 assert.equal(x.entries.length,97);
 for(const u of newData.overview_link_updates){const row=x.entries.find(r=>r.overview_id===u.overview_id);assert.equal(row.mapping_status,u.new_status);assert.equal(row.reader_links[0].reader_id,u.reader_id);}
 assert.deepEqual([x.metrics.direct_topic,x.metrics.partial_coverage,x.metrics.background_only,x.metrics.no_match],[64,14,1,18]);
 assert.equal(x.entries.find(r=>r.overview_id==='OV-E-027').mapping_status,'PARTIAL_COVERAGE');
 assert.equal(x.entries.find(r=>r.overview_id==='OV-D-017').mapping_status,'PARTIAL_COVERAGE');
 assert.deepEqual(x.entries.map(r=>r.overview_record),cross.entries.map(r=>r.overview_record));
});
test('identity collision and revoked hold are rejected',()=>{
 const z=structuredClone(newData);z.chapters[0].id=base.readers[0].id;assert.throws(()=>assembleMediumDelivery(base,z,cross));
 const q=structuredClone(base);q.publication_gate.published=true;assert.throws(()=>assembleMediumDelivery(q,newData,cross),/HOLD/);
});
