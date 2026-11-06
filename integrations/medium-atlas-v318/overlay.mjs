/** V3.18 — Actual photographed 1649 IPM pages vs 1648 *catalogue*, with zero false cross-edition variants.
 * Editorial research only. Signed diplomatic originals were NOT inspected.
 */
import {assembleV317} from '../medium-atlas-v317/overlay.mjs';
const check=(b,msg)=>{if(!b)throw new Error('V318 facsimile provenance: '+msg);};
const pageIds=['SCAN-1649-TITLE','SCAN-1649-PREFACE','SCAN-1649-PRIVILEGE'];
const pageSources=['IPM49-SCAN-TITLE','IPM49-SCAN-PREFACE','IPM49-SCAN-PRIVILEGE'];
const expectedFiles=[1,3,4], printedLabels=[null,5,6];
const sourceTiers=new Set(['DIRECT_PRINT_PAGE_SCAN_VISUALLY_INSPECTED','DIGITAL_EDITION_INDEX_AND_TRANSCRIPTION_RULES',
 'LIBRARY_METADATA_ONLY_NO_ORIGINAL_PAGE_IMAGE','LIBRARY_CATALOGUE_AND_IIIF_RANGE_METADATA_NOT_PAGE_SCAN',
 'MODERN_TRANSCRIPTION_PAIRED_TO_THREE_DIRECTLY_READ_SCAN_PAGES']);
export function assembleV318(inputs,a309,a310,v311,v312,v313,v314,v315,rat316,print317,unresolved317,scan318){
 const {delivery,crosswalk}=assembleV317(inputs,a309,a310,v311,v312,v313,v314,v315,rat316,print317);
 const oldState=JSON.stringify({
  readers:delivery.readers,sources:delivery.sources,verification:delivery.source_verification,
  overviews:crosswalk,v311:delivery.primary_passage_addenda,
  v312:delivery.latin_english_limited_concordance_v312,v313:delivery.edition_archive_provenance_v313,
  v314:delivery.source_attestation_v314,v315:delivery.attestation_wording_v315,
  v316:delivery.ratification_event_v316,v317:delivery.early_print_witness_v317,
  published:delivery.publication_gate
 });
 check(unresolved317?.version==='3.17.1'&&unresolved317.status==='DRAFT'&&
  unresolved317.metrics?.open_comparisons===2&&unresolved317.metrics.verified_variants===0&&
  unresolved317.metrics.archival_pages_collated===0,'V3.17 publication ambiguity was altered');
 check(unresolved317.unresolved_comparisons?.length===2&&
  unresolved317.unresolved_comparisons.every(x=>x.conclusion==='UNRESOLVED'&&x.primary_print_pages_collated===false),
  'publication chronology conflict marked resolved without comparison');
 check(scan318?.version==='3.18'&&scan318.status==='DRAFT'&&scan318.depth==='MEDIUM','invalid research draft');
 check(scan318.publication_gate&&Object.values(scan318.publication_gate).every(v=>v===false),'publication HOLD');
 const p=scan318.preserve,m=scan318.metrics,inspection=scan318.inspection_status;
 check(p?.readers===513&&p.sources===723&&p.overviews===97&&p.selected_claims===22&&
  p.v311_addenda===4&&p.v312_notes===2&&p.v313_studies===2&&p.v314_studies===2&&
  p.v315_studies===2&&p.v316_ratification_events===4&&p.v317_studies===3&&p.v317_claims===10,
  'frozen upstream content counts');
 check(delivery.readers.length===513&&delivery.sources.length===723&&
  delivery.source_verification.selected_claims.length===22&&crosswalk.entries.length===97,
  'legacy corpus changed');
 check(m?.sources===7&&m.inspected_scan_pages===3&&m.claim_cards===10&&m.readings===3&&
  m.sections===9&&m.open_issues===4&&m.body_characters===2841&&
  m.printed_1648_to_1649_aligned_page_pairs===0&&m.new_verified_variants===0,
  'research metrics drift');
 check(inspection?.scanned_1649_ipm_print_pages_directly_seen===3&&
  inspection.scanned_1648_ipm_print_pages_directly_seen===0&&
  inspection.scanned_1648_ipo_print_pages_directly_seen===0&&
  inspection.diplomatic_original_pages_directly_seen===0&&
  inspection.paired_1648_1649_original_print_paragraphs_collated===0&&
  inspection.confirmed_cross_edition_textual_variants===0&&
  inspection.wikisource_modern_transcription_distinguished===true,
  'fabricated 1648 or diplomatic-original page comparison');
 const src=new Map();
 check(scan318.source_records?.length===7,'seven bounded sources required');
 for(const s of scan318.source_records){
  check(s.id&&!src.has(s.id)&&['IPM','IPO'].includes(s.work)&&
   Number.isInteger(s.edition_year)&&s.url?.startsWith('https://')&&sourceTiers.has(s.kind)&&
   s.locator&&s.inspected?.length>35&&s.limit?.length>30,
   'source record or inspection missing '+s.id);
  if(s.kind==='DIRECT_PRINT_PAGE_SCAN_VISUALLY_INSPECTED')
   check(s.work==='IPM'&&s.edition_year===1649&&s.image_url?.startsWith('https://upload.wikimedia.org/'),
    '1648/other treaty incorrectly marked as direct scan');
  else check(s.image_url===null,'catalogue promoted to inspected image');
  src.set(s.id,s);
 }
 check(pageSources.every(id=>src.get(id)?.kind==='DIRECT_PRINT_PAGE_SCAN_VISUALLY_INSPECTED'),
  'three scan images not available');
 check(src.get('IPM48-BSB-DDB-CATALOGUE')?.kind==='LIBRARY_METADATA_ONLY_NO_ORIGINAL_PAGE_IMAGE'&&
  src.get('IPM48-BSB-DDB-CATALOGUE').edition_year===1648,'1648 IPM became falsely scan-verified');
 check(src.get('IPO48-PADERBORN-METADATA')?.work==='IPO'&&
  src.get('IPO48-PADERBORN-METADATA').kind==='LIBRARY_CATALOGUE_AND_IIIF_RANGE_METADATA_NOT_PAGE_SCAN',
  '1648 IPO mistakenly counted as 1648 IPM scan');
 const imageAnchors=new Map();
 check(scan318.scan_page_anchors?.length===3,'three page-anchored visuals required');
 for(const [idx,a] of scan318.scan_page_anchors.entries()){
  check(a.id===pageIds[idx]&&a.source_id===pageSources[idx]&&a.file_seq===expectedFiles[idx]&&
   a.printed_page===printedLabels[idx]&&a.image_inspected===true&&a.printed_heading&&
   a.observations?.length>=2&&a.not_established?.length>25,'scan page anchor or printed page confused');
  check(!imageAnchors.has(a.id),'duplicate image');
  imageAnchors.set(a.id,a);
 }
 check(imageAnchors.get('SCAN-1649-PREFACE').observations.some(s=>s.includes('오스나브뤼크')&&s.includes('스웨덴')),
  'IPM preface contains IPO/Sverige reference which needs interpretation guard');
 const existingParents=new Set(delivery.early_print_witness_v317.studies.map(s=>s.id));
 const overviewIds=new Set(crosswalk.entries.map(s=>s.overview_id));
 const notes=new Map();let chars=0;
 check(scan318.medium_readings?.length===3,'three reading notes missing');
 for(const n of scan318.medium_readings){
  check(n.id&&!notes.has(n.id)&&existingParents.has(n.parent_v317)&&
   n.overview_ids?.length>0&&n.overview_ids.every(id=>overviewIds.has(id))&&
   n.source_ids?.length>0&&n.source_ids.every(id=>src.has(id))&&n.question?.endsWith('?'),
   'orphan manuscript reading');
  check(n.sections?.length===3&&n.sections.every(s=>s.heading&&s.body?.length>=220),
   'medium depth reading section missing');
  chars+=n.sections.reduce((sum,s)=>sum+s.body.length,0);
  notes.set(n.id,n);
 }
 check(chars===m.body_characters,'reading body checksum mismatch');
 const cards=new Set();
 check(scan318.historical_claim_cards?.length===10,'claims incomplete');
 for(const c of scan318.historical_claim_cards){
  check(c.id&&!cards.has(c.id)&&c.statement?.length>=35&&c.scope&&c.evidence&&
   c.source_ids?.length>0&&c.source_ids.every(id=>src.has(id))&&
   c.original_diplomatic_witness_collated===false&&c.expert_approved===false,'orphan or falsely approved claim');
  cards.add(c.id);
 }
 check(scan318.historical_claim_cards.find(c=>c.id==='V318-C08')?.evidence==='CROSS_LEVEL_CATALOGUE_VS_SCAN'&&
  scan318.historical_claim_cards.find(c=>c.id==='V318-C08')?.source_ids.includes('IPM48-BSB-DDB-CATALOGUE'),
  '1648/1649 mixed evidence comparison wrongly upgraded');
 check(scan318.historical_claim_cards.find(c=>c.id==='V318-C05')?.evidence==='VISUALLY_READ_PRINT_SCAN_WITH_SCOPE_GUARD'&&
  scan318.historical_claim_cards.find(c=>c.id==='V318-C05')?.source_ids.includes('IPM49-SCAN-PREFACE'),
  'Osnabrück/Sweden preface interpreted as IPM treaty party');
 check(scan318.open_issues?.length===4&&
  scan318.open_issues.every(o=>o.status!=='RESOLVED'&&o.variant_claim_prohibited===true&&o.evidence_needed),
  'uninspected counterpart print marked collated');
 check(scan318.methods?.length>=5,'source-critical safeguards missing');
 const chronology=delivery.ratification_event_v316.chronology.map(x=>x.date);
 check(JSON.stringify(chronology)===JSON.stringify(['1648-10-24','1648-10-25','1649-02-18','1649-02-21']),
  'verified ratification timeline changed');
 delivery.version='3.18';
 delivery.kind='PHYSICAL_1649_IPM_PRINT_PAGE_ANCHORS_513_EDITORIAL_PREVIEW';
 delivery.physical_ipm_scan_evidence_v318={
  source_records:structuredClone(scan318.source_records),
  scan_pages:structuredClone(scan318.scan_page_anchors),
  medium_readings:structuredClone(scan318.medium_readings),
  historical_claim_cards:structuredClone(scan318.historical_claim_cards),
  unresolved_issues:structuredClone(scan318.open_issues),
  prior_v317_publication_conflicts:structuredClone(unresolved317.unresolved_comparisons),
  comparison_status:structuredClone(inspection)
 };
 delivery.editorial_audit.v318_ipm_print_images={
  visually_inspected_printed_pages_1649:3,
  inspected_printed_pages_1648:0,
  direct_diplomatic_originals_read:0,
  matched_1648_1649_paragraphs:0,
  verified_cross_edition_variants:0,
  medium_readings:3,sections:9,claim_cards:10,open_issues:4,
  historian_approved:false,actual_app_updated:false
 };
 delivery.editorial_note+=' / V3.18 IPM 1649 표제·독자 서문·인쇄특허 사진 3면 실제 검토; IPM 1648은 서지만 확인. 직접 교감한 1648·1649 이문 0건.';
 check(JSON.stringify({
  readers:delivery.readers,sources:delivery.sources,verification:delivery.source_verification,
  overviews:crosswalk,v311:delivery.primary_passage_addenda,
  v312:delivery.latin_english_limited_concordance_v312,v313:delivery.edition_archive_provenance_v313,
  v314:delivery.source_attestation_v314,v315:delivery.attestation_wording_v315,
  v316:delivery.ratification_event_v316,v317:delivery.early_print_witness_v317,
  published:delivery.publication_gate
 })===oldState,'prior manuscripts or corroborated chronology mutated');
 check(Object.values(delivery.publication_gate).every(x=>x===false),'public release unlocked');
 return {delivery,crosswalk,
  getScansForEdition(work,year){
   check(work==='IPM'||work==='IPO','unknown treaty');
   check(Number.isInteger(year),'edition year required');
   const selected=scan318.source_records.filter(x=>x.work===work&&x.edition_year===year);
   return structuredClone({
    record_count:selected.length,
    image_scans:selected.filter(s=>s.kind==='DIRECT_PRINT_PAGE_SCAN_VISUALLY_INSPECTED'),
    catalogue_only:selected.filter(s=>s.kind!=='DIRECT_PRINT_PAGE_SCAN_VISUALLY_INSPECTED'),
    scan_page_anchors:scan318.scan_page_anchors.filter(a=>selected.some(s=>s.id===a.source_id))
   });
  },
  getResearchForV317(id){
   check(existingParents.has(id),'unknown V3.17 parent');
   return structuredClone(scan318.medium_readings.filter(x=>x.parent_v317===id));
  }
 };
}
