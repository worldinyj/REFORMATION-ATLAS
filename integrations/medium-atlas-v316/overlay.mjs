/** V3.16 editorial research: distinguish pre-signing imprints, signed instruments and later authority claims. */
import {assembleV315} from '../medium-atlas-v315/overlay.mjs';
const guard=(v,m)=>{if(!v)throw Error('V316 witness-and-print: '+m);};
const TIERS=new Set(['CATALOGUE_SEARCH_INDEX','LIBRARY_LIVE_HTML','INSTITUTION_LIVE_HTML',
 'SCHOLARLY_SEARCH_INDEX_ONLY','HISTORIAN_LIVE_HTML','LIBRARY_LIVE_METADATA','EARLY_PRINT_MODERN_TRANSCRIPTION']);
const BASE={sources:7,studies:3,sections:9,claims:10,unresolved_issues:4,body_characters:2350};
export function assembleV316(inputs,a309,a310,v311,v312,v313,v314,v315,v316){
 const {delivery,crosswalk}=assembleV315(inputs,a309,a310,v311,v312,v313,v314,v315);
 guard(v316?.version==='3.16'&&v316.status==='DRAFT'&&v316.depth==='MEDIUM','draft contract');
 guard(v316.publication_gate&&Object.values(v316.publication_gate).every(x=>x===false),'publication HOLD');
 guard(delivery.publication_gate&&Object.values(delivery.publication_gate).every(x=>x===false),'inherited publication HOLD');
 const p=v316.preserve,i=v316.inspection;
 guard(p?.readers===513&&p.sources===723&&p.overviews===97&&p.selected_claims===22&&
  p.v311_addenda===4&&p.v312_notes===2&&p.v313_studies===2&&p.v314_studies===2&&p.v315_studies===2,'prior corpus contract');
 guard(i?.original_print_pages_collated===0&&i.original_diplomatic_pages_collated===0&&
  i.new_textual_variants_proven===0,'false original witness examination');
 guard(Object.entries(BASE).every(([k,v])=>v316.metrics?.[k]===v),'research metrics changed');
 guard(delivery.readers?.length===513&&delivery.sources?.length===723&&
  delivery.source_verification?.selected_claims?.length===22&&crosswalk.entries?.length===97&&
  delivery.attestation_wording_v315?.studies?.length===2,'prior research modified');
 const old=JSON.stringify({readers:delivery.readers,sources:delivery.sources,source_verification:delivery.source_verification,
  crosswalk,prior:delivery.attestation_wording_v315,other:delivery.source_attestation_v314});
 guard(v316.source_records?.length===7&&v316.studies?.length===3&&v316.claim_cards?.length===10&&
  v316.issues?.length===4,'incomplete history review');
 const sourceMap=new Map();
 for(const s of v316.source_records){
  guard(s.id&&!sourceMap.has(s.id)&&['IPO','IPM','BOTH'].includes(s.work)&&TIERS.has(s.tier)&&
   s.url?.startsWith('https://')&&s.verified?.length>=25&&s.boundary?.length>=20&&
   s.original_pages_read===false,'bad witness/source record '+s.id);
  sourceMap.set(s.id,s);
 }
 guard(sourceMap.get('STETTIN')?.tier==='CATALOGUE_SEARCH_INDEX'&&
  sourceMap.get('STETTIN').boundary.includes('미검증'),'Stettin image falsely claimed');
 guard(sourceMap.get('LWL741')?.tier==='SCHOLARLY_SEARCH_INDEX_ONLY'&&
  sourceMap.get('LWL741').boundary.includes('유지관리'),'LWL blocked text promoted');
 guard(sourceMap.get('PADERBORN')?.tier==='LIBRARY_LIVE_HTML'&&
  sourceMap.get('PADERBORN').verified.includes('VD17 12:187744L'),'Paderborn identifier');
 guard(sourceMap.get('DDB1648')?.work==='IPM'&&sourceMap.get('WS1649')?.work==='IPM'&&
  sourceMap.get('STETTIN')?.work==='IPO','two treaty identities merged');
 const overviewIds=new Set(crosswalk.entries.map(e=>e.overview_id));
 const parents=new Set(delivery.attestation_wording_v315.studies.map(e=>e.id));
 const studyMap=new Map();let total=0;
 for(const e of v316.studies){
  guard(e.id&&!studyMap.has(e.id)&&parents.has(e.parent_v315)&&
   e.overviews?.length&&e.overviews.every(id=>overviewIds.has(id))&&
   e.sources?.length&&e.sources.every(id=>sourceMap.has(id))&&
   e.sections?.length===3&&e.question?.endsWith('?'),'unresolved study '+e.id);
  for(const s of e.sections){guard(s.heading&&s.body?.length>=200,'short study section '+e.id);total+=s.body.length;}
  studyMap.set(e.id,e);
 }
 guard(total===BASE.body_characters,'body character count drift');
 guard(studyMap.size===3&&[...studyMap.values()].every(e=>e.parent_v315==='V315-SIGNING'),'wrong genealogy');
 const claimIds=new Set();
 for(const c of v316.claim_cards){
  guard(c.id&&!claimIds.has(c.id)&&c.source_ids?.length&&c.source_ids.every(s=>sourceMap.has(s))&&
   c.statement?.length>=30&&c.level&&c.original_witness_collated===false&&
   c.historian_approved===false,'incomplete claim evidence '+c.id);
  claimIds.add(c.id);
 }
 guard(claimIds.size===10,'duplicate claims');
 const issueIds=new Set(),allowedStatus=new Set(['UNRESOLVED','NOT_COLLATED']);
 for(const issue of v316.issues){
  guard(issue.id&&!issueIds.has(issue.id)&&issue.issue?.length>=30&&allowedStatus.has(issue.status),
   'invalid unresolved issue');
  issueIds.add(issue.id);
 }
 guard(issueIds.has('STETTIN_MONTH')&&issueIds.has('SIGNING_VENUE')&&issueIds.has('PRINT_VARIANTS'),
  'missing key uncertainties');
 delivery.version='3.16';delivery.kind='EDITORIAL_WITNESS_PRINTING_REVIEW_ONLY';
 delivery.westphalia_witness_printing_v316={
  sources:structuredClone(v316.source_records),
  studies:structuredClone(v316.studies),
  claim_cards:structuredClone(v316.claim_cards),
  open_questions:structuredClone(v316.issues),
  original_pages_inspected:0,textual_variants_proven:0
 };
 delivery.editorial_audit.v316_witness_printing={
  printed_corpus_unchanged:true,medium_studies:3,sections:9,source_records:7,
  claims:10,unresolved_issues:4,original_pages_inspected:0,variants_proven:0,
  expert_approved:false,actual_app_updated:false,publication_released:false
 };
 delivery.editorial_note+=' / V3.16 슈테틴 선행 인쇄·조약 원본·인쇄특권과 서명 장소의 미해결 범위 구분, 외부 감수 및 원판교감 미완료.';
 guard(JSON.stringify({readers:delivery.readers,sources:delivery.sources,source_verification:delivery.source_verification,
  crosswalk,prior:delivery.attestation_wording_v315,other:delivery.source_attestation_v314})===old,
  'frozen manuscripts or inherited research mutated');
 return {delivery,crosswalk,getForV315:id=>{
  guard(parents.has(id),'unknown V315 reading');
  return structuredClone(v316.studies.filter(e=>e.parent_v315===id).map(e=>({
   ...e,source_records:e.sources.map(s=>sourceMap.get(s)),
   claims:v316.claim_cards.filter(c=>c.source_ids.some(s=>e.sources.includes(s)))
  })));
 }};
}
