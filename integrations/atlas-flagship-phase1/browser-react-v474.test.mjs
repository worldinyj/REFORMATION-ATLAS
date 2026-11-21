import test from "node:test";
import assert from "node:assert/strict";
import {mkdir,readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {dirname,join} from "node:path";
import {build} from "esbuild";
import {chromium,webkit} from "playwright";
const folder=dirname(fileURLToPath(import.meta.url));
const engines={chromium,webkit};
const name=process.env.ATLAS_BROWSER||"chromium";
assert.ok(engines[name],"Supported engines: chromium, webkit");
const bundler=await build({entryPoints:[join(folder,"react-v474-fixture.jsx")],
  bundle:true,write:false,format:"iife",platform:"browser",jsx:"automatic",
  loader:{".css":"empty"},define:{"process.env.NODE_ENV":'"production"'}});
const script=bundler.outputFiles.find(f=>f.path.endsWith(".js"))?.text||bundler.outputFiles[0].text;
const css=await readFile(join(folder,"atlas-flagship.css"),"utf8");
async function mount(browser,width,{granted=true,corrupt=false}={}){
 const page=await browser.newPage({viewport:{width,height:820},reducedMotion:"reduce"});
 const errors=[],network=[];
 page.on("pageerror",e=>errors.push(String(e)));
 page.on("console",x=>{if(x.type()==="error")errors.push(x.text())});
 page.on("request",r=>{if(/^https?:/i.test(r.url()))network.push(r.url())});
 await page.setContent('<!doctype html><html lang="ko"><head><meta charset="utf-8"></head><body style="margin:0"><div id="root"></div></body></html>');
 await page.evaluate(({granted,corrupt})=>{window.__ATLAS_V474_TEST_GRANT__=granted;window.__ATLAS_V474_CORRUPT_PACK__=corrupt},{granted,corrupt});
 await page.addStyleTag({content:css});
 await page.addScriptTag({content:script});
 return {page,errors,network};
}
test("V4.74 React source-aware research panel (actual React DOM, not HTML mock)",async t=>{
 const engine=engines[name];
 const browser=await engine.launch({headless:true});
 t.after(async()=>browser.close());
 const out=join(folder,"qa-artifacts");await mkdir(out,{recursive:true});
 for(const width of [320,375,768,1440]){
  await t.test(name+" React responsive "+width,async()=>{
   const {page,errors,network}=await mount(browser,width);
   try{
    await page.locator('[data-atlas-state="RESEARCH_PREVIEW"]').waitFor();
    assert.equal(await page.locator(".atlas-fp-year").count(),4);
    assert.equal(await page.locator(".atlas-fp-source").count(),6,"1529 shows five source cards and one evidence-kind legend");
    assert.equal(await page.locator(".atlas-fp-sources article.atlas-fp-source").count(),5);
    assert.match(await page.locator(".atlas-fp-prose").innerText(),/핵심 쟁점 가운데 하나/);
    assert.match(await page.locator(".atlas-fp-provenance").innerText(),/\[GA\]/);
    await page.getByRole("tab",{name:/L1/}).click();
    assert.equal(await page.locator(".atlas-fp-prose h3").count(),6);
    assert.match(await page.locator(".atlas-fp-prose").innerText(),/저본의 전승 관계를 확정할 수는 없다/);
    assert.equal(await page.locator(".atlas-fp-provenance a").count(),6);
    await page.getByRole("button",{name:/1530·1531·1540년 판본 비교/}).click();
    assert.equal(await page.locator(".atlas-fp-compare").first().locator("tbody tr").count(),3);
    await page.getByRole("button",{name:/1529년 인쇄본·번역문·서명본 비교/}).click();
    assert.equal(await page.locator(".atlas-fp-witness tbody tr").count(),3);
    assert.match(await page.locator(".atlas-fp-witness").innerText(),/0\/2/);
    await page.locator(".atlas-fp-year").last().click();
    assert.equal(await page.locator(".atlas-fp-sources article.atlas-fp-source").count(),2);
    await page.getByRole("button",{name:/사료 카드 접기/}).click();
    assert.equal(await page.locator(".atlas-fp-sources").isVisible(),false);
    const size=await page.evaluate(()=>({viewport:window.innerWidth,scroll:document.documentElement.scrollWidth}));
    assert.ok(size.scroll<=size.viewport+2,"Unexpected overflow "+JSON.stringify(size));
    await page.screenshot({path:join(out,"v474-react-"+name+"-"+width+".png"),fullPage:false});
    await page.getByRole("button",{name:/1529년으로 돌아가기/}).click();
    assert.equal(await page.getByRole("tab",{name:/L0/}).getAttribute("aria-selected"),"true");
    assert.equal(await page.locator(".atlas-fp-witness").isVisible(),false);
    assert.equal(await page.locator(".atlas-fp-sources").isVisible(),true);
    assert.equal(await page.locator(".atlas-fp-sources article.atlas-fp-source").count(),5);
    assert.deepEqual(errors,[]);
    assert.deepEqual(network,[]);
   }finally{await page.close()}
  });
 }
 for(const scenario of [{granted:false,corrupt:false},{granted:true,corrupt:true}]){
  await t.test(name+" fail-closed "+JSON.stringify(scenario),async()=>{
   const {page,errors,network}=await mount(browser,375,scenario);
   try{
    await page.locator('[data-atlas-state="BLOCKED"]').waitFor();
    assert.equal(await page.locator(".atlas-fp-prose").count(),0);
    assert.equal(await page.locator(".atlas-fp-sources").count(),0);
    assert.deepEqual(errors,[]);
    assert.deepEqual(network,[]);
   }finally{await page.close()}
  });
 }
});
