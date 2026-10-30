#!/usr/bin/env python3
import json
from pathlib import Path
d=json.loads((Path(__file__).resolve().parents[1]/"data/deep/vol03_parallel_text_comparison_v122.json").read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
ids=[x["id"] for x in d["comparisons"]]
assert len(ids)==len(set(ids))==2
ev=d["comparisons"][0]
assert ev["passage"]=="Genesis 1:3" and "Be maad" in ev["earlier"]["text"]
assert ev["medieval_manuscript_collated"] is False
hus=d["comparisons"][1]
assert hus["latin_text_collated"] is False and hus["translation_rights_reviewed"] is False
assert all(x["publication_approved"] is False for x in d["comparisons"])
print("PASS: V1.22 comparison structure and evidence/publication gates")
