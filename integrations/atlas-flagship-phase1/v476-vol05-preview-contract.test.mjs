import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const read=path=>readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const b=JSON.parse(await read("../../research/data/ATLAS_V476_VOL05_REVIEW_BUNDLE.json"));
const html=await read("./preview-v476-vol05.html");
const embedded=JSON.parse(html.split('id="data">')[1].split("</script>")[0]);
test("VOL05 browser preview has full real research text and exactly six anchored events",()=>{
 assert.deepEqual(embedded.layers,b.layers);
 assert.deepEqual(embedded.timeline,b.timeline);
 assert.deepEqual(embedded.sources,b.sources);
 assert.deepEqual(embedded.comparisons,b.comparisons);
 assert.equal(embedded.timeline.length,6);
 assert.equal((embedded.layers[1].markdown.match(/^### /gm)||[]).length,8);
});
test("Preview is a standalone research artifact, not a shipping app or private host",()=>{
 assert.equal(embedded.releaseGate.canShip,false);
 assert.equal(embedded.releaseGate.canImportAIStudio,false);
 assert.match(html,/GitHub/); 
 assert.doesNotMatch(html,/<script\s+src|\bfetch\s*\(|XMLHttpRequest|localStorage|sessionStorage|sendBeacon|innerHTML|<img\b/i);
});
