/** Two scoped Latin/English textual comparison readings; no archival original images examined. */
import {assembleV311} from '../medium-atlas-v311/overlay.mjs';
const ensure=(v,m)=>{if(!v)throw Error('V312 Latin concordance: '+m);};
const knownLevels=new Set(['MODERN_ONLINE_LATIN_TRANSCRIPTION_OF_LATER_PRINT','MODERN_ONLINE_LATIN_TRANSCRIPTION_OF_HISTORICAL_TREATY','LATER_ENGLISH_TRANSLATION','CURATED_LATER_TRANSLATED_EXCERPT']);
export function assembleV312(inputs,sourceAudit,qualityAudit,v311,v312){
 const prev=assembleV311(inputs,sourceAudit,qualityAudit,v311);
 const {delivery:b,crosswalk:x}=prev;
 ensure(v312?.version==='3.12'&&v312.status==='DRAFT'&&v312.depth==='MEDIUM','invalid draft');
 ensure(v312.publication_gate&&Object.values(v312.publication_gate).every(x=>x===false),'publication HOLD');
 ensure(v312.metrics?.new_medium_reading_notes===2&&v312.metrics.new_sections===6&&v312.metrics.paired_latin_english_claims===4&&v312.metrics.source_records===5&&v312.metrics.base_reader_count===513&&v312.metrics.v311_addendum_count===4&&v312.metrics.v311_claim_count===12&&v312.metrics.original_archival_witness_collations===0,'metrics contract');
 const beforeReaders=JSON.stringify(b.readers),beforeSources=JSON.stringify(b.sources),beforeClaims=JSON.stringify(b.source_verification),beforeCrosswalk=JSON.stringify(x);
 const baseClaims=new Set(b.primary_passage_claims.map(c=>c.id)),baseAddenda=new Set(b.primary_passage_addenda.map(a=>a.id)),baseOverview=new Set(x.entries.map(e=>e.overview_id));
 ensure(baseClaims.size===12&&baseAddenda.size===4&&baseOverview.size===97,'parent corpus mismatch');
 const sources=new Map(),readings=new Map(),ids=new Set();
 ensure(v312.source_records?.length===5&&v312.medium_readings?.length===2&&v312.concordance_cards?.length===4,'incomplete Latin source set');
 for(const s of v312.source_records){
   ensure(s.id&&!sources.has(s.id)&&s.url?.startsWith('https://')&&knownLevels.has(s.evidence_level)&&s.inspection_note,'invalid source');
   ensure(s.original_1547_1563_witness_collated===false||s.original_1547_1563_witness_collated===undefined,'false original witness flag');
   ensure(s.original_1648_witness_collated===false||s.original_1648_witness_collated===undefined,'false 1648 witness flag');
   sources.set(s.id,s);
 }
 let sumChars=0;
 for(const a of v312.medium_readings){
   ensure(a.id&&!readings.has(a.id)&&baseAddenda.has(a.parent_addendum)&&a.sections?.length===3&&a.question?.endsWith('?'),'invalid reading');
   ensure(a.overview_ids?.every(id=>baseOverview.has(id)),'unresolved overview');
   for(const sec of a.sections){ensure(sec.heading&&sec.body?.length>=200,'too-short essay section');sumChars+=sec.body.length;}
   readings.set(a.id,a);
 }
 ensure(sumChars===v312.metrics.new_body_characters,'body content drift');
 for(const c of v312.concordance_cards){
   ensure(c.id&&!ids.has(c.id)&&readings.has(c.reading_id)&&baseClaims.has(c.parent_v311_claim),'invalid paired claim');
   ids.add(c.id);
   ensure(sources.has(c.latin_source_id)&&sources.get(c.latin_source_id).language==='la','missing Latin transcription');
   ensure(sources.has(c.english_source_id)&&sources.get(c.english_source_id).language==='en','missing English translation');
   ensure(c.original_fragment?.length>15&&c.original_fragment.split(/\s+/).length<13&&c.original_language==='la','invalid short fragment');
   ensure(c.latin_locator&&c.english_locator&&c.interpretation_ko&&c.limits&&c.original_witness_collated===false,'unqualified evidence');
 }
 ensure(ids.size===4&&readings.size===2&&sources.size===5,'ID count mismatch');
 b.version='3.12';b.kind='LATIN_TRANSCRIPTION_COMPARISON_513_EDITORIAL_BUNDLE';
 b.latin_english_limited_concordance_v312={source_records:structuredClone(v312.source_records),
   medium_readings:structuredClone(v312.medium_readings),claim_cards:structuredClone(v312.concordance_cards)};
 b.editorial_audit.v312_latin_concordance={scoped_readings:2,sections:6,paired_claims:4,source_records:5,
   new_body_characters:sumChars,archival_original_collations:0,expert_approved:false,app_updated:false};
 b.editorial_note+=' / V3.12 라틴어 후대 편집 전사·영어 번역 구절 대조 2편. 역사 원판 이미지·서명 필사본은 미확인.';
 ensure(JSON.stringify(b.readers)===beforeReaders&&JSON.stringify(b.sources)===beforeSources&&JSON.stringify(b.source_verification)===beforeClaims&&JSON.stringify(x)===beforeCrosswalk,'prior material changed');
 ensure(Object.values(b.publication_gate).every(x=>x===false),'unexpected publication');
 const getLatinNotesForAddendum=id=>{
   ensure(baseAddenda.has(id),'unknown parent addendum');
   return structuredClone(v312.medium_readings.filter(r=>r.parent_addendum===id).map(r=>({...r,
     claim_cards:v312.concordance_cards.filter(c=>c.reading_id===r.id)})));
 };
 return {delivery:b,crosswalk:x,getLatinNotesForAddendum};
}
