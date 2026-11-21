import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {parseResearchMarkdown} from "./research-markdown.mjs";
const f=path=>readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const html=await f("./preview-v473-1529-1540.html");
const raw=html.split('id="data">')[1]?.split("</script>")[0];
const js=html.split("<script>")[1]?.split("</script>")[0];
assert.ok(raw&&js);
const data=JSON.parse(raw);
const v472=await f("./V472_MARBURG_1529_L0_L1_REVISED_READER_CANDIDATE_KO.md");
const audit=JSON.parse(await f("../../research/data/ATLAS_V472_MARBURG_REVISED_READER_CANDIDATE_AND_REDLINES.json"));
const slice=(a,b)=>v472.split(a)[1].split(b)[0].trim().replace(/^[^\n]*\n/,"").trim();
class El{
 constructor(tag,doc){this.tag=tag;this.doc=doc;this.children=[];this.attrs={};this.handlers={};this.hidden=false;this._text="";}
 get textContent(){return this._text+this.children.map(c=>c.textContent??"").join("")}
 set textContent(v){this._text=String(v);this.children=[]}
 append(...args){this.children.push(...args)}
 appendChild(x){this.children.push(x);return x}
 replaceChildren(...args){this.children=[...args];this._text=""}
 setAttribute(k,v){this.attrs[k]=v}
 addEventListener(k,f){this.handlers[k]=f}
 click(){this.handlers.click?.()}
 focus(){this.doc.activeElement=this}
}
function runtime(){
 const nodes=new Map();
 const doc={activeElement:null,getElementById(id){if(!nodes.has(id))nodes.set(id,new El(id,doc));return nodes.get(id)},createElement(tag){return new El(tag,doc)},createTextNode(s){const n=new El("#text",doc);n.textContent=s;return n}};
 doc.getElementById("data").textContent=raw;
 new Function("document","URL",js)(doc,URL);
 return {n:id=>doc.getElementById(id),doc};
}
const human=s=>parseResearchMarkdown(s).map(b=>b.segments.map(t=>t.text).join("")).join("");
test("V4.73 actually embeds complete and unmodified V4.72 L0 and L1 research copy",()=>{
 assert.equal(data.l0.text,slice("## L0 |","## L1 |"));
 assert.equal(data.l1.text,slice("## L1 |","## 독자에게 열어 둘 질문"));
 assert.equal(parseResearchMarkdown(data.l1.text).filter(b=>b.tag==="h3").length,6);
 assert.ok(data.l0.text.includes("핵심 쟁점 가운데 하나"));
 assert.equal(data.contentOrigin.sourceDocumentBlobSha.length,40);
});
test("All six evidence cards keep exact audited external sources and claims separation",()=>{
 assert.equal(data.docs.length,6);
 assert.deepEqual(new Set(data.docs.map(d=>d.id)),new Set(["GA","GE","WP","ZA","SC","GR"]));
 const map={GA:"GHDI_ARTICLES",GE:"GHDI_EYEWITNESS",WP:"W2119_PRINT",ZA:"Z_ARCHIVE",SC:"SCHAFF",GR:"GRUBER"};
 for(const doc of data.docs){
  assert.equal(doc.sourceUrl,audit.sourceRegistry.find(x=>x.id===map[doc.id]).url);
  assert.ok(doc.sourceUrl.startsWith("https://")&&doc.note.length>10);
 }
 assert.equal(data.witnessComparison.length,3);
 assert.match(data.witnessComparison[2].limit,/0\/2/);
});
test("Offline standalone document is a research-only open HTML, not a private preview or production app",()=>{
 assert.equal(data.previewOnly,true);
 assert.equal(data.canShip,false);
 assert.equal(data.releaseGate.canShip,false);
 assert.equal(data.releaseGate.canImportAIStudio,false);
 assert.equal(data.releaseGate.hostAccessControlsVerified,false);
 assert.match(html,/GitHub의 연구 파일은 비공개 접근 통제를 제공하지 않음/);
 assert.doesNotMatch(html,/<script\s+src=/i);
 assert.doesNotMatch(js,/\bfetch\s*\(|XMLHttpRequest|localStorage|sessionStorage|sendBeacon|innerHTML|insertAdjacentHTML/);
});
test("V4.72 L0/L1, evidence trace and six sourced cards actually operate in DOM",()=>{
 const {n}=runtime();
 assert.equal(n("steps").children.length,4);
 assert.equal(n("docs").children.length,5);
 assert.equal(n("reader").textContent,human(data.l0.text));
 assert.match(n("evidenceTrace").textContent,/\[GA\]/);
 assert.match(n("evidenceTrace").textContent,/\[ZA\]/);
 n("l1").click();
 assert.equal(n("reader").textContent,human(data.l1.text));
 assert.equal(n("reader").children.filter(c=>c.tag==="h3").length,6);
 assert.equal(n("l1").attrs["aria-selected"],"true");
 assert.match(n("evidenceTrace").textContent,/\[GR\]/);
});
test("Year, edition comparison, witness comparison and reset work in a real DOM simulator",()=>{
 const {n}=runtime();
 n("compare").click();
 assert.equal(n("comparison").hidden,false);
 assert.equal(n("comparisonRows").children.length,3);
 n("witnessBtn").click();
 assert.equal(n("witnessEvidence").hidden,false);
 assert.equal(n("witnessRows").children.length,3);
 n("steps").children[3].click();
 assert.equal(n("docs").children.length,2);
 assert.match(n("docs").textContent,/그루버/);
 n("sourcesBtn").click();
 assert.equal(n("sources").hidden,true);
 n("restart").click();
 assert.equal(n("comparison").hidden,true);
 assert.equal(n("witnessEvidence").hidden,true);
 assert.equal(n("sources").hidden,false);
 assert.equal(n("docs").children.length,5);
 assert.equal(n("reader").textContent,human(data.l0.text));
});
