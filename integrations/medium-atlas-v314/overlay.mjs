/** Source authentication reading notes; source-description evidence != physical collation. */
import {assembleV313} from '../medium-atlas-v313/overlay.mjs';
const assert=(v,msg)=>{if(!v)throw Error('V314 attestation: '+msg);};
const evidenceTiers=new Set(['HOLDING_INSTITUTION_DESCRIPTION','DETAILED_INSTITUTIONAL_COPY_CATALOGUE',
  'HISTORICAL_EDITORIAL_SOURCE_TEXT_IN_SEARCH_INDEX','ARCHIVAL_ORIGINAL_HOLDING_SEARCH_INDEX',
  'DIGITAL_LIBRARY_PRINT_METADATA','RECENT_ACADEMIC_SECONDARY_REFERENCE']);
export function assembleV314(inputs,a309,a310,v311,v312,v313,v314){
 const {delivery,crosswalk}=assembleV313(inputs,a309,a310,v311,v312,v313);
 assert(v314?.version==='3.14'&&v314.status==='DRAFT'&&v314.depth==='MEDIUM','invalid scope version');
 assert(v314.publication_gate&&Object.values(v314.publication_gate).every(v=>v===false),'publication HOLD');
 assert(v314.archive_inspection?.museum_original_page_images_inspected===0&&
  v314.archive_inspection.westphalia_original_page_images_inspected===0&&
  v314.archive_inspection.actual_textual_variants_proven===0,'invented original image collation');
 const metrics=v314.metrics;
 assert(metrics?.sources===6&&metrics.claims===6&&metrics.studies===2&&metrics.sections===6&&
  metrics.body_characters===2017&&metrics.full_archival_collations===0,'unexpected source authentication scope');
 const p=v314.preserve;
 assert(p?.readers===513&&p.sources===723&&p.overviews===97&&p.verified_claims===22&&p.v311_addenda===4&&
  p.v312_readings===2&&p.v313_studies===2,'prior scope is not pinned');
 assert(delivery.readers?.length===513&&delivery.sources?.length===723&&delivery.primary_passage_addenda?.length===4&&
  delivery.edition_archive_provenance_v313?.studies?.length===2,'inherited contents mismatch');
 const original=structuredClone({readers:delivery.readers,sources:delivery.sources,
  verification:delivery.source_verification,crosswalk,earlier:delivery.edition_archive_provenance_v313});
 const originals=new Map(delivery.edition_archive_provenance_v313.sources.map(s=>[s.id,s]));
 assert(originals.get('TR-ROME-1564-F')?.year===1564&&originals.get('IPO-AK-1648')?.year===1648,
  'unrecognized prior edition sources');
 assert(v314.sources?.length===6&&v314.claims?.length===6&&v314.studies?.length===2,'missing source notes');
 const srcs=new Map();
 for(const s of v314.sources){
  assert(s.id&&!srcs.has(s.id)&&evidenceTiers.has(s.evidence_tier)&&s.url?.startsWith('https://'),
    'invalid source type');
  assert(s.access&&s.locator&&s.checked_on==='2026-11-06'&&s.finding&&s.not_done,
    'unqualified source inspection');
  if(s.id.includes('WESTPHALIA-LWL')||s.id==='V314-WESTPHALIA-IPO')
   assert(s.access.includes('MAINTENANCE')&&s.not_done.includes('않'),'blocked website marked read');
  srcs.set(s.id,s);
 }
 assert(srcs.has('V314-TRENT-MD243')&&srcs.has('V314-TRENT-MUSEUM')&&srcs.has('V314-WESTPHALIA-LWL741'),
 'missing museum/printed edition distinction');
 const claims=new Set();
 for(const c of v314.claims){
  assert(c.id&&!claims.has(c.id)&&['TRENT','WESTPHALIA'].includes(c.topic)&&
   c.source_ids?.length&&c.source_ids.every(id=>srcs.has(id)),'unknown source claim');
  assert(c.statement?.length>40&&c.scope&&c.guard?.length>30&&c.historian_approved===false&&
   c.original_page_collated===false,'claim overstates archival inspection');
  claims.add(c.id);
 }
 const existingStudies=new Map(delivery.edition_archive_provenance_v313.studies.map(s=>[s.id,s]));
 const studies=new Map();let totalChars=0;
 for(const a of v314.studies){
  assert(a.id&&!studies.has(a.id)&&existingStudies.has(a.parent_v313_study),'orphan study');
  assert(a.sections?.length===3&&a.source_ids?.length>=2&&
    a.source_ids.every(id=>srcs.has(id))&&a.question?.endsWith('?'),'incomplete study');
  for(const sec of a.sections){assert(sec.heading&&sec.body?.length>250,'insufficient middle-depth chapter');totalChars+=sec.body.length;}
  studies.set(a.id,a);
 }
 assert(totalChars===2017,'changed research body');
 assert(v314.scope_warnings?.length>=4,'missing source-scope caveats');
 delivery.version='3.14';
 delivery.kind='SOURCE_AUTHENTICATION_SCOPE_513_MEDIUM_EDITORIAL_PREVIEW';
 delivery.source_attestation_v314={sources:structuredClone(v314.sources),
  claims:structuredClone(v314.claims),studies:structuredClone(v314.studies),
  original_pages_inspected:0,variants_confirmed:0};
 delivery.editorial_audit.v314_source_attestation={studies:2,sections:6,new_body_characters:totalChars,
  new_sources:6,new_claims:6,physical_original_pages_read:0,
  textual_variants_confirmed:0,expert_approved:false,app_updated:false};
 delivery.editorial_note+=' / V3.14 박물관 서기·공증인 인증 흔적 및 베스트팔렌 인쇄권한의 차이. 원판 전권 미판독·공개 보류.';
 assert(JSON.stringify(original)===JSON.stringify({readers:delivery.readers,sources:delivery.sources,
  verification:delivery.source_verification,crosswalk,earlier:delivery.edition_archive_provenance_v313}),
  'prior frozen records mutated');
 assert(Object.values(delivery.publication_gate).every(v=>v===false),'publication changed');
 return {delivery,crosswalk,getAuthenticationNotesForStudy(id){
  assert(existingStudies.has(id),'unknown parent edition study');
  return structuredClone(v314.studies.filter(s=>s.parent_v313_study===id).map(s=>({
    ...s,sources:s.source_ids.map(x=>srcs.get(x)),
    evidence_cards:v314.claims.filter(c=>c.source_ids.some(x=>s.source_ids.includes(x)))})));
 }};
}
