#!/usr/bin/env python3
"""Vol.03 expanded draft integrity: relationships, ids, sources and date precision."""
from pathlib import Path
import json
import re
import sys
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VOL = ROOT / "docs/01_CONTENT/VOL03"
P = DATA / "vol03_extension.json"
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

def load(relpath):
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))

ext = load("data/vol03_extension.json")
base = {k: load(f"data/{k}.json") for k in ["people", "events", "locations", "relations"]}
sources_text = (VOL / "05_SOURCE_REGISTER.md").read_text(encoding="utf-8")
source_ids = {f"V03-S{i:02}" for i in range(1, 36)}
found = set(re.findall(r"V03-S\d{2}", sources_text))
check(source_ids <= found, "Missing source IDs in VOL03 register")
base_sources = set(re.findall(r"SRC-\d{4}", (ROOT / "docs/01_CONTENT/RESEARCH_SOURCES.md").read_text(encoding="utf-8")))
actor_ids = {x["id"] for x in ext["actors"]}
loc_ids = {x["id"] for x in ext["locations"]}
event_ids = {x["id"] for x in ext["events"]}
rel_ids = {x["id"] for x in ext["relationships"]}

for kind, items, ids, prefix in [
    ("actors", ext["actors"], actor_ids, r"(PER|MOV)-\d{4}"),
    ("locations", ext["locations"], loc_ids, r"LOC-\d{4}"),
    ("events", ext["events"], event_ids, r"EVT-\d{4}"),
    ("relationships", ext["relationships"], rel_ids, r"REL-\d{4}")
]:
    check(len(ids) == len(items), f"Duplicate IDs in {kind}")
    for item in items:
        check(bool(re.fullmatch(prefix, item["id"])), f"Malformed {kind} ID {item['id']}")
    base_kind = {"actors":"people","locations":"locations","events":"events","relationships":"relations"}[kind]
    base_ids = {x["id"] for x in base[base_kind]}
    check(not (ids & base_ids), f"Colliding IDs in {kind}: {ids & base_ids}")

all_actors = actor_ids | {x["id"] for x in base["people"]}
all_locs = loc_ids | {x["id"] for x in base["locations"]}
all_events = event_ids | {x["id"] for x in base["events"]}

def ref_ids(item, field, ids):
    for ref in item.get(field, []):
        check(ref in ids, f"{item['id']}: invalid {field} -> {ref}")

def source_check(item):
    check(bool(item.get("source_ids")), f"{item['id']}: no evidence")
    for ref in item.get("source_ids", []):
        check(ref in source_ids | base_sources, f"{item['id']}: missing source {ref}")

for actor in ext["actors"]:
    ref_ids(actor, "locations", all_locs)
    source_check(actor)
for event in ext["events"]:
    ref_ids(event, "actor_ids", all_actors)
    ref_ids(event, "location_ids", all_locs)
    source_check(event)
    prec = event.get("date_precision")
    check(bool(event.get("date_label")), f"{event['id']}: missing date_label")
    if prec in ("approximate_period", "approximate_year", "year"):
        check(not event.get("date_start"), f"{event['id']}: unjustified exact date")
        check("year_start" in event, f"{event['id']}: no sortable year")
    elif prec == "day":
        check(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", event.get("date_start",""))), f"{event['id']}: invalid day")
    elif prec == "range":
        check(event.get("year_start") is not None and event.get("year_end") is not None, f"{event['id']}: range without years")
    else:
        check(False, f"{event['id']}: invalid date_precision {prec}")
for relation in ext["relationships"]:
    check(relation.get("from") in all_actors, f"{relation['id']}: invalid source actor")
    check(relation.get("to") in all_actors | all_events, f"{relation['id']}: invalid target")
    source_check(relation)

claims = load("data/vol03_source_claims.json")
claim_ids = [x["id"] for x in claims.get("claims", [])]
check(len(claim_ids) == len(set(claim_ids)), "Duplicate primary claim IDs")
check(claims.get("publication_status") == "DRAFT", "Source claims unexpectedly published")
for claim in claims.get("claims", []):
    check(bool(re.fullmatch(r"CLM-V03-\d{3}", claim.get("id", ""))), f"Malformed claim ID {claim.get('id')}")
    check(claim.get("evidence_tier") in claims.get("evidence_tiers", {}), f"Unknown tier: {claim.get('id')}")
    check(bool(claim.get("locator")), f"Missing edition locator {claim.get('id')}")
    check(bool(claim.get("pending")), f"Missing limitations {claim.get('id')}")
    for ref in claim.get("subject_ids", []):
        check(ref in all_actors, f"Unknown claim subject {claim.get('id')} -> {ref}")
    source_check(claim)

manifest = load("assets/asset_manifest.json")
for asset in manifest:
    check(bool(asset.get("rights_status")), f"{asset['asset_id']}: rights missing")
    check(bool(asset.get("review_status")), f"{asset['asset_id']}: review missing")
    for src in asset.get("source_ids",[]):
        check(src in source_ids | base_sources, f"{asset['asset_id']}: unknown source {src}")
    file_path = ROOT / asset["relative_path"]
    check(file_path.is_file(), f"{asset['asset_id']}: missing {file_path}")
    if file_path.is_file() and file_path.suffix == ".svg":
        try:
            ElementTree.parse(file_path)
        except ElementTree.ParseError as exc:
            errors.append(f"{asset['asset_id']}: invalid SVG {exc}")

if errors:
    print("FAIL:", len(errors), "issue(s)")
    for issue in errors:
        print(" -", issue)
    sys.exit(1)
claims = load("data/vol03_primary_claims.json")["claims"]
claim_ids = [item["id"] for item in claims]
check(len(claim_ids) == len(set(claim_ids)), "Duplicate source claim IDs")
known_subject_ids = all_actors | all_events
for claim in claims:
    check(claim.get("subject_id") in known_subject_ids, f"{claim['id']}: unknown subject")
    source_check(claim)
    check(bool(claim.get("textual_basis")), f"{claim['id']}: missing textual_basis")
    check(bool(claim.get("evidence_tier")), f"{claim['id']}: missing evidence_tier")
    check(bool(claim.get("limitations_ko")), f"{claim['id']}: missing limitations")
    check(claim.get("review_status") == "DRAFT", f"{claim['id']}: cannot auto-approve claims")
if errors:
    print("FAIL: " + str(len(errors)) + " source claim issue(s)")
    for issue in errors:
        print(" -", issue)
    sys.exit(1)
print(f"PASS: {len(claims)} provenance claim cards checked")
print(f"PASS: Vol03 {len(ext['actors'])} actors, {len(ext['events'])} events, {len(ext['relationships'])} relations, {len(ext['locations'])} locations, {len(source_ids)} sources, {len(manifest)} assets, {len(claims["claims"])} claims.")
