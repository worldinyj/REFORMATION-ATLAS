#!/usr/bin/env python3
"""Check the materialized VOL03 graph against canonical source JSON and publication gates.

Run from the project root. Requires Python 3.11+ standard library only.
"""
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
index=load("data/vol03_integrated_catalog_v08.json")
stage=load("assets/illustrations/vol03/ILLUSTRATION_STAGE.json")
canonical=load("assets/asset_manifest.json")
errors=[]
nodes=index.get("nodes",[])
edges=index.get("edges",[])
ids=[x["id"] for x in nodes]
seen=set(ids)
if len(ids)!=len(seen):errors.append("duplicate catalog node ID")
keys=[]
for edge in edges:
    keys.append((edge["from"],edge["to"],edge["type"]))
    if edge["from"] not in seen or edge["to"] not in seen:
        errors.append(f"broken graph edge: {edge}")
if len(keys)!=len(set(keys)):errors.append("duplicate graph edge")
sources=set(re.findall(r"V03-S\d{2}",(ROOT/"docs/01_CONTENT/VOL03/05_SOURCE_REGISTER.md").read_text(encoding="utf-8")))
sources|=set(re.findall(r"SRC-\d{4}",(ROOT/"docs/01_CONTENT/RESEARCH_SOURCES.md").read_text(encoding="utf-8")))
for source in sources:
    if source not in seen:errors.append(f"missing source node: {source}")
for x in nodes:
    for source in x.get("source_ids",[]):
        if source not in sources:errors.append(f"{x['id']} has unknown source {source}")
    typ=x.get("type")
    path=x.get("source_path","")
    if not path:errors.append(f"{x['id']}: missing source_path")
    if typ=="asset_committed":
        if not x.get("exists_in_git") or not (ROOT/path).is_file():
            errors.append(f"{x['id']}: registered graphic file missing")
        if x.get("public_visible") is not False:
            errors.append(f"{x['id']}: premature publication")
    elif typ=="asset_pending_binary":
        if x.get("exists_in_git") is not False or x.get("public_visible") is not False:
            errors.append(f"{x['id']}: pending file marked committed/publishable")
    elif typ not in ("source_reference",):
        if not (ROOT/path).is_file():errors.append(f"{x['id']}: missing source document {path}")
    if x.get("publication_allowed") is True:errors.append(f"{x['id']}: page not approved")
actual_staged={i["id"] for i in stage["assets"]}
expected_staged={i["id"] for i in nodes if i["type"]=="asset_pending_binary"}
if expected_staged!=actual_staged:errors.append("staged artifact set inconsistent")
canonical_ids={i["asset_id"] for i in canonical}
if canonical_ids & expected_staged:errors.append("binary pending items wrongly in asset manifest")
if index["publication_gate"].get("approved") or index["publication_gate"].get("can_ship"):
    errors.append("publication flag enabled without human approval")
expected_edges=set(keys)
for n in nodes:
    for sid in n.get("source_ids",[]):
        if (n["id"],sid,"grounded_in") not in expected_edges:
            errors.append(f"{n['id']}: missing provenance edge to {sid}")
if errors:
    print("FAIL:",len(errors))
    for x in errors:print(" -",x)
    sys.exit(1)
print("PASS:",len(nodes),"nodes,",len(edges),"edges,",len(sources),"source refs,",len(expected_staged),"staged binary images")
