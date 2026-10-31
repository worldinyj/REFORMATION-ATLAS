import {test,expect} from '@playwright/test';
const path='/integrations/atlas-explorer-v168/';
test('keyboard navigation controls stay reachable',async({page})=>{
 await page.goto(path);await page.keyboard.press('Tab');const count=await page.locator('nav button').count();expect(count).toBe(4);
 for(const b of await page.locator('nav button').all())await expect(b).toBeVisible();
});
test('mobile buttons and search minimum sizes',async({page})=>{
 await page.goto(path);for(const b of await page.locator('nav button').all()){
  const box=await b.boundingBox();expect(box?.height??0).toBeGreaterThanOrEqual(40);
 }
 const search=await page.locator('#q').boundingBox();expect(search?.width??0).toBeGreaterThan(200);
});
test('server failure shows user-facing error and no cards',async({page})=>{
 await page.route('**/data/contracts/atlas_v165_integration_readiness_manifest.json',r=>r.fulfill({status:503,body:'Unavailable'}));
 await page.goto(path);
 await expect(page.locator('#status')).toContainText('자료를 불러올 수 없습니다');
 await expect(page.locator('#status')).toHaveAttribute('role','alert');
 await expect(page.locator('.card')).toHaveCount(0);
});
test('source links have http protocol, no javascript URLs',async({page})=>{
 await page.goto(path);await expect(page.locator('.card').first()).toBeVisible();
 const links=await page.locator('.card a').evaluateAll(nodes=>nodes.map(x=>x.href));
 expect(links.length).toBeGreaterThan(0);
 for(const href of links)expect(href.startsWith('https://')).toBeTruthy();
});
test('viewport resize and tab cycles preserve cards',async({page})=>{
 await page.goto(path);await page.setViewportSize({width:320,height:700});
 await page.locator('[data-tab=cities]').click();await expect(page.locator('.card')).toHaveCount(11);
 await page.setViewportSize({width:1440,height:900});await expect(page.locator('.card')).toHaveCount(11);
});
