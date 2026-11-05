/** Real Chromium screen checks, against a loopback-only server. No production app writes. */
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile, mkdir, writeFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import {resolve, extname, sep} from 'node:path';
import {fileURLToPath} from 'node:url';
import {tmpdir} from 'node:os';
const require=createRequire(import.meta.url);
let playwright;
for(const candidate of [process.env.ATLAS_PLAYWRIGHT_MODULE,'playwright',process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright':null].filter(Boolean)){
 try{playwright=require(candidate);break;}catch{}
}
if(!playwright)throw Error('Playwright is required. See README; no browser checks were run.');
const root=resolve(fileURLToPath(new URL('../../',import.meta.url)));
const artifactDir=process.env.ATLAS_UI_ARTIFACT_DIR??resolve(tmpdir(),'atlas-v299-browser-review');
await mkdir(artifactDir,{recursive:true});
const mime={'.html':'text/html; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8'};
const server=createServer(async(req,res)=>{
 try{
  let path=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(path.endsWith('/'))path+='index.html';
  const file=resolve(root,'.'+path);if(!file.startsWith(root+sep))throw Error('outside root');
  const content=await readFile(file);res.writeHead(200,{'Content-Type':mime[extname(file)]??'application/octet-stream'});res.end(content);
 }catch{res.writeHead(404);res.end('Not found');}
});
await new Promise(done=>server.listen(0,'127.0.0.1',done));
const url=`http://127.0.0.1:${server.address().port}/integrations/medium-atlas-v299/`;
let browser;const results=[];
async function check(name,fn){await fn();results.push({name,result:'PASS'});console.log('PASS',name);}
try{
 browser=await playwright.chromium.launch({headless:true,args:['--no-sandbox']});
 for(const width of [320,375,1440]){
  const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await check(`${width}: load all readers`,async()=>{await page.goto(url);await page.getByRole('status').filter({hasText:'전체 435편 중 435편'}).waitFor();assert.equal(await page.locator('.reader-card').count(),12);});
  await check(`${width}: keyboard skip preserves navigation`,async()=>{const prior=page.url();await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.classList.contains('skip')),true);await page.keyboard.press('Enter');assert.equal(await page.evaluate(()=>document.activeElement.id),'results');assert.equal(page.url(),prior);});
  await check(`${width}: Korean spaced search`,async()=>{await page.getByLabel('무엇이 궁금한가요?').fill('카를 5세');await page.getByRole('button',{name:'찾기',exact:true}).click();await page.locator('.reader-card[data-reader="MEDIUM-LUTHER1521"]').waitFor();});
  await check(`${width}: detail and focus`,async()=>{await page.locator('.reader-card[data-reader="MEDIUM-LUTHER1521"]').click();assert.match(await page.locator('#detail h2').textContent(),/1521년 보름스/);assert.equal(await page.evaluate(()=>document.activeElement===document.querySelector('#detail h2')),true);assert.equal(await page.locator('#detail .prose').count(),3);await page.getByRole('heading',{name:'생각해 볼 질문'}).waitFor();});
  await check(`${width}: distinct source state`,async()=>{await page.locator('#detail').getByText(/이번 확인에서 접근 실패/).first().waitFor();await page.getByRole('heading',{name:'출처를 읽는 안내'}).waitFor();});
  await check(`${width}: evidence keyboard toggle`,async()=>{const summary=page.getByText('선택한 주장과 확인 범위 보기',{exact:true});await summary.focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#detail details').evaluate(el=>el.open),true);assert.equal(await page.locator('#detail .claim').count(),2);});
  await check(`${width}: responsive content overflow`,async()=>{assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),true);await page.locator('#detail').screenshot({path:resolve(artifactDir,`detail-${width}.png`)});});
  await check(`${width}: related link and browser back`,async()=>{const linkedPage=await context.newPage();linkedPage.on('pageerror',e=>errors.push(e.message));await linkedPage.goto(url+'#reader=PERSON-HANS_TAUSEN');await linkedPage.locator('#detail .related button').first().waitFor();const related=linkedPage.locator('#detail .related button').first();const id=await related.getAttribute('data-reader');await related.click();assert.equal(new URLSearchParams(new URL(linkedPage.url()).hash.slice(1)).get('reader'),id);await linkedPage.goBack();await linkedPage.waitForFunction(()=>new URLSearchParams(location.hash.slice(1)).get('reader')==='PERSON-HANS_TAUSEN');await linkedPage.locator('#detail h2').filter({hasText:'한스 타우센'}).waitFor();await linkedPage.close();});
  await check(`${width}: reload keeps query and reader`,async()=>{await page.reload();await page.getByRole('heading',{name:/1521년 보름스/}).waitFor();assert.equal(await page.getByLabel('무엇이 궁금한가요?').inputValue(),'카를 5세');});
  await check(`${width}: empty search`,async()=>{await page.getByLabel('무엇이 궁금한가요?').fill('존재하지않는검색어XYZ');await page.getByRole('button',{name:'찾기',exact:true}).click();await page.getByText('조건에 맞는 해설이 없습니다.',{exact:false}).waitFor();assert.equal(await page.locator('.reader-card').count(),0);});
  await check(`${width}: path and type filter`,async()=>{await page.getByLabel('무엇이 궁금한가요?').fill('');await page.getByRole('button',{name:'찾기',exact:true}).click();await page.getByLabel('함께 읽는 경로').selectOption('REGION-NORDIC');assert.equal(await page.locator('.reader-card').count(),8);await page.getByLabel('분야',{exact:true}).selectOption('PERSON');assert.equal(await page.locator('.reader-card').count(),1);});
  await check(`${width}: pagination`,async()=>{await page.getByLabel('함께 읽는 경로').selectOption('');await page.getByLabel('분야',{exact:true}).selectOption('');await page.getByRole('button',{name:'다음',exact:true}).click();await page.getByRole('status').filter({hasText:'2/37페이지'}).waitFor();assert.equal(await page.locator('.reader-card').count(),12);});
  await check(`${width}: unknown ID is a readable state`,async()=>{await page.goto(url+'#reader=unknown');await page.getByRole('heading',{name:'해설을 찾을 수 없습니다'}).waitFor();});
  await check(`${width}: no runtime errors`,async()=>assert.deepEqual(errors,[]));
  await context.close();
 }
 for(const mode of ['missing','hash-drift']){
  const context=await browser.newContext();const page=await context.newPage();
  await check(`invalid delivery: ${mode}`,async()=>{
   await page.route('**/atlas_v297_source_checked_medium_content_delivery_bundle.json',route=>mode==='missing'?route.fulfill({status:404,body:'missing'}):route.fulfill({status:200,contentType:'application/json',body:'{}'}));
   await page.goto(url);await page.getByRole('button',{name:'다시 불러오기'}).waitFor();assert.equal(await page.locator('.reader-card').count(),0);assert.equal(await page.locator('#load-error').isVisible(),true);
  });await context.close();
 }
 await writeFile(resolve(artifactDir,'results.json'),JSON.stringify({scope:'ISOLATED_REVIEW_UI_NOT_ACTUAL_AI_STUDIO',viewports:[320,375,1440],checks:results.length,results},null,2)+'\n');
 console.log(JSON.stringify({checks:results.length,viewports:[320,375,1440],artifacts:artifactDir,result:'PASS'}));
}finally{if(browser)await browser.close();await new Promise(done=>server.close(done));}
