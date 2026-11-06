#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {assembleV318} from '../integrations/medium-atlas-v318/overlay.mjs';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const read=p=>readFileSync(join(root,p));
const manifest=JSON.parse(read('integrations/medium-atlas-v318/manifest.json'));
const load=record=>{
 const bytes=read(record.path);
 if(record.sha256)assert.equal(createHash('sha256').update(bytes).digest('hex'),record.sha256,record.path);
 if(record.gitBlobSha1){
  const sha=createHash('sha1').update(Buffer.concat([Buffer.from('blob '+bytes.length+'\0'),bytes])).digest('hex');
  assert.equal(sha,record.gitBlobSha1,'Git blob SHA mismatch: '+record.path);
 }
 return JSON.parse(bytes.toString('utf8'));
};
const inputs=manifest.inputs.map(load),audits=manifest.auditInputs.map(load);
const [v311,v312,v313,v314,v315,rat316,prints317,conflicts317,scans318]=[
 manifest.addendumInput,manifest.latinInput,manifest.editionInput,
 manifest.authInput,manifest.wordingInput,manifest.ratificationInput,
 manifest.witnessPrintInput,manifest.printingConflictInput,manifest.scanInput
].map(load);
const {delivery,crosswalk}=assembleV318(inputs,...audits,v311,v312,v313,v314,v315,rat316,prints317,conflicts317,scans318);
assert.deepEqual([delivery.readers.length,delivery.sources.length,delivery.source_verification.selected_claims.length,crosswalk.entries.length],[513,723,22,97]);
const expected=manifest.expectedScan,actual={
 sources:scans318.source_records.length,pageScans:scans318.scan_page_anchors.length,
 readings:scans318.medium_readings.length,
 sections:scans318.medium_readings.reduce((n,x)=>n+x.sections.length,0),
 claims:scans318.historical_claim_cards.length,
 openIssues:scans318.open_issues.length,
 bodyCharacters:scans318.metrics.body_characters,
 actual1648PrintScansSeen:scans318.inspection_status.scanned_1648_ipm_print_pages_directly_seen,
 diplomaticOriginalPagesSeen:scans318.inspection_status.diplomatic_original_pages_directly_seen,
 matchedEditionPairs:scans318.inspection_status.paired_1648_1649_original_print_paragraphs_collated,
 textualVariantsProven:scans318.inspection_status.confirmed_cross_edition_textual_variants
};
assert.deepEqual(actual,expected);
assert.equal(delivery.publication_gate.published,false);
const exportAt=process.argv.indexOf('--export');
if(exportAt!==-1){
 const target=process.argv[exportAt+1];assert.ok(target&&!target.startsWith('--'),'--export requires directory');
 const dir=resolve(target);mkdirSync(dir,{recursive:true});
 const outputs=[
  ['atlas_v318_513_frozen_scan_evidence_delivery.json',delivery],
  ['atlas_v318_97_overview_crosswalk.json',crosswalk],
  ['atlas_v318_three_physically_inspected_1649_pages.json',scans318.scan_page_anchors],
  ['atlas_v318_10_claims_scoped_to_print_or_catalogue.json',scans318.historical_claim_cards],
  ['atlas_v318_3_medium_reading_notes.json',scans318.medium_readings],
  ['atlas_v318_unverified_1648_and_edition_variants.json',scans318.open_issues],
  ['atlas_v318_legacy_printing_contradictions.json',conflicts317.unresolved_comparisons]
 ];
 for(const [name,obj] of outputs){
  const json=JSON.stringify(obj,null,2)+'\n';
  writeFileSync(join(dir,name),json);
  console.log(name,createHash('sha256').update(json).digest('hex'));
 }
}
console.log('V3.18 PASS: 513 originals, 723 sources, 97 overview unchanged; 1649 IPM print scans 3 verified; 1648 IPM physical scans 0, print-page alignments 0, variants 0; HOLD');
