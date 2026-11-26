import {safeURL,assetPath,searchRecords,parseRoute,validateData} from './core.js';
const main=document.getElementById('main');
// Skip navigation without replacing the currently selected chapter hash.
document.getElementById('skip-link')?.addEventListener('click',event=>{event.preventDefault();main.focus();});
let data,index;
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
const add=(parent,tag,cls,text)=>{const n=el(tag,cls,text);parent.append(n);return n;};
const href=(parent,label,hash)=>{const a=add(parent,'a','',label);a.href=hash;return a;};
const chapterLink=(parent,id,label)=>href(parent,label||data.chapters.find(c=>c.id===id)?.title||id,'#chapter/'+id+'/overview');
const title=(label,heading,lead)=>{add(main,'div','eyebrow',label);add(main,'h1','',heading);if(lead)add(main,'p','lead',lead);};
const paragraph=(parent,text)=>{for(const line of String(text??'').split(/\n\s*\n/)){if(line.trim())add(parent,'p','',line);}};
function inline(parent,text){
  // Deliberately limited Markdown: bold, code and explicit HTTP(S) link only.
  const re=/\*\*([^*\n]+)\*\*|`([^`\n]+)`|\[([^\]\n]+)\]\((https?:\/\/[^\s)]+)\)/g;
  let last=0;for(const m of String(text).matchAll(re)){parent.append(document.createTextNode(text.slice(last,m.index)));if(m[1])inline(add(parent,'strong'),m[1]);else if(m[2])add(parent,'code','',m[2]);else {const url=safeURL(m[4]);if(url){const a=href(parent,m[3],url);a.rel='noopener noreferrer';}else parent.append(document.createTextNode(m[0]));}last=m.index+m[0].length;}parent.append(document.createTextNode(text.slice(last)));
}
function markdown(parent,raw){
  // Treat unsupported syntax as literal text; never use innerHTML.
  let list=null,block=null;for(const line of String(raw??'').split('\n')){
    if(!line.trim()){list=null;block=null;continue;}
    const h=line.match(/^(#{1,6})\s+(.+)$/);const li=line.match(/^\s*[-*]\s+(.+)$/);
    if(h){list=null;block=null;inline(add(parent,'h'+Math.min(6,h[1].length+1),'',undefined),h[2]);}
    else if(/^\s*---+\s*$/.test(line)){list=null;block=null;add(parent,'hr');}
    else if(li){block=null;if(!list)list=add(parent,'ul');inline(add(list,'li'),li[1]);}
    else {list=null;if(!block)block=add(parent,'p');else block.append(document.createTextNode(' '));inline(block,line);}
  }
}
function sources(parent,urls){const valid=[...new Set((urls||[]).map(safeURL).filter(Boolean))];if(!valid.length)return;const details=add(parent,'details','sources');add(details,'summary','','참고 문헌 · '+valid.length+'건');const list=add(details,'ul');for(const u of valid){const a=href(add(list,'li'),u,u);a.rel='noopener noreferrer';}}
function visual(parent,id,caption,cls=''){
  const a=data.assets.find(x=>x.id===id),path=assetPath(a),fig=add(parent,'figure','visual '+cls);
  if(!path){add(fig,'p','missing','시각 자료 경로를 확인할 수 없습니다.');return;}
  const img=add(fig,'img');img.alt=caption;img.loading='lazy';img.addEventListener('error',()=>{img.remove();add(fig,'p','missing','시각 자료를 불러오지 못했습니다. 관련 역사 설명은 계속 읽을 수 있습니다.');},{once:true});img.src=path;add(fig,'figcaption','',caption);
}
function card(parent,label,heading,desc,hash){const box=add(parent,'article','card');add(box,'div','meta',label);const h=add(box,'h3');if(hash)href(h,heading,hash);else h.textContent=heading;paragraph(box,desc);return box;}
function home(){title('세계 기독교 역사 · 8권 24장','종교개혁 ATLAS','고대 교회에서 종교개혁과 세계 기독교까지. 역사·신학·지역의 여러 관점을 함께 탐색합니다.');const grid=add(main,'div','grid');for(const v of data.volumes)card(grid,v.id,v.title,v.subtitle,'#volume/'+v.id);}
function volume(id){const v=data.volumes.find(x=>x.id===id);title(v.id,v.title,v.subtitle);const read=add(main,'div','reading');paragraph(read,v.intro);const grid=add(main,'div','grid');for(const cid of v.chapter_ids){const c=data.chapters.find(x=>x.id===cid);card(grid,c.period,c.title,c.overview.text,'#chapter/'+cid+'/overview');}add(main,'h2','','역사 지도');visual(main,v.map_asset_id,'현대 해안선과 역사 관련 근사 위치 · 역사 국경 및 이동 경로 아님');paragraph(add(main,'div','reading'),v.outro);}
function unit(parent,u,isTheology){const b=add(parent,'article','card');add(b,'h3','',u.title);markdown(b,u.body);add(b,'p','limit',u.boundary||u.limit||'연구 검토용');if(u.source_scope)add(b,'p','meta','자료 검토 범위: '+u.source_scope);const urls=isTheology?(u.refs||[]).map(([key])=>data.theology.sources[key]?.url):(u.sources||[]).map(x=>Array.isArray(x)?x[0]:x.url);sources(b,urls);chapterLink(b,u.home,'관련 역사 장 읽기');return b;}
function caseCard(parent,k){const b=card(parent,k.period+' · '+k.region,k.label,k.primary_evidence_genre);add(b,'p','limit',k.interpretation_limit);add(b,'p','meta','근거: 기존 연구 원고에서 정리한 사례입니다. 개별 출처가 이 사례의 모든 주장을 뒷받침하는지 별도로 확인해야 합니다.');for(const loc of k.locations)add(b,'p','meta',loc.name+(loc.coordinates?' · 근사 위치':' · 좌표 미확정'));chapterLink(b,k.chapter_id,'관련 장 읽기');}
function personCard(parent,p){const b=card(parent,p.period+' · '+p.region,p.name,p.summary);visual(b,p.symbol_asset_id,p.name+' · 상징형 카드, 실제 초상 아님','person');add(b,'p','limit',p.evidence_note);sources(b,p.sources);chapterLink(b,p.chapter_id,'관련 역사 장');}
function chapter(id,level){const c=data.chapters.find(x=>x.id===id),v=data.volumes.find(x=>x.id===c.volume_id);href(main,v.title,'#volume/'+v.id);title(c.period,c.title);const tabs=add(main,'nav','tabs');tabs.setAttribute('aria-label','읽기 깊이');for(const [k,label] of [['overview','개요'],['intermediate','중간 해설'],['deep','심층 연구']]){const a=href(tabs,label,'#chapter/'+id+'/'+k);if(k===level)a.setAttribute('aria-current','page');}const read=add(main,'article','reading');if(level==='overview'){markdown(read,c.overview.text);if(c.overview.question)add(read,'p','limit',c.overview.question);}
else if(level==='intermediate'){add(read,'h2','',c.intermediate.title);markdown(read,c.intermediate.text);if(c.intermediate.question)add(read,'p','limit',c.intermediate.question);const ladder=c.intermediate.evidence_ladder||[];if(ladder.length){const details=add(read,'details');add(details,'summary','','증거와 해석의 한계');for(const x of ladder){add(details,'h3','',x.level||x.kind||'근거');paragraph(details,[x.claim,x.limit].filter(Boolean).join(' — '));}}sources(read,c.intermediate.supplemental_urls);sources(read,(c.intermediate.public_context_records||[]).map(x=>x.url));}
else{markdown(read,c.deep.markdown);if(c.deep.needs_expert_review)add(read,'p','limit','역사·신학 전문가 검토가 아직 완료되지 않은 연구 원고입니다.');sources(read,c.deep.source_urls);}
if(c.document_asset_ids.length){add(main,'h2','','관련 문헌 도해');for(const a of c.document_asset_ids)visual(main,a,'문헌 간행 단계 비교 · 확정된 직접 계보 아님');}
const cases=data.cases.filter(x=>c.case_ids.includes(x.case_id));if(cases.length){add(main,'h2','','역사 사례');const g=add(main,'div','grid');for(const k of cases)caseCard(g,k);}
const persons=data.people.filter(x=>c.person_ids.includes(x.id));if(persons.length){add(main,'h2','','관련 인물');const g=add(main,'div','grid');for(const p of persons)personCard(g,p);}
const us=[...data.theology.units.filter(x=>c.theology_ids.includes(x.id)).map(u=>[u,true]),...data.global_units.filter(x=>c.global_ids.includes(x.id)).map(u=>[u,false])];if(us.length){add(main,'h2','','신학·지역 심화 해설');for(const [u,t] of us)unit(main,u,t);}
const next=add(main,'div','next');add(next,'h3','','이어 읽기');paragraph(next,c.transition.text);chapterLink(next,c.transition.next_chapter_id);
}
function maps(){title('공간 탐색','역사 지도','현대 지형 기반 지도입니다. 역사적 국경·이동 경로를 복원한 자료는 아닙니다.');const label=add(main,'label','','권 선택 ');const select=add(label,'select');for(const v of data.volumes){const opt=add(select,'option','',v.title);opt.value=v.id;}const view=add(main,'section');function draw(){view.replaceChildren();const v=data.volumes.find(x=>x.id===select.value);visual(view,v.map_asset_id,v.title+' · 관련 장소와 지역 정보');const rows=data.cases.filter(c=>v.kind==='thematic'||c.volume_id===v.id);add(view,'h2','','연결된 사례 '+rows.length+'개');const g=add(view,'div','grid');for(const c of rows)caseCard(g,c);}select.addEventListener('change',draw);draw();}
function people(){title('인물 아카이브','역사를 만든 사람들','10명의 활동과 증거를 살펴봅니다. 그림은 외모가 아닌 업적을 표현한 상징 삽화입니다.');const g=add(main,'div','grid');for(const p of data.people)personCard(g,p);}
function documents(){title('문헌 아카이브','기록과 판본의 시간','연표와 문헌의 사건·기록·인쇄 시점을 구분합니다.');visual(main,data.timeline.asset_id,'세계 기독교 병행 연표 · 시간 비례 아님');for(const a of data.assets.filter(x=>x.kind==='diagram'&&x.id!==data.timeline.asset_id)){const label={'asset:augsburg.svg':'아우크스부르크 신앙고백','asset:tamil.svg':'타밀어 신약','asset:korean.svg':'한국어 성경','asset:stele.svg':'경교비'}[a.id]||a.id;add(main,'h2','',label);visual(main,a.id,label+' · 연구용 문헌 단계 비교');}}
function themes(){title('신학과 지역','여러 전통의 역사','각 전통의 신앙고백과 지역 공동체의 역사를 비교합니다.');add(main,'h2','','핵심 신학 5편');for(const u of data.theology.units)unit(main,u,true);add(main,'h2','','세계사적 보강 6편');for(const u of data.global_units)unit(main,u,false);}
function search(){title('통합 검색','어떤 역사를 찾으시나요?','제목·개요·중간 해설·사례·인물·신학 주제 색인에서 검색합니다.');const form=add(main,'form','search-row'),input=add(form,'input');input.type='search';input.placeholder='예: 루터, 타밀어, 서상륜';input.setAttribute('aria-label','검색어');const button=add(form,'button','','검색');button.type='submit';const out=add(main,'section');out.setAttribute('aria-live','polite');function run(){out.replaceChildren();const hits=searchRecords(index,input.value);add(out,'p','count',input.value.trim()?'검색 결과 '+hits.length+'개':'검색어를 입력하세요.');const g=add(out,'div','grid');for(const h of hits){const c=data.chapters.find(x=>x.id===h.id);card(g,c.period,c.title,c.overview.text,'#chapter/'+c.id+'/overview');}}form.addEventListener('submit',e=>{e.preventDefault();run();});run();}
function render(){const r=parseRoute(location.hash,data);main.replaceChildren();for(const a of document.querySelectorAll('#nav a')){if(a.getAttribute('href')==='#'+r.view)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}if(r.view==='chapter')chapter(r.id,r.level);else if(r.view==='volume')volume(r.id);else ({home,maps,people,documents,themes,search}[r.view]||home)();main.focus({preventScroll:true});window.scrollTo(0,0);}
async function load(){try{const [a,b]=await Promise.all(['atlas_preview.json','search_index.json'].map(async p=>{const r=await fetch(p);if(!r.ok)throw Error('파일 로드 실패: '+p);return r.json();}));validateData(a,b);data=a;index=b;window.addEventListener('hashchange',()=>{render();});render();}catch(e){main.replaceChildren();add(main,'h1','','미리보기를 열 수 없습니다');add(main,'p','missing',String(e.message||e));add(main,'p','','ZIP을 풀고 로컬 HTTP 서버에서 실행했는지 확인하세요. 운영 앱에는 영향을 주지 않습니다.');}}
load();
