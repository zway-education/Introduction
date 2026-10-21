// node tools/rec.mjs 影格資料夾 起秒 迄秒（需要 http://localhost:8767）
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const [out,a,b]=process.argv.slice(2); const FPS=30, N0=Math.round(+a*FPS), N1=Math.round(+b*FPS);
fs.mkdirSync(out,{recursive:true});
const br=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const pg=await br.newPage({viewport:{width:1080,height:1920}});
await pg.goto('http://localhost:8767/promo60.html?rec=1');
await pg.waitForFunction('window.__ready===true',null,{timeout:120000});
fs.writeFileSync(out+'/../pencil.json',JSON.stringify(await pg.evaluate(()=>window.__PENCIL)));
// 從頭跑一遍到起點，讓「只畫一次」的元素狀態一致
for(let i=N0;i<N1;i++){ await pg.evaluate(t=>window.__render(t),i/FPS); await pg.screenshot({path:`${out}/f_${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:94}); if(i%150===0) console.log(i); }
await br.close();
