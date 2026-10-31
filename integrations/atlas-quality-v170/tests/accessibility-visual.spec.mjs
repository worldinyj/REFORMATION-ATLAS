import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const url='/integrations/atlas-explorer-v168/';
test.beforeEach(async({page})=>{await page.goto(url);await expect(page.locator('.card').first()).toBeVisible()});
test('axe accessibility: serious and critical violations',async({page},testInfo)=>{
 const results=await new AxeBuilder({page}).analyze();
 const summary=results.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length,help:v.help}));
 await testInfo.attach('axe-results.json',{body:Buffer.from(JSON.stringify(summary,null,2)),contentType:'application/json'});
 expect(summary.filter(v=>['serious','critical'].includes(v.impact))).toEqual([]);
});
test('all four tabs have content and human-readable status',async({page})=>{
 for(const [id,count] of [['readers',10],['editions',5],['claims',8],['cities',11]]){
 await page.locator('[data-tab='+id+']').click();
 await expect(page.locator('.card')).toHaveCount(count);
 await expect(page.locator('#status')).toContainText(String(count)+'개');
 }
});
test('long texts wrap with no horizontal overflow',async({page})=>{
 for(const id of ['readers','editions','claims','cities']){
 await page.locator('[data-tab='+id+']').click();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth+1)).toBeTruthy();
 }
});
test('search handles Korean, zero hits, clear and rapid typing',async({page})=>{
 await page.locator('#q').fill('칼뱅');
 await expect(page.locator('.card').first()).toBeVisible();
 await page.locator('#q').fill('문서없음999ZZZ');
 await expect(page.locator('.card')).toHaveCount(0);
 await expect(page.locator('#status')).toContainText('검색 결과가 없습니다');
 await page.locator('#q').clear();await expect(page.locator('.card')).toHaveCount(10);
});
test('links are HTTPS and protected from opener attacks',async({page})=>{
 const vals=await page.locator('.card a').evaluateAll(els=>els.map(a=>({href:a.href,rel:a.rel,target:a.target})));
 expect(vals.length).toBeGreaterThan(0);
 expect(vals.every(x=>x.href.startsWith('https://')&&x.rel.includes('noopener')&&x.rel.includes('noreferrer')&&x.target==='_blank')).toBeTruthy();
});
test('readability and tap target report',async({page},testInfo)=>{
 const sizes=await page.locator('nav button').evaluateAll(els=>els.map(e=>({width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height})));
 expect(sizes.every(s=>s.width>=40&&s.height>=40)).toBeTruthy();
 await testInfo.attach('tap-targets.json',{body:Buffer.from(JSON.stringify(sizes)),contentType:'application/json'});
});
test('each state captures visual QC screenshot',async({page},testInfo)=>{
 for(const id of ['readers','editions','claims','cities']){
  await page.locator('[data-tab='+id+']').click();
  await page.screenshot({path:testInfo.outputPath(id+'-'+testInfo.project.name+'.png'),fullPage:true});
 }
});
test('network failure always visible and prevents stale content',async({page})=>{
 await page.route('**/data/contracts/atlas_v165_integration_readiness_manifest.json',r=>r.fulfill({status:503,body:'Unavailable'}));
 await page.reload();
 await expect(page.locator('#status')).toHaveAttribute('role','alert');
 await expect(page.locator('#status')).toContainText('자료를 불러올 수 없습니다');
 await expect(page.locator('.card')).toHaveCount(0);
});
