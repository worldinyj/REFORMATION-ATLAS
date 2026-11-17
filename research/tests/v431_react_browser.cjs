#!/usr/bin/env node
"use strict";
// Actual React browser consumer QA, NOT a test of the separate AI Studio app.
const fs=require("node:fs"),path=require("node:path"),http=require("node:http");
const {execFileSync}=require("node:child_process");
const {chromium,webkit}=require("playwright");
const ROOT=path.resolve(__dirname,"../.."),OUT=path.join(ROOT,"research/artifacts/V431_react_checks");
const BUNDLE="/tmp/atlas-v431-build";
const PINNED={
 "integrations/atlas-l0-v431/AtlasL0Panel.jsx":"c62d691430eccddd9fa52d1d1b38782404352ba1",
 "integrations/atlas-l0-v431/atlas-l0.css":"1eaca9d7f08d8afcfe785e319be3a41516c067b1",
 "integrations/atlas-l0-v431/demo-entry.jsx":"244a85496ccab8c8fca0d9858b4759430c1d2307",
 "integrations/atlas-l0-v431/demo.html":"a4e66ceddffcc02fa597d494888a792bf5b7796e",
 "integrations/atlas-l0-v430/bridge.mjs":"1f585f31cf10e05530662e05c228de3519ef8632",
 "handoff/V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json":"64c27c0dfe05394acbb049807e4c4384d58908b9"
};
for(const [file,sha] of Object.entries(PINNED)){
 const found=execFileSync("git",["hash-object",path.join(ROOT,file)],{encoding:"utf8"}).trim();
 if(sha!==found)throw Error("V431 input SHA mismatch: "+file+" "+found);
}
for(const f of ["bundle.js","bundle.css"])if(!fs.existsSync(path.join(BUNDLE,f)))throw Error("Missing browser bundle "+f);
const allowed=new Map([
 ["/demo.html",path.join(ROOT,"integrations/atlas-l0-v431/demo.html")],
 ["/bundle.js",path.join(BUNDLE,"bundle.js")],
 ["/bundle.css",path.join(BUNDLE,"bundle.css")]
]);
const mime=p=>p.endsWith(".css")?"text/css; charset=utf-8":p.endsWith(".js")?"text/javascript; charset=utf-8":"text/html; charset=utf-8";
const server=http.createServer((req,res)=>{
 const name=new URL(req.url,"http://127.0.0.1").pathname;
 const file=allowed.get(name);if(!file){res.writeHead(404);res.end("Not found");return;}
 res.writeHead(200,{"Content-Type":mime(name),"Cache-Control":"no-store","X-Content-Type-Options":"nosniff"});
 fs.createReadStream(file).pipe(res);
});
fs.mkdirSync(OUT,{recursive:true});
const rows=[],errors=[],shots=[];
function check(engine,size,key,passed,detail){
 const row={engine,size,key,status:passed?"PASS":"FAIL",detail:String(detail??"")};
 rows.push(row);if(!passed)errors.push(row);
}
async function verifyBrowser(name,engine,base){
 const browser=await engine.launch({headless:true});
 try{
  const profiles=[{id:"desktop",w:1440,h:900},{id:"mobile",w:375,h:812},{id:"small",w:320,h:700}];
  for(const size of profiles){
   const ctx=await browser.newContext({viewport:{width:size.w,height:size.h},locale:"ko-KR",reducedMotion:"reduce"});
   const page=await ctx.newPage(),exceptions=[],remote=[];
   page.on("pageerror",e=>exceptions.push(e.message));
   page.on("request",r=>{if(!r.url().startsWith(base))remote.push(r.url());});
   try{
    await page.goto(base+"/demo.html");
    await page.waitForSelector('[data-atlas-state="READY"]',{timeout:20000});
    check(name,size.id,"React+V429 bridge initialized",true);
    check(name,size.id,"8 volume cards",(await page.locator('[data-testid^="entry-VOL-"]').count())===8);
    check(name,size.id,"VOL08 thematic archive",(await page.locator('[data-testid="entry-VOL-08"]').innerText()).includes("주제 아카이브"));
    await screenshot(page,name,size.id,"volumes");
    await overflow(page,name,size.id,"volumes");
    await page.locator('[data-testid="entry-VOL-01"]').click();
    const article=page.locator(".atlas-l0-article");
    const volText=await article.innerText();
    check(name,size.id,"exact first historical prose",volText.includes("니케아")&&volText.includes("악숨")&&volText.length>250);
    check(name,size.id,"actual Markdown rendered as heading",await page.locator(".atlas-l0-text h4").count()>0);
    check(name,size.id,"strong text semantic tag",await page.locator(".atlas-l0-text strong").count()>0);
    await overflow(page,name,size.id,"volume article");
    await page.locator('[data-testid="tab-THEME_INDEX"]').click();
    check(name,size.id,"six themes",(await page.locator('[data-testid^="entry-T415-"]').count())===6);
    await page.locator('[data-testid="entry-T415-06"]').click();
    check(name,size.id,"seven temporal cross links",(await page.locator('[data-testid^="link-VOL-"]').count())===7);
    await page.locator('[data-testid="link-VOL-07"]').click();
    check(name,size.id,"theme link to Korean volume",(await article.innerText()).includes("한국")&&(await article.innerText()).length>200);
    await overflow(page,name,size.id,"linked article");
    await screenshot(page,name,size.id,"linked-vol07");
    await page.locator('[data-testid="tab-CHAPTER_INDEX"]').click();
    check(name,size.id,"six introduction scenes",(await page.locator('[data-testid^="entry-INTRO-"]').count())===6);
    await page.locator('[data-testid="entry-INTRO-1"]').click();
    check(name,size.id,"first intro chapter rendered",(await article.innerText()).includes("1517년"));
    await page.getByRole("button",{name:/다음 →/}).first().click();
    check(name,size.id,"next chapter action",(await article.innerText()).includes("2."));
    await overflow(page,name,size.id,"reader chapter");
    const search=page.locator("#atlas-l0-search");
    await search.fill("후스");
    check(name,size.id,"Korean real corpus search",(await page.locator('[data-testid^="hit-"]').count())>0);
    await screenshot(page,name,size.id,"search");
    await overflow(page,name,size.id,"search");
    await search.fill("");
    check(name,size.id,"empty search returns to index",(await page.locator('[data-testid^="entry-VOL-"]').count())===8);
    check(name,size.id,"clear search retains input focus",await search.evaluate(el=>document.activeElement===el));
    check(name,size.id,"no dynamic raw HTML injection",await page.locator(".atlas-l0-article script,.atlas-l0-article img,.atlas-l0-article iframe").count()===0);
    check(name,size.id,"browser runtime exceptions",exceptions.length===0,JSON.stringify(exceptions));
    check(name,size.id,"offline-only app resource calls",remote.length===0,JSON.stringify(remote));
    // Reject unauthenticated local UI. Real auth must still be enforced by the host.
    await page.goto(base+"/demo.html?blocked=1");
    await page.waitForSelector('[data-atlas-state="BLOCKED"]',{timeout:20000});
    check(name,size.id,"blocked flag does not render raw narratives",await page.locator(".atlas-l0-text").count()===0);
   }catch(e){check(name,size.id,"scenario exception",false,e.stack?.slice(0,900));}
   await ctx.close();
  }
 }finally{await browser.close();}
}
async function overflow(page,name,size,phase){
 const m=await page.evaluate(()=>({w:innerWidth,html:document.documentElement.scrollWidth,body:document.body.scrollWidth}));
 check(name,size,phase+" responsive width",m.html<=m.w+1&&m.body<=m.w+1,JSON.stringify(m));
}
async function screenshot(page,name,size,stage){
 const folder=path.join(OUT,name);fs.mkdirSync(folder,{recursive:true});
 const file=path.join(folder,size+"-"+stage+".png");await page.screenshot({path:file,fullPage:true,animations:"disabled"});
 shots.push(path.relative(ROOT,file));
}
(async()=>{
 try{
  await new Promise((resolve,reject)=>{server.once("error",reject);server.listen(0,"127.0.0.1",resolve)});
  const base="http://127.0.0.1:"+server.address().port;
  await verifyBrowser("chromium",chromium,base);
  await verifyBrowser("webkit",webkit,base);
 }catch(e){check("harness","all","fatal",false,e.stack);}
 finally{await new Promise(resolve=>server.close(resolve));}
 const report={
  schema:"ATLAS_V431_REACT_PRIVATE_INTEGRATION_BROWSER_TEST",version:"V4.31",
  status:errors.length?"FAIL":"PASS",checks:rows.length,passed:rows.length-errors.length,failed:errors.length,
  engines:["chromium","webkit"],widths:[1440,375,320],
  pinnedGitBlobs:PINNED,screenshots:shots,failures:errors,
  browserFixture:"React component importing genuine V4.29 JSON with V4.30 source bridge",
  actualAIStudioProjectInspected:false,actualAIStudioModified:false,actualAIStudioStagingTested:false,
  hostAuthenticationTested:false,historianApproved:false,actualReadersTested:0,canShip:false
 };
 fs.writeFileSync(path.join(OUT,"V431_REACT_BROWSER_RESULTS.json"),JSON.stringify(report,null,2)+"\n");
 console.log(JSON.stringify(report,null,2));if(report.failed)process.exitCode=1;
})();
