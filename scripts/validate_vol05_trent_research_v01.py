#!/usr/bin/env python3
"""VOL05 Trent three periods: historical-research references and default deny.

Structural QA only, not scholarly peer review, original Latin collation, or approval.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
PATH="data/deep/vol05_trent_catholic_reform_registry_v01.json"
EXPECTED_PHASES=[(1,1545,1547),(2,1551,1552),(3,1562,1563)]
EXPECTED_SESSIONS={4:("1546-04-08",1),6:("1547-01-13",1),7:("1547-03-03",1),
                   13:("1551-10-11",2),22:("1562-09-17",3),23:("1563-07-15",3),
                   24:("1563-11-11",3),25:("1563-12-03/04",3)}
EXPECTED_PERSONS={"OV-P-021","OV-P-022"}
EXPECTED_TYPES={"JUSTIFICATION","EUCHARISTIC_PRESENCE","EDUCATION_AND_REFORM"}

def read(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

def validate(d=None):
    d=read(PATH) if d is None else d
    if d["kind"]!="VOL05_TRENT_RESEARCH_DRAFT" or d["status"]!="DRAFT_RESEARCH_NOT_PUBLIC" or d["volume_id"]!="VOL-05":
        raise ValueError("wrong research contract")
    if (d["canonical_event_id"],d["canonical_document_id"])!=("OV-E-021","OV-D-014"):
        raise ValueError("existing event/document IDs must be preserved")
    if set(d["canonical_person_ids"])!=EXPECTED_PERSONS or len(d["canonical_person_ids"])!=2:
        raise ValueError("existing Catholic reform people changed")
    if d["created_canonical_ids"]!=0 or d["ai_studio_modified"] is not False or d["overview_modified"] is not False or any(d["release_gate"].values()):
        raise ValueError("unauthorized publication or overview/app change")
    overview=read("data/overview/events_documents_v01.json")
    people=read("data/overview/volumes_and_people_v01.json")
    event=next(e for e in overview["events"] if e["id"]=="OV-E-021")
    document=next(e for e in overview["documents"] if e["id"]=="OV-D-014")
    if (event["year_start"],event["year_end"])!=(1545,1563) or "VOL-05" not in event["volume_ids"] or "VOL-05" not in document["volume_ids"]:
        raise ValueError("Trent overview start/end/volume mismatch")
    known_people={x["id"]:x for x in people["people"]}
    if not all("VOL-05" in known_people[k]["volume_ids"] for k in EXPECTED_PERSONS):
        raise ValueError("wrong person volume")
    if len(d["chapters"])!=3 or len(set(d["chapters"]))!=3:
        raise ValueError("3 deep chapters expected")
    for path in d["chapters"]:
        rel=Path(path)
        if rel.is_absolute() or ".." in rel.parts or rel.suffix!=".md" or not str(rel).startswith("docs/01_CONTENT/VOL05/"):
            raise ValueError("unsafe narrative path")
        body=(ROOT/rel).read_text(encoding="utf-8")
        if len(body)<4200 or body.count("\n## ")<5:
            raise ValueError("underdeveloped reader chapter: "+path)
        if "DRAFT_RESEARCH_NOT_PUBLIC" not in body:
            raise ValueError("missing publication warning")
    source_index={}
    if len(d["source_records"])!=11:
        raise ValueError("11 source records required")
    for s in d["source_records"]:
        key=s["research_source_key"]
        if key in source_index or not key.startswith("TR-SRC-PROP-"):
            raise ValueError("bad/duplicate source ID")
        if s["canonical_source_id"] is not None or s["original_latin_text_collated"] is not False or s["reproduction_rights_approved"] is not False or s["public_approved"] is not False:
            raise ValueError("source verified/collated/released without approval")
        parsed=urlparse(s["url"])
        if parsed.scheme!="https" or not parsed.netloc or not s["source_type"] or not s["evidence_level"]:
            raise ValueError("invalid source evidence")
        source_index[key]=s
    phases=d["phase_records"]
    if len(phases)!=3 or [(p["ordinal"],p["year_start"],p["year_end"]) for p in phases]!=EXPECTED_PHASES:
        raise ValueError("wrong phase boundary")
    if [p["opening"] for p in phases]!=["1545-12-13","1551-05-01","1562-01-18"]:
        raise ValueError("phase openings drift")
    if any(p["research_only"] is not True or not p["primary_issues"] or p["key"]!=f"TR-PHASE-PROP-{p['ordinal']}" for p in phases):
        raise ValueError("invalid phase record")
    sessions=d["sessions"]
    if len(sessions)!=8 or {s["number"] for s in sessions}!=set(EXPECTED_SESSIONS):
        raise ValueError("session inventory drift")
    for s in sessions:
        num=s["number"]
        if (s["date"],s["phase"])!=EXPECTED_SESSIONS[num]:
            raise ValueError("session date/phase drift "+str(num))
        if s["key"]!=f"TR-SESSION-PROP-{num:02d}" or s["promoted_to_canonical"] is not False or s["full_original_collation"] is not False:
            raise ValueError("unapproved session ID or collation")
        if not s["subject"] or not s["category"] or not s["source_keys"] or not set(s["source_keys"])<=set(source_index):
            raise ValueError("unlinked session evidence")
    if "seminaries" not in next(s for s in sessions if s["number"]==23)["subject"]:
        raise ValueError("session 23 seminary context erased")
    comparisons=d["interpretive_comparisons"]
    if len(comparisons)!=3 or {c["kind"] for c in comparisons}!=EXPECTED_TYPES:
        raise ValueError("doctrinal comparisons missing")
    for c in comparisons:
        if c["direct_parallel_original_text_collated"] is not False or c["scholarly_debate_open"] is not True:
            raise ValueError("premature comparative scholarly closure")
        if not c["source_keys"] or not set(c["source_keys"])<=set(source_index) or not c["claims_ko"]:
            raise ValueError("comparison provenance missing")
        if len(c["participants"])<2:
            raise ValueError("doctrinal comparison collapsed to one side")
    context=d["catholic_reform_context"]
    if len(context)!=2 or {c["person_id"] for c in context}!=EXPECTED_PERSONS:
        raise ValueError("Catholic reform person identity mismatch")
    ignatius=next(c for c in context if c["person_id"]=="OV-P-021")
    teresa=next(c for c in context if c["person_id"]=="OV-P-022")
    if (ignatius["year"],ignatius["relation_to_trent"])!=(1540,"BEFORE_COUNCIL_NOT_CREATED_BY_COUNCIL"):
        raise ValueError("1540 Society of Jesus erroneously created by Trent")
    if (teresa["year"],teresa["relation_to_trent"])!=(1562,"PARALLEL_REFORM_MOVEMENT"):
        raise ValueError("Teresa reform chronological relation wrong")
    if any(not c["source_keys"] or not set(c["source_keys"])<=set(source_index) for c in context):
        raise ValueError("religious order source missing")
    if len(d["editorial_holds"])<8:
        raise ValueError("history and rights holds erased")
    return {"chapters":3,"phases":len(phases),"sessions":len(sessions),"sources":len(source_index),"comparisons":len(comparisons),"public":0}

if __name__=="__main__":
    r=validate()
    print(f"PASS: {r['chapters']} VOL05 chapters, {r['phases']} periods, {r['sessions']} session anchors, {r['sources']} sources, PUBLIC 0")
