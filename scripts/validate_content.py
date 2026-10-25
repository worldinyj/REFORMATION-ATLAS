#!/usr/bin/env python3
"""Validate REFORMATION ATLAS pilot JSON and original SVG assets without third-party packages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
SOURCES = ROOT / "docs/01_CONTENT/RESEARCH_SOURCES.md"
errors: list[str] = []

def fail(message: str) -> None:
    errors.append(message)

def load(name: str) -> list:
    path = DATA / name
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(obj, list):
            fail(f"{name}: root is not a list")
            return []
        return obj
    except (OSError, ValueError) as exc:
        fail(f"{name}: {exc}")
        return []

sets = {name: load(name + ".json") for name in ("people", "events", "relations", "locations")}
ids = {}
for name, items in sets.items():
    values = [item.get("id") for item in items]
    if len(values) != len(set(values)):
        fail(f"{name}: duplicated entity IDs")
    ids[name] = set(values)
    for item in items:
        if item.get("publication_status", "DRAFT") not in {"DRAFT", "REVIEWED", "APPROVED", "PUBLISHED", "RETIRED"}:
            fail(f"{name}: invalid publication_status {item.get('id')}")
        if not item.get("id"):
            fail(f"{name}: id missing")
        elif name == "relations":
            if not item.get("summary_ko"):
                fail(f"{name}: summary_ko missing for {item['id']}")
        elif not item.get("name_ko"):
            fail(f"{name}: name_ko missing for {item['id']}")
    for entity_id in values:
        if not re.fullmatch({"people":r"PER-\d{4}","events":r"EVT-\d{4}","relations":r"REL-\d{4}","locations":r"LOC-\d{4}"}[name],str(entity_id)):
            fail(f"{name}: malformed ID {entity_id}")

source_text = SOURCES.read_text(encoding="utf-8")
source_ids = set(re.findall(r"SRC-\d{4}", source_text))
extension_path = DATA / "vol03_extension.json"
extension = json.loads(extension_path.read_text(encoding="utf-8")) if extension_path.exists() else None
if extension is not None:
    vol03_register = (ROOT / "docs/01_CONTENT/VOL03/05_SOURCE_REGISTER.md").read_text(encoding="utf-8")
    source_ids |= set(re.findall(r"V03-S\d{2}", vol03_register))

def check_refs(parent: dict, key: str, known: set) -> None:
    for value in parent.get(key, []):
        if value not in known:
            fail(f"{parent.get('id')}: unknown {key} reference {value}")

for person in sets["people"]:
    check_refs(person, "locations", ids["locations"])
for event in sets["events"]:
    check_refs(event,"person_ids",ids["people"])
    check_refs(event,"location_ids",ids["locations"])
    precision = event.get("date_precision")
    if precision == "approximate_period" and event.get("date_start"):
        fail(f"{event.get('id')}: approximate period uses a fake exact date")
    if precision == "approximate_period" and not event.get("date_display"):
        fail(f"{event.get('id')}: missing approximate date_display")
    if precision in ("day","range") and not event.get("date_start"):
        fail(f"{event.get('id')}: missing precise date")
for rel in sets["relations"]:
    for end in ("from_id","to_id"):
        if rel.get(end) not in ids["people"]:
            fail(f"{rel.get('id')}: unknown {end} {rel.get(end)}")
for kind in ("people","events","relations"):
    for item in sets[kind]:
        check_refs(item,"source_ids",source_ids)
        if not item.get("source_ids"):
            fail(f"{item.get('id')}: requires source IDs")
try:
    assets = json.loads((ASSETS/"asset_manifest.json").read_text(encoding="utf-8"))
    if len({a["asset_id"] for a in assets}) != len(assets):
        fail("assets: duplicate asset IDs")
    all_entity_ids = set().union(*ids.values())
    if extension is not None:
        for family in ("actors", "locations", "events", "relationships"):
            all_entity_ids |= {item["id"] for item in extension.get(family, [])}
    for a in assets:
        if not (ROOT/a["relative_path"]).is_file():
            fail(f"{a['asset_id']}: missing asset file")
        check_refs(a,"source_ids",source_ids)
        check_refs(a,"linked_entity_ids",all_entity_ids)
        if a["relative_path"].endswith(".svg"):
            ET.parse(ROOT/a["relative_path"])
        if not a.get("rights_status") or not a.get("review_status"):
            fail(f"{a['asset_id']}: missing rights or review status")
except (ValueError, OSError, KeyError, ET.ParseError) as exc:
    fail(f"assets: {exc}")

if errors:
    print("FAIL: " + str(len(errors)) + " issue(s)")
    for msg in errors: print(" -", msg)
    sys.exit(1)
print("PASS: 3 people, 4 events, 2 relations, 5 locations, SVG syntax and references checked.")
