#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
x=json.loads((r/"data/deep/atlas_v136_trent_clause_comparison.json").read_text(encoding="utf8"))
assert x["publication_gate"]=={"approved":False,"can_ship":False}
assert len(x["clauses"])==4
assert len({a["id"] for a in x["clauses"]})==4
assert {a["session"] for a in x["clauses"]}=={"VI","XXV"}
assert all(not a["original_latin_print_collated"] for a in x["clauses"])
assert not x["teresa"]["variants_directly_collated"]
assert x["clauses"][-1]["date"]=="1563-12-04"
print("PASS V1.36: clauses, dates, sources and publication gate")
