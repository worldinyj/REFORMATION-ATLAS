/** V3.17: early treaty print, privilege and venue notes layered over the frozen V3.16 ratification chronology.
 * NOT a signed-original, manuscript, or first-print priority collation.
 */
import {assembleV316} from '../medium-atlas-v316/overlay.mjs';
const ensure=(yes,reason)=>{if(!yes)throw new Error('V317 print witnesses: '+reason);};
const requiredIds=['STETTIN','PADERBORN','UNESCO','LWL741','ARNDT','DDB1648','WS1649'];
const noteIds=['V316-STETTIN','V316-PRINT-PRIVILEGE','V316-VENUE-PRECISION'];
const issues=['STETTIN_MONTH','PRINT_VARIANTS','SIGNING_VENUE','PRINT_AUTHORITY'];
export function assembleV317(inputs,a309,a310,v311,v312,v313,v314,v315,rat316,printing317){
 const {delivery,crosswalk}=assembleV316(inputs,a309,a310,v311,v312,v313,v314,v315,rat316);
 ensure(printing317?.version==='3.17'&&printing317.status==='DRAFT'&&printing317.depth==='MEDIUM','wrong draft/version');
 ensure(printing317.publication_gate&&Object.values(printing317.publication_gate).every(x=>x===false),'publication HOLD');
 const a=printing317.inspection,m=printing317.metrics,p=printing317.preserve;
 ensure(a?.original_print_pages_collated===0&&a.original_diplomatic_pages_collated===0&&a.new_textual_variants_proven===0,'fabricated printed/original collation');
 ensure(m?.sources===7&&m.studies===3&&m.sections===9&&m.claims===10&&m.unresolved_issues===4&&m.body_characters===2350,'unapproved metrics');
 ensure(p?.readers===513&&p.sources===723&&p.overviews===97&&p.selected_claims===22&&
        p.v311_addenda===4&&p.v312_notes===2&&p.v313_studies===2&&p.v314_studies===2&&p.v315_studies===2,
        'frozen manuscript/research counts');
 ensure(delivery.readers.length===513&&delivery.sources.length===723&&
        delivery.source_verification.selected_claims.length===22&&crosswalk.entries.length===97,'legacy readers changed');
 ensure(delivery.ratification_event_v316?.chronology.length===4&&
        delivery.attestation_wording_v315?.studies.length===2,'V3.16 or V3.15 lineage lost');
 const snapshot=JSON.stringify({
  readers:delivery.readers,sources:delivery.sources,verification:delivery.source_verification,crosswalk,
  v311:delivery.primary_passage_addenda,v312:delivery.latin_english_limited_concordance_v312,
  v313:delivery.edition_archive_provenance_v313,v314:delivery.source_attestation_v314,
  v315:delivery.attestation_wording_v315,v316:delivery.ratification_event_v316,
  publication_gate:delivery.publication_gate
 });
 const src=new Map();
 ensure(printing317.source_records?.length===7,'seven source records required');
 for(const s of printing317.source_records){
  ensure(s.id&&!src.has(s.id)&&requiredIds.includes(s.id)&&['IPO','IPM','BOTH'].includes(s.work)&&
        s.url?.startsWith('https://')&&s.tier&&s.verified?.length>=35&&s.boundary?.length>=22&&
        s.original_pages_read===false,'unqualified source '+s.id);
  src.set(s.id,s);
 }
 ensure(requiredIds.every(id=>src.has(id)),'missing source identity');
 ensure(src.get('STETTIN').tier==='CATALOGUE_SEARCH_INDEX'&&
        src.get('STETTIN').boundary.includes('미검증'),'Stettin original or printing month overclaimed');
 ensure(src.get('LWL741').tier==='SCHOLARLY_SEARCH_INDEX_ONLY'&&
        src.get('LWL741').boundary.includes('유지관리'),'blocked LWL source falsely upgraded');
 ensure(src.get('PADERBORN').tier==='LIBRARY_LIVE_HTML'&&
        src.get('PADERBORN').verified.includes('VD17 12:187744L'),'Paderborn item unresolved');
 ensure(src.get('DDB1648').work==='IPM'&&src.get('PADERBORN').work==='IPO','IPO/IPM conflated');
 ensure(src.get('WS1649').tier==='EARLY_PRINT_MODERN_TRANSCRIPTION'&&
        src.get('WS1649').work==='IPM','wrong historical printer witness');
 const parentIds=new Set(delivery.attestation_wording_v315.studies.map(x=>x.id));
 const validOverviews=new Set(crosswalk.entries.map(x=>x.overview_id));
 const notes=new Map();let bodyChars=0;
 ensure(printing317.studies?.length===3,'three bounded studies required');
 for(const study of printing317.studies){
  ensure(study.id&&!notes.has(study.id)&&noteIds.includes(study.id)&&parentIds.has(study.parent_v315)&&
   study.parent_v315==='V315-SIGNING'&&study.overviews?.length>0&&study.overviews.every(id=>validOverviews.has(id))&&
   study.sources?.length>0&&study.sources.every(id=>src.has(id))&&study.question?.endsWith('?'),
   'invalid study links '+study.id);
  ensure(study.sections?.length===3&&study.sections.every(s=>s.heading&&s.body?.length>=200),
   'insufficient middle-depth text '+study.id);
  for(const section of study.sections)bodyChars+=section.body.length;
  notes.set(study.id,study);
 }
 ensure(noteIds.every(id=>notes.has(id))&&bodyChars===m.body_characters,'research body or ID drift');
 const ids=new Set();
 ensure(printing317.claim_cards?.length===10,'ten bounded claims required');
 for(const c of printing317.claim_cards){
  ensure(c.id&&!ids.has(c.id)&&c.source_ids?.length>0&&c.source_ids.every(id=>src.has(id))&&
   c.statement?.length>=35&&c.level&&c.expert_approved===false&&c.original_witness_collated===false,
   'unqualified historical assertion '+c.id);
  ids.add(c.id);
 }
 ensure(ids.size===10,'duplicate claims');
 ensure(printing317.claim_cards.find(c=>c.id==='ST-2')?.level==='INDEXED_EDITORIAL_PROBABILITY'&&
   printing317.claim_cards.find(c=>c.id==='ST-2')?.source_ids.includes('LWL741'),
   'Stettin probability falsely stated as fact');
 ensure(printing317.claim_cards.find(c=>c.id==='IP-3')?.level==='PRINTER_SELF_ATTESTATION'&&
   printing317.claim_cards.find(c=>c.id==='IP-3')?.source_ids.includes('WS1649'),
   'publisher self-claim upgraded to official act');
 ensure(printing317.claim_cards.find(c=>c.id==='VE-2')?.level==='UNRESOLVED_VENUE_DETAIL',
   'signing venue uncertainty incorrectly resolved');
 const issuesSeen=new Set();
 ensure(printing317.issues?.length===4,'unresolved-issue registry incomplete');
 for(const q of printing317.issues){
  ensure(q.id&&!issuesSeen.has(q.id)&&issues.includes(q.id)&&
  ['UNRESOLVED','NOT_COLLATED'].includes(q.status)&&q.issue,
  'unsupported resolution of historical conflict');
  issuesSeen.add(q.id);
 }
 ensure(issues.every(id=>issuesSeen.has(id)),'lost unresolved issue');
 const expectedDates=['1648-10-24','1648-10-25','1649-02-18','1649-02-21'];
 ensure(JSON.stringify(delivery.ratification_event_v316.chronology.map(x=>x.date))===
        JSON.stringify(expectedDates),'parent ratification chronology modified');
 delivery.version='3.17';
 delivery.kind='SCOPED_EARLY_TREATY_PRINT_WITNESS_513_EDITORIAL_PREVIEW';
 delivery.treaty_print_witnesses_v317={
  source_records:structuredClone(printing317.source_records),
  medium_studies:structuredClone(printing317.studies),
  claim_cards:structuredClone(printing317.claim_cards),
  unresolved_issues:structuredClone(printing317.issues),
  evidence_boundaries:{
   original_print_pages_read:0,original_diplomatic_pages_read:0,textual_variants_proven:0,
   Stettin_print_month:'PROBABLE_IN_INDEX_NOT_WITNESS_VERIFIED',
   privileged_print_status:'PRINTER_SELF_CLAIM_NOT_OFFICIAL_CRITICAL_EDITION',
   signing_venue:'NOT_ALL_PARTICIPANTS_MAPPED'
  }
 };
 delivery.editorial_audit.v317_print_witnesses={
  study_notes:3,sections:9,source_records:7,claim_cards:10,unresolved_issues:4,
  body_characters:bodyChars,original_witnesses_collated:0,historian_approved:false,actual_app_updated:false
 };
 delivery.editorial_note+=' / V3.17 슈테틴 선행 인쇄 가능성·독일어 조약 서지·정본 권위·다중 서명장소 연구 3편. 기존 513편 및 V3.16 비준 연대기는 동결.';
 ensure(JSON.stringify({
  readers:delivery.readers,sources:delivery.sources,verification:delivery.source_verification,crosswalk,
  v311:delivery.primary_passage_addenda,v312:delivery.latin_english_limited_concordance_v312,
  v313:delivery.edition_archive_provenance_v313,v314:delivery.source_attestation_v314,
  v315:delivery.attestation_wording_v315,v316:delivery.ratification_event_v316,
  publication_gate:delivery.publication_gate
 })===snapshot,'existing history/chronology changed');
 ensure(Object.values(delivery.publication_gate).every(v=>v===false),'publication released');
 return {delivery,crosswalk,getPrintStudiesForV315(id){
  ensure(parentIds.has(id),'unknown V3.15 study');
  return structuredClone(printing317.studies.filter(x=>x.parent_v315===id).map(x=>({
   ...x,source_records:x.sources.map(k=>src.get(k)),
   evidence_cards:printing317.claim_cards.filter(c=>c.source_ids.some(k=>x.sources.includes(k)))
  })));
 }};
}
