#!/usr/bin/env python3
"""V1.65 cross-file integration readiness: fail closed on IDs, sources and permissions."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
manifest=read("data/contracts/atlas_v165_integration_readiness_manifest.json")
assert manifest["publication_gate"]=={"approved":False,"can_ship":False}
assert manifest["release_policy"]["main_untouched"] and manifest["release_policy"]["ai_studio_untouched"]
files=[p for group in manifest["domain_groups"] for p in group["file_paths"]]
assert len(files)==18 and len(files)==len(set(files))
assert all((ROOT/f).is_file() for f in files)
r154=[read(f"data/deep/atlas_v154_group_{x}.json") for x in "abcdef"]
assert sum(len(g["modules"]) for g in r154)==60
pages=read("data/deep/atlas_v156_extended_narratives.json")["pages"]
pids={p["id"] for p in pages}
assert len(pids)==10
mapdata=read("data/contracts/atlas_v157_historical_city_map.json")
city_ids={p["id"] for p in mapdata["places"]}
links=read("data/contracts/atlas_v157_spatiotemporal_links.json")["links"]
assert len(city_ids)==11 and all(x["reader_page_id"] in pids and x["place_id"] in city_ids for x in links)
assert all(p["coordinate_scope"]=="CITY_CENTROID_APPROXIMATE" for p in mapdata["places"])
visual=read("data/contracts/atlas_v158_visual_rights_registry.json")["assets"]
portraits=read("data/contracts/atlas_v159_portrait_item_provenance.json")["portrait_candidates"]
facsimiles=read("data/contracts/atlas_v160_document_facsimile_review.json")["facsimiles"]
assert len(visual)==14 and len(portraits)==5 and len(facsimiles)==4
assert all(not v["approved_to_publish"] for v in visual+portraits)
assert all(not x["image_approved"] for x in facsimiles)
ed=read("data/contracts/atlas_v161_edition_comparison_cards.json")["works"]
edition_ids={e["id"] for w in ed for e in w["editions"]}
assert len(edition_ids)==5
matrix=read("data/contracts/atlas_v162_edition_article_matrix.json")["rows"]
matrix_ids={m["id"] for m in matrix}
assert len(matrix_ids)==6 and all(set(m["references"])<=edition_ids for m in matrix)
ev=read("data/contracts/atlas_v163_source_evidence_cards.json")["cards"]
nav=read("data/contracts/atlas_v164_evidence_navigation.json")["claims"]
assert len(ev)==len(nav)==8
ev_ids={e["id"] for e in ev}
assert ev_ids=={n["claim_id"] for n in nav}
assert all(e["matrix_id"] in matrix_ids and not e["primary_original_folio_checked"] for e in ev)
assert all(n["reader_page_id"] in pids and set(n["edition_ids"])<=edition_ids and not n["verified_primary"] for n in nav)
assert {x["id"] for x in manifest["blocking_issues"]}=={f"BLOCK-{i:02d}" for i in range(1,6)}
print("PASS V1.65 cross-domain: 18 files, 60 units, 10 pages, 11 cities, 14 assets, 5 editions, 8 evidence paths; publication BLOCKED")
