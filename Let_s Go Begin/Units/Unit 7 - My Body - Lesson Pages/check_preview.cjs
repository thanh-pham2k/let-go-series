const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=__dirname;
const html=fs.readFileSync(path.join(root,'preview.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements={};
function el(){return {children:[],style:{},disabled:false,textContent:'',value:0,src:'',append(e){this.children.push(e)},replaceChildren(){this.children=[]},pause(){},addEventListener(name,f){this[name]=f}}}
const document={getElementById(id){return elements[id]??=el()},createElement:el};
const ctx={document};vm.createContext(ctx);vm.runInContext(script,ctx);
const m=JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
assert.equal(elements.tracks.children.length,17);
for(let i=0;i<17;i++){
 elements.tracks.value=i;elements.tracks.onchange();
 assert.equal(elements['lesson-image'].src,m.items[i].output.webp);
 assert.equal(elements.audio.src,m.items[i].audio_file);
 assert.equal(elements.practice.style.display,'none');
 assert.equal(elements.review.disabled,true);
 for(const p of [elements['lesson-image'].src,elements.audio.src])assert(fs.existsSync(path.join(root,p)));
 elements.audio.ended();
 assert.equal(elements.practice.style.display,'block');assert.equal(elements.review.disabled,false);
 assert.equal(elements.choices.children.length,3);
 const q=m.items[i].question,good=q.choices.findIndex(c=>c.id===q.correct_choice_id);
 elements.choices.children[(good+1)%3].onclick();assert(elements.result.textContent.startsWith('Chưa đúng'));
 elements.choices.children[good].onclick();assert.equal(elements.result.textContent,'Đúng rồi!');
}
const result={result:'pass',tracks:17,checks:['All image/audio paths exist','Practice hidden until audio ended','Track changes reset practice','Three choices and valid correct/wrong feedback'],limitation:'DOM harness; does not decode/play audio or visually render browser.'};
fs.writeFileSync(path.join(root,'preview-validation.json'),JSON.stringify(result,null,2));
console.log('PASS preview logic: 17 tracks, audio gating, choice feedback, local links.');

