import fs from 'node:fs';
import {createResearchAdapter} from './research_adapter.mjs';
const crosswalk=JSON.parse(fs.readFileSync(new URL('./legacy_crosswalk.json',import.meta.url),'utf8'));
const preview=JSON.parse(fs.readFileSync(new URL('../../v539/site/atlas_preview.json',import.meta.url),'utf8'));
const opt={preview,crosswalk,enabled:true,hostNamespace:'ATLAS_OVERVIEW_V01'};
const adapter=createResearchAdapter(opt);
if(adapter.status!=='REVIEW_ADAPTER_READY')throw Error(adapter.status);
let n=0;for(const r of crosswalk.records){const record={id:r.legacy_id,...(['person','place'].includes(r.kind)?{name_ko:r.legacy_label}:{title:r.legacy_label})};const actual=adapter.getSupplement(r.kind,record);if(Boolean(actual)!==(r.relation!=='no_curated_match'))throw Error(r.legacy_id);n++;}
if(createResearchAdapter({...opt,enabled:false}).status!=='DISABLED'||createResearchAdapter({...opt,hostNamespace:'UNKNOWN'}).status!=='DISABLED'||createResearchAdapter({...opt,preview:{...preview,can_ship:true}}).status!=='DISABLED'||adapter.listNewPeople().length!==7)throw Error('guard failure');
console.log('PASS: '+n+' legacy objects; review only');
