import {test,expect} from '@playwright/test';
const path='/integrations/atlas-explorer-v168/';
test.beforeEach(async({page})=>{await page.goto(path);await expect(page.locator('#status')).not.toContainText('로딩 중');});
test('four tabs and accurate item counts',async({page})=>{
 for(const [tab,count] of [['readers',10],['editions',5],['claims',8],['cities',11]]){
  await page.locator('[data-tab="'+tab+'"]').click();
  await expect(page.locator('[data-tab="'+tab+'"]')).toHaveAttribute('aria-selected','true');
  await expect(page.locator('.card')).toHaveCount(count);
 }
});
test('Korean search and empty result recovery',async({page})=>{
 await page.locator('#q').fill('후스');
 await expect(page.locator('.card')).toHaveCount(2);
 await page.locator('#q').fill('없는검색어98765');
 await expect(page.locator('.card')).toHaveCount(0);
 await expect(page.locator('#status')).toContainText('검색 결과가 없습니다');
 await page.locator('#q').fill('');
 await expect(page.locator('.card')).toHaveCount(10);
});
test('sources safe and no horizontal overflow',async({page})=>{
 const links=page.locator('.card a');
 await expect(links.first()).toHaveAttribute('rel',/noopener noreferrer/);
 await expect(links.first()).toHaveAttribute('target','_blank');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1)).toBeTruthy();
 for(const tab of ['editions','claims','cities']){
  await page.locator('[data-tab="'+tab+'"]').click();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1)).toBeTruthy();
 }
});
test('a11y controls & typography and no image embeds',async({page})=>{
 await expect(page.locator('html')).toHaveAttribute('lang','ko');
 await expect(page.locator('#status')).toHaveAttribute('role','status');
 await expect(page.locator('nav button')).toHaveCount(4);
 await expect(page.locator('img, iframe')).toHaveCount(0);
 await expect(page.locator('input[type=search]')).toHaveCount(1);
});
test('blocked public access notice and immutable research state',async({page})=>{
 await expect(page.locator('.warning')).toContainText('공개 불가');
 await expect(page.locator('.warning')).toContainText('원본 판면');
});
test('screenshot baseline artifacts for human QC',async({page},testInfo)=>{
 await page.screenshot({path:testInfo.outputPath('overview-'+testInfo.project.name+'.png'),fullPage:true});
});
