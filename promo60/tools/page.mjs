import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [file,out]=process.argv.slice(2);
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const pg=await b.newPage({viewport:{width:2000,height:1000}});
await pg.goto('file://'+file); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(500);
await pg.screenshot({path:out,fullPage:true,type:'jpeg',quality:88}); await b.close();
