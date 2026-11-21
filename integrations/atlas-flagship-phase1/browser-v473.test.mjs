import test from "node:test";
import assert from "node:assert/strict";
import {mkdir} from "node:fs/promises";
import {fileURLToPath,pathToFileURL} from "node:url";
import {dirname,join,resolve} from "node:path";
import {chromium,webkit} from "playwright";
const here=dirname(fileURLToPath(import.meta.url));
const name=process.env.ATLAS_BROWSER||"chromium", engines={chromium,webkit};
assert.ok(engines[name],"ATLAS_BROWSER must be chromium or webkit");
test("V4.73 browser: complete revised L0/L1, sources, witness table, safe restart across viewports",async t=>{
 const browser=await engines[name].launch({headless:true});
 t.after(async()=>browser.close());
 const dir=join(here,"qa-artifacts");await mkdir(dir,{recursive:true});
 for(const width of [320,375,768,1440]){
  await t.test(name+" viewport "+width,async()=>{
   const page=await browser.newPage({viewport:{width,height:820},reducedMotion:"reduce"});
   const errors=[],requests=[];
   page.on("pageerror",e=>errors.push(String(e)));
   page.on("console",m=>{if(m.type()==="error")errors.push(m.text())});
   page.on("request",r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
   try{
    await page.goto(pathToFileURL(resolve(here,"preview-v473-1529-1540.html")).href);
    const payload=JSON.parse(await page.locator("#data").textContent());
    assert.equal(payload.canShip,false);
    assert.equal(payload.docs.length,6);
    assert.equal(await page.locator("#steps button").count(),4);
    assert.equal(await page.locator("#docs article").count(),5);
    assert.match(await page.locator("#reader").innerText(),/핵심 쟁점 가운데 하나/);
    await page.locator("#l1").click();
    assert.equal(await page.locator("#reader h3").count(),6);
    assert.match(await page.locator("#reader").innerText(),/저본의 전승 관계를 확정할 수는 없다/);
    assert.match(await page.locator("#evidenceTrace").innerText(),/\[GR\]/);
    await page.locator("#compare").click();
    assert.equal(await page.locator("#comparisonRows tr").count(),3);
    await page.locator("#witnessBtn").click();
    assert.equal(await page.locator("#witnessRows tr").count(),3);
    assert.match(await page.locator("#witnessEvidence").innerText(),/직접 판독 0\/2/);
    await page.locator("#steps button").nth(3).click();
    assert.equal(await page.locator("#docs article").count(),2);
    const size=await page.evaluate(()=>({viewport:window.innerWidth,body:document.documentElement.scrollWidth}));
    assert.ok(size.body<=size.viewport+2,"horizontal overflow "+JSON.stringify(size));
    await page.screenshot({path:join(dir,"v473-"+name+"-"+width+".png"),fullPage:false});
    await page.locator("#restart").click();
    assert.equal(await page.locator("#witnessEvidence").isVisible(),false);
    assert.equal(await page.locator("#comparison").isVisible(),false);
    assert.equal(await page.locator("#l0").getAttribute("aria-selected"),"true");
    assert.equal(await page.locator("#docs article").count(),5);
    assert.deepEqual(errors,[]);
    assert.deepEqual(requests,[]);
   }finally{await page.close()}
  });
 }
});
