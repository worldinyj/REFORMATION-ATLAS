#!/usr/bin/env python3
"""V210 revision-aware sentence and quote anchor QA; source authenticity remains HOLD."""
import json,re
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
x=load("data/deep/atlas_v210_reader_sentences_and_focus_anchors.json")
v9=load("data/deep/atlas_v209_unified_ten_revised_readers.json")
v7=load("data/deep/atlas_v207_sentence_classification_and_provisional_claims.json")
v8=load("data/deep/atlas_v208_critical_passage_dossiers.json")
v4=load("data/deep/atlas_v204_paragraph_review_units.json")
assert x["version"]=="2.10" and x["base_commit"]=="eb519da82c8626736070ad6fe5dab4396d4303f6"
assert all(v is False for v in x["publication_gate"].values())
m=x["metrics"]
assert (m["reader_count"],m["paragraph_count"],m["old_sentence_count"])==(10,124,521)
assert m["old_sentence_count"]==m["unchanged_sentences_rebased"]+m["old_sentences_replaced"]
assert m["current_sentence_count"]==m["unchanged_sentences_rebased"]+m["new_sentences_created"]==len(x["sentences"])
assert (m["focus_total"],m["retired_focus_reanchored"],m["unchanged_focus_rebased"])==(30,8,22)
assert m["editorial_findings"]==len(x["editorial_issues"])==12
assert m["original_witnesses_verified"]==m["expert_approvals"]==m["publication_approvals"]==0
body={c["key"]:c["body"] for c in v9["chapters"]}
para={p["id"]:p for p in v9["paragraph_spans"]}
old_sent={s["id"]:s for s in v7["sentences"]}
edits={}
for e in v8["reader_paragraph_drafts"]: edits.setdefault(e["reader_key"],[]).append(e)
for items in edits.values():items.sort(key=lambda x:x["start_char"])
def translate(key,position):
    delta=0
    for e in edits.get(key,[]):
        assert not (e["start_char"]<position<e["end_char"])
        if position>=e["end_char"]:delta+=len(e["proposed_paragraph"])-len(e["original_paragraph"])
    return position+delta
categories=[(r["category"],r["js_regex"]) for r in x["categories"]]
def classify(text):return next(k for k,p in categories if re.search(p,text))
counter=Counter()
by_para={}
by_id={}
seen_old=set()
for s in x["sentences"]:
    k=s["reader_key"]
    counter[k]+=1
    assert s["id"]==f"SNT-V210-{k}-{counter[k]:04d}"
    assert s["id"] not in by_id
    by_id[s["id"]]=s
    p=para[s["passage_id"]]
    assert (s["reader_key"],s["section_id"])==(p["reader_key"],p["section_id"])
    a,b=s["start_char"],s["end_char"]
    assert p["start_char"]<=a<b<=p["end_char"]
    text=body[k][a:b]
    assert s["excerpt"]==text[:110] and s["codepoint_count"]==len(text)
    assert s["suggested_category"]==classify(text)
    assert s["human_review"]=="PENDING" and s["is_atomic_claim"]=="UNDETERMINED"
    assert s["original_witness_collated"] is False and s["expert_approved"] is False and s["can_publish"] is False
    if s["old_v207_id"] is not None:
        old=old_sent[s["old_v207_id"]]
        assert old["id"] not in seen_old
        seen_old.add(old["id"])
        assert s["segmentation_origin"]=="EXACT_REBASED_V207"
        assert (a,b)==(translate(k,old["start_char"]),translate(k,old["end_char"]))
    else:
        assert s["segmentation_origin"]=="REVISED_PARAGRAPH_RESPLIT"
        assert p["changed_by_v208_revision_id"] is not None
    by_para.setdefault(p["id"],[]).append(s)
assert len(by_para)==124 and len(counter)==10 and len(seen_old)==m["unchanged_sentences_rebased"]
for p in para.values():
    q=body[p["reader_key"]]
    prev=p["start_char"]
    for s in by_para[p["id"]]:
        assert not q[prev:s["start_char"]].strip()
        prev=s["end_char"]
    assert not q[prev:p["end_char"]].strip()
focus={f["id"]:f for f in v4["focus_tasks"]}
v9_migration={f["focus_id"]:f for f in v9["focus_migration"]}
dossiers={z["id"]:z for z in v8["source_passage_dossiers"]}
anchors={}
count_new=0
for a in x["focus_anchors"]:
    fid=a["focus_id"]
    assert fid in focus and fid not in anchors
    anchors[fid]=a
    old=v9_migration[fid]
    p=para[a["passage_id"]]
    assert p["reader_key"]==a["reader_key"] and p["section_id"]==a["section_id"]
    aa,bb=a["start_char"],a["end_char"]
    assert p["start_char"]<=aa<bb<=p["end_char"]
    assert body[a["reader_key"]][aa:bb]==a["excerpt_exact"]
    s=by_id[a["sentence_id"]]
    assert s["passage_id"]==p["id"] and s["start_char"]<=aa<bb<=s["end_char"]
    assert a["id"] in s["focus_anchor_ids"]
    if a["anchor_method"]=="RESEARCHER_PROPOSED_NEW_QUOTE_LOCATION":
        count_new+=1
        assert old["migration_status"].startswith("ANCHOR_RETIRED")
        assert a["v208_dossier_id"] in dossiers
        assert dossiers[a["v208_dossier_id"]]["focus_id"]==fid
    else:
        assert a["anchor_method"]=="UNCHANGED_EXACT_QUOTE_REBASED"
        assert old["migration_status"]=="UNCHANGED_EXACT_EXCERPT_REBASED"
        assert (aa,bb)==(old["new_excerpt_start_char"],old["new_excerpt_end_char"])
        assert a["v208_dossier_id"] is None
    assert a["source_proof_status"]=="NOT_DIRECTLY_VERIFIED_AGAINST_HISTORIC_ORIGINAL"
    assert a["human_review"]=="PENDING" and a["original_witness_collated"] is False and a["can_publish"] is False
assert len(anchors)==30 and count_new==8
for s in x["sentences"]:
    assert len(s["focus_anchor_ids"])==sum(a["sentence_id"]==s["id"] for a in anchors.values())
assert len(x["blockers"])>=6
print(f"PASS V210: {len(x['sentences'])} V209-sourced sentences, 30 exact focus anchors, 8 replacement reanchors, 12 editorial audit items; NO PUBLICATION")
