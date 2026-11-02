#!/usr/bin/env python3
"""V222: assertion-typed source-route QA (NOT image inspection or 16c collation)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

v219 = load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v220 = load("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")
v221 = load("data/deep/atlas_v221_marburg_witness_accession.json")
d = load("data/deep/atlas_v222_original_image_routes_and_assertions.json")
assert d["version"] == "2.22" and d["parent_commit"] == "28295da1fa87217441057f91c445ffcaee489661"
assert d["base_dataset"] == "data/deep/atlas_v221_marburg_witness_accession.json"
assert all(x is False for x in d["publication_gate"].values())
assert all(x is False for x in v221["publication_gate"].values())
assert v219["metrics"]["chapters"] == 10
assert v219["metrics"]["sentences"] == len(v219["sentences"]) == 543
assert v219["metrics"]["full_integrated_codepoints"] == 35102
assert v220["metrics"]["comparison_units"] == 5
assert v220["metrics"]["direct_16c_witness_collations"] == 0
assert v221["metrics"]["original_exemplar_pages_read"] == 0

sources = {x["id"]: x for x in d["source_records"]}
routes = {x["id"]: x for x in d["route_records"]}
accession = {x["id"]: x for x in v221["accession_targets"]}
assert len(sources) == len(d["source_records"]) == 7
assert len(routes) == len(d["route_records"]) == 4
assert set(routes) == {"ROUTE-V222-K-GALLERY", "ROUTE-V222-Z-CATALOGUE",
                       "ROUTE-V222-ZURICH-W2119", "ROUTE-V222-ZURICH-W2118"}
for src in sources.values():
    assert src["url"].startswith("https://") and src["page_images_directly_inspected"] == 0
for route in routes.values():
    assert route["v221_accession_id"] in accession
    assert route["source_ids"] and set(route["source_ids"]) <= sources.keys()
    assert route["contents_fetched"] is False
    assert route["original_page_inspected"] is False
    assert route["page_number_or_folio_match_verified"] is False
    assert route["action"]
    if route["url"] is not None:
        assert route["url"].startswith("https://")
assert routes["ROUTE-V222-K-GALLERY"]["v221_accession_id"] == "ACC-V221-K"
assert routes["ROUTE-V222-K-GALLERY"]["url"] == "https://www.hapuls.de/node/1472"
assert routes["ROUTE-V222-ZURICH-W2119"]["url"] == "https://www.e-rara.ch/i3f/v20/170052/manifest"
assert routes["ROUTE-V222-ZURICH-W2119"]["item_url"] == "https://www.e-rara.ch/zuz/content/titleinfo/170052"
assert routes["ROUTE-V222-ZURICH-W2118"]["url"] is None
fixes = {f["id"]:f for f in d["identity_corrections"]}
assert set(fixes) == {"FIX-V222-W2119", "PENDING-V222-W2118"}
assert fixes["FIX-V222-W2119"]["value"] == "W 2119"
assert fixes["PENDING-V222-W2118"]["value"] is None
assert all(f["source_ids"] and set(f["source_ids"]) <= sources.keys()
           and f["independent_page_read"] is False for f in fixes.values())

assertions = {x["id"]: x for x in d["assertion_relations"]}
assert set(assertions) == {"ASSERT-V222-Z-K", "ASSERT-V222-DRAFT"}
assert assertions["ASSERT-V222-Z-K"]["type"] == "SIGNED_WITNESS_DELTA_CATALOGUE_STATEMENT"
assert set(assertions["ASSERT-V222-Z-K"]["articles"]) == {"7","13","15"}
assert assertions["ASSERT-V222-DRAFT"]["type"] == "NEGOTIATION_OR_DRAFT_REVISION_SECONDARY_SCHOLARSHIP"
assert set(assertions["ASSERT-V222-DRAFT"]["articles"]) == {"8","11","15"}
assert all(not a["textual_additions_transcribed"] for a in assertions.values())
assert all(set(a["source_ids"]) <= sources.keys() for a in assertions.values())
issues = {x["id"]:x for x in d["open_issues"]}
assert len(issues) == 3
assert all(x["status"] == "OPEN" and set(x["source_ids"]) <= sources.keys() for x in issues.values())
assert d["metrics"] == {
    "source_records":7,
    "original_image_route_candidates":4,
    "confirmed_w2119_bibliography":1,
    "unresolved_w2118_mapping":1,
    "distinct_textual_assertion_types":2,
    "open_issues":3,
    "original_pages_visually_read":0,
    "zk_variant_wordings_collated":0,
    "expert_signoffs":0,
    "published_items":0
}
print("PASS V222: 7 sources; 4 image routes; W2119 identity resolved, W2118 pending")
print("PASS V222: Z/K witness difference separate from drafting changes; original pages 0, HOLD")
