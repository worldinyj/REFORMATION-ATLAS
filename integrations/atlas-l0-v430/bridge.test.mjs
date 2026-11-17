import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {dirname,resolve} from "node:path";
import {CONTRACT_VERSION,createAtlasL0ReadOnlyBridge} from "./bridge.mjs";

const root=resolve(dirname(fileURLToPath(import.meta.url)),"../..");
const pkg=JSON.parse(readFileSync(resolve(root,"handoff/V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json"),"utf8"));
const frozen=JSON.parse(readFileSync(resolve(root,"research/data/V4_23_L0_INTERNAL_ALPHA_CONTENT_BUNDLE_DRAFT.json"),"utf8"));
const host={environment:"PRIVATE_STAGING",accessControlDeclared:true};
const make=(data=pkg,opts=host)=>createAtlasL0ReadOnlyBridge(data,opts);
const corrupt=fn=>{const x=structuredClone(pkg);fn(x);return x;};
const rejects=(description,fn)=>test(description,()=>assert.throws(fn,/ATLAS_V430_PRIVATE_STAGING_REJECTED/));

test("real V4.29 import instantiates with all 20 content entities and 42 links",()=>{
  const a=make();
  assert.equal(CONTRACT_VERSION,"V4.30");
  assert.deepEqual(a.counts,{volumes:8,themes:6,chapters:6,themeToVolumeLinks:42});
  assert.equal(a.contractVersion,"V4.30");
  assert.equal(a.runtimeMode,"PRIVATE_STAGING_ONLY");
  assert.equal(a.canPublish,false);
  assert.equal(a.canMergeMain,false);
  assert.equal(a.mayCollectResponses,false);
  assert.equal(a.hostAccessControlNotImplementedByAdapter,true);
  assert.equal(a.sourceGitBlobSha,frozen.source_snapshots.find(x=>x.name==="reader") ? pkg.provenance.sourceGitBlobSha:"IMPOSSIBLE");
});
test("exact 8 volume narratives survive without modification",()=>{
  const a=make();
  for(let i=0;i<8;i++){
    const orig=frozen.volumes[i],seen=a.getVolume(orig.id);
    assert.equal(seen.id,orig.id);
    assert.equal(seen.bodyMarkdown,orig.reader_content_markdown);
    assert.equal(seen.isThematicArchive,i===7);
    assert.equal(seen.relatedThemeIds.length,i===7?0:6);
    assert.equal(a.resolve({kind:"VOLUME",id:orig.id}),seen);
  }
  assert.equal(a.catalog.volumes.length,8);
});
test("exact 6 thematic essays survive; 42 links resolve to real era volumes",()=>{
  const a=make();
  let count=0;
  for(const orig of frozen.themes){
    const t=a.getTheme(orig.id);
    assert.equal(t.bodyMarkdown,orig.overview_markdown);
    assert.equal(t.links.length,7);
    for(const [i,ref] of t.links.entries()){
      assert.equal(ref.targetId,orig.anchors[i].volume_id);
      assert.ok(a.resolve({kind:ref.targetKind,id:ref.targetId}));
      assert.notEqual(ref.targetId,"VOL-08");
      assert.match(ref.relationLabel,/핵심 사례|맥락 연결|제한된 배경/);
      count++;
    }
  }
  assert.equal(count,42);
  assert.equal(a.catalog.themes.length,6);
});
test("exact 6 reader chapters and unmeasured time preserved",()=>{
  const a=make();
  assert.equal(a.readerIntro.title,frozen.introduction.title);
  assert.equal(a.readerIntro.prefaceMarkdown,frozen.introduction.intro_preface_markdown);
  assert.equal(a.readerIntro.readingTimeTargetMinutes,10);
  assert.equal(a.readerIntro.readingTimeMeasured,false);
  for(const orig of frozen.introduction.scenes){
    assert.equal(a.getChapter(orig.id).bodyMarkdown,orig.markdown);
  }
  assert.equal(a.catalog.chapters.length,6);
});
test("real Korean full-text search resolves valid navigation, no external URLs",()=>{
  const a=make();
  for(const phrase of ["후스","성찬","아우크스부르크","한국","번역"]){
    const results=a.search(phrase);
    assert.ok(results.length>0,phrase+" returned no hits");
    for(const row of results){
      assert.equal(row.navigation.kind,row.kind);
      assert.equal(row.navigation.id,row.id);
      assert.equal(a.resolve(row.navigation)?.id,row.id);
      assert.equal(Object.hasOwn(row,"url"),false);
      assert.equal(Object.hasOwn(row,"sourceUrl"),false);
      assert.equal(Object.hasOwn(row,"claim_ids"),false);
    }
  }
  assert.equal(a.search("").length,0);
  assert.equal(a.search(null).length,0);
  assert.ok(a.search("후스",{limit:2}).length<=2);
});
test("methods do not leak evaluator keys, rights metadata, or held claim identifiers",()=>{
 const a=make();
 const exposed=[
   a.catalog,a.readerIntro,...a.catalog.volumes.map(v=>a.getVolume(v.id)),
   ...a.catalog.themes.map(v=>a.getTheme(v.id)),
   ...a.catalog.chapters.map(v=>a.getChapter(v.id)),
   ...a.search("후스")
 ];
 const serialized=JSON.stringify(exposed);
 for(const k of ["editor_only","claim_ids","answer_key","C417-11","C417-12","C417-18","Q419-01","publicationState"]){
   assert.equal(serialized.includes(k),false,"leaked "+k);
 }
});
test("host-mutating V4.29 object after creating bridge cannot change original content",()=>{
 const mutable=structuredClone(pkg),a=make(mutable);
 const first=a.getVolume("VOL-01").bodyMarkdown;
 mutable.volumes[0].bodyMarkdown="MUTATED";
 mutable.themes[0].compareLinks[0].title="MUTATED";
 assert.equal(a.getVolume("VOL-01").bodyMarkdown,first);
 assert.notEqual(a.getTheme("T415-01").links[0].title,"MUTATED");
 assert.ok(Object.isFrozen(a));
 assert.ok(Object.isFrozen(a.catalog.volumes));
 assert.ok(Object.isFrozen(a.getVolume("VOL-01")));
 assert.ok(Object.isFrozen(a.getTheme("T415-01").links[0]));
 assert.throws(()=>{a.getVolume("VOL-01").title="MUTATED";},TypeError);
});
test("unknown ids, URL-looking ids or wrong route kinds resolve to null",()=>{
 const a=make();
 for(const request of [
  {kind:"VOLUME",id:"VOL-99"},
  {kind:"VOLUME",id:"https://example.com/"},
  {kind:"THEME",id:"VOL-01"},
  {kind:"CHAPTER",id:"T415-01"},
  {kind:"FILE",id:"VOL-01"},
  {kind:"VOLUME",id:""},
  null
 ])assert.equal(a.resolve(request),null);
});
rejects("reject missing declared host access",()=>make(pkg,{}));
rejects("reject public environment even with access flag",()=>make(pkg,{environment:"PUBLIC",accessControlDeclared:true}));
rejects("reject absent host declaration",()=>createAtlasL0ReadOnlyBridge(pkg));
rejects("reject release-gate unlock canShip",()=>make(corrupt(x=>{x.privacyAndRights.canShip=true;})));
rejects("reject public indexable data",()=>make(corrupt(x=>{x.privacyAndRights.allowsPublicIndexing=true;})));
rejects("reject fabricated historian signoff",()=>make(corrupt(x=>{x.integrationChecks.realHistorianReviewCompleted=true;})));
rejects("reject fabricated staging signoff",()=>make(corrupt(x=>{x.integrationChecks.realAiStudioStagingTestCompleted=true;})));
rejects("reject first volume missing",()=>make(corrupt(x=>{x.volumes.splice(0,1);})));
rejects("reject duplicate volume id",()=>make(corrupt(x=>{x.volumes[1].id="VOL-01";})));
rejects("reject VOL-08 masquerading as chronological",()=>make(corrupt(x=>{x.volumes[7].kind="CHRONOLOGICAL_VOLUME";})));
rejects("reject 42-link graph with missing target",()=>make(corrupt(x=>{x.themes[0].compareLinks[0].target.id="VOL-99";})));
rejects("reject relation taxonomy altered",()=>make(corrupt(x=>{x.themes[0].compareLinks[0].connectionLabel="random";})));
rejects("reject bad chapter reading measurement claim",()=>make(corrupt(x=>{x.reader.readingTimeMeasured=true;})));
rejects("reject injected image embed",()=>make(corrupt(x=>{x.themes[1].bodyMarkdown+="\n![image](https://example.com/a.jpg)";})));
rejects("reject active html/script injection",()=>make(corrupt(x=>{x.volumes[1].bodyMarkdown+="<script>alert(1)</script>";})));
rejects("reject held IDs in readers",()=>make(corrupt(x=>{x.reader.chapters[0].bodyMarkdown+="C417-11";})));
rejects("reject editor-only registry added",()=>make(corrupt(x=>{x.editor_only={answer_key:"secret"};})));
rejects("reject public release scope",()=>make(corrupt(x=>{x.usageScope="PUBLIC";})));
rejects("reject search result limit over 20",()=>make().search("후스",{limit:99}));
