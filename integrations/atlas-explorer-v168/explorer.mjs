import {buildAtlasPreview} from '../ai-studio-readonly-v166/adapter.mjs';
import {safeText,filterCards,resultMessage,loadJson} from './ux-helpers.mjs';
const prefix='../../';
const files={manifest:'data/contracts/atlas_v165_integration_readiness_manifest.json',narratives:'data/deep/atlas_v156_extended_narratives.json',cities:'data/contracts/atlas_v157_historical_city_map.json',geoLinks:'data/contracts/atlas_v157_spatiotemporal_links.json',editions:'data/contracts/atlas_v161_edition_comparison_cards.json',evidence:'data/contracts/atlas_v163_source_evidence_cards.json',navigation:'data/contracts/atlas_v164_evidence_navigation.json'};
const status=document.querySelector('#status'),holder=document.querySelector('#cards'),query=document.querySelector('#q');let current='readers';
try{
const input=Object.fromEntries(await Promise.all(Object.entries(files).map(async ([k,v])=>[k,await loadJson(fetch,prefix+v)])));
const vm=buildAtlasPreview(input);if(vm.canPublish!==false)throw Error('Publication gate violated');
const sets={
 readers:vm.readerCards.map(x=>({heading:x.title,sub:x.period,body:x.sections.map(s=>s.heading+' — '+s.text).join(' '),source:x.sourceUrls[0]})),
 editions:vm.editionCards.map(x=>({heading:x.title+' · '+x.year,sub:x.kind,body:x.editionId,source:null})),
 claims:vm.claimCards.map(x=>({heading:x.id,sub:x.evidenceLevel,body:x.editionIds.join(' · '),source:input.evidence.cards.find(c=>c.id===x.id)?.source_urls[0]})),
 cities:vm.mapPins.map(x=>({heading:x.name,sub:'도시 중심 근사 좌표',body:x.lat+', '+x.lon,source:null}))
};
function render(){
 const items=filterCards(sets[current],query.value);holder.replaceChildren();
 for(const item of items){const el=document.createElement('article');el.className='card';el.innerHTML='<p class="meta">'+safeText(item.sub)+'</p><h3>'+safeText(item.heading)+'</h3><p>'+safeText(item.body)+'</p>';if(item.source?.startsWith('https://')){const a=document.createElement('a');a.href=item.source;a.target='_blank';a.rel='noopener noreferrer';a.textContent='출처 확인';el.append(a)}holder.append(el)}
 status.textContent=resultMessage(items.length);
}
document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{current=b.dataset.tab;document.querySelectorAll('[data-tab]').forEach(x=>x.setAttribute('aria-selected',String(x===b)));render()}));
query.addEventListener('input',render);render();
}catch(err){status.setAttribute('role','alert');status.textContent='자료를 불러올 수 없습니다. 서버와 JSON 파일을 확인해 주세요.';console.error(err)}
