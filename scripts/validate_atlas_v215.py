#!/usr/bin/env python3
"""V215 check pedagogical journeys against 10 readers, dated events, holding identities and source gates.
This verifies data linking, NOT factual truth, expert signoff or historical map precision.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rd(p):return json.loads((R/p).read_text(encoding="utf-8"))
x=rd("data/deep/atlas_v215_historical_exploration_journeys.json")
v11=rd("data/deep/atlas_v211_ten_reader_hus_augsburg_revision.json")
v12=rd("data/deep/atlas_v212_historical_connections_and_comparisons.json")
v14=rd("data/deep/atlas_v214_geography_and_witness_provenance.json")
assert x["version"]=="2.15" and x["lineage"]["base_commit"]=="b38706599e19ccc70b7e2c9eed580f8ce61bee1e"
assert all(v is False for v in x["publication_gate"].values())
m=x["metrics"]
assert (m["route_count"],m["reader_steps"],m["directed_reading_transitions"],m["unique_v214_events_covered"],m["unique_v211_readers_covered"],m["unique_held_witnesses_covered"])==(5,30,25,19,10,3)
assert m["total_v214_events"]==len(v14["event_links"])==19
assert m["total_v211_readers"]==len(v11["chapters"])==10
assert m["source_review_crosschecks"]==len(x["editorial_source_crosschecks"])==2
assert m["verified_original_manuscript_folios"]==m["expert_approvals"]==m["public_map_pins_authorized"]==m["webapp_published"]==0
readers={r["key"]:r for r in v11["chapters"]}
sentences={s["id"]:s for s in v11["sentences"]}
context={r["id"]:r for r in v12["reader_connections"]}
themes={r["id"]:r for r in v12["comparisons"]}
events={e["id"]:e for e in v14["event_links"]}
holdings={h["id"]:h for h in v14["witness_holdings_without_event_pins"]}
places={p["id"]:p for p in v14["places"]}
people={p["id"] for p in v14["persons"]}
docs={d["id"] for d in v14["document_objects"]}
sources={s["id"] for s in v12["source_register"]}|{s["id"] for s in v14["source_registry"]}
journeys={j["id"]:j for j in x["journeys"]}
stages={s["id"]:s for s in x["stages"]}
assert len(journeys)==5 and len(stages)==30
all_stages=[]
for j in journeys.values():
    assert j["guiding_question_ko"] and len(j["teaser_ko"])>40
    assert j["related_theme_id"] in themes
    assert len(j["stage_ids"])==6
    assert j["historical_route_not_navigation"] and j["geographical_travel_times_not_applicable"]
    assert j["academic_signoff"] is False and j["can_publish"] is False
    assert len(j["stage_ids"])==len(set(j["stage_ids"]))
    all_stages+=j["stage_ids"]
assert len(all_stages)==len(set(all_stages))==30 and set(all_stages)==set(stages)
old_event_coverage=set()
held=set()
reader_coverage=set()
for s in stages.values():
    assert s["journey_id"] in journeys and s["scene_type"] in ("EVENT","HOLDING","COMPARISON")
    assert journeys[s["journey_id"]]["stage_ids"][s["sequence"]-1]==s["id"]
    assert len(s["narrative_ko"])>=115 and s["title_ko"] and s["evidence_note_ko"]
    assert s["reading_reader_key"] in readers
    reader_coverage.add(s["reading_reader_key"])
    sent=sentences[s["v211_reader_sentence_id"]]
    assert sent["reader_key"]==s["reading_reader_key"]
    assert readers[s["reading_reader_key"]]["body"][sent["start_char"]:sent["end_char"]].startswith(s["v211_excerpt"])
    assert context[s["v212_context_essay_id"]]["reader_key"]==s["reading_reader_key"]
    assert s["source_ids"] and set(s["source_ids"])<=sources
    assert s["map_pin_allowed"] is False and s["original_witness_folio_verified"] is False
    assert s["historical_causality_inferred"] is False and s["semantic_link_human_approved"] is False and s["can_publish"] is False
    if s["scene_type"]=="EVENT":
        e=events[s["v214_event_id"]]
        old_event_coverage.add(e["id"])
        assert e["reader_key"]==s["reading_reader_key"]
        assert s["v214_historical_place_id"]==e["historical_place_id"] in places
        assert s["v214_person_ids"]==e["person_ids"]
        assert s["v214_document_ids"]==e["document_ids"]
        assert set(e["source_ids"])<=set(s["source_ids"])
        assert s["research_preview_place_marker"] is True
        assert s["place_precision"]==places[e["historical_place_id"]]["coordinate_precision"]
        assert s["v214_holding_id"] is None
    elif s["scene_type"]=="HOLDING":
        assert s["v214_event_id"] is None and s["v214_historical_place_id"] is None
        assert s["v214_holding_id"] in holdings
        held.add(s["v214_holding_id"])
        assert s["research_preview_place_marker"] is False
        assert holdings[s["v214_holding_id"]]["has_event_map_pin"] is False
    else:
        assert s["v214_event_id"] is None and s["v214_historical_place_id"] is None and s["v214_holding_id"] is None
        assert s["research_preview_place_marker"] is False
assert len(old_event_coverage)==len(events)==19
assert len(held)==3 and len(reader_coverage)==10
transition={t["id"]:t for t in x["transitions"]}
assert len(transition)==25
for j in journeys.values():
    edges=[t for t in transition.values() if t["from_stage_id"] in j["stage_ids"]]
    assert len(edges)==5
    assert {(t["from_stage_id"],t["to_stage_id"]) for t in edges}==set(zip(j["stage_ids"],j["stage_ids"][1:]))
for t in transition.values():
    assert t["relation_kind"] and t["narrative_ko"] and t["historical_direct_causation_not_claimed"] is True and t["can_publish"] is False
for s in x["editorial_source_crosschecks"]:
    assert s["url"].startswith("https://") and s["historical_original_folio_inspected"] is False
assert len(x["release_checklist"])==5
assert all(g["status"]=="BLOCKED" for g in x["release_checklist"])
assert len(x["unresolved"])>=7
print("PASS V215: 5 journeys, 30 substantive stages, 25 links, all 19 events + 10 readers, 3 non-map holdings, research-only gates CLOSED")
