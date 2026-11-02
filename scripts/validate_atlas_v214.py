#!/usr/bin/env python3
"""V214 geography and holdings QA: no precision, primary-scan or scholarly certification."""
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def rd(p): return json.loads((R/p).read_text(encoding="utf-8"))
v=rd("data/deep/atlas_v214_geography_and_witness_provenance.json")
old=rd("data/deep/atlas_v212_historical_connections_and_comparisons.json")
geo=rd("data/maps/atlas_v214_private_historical_geography.geojson")
assert v["version"]=="2.14" and v["parent_commit"]=="71499b63595f5ac1fd93190682bdc3f14933cd44"
assert all(flag is False for flag in v["publication_gate"].values())
m=v["metrics"]
assert (m["source_events"],m["event_location_links"],m["unique_places"],m["geojson_features"])==(19,19,11,11)
assert (m["historic_site_reported_coordinates"],m["modern_approximate_city_centres"])==(1,10)
assert (m["history_persons"],m["historical_document_objects"],m["modern_witness_holdings"])==(10,14,6)
assert (m["new_source_records"],m["site_essays"],m["inspected_original_language_critical_transcription_records"])==(15,11,1)
assert m["source_original_folio_images_collated"]==m["public_geocodes_verified"]==m["human_scholar_approvals"]==m["public_items"]==0
src={s["id"] for s in old["source_register"]}|{s["id"] for s in v["source_registry"]}
assert len(src)==len(old["source_register"])+15
assert all(s["url"].startswith("https://") and s["original_image_inspected"] is False and s["rights_cleared"] is False for s in v["source_registry"])
places={p["id"]:p for p in v["places"]};persons={p["id"]:p for p in v["persons"]};docs={d["id"]:d for d in v["document_objects"]}
assert (len(places),len(persons),len(docs))==(11,10,14)
for p in places.values():
    assert -90<=p["lat"]<=90 and -180<=p["lon"]<=180
    assert len(p["place_essay_ko"])>=100
    assert p["source_ids"] and set(p["source_ids"])<=src
    assert p["historian_approved"] is False and p["can_publish"] is False
    assert p["site_building_or_room_verified"] is (p["id"]=="PLACE-V214-KOZI")
    assert p["coordinate_precision"] in ("HISTORIC_SITE_COORD_FROM_HERITAGE_WEBSITE","MODERN_CITY_CENTROID_APPROXIMATE")
assert geo["type"]=="FeatureCollection" and len(geo["features"])==11
assert {p["properties"]["place_id"] for p in geo["features"]}==set(places)
for f in geo["features"]:
    p=places[f["properties"]["place_id"]]
    assert f["geometry"]["coordinates"]==[p["lon"],p["lat"]] and f["properties"]["can_publish"] is False
old_e={e["id"]:e for e in old["chronology"]}
ev={e["v212_event_id"]:e for e in v["event_links"]}
assert len(ev)==19 and set(ev)==set(old_e)
for k,e in ev.items():
    parent=old_e[k]
    assert (e["history_date_start"],e["history_date_end"],e["date_precision"],e["reader_key"])==(parent["start_date"],parent["end_date"],parent["date_precision"],parent["reader_key"])
    assert e["historical_place_id"] in places
    assert parent["source_ids"] and set(parent["source_ids"])<=set(e["source_ids"])<=src
    assert set(e["person_ids"])<=set(persons) and set(e["document_ids"])<=set(docs)
    assert e["exact_historic_event_spot_verified"] is False and e["expert_approved"] is False and e["can_publish"] is False
    assert e["document_current_holding_is_not_event_location"] is True
assert sum(e["map_reference_precision"]=="REPORTED_HISTORIC_SITE_COORDINATE" for e in ev.values())==1
assert len(v["witness_holdings_without_event_pins"])==6
for h in v["witness_holdings_without_event_pins"]:
    assert h["catalogue_url"].startswith("https://") and h["coordinates"] is None
    assert h["has_event_map_pin"] is False and h["historic_original_scan_checked"] is False and h["can_publish"] is False
assert sum(r["original_language_critical_transcription_read"] is True for r in v["source_reading_progress"])==1
assert len(v["pending_historical_geometry"])==6
print("PASS V214: 19 dated events, 11 place cards and preview reference pins, 10 persons, 14 documents, 6 separate modern holdings; no public map/geographic precision claim")
