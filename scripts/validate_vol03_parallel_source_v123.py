#!/usr/bin/env python3
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"data/deep/vol03_parallel_source_audit_v123.json"
d=json.loads(p.read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
assert len(d["comparisons"])==2 and len(d["hus"])==3
assert all(x["manuscript_collated"] is False for x in d["comparisons"])
assert all(x["latin_full_passage_collated"] is False for x in d["hus"])
assert {x["passage"] for x in d["comparisons"]}=={"Lamentations 2:19","Exodus 7:25"}
assert next(x for x in d["hus"] if x["id"]=="HUS-V123-RELATIO-286")["print_page"]==286
print("PASS V1.23: source-level claims and closed publication gates")
