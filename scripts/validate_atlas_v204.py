#!/usr/bin/env python3
"""V2.04 validation: provenance, exact offsets, identity and fail-closed research flags."""
import json
import re
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
d=load("data/deep/atlas_v204_paragraph_review_units.json")
src=load("data/deep/atlas_v202_unified_ten_revised_readers.json")
nav=load("data/contracts/atlas_v203_ten_reader_navigation.json")
legacy=load("data/contracts/atlas_v179_ten_reader_claim_evidence.json")
assert d["version"]=="2.04" and src["version"]=="2.02" and nav["version"]=="2.03"
assert d["origin"]["parent_commit"]=="4bbc78f2d4b9c8cd819e9469d77216296c3d00cf"
assert all(v is False for v in d["publication_gate"].values())
assert nav["publication_gate"]["can_ship"] is False
assert d["metrics"]["reader_count"]==10 and d["metrics"]["section_count"]==70
assert d["metrics"]["passage_units"]==len(d["passages"])==124
assert d["metrics"]["focus_tasks"]==len(d["focus_tasks"])==30
assert d["metrics"]["passage_specific_sources_verified"]==d["metrics"]["original_witnesses_collated"]==0
chap={x["key"]:x for x in src["chapters"]}
rr={x["key"]:x for x in nav["readers"]}
old={x["reader_key"]:x for x in legacy["claims"]}
assert set(chap)==set(rr)==set(old) and len(chap)==10
expected={}
for key,c in chap.items():
  assert rr[key]["reader_page_id"]==c["source_id"]
  units=[]
  for sec in rr[key]["section_anchors"]:
    text=c["body"][sec["start_char"]:sec["end_char"]]
    for m in re.finditer(r"[^\n]+",text):
      raw=m.group(); line=raw.strip()
      if (len(line)<70 or line.startswith("#") or line=="---"
         or re.match(r"^\*\*(?:연구 출처|사료 확인 경로|한계|출처 경로|편집 상태)",line)
         or line.startswith("http://") or line.startswith("https://")
         or line.startswith("독서 질문:")): continue
      a=sec["start_char"]+m.start()+raw.index(line)
      units.append((sec["id"],a,a+len(line),line))
  expected[key]=units
assert sum(map(len,expected.values()))==124
ids=set();counts=Counter()
for unit in d["passages"]:
  k=unit["reader_key"]; ix=counts[k];counts[k]+=1
  sec,start,end,full=expected[k][ix]
  assert unit["id"]==f"PAR-V204-{k}-{ix+1:03d}" and unit["id"] not in ids
  ids.add(unit["id"])
  assert unit["reader_page_id"]==rr[k]["reader_page_id"]
  assert unit["section_id"]==sec
  assert (unit["start_char"],unit["end_char"],unit["character_count"])==(start,end,len(full))
  assert unit["excerpt"]==full[:140]
  assert chap[k]["body"][start:end]==full
  assert unit["unit_kind"]=="PROSE_REVIEW_UNIT_NOT_ATOMIC_CLAIM"
  assert unit["review_status"]=="NOT_REVIEWED"
  assert unit["passage_evidence_verified"] is False
  assert unit["original_collated"] is False and unit["can_publish"] is False
for row in d["reader_counts"]:
  assert counts[row["reader_key"]]==row["passage_units"]
  assert row["focus_tasks"]==3
assert set(counts)==set(chap)
units_by_id={x["id"]:x for x in d["passages"]}
task_ids=set();task_counts=Counter();priority=set()
for task in d["focus_tasks"]:
  k=task["reader_key"];task_counts[k]+=1
  assert task["id"]==f"FOCUS-V204-{k}-{task_counts[k]:02d}"
  assert task["id"] not in task_ids and task["passage_id"] in units_by_id
  task_ids.add(task["id"]);priority.add(task["passage_id"])
  unit=units_by_id[task["passage_id"]]
  assert unit["reader_key"]==k and unit["section_id"]==task["section_id"]
  start,end=task["excerpt_start_char"],task["excerpt_end_char"]
  excerpt=task["exact_source_excerpt"];body=chap[k]["body"]
  assert body[start:end]==excerpt and body.count(excerpt)==1
  assert unit["start_char"]<=start<end<=unit["end_char"]
  assert task["representative_legacy_claim_id"]==old[k]["id"]
  assert task["existing_topic_lead_urls_not_proof"]==old[k]["urls"]
  assert task["existing_evidence_cards_not_proof"]==old[k]["linked_evidence_cards"]
  assert task["required_evidence_kind"] and task["verification_question_ko"]
  assert task["witness_identifier"] is None and task["folio_page_or_clause"] is None
  assert task["expert_review"]=="PENDING" and task["verification_status"]=="UNVERIFIED"
  assert task["passage_checked_against_source"] is False
  assert task["original_folio_collated"] is False and task["can_publish"] is False
assert set(task_counts)==set(chap) and all(n==3 for n in task_counts.values())
assert d["metrics"]["distinct_priority_passages"]==len(priority)
assert len(d["open_issues"])>=5
print(f"PASS V204: {len(chap)} readers, {len(ids)} prose review units, {len(task_ids)} anchored focus tasks, {len(priority)} distinct priority passages; no scholarly/publication approval")
