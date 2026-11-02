#!/usr/bin/env python3
"""V213 route integrity: 4 self-contained deep-reading paths anchored in V211 only.
Structural validation must NEVER be construed as a primary source/academic approval.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rd(f):return json.loads((ROOT/f).read_text(encoding="utf-8"))
v=rd("data/deep/atlas_v213_thematic_deep_reading_paths.json")
v11=rd("data/deep/atlas_v211_ten_reader_hus_augsburg_revision.json")
v12=rd("data/deep/atlas_v212_cross_reader_links_and_timeline.json")
assert v["version"]=="2.13" and v["lineage"]["parent_commit"]=="095230bee9eeffc854ff5cd47814e9308f1c4cd2"
assert all(state is False for state in v["publication_gate"].values())
met=v["metrics"]
assert (met["themes"],met["reader_chapters"],met["route_stops"],met["transitions"],met["integrative_case_studies"])==(4,10,19,15,4)
assert (met["verified_original_folios"],met["historian_approvals"],met["public_published"])==(0,0,0)
chapter={c["key"]:c for c in v11["chapters"]}
secs={s["id"]:(r["reader_key"],s) for r in v11["sections"] for s in r["sections"]}
pars={p["id"]:p for p in v11["paragraphs"]}
sents={s["id"]:s for s in v11["sentences"]}
oldRel={r["id"]:r for r in v12["typed_links"]}
src={s["id"]:s for s in v["source_register"]}
assert len(src)==met["referenced_sources"] and len(chapter)==10
assert all(s["url"].startswith("https://") and s["verified_to_exact_excerpts"] is False and s["historic_original_witness_collated"] is False and s["media_reuse_cleared"] is False for s in src.values())
path={p["id"]:p for p in v["thematic_paths"]}
stops={s["id"]:s for s in v["reader_stop_cards"]}
assert len(path)==4 and len(stops)==19
coverage=set()
for key,p in path.items():
    assert p["route_approval"]=="RESEARCH_DRAFT_REQUIRES_EXPERT_QA" and p["can_publish"] is False
    assert p["stop_ids"] and len(p["stop_ids"])==len(set(p["stop_ids"]))
    assert len(p["introduction_ko"])>=150 and len(p["integrative_conclusion_ko"])>=150
    assert all(i in stops for i in p["stop_ids"])
    assert p["reader_keys"]==list(dict.fromkeys(stops[i]["reader_key"] for i in p["stop_ids"]))
    for n,i in enumerate(p["stop_ids"],1):
        s=stops[i]
        assert s["position"]==n and s["id"] not in coverage
        coverage.add(s["id"])
assert coverage==set(stops)
for s in stops.values():
    key=s["reader_key"]
    assert key in chapter and s["section_id"] in secs
    assert secs[s["section_id"]][0]==key
    p=pars[s["paragraph_id"]]
    sent=sents[s["sentence_id"]]
    assert p["reader_key"]==key and p["section_id"]==s["section_id"]
    assert sent["reader_key"]==key and sent["passage_id"]==p["id"] and sent["section_id"]==s["section_id"]
    assert p["start_char"]<=s["anchor_start_char"]==sent["start_char"]<s["anchor_end_char"]==sent["end_char"]<=p["end_char"]
    assert chapter[key]["body"][sent["start_char"]:sent["end_char"]]==s["anchor_text_exact"]
    assert len(s["original_explanation_ko"])>=130 and len(s["overclaim_guard_ko"])>=25
    assert s["guiding_question_ko"] and s["source_lead_ids"] and set(s["source_lead_ids"])<=set(src)
    assert s["historical_original_witness_verified"] is False and s["expert_approved"] is False and s["can_publish"] is False
assert len(v["route_transitions"])==15
transids=set()
for t in v["route_transitions"]:
    assert t["id"] not in transids;transids.add(t["id"])
    assert t["path_id"] in path
    route=path[t["path_id"]]["stop_ids"]
    assert (t["from_stop_id"],t["to_stop_id"]) in list(zip(route,route[1:]))
    a=stops[t["from_stop_id"]]["reader_key"]
    b=stops[t["to_stop_id"]]["reader_key"]
    if t["relationship_id"] is not None:
        o=oldRel[t["relationship_id"]]
        assert {a,b}=={o["from"],o["to"]}
        assert t["edge_scope"]=="TYPED_PREEXISTING_RELATION"
    else:
        assert t["edge_scope"]=="PARALLEL_EDITORIAL_COMPARISON_NO_DIRECT_RECEPTION_ASSERTED"
    assert t["expert_approved"] is False and t["can_publish"] is False
assert len(v["interpretive_case_studies"])==4
assert {c["path_id"] for c in v["interpretive_case_studies"]}==set(path)
for c in v["interpretive_case_studies"]:
    assert len(c["recommended_analytical_answer_ko"])>=150 and c["expert_approved"] is False and c["can_publish"] is False
assert len(v["chapter_coverage"])==10
assert {x["reader_key"] for x in v["chapter_coverage"]}==set(chapter)
for x in v["chapter_coverage"]:
    assert x["used_as_stops"]==sum(s["reader_key"]==x["reader_key"] for s in stops.values())
assert len(v["blockers"])>=6
print("PASS V213: 4 reader pathways / 19 exact sentence anchors / 15 typed-or-noncausal transitions / 4 case studies. Publish gate HOLD.")
