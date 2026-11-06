import test from 'node:test';
import assert from 'node:assert/strict';
import {loadInputs,validateV332,reviewOnly} from '../../scripts/build_v332_augsburg_article_triads.mjs';
const clone=x=>structuredClone(x);
test('V3.31 contract frozen and V3.32 five three-text article triads verified',()=>{
 const d=loadInputs();
 assert.deepEqual(validateV332(d),{sources:20,triads:5,claims:15,readings:5,sections:15,edition_witnesses:8,issues:10});
 assert.equal(d.contract.publication_gate.published,false);
});
test('Roman Confutation VIII explicitly ACCEPTS the sacrament validity article',()=>{
 const d=loadInputs(),t=d.contract.triads.find(x=>x.article==='VIII');
 assert.equal(t.classification,'EXPLICIT_CONFUTATION_ACCEPTANCE');
 assert.equal(t.source_ids[1],'V332-S-CF08');
 const bad=clone(d);bad.contract.triads.find(x=>x.article==='VIII').classification='REJECTION';
 assert.throws(()=>validateV332(bad),/Expected values to be strictly equal/);
});
test('confutation IV rejects Pelagius yet disputes meritorious grace-assisted works',()=>{
 const d=loadInputs(),t=d.contract.triads.find(x=>x.article==='IV');
 assert.equal(t.classification,'PARTIAL_ACCEPTANCE_AND_DIFFERENCE');
 assert.ok(t.shared.includes('자력구원'));
 const bad=clone(d);bad.contract.triads.find(x=>x.article==='IV').classification='CATEGORICAL_DENIAL_OF_ALL_GRACE';
 assert.throws(()=>validateV332(bad),/Expected values to be strictly equal/);
});
test('church VII conditional objection is separate from VIII positive answer',()=>{
 const d=loadInputs();assert.equal(d.contract.triads.find(x=>x.article==='VII').classification,'CONDITIONAL_REJECTION_WITH_LIMITED_AGREEMENT');
 assert.equal(d.contract.triads.find(x=>x.article==='VIII').classification,'EXPLICIT_CONFUTATION_ACCEPTANCE');
 const bad=clone(d);bad.contract.triads.find(x=>x.article==='VII').classification='COMPLETE_ACCEPTANCE';
 assert.throws(()=>validateV332(bad),/Expected values to be strictly equal/);
});
test('Apology article locators contain parallel section numbering and are not same as AC',()=>{
 const d=loadInputs();validateV332(d);
 assert.match(d.contract.triads.find(x=>x.article==='IV').apology_locator,/IV \(II\)/);
 assert.match(d.contract.triads.find(x=>x.article==='VII').apology_locator,/VII\/VIII \(IV\)/);
 assert.match(d.contract.triads.find(x=>x.article==='XXI').apology_locator,/XXI \(IX\)/);
 assert.match(d.contract.triads.find(x=>x.article==='XXIV').apology_locator,/XXIV \(XII\)/);
});
test('no contemporary 1530 and 1531 Latin German primary print pages are invented',()=>{
 const d=loadInputs();assert.equal(d.contract.witness_ledger.primary_original_language_cross_text_page_pairs,0);
 const bad=clone(d);bad.contract.witness_ledger.original_1531_apology_latin_print_pages=1;
 assert.throws(()=>validateV332(bad),/Expected values to be strictly equal/);
 const bad2=clone(d);bad2.contract.sources.find(x=>x.id==='V332-S-CF08').original_1530_1531_language_leaf_read=true;
 assert.throws(()=>validateV332(bad2),/The expression evaluated to a falsy value/);
});
test('1530 reading and 1531 first quarto, later octavo, Jonas translation, Variata distinguish editions',()=>{
 const d=loadInputs();validateV332(d);
 assert.ok(d.contract.edition_witnesses.some(x=>x.slug==='APOLOGY_LATIN_QUARTO1531'));
 assert.ok(d.contract.edition_witnesses.some(x=>x.slug==='APOLOGY_LATIN_OCTAVO1531'));
 assert.ok(d.contract.edition_witnesses.some(x=>x.slug==='APOLOGY_GERMAN_JONAS1531'));
 assert.ok(d.contract.edition_witnesses.some(x=>x.slug==='AC_VARIATA1540'));
 const bad=clone(d);bad.contract.chronology.find(x=>x.date==='1530-08-03').type='FIRST_APOLOGY_PRINTED';
 assert.throws(()=>validateV332(bad),/Expected values to be strictly equal/);
});
test('reader essays and review-only outputs are not app publications',()=>{
 const d=loadInputs();validateV332(d);const exports=reviewOnly(d);
 assert.deepEqual(Object.keys(exports),['v332_augsburg_article_triads.json','v332_confutation_response_claims.json','v332_edition_witness_followup.json']);
 assert.deepEqual(Object.values(exports).map(x=>x.count),[5,15,10]);
 assert.ok(Object.values(exports).every(x=>x.public_release_approved===false&&x.webapp_integrated===false&&x.original_1530_1531_language_pairs===0));
});
