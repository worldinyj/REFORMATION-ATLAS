#!/usr/bin/env python3
"""V225 documentary transmission QA: 1529 manuscripts, chronology, printed editions.

Validates historical provenance constraints only; no primary image is implied read.
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((R / path).read_text(encoding="utf-8"))

v19 = load("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v20 = load("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")
v21 = load("data/deep/atlas_v221_marburg_witness_accession.json")
v22 = load("data/deep/atlas_v222_original_image_routes_and_assertions.json")
v23 = load("data/deep/atlas_v223_marburg_critical_text_and_date_provenance.json")
v24 = load("data/deep/atlas_v224_primary_facsimile_retrieval_gate.json")
d = load("data/deep/atlas_v225_marburg_fair_copy_print_transmission.json")

assert d["version"] == "2.25"
assert d["parent_commit"] == "e811b6d29868e79a3af65a01999ca3909997bf21"
assert d["base_dataset"] == "data/deep/atlas_v224_primary_facsimile_retrieval_gate.json"
assert all(value is False for value in d["publication_gate"].values())
assert v19["metrics"]["chapters"] == 10
assert v19["metrics"]["sections"] == 74
assert v19["metrics"]["paragraphs"] == 128
assert v19["metrics"]["sentences"] == len(v19["sentences"]) == 543
assert v19["metrics"]["full_integrated_codepoints"] == 35102
assert v20["metrics"]["comparison_units"] == 5
assert v20["metrics"]["direct_16c_witness_collations"] == 0
assert v21["metrics"]["original_exemplar_pages_read"] == 0
assert v22["metrics"]["original_pages_visually_read"] == 0
assert v23["metrics"]["successful_original_image_page_reads"] == 0
assert v24["metrics"]["direct_original_pages_read"] == 0

def unique_dict(seq):
    keyed = {x["id"]: x for x in seq}
    assert len(keyed) == len(seq)
    return keyed

sources = unique_dict(d["sources"])
objects = unique_dict(d["objects"])
relations = unique_dict(d["relations"])
claims = unique_dict(d["claims"])
sections = unique_dict(d["reader_sections"])
questions = unique_dict(d["open_questions"])
assert (len(sources), len(objects), len(relations), len(claims),
        len(sections), len(questions)) == (9, 10, 10, 7, 3, 7)
assert all(x["url"].startswith("https://") and x["original_image_inspected"] is False for x in sources.values())
assert {x["type"] for x in objects.values()} >= {
    "SIGNED_SURVIVING_MANUSCRIPT", "REPORTED_FAIR_COPIES_COUNT",
    "ZURICH_CONTEMPORARY_PRINT", "MARBURG_CONTEMPORARY_PRINTING"}
assert objects["OBJ-V225-COPIES-THREE"]["reported_made"] == 3
assert objects["OBJ-V225-COPIES-THREE"]["reported_extant"] == 2
assert objects["OBJ-V225-UNKNOWN-COPY"]["known_provenance"] is None
assert objects["OBJ-V225-Z"]["additions_reported_articles"] == ["7","13","15"]
assert objects["OBJ-V225-K"]["manuscript_image_inspected"] is False
assert objects["OBJ-V225-Z"]["manuscript_image_inspected"] is False
assert objects["OBJ-V225-W2119"]["vd16"] == "W 2119"
assert objects["OBJ-V225-W2119"]["vlid"] == "170052"
assert objects["OBJ-V225-ZH2"]["vd16"] is None
assert objects["OBJ-V225-ZH2"]["mapping_status"] == "UNVERIFIED_W2118"
assert objects["OBJ-V225-RHODE"]["date_assertion"] == "INFERRED_FROM_DIGIREF_NEXT_DAY_AFTER_OCT4_AND_NOT_IMPRINT_READ"
assert objects["OBJ-V225-PRINT-CHAIN"]["count_directly_verified"] is False

for e in relations.values():
    assert e["from"] in objects and e["to"] in objects
    assert set(e["source_ids"]) <= sources.keys() and e["source_ids"]
    assert e["certainty"] not in ("PRIMARY_MANUSCRIPT_READ","DIRECT_16C_PRINT_READ")
for c in claims.values():
    assert c["source_ids"] and set(c["source_ids"]) <= sources.keys()
    assert c["certainty"] not in ("PRIMARY_MANUSCRIPT_READ","DIRECT_16C_PRINT_READ")
assert relations["EDG-V225-10"]["relationship"] == "MANUSCRIPT_WITNESS_COMPARISON_CATALOGUE_ADDITIONS"
assert "NOT_PROVEN_DIRECTLY_COPIED_FROM_Z" in relations["EDG-V225-6"]["relationship"]
for section in sections.values():
    assert section["linked_claim_ids"] and set(section["linked_claim_ids"]) <= claims.keys()
assert {i for s in sections.values() for i in s["linked_claim_ids"]} == claims.keys()
assert all(q["status"] == "OPEN" and q["question"] for q in questions.values())
assert all(d["methodology"][k] is True for k in (
    "no_direct_manuscript_scan_claim",
    "manuscript_z_to_print_w2119_copy_relationship_not_demonstrated"))
assert d["access_summary"]["new_original_files_downloaded"] == 0
assert d["access_summary"]["new_original_pages_read"] == 0
assert d["access_summary"]["original_manuscript_wordings_transcribed"] == 0
assert d["metrics"] == {
    "source_records":9, "transmission_objects":10, "source_linked_relations":10,
    "critical_claims":7, "reader_sections":3, "open_questions":7,
    "original_page_reads":0, "zk_wordings_collated":0, "publication_items":0}
print("PASS V225: 10 documentary objects, 10 source-linked transmission relations, 7 critical claims")
print("PASS V225: Oct 3/4 split, copy hierarchy, divergent signature order, print-chain status, HOLD")
