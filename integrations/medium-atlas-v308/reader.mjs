import {createMediumAtlas} from './adapter.mjs';
import {assembleV308} from './assemble.mjs';
const $=id=>document.getElementById(id);
const PAGE_SIZE=12;
let atlas=null;
const typeLabels={MEDIUM:'핵심 해설',THEME:'쟁점과 생활',REGION:'지역 개관',GLOBAL:'세계 연결',PERSON:'인물',DOCUMENT:'문헌',CITY:'도시',EVENT:'사건'};
const make=(tag,text,cls)=>{const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(cls)el.className=cls;return el;};
const button=(text,id,cls='text-button')=>{const b=make('button',text,cls);b.type='button';b.dataset.reader=id;return b;};
function state(){const p=new URLSearchParams(location.hash.slice(1));return {q:p.get('q')??'',type:p.get('type')??'',path:p.get('path')??'',reader:p.get('reader')??'',page:Math.max(0,Number.parseInt(p.get('page'),10)||0)};}
function navigate(patch,{focus=false}={}){const next={...state(),...patch};const p=new URLSearchParams();for(const [k,v]of Object.entries(next))if(v)p.set(k,String(v));history.pushState(null,'','#'+p.toString());render({focus});}
function sourceList(sources){const ul=make('ul',undefined,'source-list');for(const s of sources){const li=make('li'),a=make('a',s.title);a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';li.append(a,make('span',s.access.label+(s.access.checkedOn?' · '+s.access.checkedOn:''),'access-label'),make('span',s.access.note,'source-note'));if(s.priorInspection)li.append(make('span','이전 확인 범위 · '+s.priorInspection.checkedOn+' · '+s.priorInspection.scope+(s.priorInspection.restoredOn?' · 기록 복구 '+s.priorInspection.restoredOn:'')+' · '+s.priorInspection.note+' (이번 재확인 없음)','source-note'));ul.append(li);}return ul;}
function detail(id,{focus=false}={}){
 const article=$('detail');article.replaceChildren();
 if(!id){const h=make('h2','해설을 선택해 주세요');h.tabIndex=-1;article.append(h,make('p','목록에서 한 편을 고르면 본문과 질문, 관련 해설과 출처를 읽을 수 있습니다.'));return;}
 const c=atlas.getReader(id),h=make('h2',c?.title??'해설을 찾을 수 없습니다');h.tabIndex=-1;
 if(!c){article.append(h,make('p','목록에서 다른 해설을 선택해 주세요.'));if(focus)h.focus();return;}
 article.append(make('span',typeLabels[c.type]??'해설','chip'),h,make('p',c.lead,'lead'));
 for(const s of c.sections){const section=make('section',undefined,'prose');section.append(make('h3',s.heading),make('p',s.body));article.append(section);}
 const question=make('section',undefined,'question');question.append(make('h3','생각해 볼 질문'),make('p',c.readingQuestion));article.append(question);
 if(c.relatedReaders.length){article.append(make('h3','연결해서 읽기'));const related=make('ul',undefined,'related');for(const r of c.relatedReaders){const li=make('li');li.append(button(r.title,r.id));related.append(li);}article.append(related);}
 article.append(make('h3','출처'),sourceList(c.sources));
 if(c.sourceGuide){const g=c.sourceGuide,section=make('section',undefined,'guide');section.append(make('h3','출처를 읽는 안내'),make('p',g.readingGuide),make('p',g.verificationNote,'source-note'));for(const w of g.cautions)section.append(make('p',w.note,'caution'));
  const d=make('details');d.append(make('summary','선택한 주장과 확인 범위 보기'));
  for(const claim of g.claims){const box=make('div',undefined,'claim');box.append(make('strong',claim.label),make('p','본문: '+claim.exact_text_span),make('p','근거 위치: '+claim.source_locator),make('p',claim.evidence_summary));d.append(box);}section.append(d);article.append(section);
 }
 if(focus){h.focus();article.scrollIntoView({block:'start'});}
}
function render({focus=false}={}){
 if(!atlas)return;
 const s=state();$('query').value=s.q;$('type').value=s.type;$('path').value=s.path;
 let results;
 if(s.q.trim()){
  const first=atlas.search(s.q,{type:s.type||null,limit:100});results=[...first.items];
  for(let offset=100;offset<first.total;offset+=100)results.push(...atlas.search(s.q,{type:s.type||null,limit:100,offset}).items);
 }else results=atlas.listReaders().filter(c=>!s.type||c.type===s.type);
 const path=s.path?atlas.getReadingPath(s.path):null;const intro=$('path-intro');intro.replaceChildren();
 if(s.path){if(path){const order=new Map(path.reader_ids.map((id,i)=>[id,i]));results=results.filter(c=>order.has(c.id)).sort((a,b)=>order.get(a.id)-order.get(b.id));intro.append(make('h3',path.title),make('p',path.reading_question),make('p',path.interpretive_limit));}else{results=[];intro.append(make('p','이 읽기 경로를 찾을 수 없습니다. 다른 경로를 선택해 주세요.'));}}
 const pages=Math.max(1,Math.ceil(results.length/PAGE_SIZE)),page=Math.min(s.page,pages-1);$('status').textContent=`전체 ${atlas.counts.readers}편 중 ${results.length}편 · ${page+1}/${pages}페이지`;
 $('result-title').textContent=s.q.trim()?'검색 결과':'해설 목록';const list=$('reader-list');list.replaceChildren();
 for(const c of results.slice(page*PAGE_SIZE,(page+1)*PAGE_SIZE)){
  const li=make('li'),b=button('',c.id,'reader-card');b.setAttribute('aria-current',String(c.id===s.reader));b.append(make('span',typeLabels[c.type]??'해설','chip'),make('span',c.title,'card-title'),make('span',c.lead,'card-lead'));li.append(b);list.append(li);
 }
 if(!results.length)list.append(make('li','조건에 맞는 해설이 없습니다. 검색어 또는 분야를 바꾸어 보세요.'));
 const nav=$('pagination');nav.replaceChildren();const prev=make('button','이전'),next=make('button','다음');prev.type=next.type='button';prev.disabled=page===0;next.disabled=page>=pages-1;
 prev.onclick=()=>navigate({page:page-1});next.onclick=()=>navigate({page:page+1});nav.append(prev,make('span',`${page+1} / ${pages}`),next);
 detail(s.reader,{focus});
}
async function start(){
 try{
  const manifestURL=new URL('./manifest.json',import.meta.url);const response=await fetch(manifestURL);if(!response.ok)throw Error('manifest unavailable');const manifest=await response.json();
  if(manifest.contractVersion!=='3.08'||manifest.canPublish!==false)throw Error('unsupported manifest');
  const [base,addition,cross,remaining]=await Promise.all(manifest.inputs.map(async input=>{
    const response=await fetch(new URL('../../'+input.path,import.meta.url));
    if(!response.ok)throw Error('frozen input unavailable');
    const raw=await response.text(),data=new TextEncoder().encode(raw);
    if(input.sha256){
      const hash=await crypto.subtle.digest('SHA-256',data);
      const digest=[...new Uint8Array(hash)].map(n=>n.toString(16).padStart(2,'0')).join('');
      if(digest!==input.sha256)throw Error('SHA256 mismatch');
    }
    if(input.gitBlobSha1){
      const head=new TextEncoder().encode('blob '+data.length+'\0');
      const combined=new Uint8Array(head.length+data.length);
      combined.set(head);combined.set(data,head.length);
      const hash=await crypto.subtle.digest('SHA-1',combined);
      const digest=[...new Uint8Array(hash)].map(n=>n.toString(16).padStart(2,'0')).join('');
      if(digest!==input.gitBlobSha1)throw Error('Git blob mismatch');
    }
    return JSON.parse(raw);
  }));
  const merged=assembleV308(base,addition,cross,remaining);
  atlas=createMediumAtlas(merged.delivery);
  for(const g of atlas.listGroups()){const option=make('option',g.title+` (${g.reader_ids.length})`);option.value=g.id.replace('TYPE-','');$('type').append(option);}
  for(const p of atlas.listReadingPaths()){const option=make('option',p.title);option.value=p.id;$('path').append(option);}
  render();
 }catch{atlas=null;$('status').textContent='자료를 불러오지 못했습니다.';$('load-error').hidden=false;}
}
$('search-form').addEventListener('submit',e=>{e.preventDefault();navigate({q:$('query').value.trim(),type:$('type').value,path:$('path').value,page:0});});
$('type').addEventListener('change',()=>navigate({type:$('type').value,page:0}));
$('path').addEventListener('change',()=>navigate({path:$('path').value,page:0}));
document.addEventListener('click',e=>{const b=e.target.closest('button[data-reader]');if(b)navigate({reader:b.dataset.reader},{focus:true});});
document.querySelector('.skip').addEventListener('click',e=>{e.preventDefault();$('results').focus();$('results').scrollIntoView({block:'start'});});
$('retry').addEventListener('click',()=>location.reload());
window.addEventListener('popstate',()=>render());
window.addEventListener('hashchange',()=>render());
start();
