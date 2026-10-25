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
source_ids = {f"V03-S{i:02}" for i in range(1, 54)}
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

# V0.4 provenance object validation (historical texts are separate from later editions).
documents = load("data/vol03_document_witnesses.json")["objects"]
doc_ids = [doc["id"] for doc in documents]
check(len(doc_ids) == len(set(doc_ids)), "Duplicate document/edition IDs")
all_doc_ids = set(doc_ids)
for doc in documents:
    check(bool(doc.get("kind")), f"{doc['id']}: missing provenance kind")
    check(bool(doc.get("date_label")), f"{doc['id']}: missing historical/edition date")
    check(doc.get("review_status") == "DRAFT", f"{doc['id']}: publication not approved")
    source_check(doc)
    parent = doc.get("based_on_id")
    if parent:
        check(parent in all_doc_ids, f"{doc['id']}: unknown based_on_id {parent}")
        check(parent != doc["id"], f"{doc['id']}: self reference")
    ref_ids(doc, "event_ids", all_events)
    ref_ids(doc, "related_document_ids", all_doc_ids)
# A 1433 original agreement and a 2019 edition cannot silently become the same source object.
check("DOC-V03-002" in all_doc_ids and "EDN-V03-003" in all_doc_ids, "Agreement and edited collection must remain distinct")


# V0.5 theological axis and event-causality reference validation.
analysis = load("data/vol03_theology_causality.json")
axes = analysis["axes"]
cases = analysis["cases"]
axis_ids = [item["axis_id"] for item in axes]
case_ids = [item["id"] for item in cases]
check(len(axis_ids) == len(set(axis_ids)), "Duplicate theological axis IDs")
check(len(case_ids) == len(set(case_ids)), "Duplicate causal case IDs")
for axis in axes:
    ref_ids({"id":axis["axis_id"],"subject_ids":axis.get("subject_ids",[])}, "subject_ids", all_actors)
    for sid in axis.get("sources", []):
        check(sid in source_ids | base_sources, f"{axis['axis_id']}: missing source {sid}")
    check(bool(axis.get("uncertainty")), f"{axis['axis_id']}: missing historical uncertainty")
for case in cases:
    ref_ids(case,"event_ids",all_events)
    ref_ids(case,"actors",all_actors)
    source_check(case)
    check(bool(case.get("causal_factors")), f"{case['id']}: missing causal factors")
    check(case.get("interpretation_status") == "DRAFT", f"{case['id']}: not human approved")


# Map coordinate provenance and historical cartography guards.
maps = load("data/vol03_map_points.json")
map_ids = {"MAP-V03-01","MAP-V03-02","MAP-V03-03","MAP-V03-04"}
map_assets = {asset["asset_id"] for asset in manifest if asset.get("type") == "svg_historical_educational_point_map"}
check(map_ids <= map_assets, f"Missing registered map assets: {map_ids - map_assets}")
check(len(maps["points"]) == 13, "Expected 13 approximate map reference points")
check(len({p["key"] for p in maps["points"]}) == len(maps["points"]), "Duplicate map point keys")
for point in maps["points"]:
    check(point["location_id"] in all_locs, f"map point {point['key']}: unknown location")
    check(-90 <= point["latitude"] <= 90 and -180 <= point["longitude"] <= 180, f"{point['key']}: bad coordinates")
    check(bool(point.get("source_url")), f"{point['key']}: missing coordinate provenance")
    check("approx" in point["coordinate_status"] or "vicinity" in point["coordinate_status"], f"{point['key']}: false precision")
    for mid in point.get("maps",[]):
        check(mid in map_ids, f"{point['key']}: unknown map {mid}")
check(maps["map_kind"] == "modern_reference_points_historical_education", "Maps must be flagged as modern-coordinate schematics")



# V0.7 six binary illustrations: validate staging without pretending absent files were committed.
art_stage = load("assets/illustrations/vol03/ILLUSTRATION_STAGE.json")
art_items = art_stage["assets"]
art_ids = [entry["id"] for entry in art_items]
check(len(art_items) == 6 and len(art_ids) == len(set(art_ids)),
      "Expected six unique staged illustrations")
check(bool(re.fullmatch(r"[0-9a-f]{64}", art_stage.get("zip_sha256", ""))),
      "Invalid artwork ZIP checksum")
registered_assets = {item["asset_id"] for item in manifest}
for entry in art_items:
    srcs = entry.get("source_ids", [])
    check(bool(srcs), f"{entry['id']}: illustration lacks source")
    for source in srcs:
        check(source in source_ids | base_sources, f"{entry['id']}: unregistered visual source {source}")
    check(bool(re.fullmatch(r"[0-9a-f]{64}", entry.get("webp_sha256", ""))),
          f"{entry['id']}: invalid WebP SHA256")
    check(bool(entry.get("historical_limitation_ko")),
          f"{entry['id']}: missing reconstruction limitations")
    st = entry.get("status")
    if st == "PENDING_BINARY_COMMIT":
        check(entry["id"] not in registered_assets,
              f"{entry['id']}: manifest pretends uncommitted file is present")
    elif st == "IN_WORKTREE_PENDING_GIT_COMMIT":
        check(entry["id"] in registered_assets,
              f"{entry['id']}: locally installed image lacks manifest entry")
        webp_path = ROOT / entry["relative_path"]
        check(webp_path.is_file(), f"{entry['id']}: installed image missing")
        if webp_path.is_file():
            from hashlib import sha256
            check(sha256(webp_path.read_bytes()).hexdigest() == entry["webp_sha256"],
                  f"{entry['id']}: installed image SHA256 mismatch")
    else:
        check(False, f"{entry['id']}: invalid pending image state {st}")


# V0.7 presentation/UX index is non-published; unresolved image binaries must never
# be mistakenly marked safe to display.
presentation = load("data/vol03_presentation_index.json")
stage_ids = {entry["id"] for entry in art_stage["assets"]}
map_ids = {"MAP-V03-01", "MAP-V03-02", "MAP-V03-03", "MAP-V03-04"}
for page in presentation["people_pages"]:
    check(page["person_id"] in all_actors, f"{page['id']}: unknown person ID")
    check(page["media_id"] in stage_ids, f"{page['id']}: missing portrait staging ID")
    check(page["map_id"] in map_ids, f"{page['id']}: unknown map ID")
    check((ROOT / page["chapter_path"]).is_file(),
          f"{page['id']}: missing chapter")
    for source in page["source_ids"]:
        check(source in source_ids, f"{page['id']}: missing research source {source}")
    check(not page["media_safe_to_display"] and not page["is_published"],
          f"{page['id']}: cannot display unpublished AI portrait")
for page in presentation["visual_story_pages"]:
    check(page["media_id"] in stage_ids,
          f"{page['card_id']}: unknown historical reconstruction")
    check((ROOT / page["chapter_path"]).is_file(),
          f"{page['card_id']}: missing chapter")
    ref_ids({"id": page["card_id"], "linked_entity_ids":page["linked_entity_ids"]},
            "linked_entity_ids", all_actors | all_locs | all_events)
    check(not page["media_safe_to_display"],
          f"{page['card_id']}: cannot display unpublished reconstruction")
for item in presentation["map_views"]:
    check(item["asset_id"] in map_ids and item["asset_id"] in registered_assets,
          f"{item['id']}: map SVG not registered")
for item in presentation["research_views"]:
    check((ROOT / item["document_path"]).is_file(),
          f"{item['view_id']}: research document not found")
    check((ROOT / item["data_path"]).is_file(),
          f"{item['view_id']}: research JSON not found")
check(not presentation["publication_gate"]["approved"] and
      not presentation["publication_gate"]["can_ship"],
      "Published flags not authorized")

if errors:
    print("FAIL: " + str(len(errors)) + " source claim issue(s)")
    for issue in errors:
        print(" -", issue)
    sys.exit(1)
print(f"PASS: {len(claims)} provenance claim cards checked")
print(f"PASS: Vol03 {len(ext['actors'])} actors, {len(ext['events'])} events, {len(ext['relationships'])} relations, {len(ext['locations'])} locations, {len(source_ids)} sources, {len(manifest)} assets, {len(claims)} claims, {len(documents)} provenance objects, {len(axes)} theological axes, {len(cases)} causal cases, {len(maps['points'])} mapped coordinate points, {len(art_items)} staged AI illustrations, {len(presentation["people_pages"])} persona pages.")
