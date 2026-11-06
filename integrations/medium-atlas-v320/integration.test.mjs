import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const doc=JSON.parse(readFileSync(new URL('../../data/contracts/atlas_v320_ipm1648_witness_provenance.json',import.meta.url),'utf8'));
const src=id=>doc.sources.find(s=>s.id===id);
test('parent V3.19 contract exact git blob and inherited publication hold',()=>{
 assert.equal(execFileSync('git',['hash-object','data/contracts/atlas_v319_ipm_print_privilege_dating.json'],{encoding:'utf8'}).trim(),doc.parent.locked_prior_blob_sha);
 assert.equal(doc.version,'3.20');assert.equal(doc.status,'DRAFT');assert.equal(doc.depth,'MEDIUM');
 assert.deepEqual(doc.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(doc.preserved_original_corpus,{readers:513,sections:1539,sources:723,overviews:97,selected_claims:22});
});
test('1648 bibliographic matches cannot become physical collations or variants',()=>{
 const ids=['IPM48-BSB-VD17-187750M','IPM48-ZURICH-RI240','IPM48-ZURICH-MS-J1801'];
 for(const id of ids){const v=src(id);assert.equal(v.work,'IPM');assert.equal(v.catalogue_edition_year,1648);assert.equal(v.original_print_pages_visualized,0);assert.equal(v.evidence,'LIBRARY_CATALOGUE_TEXT_ONLY');}
 assert.match(src(ids[0]).reported_imprint,/XLVIII/);assert.match(src(ids[1]).reported_imprint,/XLVIII/);
 assert.match(src(ids[0]).reported_extent,/62/);assert.match(src(ids[1]).reported_extent,/62/);
 assert.notEqual(src(ids[1]).reported_extent,src(ids[2]).reported_extent);
 assert.equal(doc.inspection.verified_1648_ipm_pages,0);
 assert.equal(doc.inspection.verified_same_treaty_cross_edition_page_pairs,0);
 assert.equal(doc.inspection.verified_textual_variants,0);
 assert.equal(doc.inspection.new_physical_print_pages_visually_read,0);
});
test('TextGrid titles describing event 1648 cannot be a 1648 edition print',()=>{
 const t=src('IPM49-TEXTGRID-4BHH3');
 assert.equal(t.transcribed_imprint_year,1649);
 assert.equal(t.catalogue_edition_year,null);
 assert.equal(t.work,'IPM');assert.equal(t.original_print_pages_visualized,0);
 assert.match(t.reported_imprint,/XLIX/);
 const w=src('IPM49-WIKISOURCE-1649');assert.equal(w.original_print_pages_visualized,5);
 assert.equal(doc.inspection.cumulative_verified_1649_ipm_pages,5);
 assert.equal(doc.relations.find(x=>x.id==='V320-L04').type,'BOTH_REPORT_1649_IMPRINT_NO_NEW_INDEPENDENT_SCAN');
});
test('Osnabrück/Sweden IPO excluded even if printer is the same',()=>{
 const ipo=src('IPO48-PADERBORN-EXCLUSION');assert.equal(ipo.work,'IPO');
 assert.equal(ipo.catalogue_identifier,'VD17 12:187744L');
 assert.notEqual(ipo.catalogue_identifier,src('IPM48-BSB-VD17-187750M').catalogue_identifier);
 assert.equal(doc.relations.find(x=>x.id==='V320-L05').type,'DIFFERENT_TREATY_EXCLUDED');
});
test('three medium readings and every claim bounded to evidence',()=>{
 assert.equal(doc.sources.length,6);assert.equal(doc.relations.length,5);
 assert.equal(doc.readings.length,3);assert.equal(doc.readings.reduce((n,r)=>n+r.sections.length,0),9);
 assert.equal(doc.claims.length,10);assert.equal(new Set(doc.claims.map(x=>x.id)).size,10);
 assert.ok(doc.claims.every(c=>c.physical_1648_scan_inspected===false&&c.verified_variant===false&&c.expert_approved===false));
 const known=new Set(doc.sources.map(x=>x.id));assert.ok(doc.claims.every(c=>c.source_ids.every(id=>known.has(id))));
 assert.equal(doc.unresolved.length,5);assert.ok(doc.unresolved.every(x=>x.state.startsWith('NOT_')));
});
