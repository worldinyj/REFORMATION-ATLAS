#!/usr/bin/env python3
"""Research-only V205 sentence segmentation & limited evidence dossier QA.
Historical truth, source authenticity, rights and editorial approval are NOT guaranteed.
"""
import json
import re
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
d=load("data/deep/atlas_v205_sentence_evidence_dossiers.json")
old=load("data/deep/atlas_v204_paragraph_review_units.json")
src=load("data/deep/atlas_v202_unified_ten_revised_readers.json")
assert d["version"]=="2.05" and d["origin"]["reader_version"]=="2.02"
assert d["origin"]["parent_commit"]=="28b64aca7ae19b18e1d36a7c3e8b087b9bca8580"
assert all(v is False for v in d["publication_gate"].values())
m=d["metrics"]
assert m["reader_count"]==10 and m["v204_passage_units"]==124
assert m["v204_focus_tasks"]==30
assert m["limited_scope_dossiers"]==len(d["evidence_dossiers"])==7
assert m["not_externally_rechecked_focus_tasks"]==len(d["remaining_focus_queue"])==23
assert m["distinct_reviewed_source_leads"]==len(d["source_register"])==7
assert m["original_witnesses_collated"]==m["passages_certified_for_publication"]==0
assert m["v205_sentence_candidates"]==len(d["sentence_candidates"])>=200
chap={x["key"]:x for x in src["chapters"]}
pars={x["id"]:x for x in old["passages"]}
tasks={x["id"]:x for x in old["focus_tasks"]}
assert len(chap)==10 and len(pars)==124 and len(tasks)==30
segs={}
counts=Counter()
for s in d["sentence_candidates"]:
    p=pars[s["passage_id"]]
    key=s["reader_key"]
    assert p["reader_key"]==key and s["section_id"]==p["section_id"]
    counts[key]+=1
    assert s["id"]==f"SNT-V205-{key}-{counts[key]:04d}"
    assert s["id"] not in segs
    assert p["start_char"]<=s["start_char"]<s["end_char"]<=p["end_char"]
    body=chap[key]["body"]
    t=body[s["start_char"]:s["end_char"]]
    assert t and s["excerpt"]==t[:100] and s["codepoint_count"]==len(t)
    assert s["manual_claim_type"]=="UNCLASSIFIED"
    assert s["unit_kind"]=="SENTENCE_CANDIDATE_NOT_ATOMIC_HISTORICAL_CLAIM"
    assert s["historical_truth_verified"] is False
    assert s["source_passage_checked"] is False and s["can_publish"] is False
    segs[s["id"]]=s
for p in old["passages"]:
    sent=sorted((x for x in d["sentence_candidates"] if x["passage_id"]==p["id"]),key=lambda x:x["start_char"])
    assert sent
    # Coverage: whitespace gaps only and each punctuation boundary must be preserved.
    text=chap[p["reader_key"]]["body"]
    cursor=p["start_char"]
    for s in sent:
        assert not text[cursor:s["start_char"]].strip()
        cursor=s["end_char"]
    assert not text[cursor:p["end_char"]].strip()
for c in d["per_reader"]:
    assert c["sentence_candidates"]==counts[c["key"]]
    assert c["v204_passages"]==sum(p["reader_key"]==c["key"] for p in pars.values())
assert set(counts)==set(chap)
sources={x["id"]:x for x in d["source_register"]}
assert len(sources)==7
for x in sources.values():
    assert x["url"].startswith("https://") and x["source_class"]
    assert x["content_licence_cleared_for_republication"] is False
    assert "direct_" in " ".join(x.keys())
dossier_ids=set()
for x in d["evidence_dossiers"]:
    assert x["focus_id"] in tasks and x["focus_id"] not in dossier_ids
    dossier_ids.add(x["focus_id"])
    t=tasks[x["focus_id"]]
    assert x["reader_key"]==t["reader_key"]
    assert x["passage_id"]==t["passage_id"] and x["source_excerpt"]==t["exact_source_excerpt"]
    assert x["sources"] and all(s in sources for s in x["sources"])
    assert x["research_state"]=="LIMITED_SOURCE_SCOPE_CHECK_NOT_PUBLICATION_PROOF"
    assert x["reviewed_source_scope"] is True
    assert x["original_manuscript_collated"] is False
    assert x["full_passage_verified"] is False and x["expert_signoff"] is False
    assert x["can_publish"] is False
    if x["anchored_sentence_id"] is not None:
        s=segs[x["anchored_sentence_id"]]
        assert s["passage_id"]==t["passage_id"]
        assert s["start_char"]<=t["excerpt_start_char"]
        assert t["excerpt_end_char"]<=s["end_char"]
assert set(dossier_ids)|{x["focus_id"] for x in d["remaining_focus_queue"]}==set(tasks)
assert set(dossier_ids).isdisjoint(x["focus_id"] for x in d["remaining_focus_queue"])
assert all(x["can_publish"] is False for x in d["remaining_focus_queue"])
print(f"PASS V205: {len(chap)} readers, {len(pars)} paragraph units, {len(segs)} sentence candidates, {len(dossier_ids)} limited source dossiers, {len(d['remaining_focus_queue'])} pending; original/source/publication approval remains blocked")
