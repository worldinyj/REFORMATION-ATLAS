#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
m=json.loads((r/"data/contracts/atlas_v162_edition_article_matrix.json").read_text(encoding="utf8"))
p=json.loads((r/"data/contracts/atlas_v161_edition_comparison_cards.json").read_text(encoding="utf8"))
assert m["publication_gate"]=={"approved":False,"can_ship":False}
ids={e["id"] for w in p["works"] for e in w["editions"]}
assert len(m["rows"])==6 and len({v["id"] for v in m["rows"]})==6
assert all(set(v["references"])<=ids for v in m["rows"])
assert all(not v["collated"] and len(v["source_urls"])>=1 for v in m["rows"])
assert all(v["difference"] and v["evidence"] for v in m["rows"])
assert (r/"docs/01_CONTENT/V162_EDITION_ARTICLE_MATRIX.md").exists()
print("PASS V1.62: six source-labelled matrix rows, refs and release gates")
