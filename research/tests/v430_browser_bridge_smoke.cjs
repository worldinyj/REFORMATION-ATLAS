#!/usr/bin/env node
"use strict";
// Browser integration proof: local-only V4.30 adapter + real V4.29 JSON.
// Neither Google AI Studio nor deployed public hosting is exercised here.
const fs=require("node:fs");
const http=require("node:http");
const path=require("node:path");
const {execFileSync}=require("node:child_process");
const {chromium,webkit}=require("playwright");

const ROOT=path.resolve(__dirname,"../..");
const OUT=path.join(ROOT,"research/artifacts/V430_browser_bridge");
const PAGES=[
  "integrations/atlas-l0-v430/local-smoke.html",
  "integrations/atlas-l0-v430/bridge.mjs",
  "handoff/V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json"
];
const HASHES={
  "integrations/atlas-l0-v430/local-smoke.html":"14aa2c71503e4a987f08ca6d9896495f73b4c888",
  "integrations/atlas-l0-v430/bridge.mjs":"1f585f31cf10e05530662e05c228de3519ef8632",
  "handoff/V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json":"64c27c0dfe05394acbb049807e4c4384d58908b9"
};
const checks=[],failures=[],screenshots=[];
fs.mkdirSync(OUT,{recursive:true});
for(const rel of PAGES){
 const sha=execFileSync("git",["hash-object",path.join(ROOT,rel)],{encoding:"utf8"}).trim();
 if(sha!==HASHES[rel])throw Error("Source blob mismatch: "+rel+" / "+sha);
}
const mime={".html":"text/html; charset=utf-8",".mjs":"text/javascript; charset=utf-8",".json":"application/json; charset=utf-8"};
const authorized=new Set(PAGES.map(x=>"/"+x));
const server=http.createServer((req,res)=>{
 const pathname=new URL(req.url,"http://127.0.0.1").pathname;
 if(!authorized.has(pathname)){res.writeHead(404);res.end("Not found");return;}
 const relative=pathname.slice(1),filename=path.join(ROOT,relative);
 res.writeHead(200,{"Content-Type":mime[path.extname(filename)],"Cache-Control":"no-store","X-Content-Type-Options":"nosniff"});
 fs.createReadStream(filename).pipe(res);
});
function record(engine,device,name,passed,detail=""){
 const o={engine,device,name,status:passed?"PASS":"FAIL",detail:String(detail)};
 checks.push(o);if(!passed)failures.push(o);
}
function viewMetric(page){return page.evaluate(()=>({
 viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,bodyWidth:document.body.scrollWidth
}));}
async function noOverflow(page,engine,device,stage){
 const x=await viewMetric(page),ok=x.documentWidth<=x.viewport+1&&x.bodyWidth<=x.viewport+1;
 record(engine,device,stage+" horizontal layout",ok,JSON.stringify(x));
}
async function screenshot(page,engine,device,stage){
 const dir=path.join(OUT,engine);fs.mkdirSync(dir,{recursive:true});
 const file=path.join(dir,device+"-"+stage+".png");
 await page.screenshot({path:file,fullPage:true,animations:"disabled"});
 screenshots.push(path.relative(ROOT,file));
}
async function run(){
 await new Promise((resolve,reject)=>{server.once("error",reject);server.listen(0,"127.0.0.1",resolve)});
 const port=server.address().port,url="http://127.0.0.1:"+port+"/"+PAGES[0];
 const devices=[{name:"desktop",width:1440,height:900},{name:"mobile",width:375,height:812},{name:"small",width:320,height:700}];
 try{
 for(const [engine,loader] of [["chromium",chromium],["webkit",webkit]]){
  const browser=await loader.launch({headless:true});
  try{
  for(const d of devices){
   const context=await browser.newContext({viewport:{width:d.width,height:d.height},locale:"ko-KR",reducedMotion:"reduce"});
   const page=await context.newPage(),pageErrors=[],remote=[];
   page.on("pageerror",e=>pageErrors.push(e.message));
   page.on("request",req=>{if(!req.url().startsWith("http://127.0.0.1:"+port+"/"))remote.push(req.url())});
   try{
    await page.goto(url,{waitUntil:"load"});
    await page.waitForFunction(()=>document.querySelector("#state")?.dataset.status==="READY",{timeout:15000});
    record(engine,d.name,"private local harness initialized",true,"actual ES module imported");
    record(engine,d.name,"8 source volumes listed",(await page.locator('button[data-record-kind="VOLUME"]').count())===8);
    await noOverflow(page,engine,d.name,"volume catalog");
    await screenshot(page,engine,d.name,"volume-catalog");
    await page.locator('button[data-record-id="VOL-03"]').click();
    record(engine,d.name,"volume opens full narrative",await page.locator("article pre").innerText().then(s=>s.includes("위클리프")&&s.length>400));
    await noOverflow(page,engine,d.name,"volume full text");
    await page.locator("#themes-tab").click();
    record(engine,d.name,"6 source themes listed",(await page.locator('button[data-record-kind="THEME"]').count())===6);
    await page.locator('button[data-record-id="T415-06"]').click();
    record(engine,d.name,"theme has seven active era links",(await page.locator("button[data-target-id]").count())===7);
    await page.locator('button[data-target-id="VOL-07"]').click();
    record(engine,d.name,"theme link resolves actual VOL-07",await page.locator("article pre").innerText().then(s=>s.includes("한국")&&s.length>400));
    await noOverflow(page,engine,d.name,"linked volume");
    await screenshot(page,engine,d.name,"linked-volume");
    await page.locator("#chapters-tab").click();
    record(engine,d.name,"6 intro chapters listed",(await page.locator('button[data-record-kind="CHAPTER"]').count())===6);
    await page.locator('button[data-record-id="INTRO-3"]').click();
    record(engine,d.name,"intro chapter opens real text",await page.locator("article pre").innerText().then(s=>s.length>100));
    await noOverflow(page,engine,d.name,"reader chapter");
    const input=page.locator("#search-box");
    await input.fill("후스");
    const hits=await page.locator("main .items button").count();
    record(engine,d.name,"Korean full-text lookup returns results",hits>0,"hits="+hits);
    await noOverflow(page,engine,d.name,"search results");
    await screenshot(page,engine,d.name,"search");
    await input.fill("");
    record(engine,d.name,"search clears without exceptions",await page.locator("#state").innerText().then(t=>t.includes("검색어 없음")));
    record(engine,d.name,"no JavaScript runtime errors",pageErrors.length===0,JSON.stringify(pageErrors));
    record(engine,d.name,"no remote HTTP requests",remote.length===0,JSON.stringify(remote));
   }catch(e){record(engine,d.name,"browser scenario exception",false,e.stack?.slice(0,1000)??String(e));}
   await context.close();
  }
  }finally{await browser.close();}
 }
 }finally{await new Promise(resolve=>server.close(resolve));}
}
(async()=>{
 try{await run();}
 catch(e){record("harness","all","fatal launch or HTTP error",false,e.stack??String(e));}
 const summary={
  version:"V4.30",schema:"ATLAS_PRIVATE_L0_BRIDGE_ACTUAL_BROWSER_INTEGRATION",
  status:failures.length?"FAIL":"PASS",
  engines:["chromium","webkit"],deviceWidths:[1440,375,320],
  unitOfTest:"isolated loopback fixture consuming actual V4.29 JSON via V4.30 module",
  checkedSourceBlobs:HASHES,
  tests:checks.length,passed:checks.length-failures.length,failed:failures.length,
  failures,screenshots,
  aiStudioAppModified:false,realAiStudioStageExecuted:false,publicDeployment:false,realHostAuthenticationVerified:false,
  realReaderPilots:0,realHistorianApprovals:0,canShip:false
 };
 fs.writeFileSync(path.join(OUT,"V430_BROWSER_BRIDGE_RESULTS.json"),JSON.stringify(summary,null,2)+"\n");
 console.log(JSON.stringify({...summary,allTestRows:undefined},null,2));
 if(failures.length)process.exitCode=1;
})();
