#!/usr/bin/env python3
"""V221 accession ledger QA: schema and cross-release identity, not original image inspection."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

v19 = read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v20 = read("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")
v21 = read("data/deep/atlas_v221_marburg_witness_accession.json")
assert v21["version"] == "2.21" and v20["version"] == "2.20"
assert v21["parent_v220_commit"] == "8a77b9d2be532d1473358f320f6c77e358d338e1"
assert v21["baseline_dataset"] == "data/deep/atlas_v220_marburg_augsburg_variant_collation.json"
assert all(v is False for v in v21["publication_gate"].values())
assert all(v is False for v in v20["publication_gate"].values())
assert v19["metrics"]["chapters"] == 10 and v19["metrics"]["sentences"] == 543
assert v20["metrics"]["comparison_units"] == 5 and v20["metrics"]["direct_16c_witness_collations"] == 0

sources = {s["id"]: s for s in v21["source_records"]}
targets = {t["id"]: t for t in v21["accession_targets"]}
# V221 alignment entries use the V220 variant ID as their primary reference key.\nunits = {u["v220_variant_id"]: u for u in v21["variant_alignment_targets"]}
parent_units = {u["id"]: u for u in v20["variant_units"]}
assert len(sources) == len(v21["source_records"]) == 7
assert len(targets) == len(v21["accession_targets"]) == 6
assert len(units) == len(v21["variant_alignment_targets"]) == 3
assert set(units) == {"V220-MAR-07","V220-MAR-13","V220-MAR-15"}
assert set(targets) == {"ACC-V221-Z","ACC-V221-K","ACC-V221-ZH1",
                        "ACC-V221-ZH2","ACC-V221-BS","ACC-V221-U1883"}
assert {targets[x]["kind"] for x in ("ACC-V221-Z","ACC-V221-K")} == {"SIGNED_MANUSCRIPT"}
assert sum(t["kind"] == "SIXTEENTH_CENTURY_PRINT_EXEMPLAR" for t in targets.values()) == 3
assert sum(t["kind"] == "NINETEENTH_CENTURY_FACSIMILE_REPRODUCTION" for t in targets.values()) == 1
assert targets["ACC-V221-BS"]["vd16_id"] == "W 2108"
assert targets["ACC-V221-BS"]["shelfmark"] == "UBH Falk 2950:5"
assert targets["ACC-V221-K"]["shelfmark"] == "Best. 3 Nr. 245 fol. 60r–64v"
for x in ("ACC-V221-ZH1","ACC-V221-ZH2"):
    assert targets[x]["vd16_mapping_verified"] is False
    assert targets[x]["possible_vd16_ids"] == ["W 2118","W 2119"]

for s in sources.values():
    assert s["url"].startswith("https://")
    assert s["image_pages_inspected"] == 0
for t in targets.values():
    assert t["source_ids"] and set(t["source_ids"]) <= sources.keys()
    assert t["exemplar_direct_page_opened"] is False
    assert t["sections_to_collate"] == ["7","13","15"]
    assert t["stable_url"].startswith("https://")
for uid, unit in units.items():
    assert uid in parent_units and parent_units[uid]["reader_key"] == "MARBURG"
    assert unit["article"] == parent_units[uid]["article"]
    assert unit["z_added_text"] is None
    assert unit["k_parallel_text"] is None
    assert unit["print_variant_texts"] == []
    assert unit["status"] == "OPEN"
    assert set(("ACC-V221-Z","ACC-V221-K")) <= set(unit["witness_candidates"])
    assert set(unit["witness_candidates"]) <= targets.keys()
assert v21["release_policy"] == {
    "source_discovery_is_not_original_page_reading":True,
    "third_party_handwriting_attribution_requires_primary_confirmation":True,
    "publication_approved":False}
assert v21["metrics"] == {
    "source_records":7, "accession_targets":6, "original_manuscripts":2,
    "original_print_exemplars":3, "later_facsimile_references":1,
    "variant_alignment_targets":3, "original_exemplar_pages_read":0,
    "completed_variant_collations":0, "publication_items":0}
assert len(v21["next_work_order"]) == 6
assert {x["target"] for x in v21["next_work_order"]} == set(targets)
print("PASS V221: 6 accession objects, 7 bibliographic sources, 3 unresolved Z/K alignments")
print("PASS V221: V219/V220 baselines intact, original pages read=0, publication HOLD")
