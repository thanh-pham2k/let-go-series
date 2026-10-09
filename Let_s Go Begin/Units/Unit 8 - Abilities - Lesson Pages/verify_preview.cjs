const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/preview.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements={};
function el(){return {style:{},children:[],textContent:'',disabled:false,value:null,append(x){this.children.push(x)},replaceChildren(){this.children=[]},pause(){},addEventListener(name,fn){this[name]=fn}}}
const document={getElementById(id){return elements[id]??=(el())},createElement(){return el()}};
const ctx=vm.createContext({document});
vm.runInContext(script,ctx);
assert.equal(elements.tracks.children.length,16);
assert.equal(elements['practice'].style.display,'none');
assert.equal(elements.previous.disabled,true);
assert.equal(elements['lesson-image'].src,'pages/webp/CD2_54.webp');
assert.equal(elements.audio.src,'audio/Track54.mp3');
elements.audio.ended();
assert.equal(elements.practice.style.display,'block');
elements.choices.children[0].onclick();
assert.equal(elements.result.textContent,'Đúng rồi!');
elements.choices.children[1].onclick();
assert.equal(elements.result.textContent,'Chưa đúng, bé thử lại nhé.');
elements.next.onclick();
assert.equal(elements.practice.style.display,'none');
assert.equal(elements.result.textContent,'');
for(let i=0;i<16;i++){
 elements.tracks.value=i;elements.tracks.onchange();
 assert.equal(elements['lesson-image'].src,'pages/webp/CD2_'+(54+i)+'.webp');
 assert.equal(elements.audio.src,'audio/Track'+(54+i)+'.mp3');
 assert.equal(elements.choices.children.length,3);
 assert.equal(elements.practice.style.display,'none');
}
assert.equal(elements.next.disabled,true);
assert.equal(elements.previous.disabled,false);
elements.review.onclick();
assert.equal(elements.practice.style.display,'block');
console.log('Preview runtime passed:16 options/media/quiz choices,ended reveal,correct/wrong feedback,reset and navigation bounds. Mock DOM; no audio listened.');

