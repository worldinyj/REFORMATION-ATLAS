import test from "node:test";
import assert from "node:assert/strict";
import {mkdir} from "node:fs/promises";
import {fileURLToPath,pathToFileURL} from "node:url";
import {dirname,join} from "node:path";
import {chromium,webkit} from "playwright";
const here=dirname(fileURLToPath(import.meta.url)),browserName=process.env.ATLAS_BROWSER||"chromium";
const engine={chromium,webkit}[browserName];
assert.ok(engine,"browser missing");
test("V4.76 VOL05 actual browser L0/L1, six events, evidence 8, print witness",async t=>{
 const browser=await engine.launch({headless:true});t.after(async()=>browser.close());
 const shots=join(here,"qa-artifacts");await mkdir(shots,{recursive:true});
 for(const width of [320,375,768,1440])await t.test(browserName+" VOL05 "+width,async()=>{
  const page=await browser.newPage({viewport:{width,height:850},reducedMotion:"reduce"});
  const faults=[],requests=[];page.on("pageerror",e=>faults.push(String(e)));
  page.on("request",r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  try{
   await page.goto(pathToFileURL(join(here,"preview-v476-vol05.html")).href);
   assert.equal(await page.locator("#years button").count(),6);
   assert.equal(await page.locator("#sourceCards article").count(),2);
   assert.match(await page.locator("#reader").innerText(),/예수회/);
   await page.locator("#l1").click();
   assert.equal(await page.locator("#reader h3").count(),8);
   assert.match(await page.locator("#trace").innerText(),/\[TM\]/);
   await page.locator("#compareBtn").click();
   assert.equal(await page.locator("#compareRows tr").count(),3);
   await page.locator("#years button").last().click();
   assert.equal(await page.locator("#sourceCards article").count(),3);
   assert.match(await page.locator("#caution").innerText(),/인쇄본/);
   const dims=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth}));
   assert.ok(dims.scroll<=dims.viewport+2,"horizontal overflow "+JSON.stringify(dims));
   await page.screenshot({path:join(shots,"v476-vol05-"+browserName+"-"+width+".png"),fullPage:false});
   await page.locator("#reset").click();
   assert.equal(await page.locator("#l0").getAttribute("aria-selected"),"true");
   assert.equal(await page.locator("#compare").isVisible(),false);
   assert.deepEqual(faults,[]);assert.deepEqual(requests,[]);
  }finally{await page.close()}
 });
});
