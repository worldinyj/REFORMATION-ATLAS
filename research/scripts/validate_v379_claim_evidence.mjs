#!/usr/bin/env node
/** V3.79 research claim-evidence validator. No network or external dependencies. */
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import process from "node:process";

const path = resolve(process.argv[2] ?? "research/data/V3_79_BUCER_VADIAN_CLAIM_EVIDENCE.json");
const problems = [];
let root;
try { root = JSON.parse(readFileSync(path, "utf8")); }
catch (err) { console.error("FAIL: Cannot load JSON:", err.message); process.exit(2); }

const E = root.evidence ?? [], C = root.claims ?? [];
const unique = arr => new Set(arr).size === arr.length;
const evidence = new Map(E.map(x => [x.id, x]));
const claim = new Map(C.map(x => [x.id, x]));
const fail = (key,msg) => problems.push(`${key}: ${msg}`);
if(root.version !== "V3.79") fail("VERSION","expected V3.79");
if(root.deployment?.can_ship !== false) fail("RELEASE","research branch must remain not shippable");
if(!unique(E.map(x=>x.id)))fail("EVIDENCE","duplicate evidence ids");
if(!unique(C.map(x=>x.id)))fail("CLAIMS","duplicate claim ids");
if(C.length === 0 || E.length === 0)fail("SIZE","no claims or no evidence");

for(const e of E) {
  if(!e.id || !e.kind || !e.inspection || !e.title)fail(e.id??"E?","missing evidence metadata");
  if(e.kind !== "prior_research_unverified" && !e.uri)fail(e.id,"citable source URI missing");
}
const allowed = new Set(["editorial_eligible","research_only","blocked"]);
for (const c of C) {
  if(!c.id || !c.text || !c.assessment)fail(c.id??"C?","incomplete claim");
  if(!allowed.has(c.public_use))fail(c.id,"unrecognized publication status");
  if(!Array.isArray(c.evidence_ids) || !c.evidence_ids.length)fail(c.id,"no evidentiary references");
  for(const id of c.evidence_ids ?? []) if(!evidence.has(id))fail(c.id,`evidence ${id} missing`);
  if(c.public_use === "editorial_eligible") {
    if(!c.editorial_attribution)fail(c.id,"requires explicit editorial/source attribution");
    for(const id of c.evidence_ids ?? []) {
      const e=evidence.get(id);
      if(["catalog_search_index","prior_research_unverified"].includes(e?.kind))fail(c.id,`cannot publish using ${e.kind}`);
    }
  }
  if(["unresolved_identity","unverified_equivalence","not_directly_inspected"].includes(c.assessment) && c.public_use !== "blocked")
    fail(c.id,"identity or direct-inspection claim must be blocked");
}
const forcedBlocks = ["ATLAS-1536-VAD-006","ATLAS-1536-VAD-007","ATLAS-1536-VAD-008"];
for(const id of forcedBlocks)if(claim.get(id)?.public_use !== "blocked")fail(id,"hard gate violated");
for(const d of root.provenance_distinctions ?? [])if(!Array.isArray(d.not_equal)||d.not_equal.length!==2)fail("PROVENANCE","bad not_equal pair");
const count={editorial_eligible:0,research_only:0,blocked:0};
for(const c of C)if(count[c.public_use]!==undefined)count[c.public_use]++;
console.log(JSON.stringify({version:root.version,claim_count:C.length,evidence_count:E.length,publication_status_count:count,problems},null,2));
if(problems.length)process.exit(1);
console.log("PASS: Research claim-evidence integrity gates; no deployment authorized.");
