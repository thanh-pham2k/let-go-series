const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const folder=__dirname,html=fs.readFileSync(path.join(folder,'preview.html'),'utf8'),elements={};
function el(){return{children:[],style:{},handlers:{},append(x){this.children.push(x)},replaceChildren(){this.children=[]},pause(){},addEventListener(k,f){this.handlers[k]=f}}}
const document={getElementById(id){return elements[id]??=el()},createElement(){return el()}};
const context={document};vm.createContext(context);vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
const pages=vm.runInContext('pages',context);assert.equal(pages.length,2);
for(let i=0;i<2;i++){
 vm.runInContext(`show(${i})`,context);const p=pages[i];assert.equal(elements.practice.style.display,'none');assert.equal(elements.choices.children.length,3);
 assert.equal(elements['lesson-image'].src,p.output.webp);assert.equal(elements.audio.src,p.audio_file);
 for(const file of [p.output.webp,p.audio_file])assert(fs.existsSync(path.join(folder,file)));
 elements.audio.handlers.ended();assert.equal(elements.practice.style.display,'block');
 const j=p.question.choices.findIndex(c=>c.id===p.question.correct_choice_id);elements.choices.children[j].onclick();assert.equal(elements.result.textContent,'Đúng rồi!');
 elements.choices.children[(j+1)%3].onclick();assert(elements.result.textContent.includes('Chưa đúng'));
 vm.runInContext(`show(${i})`,context);elements.review.onclick();assert.equal(elements.practice.style.display,'block');
}
vm.runInContext('show(0)',context);assert(elements.previous.disabled);elements.next.onclick();assert.equal(elements.tracks.value,1);assert(elements.next.disabled);elements.previous.onclick();assert.equal(elements.tracks.value,0);
const report={result:'pass',tracks:pages.map(p=>p.track),checks:['Actual preview JS executed','Initial quiz hidden','Audio-ended and manual review reveal one quiz','Correct/incorrect feedback','Navigation/select logic','Local image/audio paths exist'],limitation:'DOM harness, not independent audio listening or browser layout audit'};
fs.writeFileSync(path.join(folder,'preview-validation.json'),JSON.stringify(report,null,2));console.log('PASS preview JS2 tracks,quiz reveal/feedback/navigation/resource paths');
