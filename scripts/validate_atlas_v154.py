#!/usr/bin/env python3
"""Validate 60 research microchapters, their sources, ID uniqueness and release gate."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/"data/deep"
outline=json.loads((root/"data/contracts/atlas_v154_60_module_outline.json").read_text(encoding="utf-8"))
all_modules=[]
for letter in "abcdef":
    doc=json.loads((p/f"atlas_v154_group_{letter}.json").read_text(encoding="utf-8"))
    assert doc["publication_gate"]["can_ship"] is False
    assert len(doc["modules"])==10
    all_modules+=doc["modules"]
assert len(all_modules)==60
assert len({x["id"] for x in all_modules})==60
assert sum(len(g["topics"]) for g in outline["groups"])==60
assert all(x["reader_text"] and len(x["reader_text"])>=45 for x in all_modules)
assert all(x["source_urls"] and all(s.startswith("https://") for s in x["source_urls"]) for x in all_modules)
assert all(x["verified_primary"] is False for x in all_modules)
assert len({x["title"] for x in all_modules})==60
print("PASS V1.54: 60 unique contextualized modules, 60 questions, provenance links, six release holds")
