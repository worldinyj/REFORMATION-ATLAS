#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/"data/contracts/atlas_v161_edition_comparison_cards.json").read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
works=d["works"]
assert len(works)==2
assert len(works[0]["editions"])==3 and len(works[1]["editions"])==2
assert [x["year"] for x in works[0]["editions"]]==[1530,1531,1540]
assert [x["year"] for x in works[1]["editions"]]==[1536,1559]
assert works[1]["editions"][0]["chapter_count"]==6
assert works[1]["editions"][1]["book_count"]==4
assert works[1]["editions"][1]["chapter_count"]==80
assert len({e["id"] for w in works for e in w["editions"]})==5
assert not d["verification"]["direct_primary_text_collation"]
assert not d["verification"]["rights_for_facsimile_images"]
print("PASS V1.61: 5 edition cards and publication safeguards")
