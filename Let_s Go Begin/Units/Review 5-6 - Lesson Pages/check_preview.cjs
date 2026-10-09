const fs=require('fs'),vm=require('vm'),assert=require('assert');
const root=__dirname,html=fs.readFileSync(root+'/preview.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map();
function element(){return {style:{},children:[],events:{},textContent:'',disabled:false,append(c){this.children.push(c)},replaceChildren(){this.children=[]},pause(){},addEventListener(k,v){this.events[k]=v}}}
const document={getElementById(id){if(!nodes.has(id))nodes.set(id,element());return nodes.get(id)},createElement:element};
const context={document,assert};vm.createContext(context);
vm.runInContext(script+`
assert.equal(pages.length,2);assert.equal(select.children.length,2);
for(let i=0;i<pages.length;i++){
 show(i);const p=pages[i];
 assert.equal(document.getElementById('lesson-image').src,p.output.webp);
 assert.equal(audio.src,p.audio_file);
 assert.equal(document.getElementById('practice').style.display,'none');
 assert.equal(document.getElementById('result').textContent,'');
 audio.events.ended();assert.equal(document.getElementById('practice').style.display,'block');
 assert.equal(document.getElementById('choices').children.length,3);
 const wrong=p.question.choices.findIndex(c=>c.id!==p.question.correct_choice_id);
 document.getElementById('choices').children[wrong].onclick();
 assert.equal(document.getElementById('result').textContent,'Chưa đúng, bé thử lại nhé.');
 const correct=p.question.choices.findIndex(c=>c.id===p.question.correct_choice_id);
 document.getElementById('choices').children[correct].onclick();
 assert.equal(document.getElementById('result').textContent,'Đúng rồi!');
 show(i);document.getElementById('review').onclick();
 assert.equal(document.getElementById('practice').style.display,'block');
}
show(0);assert.equal(document.getElementById('previous').disabled,true);
document.getElementById('next').onclick();assert.equal(current,1);
assert.equal(document.getElementById('next').disabled,true);
document.getElementById('previous').onclick();assert.equal(current,0);
select.value='1';select.onchange();assert.equal(current,1);
`,context);
const report={result:'pass',item_count:2,checks:['Script parses and initializes two track options','All track/image/audio/question mappings','Quiz hidden on load/change','Synthetic audio ended reveals quiz','Manual review reveals quiz','Correct/wrong answer feedback only after selection','Previous/next/select navigation, disabled boundary buttons, state reset'],limitation:'DOM/event stubs, not a real browser or independent listening audit.'};
fs.writeFileSync(root+'/preview.checks.json',JSON.stringify(report,null,2));
console.log('Preview PASS: 2 mappings, navigation, ended/manual review, feedback and state reset.');
