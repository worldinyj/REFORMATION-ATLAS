import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const data=JSON.parse(await readFile(fileURLToPath(new URL("../../research/data/ATLAS_V459_MANUSCRIPT_PRINT_WITNESS_VARIANT_GRAPH.json",import.meta.url)),"utf8"));
const get=id=>data.witnesses.find(x=>x.id===id);

test("V4.59 every witness is a distinct identified record, with strict source provenance",()=>{
 assert.equal(data.witnessCount,10);
 assert.equal(data.witnesses.length,10);
 assert.equal(new Set(data.witnesses.map(w=>w.id)).size,10);
 assert.equal(new Set(data.manuscriptVariations.map(v=>v.id)).size,3);
 for(const w of data.witnesses){
   assert.equal(w.fullWitnessCollated,false);
   assert.ok(Array.isArray(w.sourceIds)&&w.sourceIds.length>0);
   for(const id of w.sourceIds)assert.match(data.sources[id]?.url||"",/^https:\/\//,w.id+" "+id);
 }
 for(const v of data.manuscriptVariations)for(const id of v.sourceIds)assert.ok(data.sources[id]?.url);
});

test("V4.59 Zurich Z additions at 7, 13 and 15 cannot be silently assigned to Hessian K",()=>{
 assert.equal(get("M1529-K").kind,"SIGNED_MANUSCRIPT");
 assert.equal(get("M1529-Z").kind,"SIGNED_MANUSCRIPT");
 assert.equal(get("M1529-K").article15FullPageRead,false);
 assert.equal(get("M1529-Z").article15FullPageRead,false);
 assert.deepEqual(new Set(data.manuscriptVariations.map(v=>v.section)),new Set(["Article 7","Article 13","Article 15"]));
 for(const v of data.manuscriptVariations){
   assert.equal(v.from,"M1529-K");
   assert.equal(v.to,"M1529-Z");
   assert.equal(v.preciseOriginalGermanVerified,false);
   assert.equal(v.status,"WITNESS_LEVEL_VARIANT_CONFIRMED_TEXT_NOT_COLLATED");
 }
});

test("V4.59 four 1529 prints are not equated with signed manuscripts",()=>{
 const printIds=["W2117","W2118","W2119","W2108"];
 const prints=data.witnesses.filter(w=>w.kind==="CONTEMPORARY_PRINT"&&w.year===1529);
 assert.deepEqual(new Set(prints.map(w=>w.vd16)),new Set(printIds));
 assert.ok(prints.every(w=>w.article15FullPageRead===false));
 assert.ok(get("M1529-Z").vd16===null&&get("M1529-K").vd16===null);
 assert.equal(data.sources.Z_PRINT_W2118.url,"https://doi.org/10.3931/e-rara-1085");
 assert.equal(data.sources.Z_PRINT_W2119.url,"https://doi.org/10.3931/e-rara-597");
});

test("V4.59 separate 1531 Latin and German digitized volumes, 1540 Variata and Gruber non-Variata",()=>{
 assert.equal(get("P1531-C4734").language,"Latin");
 assert.equal(get("P1531-C4734").digitalObjectId,"bsb11411960");
 assert.equal(get("P1531-C4736").language,"German");
 assert.equal(get("P1531-C4736").digitalObjectId,"bsb10160424");
 assert.equal(get("P1540-C4713").vd16,"C4713");
 assert.equal(get("P1540-C4713").year,1540);
 assert.equal(get("P1540-GRUBER-NV-UNKNOWN").vd16,null);
 assert.equal(get("P1540-GRUBER-NV-UNKNOWN").objectNumber,null);
 assert.equal(get("P1540-GRUBER-NV-UNKNOWN").article10FullPageRead,false);
});

test("V4.59 inspection level and release gates cannot be inferred from catalogue presence",()=>{
 assert.ok(get("M1529-K").textLeafInspected.includes("opening-page"));
 assert.equal(get("M1529-K").article15FullPageRead,false);
 assert.equal(data.editorialGate.historianApproved,false);
 assert.equal(data.editorialGate.canShip,false);
 assert.equal(data.editorialGate.canMergeMain,false);
 assert.equal(data.editorialGate.canImportAIStudio,false);
 assert.ok(data.unresolved.some(x=>x.includes("Gruber")));
});
