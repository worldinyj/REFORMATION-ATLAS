import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {createAtlasResearchReadOnlyBridge} from "./bridge.mjs";

const importPath=(relative)=>fileURLToPath(new URL(relative,import.meta.url));
const read=async relative=>JSON.parse(await readFile(importPath(relative),"utf8"));
const sources=async()=>({
 frozenStagingPackage:await read("../../handoff/V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json"),
 researchOverview:await read("../../research/data/V4_47_TWO_SOURCE_GROUNDED_L0_HISTORY_CORRECTIONS.json"),
 researchIntermediate:await read("../../research/data/V4_50_L1_24_CHAPTER_INTEGRATED_REVISED_MASTER.json")
});
const make=s=>createAtlasResearchReadOnlyBridge(s,{mode:"LOCAL_RESEARCH_PREVIEW"});
const copy=x=>JSON.parse(JSON.stringify(x));

test("supports exactly 8 historical volumes, 24 L1 chapters, 6 themes, 42 links, 6 intro chapters",async()=>{
 const b=make(await sources());
 assert.equal(b.meta.volumeCount,8);
 assert.equal(b.meta.intermediateChapterCount,24);
 assert.equal(b.meta.themeCount,6);
 assert.equal(b.meta.themeToHistoryLinks,42);
 assert.equal(b.meta.introChapterCount,6);
 assert.equal(b.getTheme("T415-03").links.length,7);
 assert.equal(b.catalog.length,8);
});
test("keeps V4.29 and V4.47 version identities separate for every volume",async()=>{
 const b=make(await sources());
 assert.deepEqual(b.meta.changedStagingOverviewIds,Array.from({length:8},(_,i)=>"VOL-"+String(i+1).padStart(2,"0")));
 assert.equal(b.getVolume("VOL-08").chapterIds.length,3);
 assert.equal(b.getVolume("VOL-04").stagingBodyIsSame,false);
});
test("finds historically high-risk L1 chapter and keeps evidence without implying signoff",async()=>{
 const b=make(await sources());
 const c=b.getChapter("L448-04-02");
 assert.ok(c.bodyMarkdown.includes("마르부르크"));
 assert.ok(c.sourceUrls.some(x=>x.includes("germanhistorydocs.org")));
 assert.equal(c.canShip,false);
 assert.ok(b.search("마르부르크").length>0);
 assert.ok(Object.isFrozen(c));
});
test("rejects publication, malformed routes and invalid limits",async()=>{
 const s=await sources(),b=make(s);
 assert.throws(()=>createAtlasResearchReadOnlyBridge(s,{mode:"PUBLIC_DEPLOYMENT"}),/requires explicit/);
 assert.equal(b.resolve({kind:"L1_CHAPTER",id:"NOT-REAL"}),null);
 assert.equal(b.resolve({kind:"MYTHICAL",id:"VOL-01"}),null);
 assert.throws(()=>b.search("후스",{limit:999}),/invalid search limit/);
});
test("fails closed for duplicate chapter IDs or publishing flag",async()=>{
 const s=await sources(),mutated=copy(s);
 mutated.researchIntermediate.volumes[1].chapters[0].id=mutated.researchIntermediate.volumes[0].chapters[0].id;
 assert.throws(()=>make(mutated),/globally unique/);
 const pub=copy(s);
 pub.researchIntermediate.volumes[0].chapters[0].canShip=true;
 assert.throws(()=>make(pub),/unexpectedly publishable/);
});
test("fails closed for source URL or thematic archive corruption",async()=>{
 const s=await sources(),bad=copy(s);
 bad.researchIntermediate.volumes[0].chapters[0].sourceUrls=["http://invalid.local/"];
 assert.throws(()=>make(bad),/citation field/);
 const wrong=copy(s);
 wrong.researchOverview.volumes[7].kind="CHRONOLOGICAL_VOLUME";
 assert.throws(()=>make(wrong),/thematic archive/);
});
test("fails closed if existing V4.29 baseline is marked published",async()=>{
 const s=await sources(),bad=copy(s);
 bad.frozenStagingPackage.publicationState="PUBLISHED";
 assert.throws(()=>make(bad),/must remain blocked/);
});
