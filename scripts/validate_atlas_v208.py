#!/usr/bin/env python3
"""V208 research-only exact source alignment and draft revision checks."""
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
def read(p):return json.loads((r/p).read_text(encoding="utf-8"))
x=read("data/deep/atlas_v208_critical_passage_dossiers.json")
v2=read("data/deep/atlas_v202_unified_ten_revised_readers.json")
v4=read("data/deep/atlas_v204_paragraph_review_units.json")
v7=read("data/deep/atlas_v207_sentence_classification_and_provisional_claims.json")
assert x["version"]=="2.08" and x["base_commit"]=="9d7a99519d81513c8b20977275990bf04ada761f"
assert all(a is False for a in x["publication_gate"].values())
m=x["metrics"]
assert (m["priority_total"],m["source_checked_priority"],m["unique_draft_paragraphs"],m["source_records"])==(30,8,7,7)
assert m["original_witnesses_collated"]==m["human_approvals"]==0
src={s["id"]:s for s in x["sources"]}
assert len(src)==7
assert all(s["original_early_print_or_manuscript_image_read"] is False and s["original_text_variants_collated"] is False for s in src.values())
chap={z["key"]:z["body"] for z in v2["chapters"]}
focus={z["id"]:z for z in v4["focus_tasks"]}
claims={z["id"]:z for z in v7["provisional_focus_claims"]}
paras={z["id"]:z for z in v4["passages"]}
used=set()
for d in x["source_passage_dossiers"]:
    assert d["focus_id"] in focus and d["focus_id"] not in used
    used.add(d["focus_id"])
    f=focus[d["focus_id"]]
    assert d["v207_claim_id"] in claims and claims[d["v207_claim_id"]]["original_focus_task_id"]==d["focus_id"]
    assert (d["reader_key"],d["passage_id"],d["original_focus_text"])==(f["reader_key"],f["passage_id"],f["exact_source_excerpt"])
    assert chap[f["reader_key"]][f["excerpt_start_char"]:f["excerpt_end_char"]]==d["original_focus_text"]
    assert d["source_ids"] and all(s in src for s in d["source_ids"])
    assert d["inspected_source_locator"] and d["missing_original_witness_verification"]
    assert d["edited_digital_source_inspected"] is True
    assert d["original_manuscript_or_print_image_collated"] is False
    assert d["expert_approved"] is False and d["can_publish"] is False
assert len(used)==8
covered=set()
for p in x["reader_paragraph_drafts"]:
    old=paras[p["passage_id"]]
    assert p["reader_key"]==old["reader_key"]
    assert (p["start_char"],p["end_char"])==(old["start_char"],old["end_char"])
    assert p["original_paragraph"]==chap[p["reader_key"]][p["start_char"]:p["end_char"]]
    assert len(p["proposed_paragraph"])>=125 and p["original_paragraph"]!=p["proposed_paragraph"]
    assert p["status"]=="PROPOSED_NOT_APPLIED"
    assert p["expert_approved"] is False and p["can_publish"] is False
    assert p["linked_focus_ids"] and all(focus[k]["passage_id"]==p["passage_id"] for k in p["linked_focus_ids"])
    covered.update(p["linked_focus_ids"])
assert len(x["reader_paragraph_drafts"])==7
assert covered==used
print("PASS V208: 8 source-scoped dossiers, 7 unchanged-reader revision drafts, all release gates CLOSED")
