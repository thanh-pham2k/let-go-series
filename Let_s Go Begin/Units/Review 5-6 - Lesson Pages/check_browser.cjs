const {chromium}=require('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname),profile=path.resolve(root,'assets/browser-check-profile');
assert(profile.startsWith(root+path.sep));
(async()=>{
 let browser;
 try{
  browser=await chromium.launchPersistentContext(profile,{executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,viewport:{width:1280,height:1000}});
  const page=await browser.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const response=await page.goto('http://127.0.0.1:8765/preview.html');assert.equal(response.status(),200);
  const manifest=JSON.parse(fs.readFileSync(root+'/manifest.json','utf8'));
  const results=[];
  for(let i=0;i<manifest.items.length;i++){
   const item=manifest.items[i];await page.selectOption('#tracks',String(i));
   await page.waitForFunction(()=>document.getElementById('lesson-image').complete&&document.getElementById('lesson-image').naturalWidth===1200&&Number.isFinite(document.getElementById('audio').duration)&&document.getElementById('audio').duration>0,{},{timeout:30000});
   assert.equal(await page.locator('#practice').isVisible(),false);
   const media=await page.evaluate(()=>({image:document.getElementById('lesson-image').getAttribute('src'),audio:document.getElementById('audio').getAttribute('src'),duration:document.getElementById('audio').duration}));
   assert.equal(media.image,item.output.webp);assert.equal(media.audio,item.audio_file);
   await page.screenshot({path:root+'/assets/browser-'+item.track+'.png',fullPage:true});
   await page.locator('#review').click();assert.equal(await page.locator('#practice').isVisible(),true);
   assert.equal(await page.locator('#choices button').count(),3);
   const wrong=item.question.choices.findIndex(c=>c.id!==item.question.correct_choice_id);
   await page.locator('#choices button').nth(wrong).click();assert.equal(await page.locator('#result').textContent(),'Chưa đúng, bé thử lại nhé.');
   const correct=item.question.choices.findIndex(c=>c.id===item.question.correct_choice_id);
   await page.locator('#choices button').nth(correct).click();assert.equal(await page.locator('#result').textContent(),'Đúng rồi!');
   await page.selectOption('#tracks',String(1-i));await page.selectOption('#tracks',String(i));
   assert.equal(await page.locator('#practice').isVisible(),false);
   await page.evaluate(()=>document.getElementById('audio').dispatchEvent(new Event('ended')));
   assert.equal(await page.locator('#practice').isVisible(),true);
   for(const asset of [item.output.png,item.output.webp,item.audio_file]){const r=await page.request.get('http://127.0.0.1:8765/'+asset);assert.equal(r.status(),200);}
   results.push({track:item.track,...media,image_size:[1200,1200],manual_review:'pass',synthetic_ended:'pass',answer_feedback:'pass',http_assets:'200'});
  }
  await page.selectOption('#tracks','0');assert(await page.locator('#previous').isDisabled());await page.locator('#next').click();assert.equal(await page.locator('#tracks').inputValue(),'1');assert(await page.locator('#next').isDisabled());await page.locator('#previous').click();assert.equal(await page.locator('#tracks').inputValue(),'0');
  assert.deepEqual(errors,[]);
  fs.writeFileSync(root+'/browser.checks.json',JSON.stringify({result:'pass',browser:'Headless installed Google Chrome via bundled Playwright',item_count:2,checks:results,navigation:'pass',page_errors:errors,limitation:'MP3 metadata loaded; audio ended event simulated for UI check. No independent listening/transcription.'},null,2));
  console.log('Browser PASS: 2 images decoded, 2 MP3 durations loaded, all asset HTTP200, quiz/manual+ended/feedback/reset/navigation, no page errors.');
 }finally{
  if(browser)await browser.close();
  const target=path.resolve(profile);assert(target.startsWith(root+path.sep)&&target===profile);
  fs.rmSync(target,{recursive:true,force:true});
 }
})().catch(e=>{console.error(e);process.exitCode=1});
