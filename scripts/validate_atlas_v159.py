#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/"data/contracts/atlas_v159_portrait_item_provenance.json").read_text(encoding="utf8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
p=d["portrait_candidates"]
assert len(p)==5 and len({v["subject"] for v in p})==5
assert all(v["file_page"].startswith("https://commons.wikimedia.org/wiki/File:") for v in p)
assert all(not v["approved_to_publish"] and not v["downloaded"] for v in p)
assert all(v["artist"] and v["creation"] and v["contemporaneity"] for v in p)
assert p[0]["contemporaneity"]=="POSTHUMOUS" and p[1]["contemporaneity"]=="POSTHUMOUS"
print("PASS V1.59 five item pages, period labels and publication holds")
