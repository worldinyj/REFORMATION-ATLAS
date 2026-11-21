import test from "node:test";
import assert from "node:assert/strict";
import {mkdir,readFile} from "node:fs/promises";
import {dirname,join} from "node:path";
import {fileURLToPath} from "node:url";
import {build} from "esbuild";
import {chromium,webkit} from "playwright";
const root=dirname(fileURLToPath(import.meta.url));
const engines={chromium,webkit},name=process.env.ATLAS_BROWSER||"chromium";
assert.ok(engines[name],"Use ATLAS_BROWSER=chromium or webkit");
const compiled=await build({entryPoints:[join(root,"react-v477-cross-volume-fixture.jsx")],
 bundle:true,write:false,format:"iife",platform:"browser",jsx:"automatic",loader:{".css":"empty"},
 define:{"process.env.NODE_ENV":'"production"'}});
const script=compiled.outputFiles.find(x=>x.path.endsWith(".js"))?.text||compiled.outputFiles[0].text;
const styles=await readFile(join(root,"atlas-cross-volume.css"),"utf8");
async function mount(browser,width,{granted=true,corrupt=false,tamper=false}={}){
 const page=await browser.newPage({viewport:{width,height:900},reducedMotion:"reduce"});
 const faults=[],requests=[];
 page.on("pageerror",x=>faults.push(String(x)));
 page.on("console",m=>{if(m.type()==="error")faults.push(m.text())});
 page.on("request",r=>{if(/^https?:/i.test(r.url()))requests.push(r.url())});
 await page.setContent('<!doctype html><html lang="ko"><head><meta charset="utf-8"></head><body style="margin:0"><div id="root"></div></body></html>');
 await page.evaluate(args=>{window.__V477_ACCESS__=args.granted;window.__V477_CORRUPT_SOURCE__=args.corrupt;window.__V477_TAMPER_PATH__=args.tamper},{granted,corrupt,tamper});
 await page.addStyleTag({content:styles});await page.addScriptTag({content:script});
 return {page,faults,requests};
}
test("V4.77 actual unified React reader links VOL04 and VOL05 with separate sources",async t=>{
 const browser=await engines[name].launch({headless:true});
 t.after(async()=>browser.close());
 const dir=join(root,"qa-artifacts");await mkdir(dir,{recursive:true});
 for(const width of [320,375,768,1440]){
  await t.test(name+" two-volume React "+width,async()=>{
   const {page,faults,requests}=await mount(browser,width);
   try{
    await page.locator('[data-atlas-state="CROSS_VOLUME_RESEARCH"]').waitFor();
    assert.equal(await page.locator(".atlas-cv-volume").count(),2);
    assert.equal(await page.locator(".atlas-cv-event").count(),4);
    assert.equal(await page.locator(".atlas-cv-source-card").count(),5);
    assert.equal(await page.locator(".atlas-cv-route").count(),3);
    assert.equal(await page.locator(".atlas-cv-jump").count(),6);
    assert.match(await page.locator(".atlas-cv-prose").innerText(),/마르부르크/);
    await page.getByRole("tab",{name:/L1/}).click();
    assert.equal(await page.locator(".atlas-cv-prose h3").count(),6);
    assert.match(await page.locator(".atlas-cv-trace").innerText(),/\[GA\]/);
    await page.locator(".atlas-cv-controls button").click();
    assert.equal(await page.locator(".atlas-cv-comparison tbody tr").count(),3);
    // Navigate the actual 1529→1551 guided path.  Different source corpus, same UI.
    await page.locator(".atlas-cv-route").first().locator(".atlas-cv-jump").last().click();
    assert.equal(await page.locator(".atlas-cv-volume[aria-current=page]").count(),1);
    assert.match(await page.locator(".atlas-cv-volume[aria-current=page]").innerText(),/제5권/);
    assert.equal(await page.locator(".atlas-cv-event").count(),6);
    assert.match(await page.locator(".atlas-cv-main h2").first().innerText(),/제13회기 성찬 교령/);
    assert.equal(await page.locator(".atlas-cv-prose h3").count(),8);
    assert.equal(await page.locator(".atlas-cv-source-card").count(),2);
    assert.match(await page.locator(".atlas-cv-trace").innerText(),/\[TM\]/);
    await page.locator(".atlas-cv-controls button").click();
    assert.equal(await page.locator(".atlas-cv-comparison tbody tr").count(),3);
    await page.locator(".atlas-cv-event").last().click();
    assert.equal(await page.locator(".atlas-cv-source-card").count(),3);
    assert.match(await page.locator(".atlas-cv-source-card").first().innerText(),/학술|트리엔트/);
    const dims=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth}));
    assert.ok(dims.scroll<=dims.viewport+2,"horizontal document overflow "+JSON.stringify(dims));
    await page.screenshot({path:join(dir,"v477-react-"+name+"-"+width+".png"),fullPage:false});
    await page.locator(".atlas-cv-volume").first().click();
    assert.equal(await page.locator(".atlas-cv-event").count(),4);
    assert.equal(await page.locator(".atlas-cv-prose h3").count(),0);
    assert.equal(await page.locator(".atlas-cv-source-card").count(),5);
    await page.locator(".atlas-cv-route").nth(1).locator(".atlas-cv-jump").first().click();
    assert.match(await page.locator(".atlas-cv-main h2").first().innerText(),/아우크스부르크 신앙고백 제출/);
    await page.getByRole("button",{name:/읽기 시작점으로/}).click();
    assert.equal(await page.getByRole("tab",{name:/L0/}).getAttribute("aria-selected"),"true");
    assert.equal(await page.locator(".atlas-cv-comparison").isVisible(),false);
    assert.deepEqual(faults,[]);
    assert.deepEqual(requests,[]);
   }finally{await page.close()}
  });
 }
 for(const caseData of [{granted:false,corrupt:false,tamper:false},{granted:true,corrupt:true,tamper:false},{granted:true,corrupt:false,tamper:true}]){
  await t.test(name+" fail-closed "+JSON.stringify(caseData),async()=>{
   const {page,faults,requests}=await mount(browser,375,caseData);
   try{
    await page.locator('[data-atlas-state="BLOCKED"]').waitFor();
    assert.equal(await page.locator(".atlas-cv-prose").count(),0);
    assert.equal(await page.locator(".atlas-cv-source-card").count(),0);
    assert.deepEqual(faults,[]);assert.deepEqual(requests,[]);
   }finally{await page.close()}
  });
 }
});
