import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {assembleV317} from '../medium-atlas-v317/overlay.mjs';
import {assembleV318} from './overlay.mjs';
const bytes=p=>readFileSync(new URL('../../'+p,import.meta.url));
const read=p=>JSON.parse(bytes(p));
const m=read('integrations/medium-atlas-v318/manifest.json');
const inputs=m.inputs.map(x=>read(x.path)),audits=m.auditInputs.map(x=>read(x.path));
const [v311,v312,v313,v314,v315,rat316,print317,conflict317,scan318]=[
 m.addendumInput,m.latinInput,m.editionInput,m.authInput,m.wordingInput,
 m.ratificationInput,m.witnessPrintInput,m.printingConflictInput,m.scanInput
].map(x=>read(x.path));
const prev=assembleV317(inputs,...audits,v311,v312,v313,v314,v315,rat316,print317);
const next=assembleV318(inputs,...audits,v311,v312,v313,v314,v315,rat316,print317,conflict317,scan318);
const invalid=fn=>{const x=structuredClone(scan318);fn(x);
 return ()=>assembleV318(inputs,...audits,v311,v312,v313,v314,v315,rat316,print317,conflict317,x);
};
test('all 4 canonical inputs, audits and every research extension use pinned digest',()=>{
 for(const x of [...m.inputs,...m.auditInputs,m.addendumInput,m.latinInput,m.editionInput,
  m.authInput,m.wordingInput,m.ratificationInput,m.witnessPrintInput,m.printingConflictInput,m.scanInput]){
  const b=bytes(x.path);
  if(x.sha256)assert.equal(createHash('sha256').update(b).digest('hex'),x.sha256,x.path);
  if(x.gitBlobSha1)assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex'),x.gitBlobSha1,x.path);
 }
});
test('original 513 readers, 723 sources, 97 overviews, selected 22 claims and V311-317 are unchanged',()=>{
 for(const k of ['readers','sources','source_verification','primary_passage_addenda','primary_passage_claims',
  'latin_english_limited_concordance_v312','edition_archive_provenance_v313',
  'source_attestation_v314','attestation_wording_v315','ratification_event_v316','early_print_witness_v317'])
  assert.deepEqual(next.delivery[k],prev.delivery[k],k);
 assert.deepEqual(next.crosswalk,prev.crosswalk);
 assert.deepEqual(next.delivery.ratification_event_v316.chronology.map(x=>x.date),[
  '1648-10-24','1648-10-25','1649-02-18','1649-02-21']);
 assert.equal(next.delivery.publication_gate.published,false);
});
test('exactly three 1649 printed scan images were visually inspected with page labels 1/5/6 context',()=>{
 assert.deepEqual(scan318.scan_page_anchors.map(p=>p.file_seq),[1,3,4]);
 assert.deepEqual(scan318.scan_page_anchors.map(p=>p.printed_page),[null,5,6]);
 assert.ok(scan318.scan_page_anchors.every(p=>p.image_inspected===true));
 const images=scan318.source_records.filter(x=>x.kind==='DIRECT_PRINT_PAGE_SCAN_VISUALLY_INSPECTED');
 assert.equal(images.length,3);
 assert.ok(images.every(x=>x.work==='IPM'&&x.edition_year===1649&&x.image_url.startsWith('https://upload.wikimedia.org/')));
 assert.equal(scan318.inspection_status.scanned_1648_ipm_print_pages_directly_seen,0);
 assert.equal(scan318.inspection_status.paired_1648_1649_original_print_paragraphs_collated,0);
 assert.equal(scan318.inspection_status.confirmed_cross_edition_textual_variants,0);
});
test('1648 IPM library catalogue and 1648 IPO IIIF manifest are not falsely promoted to inspected IPM pages',()=>{
 const src=new Map(scan318.source_records.map(x=>[x.id,x]));
 assert.equal(src.get('IPM48-BSB-DDB-CATALOGUE').kind,'LIBRARY_METADATA_ONLY_NO_ORIGINAL_PAGE_IMAGE');
 assert.equal(src.get('IPM48-BSB-DDB-CATALOGUE').image_url,null);
 assert.equal(src.get('IPO48-PADERBORN-METADATA').work,'IPO');
 assert.equal(src.get('IPO48-PADERBORN-METADATA').image_url,null);
 const ipm49=next.getScansForEdition('IPM',1649);
 const ipm48=next.getScansForEdition('IPM',1648);
 const ipo48=next.getScansForEdition('IPO',1648);
 assert.equal(ipm49.image_scans.length,3);
 assert.equal(ipm48.image_scans.length,0);
 assert.equal(ipm48.catalogue_only.length,1);
 assert.equal(ipo48.image_scans.length,0);
 assert.equal(ipo48.catalogue_only.length,1);
});
test('preface Osnabruck/Sweden reference stays a contextual note, not treaty-party substitution',()=>{
 const page=scan318.scan_page_anchors.find(x=>x.id==='SCAN-1649-PREFACE');
 assert.ok(page.observations.some(x=>x.includes('오스나브뤼크')&&x.includes('스웨덴')));
 assert.equal(scan318.historical_claim_cards.find(x=>x.id==='V318-C05').evidence,
  'VISUALLY_READ_PRINT_SCAN_WITH_SCOPE_GUARD');
 assert.equal(scan318.historical_claim_cards.find(x=>x.id==='V318-C08').evidence,'CROSS_LEVEL_CATALOGUE_VS_SCAN');
 assert.equal(conflict317.unresolved_comparisons.length,2);
 assert.ok(conflict317.unresolved_comparisons.every(x=>x.conclusion==='UNRESOLVED'));
});
test('three medium research notes, ten cards, four open issues and defensive navigation',()=>{
 assert.deepEqual([scan318.medium_readings.length,scan318.medium_readings.flatMap(x=>x.sections).length,
  scan318.historical_claim_cards.length,scan318.open_issues.length],[3,9,10,4]);
 assert.equal(scan318.metrics.body_characters,2841);
 const notes=next.getResearchForV317('V317-PRINT-PRIVILEGE');
 assert.equal(notes.length,3);
 notes[0].sections[0].body='mutated';
 assert.notEqual(next.getResearchForV317('V317-PRINT-PRIVILEGE')[0].sections[0].body,'mutated');
 assert.throws(()=>next.getResearchForV317('unknown'),/unknown V3.17 parent/);
});
test('fictitious 1648 scans, new variants, bad printed label, missing source and unlocked publication fail closed',()=>{
 assert.throws(invalid(x=>x.inspection_status.scanned_1648_ipm_print_pages_directly_seen=1),/fabricated 1648/);
 assert.throws(invalid(x=>x.inspection_status.confirmed_cross_edition_textual_variants=1),/fabricated 1648/);
 assert.throws(invalid(x=>x.source_records.find(s=>s.id==='IPM48-BSB-DDB-CATALOGUE').kind='DIRECT_PRINT_PAGE_SCAN_VISUALLY_INSPECTED'),/1648\/other treaty/);
 assert.throws(invalid(x=>x.scan_page_anchors[1].printed_page=4),/scan page anchor/);
 assert.throws(invalid(x=>x.historical_claim_cards[0].source_ids=['NO_EVIDENCE']),/orphan or falsely approved/);
 assert.throws(invalid(x=>x.historical_claim_cards.find(c=>c.id==='V318-C05').evidence='SURE_IPM_IS_SWEDISH'),/Osnabrück\/Sweden/);
 assert.throws(invalid(x=>x.open_issues[0].status='RESOLVED'),/uninspected counterpart/);
 assert.throws(invalid(x=>x.publication_gate.published=true),/publication HOLD/);
});
