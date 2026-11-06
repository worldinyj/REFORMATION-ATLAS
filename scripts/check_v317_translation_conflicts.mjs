#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,join} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('../',import.meta.url)));
const raw=p=>readFileSync(join(root,p));
const parsed=p=>JSON.parse(raw(p));
const contract=parsed('data/contracts/atlas_v317_print_translation_conflict_audit.json');
const canonical=raw(contract.canonical_research.path);
const digest=createHash('sha1').update(Buffer.concat([Buffer.from('blob '+canonical.length+'\0'),canonical])).digest('hex');
assert.equal(digest,contract.canonical_research.gitBlobSha1,'canonical V3.17 study SHA changed');
const corpus=JSON.parse(canonical);
assert.deepEqual([corpus.metrics.sources,corpus.metrics.studies,corpus.metrics.sections,
 corpus.metrics.claims,corpus.metrics.unresolved_issues,corpus.metrics.body_characters],
 [7,3,9,10,4,2446]);
assert.equal(contract.version,'3.17.1');
assert.equal(contract.status,'DRAFT');
assert.ok(Object.values(contract.publication_gate).every(x=>x===false));
assert.deepEqual([contract.metrics.open_comparisons,contract.metrics.archival_pages_collated,
 contract.metrics.verified_variants,contract.metrics.legacy_readers],[2,0,0,513]);
const catalogues=new Map(corpus.source_records.map(s=>[s.id,s]));
assert.equal(catalogues.get('PADERBORN').work,'IPO');
assert.match(catalogues.get('PADERBORN').verified,/VD17 12:187744L/);
assert.equal(catalogues.get('STETTIN').work,'IPO');
assert.equal(catalogues.get('LWL741').tier,'SCHOLARLY_SEARCH_INDEX_ONLY');
assert.match(catalogues.get('LWL741').boundary,/유지관리/);
const pairs=contract.unresolved_comparisons;
assert.deepEqual(pairs.map(x=>x.id),['V317-F1','V317-F2']);
assert.ok(pairs.every(x=>x.conclusion==='UNRESOLVED'&&x.primary_print_pages_collated===false&&
 x.earlier_source?.url?.startsWith('https://')&&x.later_source?.url?.startsWith('https://')&&
 x.next_check?.length>=35));
assert.ok(pairs[0].earlier_source.url.includes('paderborn.de')&&
 pairs[0].later_source.url.includes('historisches-lexikon-bayerns.de'));
assert.ok(pairs[1].earlier_source.url.includes('szczecin.pl')&&
 pairs[1].later_source.url.includes('lwl.org'));
const outputIndex=process.argv.indexOf('--export');
if(outputIndex!==-1){
 const dest=process.argv[outputIndex+1];
 assert.ok(dest&&!dest.startsWith('--'),'--export destination missing');
 mkdirSync(resolve(dest),{recursive:true});
 writeFileSync(join(resolve(dest),'atlas_v317_unresolved_print_translation_comparison.json'),
 JSON.stringify(contract,null,2)+'\n');
}
console.log('V3.17.1 PASS: two unresolved, source-bound publication chronology comparisons; V3.17 canonical data unchanged; no invented textual variants; HOLD');
