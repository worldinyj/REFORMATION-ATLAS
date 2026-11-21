import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {buildAtlasCrossVolumeResearch,getAtlasResearchEvent} from "./atlas-cross-volume-research.mjs";
const read=path=>readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const fourth=JSON.parse(await read("../../research/data/ATLAS_V475_CROSS_VOLUME_REVIEW_BUNDLE.json"));
const fifth=JSON.parse(await read("../../research/data/ATLAS_V476_VOL05_REVIEW_BUNDLE.json"));
const registry=JSON.parse(await read("../../research/data/ATLAS_V477_CROSS_VOLUME_READING_LINKS.json"));
const clone=x=>JSON.parse(JSON.stringify(x));
test("V4.77 validates actual V4.75 and V4.76 bundles without changing historical source text",()=>{
 const result=buildAtlasCrossVolumeResearch([fourth,fifth],registry);
 assert.equal(result.ok,true,JSON.stringify(result.errors));
 assert.deepEqual(result.volumes.map(x=>x.identity.volumeId),["VOL-04","VOL-05"]);
 assert.deepEqual(result.volumes.map(x=>x.timeline.length),[4,6]);
 assert.deepEqual(result.volumes.map(x=>x.sources.length),[6,8]);
 assert.deepEqual(result.volumes.map(x=>x.layers[1].markdown.split(/^### /gm).length-1),[6,8]);
 assert.equal(result.volumes[0].layers[1].markdown,fourth.layers[1].markdown);
 assert.equal(result.volumes[1].layers[1].markdown,fifth.layers[1].markdown);
});
test("Cross-volume paths are anchored in event-specific existing sources, not just matching years",()=>{
 const result=buildAtlasCrossVolumeResearch([fourth,fifth],registry);
 assert.equal(result.links.length,3);
 for(const p of result.links){
  assert.notEqual(p.from.volumeId,p.to.volumeId);
  assert.equal(p.interpretationStatus,"UNREVIEWED_COMPARATIVE_EDITORIAL_LINK");
  for(const end of [p.from,p.to]){
   const resolved=getAtlasResearchEvent(result,end.volumeId,end.eventId);
   assert.ok(resolved,p.id);
   assert.ok(end.sourceIds.every(id=>resolved.event.sourceRefs.includes(id)));
  }
  assert.ok(p.caution.length>60,"Require meaningful historical caveat");
 }
 assert.match(result.links.find(x=>x.id==="CV-PATH-1540").caution,/같은 연도/);
});
test("No false historian, reader, rights or production approval is allowed",()=>{
 for(const route of registry.editorialComparisons)assert.equal(route.expertApproved,false);
 assert.equal(registry.actualReaderParticipants,0);
 assert.equal(registry.actualExpertApprovals,0);
 assert.equal(registry.operatingAppModified,false);
 assert.equal(registry.mainModified,false);
 assert.deepEqual(Object.values(registry.releaseGate).every(x=>x===false),true);
 for(const b of [fourth,fifth]){
  assert.ok(b.expertReview.claims.every(x=>x.decision==="PENDING"));
  assert.equal(b.participant.actualParticipants,0);
 }
});
test("Missing/unsafe source, fabricated review, and tampered cross-link all fail closed",()=>{
 const invalids=[
  ()=>{const a=clone(fifth);a.releaseGate.canShip=true;return [[fourth,a],registry]},
  ()=>{const a=clone(fourth);a.sources[0].url="http://unsafe.invalid";return [[a,fifth],registry]},
  ()=>{const a=clone(registry);a.editorialComparisons[0].to.sourceIds=["TD"];return [[fourth,fifth],a]},
  ()=>{const a=clone(registry);a.editorialComparisons[0].caution="";return [[fourth,fifth],a]},
  ()=>{const a=clone(registry);a.editorialComparisons[1].expertApproved=true;return [[fourth,fifth],a]},
  ()=>{const a=clone(registry);a.releaseGate.canImportAIStudio=true;return [[fourth,fifth],a]},
  ()=>{const a=clone(registry);a.actualReaderParticipants=8;return [[fourth,fifth],a]},
  ()=>{const a=clone(registry);a.editorialComparisons[0].to.volumeId="VOL-04";return [[fourth,fifth],a]}
 ];
 for(const factory of invalids){const [bs,links]=factory();assert.equal(buildAtlasCrossVolumeResearch(bs,links).ok,false)}
});
test("Unique IDs, absent volume and wrong order cannot silently fall back",()=>{
 assert.equal(buildAtlasCrossVolumeResearch([fourth,fourth],registry).ok,false);
 assert.equal(buildAtlasCrossVolumeResearch([fourth],registry).ok,false);
 const a=clone(registry);a.visualOrder=["VOL-04","VOL-04"];
 assert.equal(buildAtlasCrossVolumeResearch([fourth,fifth],a).ok,false);
});
