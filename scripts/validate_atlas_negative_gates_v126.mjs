/** V1.26 research-only publication guard. Run: node scripts/validate_atlas_negative_gates_v126.mjs */
import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url);
const read=(p)=>JSON.parse(readFileSync(new URL(p,root),'utf8'));
const fixtures=read('data/deep/atlas_v126_negative_fixtures.json');
export const review=(entry)=>{
  const flagged=fixtures.cases.filter(c=>entry[c.flag]===c.value).map(c=>c.id);
  if(entry.can_ship===true || entry.public_visible===true)flagged.push('PUBLICATION_BLOCK');
  return {decision:flagged.length?'REJECT':'PASS_RESEARCH_ONLY',rule_ids:flagged};
};
export function selftest(){
 assert.equal(fixtures.cases.length,30);
 const ids=new Set(fixtures.cases.map(c=>c.id));assert.equal(ids.size,30);
 const flags=new Set(fixtures.cases.map(c=>c.flag));assert.equal(flags.size,30);
 for(const c of fixtures.cases){
  const record={[c.flag]:c.value,can_ship:false,public_visible:false};
  assert.deepEqual(review(record),{decision:'REJECT',rule_ids:[c.id]},c.id);
  assert.equal(review({can_ship:false,public_visible:false})['decision'],'PASS_RESEARCH_ONLY');
 }
 assert.equal(fixtures.publication_gate.can_ship,false);
 const audit=read('data/deep/atlas_v126_cross_volume_semantic_audit.json');
 assert.equal(audit.reviewed_cross_volume[1].decision,'HOLD_WRONG_SOURCE_DOMAIN');
 return {negative_cases:30,normal_cases:30,semantic_audit:1,status:'PASS'};
}
if(import.meta.url===new URL(process.argv[1], 'file://').href)console.log(JSON.stringify(selftest()));
