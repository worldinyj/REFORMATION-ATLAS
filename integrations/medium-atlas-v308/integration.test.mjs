import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleMediumDelivery as assembleV306} from '../medium-atlas-v306/assemble.mjs';
import {assembleV308,readingPathSpecs} from './assemble.mjs';
import {createMediumAtlas} from './adapter.mjs';
import {createOverviewReadingBridge} from './bridge.mjs';
const root=new URL('../../',import.meta.url);
const bytes=p=>readFileSync(new URL(p,root));
const manifest=JSON.parse(bytes('integrations/medium-atlas-v308/manifest.json'));
const inputs=manifest.inputs.map(i=>JSON.parse(bytes(i.path)));
const [old475,v305,cross304,v307]=inputs;
const previous=assembleV306(old475,v305,cross304);
const {delivery:b,crosswalk:x}=assembleV308(...inputs);
const atlas=createMediumAtlas(b),bridge=createOverviewReadingBridge(x,atlas);
test('all four pinned input identities and expected consumer counts',()=>{
  assert.equal(manifest.inputs.length,4);
  for(const input of manifest.inputs){
    const raw=bytes(input.path);
    if(input.sha256)assert.equal(createHash('sha256').update(raw).digest('hex'),input.sha256,input.path);
    if(input.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+raw.length+'\0'),raw])).digest('hex'),input.gitBlobSha1,input.path);
  }
  assert.deepEqual(atlas.counts,manifest.expectedCounts);
  assert.equal(atlas.canPublish,false);
});
test('previous 495 body and 697 source records are unchanged',()=>{
  assert.deepEqual(b.readers.slice(0,495),previous.delivery.readers);
  assert.deepEqual(b.sources.slice(0,697),previous.delivery.sources);
  assert.deepEqual(b.source_verification,previous.delivery.source_verification);
  assert.deepEqual(b.reader_source_cards,previous.delivery.reader_source_cards);
  assert.deepEqual(b.reading_paths.slice(0,27),previous.delivery.reading_paths);
});
test('V3.07 keeps all 18 sections/questions and original source check levels',()=>{
  assert.equal(v307.chapters.length,18);
  for(const c of v307.chapters){
    const article=atlas.getReader(c.id);
    assert.deepEqual(article.sections,c.sections);
    assert.equal(article.readingQuestion,c.reading_question);
    assert.equal(article.editorialStatus,'편집 초안');
    assert.equal(article.expertApproved,false);
    assert.deepEqual(article.sources.map(s=>s.id),c.sources.map(id=>'V307-'+id));
    assert.ok(article.sources.every(s=>s.access.status==='NOT_CHECKED'&&s.access.checkedOn===null));
    assert.ok(article.sources.every(s=>s.priorInspection?.recheckedThisVersion===false));
    assert.ok(article.sources.every(s=>s.priorInspection?.checkedOn==='2026-11-06'));
  }
  assert.equal(b.sources.slice(697).length,26);
  assert.ok(b.sources.slice(697).every(s=>s.inspection_level==='PUBLIC_LANDING_PAGE_OR_SEARCH_EXCERPT'&&!s.original_image_read));
});
test('97 original overview records remain identical; 18 targets move from NO_MATCH',()=>{
  assert.deepEqual(x.entries.map(e=>e.overview_record),cross304.entries.map(e=>e.overview_record));
  assert.deepEqual(bridge.coverage,{total:97,direct:78,partial:18,background:1,missing:0});
  assert.equal(bridge.listOverview().length,97);
  assert.equal(bridge.listOverview({status:'NO_MATCH'}).length,0);
  for(const u of v307.overview_link_updates){
    const result=bridge.resolve(u.overview_id);
    assert.equal(result.status,u.new_status);
    assert.equal(result.scope,u.scope);
    assert.equal(result.readers[0].id,u.reader_id);
    assert.equal(result.readers[0].role,'PRIMARY');
  }
  for(const id of ['OV-E-001','OV-D-019','TOP-09','TOP-10']){
    assert.equal(bridge.resolve(id).status,'PARTIAL_COVERAGE',id);
  }
  assert.equal(bridge.resolve('OV-E-027').status,'PARTIAL_COVERAGE');
  assert.equal(bridge.resolve('OV-D-017').status,'PARTIAL_COVERAGE');
});
test('four new paths cover each V3.07 reader exactly once',()=>{
  assert.equal(readingPathSpecs.length,4);
  assert.equal(atlas.listReadingPaths().length,31);
  const ids=b.reading_paths.slice(27).flatMap(p=>p.reader_ids);
  assert.equal(ids.length,18);
  assert.equal(new Set(ids).size,18);
  assert.deepEqual(new Set(ids),new Set(v307.chapters.map(c=>c.id)));
  assert.equal(b.reading_paths[27].reader_ids.length,3);
  assert.equal(b.reading_paths[28].reader_ids.length,10);
  assert.equal(b.reading_paths[29].reader_ids.length,3);
  assert.equal(b.reading_paths[30].reader_ids.length,2);
});
test('search, source guide and historical identity distinctions survive',()=>{
  assert.ok(atlas.search('이승훈',{limit:100}).items.some(r=>r.id==='PERSON-YI_SEUNG_HUN'));
  assert.ok(atlas.search('1887년 신약',{limit:100}).items.length>0);
  assert.ok(atlas.search('세계교회협의회',{limit:100}).items.some(r=>r.id==='EVENT-WCC_FOUNDING1948'));
  assert.equal(bridge.resolve('OV-P-001').readers[0].id,'PERSON-IGNATIUS_ANTIOCH');
  assert.equal(bridge.resolve('OV-E-019').readers[0].id,'MEDIUM-AUGSBURG');
  assert.equal(bridge.resolve('OV-E-020').readers[0].id,'MEDIUM-CALVIN1536');
  assert.equal(atlas.counts.claims,22);
  assert.equal(atlas.counts.guides,11);
});
test('collision, wrong target, revoked publication hold are rejected',()=>{
  const collision=structuredClone(v307);collision.chapters[0].id=previous.delivery.readers[0].id;
  assert.throws(()=>assembleV308(old475,v305,cross304,collision),/duplicate reader/);
  const badLink=structuredClone(v307);badLink.chapters[0].related_readers[0]='UNKNOWN-READER';
  assert.throws(()=>assembleV308(old475,v305,cross304,badLink),/related-reading/);
  const badHold=structuredClone(v307);badHold.publication_gate.published=true;
  assert.throws(()=>assembleV308(old475,v305,cross304,badHold),/publication gate/);
  const invalid=structuredClone(b);invalid.publication_gate.published=true;
  assert.throws(()=>createMediumAtlas(invalid),/hold/);
});
