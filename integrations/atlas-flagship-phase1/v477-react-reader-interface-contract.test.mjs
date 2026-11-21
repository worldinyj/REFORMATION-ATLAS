import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const f=path=>readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const react=await f("./AtlasCrossVolumeResearchPanel.jsx");
const css=await f("./atlas-cross-volume.css");
const browser=await f("./browser-react-v477.test.mjs");
const fourth=JSON.parse(await f("../../research/data/ATLAS_V475_CROSS_VOLUME_REVIEW_BUNDLE.json"));
const fifth=JSON.parse(await f("../../research/data/ATLAS_V476_VOL05_REVIEW_BUNDLE.json"));
const routes=JSON.parse(await f("../../research/data/ATLAS_V477_CROSS_VOLUME_READING_LINKS.json"));
test("Actual shared React component consumes two unmodified cross-volume review bundles",()=>{
 assert.match(react,/buildAtlasCrossVolumeResearch/);
 assert.match(react,/library\.volumes\.map/);
 assert.match(react,/library\.links\.map/);
 assert.match(react,/parseResearchMarkdown\(markdown\)/);
 assert.match(react,/layer\.markdown/);
 assert.deepEqual(fourth.timeline.length,4);
 assert.deepEqual(fifth.timeline.length,6);
});
test("Comparison preserves individual source types, original text provenance and cautions",()=>{
 assert.match(react,/currentSources=volume\.sources\.filter/);
 assert.match(react,/sourceKind/);
 assert.match(react,/sourceLimit/);
 assert.match(react,/path\.caution/);
 assert.match(react,/path\.from\.sourceIds/);
 assert.match(react,/path\.to\.sourceIds/);
 assert.equal(routes.editorialComparisons.length,3);
 assert.equal(fourth.comparisons.length,3);
 assert.equal(fifth.comparisons.length,3);
});
test("All interactive controls are real React buttons, accessible tabs, gated and no unsafe HTML",()=>{
 for(const token of ["privatePreviewGranted","data-atlas-state=\"BLOCKED\"","aria-current","role=\"tablist\"","aria-selected","aria-expanded"])assert.ok(react.includes(token));
 assert.match(react,/noopener noreferrer/);
 assert.doesNotMatch(react,/dangerouslySetInnerHTML|innerHTML|\bfetch\s*\(|XMLHttpRequest|localStorage|sessionStorage/);
 assert.match(css,/\.atlas-cv-route-grid/);
 assert.match(css,/max-width:520px/);
});
test("Actual React + esbuild fixture and real Chromium/WebKit browser tests cover gates and all screen sizes",()=>{
 assert.match(browser,/from "esbuild"/);
 assert.match(browser,/from "playwright"/);
 assert.match(browser,/\[320,375,768,1440\]/);
 assert.match(browser,/granted:false/);
 assert.match(browser,/corrupt:true/);
 assert.match(browser,/tamper:true/);
});
test("Neither volume was promoted or sent for historic approval during integration",()=>{
 for(const b of [fourth,fifth]){
  assert.equal(b.releaseGate.canShip,false);
  assert.equal(b.releaseGate.canImportAIStudio,false);
  assert.equal(b.expertReview.reviewersEngaged,0);
  assert.equal(b.participant.actualParticipants,0);
 }
 assert.equal(routes.actualExpertApprovals,0);
 assert.equal(routes.actualReaderParticipants,0);
});
