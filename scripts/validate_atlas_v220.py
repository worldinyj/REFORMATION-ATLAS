#!/usr/bin/env python3
"""V220 research variant appendix QA. Checks internal evidence links, NOT historical truth."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

v219 = read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
d = read("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")

assert d["version"] == "2.20"
assert d["base_v219_commit"] == "f865c18651b0e3a393fc80dfb1577c96dfdb5994"
assert d["base_dataset"] == "data/deep/atlas_v219_structured_ten_reader_critical_editions.json"
assert all(value is False for value in d["publication_gate"].values())
assert all(value is False for value in v219["publication_gate"].values())
expected = dict(chapters=10, sections=74, paragraphs=128, sentences=543,
                focus_anchors=30, journey_stage_bridges=30, codepoints=35102)
assert d["preservation_baseline"] == expected
m = v219["metrics"]
assert (m["chapters"], m["sections"], m["paragraphs"], m["sentences"],
        len(v219["focus_anchors"]), len(v219["v215_stage_sentence_bridge"]),
        m["full_integrated_codepoints"]) == tuple(expected.values())

sources = {s["id"]: s for s in d["source_registry"]}
witnesses = {w["id"]: w for w in d["witness_registry"]}
units = {u["id"]: u for u in d["variant_units"]}
notes = {n["id"]: n for n in v219["source_notes"]}
sentences = {s["id"]: s for s in v219["sentences"]}
assert len(sources) == 4 and len(witnesses) == 8 and len(units) == 5
assert len(notes) == 4 and len(sentences) == 543
assert set(units) == {"V220-MAR-07", "V220-MAR-13", "V220-MAR-15",
                      "V220-AUG-04", "V220-AUG-10"}
assert len(set(sources)) == len(d["source_registry"])
assert len(set(witnesses)) == len(d["witness_registry"])
assert len(set(units)) == len(d["variant_units"])
for source in sources.values():
    assert source["url"].startswith("https://")
    assert source["visually_read_original"] is False
for witness in witnesses.values():
    assert witness["source_ids"] and set(witness["source_ids"]) <= sources.keys()
    assert witness["evidence"]
for unit in units.values():
    assert unit["original_witness_collated"] is False
    assert unit["evidence_source_ids"] and set(unit["evidence_source_ids"]) <= sources.keys()
    assert unit["witness_ids"] and set(unit["witness_ids"]) <= witnesses.keys()
    assert unit["v219_sentence_ids"]
    note = notes[unit["source_note_id"]]
    assert note["reader_key"] == unit["reader_key"]
    assert note["original_sixteenth_century_witness_collated"] is False
    for sid in unit["v219_sentence_ids"]:
        sentence = sentences[sid]
        assert sentence["reader_key"] == unit["reader_key"]
        assert sentence["passage_id"] == note["passage_id"]
        assert sentence["can_publish"] is False
    if unit["reader_key"] == "MARBURG":
        assert unit["article"] in ("7","13","15")
        assert unit["z_extra_text"] is None and unit["k_counterpart_text"] is None
        assert unit["evidence_level"].startswith("CATALOGUE_")
        assert unit["review_status"] == "PENDING_DUAL_WITNESS_IMAGES"
        assert unit["evidence_source_ids"] == ["V220-ZCAT","V220-GHDI"]
    else:
        assert unit["reader_key"] == "AUGSBURG" and unit["article"] in ("IV","X")
        assert unit["ed1_reading_excerpt"] != unit["ed3_reading_excerpt"]
        assert unit["evidence_level"].startswith("CR1858_")
        assert unit["review_status"] == "CR_PAGE_CHECKED_EARLY_PRINT_PENDING"
assert "distribuantur" in units["V220-AUG-10"]["ed1_reading_excerpt"]
assert "exhibeantur" in units["V220-AUG-10"]["ed3_reading_excerpt"]
assert "WHOLE_ARTICLE" in units["V220-AUG-04"]["delta_class"]
unique_sentences = set(sid for u in units.values() for sid in u["v219_sentence_ids"])
metrics = d["metrics"]
assert metrics == {
    "comparison_units":5, "marburg_catalogue_differences":3,
    "augsburg_critical_print_collations":2, "direct_16c_witness_collations":0,
    "linked_v219_sentence_ids_unique":len(unique_sentences),
    "expert_signoffs":0, "published_items":0,
}
assert len(d["next_evidence_tasks"]) == 5
assert all(task["status"] == "OPEN" for task in d["next_evidence_tasks"])
print("PASS V220: 5 comparison units (3 Z/K catalogue + 2 CR1858 printed), "
      f"{len(unique_sentences)} V219 sentence bridges, publication HOLD, 16c collation 0")
