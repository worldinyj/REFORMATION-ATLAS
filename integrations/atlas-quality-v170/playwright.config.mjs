import {defineConfig,devices} from '@playwright/test';
export default defineConfig({
 testDir:'./tests',timeout:45000,retries:0,workers:2,
 reporter:[['list'],['html',{outputFolder:'playwright-report',open:'never'}],['junit',{outputFile:'test-results/junit.xml'}]],
 use:{baseURL:'http://127.0.0.1:8765',trace:'retain-on-failure',screenshot:'only-on-failure'},
 projects:[
  {name:'mobile-320',use:{...devices['Desktop Chrome'],viewport:{width:320,height:700}}},
  {name:'mobile-375',use:{...devices['iPhone 12'],browserName:'chromium'}},
  {name:'tablet-768',use:{...devices['Desktop Chrome'],viewport:{width:768,height:1024}}},
  {name:'desktop-1440',use:{...devices['Desktop Chrome'],viewport:{width:1440,height:900}}}
 ],
 webServer:{command:'cd ../.. && python3 -m http.server 8765 --bind 127.0.0.1',url:'http://127.0.0.1:8765/integrations/atlas-explorer-v168/',reuseExistingServer:false,timeout:30000}
});