#!/usr/bin/env python3
"""V213 historical city/site vs current witness holding and references validation."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rd(p):return json.loads((R/p).read_text(encoding="utf-8"))
a=rd("data/deep/atlas_v213_historical_gazetteer.json")
b=rd("data/deep/atlas_v212_historical_connections_and_comparisons.json")
geo=rd("data/maps/atlas_v213_research_geography.geojson")
assert a["version"]=="2.13" and a["parent_commit"]=="71499b63595f5ac1fd93190682bdc3f14933cd44"
assert all(v is False for v in a["publication_gate"].values())
m=a["metrics"]
assert [m[k] for k in ("chronology_events","historical_locations","map_preview_features","historic_site_reported_gps","city_context_estimates","persons","documents","holdings_separate_from_event_map","reader_geography_views","supplementary_sources")]==[19,12,12,1,11,10,14,7,10,20]
assert m["original_folios_collated"]==m["expert_approvals"]==m["public_approved"]==0
sources={s["id"] for s in a["supplementary_sources"]}|{s["id"] for s in b["source_register"]}
assert len(sources)==34
assert all(s["url"].startswith("https://") and s["exact_historical_folio_or_print_image_inspected"] is False for s in a["supplementary_sources"])
places={p["id"]:p for p in a["historical_places"]}
people={p["id"]:p for p in a["historical_persons"]}
docs={p["id"]:p for p in a["historical_document_objects"]}
assert len(places)==12 and len(people)==10 and len(docs)==14
assert all(set(p["source_ids"])<=sources and p["source_ids"] and p["can_publish"] is False for p in places.values())
assert sum(p["geographic_precision"]=="REPORTED_HISTORIC_SITE" for p in places.values())==1
for p in places.values():
  assert -90<=p["latitude"]<=90 and -180<=p["longitude"]<=180
  assert p["exact_16c_building_position_certified"] is False and p["modern_reference_not_historic_venue"] is True
for d in docs.values():
  assert d["source_ids"] and set(d["source_ids"])<=sources and d["can_publish"] is False
old={x["id"]:x for x in b["chronology"]}
mapped={x["source_chronology_id"]:x for x in a["event_links"]}
assert len(old)==len(mapped)==19 and set(old)==set(mapped)
for k,e in mapped.items():
  o=old[k]
  assert (e["date_start"],e["date_end"],e["date_precision"],e["reader_key"],e["event_ko"])==(o["start_date"],o["end_date"],o["date_precision"],o["reader_key"],o["event_ko"])
  assert e["historical_place_id"] in places
  assert e["historic_site_geo_precision"] in ("CITY_ONLY","REPORTED_SITE")
  assert set(e["person_ids"])<=set(people) and set(e["document_ids"])<=set(docs)
  assert set(e["source_ids"])<=sources and set(o["source_ids"])<=set(e["source_ids"])
  assert e["exact_site_or_print_shop_geocode_confirmed"] is False
  assert e["primary_historical_folio_checked"] is False and e["expert_approved"] is False and e["can_publish"] is False
assert sum(e["historic_site_geo_precision"]=="REPORTED_SITE" for e in mapped.values())==1
assert len(a["current_holding_records"])==7
for h in a["current_holding_records"]:
  assert h["latitude"] is None and h["longitude"] is None and h["map_event_pin_allowed"] is False
  assert h["historic_original_folio_collated"] is False and h["can_publish"] is False
assert {r["reader_key"] for r in a["reader_place_links"]}=={r["reader_key"] for r in b["reader_connections"]}
assert all(set(r["historical_place_ids"])<=set(places) and r["can_publish"] is False for r in a["reader_place_links"])
assert geo["type"]=="FeatureCollection" and len(geo["features"])==12
for f in geo["features"]:
  p=places[f["properties"]["id"]]
  assert f["geometry"]["coordinates"]==[p["longitude"],p["latitude"]]
  assert f["properties"]["can_publish"] is False
assert len(a["historical_risks"])>=8
print("PASS V213: all 19 events mapped to 12 geo contexts, 14 historical documents/10 persons, seven current holdings kept off event pins; PUBLIC HOLD")
