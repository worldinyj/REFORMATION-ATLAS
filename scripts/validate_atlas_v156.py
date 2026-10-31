#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/"data/deep/atlas_v156_extended_narratives.json").read_text(encoding="utf-8"))
g=json.loads((r/"data/contracts/atlas_v156_reading_paths.json").read_text(encoding="utf-8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert g["publication_gate"]=={"approved":False,"can_ship":False}
assert len(d["pages"])==len(g["nodes"])==10
ids={x["id"] for x in d["pages"]}
assert ids=={n["id"] for n in g["nodes"]}
assert len(g["edges"])==10
assert all(e["from"] in ids and e["to"] in ids for e in g["edges"])
assert all(not e["verified_as_direct_citation"] for e in g["edges"])
assert all(len(p["segments"])==5 and len(p["source_urls"])>=2 and p["primary_collated"] is False for p in d["pages"])
assert (r/"docs/01_CONTENT/V156_TEN_EXTENDED_NARRATIVES.md").exists()
print("PASS V1.56: 10 narratives, 50 segments, 10 guarded navigation edges")
