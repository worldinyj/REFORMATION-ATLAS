#!/usr/bin/env python3
"""V2.05 external-source triage consistency and fail-closed research gates.
Structural verification is not historical primary-source collation or expert approval.
"""
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding="utf-8"))
d=load("data/deep/atlas_v205_source_dossiers.json")
v204=load("data/deep/atlas_v204_paragraph_review_units.json")
v203=load("data/contracts/atlas_v203_ten_reader_navigation.json")
v202=load("data/deep/atlas_v202_unified_ten_revised_readers.json")
assert d["version"]=="2.05" and v204["version"]=="2.04" and v203["version"]=="2.03" and v202["version"]=="2.02"
assert d["origin"]["research_base_commit"]=="28b64aca7ae19b18e1d36a7c3e8b087b9bca8580"
assert all(x is False for x in d["publication_gate"].values())
stats=d["metrics"]
assert stats["total_reader_count"]==10
assert stats["v204_prose_review_units"]==len(v204["passages"])==124
assert stats["v204_focus_tasks"]==len(v204["focus_tasks"])==30
assert stats["focus_with_new_web_source_dossiers"]==len(d["dossiers"])==17
assert stats["focus_without_new_web_review"]==13
assert stats["research_observations"]==len(d["atomic_research_observations"])==34
assert stats["original_witness_collations"]==stats["human_specialist_approvals"]==stats["public_approved_claims"]==0
source={x["id"]:x for x in d["sources"]}
assert len(source)==stats["source_records"]==12
assert sum(s["access_status"]=="OPENED_HTML" for s in source.values())==stats["full_web_pages_opened"]==11
assert sum(s["access_status"]=="SEARCH_RESULT_EXCERPT_ONLY" for s in source.values())==stats["search_excerpt_only_source_records"]==1
assert source["SRC-V205-MARB-ARCH"]["access_status"]=="SEARCH_RESULT_EXCERPT_ONLY"
assert all(s["original_manuscript_read"] is False and s["original_print_folio_collated"] is False and s["rights_to_embed_image_confirmed"] is False for s in source.values())
assert all(s["url"].startswith("https://") for s in source.values())
focus={x["id"]:x for x in v204["focus_tasks"]}
chapters={x["key"]:x for x in v202["chapters"]}
paragraphs={x["id"]:x for x in v204["passages"]}
dos={x["id"]:x for x in d["dossiers"]}
obs={x["id"]:x for x in d["atomic_research_observations"]}
assert len(obs)==34
reviewed=set()
for item in d["dossiers"]:
    assert item["focus_task_id"] in focus
    assert item["focus_task_id"] not in reviewed
    reviewed.add(item["focus_task_id"])
    target=focus[item["focus_task_id"]]
    assert item["reader_key"]==target["reader_key"]
    assert item["passage_id"]==target["passage_id"]
    assert item["source_excerpt"]==target["exact_source_excerpt"]
    body=chapters[item["reader_key"]]["body"]
    assert body[target["excerpt_start_char"]:target["excerpt_end_char"]]==item["source_excerpt"]
    assert all(s in source for s in item["reviewed_source_ids"])
    assert len(item["findings_observation_ids"])==2
    assert item["review_scope"]=="WEB_PAGE_OR_SEARCH_EXCERPT_NOT_ORIGINAL_WITNESS"
    assert item["primary_folio_or_original_print_read"] is False
    assert item["precise_original_page_passage_collated"] is False
    assert item["human_specialist_decision"]=="PENDING"
    assert item["public_import_allowed"] is False
    for observation_id in item["findings_observation_ids"]:
        o=obs[observation_id]
        assert o["review_id"]==item["id"]
        assert o["focus_task_id"]==item["focus_task_id"]
        assert set(o["documentary_basis_source_ids"])==set(item["reviewed_source_ids"])
        assert o["page_line_or_folio_original"] is None
        assert o["original_document_collated"] is False
        assert o["expert_approved"] is False and o["can_publish"] is False
assert set(focus)=={x["focus_task_id"] for x in d["focus_coverage"]}
assert len(d["focus_coverage"])==30
for coverage in d["focus_coverage"]:
    target=focus[coverage["focus_task_id"]]
    assert coverage["reader_key"]==target["reader_key"]
    assert coverage["passage_id"]==target["passage_id"] in paragraphs
    assert coverage["source_access_is_original_folio"] is False
    assert coverage["expert_verified"] is False and coverage["can_publish"] is False
    if target["id"] in reviewed:
        assert coverage["v205_dossier_id"] in dos
        assert coverage["research_stage"]=="WEB_SOURCE_TRIAGE_COMPLETE_OR_PARTIAL"
    else:
        assert coverage["v205_dossier_id"] is None
        assert coverage["research_stage"]=="NO_NEW_EVIDENCE_REVIEW"
assert len(d["editorial_priority_queue"])==6
for proposal in d["editorial_priority_queue"]:
    assert proposal["focus_task_id"] in reviewed
    assert proposal["status"]=="PROPOSED_NOT_MERGED"
    assert proposal["proposed_ko"]
assert len(d["blockers"])>=5
print(f"PASS V205: {len(dos)} evidence dossiers, {len(obs)} atomic research notes, "
      f"{len(focus)-len(reviewed)} PENDING focus tasks, zero primary collations, NO PUBLICATION")
