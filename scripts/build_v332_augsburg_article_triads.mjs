import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PARENT='data/contracts/atlas_v331_1788_1789_primary_page_access_matrix.json';
const CURRENT='data/contracts/atlas_v332_augsburg_article_response_triads.json';
const read=p=>JSON.parse(readFileSync(path.join(ROOT,p),'utf8'));
export function loadInputs(){return {parent:read(PARENT),contract:read(CURRENT)}}
export function validateV332({parent,contract}){
 const hash=execFileSync('git',['hash-object',PARENT],{cwd:ROOT,encoding:'utf8'}).trim();
 assert.equal(hash,contract.parent.locked_parent_contract_blob_sha,'V3.31 parent should remain untouched');
 assert.equal(parent.version,'3.31');
 assert.equal(contract.version,'3.32');assert.equal(contract.status,'DRAFT');
 assert.equal(contract.depth,'MEDIUM');assert.equal(contract.original_priority_issue,'V324-ISS02');
 assert.deepEqual(contract.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
 assert.deepEqual(contract.preserve,{readers:513,reader_sections:1539,sources:723,overviews:97,events:26,relations:12});
 assert.equal(contract.sources.length,20);
 assert.equal(contract.triads.length,5);
 assert.equal(contract.claim_cards.length,15);
 assert.equal(contract.edition_witnesses.length,8);
 assert.equal(contract.chronology.length,7);
 assert.equal(contract.readings.length,5);
 assert.equal(contract.readings.reduce((sum,x)=>sum+x.sections.length,0),15);
 assert.equal(contract.blocklist.length,12);
 assert.equal(contract.open_issues.length,10);
 const s=new Map(contract.sources.map(x=>[x.id,x]));
 assert.equal(s.size,20);
 assert.ok(contract.sources.every(x=>x.original_1530_1531_language_leaf_read===false));
 const t=new Map(contract.triads.map(x=>[x.article,x]));
 assert.deepEqual([...t.keys()],['IV','VII','VIII','XXI','XXIV']);
 for(const triad of contract.triads){
  assert.equal(triad.source_ids.length,3);
  assert.ok(triad.source_ids.every(id=>s.has(id)),'source not found in triad '+triad.article);
  assert.equal(triad.original_contemporary_language_text_checked,false);
  assert.ok(triad.shared.length>=20&&triad.tension.length>=35&&triad.response.length>=35);
 }
 assert.equal(t.get('IV').classification,'PARTIAL_ACCEPTANCE_AND_DIFFERENCE');
 assert.equal(t.get('VII').classification,'CONDITIONAL_REJECTION_WITH_LIMITED_AGREEMENT');
 assert.equal(t.get('VIII').classification,'EXPLICIT_CONFUTATION_ACCEPTANCE');
 assert.equal(t.get('VIII').source_ids[1],'V332-S-CF08');
 assert.equal(t.get('XXI').classification,'SHARED_EXAMPLE_DIFFERENT_INVOCATION');
 assert.equal(t.get('XXIV').classification,'MASS_RETAINED_DISPUTE_OVER_PRIVATE_MASS');
 assert.ok(t.get('IV').shared.includes('자력구원'));
 assert.ok(t.get('VIII').shared.includes('명시적으로 수용'));
 assert.ok(t.get('XXI').tension.includes('사망한 성인'));
 assert.ok(t.get('XXIV').response.includes('외적 행위'));
 const ids=new Set(contract.claim_cards.map(x=>x.id));
 assert.equal(ids.size,15);
 const triadIds=new Set(contract.triads.map(x=>x.id));
 for(const claim of contract.claim_cards){
  assert.ok(triadIds.has(claim.triad_id));
  assert.ok(claim.source_ids.length===3&&claim.source_ids.every(x=>s.has(x)));
  assert.equal(claim.original_leaf_verified,false);
 }
 for(const article of t.keys()){
  const entries=contract.claim_cards.filter(c=>c.triad_id===t.get(article).id);
  assert.equal(entries.length,3);
  assert.deepEqual(entries.map(e=>e.role),['AGREEMENT','DISPUTE','APOLOGY_RESPONSE']);
 }
 assert.equal(contract.chronology.find(x=>x.date==='1530-06-25').type,'CONFESSION_GERMAN_READ_LATIN_GERMAN_SUBMITTED');
 assert.equal(contract.chronology.find(x=>x.date==='1530-08-03').type,'ROMAN_CONFUTATION_READ');
 assert.equal(contract.chronology.find(x=>x.date==='1531-04').type,'LATIN_QUARTO_FIRST_EDITION_SPRING_APPROXIMATE');
 assert.ok(contract.chronology.some(x=>x.date==='1531-11'&&x.type==='JONAS_GERMAN_EDITION_COLOPHON_NOVEMBER'));
 assert.ok(contract.chronology.some(x=>x.date==='1540'&&x.type==='AUGUSTANA_VARIATA_NOT_THE_1530_TEXT'));
 assert.ok(contract.edition_witnesses.some(x=>x.slug==='APOLOGY_LATIN_OCTAVO1531'));
 assert.ok(contract.edition_witnesses.some(x=>x.slug==='APOLOGY_GERMAN_JONAS1531'));
 assert.ok(contract.edition_witnesses.every(x=>x.original_leaf_checked===false));
 assert.ok(contract.readings.every(r=>r.sections.length===3&&r.sections.every(x=>x.body.length>=140)));
 assert.ok(contract.blocklist.some(x=>x.detail.includes('제8조의 명시적 수용')));
 assert.ok(contract.blocklist.some(x=>x.detail.includes('Variata')));
 assert.ok(contract.blocklist.some(x=>x.detail.includes('현대 영문')));
 const l=contract.witness_ledger;
 for(const key of ['original_1530_confession_manuscript_pages','original_1530_confutation_latin_pages','original_1531_apology_latin_print_pages','original_1531_jonas_german_pages','primary_original_language_cross_text_page_pairs','full_latin_german_collections_collated']){
  if(!(key in l))continue;
  assert.equal(l[key],0);
 }
 assert.equal(l.original_1530_confutation_latin_pages,0);
 assert.equal(l.primary_original_language_cross_text_page_pairs,0);
 assert.equal(contract.metrics.source_records,20);
 assert.equal(contract.metrics.triads,5);
 assert.equal(contract.metrics.claim_cards,15);
 assert.equal(contract.metrics.new_readings,5);
 assert.equal(contract.metrics.new_sections,15);
 assert.equal(contract.metrics.original_corpus_mutations,0);
 return {sources:20,triads:5,claims:15,readings:5,sections:15,edition_witnesses:8,issues:10};
}
export function reviewOnly({contract}){
 const header={version:'3.32',status:'DRAFT_RESEARCH_ONLY',public_release_approved:false,webapp_integrated:false,original_1530_1531_language_pairs:0};
 return {
  'v332_augsburg_article_triads.json':{...header,count:contract.triads.length,triads:contract.triads,sources:contract.sources},
  'v332_confutation_response_claims.json':{...header,count:contract.claim_cards.length,claims:contract.claim_cards,blocked_readings:contract.blocklist},
  'v332_edition_witness_followup.json':{...header,count:contract.open_issues.length,issues:contract.open_issues,editions:contract.edition_witnesses,chronology:contract.chronology,witness_ledger:contract.witness_ledger}
 };
}
export function build(){
 const data=loadInputs();validateV332(data);const outputs=reviewOnly(data);
 const dir=path.join(ROOT,'out','atlas-v332');mkdirSync(dir,{recursive:true});
 for(const [filename,obj] of Object.entries(outputs))writeFileSync(path.join(dir,filename),JSON.stringify(obj,null,2)+'\n');
 return outputs;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const o=build();for(const [filename,obj] of Object.entries(o))console.log(filename+': '+obj.count+' RESEARCH_ONLY');
}
