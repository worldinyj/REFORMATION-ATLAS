#!/usr/bin/env python3
"""Research-only IPO original witness / APW edition crosswalk validation.

Structural checking only. Does NOT inspect original Austrian archival leaves,
read the 1998 critical-edition clauses, certify manuscript authenticity, or
grant rights for publication.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REL="data/deep/vol05_ipo_original_witness_apw_crosswalk_v02.json"
PRIOR="data/deep/vol05_ipo_latin_clause_audit_v01.json"
EXPECTED_WITNESSES={
  "IPO-WIT-AK-1648":("LWL:que2599","IMPERIAL_COMMON_NEGOTIATORS_INSTRUMENT"),
  "IPO-WIT-EMPEROR-1648":("LWL:que2595","IMPERIAL_EXECUTION"),
}
EXPECTED_EDNS={"IPO-EDN-APW-1998","IPO-EDN-APW-SUPPLEMENT","IPO-EDN-LWL-PDF"}

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def reject(detail):
    raise ValueError(detail)

def validate(d=None):
    d=load(REL) if d is None else d
    if d["kind"]!="VOL05_IPO_ORIGINAL_WITNESS_APW_CROSSWALK" or d["status"]!="DRAFT_RESEARCH_NOT_PUBLIC":
        reject("document is not an unpublished research crosswalk")
    if (d["volume_id"],d["canonical_event_id"],d["canonical_work_id"]) != ("VOL-05","OV-E-024","OV-D-015"):
        reject("canonical historical parent changed")
    if d["parent_clause_registry"]!=PRIOR or d["new_canonical_ids"]!=0:
        reject("invented ID or changed reference")
    if d["ai_studio_modified"] is not False or d["overview_modified"] is not False or any(d["publication_gate"].values()):
        reject("unauthorized app/overview change or publication approval")
    if set(d["publication_gate"])!={"original_manuscript_folios_collated","apw_primary_text_directly_compared",
             "contemporary_print_verified","scholar_approved","editor_approved","media_reuse_approved","can_ship"}:
        reject("release gate fields missing")
    sources=d["sources"]
    if len(sources)!=10 or len({s["key"] for s in sources})!=10:
        reject("ten evidence sources expected")
    by_source={}
    for source in sources:
        parsed=urlparse(source["url"])
        if not source["key"].startswith("IPO-WIT-SRC-") or parsed.scheme!="https" or not parsed.hostname:
            reject("invalid evidence URL")
        if source["rights_verified"] is not False or source["public_approved"] is not False or source["authenticated_original_page_read"] is not False or source["text_collated"] is not False:
            reject("original/rights falsely verified")
        if not source["access"] or not source["scope"] or not source["kind"]:
            reject("source type not recorded")
        by_source[source["key"]]=source
    if by_source["IPO-WIT-SRC-01"]["url"].find("urlID=2599")<0 or by_source["IPO-WIT-SRC-02"]["url"].find("urlID=2595")<0:
        reject("LWL catalog identifiers swapped")
    if by_source["IPO-WIT-SRC-07"]["kind"]!="DIGITAL_SCANNED_LATER_PUBLISHED_EDITION":
        reject("later scanned book mislabeled 1648 original")
    if by_source["IPO-WIT-SRC-10"]["access"]!="DIRECT_FETCH_TIMEOUT":
        reject("APW portal directly read without evidence")
    witnesses=d["witnesses"]
    if len(witnesses)!=2 or {w["key"] for w in witnesses}!=set(EXPECTED_WITNESSES):
        reject("two separate catalog entries required")
    witnessindex={}
    for w in witnesses:
        key=w["key"]
        if (w["record_id"],w["witness_type"])!=EXPECTED_WITNESSES[key]:
            reject("IPO-AK vs imperial-catalog identity confused")
        if w["date"]!="1648-10-24" or w["language"]!="la" or "Haus-, Hof- und Staatsarchiv" not in w["archival_institution"]:
            reject("wrong archival attribution")
        if w["exact_shelfmark"] is not None or w["page_or_folio_confirmed"] is not False or w["physical_image_read"] is not False:
            reject("invented precise archival shelfmark or leaf reading")
        if w["relationship_status"] not in {"RELATION_TO_IMPERIAL_EXECUTION_NOT_PROVED","RELATION_TO_IPO_AK_NOT_PROVED"}:
            reject("witness identity relationship prematurely decided")
        if w["readability"] not in {"CATALOG_ONLY","CATALOG_AND_LATER_PDF_ONLY"}:
            reject("physical witness directly read claim")
        if not w["source_keys"] or not set(w["source_keys"])<=set(by_source):
            reject("witness source not registered")
        if w["registry_url"]!=by_source[w["source_keys"][0]]["url"]:
            reject("witness registry URL conflict")
        witnessindex[key]=w
    if witnesses[0]["key"]==witnesses[1]["key"] or witnesses[0]["record_id"]==witnesses[1]["record_id"]:
        reject("two catalog entries merged")
    edns=d["editions"]
    if len(edns)!=3 or {e["key"] for e in edns}!=EXPECTED_EDNS:
        reject("three editions/edited resources must remain separate")
    ednidx={}
    for e in edns:
        if e["direct_text_read"] is not False or not e["editorial_relationship"]:
            reject("edition text falsely marked read")
        if not e["source_keys"] or not set(e["source_keys"])<=set(by_source):
            reject("edition not linked to bibliographic description")
        ednidx[e["key"]]=e
    a=ednidx["IPO-EDN-APW-1998"]
    if (a["year"],a["editor"],a["pages"],a["kind"])!=(1998,"Antje Oschmann","95–170","HISTORICAL_CRITICAL_EDITION"):
        reject("APW 1998 bibliographic identity drift")
    if ednidx["IPO-EDN-APW-SUPPLEMENT"]["kind"]!="SCHOLARLY_DIGITAL_TEXT_AND_TRANSLATION_RESOURCE":
        reject("digital supplement claimed to be physical original")
    if ednidx["IPO-EDN-LWL-PDF"]["kind"]!="DIGITAL_SCAN_OF_LATER_HISTORICAL_PUBLICATION":
        reject("42-page PDF claimed to be signed original")
    if len(d["clause_links"])!=8:
        reject("eight prior clause links expected")
    old=load(PRIOR)
    oldidx={x["key"]:x for x in old["clause_anchors"]}
    if len(oldidx)!=8 or {x["old_anchor_key"] for x in d["clause_links"]}!=set(oldidx):
        reject("prior Latin clause references missing or duplicated")
    for c in d["clause_links"]:
        prev=oldidx[c["old_anchor_key"]]
        if (c["article"],c["paragraph"])!=(prev["article"],prev["paragraph"]):
            reject("article locator altered in witness crosswalk")
        if c["reference_edition"]!="IPO-EDN-APW-1998" or c["witness_key_for_future"]!="IPO-WIT-AK-1648":
            reject("wrong treaty/edition association")
        if c["folio"] is not None or c["line"] is not None or c["apw_edition_page"] is not None:
            reject("unsupported line-level collation coordinates")
        if c["critical_edition_directly_compared"] is not False or c["original_document_directly_compared"] is not False:
            reject("unread witness cited as verified")
        if c["source_status"]!="RESEARCH_LINK_ONLY":
            reject("evidence level promoted without research")
    holds=d["unresolved"]
    if len(holds)<7 or len({h["key"] for h in holds})!=len(holds) or any(h["status"]!="OPEN" for h in holds):
        reject("unresolved scholarly questions silently closed")
    if d["hardened_classification"]!="CATALOG_WITNESS_LINKS_ONLY_NO_FULL_TEXT_COMPARISON":
        reject("scholarly evidence level changed")
    report=ROOT/"docs/01_CONTENT/VOL05/IPO_1648_ORIGINAL_WITNESS_APW_CROSSWALK_V02.md"
    text=report.read_text(encoding="utf-8")
    if len(text)<5000 or text.count("\n## ")<6 or "DRAFT_RESEARCH_NOT_PUBLIC" not in text:
        reject("research narrative missing or unpublished status hidden")
    for required in ["IPO-AK","1998","1649","2595","2599","95~170","직접 교감"]:
        if required not in text:
            reject("key source caveat omitted from narrative")
    return {"catalog_witness_entries":2,"academic_or_scanned_editions":3,"source_records":10,"clause_crosslinks":8,"public":0}

if __name__=="__main__":
    x=validate()
    print(f"PASS: IPO provenance V0.2 {x['catalog_witness_entries']} archival entries, {x['academic_or_scanned_editions']} edition resources, {x['source_records']} source links, {x['clause_crosslinks']} uncollated clauses, PUBLIC 0")
