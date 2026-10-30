#!/usr/bin/env python3
import json
from pathlib import Path
d=json.loads((Path(__file__).resolve().parents[1]/"data/deep/atlas_v137_confessional_parallels.json").read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
ids={s["id"] for s in d["sources"]}
assert len(ids)==6 and len(d["comparisons"])==3
assert all(set(x["source_ids"])<=ids for x in d["comparisons"])
assert {x["id"] for x in d["comparisons"]}=={"JUSTIFICATION","EUCHARIST","SAINTS_IMAGES"}
assert all(x.get("latin_1564_collated",False) is False for x in d["sources"])
print("PASS V1.37: six source records, three distinct thematic axes, closed publication")
