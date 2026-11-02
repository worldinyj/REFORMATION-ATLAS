#!/usr/bin/env python3
"""V226 provenance QA: agreement articles != Zürich autograph gloss != Utinger copy."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def get(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
v19=get("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v20=get("data/deep/atlas_v220_marburg_augsburg_variant_collation.json")
v21=get("data/deep/atlas_v221_marburg_witness_accession.json")
v22=get("data/deep/atlas_v222_original_image_routes_and_assertions.json")
v23=get("data/deep/atlas_v223_marburg_critical_text_and_date_provenance.json")
v24=get("data/deep/atlas_v224_primary_facsimile_retrieval_gate.json")
v25=get("data/deep/atlas_v225_marburg_fair_copy_print_transmission.json")
v26=get("data/deep/atlas_v226_1529_print_annotation_provenance_audit.json")

assert v26["version"]=="2.26"
assert v26["parent_commit"]=="00c245b03703f4d14244b382f41ddc7fbf018fba"
assert v26["base_dataset"]=="data/deep/atlas_v225_marburg_fair_copy_print_transmission.json"
assert all(v is False for v in v26["publication_gate"].values())
assert all(v is True for v in v26["method"].values())
assert (v19["metrics"]["chapters"],v19["metrics"]["sections"],
        v19["metrics"]["paragraphs"],v19["metrics"]["sentences"],
        v19["metrics"]["full_integrated_codepoints"]) == (10,74,128,543,35102)
assert v20["metrics"]["comparison_units"]==5
assert v21["metrics"]["original_exemplar_pages_read"]==0
assert v22["metrics"]["original_pages_visually_read"]==0
assert v23["metrics"]["successful_original_image_page_reads"]==0
assert v24["metrics"]["direct_original_pages_read"]==0
assert v25["metrics"]["original_page_reads"]==0

def as_index(xs):
    idx={x["id"]:x for x in xs}
    assert len(idx)==len(xs)
    return idx

s=as_index(v26["sources"])
o=as_index(v26["objects"])
rel=as_index(v26["relations"])
gl=as_index(v26["glosses"])
iss=as_index(v26["open_issues"])
old={x["id"] for x in v25["objects"]}
assert (len(s),len(o),len(rel),len(gl),len(iss)) == (8,6,4,3,6)
assert all(x["url"].startswith("https://") and x["original_page_read"] is False
           for x in s.values())
assert all(x["image_read"] is False for x in o.values())
assert all(x["v225_object"] is None or x["v225_object"] in old for x in o.values())
assert o["OBJ-V226-W2119"]["shelfmark"] == "ZB Zürich 5.174,5"
assert o["OBJ-V226-ZH2"]["shelfmark"] == "ZB Zürich Zwingli MvK A81,8"
assert o["OBJ-V226-GV174"]["scribal_note"].startswith("Heinrich Utinger")
assert o["OBJ-V226-HAND"]["shelfmark"] is None
assert rel["REL-V226-ZK"]["relation"]=="SIGNED_COPY_ADDITIONS_IN_Z"
assert set(rel["REL-V226-ZK"]["article_ids"])=={"7","13","15"}
assert rel["REL-V226-NOTES"]["relation"]=="REPORTS_UTINGER_COPIED_ZWINGLI_NOTES"
assert rel["REL-V226-IDENTITY"]["relation"]=="ITEM_IDENTITY_NOT_DEMONSTRATED"
for a in rel.values():
    assert a["from"] in o and a["to"] in o
    assert a["source_ids"] and set(a["source_ids"]) <= s.keys()
    assert not a["direct_collation"]
assert set(gl)=={"GLOSS-V226-1","GLOSS-V226-2","GLOSS-V226-3"}
assert all(a["article"]=="15" and a["latin_excerpt"]
           and not a["original_handwriting_seen"]
           and not a["signed_common_article_wording"] for a in gl.values())
assert all(set(a["source_ids"]) <= s.keys() for a in gl.values())
assert all(a["status"]=="OPEN" for a in iss.values())
assert v26["primary_access"]=={
  "w2119_pdf_download_success":False, "wa1910_pdf_screenshot_success":False,
  "primary_1529_pages_read":0, "original_z_k_insertions_transcribed":0}
assert v26["metrics"]=={
 "source_records":8,"source_objects":6,"source_relations":4,
 "article15_annotation_glosses":3,"open_issues":6,
 "primary_pages_read":0,"published_items":0}
print("PASS V226: source attribution and handwriting claims guarded; 8 sources/6 objects/4 relations")
print("PASS V226: 3 Article 15 later glosses separated from signed text; primary read 0; HOLD")
