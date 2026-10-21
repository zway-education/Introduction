// node tools/shot.mjs 輸出資料夾 秒數1 秒數2 ...  （需要 http://localhost:8767）
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [out,...ts]=process.argv.slice(2); const PAGE=process.env.PAGE||'promo60';
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const pg=await b.newPage({viewport:{width:1080,height:1920}});
pg.on('pageerror',e=>console.log('ERR',e.message)); pg.on('console',m=>{if(m.type()==='error')console.log('CON',m.text())});
await pg.goto('http://localhost:8767/'+PAGE+'.html?rec=1'+(process.env.QS||''));
await pg.waitForFunction('window.__ready===true',null,{timeout:120000});
for(const t of ts){ await pg.evaluate(t=>window.__render(t),+t); await pg.screenshot({path:`${out}/t_${(+t).toFixed(2).padStart(6,'0')}.jpg`,type:'jpeg',quality:90}); }
await b.close();
