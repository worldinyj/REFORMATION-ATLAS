// Run from any directory with Node 22+; no dependencies. Simulated DOM, not a browser.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
function runHarness(app,core,data,index){
 class Node{constructor(tag,text=""){this.tag=tag;this._text=String(text);this.children=[];this.attrs={};this.events={};this.className="";this._value="";this.focused=false;}append(...nodes){for(const n of nodes){n.parent=this;this.children.push(n)}}replaceChildren(...nodes){this.children=[];this._text="";this.append(...nodes)}set textContent(x){this._text=String(x);this.children=[]}get textContent(){return this._text+this.children.map(n=>n.textContent).join("")}setAttribute(k,v){this.attrs[k]=String(v)}getAttribute(k){return this.attrs[k]??null}removeAttribute(k){delete this.attrs[k]}addEventListener(k,f){(this.events[k]??=[]).push(f)}fire(k){let prevented=false;for(const f of this.events[k]||[])f({preventDefault(){prevented=true}});return prevented}focus(){this.focused=true}remove(){if(this.parent)this.parent.children=this.parent.children.filter(n=>n!==this)}set href(v){this.attrs.href=v}get href(){return this.attrs.href}set value(v){this._value=v}get value(){return this._value||(this.tag==="select"?this.children[0]?.value||"":"")}}
 const main=new Node("main"),skip=new Node("a"),nav=["home","maps","people","documents","themes","search"].map(v=>{const n=new Node("a");n.href="#"+v;return n});const document={getElementById:id=>id==="main"?main:id==="skip-link"?skip:null,createElement:t=>new Node(t),createTextNode:t=>new Node("#text",t),querySelectorAll:()=>nav};const location={hash:"#home"},listeners={};const window={addEventListener:(k,f)=>listeners[k]=f,scrollTo(){}};const fetch=async p=>({ok:true,json:async()=>p==="atlas_preview.json"?data:index});
 const code=core.replace(/^export /gm,"")+"\n"+app.replace(/^import .*?;\s*/,"").replace(/load\(\);\s*$/,"return load();");
 const all=(n,t)=>[...(n.tag===t?[n]:[]),...n.children.flatMap(x=>all(x,t))];const route=hash=>{location.hash=hash;listeners.hashchange();return main.textContent};
 const compact=s=>s.replace(/\s+/g,"");const lineText=s=>compact(s.replace(/^\s*#{1,6}\s+/,"").replace(/^\s*[-*]\s+/,"").replace(/\*\*([^*\n]+)\*\*/g,"$1").replace(/`([^`\n]+)`/g,"$1").replace(/\[([^\]\n]+)\]\((https?:\/\/[^\s)]+)\)/g,"$1"));const checks=[];const check=(name,pass,detail)=>checks.push({name,pass:!!pass,detail});
 return Function("document","location","window","fetch",code)(document,location,window,fetch).then(()=>{
 check("home",all(main,"article").length===8,8);
 for(const v of data.volumes){const out=route("#volume/"+v.id);check("volume:"+v.id,out.includes(v.title)&&all(main,"img").length===1&&all(main,"article").length===3,3)}
 let totalLines=0,missingLines=[];
 for(const ch of data.chapters){for(const level of ["overview","intermediate","deep"]){route("#chapter/"+ch.id+"/"+level);const article=all(main,"article").find(n=>n.className==="reading"),text=compact(article?.textContent||"");const expected=ch[level].text||ch[level].markdown;const lines=expected.split("\n").filter(s=>s.trim()&&!/^\s*---+\s*$/.test(s));totalLines+=lines.length;const missing=lines.filter(s=>!text.includes(lineText(s)));if(missing.length)missingLines.push({chapter:ch.id,level,sample:missing[0].slice(0,100)});const urls=level==="deep"?ch.deep.source_urls:[];const links=all(article,"a").map(n=>n.href);const validUrls=[...new Set(urls.map(u=>{try{return new URL(u).href}catch{return null}}).filter(Boolean))];check("chapter:"+ch.id+":"+level,all(main,"h1")[0]?.textContent===ch.title&&missing.length===0&&validUrls.every(u=>links.includes(u))&&all(main,"a").some(n=>n.href==="#chapter/"+ch.transition.next_chapter_id+"/overview"),{lines:lines.length,missing:missing.length,source_urls:validUrls.length});}}
 check("deepExpertDisclosure",(()=>{route("#chapter/"+data.chapters[0].id+"/deep");return main.textContent.includes("역사·신학 전문가 검토가 아직 완료되지 않은")})(),true);
 const hash=location.hash;main.focused=false;check("skipLinkPreservesRoute",skip.fire("click")&&main.focused&&location.hash===hash,hash);
 route("#maps");const select=all(main,"select")[0];for(const v of data.volumes){select.value=v.id;select.fire("change");const n=data.cases.filter(c=>v.kind==="thematic"||c.volume_id===v.id).length;check("maps:"+v.id,all(main,"article").length===n&&all(main,"img").length===1,n)}
 check("caseEvidenceDisclosure",main.textContent.includes("개별 출처가 이 사례의 모든 주장을"),true);
 route("#people");check("people",all(main,"article").length===10&&all(main,"img").length===10&&all(main,"img").every(n=>n.alt.includes("실제 초상 아님")),10);all(main,"img")[0].fire("error");check("imageFallback",main.textContent.includes("시각 자료를 불러오지 못했습니다")&&all(main,"img").length===9,9);
 route("#documents");check("documents",all(main,"img").length===5,5);route("#themes");check("themes",all(main,"article").length===11,11);
 route("#search");for(const [q,n] of [["루터",4],["타밀어",3],["서상륜",3],["zzzz_nonexistent_zzzz",0],[" ",0]]){all(main,"input")[0].value=q;all(main,"form")[0].fire("submit");check("search:"+q,all(main,"article").length===n,n)}
 check("invalidRoute",route("#chapter/invalid").includes("종교개혁 ATLAS"),true);return {checks,totalLines,missingLines,passed:checks.filter(x=>x.pass).length,total:checks.length};
 });
}
const r=await runHarness(read('research/v538/app/app.js'),read('research/v538/app/core.js'),JSON.parse(read('research/v537/preview/atlas_preview.json')),JSON.parse(read('research/v537/preview/search_index.json')));
console.log(JSON.stringify(r,null,2));if(r.passed!==r.total)process.exitCode=1;
