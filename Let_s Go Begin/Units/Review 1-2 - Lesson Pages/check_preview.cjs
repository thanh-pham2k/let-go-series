const { chromium }=require('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),assert=require('assert');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1100,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8766/preview.html');
 assert.equal(await page.locator('#tracks option').count(),2);
 for(let i=0;i<2;i++){
  await page.selectOption('#tracks',String(i));
  await page.waitForFunction(()=>document.querySelector('#lesson-image').complete&&document.querySelector('#lesson-image').naturalWidth===1200);
  assert.equal(await page.locator('#practice').isVisible(),false);
  assert.equal(await page.locator('#result').textContent(),'');
  await page.click('#review');assert.equal(await page.locator('#practice').isVisible(),true);
  assert.equal(await page.locator('#choices button').count(),3);
  const correct=i===0?0:1;await page.locator('#choices button').nth((correct+1)%3).click();assert.match(await page.locator('#result').textContent(),/Chưa đúng/);
  await page.locator('#choices button').nth(correct).click();assert.match(await page.locator('#result').textContent(),/Đúng rồi/);
  await page.selectOption('#tracks',String(i));
  await page.waitForFunction(()=>Number.isFinite(document.querySelector('#audio').duration)&&document.querySelector('#audio').duration>0);
  await page.evaluate(async()=>{const a=document.querySelector('#audio');a.muted=true;await a.play();a.currentTime=a.duration-.3;});
  await page.waitForFunction(()=>document.querySelector('#audio').ended,{},{timeout:15000});
  assert.equal(await page.locator('#practice').isVisible(),true);assert.equal(await page.locator('#result').textContent(),'');
 }
 await page.click('#previous');assert.equal(await page.locator('#tracks').inputValue(),'0');assert.equal(await page.locator('#practice').isVisible(),false);
 await page.click('#next');assert.equal(await page.locator('#tracks').inputValue(),'1');
 await page.screenshot({path:'preview-browser.png',fullPage:true});assert.deepEqual(errors,[]);
 fs.writeFileSync('runtime-check.json',JSON.stringify({result:'pass',browser:'Chrome headless via bundled Playwright',checks:['two tracks selectable','both WebP load at natural width1200','MP3 metadata decodes both tracks','questions initially hidden','review button reveals one question/three choices','incorrect and correct feedback only after choice','actual muted playback seek to end reveals question on ended for both tracks','switch resets question/feedback','previous/next work','no JavaScript errors'],limitation:'Playback used only to verify browser ended event; speech not listened/transcribed.'},null,2));
 await browser.close();console.log('Preview runtime PASS for both tracks.');
})().catch(e=>{console.error(e);process.exit(1)});
