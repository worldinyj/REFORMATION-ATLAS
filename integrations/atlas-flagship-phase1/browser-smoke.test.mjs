import test from "node:test";
import assert from "node:assert/strict";
import {mkdir} from "node:fs/promises";
import {fileURLToPath, pathToFileURL} from "node:url";
import {resolve, dirname, join} from "node:path";
import {chromium, webkit} from "playwright";

const here=dirname(fileURLToPath(import.meta.url));
const preview=pathToFileURL(resolve(here,"preview-1529-1540.html")).href;
const engineName=process.env.ATLAS_BROWSER||"chromium";
const engines={chromium,webkit};
assert.ok(engines[engineName],"ATLAS_BROWSER must be chromium or webkit");
const outDir=join(here,"qa-artifacts");

test("V4.52 research preview real-engine browser and accessibility smoke",async t=>{
 const browser=await engines[engineName].launch({headless:true});
 t.after(async()=>{await browser.close()});
 await mkdir(outDir,{recursive:true});
 for(const width of [320,375,768,1440]){
  await t.test(engineName+" viewport "+width,async()=>{
   const page=await browser.newPage({viewport:{width,height:820},reducedMotion:"reduce"});
   const errors=[],externalRequests=[];
   page.on("pageerror",error=>errors.push(String(error)));
   page.on("console",message=>{if(message.type()==="error")errors.push(message.text())});
   page.on("request",request=>{if(/^https?:/i.test(request.url()))externalRequests.push(request.url())});
   try{
    await page.goto(preview,{waitUntil:"load"});
    assert.match(await page.title(),/종교개혁 ATLAS/);
    const data=JSON.parse(await page.locator("#data").textContent());
    assert.equal(data.events.length,4);
    assert.equal(data.docs.length,2);
    assert.equal(data.canShip,false);
    assert.equal(await page.locator("#steps button").count(),4);
    assert.match(await page.locator("#eventTitle").textContent(),/마르부르크/);
    assert.equal(await page.locator("#l0").getAttribute("aria-selected"),"true");
    assert.equal(await page.locator("#reader").getAttribute("role"),"tabpanel");
    assert.equal(await page.locator("#reader").getAttribute("aria-labelledby"),"l0");
    assert.ok((await page.locator("#reader").textContent()).length>200);
    const overflow=await page.evaluate(()=>({
      viewport:window.innerWidth,scroll:document.documentElement.scrollWidth,
      mobileSteps:window.getComputedStyle(document.getElementById("steps")).display
    }));
    assert.ok(overflow.scroll<=overflow.viewport+2,"unexpected page horizontal overflow "+JSON.stringify(overflow));
    if(width<=375)assert.equal(overflow.mobileSteps,"flex","small-screen year buttons are horizontally scrollable");

    const year1531=page.locator("#steps button").nth(2);
    await year1531.focus();
    await page.keyboard.press("Enter");
    assert.match(await page.locator("#time").textContent(),/1531/);
    assert.match(await page.locator("#eventTitle").textContent(),/신앙고백과 변증서의 인쇄/);
    assert.equal(await page.locator("#steps button").nth(2).getAttribute("aria-current"),"step");
    assert.equal(await page.evaluate(()=>document.activeElement?.closest("#steps")===document.getElementById("steps")),true,"timeline selection keeps keyboard focus");

    await page.locator("#steps button").nth(3).click();
    assert.match(await page.locator("#eventTitle").textContent(),/Variata/);
    assert.equal(await page.locator("#docs article").count(),1);
    const link=page.locator("#docs article a");
    assert.match(await link.getAttribute("href"),/^https:\/\//);
    assert.equal(await link.getAttribute("target"),"_blank");
    assert.match(await link.getAttribute("rel"),/noopener/);

    await page.locator("#l1").click();
    assert.equal(await page.locator("#l1").getAttribute("aria-selected"),"true");
    assert.equal(await page.locator("#reader").getAttribute("aria-labelledby"),"l1");
    assert.ok((await page.locator("#reader").textContent()).length>200);
    await page.locator("#l1").press("ArrowLeft");
    assert.equal(await page.locator("#l0").getAttribute("aria-selected"),"true");
    assert.equal(await page.evaluate(()=>document.activeElement?.id),"l0");
    await page.locator("#l0").press("End");
    assert.equal(await page.locator("#l1").getAttribute("aria-selected"),"true");
    await page.locator("#l1").press("Home");
    assert.equal(await page.locator("#l0").getAttribute("aria-selected"),"true");

    await page.locator("#compare").click();
    assert.equal(await page.locator("#compare").getAttribute("aria-expanded"),"true");
    assert.equal(await page.locator("#comparisonRows tr").count(),3);
    await page.locator("#sourcesBtn").click();
    assert.equal(await page.locator("#sources").isHidden(),true);
    await page.locator("#restart").click();
    assert.match(await page.locator("#eventTitle").textContent(),/마르부르크/);
    assert.equal(await page.locator("#l0").getAttribute("aria-selected"),"true");
    assert.equal(await page.locator("#comparison").isHidden(),true);
    assert.equal(await page.locator("#sources").isVisible(),true);

    await page.screenshot({path:join(outDir,engineName+"-"+width+".png"),fullPage:false});
    assert.deepEqual(errors,[],"browser console/page errors");
    assert.deepEqual(externalRequests,[],"unexpected automatic outbound request");
   } finally {await page.close();}
  });
 }
});
