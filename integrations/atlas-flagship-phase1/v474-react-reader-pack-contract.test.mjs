import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const read=path=>readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const html=await read("./preview-v473-1529-1540.html");
const preview=JSON.parse(html.split('id="data">')[1].split("</script>")[0]);
const pack=JSON.parse(await read("../../research/data/ATLAS_V474_REACT_READER_PACK.json"));
const jsx=await read("./AtlasFlagship1529Panel.jsx");
const css=await read("./atlas-flagship.css");
const fixture=await read("./react-v474-fixture.jsx");
test("React reader pack preserves V4.72 L0/L1 exact reviewed editorial text",()=>{
 assert.equal(pack.l0.text,preview.l0.text);
 assert.equal(pack.l1.text,preview.l1.text);
 assert.equal(pack.sourceDocumentBlobSha,preview.contentOrigin.sourceDocumentBlobSha);
 assert.ok(pack.l1.text.includes("저본의 전승 관계를 확정할 수는 없다"));
 assert.equal((pack.l1.text.match(/^### /gm)||[]).length,6);
});
test("Six cards and three original/print/translation witness comparisons preserve source limits",()=>{
 assert.equal(pack.sources.length,6);
 assert.equal(pack.witnessComparison.length,3);
 for(const source of pack.sources){
  assert.ok(source.sourceUrl.startsWith("https://"));
  assert.equal(source.sourceUrl,preview.docs.find(x=>x.id===source.id)?.sourceUrl);
  assert.ok(source.note.length>20);
 }
 assert.ok(pack.witnessComparison.find(x=>x.id==="KZ").limit.includes("0/2"));
});
test("React host gate is strict, missing/tainted researchPack cannot silently fall back",()=>{
 assert.match(jsx,/readerPack=null/);
 assert.match(jsx,/readerPack\.schema|readerPack\?\.schema/);
 assert.match(jsx,/readerPack\.releaseGate\?\.canShip!==false/);
 assert.match(jsx,/!privatePreviewGranted\|\|!integrity/);
 assert.equal(pack.releaseGate.canShip,false);
 assert.equal(pack.releaseGate.canMergeMain,false);
 assert.equal(pack.releaseGate.canImportAIStudio,false);
 assert.equal(pack.releaseGate.hostAccessControlsVerified,false);
 assert.equal(pack.historianApproved,false);
 assert.equal(pack.readerPilotConfirmed,false);
});
test("Research-only React renders real complete texts, provenance and witness rows without unsafe HTML",()=>{
 assert.match(jsx,/SafeResearchMarkdown source=\{activeText\}/);
 assert.match(jsx,/integrity\.pack\.witnessComparison\.map/);
 assert.match(jsx,/sourceIds\.map/);
 assert.match(jsx,/setShowWitnessCompare/);
 assert.match(css,/\.atlas-fp-witness-control/);
 assert.doesNotMatch(jsx,/dangerouslySetInnerHTML|innerHTML|\bfetch\s*\(/);
 assert.match(fixture,/privatePreviewGranted=\{granted\}/);
});
test("Browser test compiles actual React with local source pack and tests fail closed",()=>{
 const code=await read("./browser-react-v474.test.mjs");
 assert.match(code,/import \{build\} from "esbuild"/);
 assert.match(code,/import \{chromium,webkit\} from "playwright"/);
 assert.match(code,/\[320,375,768,1440\]/);
 assert.match(code,/corrupt:true/);
 assert.match(code,/granted:false/);
 assert.equal(pack.canShip,false);
});
