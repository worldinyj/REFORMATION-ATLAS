import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildAtlasPreview} from './adapter.mjs';
const read = path => JSON.parse(readFileSync(new URL('../../'+path,import.meta.url),'utf8'));
const input={
 manifest:read('data/contracts/atlas_v165_integration_readiness_manifest.json'),
 narratives:read('data/deep/atlas_v156_extended_narratives.json'),
 cities:read('data/contracts/atlas_v157_historical_city_map.json'),
 geoLinks:read('data/contracts/atlas_v157_spatiotemporal_links.json'),
 editions:read('data/contracts/atlas_v161_edition_comparison_cards.json'),
 evidence:read('data/contracts/atlas_v163_source_evidence_cards.json'),
 navigation:read('data/contracts/atlas_v164_evidence_navigation.json')
};
test('preview is connected and never publishable',()=>{
 const out=buildAtlasPreview(input);
 assert.equal(out.canPublish,false);
 assert.equal(out.mode,'RESEARCH_PREVIEW_ONLY');
 assert.equal(out.readerCards.length,10);
 assert.equal(out.mapPins.length,11);
 assert.equal(out.claimCards.length,8);
 assert.equal(out.editionCards.length,5);
 assert.ok(out.mapPins.every(x=>x.accuracy==='CITY_APPROXIMATE'));
 assert.ok(out.claimCards.every(x=>x.originalVerified===false));
});
test('fail closed with missing material',()=>{
 assert.throws(()=>buildAtlasPreview({...input,manifest:null}));
 assert.throws(()=>buildAtlasPreview({...input,evidence:{cards:[]}}));
 assert.throws(()=>buildAtlasPreview({...input,geoLinks:{links:[{reader_page_id:'NONEXISTENT',place_id:'oxford'}]}}));
});
