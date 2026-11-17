#!/usr/bin/env node
"use strict";

// V4.29: exact-content, source-provenance and private-staging boundary validation.
// Uses only Node.js core APIs. No network, no AI Studio credentials, no app writes.
const fs = require("node:fs");
const path = require("node:path");
const { execFileSync } = require("node:child_process");

const root = path.resolve(__dirname, "../..");
const sourcePath = "research/data/V4_23_L0_INTERNAL_ALPHA_CONTENT_BUNDLE_DRAFT.json";
const importPath = "handoff/V429_AI_STUDIO_PRIVATE_L0_CONTENT_IMPORT.json";
const browserPath = "research/artifacts/V428_browser_evidence/V428_BROWSER_E2E_RESULTS.json";
const load = relative => JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
const blob = relative => execFileSync("git", ["hash-object", path.join(root, relative)], { encoding: "utf8" }).trim();
const orig = load(sourcePath);
const pkg = load(importPath);
const browser = load(browserPath);
const errors = [];
const check = (condition, label) => { if (!condition) errors.push(label); };
const same = (a,b) => JSON.stringify(a) === JSON.stringify(b);

check(pkg.schema === "REFORMATION_ATLAS_L0_STAGING_IMPORT_V1", "schema");
check(pkg.provenance.sourceGitBlobSha === blob(sourcePath), "frozen source SHA");
check(pkg.provenance.sourceFile === sourcePath, "source path");
check(pkg.provenance.browserEvidencePath === browserPath, "browser provenance path");
check(pkg.privacyAndRights.canShip === false && pkg.publicationState === "BLOCKED", "public release blocked");
check(pkg.privacyAndRights.allowsMainMerge === false && pkg.privacyAndRights.allowsPublicPublishing === false, "public/main restrictions");
check(pkg.privacyAndRights.requiresLoginOrPrivateAccess === true, "staging access control");
check(pkg.appContract.accessControlEnforcedByHostAppNotByJson === true, "privacy is host responsibility");
check(pkg.appContract.routeTargetsAreIdsNotURLs === true, "logical references, not invented URLs");
check(pkg.appContract.mustHideEditorScoringKeys === true, "editor answer key excluded");

check(pkg.volumes.length === 8, "8 historical volume cards");
check(pkg.themes.length === 6, "6 theme articles");
check(pkg.reader.chapters.length === 6, "6 introductory reader chapters");
check(pkg.navigation.countThemeToVolumeLinks === 42, "42 forward theme links");
check(pkg.volumes.filter(v=>v.kind === "THEMATIC_INDEX").length === 1, "exactly one cross-volume thematic archive");
check(pkg.volumes.find(v=>v.id==="VOL-08")?.relatedThemes.length===0, "VOL-08 no redundant era bridges");
check(pkg.volumes.filter(v=>v.id!=="VOL-08").every(v=>v.relatedThemes.length===6), "7 history volumes have 6 reverse links");

for (let i = 0; i < orig.volumes.length; i++) {
  const x = orig.volumes[i], y = pkg.volumes[i];
  check(x.id === y?.id && x.title === y?.title && x.kind === y?.kind, "volume metadata "+x.id);
  check(x.reader_content_markdown === y?.bodyMarkdown, "volume exact copy "+x.id);
  check(x.question === y?.leadQuestion && x.summary === y?.description, "volume overview copy "+x.id);
  check(x.source.blob_sha === y?.contentSource.gitBlobSha, "volume source SHA "+x.id);
}
const roleLabels = {
  CORE_CASE:"핵심 사례",
  CONTEXT_BRIDGE:"맥락 연결",
  LIMITED_CONTEXT_NOT_DOCTRINE:"제한된 배경"
};
const uniqueLinks = new Set();
for(let i=0;i<orig.themes.length;i++){
  const x=orig.themes[i],y=pkg.themes[i];
  check(x.id===y?.id && x.title===y?.title, "theme metadata "+x.id);
  check(x.overview_markdown===y?.bodyMarkdown, "theme exact prose "+x.id);
  check(x.anchors.length===7 && y?.compareLinks.length===7, "seven link targets per theme "+x.id);
  for(let k=0;k<x.anchors.length;k++){
    const a=x.anchors[k],z=y.compareLinks[k];
    const key=x.id+"|"+a.volume_id;
    check(!uniqueLinks.has(key), "duplicate theme/volume "+key);
    uniqueLinks.add(key);
    check(z.target.kind==="VOLUME" && z.target.id===a.volume_id && a.volume_id!=="VOL-08", "destination ID "+key);
    check(z.title===a.title && z.connectionKind===a.role && z.connectionLabel===roleLabels[a.role], "meaningful link label "+key);
    check(pkg.volumes.some(v=>v.id===z.target.id), "target exists "+key);
  }
}
check(uniqueLinks.size===42, "42 unique theme links");
check(orig.introduction.intro_preface_markdown===pkg.reader.prefaceMarkdown, "preface exact copy");
check(pkg.reader.readingTimeMeasured===false, "reader time still unmeasured");
for(let i=0;i<orig.introduction.scenes.length;i++){
 const a=orig.introduction.scenes[i],z=pkg.reader.chapters[i];
 check(a.id===z?.id && a.heading===z?.title, "intro title "+a.id);
 check(a.markdown===z?.bodyMarkdown, "intro prose exact copy "+a.id);
}
const allBodies=[
  ...pkg.volumes.map(x=>x.bodyMarkdown),
  ...pkg.themes.map(x=>x.bodyMarkdown),
  ...pkg.reader.chapters.map(x=>x.bodyMarkdown),
  pkg.reader.prefaceMarkdown
].join("\n");
check(!/!\[[^\]]*\]\([^)]+\)/.test(allBodies), "no external embedded image requests");
check(!/C417-\d+|Q419-\d+|SRC421-\d+|정답표/.test(allBodies), "no reader-facing scores or internal claim IDs");
check(!Object.hasOwn(pkg,"editor_only"), "editor-only registry not shipped in import");
for(const held of orig.editor_only.held_claims){check(!JSON.stringify(pkg).includes(held.id), "held claim IDs are not present "+held.id);}
check(!pkg.appContract.defaultShowEditorMetadata, "editor metadata not visible");

check(browser.setup.outcome==="success", "browser runner setup completed");
for(const name of ["chromium","webkit"]){
 const t=browser.engines[name];
 check(t?.exit_code==="0" && t?.report_present, name+" browser test passed");
 check(t?.test_report?.checks_performed===236 && t?.test_report?.checks_passed===236, name+" 236/236");
 check(t?.test_report?.failures?.length===0, name+" zero browser errors");
 check(t?.test_report?.expected_input_blob_sha===t?.test_report?.actual_input_blob_sha, name+" exact HTML blob check");
}
check(pkg.integrationChecks.expectedBrowserSmokeChecksPassed===472, "472 browser checks noted");
check(pkg.integrationChecks.realAiStudioStagingTestCompleted===false, "AI Studio not falsely claimed");
check(pkg.integrationChecks.realHistorianReviewCompleted===false, "no fictitious historians");
check(pkg.integrationChecks.realFiveReaderPilotCompleted===false, "no fictitious readers");
check(pkg.integrationChecks.realRightsClearanceCompleted===false, "no fictitious rights signoff");

const summary={schema:"REFORMATION_ATLAS_V429_IMPORT_CONTRACT_VALIDATION",
status:errors.length?"FAIL":"PASS",
source_sha:blob(sourcePath),package_sha:blob(importPath),
counts:{volumes:pkg.volumes.length,themes:pkg.themes.length,themeLinks:uniqueLinks.size,readerChapters:pkg.reader.chapters.length,verifiedBrowserChecks:472},
actual_staging_deployed:false,actual_human_review_sessions:0,can_ship:false,errors};
console.log(JSON.stringify(summary,null,2));
if(errors.length)process.exitCode=1;
