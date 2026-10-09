const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const folder=__dirname,html=fs.readFileSync(path.join(folder,'preview.html'),'utf8');
const elements={};
function el(){return {children:[],style:{},handlers:{},append(x){this.children.push(x)},replaceChildren(){this.children=[]},pause(){},addEventListener(k,f){this.handlers[k]=f}}}
const document={getElementById(id){return elements[id]??=el()},createElement(){return el()}};
const ctx={document};vm.createContext(ctx);vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],ctx);
const pages=vm.runInContext('pages',ctx);assert.equal(pages.length,18);
for(let i=0;i<18;i++){
 vm.runInContext(`show(${i})`,ctx);const p=pages[i];
 assert.equal(elements.practice.style.display,'none');
 assert.equal(elements['lesson-image'].src,p.output.webp);assert.equal(elements.audio.src,p.audio_file);
 assert(fs.existsSync(path.join(folder,p.output.webp)));assert(fs.existsSync(path.join(folder,p.audio_file)));
 elements.audio.handlers.ended();assert.equal(elements.practice.style.display,'block');
 const c=p.question.choices.findIndex(x=>x.id===p.question.correct_choice_id);
 elements.choices.children[c].onclick();assert.equal(elements.result.textContent,'Đúng rồi!');
 elements.choices.children[(c+1)%3].onclick();assert(elements.result.textContent.includes('Chưa đúng'));
}
vm.runInContext('show(0)',ctx);assert(elements.previous.disabled);elements.next.onclick();assert.equal(elements.tracks.value,1);
vm.runInContext('show(17)',ctx);assert(elements.next.disabled);
console.log('PASS preview script:18 tracks,asset paths,audio-ended quiz reveal,correct/wrong feedback,navigation. Audio playback not independently listened.');
