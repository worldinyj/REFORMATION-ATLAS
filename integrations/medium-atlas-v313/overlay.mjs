/** V3.13 edition/provenance metadata layer. No original witness collation or publication. */
import {assembleV312} from '../medium-atlas-v312/overlay.mjs';
const check=(x,msg)=>{if(!x)throw Error('V313 provenance: '+msg);};
const ALLOWED=new Set(['ROME_FOLIO_CATALOGUE','ROME_QUARTO_CATALOGUE','DILLINGEN_EARLY_PRINT_CATALOGUE','LATER_PRINT_TRANSCRIPTION_BASIS','ARCHIVAL_ORIGINAL_HOLDING_RECORD','DIGITIZED_LATER_LATIN_PRINT_CATALOGUE','CONTEMPORARY_GERMAN_PRINT_CATALOGUE','EARLY_PRINT_ONLINE_TRANSCRIPTION','MODERN_FACSIMILE_PUBLISHER_RECORD','CRITICAL_EDITION_DISCOVERY','HISTORICAL_EDITORIAL_INDEX_ONLY']);
export function assembleV313(inputs,audit309,audit310,addon311,latin312,edition313){
 const v312=assembleV312(inputs,audit309,audit310,addon311,latin312);
 const {delivery,crosswalk}=v312;
 check(edition313?.version==='3.13'&&edition313.status==='DRAFT'&&edition313.depth==='MEDIUM','bad edition data version');
 check(edition313.publication_gate&&Object.values(edition313.publication_gate).every(v=>v===false),'edition HOLD missing');
 check(delivery.publication_gate&&Object.values(delivery.publication_gate).every(v=>v===false),'prior HOLD missing');
 const oldReaders=JSON.stringify(delivery.readers),oldSources=JSON.stringify(delivery.sources);
 const oldVerification=JSON.stringify(delivery.source_verification),oldOverview=JSON.stringify(crosswalk);
 const oldV311=JSON.stringify(delivery.primary_passage_addenda),oldV312=JSON.stringify(delivery.latin_english_limited_concordance_v312);
 const m=edition313.metrics;
 check(m?.studies===2&&m.sections===6&&m.records===11&&m.relations===8&&m.claims===9&&m.body_characters===1812&&m.verified_textual_variants===0&&m.original_pages_collated===0,'edition metrics out of scope');
 check(delivery.readers.length===513&&delivery.sources.length===723&&delivery.source_verification?.selected_claims?.length===22&&crosswalk.entries.length===97,'frozen historical base changed');
 check(delivery.primary_passage_addenda?.length===4&&delivery.primary_passage_claims?.length===12,'v311 base changed');
 check(delivery.latin_english_limited_concordance_v312?.medium_readings?.length===2&&delivery.latin_english_limited_concordance_v312?.claim_cards?.length===4,'v312 base changed');
 check(edition313.sources?.length===11&&edition313.relations?.length===8&&edition313.provenance_claims?.length===9&&edition313.studies?.length===2,'missing records');
 const sources=new Map();
 for(const s of edition313.sources){
  check(s.id&&!sources.has(s.id)&&ALLOWED.has(s.role)&&typeof s.url==='string'&&s.url.startsWith('https://'),'bad/duplicate source');
  check(s.source_verified_scope==='METADATA_OR_INDEX_ONLY'&&s.original_pages_collated===false,'false page inspection');
  check(Number.isInteger(s.year)&&s.year>=1500&&s.year<=2026&&s.record_id&&s.bibliography&&s.inspected&&s.not_inspected,'incomplete source provenance');
  sources.set(s.id,s);
 }
 check(sources.get('TR-ROME-1564-F')?.year===1564&&sources.get('TR-ROME-1564-Q')?.year===1564&&sources.get('TR-DILLINGEN-1564')?.year===1564&&sources.get('TR-PADUA-1738')?.year===1738,'Trent edition chronology drift');
 check(sources.get('IPO-AK-1648')?.year===1648&&sources.get('IPO-LATIN-1650')?.year===1650&&sources.get('IPM-GERMAN-1648')?.year===1648&&sources.get('IPM-GERMAN-1649')?.year===1649,'Westphalia publication date drift');
 check(sources.get('IPO-AK-1648').role==='ARCHIVAL_ORIGINAL_HOLDING_RECORD'&&sources.get('IPO-LATIN-1650').role==='DIGITIZED_LATER_LATIN_PRINT_CATALOGUE','archival original confused with printing');
 check(sources.get('IPO-AK-1648').work_id==='IPO'&&sources.get('IPM-GERMAN-1648').work_id==='IPM','confused IPO and IPM');
 check(sources.get('LWL-PRINT-CAUTION')?.role==='HISTORICAL_EDITORIAL_INDEX_ONLY'&&sources.get('LWL-PRINT-CAUTION').inspected.includes('검색 색인'),'inaccessible portal promoted to original');
 const seenRelation=new Set();
 for(const [i,e] of edition313.relations.entries()){
  check(e.from!==e.to&&sources.has(e.from)&&sources.has(e.to)&&e.type&&e.note&&e.variant_proven===false,'false edition genealogy '+i);
  const id=[e.from,e.to].join('->');check(!seenRelation.has(id),'duplicate edition link');seenRelation.add(id);
 }
 check(edition313.relations.some(e=>e.type==='DIFFERENT_TREATIES_NOT_EDITION'&&sources.get(e.from).work_id==='IPO'&&sources.get(e.to).work_id==='IPM'),'missing separate treaties warning');
 const seenClaim=new Set();
 for(const c of edition313.provenance_claims){
  check(c.id&&!seenClaim.has(c.id)&&c.source_ids?.length&&c.source_ids.every(id=>sources.has(id)),'bad source claim');
  check(c.statement?.length>=30&&c.guard?.length>=20&&c.evidence==='BIBLIOGRAPHIC_CATALOGUE_OR_SCHOLARLY_INDEX','overstated claim');
  check(c.expert_approved===false&&c.original_witness_collated===false,'false expert validation');
  seenClaim.add(c.id);
 }
 const notes=new Map(),v312NoteIds=new Set(delivery.latin_english_limited_concordance_v312.medium_readings.map(x=>x.id));
 const overviewIds=new Set(crosswalk.entries.map(x=>x.overview_id));
 let total=0;
 for(const s of edition313.studies){
  check(s.id&&!notes.has(s.id)&&v312NoteIds.has(s.parent_latin_note)&&s.overview_ids?.every(id=>overviewIds.has(id)),'bad study parent');
  check(s.source_ids?.length&&s.source_ids.every(id=>sources.has(id))&&s.question?.endsWith('?'),'missing study source');
  check(s.sections?.length===3,'section number');
  for(const sec of s.sections){check(sec.heading&&sec.body?.length>=200,'short section');total+=sec.body.length;}
  notes.set(s.id,s);
 }
 check(total===m.body_characters,'changed body bytes');
 check(edition313.preserve?.readers===513&&edition313.preserve.sources===723&&edition313.preserve.selected_claims===22&&edition313.preserve.overviews===97,'publication snapshot drift');
 delivery.version='3.13';
 delivery.kind='EDITORIAL_EDITION_ARCHIVE_PROVENANCE_PREVIEW';
 delivery.edition_archive_provenance_v313={sources:structuredClone(edition313.sources),relations:structuredClone(edition313.relations),claims:structuredClone(edition313.provenance_claims),studies:structuredClone(edition313.studies)};
 delivery.editorial_audit.v313_edition_archive={
  source_catalogue_records:11,study_notes:2,sections:6,bibliographic_claims:9,edition_relations:8,
  historical_text_variants_verified:0,original_pages_collated:0,expert_approved:false,actual_app_updated:false,
  caution:'Catalogue/index metadata alone do not establish textual variants or archival-original inspection.'
 };
 delivery.editorial_note+=' / V3.13 1564·1648–1650 원전 보존·인쇄판 계보 11건. 513편 원고와 출판 상태는 동결.';
 check(JSON.stringify(delivery.readers)===oldReaders&&JSON.stringify(delivery.sources)===oldSources&&JSON.stringify(delivery.source_verification)===oldVerification,'frozen content drift');
 check(JSON.stringify(crosswalk)===oldOverview&&JSON.stringify(delivery.primary_passage_addenda)===oldV311&&JSON.stringify(delivery.latin_english_limited_concordance_v312)===oldV312,'previous research drift');
 check(Object.values(delivery.publication_gate).every(v=>v===false),'HOLD unexpectedly lifted');
 return {delivery,crosswalk,getEditionSourcesForStudy:id=>{
  check(notes.has(id),'unknown V313 study');return structuredClone(notes.get(id).source_ids.map(s=>sources.get(s)));
 }};
}
