import assert from "node:assert/strict";
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const load = (file) => JSON.parse(readFileSync(file, "utf8"));
const contractPath = "data/contracts/atlas_v323_curated_chronology_navigation_graph.json";
const basePath = "data/contracts/atlas_v304_overview_medium_reading_crosswalk.json";
const v305Path = "data/deep/atlas_v305_medium_depth_pietism_revival_readers.json";
const v307Path = "data/deep/atlas_v307_remaining_overview_medium_readers.json";
const v310Path = "data/contracts/atlas_v310_partial_coverage_quality_audit.json";
const v322Path = "data/contracts/atlas_v322_cross_document_date_age_gates.json";
const v316Path = "data/contracts/atlas_v316_ratification_chronology_scope.json";
const v319Path = "data/contracts/atlas_v319_ipm_print_privilege_dating.json";

export function assertFrozenInputs(d) {
  for (const input of d.frozen_inputs) {
    const actual = execFileSync("git", ["hash-object", input.path], {encoding:"utf8"}).trim();
    assert.equal(actual, input.git_blob_sha1, "Frozen upstream source changed: " + input.path);
  }
}

export function buildEffectiveOverviews(base, v305, v307, v310, catalogue) {
  assert.equal(base.entries.length, 97);
  const knownReaders = new Set(catalogue.map(r=>r.id));
  assert.equal(knownReaders.size, 513);
  const overviews = new Map(base.entries.map(e=>[e.overview_id, {
    overview_id:e.overview_id, category:e.category, title:e.title,
    period:e.period, mapping_status:e.mapping_status,
    scope:e.scope, reader_links:e.reader_links.map(x=>({...x}))
  }]));
  assert.equal(overviews.size, 97);
  const updateSteps = [...v305.overview_link_updates, ...v307.overview_link_updates];
  assert.equal(updateSteps.length, 29);
  for(const u of updateSteps){
    const o=overviews.get(u.overview_id);
    assert.ok(o, "Missing overview for update "+u.overview_id);
    assert.equal(o.mapping_status, u.previous_status, "Unexpected pre-overlay status for "+u.overview_id);
    assert.ok(knownReaders.has(u.reader_id), "Unknown reader "+u.reader_id);
    assert.ok(!o.reader_links.some(x=>x.reader_id===u.reader_id), "Duplicate update "+u.reader_id);
    o.mapping_status=u.new_status;
    o.scope=u.scope;
    o.reader_links.push({reader_id:u.reader_id,role:"PRIMARY",title:catalogue.find(x=>x.id===u.reader_id).title});
  }
  assert.equal(v310.navigation_patches.length, 10);
  for(const patch of v310.navigation_patches) {
    const o=overviews.get(patch.id);
    assert.ok(o, "Unknown overview patch "+patch.id);
    assert.equal(o.mapping_status,patch.previous_status, "Unexpected prior V310 patch status");
    if(patch.new_status)o.mapping_status=patch.new_status;
    o.scope=patch.scope;
    for(const target of patch.targets) {
      assert.ok(knownReaders.has(target.reader_id), "V310 patch unknown reader");
      if(!o.reader_links.some(x=>x.reader_id===target.reader_id))o.reader_links.push({...target});
    }
  }
  const stats={DIRECT_TOPIC:0,PARTIAL_COVERAGE:0,BACKGROUND_ONLY:0,NO_MATCH:0};
  for(const o of overviews.values()){
    assert.ok(Object.hasOwn(stats,o.mapping_status));
    stats[o.mapping_status]++;
    assert.ok(o.reader_links.length>0, "Orphan overview "+o.overview_id);
    assert.equal(new Set(o.reader_links.map(x=>x.reader_id)).size,o.reader_links.length);
    for (const r of o.reader_links)assert.ok(knownReaders.has(r.reader_id));
  }
  for(const exclusion of base.exclusions) {
    const o=overviews.get(exclusion.overview_id);
    for(const r of o.reader_links)assert.ok(!exclusion.forbidden_reader_ids.includes(r.reader_id),
      "Forbidden conflation "+exclusion.overview_id+" "+r.reader_id);
  }
  assert.deepEqual(stats,{DIRECT_TOPIC:78,PARTIAL_COVERAGE:19,BACKGROUND_ONLY:0,NO_MATCH:0});
  const entries=[...overviews.values()].sort((a,b)=>a.overview_id.localeCompare(b.overview_id));
  assert.equal(entries.reduce((n,x)=>n+x.reader_links.length,0),156);
  assert.equal(new Set(entries.flatMap(x=>x.reader_links.map(y=>y.reader_id))).size,107);
  return {overviews,entries,stats};
}

export function dateBounds(e){
  assert.ok(/^\d{4}(?:-\d{2}(?:-\d{2})?)?$/.test(e.date), "Bad historic date "+e.date);
  const granularity=e.date.length===4?"YEAR":e.date.length===7?"MONTH":"DAY";
  assert.equal(e.precision,granularity,"Wrong date precision "+e.id);
  const parts=e.date.split("-");
  const y=parts[0],month=parts[1]||"01",day=parts[2]||"01";
  const earliest=y+"-"+month+"-"+day;
  const latest=granularity==="YEAR"?y+"-12-31":granularity==="MONTH"?
    y+"-"+month+"-"+String(new Date(Date.UTC(Number(y),Number(month),0)).getUTCDate()).padStart(2,"0"):earliest;
  return {earliest,latest,granularity};
}

export function validateGraph(d,effective,catalogue,upstream){
  assert.equal(d.status,"DRAFT");assert.equal(d.depth,"MEDIUM");
  assert.deepEqual(d.publication_gate,{published:false,main_changed:false,webapp_integrated:false,historian_approved:false});
  assert.equal(d.guardrails.original_print_variant_pairs,0);
  assert.equal(d.guardrails.external_approval,false);
  assert.equal(d.guardrails.zero_original_1648_ipm_pages_read,true);
  assert.equal(d.guardrails.full_corpus_factual_audit,false);
  assert.equal(d.guardrails.all_513_entries_transformed,false);
  const count=d.expected_counts;
  assert.equal(count.reader_catalogue,513);assert.equal(count.overviews,97);
  assert.deepEqual(count.overview_statuses,effective.stats);
  assert.equal(count.overview_reader_links,156);assert.equal(count.unique_overview_linked_readers,107);
  assert.equal(d.events.length,count.events);assert.equal(d.paths.length,count.paths);
  assert.equal(d.document_witnesses.length,count.edition_nodes);
  assert.equal(d.witness_relations.length,count.work_relations);
  const catalogById=new Map(catalogue.map(x=>[x.id,x]));
  const events=new Map(d.events.map(e=>[e.id,e]));
  const witness=new Map(d.document_witnesses.map(w=>[w.id,w]));
  assert.equal(events.size,d.events.length);
  assert.equal(witness.size,d.document_witnesses.length);
  const sourceIds=new Set(d.evidence_sources.map(s=>s.id));
  const v322Events=new Map(upstream.v322.event_taxonomy.map(x=>[x.id,x]));
  const v316Events=new Map(upstream.v316.chronology.map(x=>[x.date,x]));
  const v319Events=new Map(upstream.v319.chronology.map(x=>[x.date,x]));
  for(const e of d.events) {
    dateBounds(e);
    assert.equal(new Set(e.reader_ids).size,e.reader_ids.length);
    assert.equal(new Set(e.overview_ids).size,e.overview_ids.length);
    for(const id of e.reader_ids)assert.ok(catalogById.has(id),"Dangling reader "+id);
    for(const id of e.overview_ids) {
      const overview=effective.overviews.get(id);
      assert.ok(overview,"Dangling overview "+id);
      assert.ok(overview.reader_links.some(link=>e.reader_ids.includes(link.reader_id)),
        "Chronology overview has no matching existing primary/followup reader: "+e.id+"/"+id);
    }
    const p=e.proof;
    if(p.version==="V322"){
      const row=v322Events.get(p.record_id);
      assert.ok(row,"Unknown V322 provenance "+p.record_id);
      assert.equal(row.date,e.date);
    } else if(p.version==="V316"){
      const row=v316Events.get(p.record_id);
      assert.ok(row,"Unknown V316 provenance "+p.record_id);
      assert.equal(row.date,e.date);assert.equal(row.type,e.kind);
    } else if(p.version==="V319"){
      const row=v319Events.get(p.record_id);
      assert.ok(row,"Unknown V319 provenance "+p.record_id);
      assert.equal(row.date,e.date);
    } else if(p.version==="CATALOGUE"){
      assert.ok(catalogById.has(p.record_id));
      assert.ok(e.reader_ids.includes(p.record_id));
    } else if(p.version==="EXTERNAL"){
      assert.ok(sourceIds.has(p.record_id));
      assert.deepEqual(e.reader_ids,[]);
      assert.deepEqual(e.overview_ids,[]);
      assert.equal(e.work,"SPAIN_DUTCH_PEACE_MUENSTER");
    } else assert.fail("Unregistered provenance "+p.version);
  }
  const assigned=new Set();
  for(const p of d.paths){
    assert.ok(p.ordered_event_ids.length>=3);
    const seenPath=new Set();
    for(const eid of [...p.ordered_event_ids,...(p.year_only_unsequenced_event_ids||[])]){
      assert.ok(events.has(eid));
      assert.ok(!seenPath.has(eid),"Duplicate event in path "+p.id);seenPath.add(eid);assigned.add(eid);
    }
    for(let i=1;i<p.ordered_event_ids.length;i++){
      const before=dateBounds(events.get(p.ordered_event_ids[i-1]));
      const after=dateBounds(events.get(p.ordered_event_ids[i]));
      assert.ok(before.latest<after.earliest,
        "Precision-sensitive timeline ordering not proven in "+p.id+" between "+
        p.ordered_event_ids[i-1]+" and "+p.ordered_event_ids[i]);
    }
    for(const id of (p.year_only_unsequenced_event_ids||[])){
      assert.equal(events.get(id).precision,"YEAR");
      assert.ok(!p.ordered_event_ids.includes(id));
    }
  }
  assert.equal(assigned.size,d.events.length,"Some event not in any timeline path");
  const namespacedWorks=new Set(["AUGSBURG_CONFESSION","CALVIN_INSTITUTES","IPM","IPO","SPAIN_DUTCH_PEACE_MUENSTER","WESLEY_GENERAL_RULES"]);
  for(const w of d.document_witnesses){
    assert.ok(namespacedWorks.has(w.work));
    assert.ok(/^\d{4}$/.test(String(w.year)));
    if(w.linked_event){const e=events.get(w.linked_event);assert.ok(e);assert.equal(Number(e.date.slice(0,4)),w.year);}
    if(w.work==="IPM" && w.year===1648)assert.equal(w.read_status,"LIBRARY_CATALOGUE_ONLY_NO_PHYSICAL_PAGE_READ");
  }
  for(const r of d.witness_relations){
    const a=witness.get(r.from),b=witness.get(r.to);
    assert.ok(a&&b);
    if(r.type==="NOT_SAME_TREATY")assert.notEqual(a.work,b.work);
    if(r.type==="EDITION_REVISION" || r.type==="AUTHORIAL_EDITION_DEVELOPMENT" || r.type==="SAME_TREATY_WORK_POSSIBLE_PRINT_COMPARISON")assert.equal(a.work,b.work);
  }
  const external=events.get("V323-E15"),french=events.get("V323-E17"),yearprint=events.get("V323-E21");
  assert.equal(external.work,"SPAIN_DUTCH_PEACE_MUENSTER");
  assert.equal(external.date,"1648-01-30");
  assert.equal(french.work,"IPM_AND_IPO_TWO_TREATIES");
  assert.equal(french.date,"1648-10-24");
  assert.equal(yearprint.precision,"YEAR");
  const peace=d.paths.find(p=>p.id==="V323-P03");
  assert.ok(!peace.ordered_event_ids.includes(yearprint.id));
  assert.ok(peace.year_only_unsequenced_event_ids.includes(yearprint.id));
  return {events,catalogById,witness};
}

export function buildOutputs(d, effective, catalogue, validated) {
  const base = {version:"3.23",review_status:"DRAFT",publication_ready:false,webapp_integrated:false};
  const readerIndex={
    ...base,count:catalogue.length,
    readers:catalogue.map(x=>({id:x.id,title:x.title,summary:x.summary||null,dataset:x.dataset,
      chapter_index:x.chapter_index,section_count:x.section_count}))
  };
  const overviewIndex={
    ...base,count:effective.entries.length,overview_status_counts:effective.stats,
    mapping_note:"V304 base + V305 and V307 links + V310 editorial navigation patches; not production app",
    overviews:effective.entries
  };
  const annotatedEvents=d.events.map(e=>({...e,
    linked_readers:e.reader_ids.map(id=>({id,title:validated.catalogById.get(id).title})),
    linked_overviews:e.overview_ids.map(id=>({id,title:effective.overviews.get(id).title,status:effective.overviews.get(id).mapping_status}))
  }));
  const directedPathEdges=d.paths.flatMap(p=>p.ordered_event_ids.slice(1).map((id,i)=>({
    from:p.ordered_event_ids[i],to:id,path:p.id,
    type:"NEXT_IN_EDITORIAL_CHRONOLOGY_ONLY_NOT_PROVEN_CAUSAL_RELATION"
  })));
  const chronology={
    ...base,coverage_scope:"26 curated events only, not 513-article fact audit",
    events:annotatedEvents,paths:d.paths,ordered_navigation_edges:directedPathEdges,
    editorial_warning:"Year-only print dates are not chronologically sequenced against month/day precision within the same year."
  };
  const editionGraph={...base,documents:d.document_witnesses,relationships:d.witness_relations,
    cautions:d.guardrails,source_records:d.evidence_sources};
  return {
    "v323_overview_97_reading_index.json":overviewIndex,
    "v323_513_reader_catalogue_index.json":readerIndex,
    "v323_curated_event_timeline.json":chronology,
    "v323_edition_relation_graph.json":editionGraph
  };
}

export function loadAll(){
  return {contract:load(contractPath),base:load(basePath),v305:load(v305Path),v307:load(v307Path),v310:load(v310Path),
    upstream:{v322:load(v322Path),v316:load(v316Path),v319:load(v319Path)}};
}

export function main(){
  const all=loadAll();assertFrozenInputs(all.contract);
  const catalogue=all.v307.catalogue;
  const effective=buildEffectiveOverviews(all.base,all.v305,all.v307,all.v310,catalogue);
  const valid=validateGraph(all.contract,effective,catalogue,all.upstream);
  const output=buildOutputs(all.contract,effective,catalogue,valid);
  const directory="out/atlas-v323";
  mkdirSync(directory,{recursive:true});
  for (const [name,data] of Object.entries(output))writeFileSync(path.join(directory,name),JSON.stringify(data,null,2)+"\n");
  process.stdout.write(JSON.stringify({success:true,output_files:Object.keys(output),overview:effective.entries.length,
    readers:catalogue.length,events:valid.events.size,paths:all.contract.paths.length,witnesses:valid.witness.size,
    overview_reader_edges:effective.entries.reduce((n,x)=>n+x.reader_links.length,0),
    publication_ready:false})+"\n");
}

if (process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main();
