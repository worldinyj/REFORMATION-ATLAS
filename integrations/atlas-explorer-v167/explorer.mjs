// V1.67 standalone explorer. No external network, image, map tiles or persistence.
import { buildAtlasPreview } from '../ai-studio-readonly-v166/adapter.mjs';
const load = async file => (await (await fetch(file)).json());
const root='../../';
const input={
 manifest:await load(root+'data/contracts/atlas_v165_integration_readiness_manifest.json'),
 narratives:await load(root+'data/deep/atlas_v156_extended_narratives.json'),
 cities:await load(root+'data/contracts/atlas_v157_historical_city_map.json'),
 geoLinks:await load(root+'data/contracts/atlas_v157_spatiotemporal_links.json'),
 editions:await load(root+'data/contracts/atlas_v161_edition_comparison_cards.json'),
 evidence:await load(root+'data/contracts/atlas_v163_source_evidence_cards.json'),
 navigation:await load(root+'data/contracts/atlas_v164_evidence_navigation.json')
};
const vm=buildAtlasPreview(input);
if(vm.canPublish!==false)throw Error('Research publication gate must remain closed');
const esc=s=>String(s??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
const cards={
 readers:vm.readerCards.map(x=>({heading:x.title,sub:x.period,body:x.sections.map(y=>y.heading+': '+y.text).join(' '),url:x.sourceUrls[0],note:'원전 직접 교감 미완료'})),
 editions:vm.editionCards.map(x=>({heading:x.title+' · '+x.year,sub:x.kind,body:x.editionId,url:null,note:'영인 이미지 게시 보류'})),
 claims:vm.claimCards.map(x=>({heading:x.id,sub:x.evidenceLevel,body:x.editionIds.join(' · ')+' / '+x.readerPageId,url:input.evidence.cards.find(e=>e.id===x.id)?.source_urls?.[0],note:'원문 판면 직접 대조 미완료'})),
 cities:vm.mapPins.map(x=>({heading:x.name,sub:'도시 중심 근사 좌표',body:x.lat+', '+x.lon+' / '+x.pageId,url:null,note:'정확한 사건 발생 위치 아님'}))
};
let tab='readers';const q=document.querySelector('#query');const msg=document.querySelector('#message');
function render(){
 const search=q.value.trim().toLocaleLowerCase('ko');const shown=cards[tab].filter(x=>(x.heading+' '+x.sub+' '+x.body).toLocaleLowerCase('ko').includes(search));
 const holder=document.querySelector('#'+tab+' .cards');holder.replaceChildren();
 for(const item of shown){
   const article=document.createElement('article');article.className='card';
   article.innerHTML='<div class="meta">'+esc(item.sub)+'</div><h3>'+esc(item.heading)+'</h3><p>'+esc(item.body)+'</p><p class="meta">'+esc(item.note)+'</p>';
   if(item.url?.startsWith('https://')){const a=document.createElement('a');a.href=item.url;a.textContent='자료 출처';a.target='_blank';a.rel='noopener noreferrer';a.className='source';article.append(a);}
   holder.append(article);
 }
 msg.textContent=shown.length+'개 자료 표시';
}
document.querySelectorAll('[data-tab]').forEach(btn=>btn.addEventListener('click',()=>{
 tab=btn.dataset.tab;
 document.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-selected',String(b===btn)));
 document.querySelectorAll('section').forEach(s=>s.classList.toggle('active',s.id===tab));
 render();
}));
q.addEventListener('input',render);render();
