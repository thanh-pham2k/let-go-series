const fs=require('fs'),path=require('path'),assert=require('assert');
(async()=>{
 const base=process.argv[2]||'http://127.0.0.1:60333';
 const root=__dirname,m=JSON.parse(fs.readFileSync(path.join(root,'review.regenerated.metadata'),'utf8')),results=[];
 for(const rel of ['preview.html','review.regenerated.metadata',...m.items.flatMap(p=>[p.image,p.audio_file])]){
  const response=await fetch(base+'/'+rel);
  assert.equal(response.status,200,rel);
  const bytes=Buffer.from(await response.arrayBuffer());
  assert(bytes.equals(fs.readFileSync(path.join(root,rel))),rel+' servedbytes');
  results.push({path:rel,status:response.status,content_type:response.headers.get('content-type'),bytes:bytes.length});
 }
 const result={result:'pass',checks:results,scope:'Direct HTTP serving and byte identity; no browser rendering/playback claim.'};
 fs.writeFileSync(path.join(root,'resource-validation.json'),JSON.stringify(result,null,2));
 console.log('PASS8 HTTP resources: preview, metadata,3 images and3 MP3s, exact servedbytes.');
})().catch(e=>{console.error(e);process.exitCode=1});

