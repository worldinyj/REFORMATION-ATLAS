#!/usr/bin/env python3
"""Validate Vol03 V1.53 reader chapters, provenance and edition identity."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
deep=root/"data/deep"
d=json.loads((deep/"atlas_v153_vol03_reader_modules.json").read_text(encoding="utf-8"))
timeline=json.loads((deep/"atlas_v153_event_work_learning_path.json").read_text(encoding="utf-8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert timeline["publication_gate"]=={"approved":False,"can_ship":False}
assert len(d["modules"])>=12
assert len(d["concept_glossary"])>=6
assert len(timeline["events"])>=10
assert len({x["id"] for x in d["modules"]})==len(d["modules"])
assert all(len(m["reader_text"])>=90 and len(m["source_urls"])>=2 and m["primary_latin_collated"] is False for m in d["modules"])
assert all(all(u.startswith("https://") for u in m["source_urls"]) for m in d["modules"])
assert d["work_id_separation"]["wycliffe"]!=d["work_id_separation"]["hus"]
assert any(p["kind"]=="INFLUENCE_NOT_IDENTICAL_WORK" for p in timeline["paths"])
assert (root/"docs/01_CONTENT/VOL03/V153_WYCLIFFE_HUS_12_READER_CHAPTERS.md").exists()
print("PASS V1.53: 12 modules, sources, distinct works, glossary, timeline, publication hold")
