const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(path.join(__dirname,'preview.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements={};
const ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
function el(){return {children:[],style:{},disabled:false,textContent:'',value:0,src:'',append(e){this.children.push(e)},replaceChildren(){this.children=[]},pause(){},addEventListener(name,f){this[name]=f}}}
const document={getElementById(id){assert(ids.has(id),'Actual HTML lacks id='+id);return elements[id]??=el()},createElement:el};
const ctx={document};vm.createContext(ctx);vm.runInContext(script,ctx);
const m=JSON.parse(fs.readFileSync(path.join(__dirname,'manifest.json'),'utf8'));
assert.equal(elements.tracks.children.length,3);
assert.equal(elements.previous.disabled,true);
for(let i=0;i<3;i++){
 elements.tracks.value=i;elements.tracks.onchange();
 const p=m.items[i];
 assert.equal(elements['lesson-image'].src,p.output.webp);
 assert.equal(elements.audio.src,p.audio_file);
 assert.equal(elements.practice.style.display,'none');
 assert.equal(elements.result.textContent,'');
 for(const f of [p.output.webp,p.audio_file])assert(fs.existsSync(path.join(__dirname,f)));
 elements.review.onclick();assert.equal(elements.practice.style.display,'block');
 elements.tracks.onchange();assert.equal(elements.practice.style.display,'none');
 elements.audio.ended();assert.equal(elements.practice.style.display,'block');
 assert.equal(elements.choices.children.length,3);
 const good=p.question.choices.findIndex(c=>c.id===p.question.correct_choice_id);
 elements.choices.children[(good+1)%3].onclick();assert(elements.result.textContent.startsWith('Chưa đúng'));
 elements.choices.children[good].onclick();assert.equal(elements.result.textContent,'Đúng rồi!');
}
assert.equal(elements.next.disabled,true);
elements.previous.onclick();assert.equal(elements['lesson-image'].src,m.items[1].output.webp);
elements.next.onclick();assert.equal(elements['lesson-image'].src,m.items[2].output.webp);
const result={result:'pass',item_count:3,checks:['All image/audio paths exist','All3 track selections','Practice initially hidden/reset per track','Manual review reveals practice','Audio ended reveals practice','One question with3 choices per track','Correct/wrong feedback','Previous/next navigation and bounds'],limitation:'Node VM DOM harness; does not claim audio listened/transcribed or browser rendering.'};
fs.writeFileSync(path.join(__dirname,'preview-validation.json'),JSON.stringify(result,null,2));
console.log('PASS3-track preview DOM behavior and all resource paths.');

