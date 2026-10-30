#!/usr/bin/env python3
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"data/contracts/atlas_v139_exploration_graph.json"
d=json.loads(p.read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
ids={n["id"] for n in d["nodes"]}
assert len(ids)==len(d["nodes"])==15
assert len(d["edges"])==13
assert all(e["from"] in ids and e["to"] in ids for e in d["edges"])
assert all(e["approval"]=="RESEARCH_ONLY" for e in d["edges"])
print("PASS V1.39: 15 nodes, 13 edges, no dangling refs, publication gate closed")
