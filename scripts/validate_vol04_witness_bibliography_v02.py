#!/usr/bin/env python3
"""Draft-only bibliographic evidence / edition-identity validator for VOL-04.

Only read-only structure/provenance validation. No network, no write, no
canonical ID allocation, and no permission to include drafts in PUBLIC apps.
Python 3 standard library.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
def read(rel: str):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

def validate(overview, bib, source_ids, report, spec):
    errors=[]
    def check(label, result):
        ok=bool(result)
        print(("PASS " if ok else "FAIL ")+label)
        if not ok:errors.append(label)

    original={p["proposal_id"]:p for p in overview["document_witness_proposals"]}
    new={p["proposal_id"]:p for p in bib["items"]}
    persons=read("data/overview/volumes_and_people_v01.json")
    works=read("data/overview/events_documents_v01.json")
    known_works={p["id"] for p in works["documents"]}
    known_people={p["id"] for p in persons["people"]}
    check("17 one-to-one proposal identities from V0.1",
          len(original)==17 and len(new)==17 and set(original)==set(new))
    check("Original proposal fields not mutated",
          all(all(n.get(k)==v for k,v in o.items())
              for pid,o in original.items() for n in [new.get(pid,{})]))
    check("Four canonical people remain in original overview",
          set(("OV-P-013","OV-P-014","OV-P-015","OV-P-016"))<=known_people)
    check("All 17 proposals have unique work/edition/witness role",
          all(x["material_kind"] and x["work_family"] for x in new.values()))
    check("No new canonical IDs have been minted",
          all(x["canonical_id"] is None and not x["promotion_allowed"]
              and not x["approved"] for x in new.values()) and
          bib["id_migration_gate"]["current_new_approved_ids"]==[])
    check("Two existing overview work families remain stable",
          set(bib["inventory"]["existing_overview_work_families"])=={"OV-D-011","OV-D-012"}
          and all(x["work_family"]==x["overview_work_id"]
                  for x in new.values() if x["overview_work_id"]))
    check("New works retain candidate rather than OV-D IDs",
          all(x["work_family"].startswith("WORK-PROP-V04-")
              for x in new.values() if x["overview_work_id"] is None))
    check("All source IDs resolve to original registered research sources",
          all(x["source_ids"] and set(x["source_ids"])<=source_ids
              for x in new.values()))
    check("All citation links use actual HTTPS URLs",
          all(x["verified_catalog_or_study_links"] and
              all(urlparse(url).scheme=="https" and urlparse(url).netloc
                  for url in x["verified_catalog_or_study_links"])
              for x in new.values()))
    check("Known language codes and metadata type",
          all(set(x["languages"])<= {"la","de","fr"} and
              bool(x["languages"]) and isinstance(x["imprint_or_provenance"],dict)
              for x in new.values()))
    check("Source-access/verification status is explicit",
          all(x["verification_status"] and x["editorial_note_ko"] and
              isinstance(x["original_full_text_collated"],bool)
              for x in new.values()))
    check("No source full-text collation claim is made",
          all(not x["original_full_text_collated"]
              and not x["translation_checked_against_original"]
              for x in new.values()))
    check("No media rights or publication approval",
          all(not x["media_rights_checked"] and not x["publish"]
              for x in new.values()) and
          not bib["release"]["approved"] and
          not bib["release"]["can_ship"] and
          not bib["release"]["web_code_modified"])
    check("Five mixed sources explicitly held for editorial split",
          {x["proposal_id"] for x in new.values()
           if x["split_required_before_promotion"]}==
          {"DOC-PROP-V04-004","DOC-PROP-V04-008",
           "EDN-PROP-V04-001","EDN-PROP-V04-002","DOC-PROP-V04-010"})
    check("Bib inventory counts correct",
          bib["inventory"]["proposals"]==17 and
          bib["inventory"]["split_required"]==5 and
          bib["inventory"]["can_migrate"]==0 and
          bib["inventory"]["original_texts_collated"]==0 and
          bib["inventory"]["approved"]==0)
    check("Augsburg editions 1530/1531/1540 stay in same work",
          {new[k]["year_start"] for k in
           ("EDN-PROP-V04-001","EDN-PROP-V04-002","EDN-PROP-V04-003")}==
          {1530,1531,1540} and
          all(new[k]["work_family"]=="OV-D-011"
              for k in ("EDN-PROP-V04-001","EDN-PROP-V04-002","EDN-PROP-V04-003")))
    check("Calvin editions 1536/1559/1541/1560 remain separate",
          {new[k]["year_start"] for k in
           ("EDN-PROP-V04-004","EDN-PROP-V04-005",
            "EDN-PROP-V04-006","EDN-PROP-V04-007")}==
          {1536,1541,1559,1560} and
          all(new[k]["work_family"]=="OV-D-012"
              for k in ("EDN-PROP-V04-004","EDN-PROP-V04-005",
                        "EDN-PROP-V04-006","EDN-PROP-V04-007")))
    check("Augsburg Apology is independent, not Confession edition",
          new["DOC-PROP-V04-010"]["work_family"]!="OV-D-011" and
          new["DOC-PROP-V04-010"]["split_required_before_promotion"])
    check("Original Marburg document and eyewitness reports distinct",
          len({new[k]["work_family"] for k in
               ("DOC-PROP-V04-001","DOC-PROP-V04-002",
                "DOC-PROP-V04-003")})==3)
    check("Marburg archive shelfmark preserved",
          new["DOC-PROP-V04-001"]["imprint_or_provenance"]["shelfmark"]=="E I 3.1 Nr. 54")
    check("Pitts Zwingli print remains composite with reference to printer",
          "Ramminger" in new["DOC-PROP-V04-004"]["imprint_or_provenance"]["printer"]
          and new["DOC-PROP-V04-004"]["split_required_before_promotion"])
    check("Geneva proposal and approval dates distinct",
          new["DOC-PROP-V04-006"]["imprint_or_provenance"]["draft_submitted"]=="1541-09-26" and
          new["DOC-PROP-V04-006"]["imprint_or_provenance"]["approved"]=="1541-11-20")
    check("1522 New Testament two-print distinction retained",
          len(new["DOC-PROP-V04-008"]["imprint_or_provenance"]["known_editions"])==2)
    check("No AI Studio app import and publication approval blocked",
          "공개" in report and "승인" in spec and
          bib["release"]["web_code_modified"] is False and
          bib["release"]["can_ship"] is False and
          "CAN_PUBLISH=false" in spec)
    check("17 proposals are all in the human review report",
          all(pid in report for pid in new))
    check("17 bibliography stages include human approval before IDs",
          len(bib["stages"])==5 and
          "Human review" in bib["stages"][3]["action"])
    return errors

def main():
    overview=read("data/deep/vol04_four_reformers_crosswalk_v01.json")
    bib=read("data/deep/vol04_witness_bibliography_v02.json")
    source_ids={s["id"] for name in ("luther","zwingli","melanchthon","calvin")
                for s in read(f"data/deep/vol04_{name}_v01.json")["sources"]}
    report=(ROOT/"docs/01_CONTENT/VOL04/WITNESS_EDITION_BIBLIOGRAPHY_V02.md").read_text(encoding="utf-8")
    spec=(ROOT/"docs/01_CONTENT/VOL04/EDITION_ID_MIGRATION_CONTRACT_V02.md").read_text(encoding="utf-8")
    errors=validate(overview,bib,source_ids,report,spec)
    print("RESULT",f"{26-len(errors)}/26" if len(errors)<=26 else "FAILED",
          "— DRAFT ONLY; does not authorize publication or IDs")
    return int(bool(errors))

if __name__=="__main__":
    raise SystemExit(main())
