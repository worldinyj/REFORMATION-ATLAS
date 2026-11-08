#!/usr/bin/env node
/**
 * V3.37.1 CR XXVI (1858) evidence-contract validator.
 * Review-only. Never rewrites corpus sources, app data, registries or manuscripts.
 * Run: node scripts/validate_v337_cr26_apparatus.mjs
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(readFileSync(path.join(root,'data/contracts/atlas_v337_cr26_apparatus_articles_iv_vii_viii.json'),'utf8'));
function assertUnique(items,name){assert.equal(new Set(items).size,items.length,`Duplicate ${name}`);}
assert.equal(data.schema,'atlas.research.v337.cr26_apparatus.v1');
assert.equal(data.version,'3.37.1');
assert.equal(data.status,'RESEARCH_DRAFT_HOLD');
assert.equal(data.published,false);
assert.equal(data.webapp_integrated,false);
assert.equal(data.source.type,'1858_PRINT_IMAGES_REEXCERPTED');
assert.deepEqual(data.source.pdf_zero_based_pages_verified,[2,3,4]);
assert.deepEqual(data.source.printed_pages_verified,[351,352,353,354,355,356]);
assert.equal(data.source.cr26_1858_1531_main_text_263_336_seen,false);
assert.equal(data.source.edition_1540_original_imprint_seen,false);
assert.deepEqual(data.edition_labels.map(x=>x.label),['Ed. 1','Ed. 2','Ed. 3','Ed. 4']);
assert.equal(data.claims.length,6);
assertUnique(data.claims.map(x=>x.id),'claim ids');
assert.deepEqual([...new Set(data.claims.map(x=>x.article))].sort(),['IV','VII','VIII']);
for(const c of data.claims){
 assert.ok(c.claim_ko.length>=35,`Missing explanation: ${c.id}`);
 assert.ok(c.print_pages.every(p=>p>=351&&p<=356),`Unsupported print page: ${c.id}`);
 assert.ok(c.pdf_zero_based_pages.every(p=>p>=2&&p<=4),`Unsupported image page: ${c.id}`);
 assert.ok(c.proof_status!=='ED1_MAIN_TEXT_DIRECTLY_SEEN',`Evidence promotion: ${c.id}`);
 assert.ok(c.not_claimed,`Missing caveat: ${c.id}`);
}
for(const id of ['V337-A01','V337-A02','V337-A03']) {
 assert.equal(data.claims.find(c=>c.id===id).proof_status,'PRINT_IMAGE_APPARATUS_DIRECTLY_SEEN');
}
assert.equal(data.online_discrepancies.length,4);
assertUnique(data.online_discrepancies.map(x=>x.id),'discrepancy ids');
assert.deepEqual(data.online_discrepancies.map(x=>x.id),['W01','W02','W03','W04']);
assert.ok(data.online_discrepancies.every(x=>/OPEN|MISSING/.test(x.status)));
assert.equal(data.online_discrepancies[0].comparability_to_ed3,'ED3_WHOLE_ARTICLE_REWRITTEN');
assert.equal(data.online_discrepancies[1].ed3_reprint,'consentire');
assert.equal(data.online_discrepancies[2].ed1_in_1858_apparatus,'mali');
assert.equal(data.online_discrepancies[3].ed3_reprint,'sentiebant');
assert.equal(data.metrics.article_groups_with_edition_apparatus_confirmed,3);
assert.equal(data.metrics.claim_cards,data.claims.length);
assert.equal(data.metrics.digital_discrepancies_still_open,4);
assert.equal(data.metrics.verified_ed1_main_text_print_pages,0);
assert.equal(data.metrics.primary_1531_print_pages,0);
assert.equal(data.metrics.original_corpus_changes,0);
assert.equal(data.metrics.publication_allowed,false);
assert.ok(data.qa_invariants.length>=4);
console.log('V3.37.1 PASS: 6 evidence claims, 3 article groups, 4 unresolved web readings; publication HOLD');
