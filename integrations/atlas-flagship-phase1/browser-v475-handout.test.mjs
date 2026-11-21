import test from "node:test";
import assert from "node:assert/strict";
import {fileURLToPath,pathToFileURL} from "node:url";
import {dirname,join} from "node:path";
import {mkdir} from "node:fs/promises";
import {chromium,webkit} from "playwright";
const folder=dirname(fileURLToPath(import.meta.url));
const engine=process.env.ATLAS_BROWSER||"chromium";
const engines={chromium,webkit};
assert.ok(engines[engine],"ATLAS_BROWSER chromium or webkit");
test("V4.75 actual browser printable 9-question participant sheet, no network or horizontal overflow",async t=>{
 const browser=await engines[engine].launch({headless:true});
 t.after(async()=>browser.close());
 const out=join(folder,"qa-artifacts");await mkdir(out,{recursive:true});
 for(const width of [320,375,768,1440]){
  await t.test(engine+" V475 participant sheet "+width,async()=>{
   const page=await browser.newPage({viewport:{width,height:900},reducedMotion:"reduce"});
   const errors=[],external=[];
   page.on("pageerror",x=>errors.push(String(x)));
   page.on("request",r=>{if(/^https?:/i.test(r.url()))external.push(r.url())});
   try{
    await page.goto(pathToFileURL(join(folder,"V475_READER_PILOT_WORKSHEET.html")).href);
    assert.equal(await page.locator(".task").count(),3);
    assert.equal(await page.locator(".question").count(),9);
    assert.equal(await page.locator('input[type="radio"]').count(),36);
    assert.equal(await page.locator("script").count(),0);
    assert.equal(await page.locator('input[name="Q09"]').count(),4);
    assert.equal(await page.locator('input[name="Q01"]:checked').count(),0);
    await page.locator('input[name="Q01"][value="A"]').check();
    assert.equal(await page.locator('input[name="Q01"]:checked').count(),1);
    const dims=await page.evaluate(()=>({page:document.documentElement.scrollWidth,screen:window.innerWidth}));
    assert.ok(dims.page<=dims.screen+2,"page overflow "+JSON.stringify(dims));
    await page.screenshot({path:join(out,"v475-worksheet-"+engine+"-"+width+".png"),fullPage:false});
    assert.deepEqual(errors,[]);
    assert.deepEqual(external,[]);
   }finally{await page.close()}
  });
 }
});
