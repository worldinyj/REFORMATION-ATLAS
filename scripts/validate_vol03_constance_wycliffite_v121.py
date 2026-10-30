#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d=json.loads((r/"data/deep/vol03_constance_wycliffite_comparison_v121.json").read_text(encoding="utf-8"))
assert d["publication_gate"]=={"approved":False,"can_ship":False}
w={x["id"]:x for x in d["witnesses"]}
assert len(w)==len(d["witnesses"])==6
for item in w.values():
 assert item["url"].startswith("https://") and item["manuscript_text_collated"] is False
for pair in d["paired_comparisons"]:
 assert len(pair["ids"])==2 and set(pair["ids"])<=w.keys()
assert w["WIT-V121-WYC-EV-EGERTON"]["version"]=="Earlier Version"
assert w["WIT-V121-WYC-LV-ROYAL"]["version"]=="Later Version"
print("PASS V1.21 catalog links / distinct witnesses / release gate")
