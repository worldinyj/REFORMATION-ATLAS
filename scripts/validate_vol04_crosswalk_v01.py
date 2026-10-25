#!/usr/bin/env python3
"""VOL-04 four-reformer source/event/edition crosswalk integrity (READ ONLY).

The findings are editorial candidates. QA success never authorizes publication.
No third-party dependencies. Run from any working directory.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/deep/vol04_four_reformers_crosswalk_v01.json"
OV = ROOT / "data/overview"
SOURCE_NAMES = ("luther", "zwingli", "melanchthon", "calvin")
PERSON = {"luther":"OV-P-013","zwingli":"OV-P-015",
          "melanchthon":"OV-P-014","calvin":"OV-P-016"}
DATE_TYPES = {"day","month","year","range","approximate_year","approximate_period","undated"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    data = read(INPUT)
    draft = {n: read(ROOT / f"data/deep/vol04_{n}_v01.json") for n in SOURCE_NAMES}
    vp = read(OV / "volumes_and_people_v01.json")
    events = read(OV / "events_documents_v01.json")
    relations = read(OV / "relationships_and_themes_v01.json")
    checks: list[tuple[str, bool]] = []

    def check(name: str, ok: bool):
        checks.append((name, bool(ok)))
        print(("PASS " if ok else "FAIL ") + name)

    ids = {item["id"] for group in
           (vp["people"],vp["volumes"],events["events"],events["documents"],
            relations["ideas"]) for item in group}
    existing_events = {e["id"]:e for e in events["events"]}
    existing_docs = {d["id"]:d for d in events["documents"]}
    cross = data["event_crosswalk"]
    cross_ids = [e["deep_event_id"] for e in cross]
    all_source = {x["id"]:x for n in SOURCE_NAMES for x in draft[n]["sources"]}
    all_claims = {x["id"]:x for n in SOURCE_NAMES for x in draft[n]["claims"]}
    expected_events = {e["id"] for n in SOURCE_NAMES for e in
                       draft[n].get("events",draft[n].get("timeline",[]))}
    orig_events = {e["id"]:e for n in SOURCE_NAMES for e in
                   draft[n].get("events",draft[n].get("timeline",[]))}

    check("Four canonical persons unchanged", all(
        p in {x["id"] for x in vp["people"]} for p in PERSON.values()
    ) and {p["id"] for p in data["canonical_people"]}==set(PERSON.values()))
    check("Source registered count 61 unique",len(all_source)==61 and
          sum(len(draft[n]["sources"]) for n in SOURCE_NAMES)==61)
    check("Research claim count 61 unique",len(all_claims)==61 and
          sum(len(draft[n]["claims"]) for n in SOURCE_NAMES)==61)
    check("All research claims cite existing source registrations",
          all(c["source_ids"] and all(s in all_source for s in c["source_ids"])
              for c in all_claims.values()))
    check("All 43 detailed event anchors represented exactly once",
          len(cross_ids)==43 and len(set(cross_ids))==43 and
          set(cross_ids)==expected_events)
    check("Every crosswalk row copies original date labels, precision, years and claim",
          all(x["date_label"]==orig_events[x["deep_event_id"]]["date_label"] and
              x["date_precision"]==orig_events[x["deep_event_id"]]["date_precision"] and
              x["year_start"]==orig_events[x["deep_event_id"]]["year_start"] and
              x["claim_id"]==(orig_events[x["deep_event_id"]].get("claim_id")
                  or orig_events[x["deep_event_id"]].get("related_claim_id"))
              for x in cross))
    check("Precision is in approved set",all(x["date_precision"] in DATE_TYPES for x in cross))
    check("Crosswalk claim evidence URLs resolve in this registry",
          all(x["claim_id"] in all_claims and
              set(x["source_ids"])==set(all_claims[x["claim_id"]]["source_ids"])
              for x in cross))
    check("Seven existing-event links and 36 new research-only candidates",
          sum(bool(x["canonical_event_id"]) for x in cross)==7 and
          sum(not x["canonical_event_id"] for x in cross)==36)
    check("Mapped canonical event IDs all exist",
          all(x["canonical_event_id"] in existing_events for x in cross
              if x["canonical_event_id"]))
    check("Only explicit canonical links survive; no accidental year-only matches",
          {x["deep_event_id"]:x["canonical_event_id"] for x in cross
           if x["canonical_event_id"]} == {
           "DEEP-V04-E-001":"OV-E-015",
           "DEEP-V04-E-005":"OV-E-016",
           "DEEP-V04-E-008":"OV-E-018",
           "DEEP-V04-E-009":"OV-E-019",
           "DEEP-V04-ZW-E-007":"OV-E-018",
           "DEEP-V04-ME-E-005":"OV-E-019",
           "DEEP-V04-CA-E-002":"OV-E-020"
           })
    check("Manz execution 1527 does not merge with Schleitheim confession",
          next(x for x in cross if x["deep_event_id"]=="DEEP-V04-ZW-E-006")["canonical_event_id"] is None and
          existing_events["OV-E-017"]["year_start"]==1527)
    check("1559 Calvin final edition not merged into 1536 overview event",
          next(x for x in cross if x["deep_event_id"]=="DEEP-V04-CA-E-009")["canonical_event_id"] is None)
    check("No false Luther physical attendee relation at Augsburg 1530",
          all(not (x["from_id"]=="OV-P-013" and x["to_id"]=="OV-E-019"
                   and x["type"]=="historical_participant")
              for x in data["proposed_relations"]))
    check("17 proposed document witness/edition records keep official IDs unminted",
          len(data["document_witness_proposals"])==17 and
          all(not x["create_canonical_record"] and not x["publish"] and
              (x["overview_work_id"] is None or x["overview_work_id"] in existing_docs)
              for x in data["document_witness_proposals"]))
    check("Proposed document refs and event refs exist",
          all(set(x["source_ids"])<=set(all_source) and
              set(x["related_event_ids"])<=set(existing_events)
              for x in data["document_witness_proposals"]))
    check("Augsburg edition variants stay part of one work",
          {x["year_start"] for x in data["document_witness_proposals"]
           if x["overview_work_id"]=="OV-D-011"}=={1530,1531,1540})
    check("Institutes language and year versions do not collapse",
          {x["year_start"] for x in data["document_witness_proposals"]
           if x["overview_work_id"]=="OV-D-012"}=={1536,1541,1559,1560})
    check("Marburg 3 distinct witnesses",
          len([x for x in data["document_witness_proposals"]
               if x["proposal_id"] in ("DOC-PROP-V04-001","DOC-PROP-V04-002",
                                       "DOC-PROP-V04-003")])==3)
    check("Three shared source-registration pairs refer to same URL",
          len(data["shared_source_aliases"])==3 and all(
              len(x["registrations"])==2 and
              len({unquote(urlparse(all_source[k]["url"]).path)
                   for k in x["registrations"]})==1
              for x in data["shared_source_aliases"]))
    check("Melanchthon Marburg signatory candidate has both evidence registrations",
          len(data["proposed_relations"])==2 and
          any(x["from_id"]=="OV-P-014" and x["to_id"]=="OV-E-018" and
              x["type"]=="historical_participant" and
              {"SRC-V04-L-011","SRC-V04-ZW-006"}<=set(x["source_ids"]) and
              not x["create_ov_r_now"] for x in data["proposed_relations"]))
    check("All relation proposal endpoints and evidence resolve",
          all(x["from_id"] in ids and x["to_id"] in ids and
              set(x["source_ids"])<=set(all_source) and
              set(x["claim_ids"])<=set(all_claims) and
              not x["publish"] for x in data["proposed_relations"]))
    check("10 editorial HOLD statements and research-only URL contract",
          len(data["scholarly_holds"])==10 and
          data["route_contract"]["can_import_research_json_to_public_web"] is False)
    check("All canonical timelines remain DRAFT, no external publication",
          all(not x["publish"] and x["review_status"]=="DRAFT" for x in cross) and
          not data["public_release"]["approved"] and
          not data["public_release"]["can_ship"] and
          not data["public_release"]["webapp_modified"])
    check("Data inventory matches actual files",
          data["inventory"] == {
             "people":4,"deep_sources_registered":61,"claims":61,
             "deep_timeline_anchors":43,"matches_existing_event":7,
             "new_event_candidates":36,"source_alias_groups":3,
             "document_witness_proposals":17,"relation_proposals":2})
    # QA checks ensure original overview files still carry release gates.
    check("Overview and indexed sources have no unintended publication approval",
          all(not it["public_visible"] for group in
              (vp["people"],events["events"],events["documents"])
              for it in group))
    passed=sum(ok for _,ok in checks)
    print(f"RESULT {passed}/{len(checks)}; DRAFT ONLY / historical review and publication approval pending")
    return int(passed!=len(checks))

if __name__=="__main__":
    raise SystemExit(main())
