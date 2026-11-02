#!/usr/bin/env python3
"""V207 strict structure and source-offset QA; NEVER a historian approval gate."""
import json
import re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def get(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
x=get("data/deep/atlas_v207_sentence_classification_and_provisional_claims.json")
v6=get("data/deep/atlas_v206_coverage_and_sentence_candidates.json")
v5=get("data/deep/atlas_v205_source_dossiers.json")
v4=get("data/deep/atlas_v204_paragraph_review_units.json")
v2=get("data/deep/atlas_v202_unified_ten_revised_readers.json")
assert x["version"]=="2.07"
assert x["lineage"]["parent_commit"]=="5d2589acde6390b078584780381be8b3c8fe38ba"
assert all(v is False for v in x["publication_gate"].values())
m=x["metrics"]
assert m["version_history_reader_count"]==10
assert m["v204_passage_units"]==len(v4["passages"])==124
assert m["v206_candidate_sentence_count"]==len(v6["sentence_candidates"])==522
assert m["repaired_technical_sentence_boundaries"]==len(x["correction_log"])==1
assert m["v207_corrected_sentence_units"]==len(x["sentences"])==521
assert m["priority_focus_claim_candidates"]==len(x["provisional_focus_claims"])==30
assert m["priorities_anchored_to_one_corrected_sentence"]==30
assert m["priority_claims_with_topic_level_dossiers"]==30
assert all(m[k]==0 for k in ("verified_primary_text_claims","human_classified_sentences","expert_approved_claims","public_claims"))
chapter={c["key"]:c["body"] for c in v2["chapters"]}
passage={p["id"]:p for p in v4["passages"]}
focus={f["id"]:f for f in v4["focus_tasks"]}
s6={s["id"]:s for s in v6["sentence_candidates"]}
v5ds={d["id"]:d for d in v5["dossiers"]}
v6ds={d["id"]:d for d in v6["remaining_focus_dossiers"]}
source_ids={s["id"] for s in v5["sources"]}|{s["id"] for s in v6["source_register"]}
rule_signals=[
 ("READER_QUESTION",r"[?？]|독서 질문:"),
 ("TEXT_EDITION_OR_BIBLIOGRAPHY",r"서지|필사본|판본|인쇄본|원전|라틴어판|프랑스어판|초판|개정판|이문|소장기호|출판|저작|헌사|필사|편집본"),
 ("EVENT_OR_CHRONOLOGY",r"[0-9]{4}년|세기|공의회|제국의회|칙령|회담|판결|처형|심문|회의|논쟁"),
 ("EDITORIAL_METHOD_OR_CAUTION",r"구분|주의|오해|단정|검토|확인|필요|다만|그러나|경계|사료|독자는|오류|자료|교감|설명해야|비교해야|혼동"),
 ("THEOLOGICAL_EXPOSITION",r"하나님|그리스도|구원|은혜|믿음|성례|성만찬|교회론|세례|예정론|성경|의롭다 함"),
 ("HISTORICAL_NARRATIVE_OR_CONTEXT",r".*")
]
assert [r["category"] for r in x["category_precedence"]]==[z[0] for z in rule_signals]
assert [r["js_regex"].removeprefix("(?:").removesuffix(")") for r in x["category_precedence"]]==[z[1] for z in rule_signals]
def classify(t):
    return next(label for label,regex in rule_signals if re.search(regex,t))
corrected=x["sentences"]
counts=Counter()
count_classes=Counter()
seen6=set()
seen_sent=set()
per_passage={}
repair=x["correction_log"][0]
assert repair["type"]=="MERGE_FALSE_PERIOD_IN_ARCHIVAL_SHELFMARK"
assert repair["problem_token"]=="E I 3.1, Nr. 54"
assert len(repair["original_sentence_ids"])==2
for s in corrected:
    p=passage[s["passage_id"]]
    k=s["reader_key"]
    counts[k]+=1
    assert s["id"]==f"SNT-V207-{k}-{counts[k]:04d}" and s["id"] not in seen_sent
    seen_sent.add(s["id"])
    assert p["reader_key"]==k and p["section_id"]==s["section_id"]
    a,b=s["start_char"],s["end_char"]
    assert p["start_char"]<=a<b<=p["end_char"]
    t=chapter[k][a:b]
    assert s["excerpt"]==t[:120] and s["character_count"]==len(t)
    assert s["suggested_category"]==classify(t)
    count_classes[s["suggested_category"]]+=1
    assert s["classification_basis"]=="DETERMINISTIC_LEXICAL_HEURISTIC_NOT_HUMAN"
    assert s["category_human_review"]=="PENDING"
    assert s["is_single_atomic_historical_claim"]=="UNDETERMINED"
    assert s["historical_claim_source_verified"] is False and s["original_witness_collated"] is False and s["can_publish"] is False
    originals=s["source_v206_sentence_ids"]
    assert originals and all(i in s6 for i in originals)
    assert all(i not in seen6 for i in originals)
    seen6.update(originals)
    assert all(s6[i]["passage_id"]==p["id"] for i in originals)
    assert a==s6[originals[0]]["start_char"] and b==s6[originals[-1]]["end_char"]
    if len(originals)==2:
        assert originals==repair["original_sentence_ids"]
        assert s["repair_id"]==repair["id"]
        assert repair["original_start_char"]==a and repair["original_end_char"]==b
        assert "E I 3.1, Nr. 54" in t
    else:
        assert len(originals)==1 and s["repair_id"] is None
    per_passage.setdefault(p["id"],[]).append(s)
assert seen6==set(s6)
assert len(per_passage)==124
assert set(counts)==set(chapter)
assert sum(count_classes.values())==521
assert m["suggested_sentence_categories"]=={r[0]:count_classes[r[0]] for r in rule_signals}
for p in v4["passages"]:
    text=chapter[p["reader_key"]]
    current=p["start_char"]
    for unit in per_passage[p["id"]]:
        assert not text[current:unit["start_char"]].strip()
        current=unit["end_char"]
    assert not text[current:p["end_char"]].strip()
s7={s["id"]:s for s in corrected}
assert len(s7)==521
seenFocus=set()
linked=Counter()
for claim in x["provisional_focus_claims"]:
    old=focus[claim["original_focus_task_id"]]
    assert old["id"] not in seenFocus
    seenFocus.add(old["id"])
    short=old["id"].removeprefix("FOCUS-V204-")
    assert claim["id"]==f"CLM-V207-{short}"
    assert (claim["reader_key"],claim["passage_id"],claim["section_id"])==(old["reader_key"],old["passage_id"],old["section_id"])
    assert claim["exact_v202_source_excerpt"]==old["exact_source_excerpt"]
    assert (claim["exact_source_excerpt_start_char"],claim["exact_source_excerpt_end_char"])==(old["excerpt_start_char"],old["excerpt_end_char"])
    assert chapter[old["reader_key"]][old["excerpt_start_char"]:old["excerpt_end_char"]]==claim["exact_v202_source_excerpt"]
    sent=s7[claim["corrected_sentence_id"]]
    assert sent["reader_key"]==old["reader_key"] and sent["passage_id"]==old["passage_id"]
    assert sent["start_char"]<=old["excerpt_start_char"]<old["excerpt_end_char"]<=sent["end_char"]
    assert claim["candidate_atomic_claim_ko"] and claim["context_and_anachronism_guard_ko"]
    assert claim["editorial_review_priority"] in ("P0","P1")
    dossier=claim["provenance_dossier_id"]
    if claim["provenance_stage"]=="V205":
        assert dossier in v5ds and v5ds[dossier]["focus_task_id"]==old["id"]
        assert claim["related_source_leads_not_direct_proof"]==v5ds[dossier]["reviewed_source_ids"]
    else:
        assert claim["provenance_stage"]=="V206"
        assert dossier in v6ds and v6ds[dossier]["focus_id"]==old["id"]
        assert claim["related_source_leads_not_direct_proof"]==v6ds[dossier]["source_ids"]
    assert all(k in source_ids for k in claim["related_source_leads_not_direct_proof"])
    assert claim["source_original_edition_id"] is None
    assert claim["source_original_page_folio_or_clause"] is None
    assert claim["human_claim_decomposition_review"]=="PENDING"
    assert claim["evidence_status"]=="SOURCE_TOPIC_TRIAGE_ONLY_NOT_EXACT_PRIMARY_TEXT"
    assert claim["primary_text_directly_collated"] is False and claim["expert_approved"] is False and claim["can_publish"] is False
    linked[claim["corrected_sentence_id"]]+=1
    assert claim["id"] in sent["linked_v207_provisional_claim_ids"]
assert seenFocus==set(focus)
for s in corrected:
    assert len(s["linked_v207_provisional_claim_ids"])==linked[s["id"]]
    assert s["editorial_priority"]==("SOURCE_REVIEW_PRIORITY" if linked[s["id"]] else "STANDARD_REVIEW")
assert len(x["unresolved"])>=6
print(f"PASS V207: {len(corrected)} corrected sentence units in 124 paragraphs, "
      f"{len(seenFocus)} anchored provisional claims, 1 archive-number repair; "
      "expert/publication approval remains zero.")
