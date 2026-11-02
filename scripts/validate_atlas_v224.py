#!/usr/bin/env python3
"""Validate V224 reproducible primary-source acquisition queue (NOT textual collation)."""
import json
from pathlib import Path
import subprocess
import sys

R=Path(__file__).resolve().parents[1]
def read(p): return json.loads((R / p).read_text(encoding="utf-8"))
v19=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v20=read("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")
v21=read("data/deep/atlas_v221_marburg_witness_accession.json")
v22=read("data/deep/atlas_v222_original_image_routes_and_assertions.json")
v23=read("data/deep/atlas_v223_marburg_critical_text_and_date_provenance.json")
d=read("data/deep/atlas_v224_primary_facsimile_retrieval_gate.json")

assert d["version"]=="2.24" and d["parent_commit"]=="17b549ad755fd9d8a865f1342487736bb2af2310"
assert d["base_dataset"]=="data/deep/atlas_v223_marburg_critical_text_and_date_provenance.json"
assert all(x is False for x in d["publication_gate"].values())
assert v19["metrics"]["chapters"]==10 and v19["metrics"]["sentences"]==543
assert v19["metrics"]["full_integrated_codepoints"]==35102
assert v20["metrics"]["comparison_units"]==5 and v20["metrics"]["direct_16c_witness_collations"]==0
assert v21["metrics"]["original_exemplar_pages_read"]==0
assert v22["metrics"]["original_pages_visually_read"]==0
assert v23["metrics"]["successful_original_image_page_reads"]==0
assert all(v is True for v in d["policy"].values())

sources={x["id"]:x for x in d["source_evidence"]}
targets={x["id"]:x for x in d["acquisition_targets"]}
gates={x["id"]:x for x in d["image_readiness"]}
variants={x["id"]:x for x in d["original_variant_queue"]}
assert len(sources)==len(d["source_evidence"])==9
assert len(targets)==len(d["acquisition_targets"])==4
assert len(gates)==len(d["image_readiness"])==3
assert len(variants)==len(d["original_variant_queue"])==3
assert set(variants)=={"VAR-V224-07","VAR-V224-13","VAR-V224-15"}
assert all(x["url"].startswith("https://") and x["original_image_seen"] is False for x in sources.values())
old_accessions={x["id"] for x in v21["accession_targets"]}
old_variants={x["id"] for x in v20["variant_units"]}
for item in targets.values():
    assert item["source_ids"] and set(item["source_ids"]) <= sources.keys()
    assert item["parent_v221_accession"] in old_accessions
    assert item["bytes_saved"]==0 and not item["verified_pdf_magic"]
    assert item["page_count"] is None and not item["page_image_visual_read"]
    assert item["transcribed_articles"] == []
    assert item["url"].startswith("https://")
for gate in gates.values():
    assert not gate["completed"] and gate["target_ids"]
    assert set(gate["target_ids"]) <= targets.keys()
    assert len(gate["needed"]) >= 4
for variant in variants.values():
    assert variant["parent_v220_variant_id"] in old_variants
    assert all(variant[key] is None for key in (
        "z_original_reading","k_original_reading","w2119_original_print_reading",
        "folio_z","folio_k","printed_page"))
    assert variant["verification_status"]=="NOT_COLLATED"
assert targets["ACQ-V224-W2119-PDF"]["url"]=="https://www.e-rara.ch/download/pdf/170052.pdf"
assert targets["ACQ-V224-W2119-IIIF"]["url"]=="https://www.e-rara.ch/i3f/v20/170052/manifest"
assert d["date_alignment"]["resolve_as_single_date"] is False
assert d["date_alignment"]["original_document_date"]=="1529-10-03"
assert d["date_alignment"]["digital_portal_event_date"]=="1529-10-04"
assert d["date_alignment"]["scholarly_regest_label"]=="3.[4.] Oktober 1529"
assert len(d["bibliographic_issues"])==4
assert all(x["status"]=="UNRESOLVED" for x in d["bibliographic_issues"])
assert d["metrics"]=={
    "source_records":9, "acquisition_targets":4, "image_readiness_gates":3,
    "variant_queue_items":3, "new_reproducible_official_pdf_pattern":1,
    "downloaded_verified_primary_files":0, "direct_original_pages_read":0,
    "actual_zk_variant_readings":0, "public_items":0
}
cmd=[sys.executable, str(R / "scripts/fetch_atlas_v224_primary_facsimile.py"), "--mode", "self-test"]
result=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=15)
assert "PASS V224" in result.stdout
print(result.stdout.strip())
print("PASS V224 source references: 9, original image targets: 4, open variants: 3; HOLD")
