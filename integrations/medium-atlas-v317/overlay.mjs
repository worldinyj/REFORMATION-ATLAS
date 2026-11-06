/** V3.17: source-scoped research on pre-signing prints and official-witness ambiguity.
 * Extends completed V3.16 ratification chronology without changing historical core.
 */
import {assembleV316} from '../medium-atlas-v316/overlay.mjs';
const check=(x,m)=>{if(!x)throw Error('V317 treaty printing: '+m);};
const TIER=new Set(['DIGITAL_LIBRARY_LIVE_CATALOGUE_HTML','INSTITUTION_LIVE_HTML','SCHOLARLY_SEARCH_INDEX_ONLY','HISTORIAN_LIVE_HTML','LIBRARY_LIVE_METADATA','EARLY_PRINT_MODERN_TRANSCRIPTION']);
export function assembleV317(inputs,a309,a310,v311,v312,v313,v314,v315,rat316,v317){
 const {delivery,crosswalk}=assembleV316(inputs,a309,a310,v311,v312,v313,v314,v315,rat316);
 check(v317?.version==='3.17'&&v317.status==='DRAFT'&&v317.depth==='MEDIUM','draft version');
 check(v317.publication_gate&&Object.values(v317.publication_gate).every(v=>v===false),'publication HOLD');
 const p=v317.preserve,m=v317.metrics,insp=v317.inspection;
 check(p?.readers===513&&p.sources===723&&p.overviews===97&&p.selected_claims===22&&
  p.v311_addenda===4&&p.v312_notes===2&&p.v313_studies===2&&p.v314_studies===2&&p.v315_studies===2&&
  p.v316_ratification_reading===1&&p.v316_ratification_chronology===4,'upstream preservation contract');
 check(m?.sources===7&&m.studies===3&&m.sections===9&&m.claims===10&&m.unresolved_issues===4&&m.body_characters===2446,'new research metrics');
 check(insp?.original_print_pages_collated===0&&insp.original_diplomatic_pages_collated===0&&insp.new_textual_variants_proven===0,'fabricated original-page inspection');
 check(delivery.readers?.length===513&&delivery.sources?.length===723&&
  delivery.source_verification?.selected_claims?.length===22&&crosswalk.entries?.length===97,'original 513 reader baseline drift');
 check(delivery.ratification_event_v316?.chronology?.length===4&&delivery.ratification_event_v316?.claims?.length===5,'V3.16 verified chronology drift');
 const frozen=JSON.stringify({readers:delivery.readers,sources:delivery.sources,claims:delivery.source_verification,
  crosswalk,v311:delivery.primary_passage_addenda,v312:delivery.latin_english_limited_concordance_v312,
  v313:delivery.edition_archive_provenance_v313,v314:delivery.source_attestation_v314,
  v315:delivery.attestation_wording_v315,v316:delivery.ratification_event_v316});
 check(v317.source_records?.length===7&&v317.studies?.length===3&&v317.claim_cards?.length===10&&v317.issues?.length===4,'incomplete V317 structure');
 const sources=new Map();
 for(const s of v317.source_records){
  check(s.id&&!sources.has(s.id)&&TIER.has(s.tier)&&s.work&&s.url?.startsWith('https://')&&s.verified&&s.boundary&&s.original_pages_read===false,'unqualified source '+s.id);
  if(s.id==='STETTIN')check(s.tier==='DIGITAL_LIBRARY_LIVE_CATALOGUE_HTML'&&s.verified.includes('7월 27일')&&s.boundary.includes('미확인'),'Stettin publication certainty overstated');
  if(s.id==='PADERBORN')check(s.tier==='DIGITAL_LIBRARY_LIVE_CATALOGUE_HTML'&&s.verified.includes('12:187744L'),'Paderborn catalogue identity drift');
  if(s.id==='LWL741')check(s.tier==='SCHOLARLY_SEARCH_INDEX_ONLY'&&s.boundary.includes('유지관리'),'LWL indexed note promoted to live treaty original');
  sources.set(s.id,s);
 }
 check(sources.get('DDB1648')?.work==='IPM'&&sources.get('WS1649')?.work==='IPM'&&sources.get('PADERBORN')?.work==='IPO','IPO/IPM conflation');
 const parentIds=new Set(delivery.attestation_wording_v315.studies.map(s=>s.id));
 const overviewIds=new Set(crosswalk.entries.map(o=>o.overview_id));
 const studies=new Map();let count=0;
 for(const s of v317.studies){
  check(s.id?.startsWith('V317-')&&!studies.has(s.id)&&parentIds.has(s.parent_v315)&&
   s.overviews?.every(k=>overviewIds.has(k))&&s.sources?.every(k=>sources.has(k))&&s.question?.endsWith('?'),'orphan study '+s.id);
  check(s.sections?.length===3,'study requires exactly 3 sections');
  for(const t of s.sections){check(t.heading&&t.body?.length>=180,'short section');count+=t.body.length;}
  studies.set(s.id,s);
 }
 check(count===m.body_characters,'body character checksum drift');
 const claims=new Set();
 for(const c of v317.claim_cards){
  check(c.id&&!claims.has(c.id)&&c.statement?.length>=25&&c.source_ids?.length&&c.source_ids.every(id=>sources.has(id))&&c.level&&c.expert_approved===false&&c.original_witness_collated===false,'unsupported historical claim '+c.id);
  claims.add(c.id);
 }
 const issues=new Map();
 for(const x of v317.issues){
  check(x.id&&!issues.has(x.id)&&['UNRESOLVED','NOT_COLLATED'].includes(x.status)&&x.issue?.length>15,'issue status prematurely resolved');
  issues.set(x.id,x);
 }
 check(issues.size===4&&issues.has('STETTIN_MONTH')&&issues.has('PRINT_VARIANTS')&&issues.has('SIGNING_VENUE')&&issues.has('PRINT_AUTHORITY'),'must preserve four open questions');
 check(v317.cautions?.some(x=>x.includes('슈테틴'))&&v317.cautions?.some(x=>x.includes('특허')),'scope caveats lost');
 delivery.version='3.17';delivery.kind='PRE_SIGNING_PRINTS_513_EDITORIAL_SCOPED_BUNDLE';
 delivery.early_print_witness_v317={source_records:structuredClone(v317.source_records),studies:structuredClone(v317.studies),claim_cards:structuredClone(v317.claim_cards),issues:structuredClone(v317.issues),cautions:[...v317.cautions]};
 delivery.editorial_audit.v317_print_witnesses={sources:7,readings:3,sections:9,claims:10,unresolved_issues:4,body_characters:count,
  archival_pages_collated:0,proven_textual_variants:0,historian_approved:false,actual_app_updated:false};
 delivery.editorial_note+=' / V3.17 조약 서명 이전 인쇄 가능성·특권 인쇄·체결 장소의 사료 간 차이를 비공개 연구 부록으로 추가.';
 check(JSON.stringify({readers:delivery.readers,sources:delivery.sources,claims:delivery.source_verification,
  crosswalk,v311:delivery.primary_passage_addenda,v312:delivery.latin_english_limited_concordance_v312,
  v313:delivery.edition_archive_provenance_v313,v314:delivery.source_attestation_v314,
  v315:delivery.attestation_wording_v315,v316:delivery.ratification_event_v316})===frozen,'previous corpus or research mutated');
 check(Object.values(delivery.publication_gate).every(v=>v===false),'HOLD bypass');
 return {delivery,crosswalk,getPrintWitnessStudiesForV315(id){
  check(parentIds.has(id),'unknown V315 parent');
  return structuredClone(v317.studies.filter(x=>x.parent_v315===id).map(x=>({...x,
    source_records:x.sources.map(k=>sources.get(k)),
    claim_cards:v317.claim_cards.filter(c=>c.source_ids.some(k=>x.sources.includes(k)))})));
 }};
}
