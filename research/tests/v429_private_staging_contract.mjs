#!/usr/bin/env node
"use strict";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { resolve, dirname } from "node:path";
import { createPrivateAtlasNavigator, validatePrivateAtlasPayload } from "../../preview/staging/atlas_private_staging_adapter.mjs";

const repo = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const data = JSON.parse(readFileSync(resolve(repo, "preview/staging/V429_L0_PRIVATE_STAGING_CONTENT.json"), "utf8"));
const checks = [];
function record(name, fn) {
  fn();
  checks.push(name);
}
record("V4.23 source snapshot", () => assert.equal(data.source.git_blob_sha, "ddf48f401ce4202166eedd308e1d5892f88ac0b8"));
record("private restriction and 8/6/42/6", () => assert.deepEqual(validatePrivateAtlasPayload(data), {valid:true,volumes:8,themes:6,anchors:42,reader_scenes:6,can_ship:false}));
const nav = createPrivateAtlasNavigator(data);
record("volume index", () => assert.equal(nav.resolve("/atlas-preview/volumes").volumes.length, 8));
record("theme index", () => assert.equal(nav.resolve("/atlas-preview/themes").themes.length, 6));
for(let i=1;i<=8;i++){
  const id="VOL-"+String(i).padStart(2,"0");
  record("volume "+id, () => {
    const x=nav.resolve("/atlas-preview/volumes/"+id);
    assert.equal(x.kind,"volume");
    assert.equal(x.publication_allowed,false);
    assert.ok(x.item.body_markdown.length>200);
  });
}
for(let i=1;i<=6;i++){
  const id="T415-"+String(i).padStart(2,"0");
  record("theme "+id, () => {
    const x=nav.resolve("/atlas-preview/themes/"+id);
    assert.equal(x.kind,"theme");
    assert.equal(x.item.anchors.length,7);
    assert.ok(x.item.anchors.every(a=>nav.resolve(a.target_route)?.kind==="volume"));
  });
  record("reader scene "+i, () => {
    assert.equal(nav.resolve("/atlas-preview/read/"+i)?.kind,"reader");
  });
}
record("VOL-08 is thematic", () => assert.equal(nav.resolve("/atlas-preview/volumes/VOL-08").item.type,"THEMATIC_INDEX"));
record("search is local with usable results",()=>assert.ok(nav.search("후스").length>0));
record("empty search no results",()=>assert.equal(nav.search(""),0));
record("bad route not resolved",()=>assert.equal(nav.resolve("/atlas-preview/volumes/VOL-99"),null));
record("public routes not resolved",()=>assert.equal(nav.resolve("/atlas/public"),null));
record("no publication authority",()=>assert.equal(nav.release().publication_allowed,false));
function mustReject(name, mutate){
  const copy=structuredClone(data);mutate(copy);
  record("reject "+name,()=>assert.throws(()=>validatePrivateAtlasPayload(copy),/ATLAS_PRIVATE_STAGING_CONTRACT/));
}
mustReject("public release",x=>x.access.can_ship=true);
mustReject("public indexing",x=>x.access.allow_public_indexing=true);
mustReject("unauthenticated stage",x=>x.access.requires_authentication=false);
mustReject("missing volume",x=>x.content.volumes.pop());
mustReject("orphan anchor",x=>x.content.themes[0].anchors[0].volume_id="VOL-99");
mustReject("reader answer key",x=>x.content.reading.chapters[0].body_markdown+=" C417-19");
mustReject("third-party image embed",x=>x.content.volumes[0].body_markdown+=" ![photo](https://example.com/image.jpg)");
const report={version:"V4.29",engine:"Node.js 22",status:"PASS",total_checks:checks.length,pass_count:checks.length,checks,release:{can_ship:false,AI_Studio_modified:false,reader_human_tested:false}};
process.stdout.write(JSON.stringify(report,null,2)+"\n");
