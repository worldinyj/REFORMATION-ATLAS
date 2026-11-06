import {assembleV314} from '../medium-atlas-v314/overlay.mjs';
const ok=(x,m)=>{if(!x)throw Error('V315 wording: '+m);};
const latin=['cum originalibus contulimus','cum eis concordare reperimus','manu propria subscripsimus','Ego Angelus Massarellus'];
export function assembleV315(inputs,a309,a310,v311,v312,v313,v314,v315){
 const {delivery,crosswalk}=assembleV314(inputs,a309,a310,v311,v312,v313,v314);
 const m=v315?.metrics,p=v315?.preserve,inspection=v315?.inspection;
 ok(v315?.version==='3.15'&&v315.status==='DRAFT'&&v315.depth==='MEDIUM','invalid draft');
 ok(v315.publication_gate&&Object.values(v315.publication_gate).every(v=>v===false),'publication HOLD');
 ok(m?.readings===2&&m.sections===6&&m.sources===2&&m.claims===8&&m.latin_fragments===4&&m.body_characters===1590,'count drift');
 ok(p?.readers===513&&p.sources===723&&p.overviews===97&&p.selected_claims===22&&p.v314_studies===2,'preservation baseline');
 ok(inspection?.original_museum_pages===0&&inspection.original_treaty_pages===0&&inspection.variant_readings_proven===0,'false original collation');
 const old=JSON.stringify({readers:delivery.readers,sources:delivery.sources,verification:delivery.source_verification,
  crosswalk,v314:delivery.source_attestation_v314,v313:delivery.edition_archive_provenance_v313});
 ok(delivery.readers.length===513&&delivery.sources.length===723&&crosswalk.entries.length===97,'inherited counts');
 ok(v315.source_records?.length===2&&v315.reading_notes?.length===2&&v315.claim_cards?.length===8,'missing research data');
 const src=new Map(v315.source_records.map(x=>[x.id,x]));
 ok(src.size===2&&src.get('MUSEUM-1564')?.kind==='MUSEUM_TRANSCRIPTION_OF_LATIN_ATTESTATION'&&
  src.get('MUSEUM-1564').access==='FULL_HTML_READ'&&
  src.get('ARNDT-1648')?.kind==='MODERN_HISTORIAN_SECONDARY_NARRATIVE'&&
  src.get('ARNDT-1648').access==='FULL_HTML_PRINT_VIEW_READ','invalid web source provenance');
 const parents=new Set(delivery.source_attestation_v314.studies.map(x=>x.id)),overview=new Set(crosswalk.entries.map(x=>x.overview_id));
 const notes=new Map();let chars=0;
 for(const n of v315.reading_notes){
  ok(n.id&&!notes.has(n.id)&&parents.has(n.parent_v314)&&n.overview_ids?.every(id=>overview.has(id))&&
   n.source_ids?.every(id=>src.has(id))&&n.sections?.length===3&&n.question?.endsWith('?'),'unresolved study');
  for(const s of n.sections){ok(s.heading&&s.body?.length>=170,'short text');chars+=s.body.length;}
  notes.set(n.id,n);
 }
 ok(chars===m.body_characters&&notes.size===2,'body drift');
 ok(notes.get('V315-ATTESTATION')?.parent_v314==='V314-MASSARELLI-AUTHENTICATION','Trent parent mismatch');
 ok(notes.get('V315-SIGNING')?.parent_v314==='V314-PRINT-AUTHORITY-WESTPHALIA','Westphalia parent mismatch');
 const claims=new Set();
 for(const c of v315.claim_cards){
  ok(c.id&&!claims.has(c.id)&&notes.has(c.reading_id)&&src.has(c.source_id)&&c.meaning&&
   c.expert_approved===false&&c.original_witness_collated===false,'invalid claim');
  claims.add(c.id);
  if(c.id.startsWith('L')){
   ok(c.reading_id==='V315-ATTESTATION'&&c.source_id==='MUSEUM-1564'&&
    c.latin_fragment===latin[Number(c.id.slice(1))-1]&&c.source_layer==='MUSEUM_TRANSCRIBED_LATIN','unverified Latin');
  } else ok(c.reading_id==='V315-SIGNING'&&c.source_id==='ARNDT-1648'&&
   c.latin_fragment===null&&c.source_layer==='MODERN_HISTORIAN_ACCOUNT','secondary evidence promoted');
 }
 ok(claims.size===8,'duplicate claims');
 delivery.version='3.15';delivery.kind='SCOPED_ATTESTATION_SIGNING_EDITORIAL_PREVIEW';
 delivery.attestation_wording_v315={sources:structuredClone(v315.source_records),
  studies:structuredClone(v315.reading_notes),claims:structuredClone(v315.claim_cards)};
 delivery.editorial_audit.v315_wording={studies:2,sections:6,claims:8,source_pages:2,
  original_pages_inspected:0,variants_proven:0,expert_approved:false,app_updated:false};
 ok(JSON.stringify({readers:delivery.readers,sources:delivery.sources,verification:delivery.source_verification,
  crosswalk,v314:delivery.source_attestation_v314,v313:delivery.edition_archive_provenance_v313})===old,'frozen corpus changed');
 ok(Object.values(delivery.publication_gate).every(v=>v===false),'release gate changed');
 return {delivery,crosswalk,getForV314:id=>{
  ok(parents.has(id),'unknown V314 parent');
  return structuredClone(v315.reading_notes.filter(n=>n.parent_v314===id).map(n=>({
   ...n,sources:n.source_ids.map(s=>src.get(s)),
   claims:v315.claim_cards.filter(c=>c.reading_id===n.id)
  })));
 }};
}
