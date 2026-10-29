#!/usr/bin/env python3
"""V1.14 fail-closed data validation."""
import json
from pathlib import Path
d=json.loads((Path(__file__).resolve().parents[1]/"data/deep/vol05_education_map_timeline_v114.json").read_text(encoding="utf-8"))
assert d["status"]=="DRAFT_RESEARCH_NOT_PUBLIC"
assert d["publication_gate"]=={"approved":False,"can_ship":False}
places={p["id"] for p in d["locations"]}
sources={s["id"] for s in d["sources"]}
events={e["id"]:e for e in d["events"]}
assert len(places)==len(d["locations"]) and len(sources)==len(d["sources"]) and len(events)==len(d["events"])
for p in d["locations"]:
    assert p["coordinate_precision"]=="modern_city_centroid_approximation" and p["historical_site_verified"] is False
for e in events.values():
    assert e["to"] in places and (e["from"] is None or e["from"] in places)
    assert e["sources"] and set(e["sources"])<=sources
    assert e["historical_site_verified"] is False
assert events["EV-ESS-1652"]["person_count"]==3
assert events["EV-PAD-PERMIT-1652"]["type"]=="authorization"
assert events["EV-PAD-PERMIT-1652"]["date"]=="1652-10-21"
assert events["EV-PAD-PERMIT-1652"]["from"] is None
assert events["EV-PAD-ARRIVAL-1658"]["date"]=="1658-03-28"
assert events["EV-PAD-ARRIVAL-1658"]["person_count"]==2
for r in d["routes"]:
    assert r["event_id"] in events
    assert r["from"] in places and r["to"] in places
    assert r["geometry"]=="abstract_straight_line_not_historical_travel_route"
    assert r["event_id"]!="EV-PAD-PERMIT-1652"
assert len(d["routes"])==2 and d["display_rules"]["split_permission_and_arrival"] is True
print("PASS: V1.14 timeline, source links, and draft publication gate")
