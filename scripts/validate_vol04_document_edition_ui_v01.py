#!/usr/bin/env python3
"""Fail closed for VOL-04 document detail UI design contract."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((root/p).read_text(encoding="utf-8"))
c=load("data/contracts/vol04_document_edition_ui_v01.json")
r=load("data/deep/vol04_edition_comparison_v01.json")
assert c["status"]=="DESIGN_ONLY" and c["public_projection_generated"] is False
assert c["compatibility"]["stable_work_ids"]==["OV-D-011","OV-D-012"]
assert c["compatibility"]["route_template"]=="/documents/:documentId"
assert c["source_data"]["never_import_directly"] and c["publication_gate"]["default_deny"]
assert c["publication_gate"]["build_time_filter"] and c["publication_gate"]["missing_field_is_false"]
assert c["publication_gate"]["no_css_only_hiding"] and c["publication_gate"]["no_client_side_import_of_research_json"]
assert len(c["publication_gate"]["required"])==7
assert set(c["view"]["comparison_tabs"])=={"structure","textual_wording","iconography"}
assert {e["research_case_id"] for e in c["research_examples"]}=={x["case_id"] for x in r["comparison_cases"]}
assert all(not e["public_visible"] for e in c["research_examples"])
assert r["publication_approved"] is False and r["source_text_collated"] is False
print("PASS: edition comparison screen contract (DESIGN ONLY, public release blocked)")
