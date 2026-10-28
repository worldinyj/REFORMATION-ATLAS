#!/usr/bin/env python3
"""Evidence-integrity and publication-gate check for VOL04 Cranmer & Prayer Books.

This does not collate printed sources or authorize public release.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATH = "data/deep/vol04_prayerbook_editions_research_v01.json"
YEARS = [1549, 1552, 1559]
TYPES = {"COMMUNION_DISTRIBUTION_FORMULA","KNEELING_BLACK_RUBRIC",
         "1549_PRINTING_ISSUE_PRIORITY","STATE_LAW_VS_LITURGICAL_TEXT"}

def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def validate(d=None):
    d = load(PATH) if d is None else d
    if (d["kind"] if "kind" in d else "BCP_RESEARCH") not in ("BCP_RESEARCH","VOL04_PRAYERBOOK_EDITION_RESEARCH"):
        raise ValueError("unknown contract kind")
    if d["status"] != "RESEARCH_NOT_PUBLIC" or d["volume_id"] != "VOL-04":
        raise ValueError("wrong research volume/status")
    if d["canonical_work_id"] != "OV-D-013" or d["canonical_person_id"] != "OV-P-019":
        raise ValueError("canonical work/person identity drift")
    if d["source_text_fully_collated"] is not False or any(d["release_gate"].values()):
        raise ValueError("unjustified publication/collation assertion")
    overview = load("data/overview/events_documents_v01.json")
    people = load("data/overview/volumes_and_people_v01.json")
    assert any(x["id"] == "OV-D-013" and x["volume_ids"] == ["VOL-04"] for x in overview["documents"])
    assert any(x["id"] == "OV-P-019" and x["volume_ids"] == ["VOL-04"] for x in people["people"])
    if len(d["chapters"]) != 2 or len(set(d["chapters"])) != 2:
        raise ValueError("two reader chapters expected")
    for p in d["chapters"]:
        rel=Path(p)
        if rel.is_absolute() or ".." in rel.parts or rel.suffix!=".md":
            raise ValueError("unsafe chapter path")
        body=(ROOT/rel).read_text(encoding="utf-8")
        if len(body)<3800 or body.count("\n## ")<4:
            raise ValueError("underdeveloped historical chapter " + p)
        if not ("RESEARCH_NOT_PUBLIC" in body or "DRAFT" in body):
            raise ValueError("missing draft marker " + p)
    sources=d["sources"]
    if len(sources)!=13:
        raise ValueError("registered source inventory drift")
    sindex={}
    for src in sources:
        k=src["research_source_key"]
        if not k.startswith("PRB-SRC-PROP-") or k in sindex:
            raise ValueError("source identifier invalid or duplicated")
        if src["canonical_source_id"] is not None or src["reuse_rights_approved"] is not False or src["full_text_collated"] is not False:
            raise ValueError("source rights or evidence falsely approved")
        if src["access_level"] not in {"ABSTRACT_ONLY","INSTITUTIONAL_WEB_DESCRIPTION_CHECKED","INSTITUTIONAL_CATALOG_ENTRY_CHECKED","INSTITUTIONAL_SEARCH_SNIPPET_CHECKED","INSTITUTIONAL_ABSTRACT_CHECKED"}:
            raise ValueError("bad source evidence level")
        u=urlparse(src["url"])
        if u.scheme!="https" or not u.netloc:
            raise ValueError("insecure evidence URL")
        sindex[k]=src
    eds=d["edition_families"]
    if [x["year"] for x in eds]!=YEARS or len({e["research_edition_key"] for e in eds})!=3:
        raise ValueError("edition family/year mismatch")
    eindex={}
    witnesskeys=set()
    witness_count=0
    for edition in eds:
        key=edition["research_edition_key"]
        if key != f"PRB-EDN-PROP-{edition['year']}" or edition["work_id"]!="OV-D-013" or edition["language"]!="en":
            raise ValueError("invalid edition proposal")
        if edition["approved"] is not False or not edition["print_witnesses"]:
            raise ValueError("edition premature release or no physical witnesses")
        if edition["posthumous_to_cranmer"] != (edition["year"]==1559):
            raise ValueError("1559 is after Cranmer death")
        if edition["compiled_by_cranmer"] != (edition["year"]!=1559):
            raise ValueError("Cranmer did not compile 1559 posthumously")
        eindex[key]=edition
        for witness in edition["print_witnesses"]:
            keyw=witness["witness_key"]
            if keyw in witnesskeys or not keyw.startswith("PRB-WIT-PROP-"):
                raise ValueError("witness key collision")
            witnesskeys.add(keyw)
            witness_count+=1
            if not witness["physical_object_confirmed_by_institution"]:
                raise ValueError("unverified holding asserted")
            if not witness["repository"] or not witness["source_keys"]:
                raise ValueError("missing institution/source")
            if not set(witness["source_keys"]) <= set(sindex):
                raise ValueError("unregistered witness evidence")
    if witness_count!=6:
        raise ValueError("witness count drift")
    comparisons=d["comparisons"]
    if len(comparisons)!=4 or {c["comparison_type"] for c in comparisons} != TYPES:
        raise ValueError("comparison coverage drift")
    if len(set(c["research_comparison_key"] for c in comparisons))!=len(comparisons):
        raise ValueError("duplicate comparison keys")
    for cmp in comparisons:
        if cmp["original_edition_text_collated"] is not False:
            raise ValueError("cannot claim original collation")
        if not cmp["observation_ko"] or not cmp["interpretation_ko"] or not cmp["evidence_level"]:
            raise ValueError("unqualified comparison")
        if not cmp["source_keys"] or not set(cmp["source_keys"]) <= set(sindex):
            raise ValueError("missing comparison sources")
        if not cmp["edition_keys"] or not set(cmp["edition_keys"]) <= set(eindex):
            raise ValueError("comparison cites nonexistent edition")
    by_type={c["comparison_type"]:c for c in comparisons}
    if len(by_type["COMMUNION_DISTRIBUTION_FORMULA"]["edition_keys"])!=3:
        raise ValueError("all three formulations must be compared")
    if by_type["KNEELING_BLACK_RUBRIC"].get("printing_variation_hold") is not True:
        raise ValueError("Black Rubric press variation hold removed")
    if by_type["1549_PRINTING_ISSUE_PRIORITY"]["edition_keys"]!=["PRB-EDN-PROP-1549"]:
        raise ValueError("printing priority must concern 1549 only")
    if "1559" not in d["person_historical_hold"]["claim"] or len(d["editorial_holds"])<6:
        raise ValueError("late author and remaining scholarly holds lost")
    if "HL/PO/PU/1/1558/1Eliz1n2" not in d["witness_warning"]:
        raise ValueError("Parliament act vs printed BCP witness boundary lost")
    return {"edition_families":len(eds),"witnesses":witness_count,"sources":len(sindex),"comparisons":len(comparisons),"public":0}

if __name__=="__main__":
    r=validate()
    print(f"PASS: {r['edition_families']} edition families, {r['witnesses']} witnesses, {r['comparisons']} comparisons, {r['sources']} sources; PUBLIC 0")
