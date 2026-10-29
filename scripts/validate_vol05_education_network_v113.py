#!/usr/bin/env python3
"""Fail-closed validation of the V1.13 Münster education network research."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data/deep/vol05_muenster_essen_paderborn_network_v113.json"
d = json.loads(path.read_text(encoding="utf-8"))
assert d["status"] == "DRAFT_RESEARCH_NOT_PUBLIC"
assert d["publication_gate"] == {"approved": False, "can_ship": False}
inst = {x["id"] for x in d["institutions"]}
src = {x["id"] for x in d["sources"]}
assert len(inst) == len(d["institutions"])
assert len(src) == len(d["sources"])
event_ids = {e["id"] for e in d["events"]}
assert len(event_ids) == len(d["events"])
for e in d["events"]:
    assert e["from"] in inst and e["to"] in inst
    assert e["source_ids"] and set(e["source_ids"]) <= src
    assert e["primary_verified"] is False
assert next(e for e in d["events"] if e["id"]=="E-ESS-1652")["persons_count"] == 3
auth = next(e for e in d["events"] if e["id"]=="E-PAD-AUTH-1652")
arr = next(e for e in d["events"] if e["id"]=="E-PAD-ARRIVE-1658")
assert auth["type"] == "authorization_document" and auth["date"] == "1652-10-21"
assert arr["type"] == "arrival_and_teaching" and arr["date"] == "1658-03-28"
assert arr["persons_count"] == 2
assert d["constraints"]["authorization_is_not_arrival"] is True
print("PASS: V1.13 draft network integrity and release gate")
