#!/usr/bin/env python3
"""V206 triage, provenance and sentence candidate reproducibility.
No text, topic/source link or CI pass implies historical fact certification.
"""
import json,re
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rd(p):return json.loads((R/p).read_text(encoding="utf-8"))
x=rd("data/deep/atlas_v206_coverage_and_sentence_candidates.json")
v205=rd("data/deep/atlas_v205_source_dossiers.json")
v204=rd("data/deep/atlas_v204_paragraph_review_units.json")
v202=rd("data/deep/atlas_v202_unified_ten_revised_readers.json")
assert x["version"]=="2.06"
assert x["parent"]["commit"]=="a0f8a69ddd4361352e1087eff8664487a9cd1bc8"
assert all(v is False for v in x["publication_gate"].values())
m=x["metrics"]
assert (m["reader_count"],m["paragraph_units"],m["focus_tasks_total"])==(10,124,30)
assert (m["previously_triaged_focus_tasks"],m["newly_triaged_focus_tasks"],m["focus_tasks_with_topic_level_triage"])==(17,13,30)
assert (m["expert_classified_atomic_claims"],m["original_manuscript_collations"],m["verified_for_publication"])==(0,0,0)
assert len(x["source_register"])==m["new_source_records"]==16
assert len(x["remaining_focus_dossiers"])==13
assert len(x["research_observations"])==m["new_research_observations"]==26
assert len(x["sentence_candidates"])==m["v206_sentence_candidates"]>=250
source={s["id"]:s for s in x["source_register"]}
assert len(source)==16 and len({s["url"] for s in source.values()})==16
assert sum(z["access_status"]=="HTML_OPENED" for z in source.values())==m["source_html_opened"]
assert sum(z["access_status"]=="SEARCH_EXCERPT_ONLY" for z in source.values())==m["source_search_excerpt_only"]
assert all(s["url"].startswith("https://") for s in source.values())
assert all(s["original_manuscript_or_sixteenth_century_print_folio_directly_collated"] is False for s in [])  # no legacy schema migration
assert all(s["manuscript_or_sixteenth_century_print_folio_directly_collated"] is False and s["primary_source_translation_reproduced_in_repository"] is False and s["external_source_image_licence_verified"] is False for s in source.values())
chap={c["key"]:c["body"] for c in v202["chapters"]}
paras={p["id"]:p for p in v204["passages"]}
task={t["id"]:t for t in v204["focus_tasks"]}
v205_done={d["focus_task_id"] for d in v205["dossiers"]}
new_ids=set()
obs={o["id"]:o for o in x["research_observations"]}
assert len(obs)==26
for d in x["remaining_focus_dossiers"]:
  assert d["focus_id"] in task and d["focus_id"] not in v205_done and d["focus_id"] not in new_ids
  new_ids.add(d["focus_id"])
  t=task[d["focus_id"]]
  assert (d["reader_key"],d["passage_id"],d["section_id"],d["exact_source_excerpt"])==(t["reader_key"],t["passage_id"],t["section_id"],t["exact_source_excerpt"])
  assert chap[t["reader_key"]][t["excerpt_start_char"]:t["excerpt_end_char"]]==t["exact_source_excerpt"]
  assert all(i in source for i in d["source_ids"])
  assert len(d["observation_ids"])==2
  assert d["primary_folio_collated"] is False and d["scholarly_signoff"] is False and d["can_publish"] is False
  assert d["claim_level_verification"]=="PROVISIONAL_RESEARCH"
  for oid in d["observation_ids"]:
    o=obs[oid]
    assert o["dossier_id"]==d["id"] and o["focus_id"]==d["focus_id"]
    assert o["source_ids"]==d["source_ids"]
    assert o["original_witness_location_verified"] is False
    assert o["human_specialist_approved"] is False and o["can_publish"] is False
assert v205_done.isdisjoint(new_ids)
assert len(v205_done|new_ids)==len(x["focus_coverage"])==30
assert {y["focus_id"] for y in x["focus_coverage"]}==set(task)
for record in x["focus_coverage"]:
  assert record["topic_triage_complete"] is True
  assert record["primary_text_verified"] is False and record["expert_signoff"] is False and record["can_publish"] is False
  assert bool(record["v205_dossier_id"])!=bool(record["v206_dossier_id"])
sn=Counter()
by_para={}
for s in x["sentence_candidates"]:
  p=paras[s["passage_id"]]
  k=p["reader_key"]
  sn[k]+=1
  assert s["id"]==f"SNT-V206-{k}-{sn[k]:04d}"
  assert s["reader_key"]==k and s["section_id"]==p["section_id"]
  a,b=s["start_char"],s["end_char"]
  assert p["start_char"]<=a<b<=p["end_char"]
  content=chap[k][a:b]
  assert len(content)==s["char_count"] and s["excerpt"]==content[:110]
  assert s["segment_type"]=="UNCLASSIFIED_CANDIDATE_NOT_ATOMIC_CLAIM"
  assert s["source_line_verified"] is False and s["original_text_collated"] is False and s["expert_classified"] is False and s["can_publish"] is False
  by_para.setdefault(p["id"],[]).append(s)
assert len(by_para)==124
for key,p in paras.items():
  units=by_para[key]
  original=chap[p["reader_key"]]
  pos=p["start_char"]
  for s in units:
    assert not original[pos:s["start_char"]].strip()
    pos=s["end_char"]
  assert not original[pos:p["end_char"]].strip()
  # Rebuild Unicode punctuation-based segmentation exactly.
  line=original[p["start_char"]:p["end_char"]]
  stops=[m.end() for m in re.finditer(r"[.!?。！？](?=\s|$)",line)]
  expected=[]
  start=0
  for end in stops+[len(line)]:
    a=start
    while a<end and line[a].isspace():a+=1
    b=end
    while b>a and line[b-1].isspace():b-=1
    if b>a:expected.append((p["start_char"]+a,p["start_char"]+b))
    start=end
  assert [(s["start_char"],s["end_char"]) for s in units]==expected
assert len(x["unresolved"])>=7
print(f"PASS V206: all 30 topics triaged (17 previous + 13 new), {len(obs)} fresh observations, {len(x['sentence_candidates'])} reproducible sentence candidates, zero primary approval")
