const fs=require('fs'),path=require('path'),assert=require('assert'),{spawn}=require('child_process');
const F=__dirname,profile=path.join(F,'.browser-check');
const proc=spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',['--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--disable-extensions','--remote-debugging-port=9336','--user-data-dir='+profile,'http://127.0.0.1:8766/preview.html'],{windowsHide:true,stdio:'ignore'});
(async()=>{
 let targets;
 for(let i=0;i<100;i++){try{targets=await(await fetch('http://127.0.0.1:9336/json/list')).json();if(targets.some(t=>t.url.includes('8766/preview.html')))break}catch{}await new Promise(r=>setTimeout(r,200))}
 const target=targets?.find(t=>t.url.includes('8766/preview.html'));assert(target,'Headless preview target not available');
 const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});let next=0;const pending=new Map();
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});assert(!r.exceptionDetails,JSON.stringify(r.exceptionDetails));return r.result.value};
 await send('Emulation.setDeviceMetricsOverride',{width:1200,height:1400,deviceScaleFactor:1,mobile:false});
 await send('Page.navigate',{url:'http://127.0.0.1:8766/preview.html'});
 for(let i=0;i<100;i++){try{if(await evaluate('typeof show === \"function\"'))break}catch{}await new Promise(r=>setTimeout(r,100))}
 await evaluate('new Promise(resolve=>{if(document.readyState==="complete")resolve();else window.addEventListener("load",resolve,{once:true})})');
 const checks=[];
 for(let i=0;i<2;i++){
  await evaluate(`show(${i})`);
  const state=await evaluate('new Promise(resolve=>{const im=document.getElementById("lesson-image"),a=document.getElementById("audio");const done=()=>resolve({imageWidth:im.naturalWidth,imageHeight:im.naturalHeight,imageLoaded:im.complete,audioReady:a.readyState,audioDuration:a.duration,practice:getComputedStyle(document.getElementById("practice")).display,choices:document.querySelectorAll("#choices button").length});function ready(){if(im.complete&&a.readyState>=1)done();else setTimeout(ready,100)}ready()})');
  assert.equal(state.imageWidth,1200);assert.equal(state.imageHeight,1200);assert.equal(state.practice,'none');assert.equal(state.choices,3);assert(state.audioDuration>0);
  await evaluate('document.getElementById("audio").dispatchEvent(new Event("ended"))');assert.equal(await evaluate('getComputedStyle(document.getElementById("practice")).display'),'block');
  const correct=await evaluate('pages[current].question.choices.findIndex(c=>c.id===pages[current].question.correct_choice_id)');
  await evaluate(`document.querySelectorAll('#choices button')[${correct}].click()`);assert.equal(await evaluate('document.getElementById("result").textContent'),'Đúng rồi!');
  await evaluate(`document.querySelectorAll('#choices button')[${(correct+1)%3}].click()`);assert((await evaluate('document.getElementById("result").textContent')).includes('Chưa đúng'));
  await evaluate(`document.querySelectorAll('#choices button')[${correct}].click()`);
  const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true});fs.writeFileSync(path.join(F,`preview-browser-${i+1}.png`),Buffer.from(shot.data,'base64'));
  checks.push({track:await evaluate('pages[current].track'),...state,result:'pass'});
 }
 await evaluate('show(0);document.getElementById("next").click()');assert.equal(await evaluate('current'),1);assert(await evaluate('document.getElementById("next").disabled'));
 await evaluate('document.getElementById("previous").click()');assert.equal(await evaluate('current'),0);
 await evaluate('document.getElementById("tracks").value="1";document.getElementById("tracks").dispatchEvent(new Event("change"))');assert.equal(await evaluate('current'),1);
 await evaluate('document.getElementById("review").click()');assert.equal(await evaluate('getComputedStyle(document.getElementById("practice")).display'),'block');
 fs.writeFileSync(path.join(F,'browser-validation.json'),JSON.stringify({result:'pass',browser:'Headless Microsoft Edge',checks,navigation:'pass',manual_review:'pass',limitation:'Audio decode/duration checked; audio not independently listened/transcribed. ended event simulated for UI test.'},null,2));
 await send('Browser.close').catch(()=>{});ws.close();console.log('PASS real browser:2 images1200x1200,audio metadata decode,quiz visibility/feedback,navigation,selector,screenshots.');
})().catch(e=>{console.error(e);proc.kill();process.exitCode=1});
