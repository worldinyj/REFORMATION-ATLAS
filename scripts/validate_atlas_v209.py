#!/usr/bin/env python3
"""V209 exact-source reconstruction, span rebase and hard publication hold.
Validating editorial provenance is not proving historical claims.
"""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
def rd(p):return json.loads((R/p).read_text(encoding="utf-8"))
v=rd("data/deep/atlas_v209_unified_ten_revised_readers.json")
v2=rd("data/deep/atlas_v202_unified_ten_revised_readers.json")
v3=rd("data/contracts/atlas_v203_ten_reader_navigation.json")
v4=rd("data/deep/atlas_v204_paragraph_review_units.json")
v8=rd("data/deep/atlas_v208_critical_passage_dossiers.json")
assert v["version"]=="2.09" and v["provenance"]["source_version"]=="2.02"
assert v["provenance"]["source_commit"]=="f2c16f3b5b006b8a745d123285201af77232301f"
assert all(x is False for x in v["publication_gate"].values())
old={x["key"]:x for x in v2["chapters"]}
new={x["key"]:x for x in v["chapters"]}
assert list(old)==list(new) and len(new)==10
edits={}
for e in v8["reader_paragraph_drafts"]:
  edits.setdefault(e["reader_key"],[]).append(e)
assert sum(len(x) for x in edits.values())==7
for key in edits: edits[key].sort(key=lambda x:x["start_char"])
def rebased(k,pos):
  delta=0
  for e in edits.get(k,[]):
    assert not (e["start_char"]<pos<e["end_char"])
    if pos>=e["end_char"]:
      delta+=len(e["proposed_paragraph"])-len(e["original_paragraph"])
  return pos+delta
changed=[]
for key,chapter in old.items():
  body=chapter["body"]
  for e in sorted(edits.get(key,[]),key=lambda x:x["start_char"],reverse=True):
    assert body[e["start_char"]:e["end_char"]]==e["original_paragraph"]
    body=body[:e["start_char"]]+e["proposed_paragraph"]+body[e["end_char"]:]
  assert new[key]["body"]==body
  assert new[key]["source_id"]==chapter["source_id"]
  assert new[key]["review_status"]=="PENDING"
  assert new[key]["editorial_stage"]=="REVISED_RESEARCH_DRAFT_NOT_APPROVED"
  assert new[key]["applied_v208_revision_ids"]==[e["id"] for e in edits.get(key,[])]
  if edits.get(key):changed.append(key)
  assert new[key]["source_version"]==("2.09" if edits.get(key) else chapter["source_version"])
assert len(changed)==5
metrics=v["metrics"]
assert (metrics["reader_count"],metrics["revised_reader_count"],metrics["unchanged_reader_count"],metrics["changed_paragraph_count"])==(10,5,5,7)
assert (metrics["section_count"],metrics["total_paragraph_review_units"],metrics["focus_count"])==(70,124,30)
assert metrics["original_codepoints"]==sum(len(x["body"]) for x in old.values())
assert metrics["new_codepoints"]==sum(len(x["body"]) for x in new.values())
assert metrics["original_nonwhitespace_chars"]==sum(sum(not q.isspace() for q in x["body"]) for x in old.values())
assert metrics["new_nonwhitespace_chars"]==sum(sum(not q.isspace() for q in x["body"]) for x in new.values())
navig={x["reader_key"]:x for x in v["section_navigation"]}
originalnav={x["key"]:x for x in v3["readers"]}
assert set(navig)==set(old)
for key in old:
  ns=navig[key]["sections"]
  os=originalnav[key]["section_anchors"]
  assert len(ns)==len(os)
  for i,(n,o) in enumerate(zip(ns,os)):
    assert n["source_section_id"]==o["id"]
    assert n["id"]==o["id"].replace("SEC-V203-","SEC-V209-")
    assert (n["start_char"],n["end_char"])==(rebased(key,o["start_char"]),rebased(key,o["end_char"]))
    if n["level"]>0:assert n["heading"] in new[key]["body"][n["start_char"]:n["end_char"]]
    assert n["evidence_review"]=="NOT_HISTORICALLY_APPROVED"
    assert n["start_char"]==(0 if i==0 else ns[i-1]["end_char"])
  assert ns[-1]["end_char"]==len(new[key]["body"])
paragraph={x["source_passage_id"]:x for x in v["paragraph_spans"]}
assert len(paragraph)==124
for oldp in v4["passages"]:
  p=paragraph[oldp["id"]]
  key=oldp["reader_key"]
  assert (p["start_char"],p["end_char"])==(rebased(key,oldp["start_char"]),rebased(key,oldp["end_char"]))
  ee=next((x for x in edits.get(key,[]) if x["passage_id"]==oldp["id"]),None)
  expected=ee["proposed_paragraph"] if ee else old[key]["body"][oldp["start_char"]:oldp["end_char"]]
  assert new[key]["body"][p["start_char"]:p["end_char"]]==p["text_exact"]==expected
  assert p["changed_by_v208_revision_id"]==(ee["id"] if ee else None)
  assert p["publication_approved"] is False
focus={x["focus_id"]:x for x in v["focus_migration"]}
assert len(focus)==30
retired=0
for oldf in v4["focus_tasks"]:
  item=focus[oldf["id"]]
  key=oldf["reader_key"]
  p=paragraph[oldf["passage_id"]]
  assert item["v209_passage_id"]==p["id"]
  e=next((x for x in edits.get(key,[]) if x["passage_id"]==oldf["passage_id"]),None)
  if e:
    retired+=1
    assert item["migration_status"]=="ANCHOR_RETIRED_REPLACED_PARAGRAPH_REQUIRES_HUMAN_REANCHOR"
    assert item["new_excerpt_start_char"] is None and item["new_excerpt_end_char"] is None
    assert item["linked_v208_revision_id"]==e["id"]
  else:
    assert item["migration_status"]=="UNCHANGED_EXACT_EXCERPT_REBASED"
    a,b=item["new_excerpt_start_char"],item["new_excerpt_end_char"]
    assert (a,b)==(rebased(key,oldf["excerpt_start_char"]),rebased(key,oldf["excerpt_end_char"]))
    assert new[key]["body"][a:b]==oldf["exact_source_excerpt"]
  assert item["has_verified_original_support"] is False and item["expert_review"]=="PENDING" and item["can_publish"] is False
assert retired==metrics["retired_focus_excerpt_anchors"]==8
assert metrics["reused_focus_excerpt_anchors"]==22
assert len(v["cross_reader_review"])==9
assert all(x["status"] in ("DRAFT_CONSISTENCY_REVIEWED","BLOCKED_PENDING_SCHOLARLY_REVIEW") for x in v["cross_reader_review"])
assert len(v["facsimile_access_audit"])==1
scan=v["facsimile_access_audit"][0]
assert scan["item_id"]=="bsb00056424" and scan["edition_ref"]=="VD16 D 924"
assert scan["scan_image_opened"] is False and scan["facsimile_page_identified"] is False
assert scan["folio_collated"] is False and scan["rights_cleared"] is False
assert len(v["blockers"])>=6
print(f"PASS V209: 10 reader bodies, 7 draft corrections in 5 chapters, 70 rebuilt sections, 124 paragraphs, 22 migrated/8 retired claim anchors, NO PUBLIC RELEASE")
