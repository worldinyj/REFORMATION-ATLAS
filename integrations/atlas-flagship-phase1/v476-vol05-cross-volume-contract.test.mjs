import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {validateAtlasReviewBundle} from "./atlas-review-bundle-contract.mjs";
const f=path=>readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const b=JSON.parse(await f("../../research/data/ATLAS_V476_VOL05_REVIEW_BUNDLE.json"));
const md=await f("./V476_VOL05_CATHOLIC_REFORM_L0_L1_KO.md");
test("VOL05 uses actual shared schema, different event count from VOL04",()=>{
 assert.deepEqual(validateAtlasReviewBundle(b),{valid:true,errors:[]});
 assert.equal(b.identity.volumeId,"VOL-05");
 assert.equal(b.timeline.length,6);assert.equal(b.sources.length,8);assert.equal(b.comparisons.length,3);
 assert.equal(b.expertReview.claims.length,13);assert.equal(b.expertReview.highRiskCount,8);
});
test("Original volume05 reader texts and sources remain linked, not a fake new master",()=>{
 for(const layer of b.layers)assert.ok(md.includes(layer.markdown));
 assert.equal((b.layers[1].markdown.match(/^### /gm)||[]).length,8);
 assert.ok(b.provenance.priorVolumeNarrative.includes("V409_VOL05"));
 for(const e of b.timeline) assert.ok(e.sourceRefs.every(id=>b.sources.some(s=>s.id===id)));
});
test("1547, 1551, 1563 decree types and 1564 physical imprint are explicitly separated",()=>{
 assert.ok(b.sources.find(x=>x.id==="TS").sourceLimit.includes("개혁 교령 제18장"));
 assert.equal(b.sources.find(x=>x.id==="TM").sourceKind,"RARE_BOOK_CATALOGUE");
 assert.ok(b.unresolved.some(x=>x.id==="V5-HOLD-LATIN"));
 assert.ok(b.unresolved.some(x=>x.id==="V5-HOLD-PRINT"));
});
test("Pilot is new, unsupervised, and releases remain fail-closed",()=>{
 assert.equal(b.participant.tasks.length,3);assert.equal(b.participant.questions.length,9);
 assert.ok(b.participant.questions.every(q=>q.choices.length===4&&!("answerKey" in q)));
 assert.equal(b.participant.actualParticipants,0);assert.equal(b.expertReview.reviewersEngaged,0);
 assert.ok(b.expertReview.claims.every(c=>c.decision==="PENDING"));
 assert.ok(Object.values(b.releaseGate).every(x=>x===false));
});
test("Shared cross-volume reviewer contract denies tampered source and phantom approval",()=>{
 const mutate=x=>JSON.parse(JSON.stringify(x));
 const a=mutate(b);a.sources[0].url="http://unsafe.invalid";assert.equal(validateAtlasReviewBundle(a).valid,false);
 const c=mutate(b);c.expertReview.claims[0].expertApproved=true;assert.equal(validateAtlasReviewBundle(c).valid,false);
 const d=mutate(b);d.participant.questions[0].answerKey="A";assert.equal(validateAtlasReviewBundle(d).valid,false);
 const e=mutate(b);e.releaseGate.canShip=true;assert.equal(validateAtlasReviewBundle(e).valid,false);
});
