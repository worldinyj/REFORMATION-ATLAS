import {assembleV315} from '../medium-atlas-v315/overlay.mjs';
const assert=(value,message)=>{if(!value)throw Error('V316 chronology: '+message);};
const DATE_TYPES=new Map([
 ['1648-10-24','SIGNING_AND_SEALING'],['1648-10-25','PUBLIC_PROCLAMATION'],
 ['1649-02-18','ACTUAL_RATIFICATION_EXCHANGE'],['1649-02-21','PUBLIC_RATIFICATION_CELEBRATION']
]);
const LEVELS=new Set(['ARCHIVAL_HOLDING_INSTITUTION_METADATA','HISTORICAL_TREATY_EDITED_TRANSLATION_INDEX_ONLY','HISTORIAN_AUTHORED_MODERN_SECONDARY','HISTORIAN_AUTHORED_REGIONAL_EVENT_NARRATIVE','ACADEMIC_HISTORICAL_CRITICAL_EDITION_DISCOVERY_METADATA']);
export function assembleV316(inputs,a309,a310,v311,v312,v313,v314,v315,rat316){
 const prev=assembleV315(inputs,a309,a310,v311,v312,v313,v314,v315);
 const {delivery,crosswalk}=prev;
 assert(rat316?.version==='3.16'&&rat316.status==='DRAFT'&&rat316.depth==='MEDIUM','invalid version or depth');
 assert(rat316.publication_gate&&Object.values(rat316.publication_gate).every(x=>x===false),'publication HOLD');
 assert(rat316.inspection?.original_treaty_pages_viewed===0&&rat316.inspection.verified_textual_variants===0&&rat316.inspection.live_ipm_treaty_fulltext_read===false,'invented original treaty inspection');
 assert(rat316.preserve?.readers===513&&rat316.preserve.sources===723&&rat316.preserve.overviews===97&&
 rat316.preserve.selected_claims===22&&rat316.preserve.v315_readings===2&&rat316.preserve.v315_claims===8,'legacy baseline drift');
 const m=rat316.metrics;
 assert(m?.sources===5&&m.claims===5&&m.chronology_events===4&&m.readings===1&&m.sections===3&&m.body_characters===1055,'ratification scope metrics mismatch');
 assert(delivery.readers.length===513&&delivery.sources.length===723&&delivery.source_verification.selected_claims.length===22&&crosswalk.entries.length===97,'corpus baseline incorrect');
 assert(delivery.attestation_wording_v315.studies.length===2&&delivery.attestation_wording_v315.claims.length===8,'parent V315 changed');
 const frozen=JSON.stringify({
 readers:delivery.readers,sources:delivery.sources,claims:delivery.source_verification,crosswalk,
 v315:delivery.attestation_wording_v315,v314:delivery.source_attestation_v314,
 v313:delivery.edition_archive_provenance_v313,v312:delivery.latin_english_limited_concordance_v312,
 v311:delivery.primary_passage_addenda
 });
 const sources=new Map();
 assert(rat316.source_records?.length===5&&rat316.claim_cards?.length===5&&rat316.chronology?.length===4,'incomplete source data');
 for(const s of rat316.source_records){
   assert(s.id&&!sources.has(s.id)&&s.url?.startsWith('https://')&&LEVELS.has(s.tier)&&s.locator&&s.access&&s.finding&&s.limit,'source qualification missing');
   sources.set(s.id,s);
 }
 const archive=sources.get('V316-ARCHIVE-IPM'),indexed=sources.get('V316-IPM-PARAGRAPHS');
 assert(archive?.access.includes('NO_PREVIEW_IMAGES')&&archive.locator.includes('34 aufgedrückte Siegel'),'improper archival seal count');
 assert(indexed?.access.includes('MAINTENANCE')&&indexed.tier==='HISTORICAL_TREATY_EDITED_TRANSLATION_INDEX_ONLY','inaccessible text promoted to direct full source');
 const eventDates=new Set(),eventTypes=new Set();
 for(const entry of rat316.chronology){
  assert(!eventDates.has(entry.date)&&DATE_TYPES.get(entry.date)===entry.type,'unverified date or conflated event');
  assert(entry.source_ids?.length&&entry.source_ids.every(s=>sources.has(s)),'chronology has missing source');
  eventDates.add(entry.date);eventTypes.add(entry.type);
 }
 assert(eventDates.size===4&&eventTypes.size===4,'missing chronology phase');
 const ids=new Set();
 for(const card of rat316.claim_cards){
  assert(card.id&&!ids.has(card.id)&&card.claim?.length>=35&&card.avoid&&card.evidence_tier&&
  card.source_ids?.length&&card.source_ids.every(s=>sources.has(s)),'unsupported claim');
  assert(card.source_images_inspected===false&&card.historian_approved===false,'unfounded expert source approval');
  ids.add(card.id);
 }
 const reading=rat316.reading,baseParents=new Set(delivery.attestation_wording_v315.studies.map(s=>s.id)),validOverviews=new Set(crosswalk.entries.map(r=>r.overview_id));
 assert(reading?.id==='V316-IPM-RATIFICATION-CHRONOLOGY'&&baseParents.has(reading.parent_v315)&&reading.parent_v315==='V315-SIGNING','unlinked study parent');
 assert(reading.overview_ids?.every(x=>validOverviews.has(x))&&reading.source_ids?.every(s=>sources.has(s))&&reading.question?.endsWith('?'),'invalid reading links');
 assert(reading.sections?.length===3&&reading.sections.every(s=>s.heading&&s.body?.length>=270),'incomplete medium prose');
 assert(reading.sections.reduce((n,s)=>n+s.body.length,0)===m.body_characters,'research body checksum mismatch');
 assert(rat316.claim_cards.find(c=>c.id==='V316-C01')?.source_ids.includes('V316-IPM-PARAGRAPHS'),'eight-week promise source missing');
 assert(rat316.claim_cards.find(c=>c.id==='V316-C02')?.source_ids.includes('V316-LEXICON-EXECUTION'),'Feb 18 actual exchange source missing');
 assert(rat316.claim_cards.find(c=>c.id==='V316-C03')?.source_ids.includes('V316-LWL-FESTIVAL'),'Feb 21 celebration source missing');
 delivery.version='3.16';delivery.kind='RATIFICATION_TIMELINE_SCOPED_513_EDITORIAL_PREVIEW';
 delivery.ratification_event_v316={sources:structuredClone(rat316.source_records),claims:structuredClone(rat316.claim_cards),chronology:structuredClone(rat316.chronology),reading:structuredClone(reading)};
 delivery.editorial_audit.v316_ratification={research_readings:1,sections:3,chronology_events:4,claims:5,original_pages_inspected:0,source_variants_verified:0,historian_approved:false,webapp_changed:false};
 delivery.editorial_note+=' / V3.16 1648 서명·공표, 1649 비준 교환·축제를 날짜별로 분리. 원고 및 원전 검증 상태 유지.';
 assert(JSON.stringify({
 readers:delivery.readers,sources:delivery.sources,claims:delivery.source_verification,crosswalk,
 v315:delivery.attestation_wording_v315,v314:delivery.source_attestation_v314,
 v313:delivery.edition_archive_provenance_v313,v312:delivery.latin_english_limited_concordance_v312,
 v311:delivery.primary_passage_addenda
 })===frozen,'frozen data mutated');
 assert(Object.values(delivery.publication_gate).every(x=>x===false),'delivery publication released');
 return {delivery,crosswalk,getRatificationReadingForV315(id){
   assert(baseParents.has(id),'unknown V315 reader');
   return structuredClone(id===reading.parent_v315?[{...reading,sources:reading.source_ids.map(x=>sources.get(x)),claim_cards:rat316.claim_cards}]:[]);
 }};
}
