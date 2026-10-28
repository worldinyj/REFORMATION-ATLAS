#!/usr/bin/env python3
"""VOL05 IPO Austria archival crossreference and tentative APW page leads.

Checks classification and provenance only. It cannot certify manuscript
identity, an Austrian archival item page, or critical-edition text collation.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_ipo_archive_id_apw_page_leads_v03.json"
PARENT="data/deep/vol05_ipo_original_witness_apw_crosswalk_v02.json"
REPORT="docs/01_CONTENT/VOL05/IPO_AUSTRIAN_ARCHIVAL_ID_APW_PAGE_AUDIT_V03.md"
GROUP="AT-OeStA/HHStA UR AUR 1648 X 24"
GATES={"human_scholarly_approved","original_item_verified","physical_foil_read",
       "apw_1998_direct_text_read","rights_approved","can_publish"}
ITEMS={"ARCH-IPO-ITEM-393786":(393786,"WAR-TREATY-IPO-1648"),
       "ARCH-IPM-ITEM-1252067":(1252067,"WAR-TREATY-IPM-1648")}
PAGES={"IPO-LAT-V-34":("V","34",121),
       "IPO-LAT-VII-1":("VII","1",129)}

def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def fail(message):
    raise ValueError(message)

def validate(d=None):
    d=read(REG) if d is None else d
    if d["kind"]!="VOL05_IPO_ARCHIVAL_ID_AND_APW_PAGE_LEADS" or d["status"]!="DRAFT_RESEARCH_NOT_PUBLIC":
        fail("wrong research type")
    if (d["volume_id"],d["canonical_work_id"],d["canonical_event_id"])!=("VOL-05","OV-D-015","OV-E-024"):
        fail("canonical object changed")
    if d["new_canonical_ids"]!=0 or d["existing_app_changed"] is not False or d["parent"]!=PARENT:
        fail("public app or ID assertion")
    if set(d["publication_gate"])!=GATES or any(d["publication_gate"].values()):
        fail("release/rights/read level falsely approved")
    parent=read(PARENT)
    if parent["canonical_work_id"]!=d["canonical_work_id"] or parent["canonical_event_id"]!=d["canonical_event_id"]:
        fail("parent archive crosswalk missing")
    sources=d["source_records"]
    if len(sources)!=13:
        fail("13 evidence links required")
    src={}
    for s in sources:
        key=s["key"]
        url=urlparse(s["url"])
        if key in src or not key.startswith("ARCH-IPO-V03-S") or url.scheme!="https" or not url.hostname:
            fail("invalid/duplicate reference")
        if s["text_completely_collated"] is not False or s["publication_rights_approved"] is not False:
            fail("false original text collation or rights")
        if not s["access"] or not s["kind"]:
            fail("evidence access classification lost")
        src[key]=s
    group=d["archive_reference_group"]
    if group["referenced_fonds_or_group"]!=GROUP or group["granularity"]!="DATE_AND_SERIES_REFERENCE_SHARED_BY_SEPARATE_TREATY_RECORDS":
        fail("date-series archive scope confused")
    if group["is_unique_physical_copy_signature"] is not False or group["assurance"]!="GOVERNMENT_CROSS_REFERENCE_NOT_DIRECT_AUSTRIAN_ITEM_READ":
        fail("date-series shelfmark mislabeled unique archival item")
    if group["found_via_source"]!="ARCH-IPO-V03-S01":
        fail("PARES provenance missing")
    if len(d["archival_item_leads"])!=2 or {i["key"] for i in d["archival_item_leads"]}!=set(ITEMS):
        fail("IPO and IPM separate item leads required")
    for item in d["archival_item_leads"]:
        key=item["key"]
        if (item["registry_numeric_id"],item["treaty_key"])!=ITEMS[key]:
            fail("IPO vs IPM item/treaty identity error")
        if item["url"] not in [s["url"] for s in sources] or f"ID={item['registry_numeric_id']}" not in item["url"]:
            fail("archival detail URL mismatch")
        if not item["source_keys"] or not set(item["source_keys"])<=set(src):
            fail("archival item evidence lost")
        if item["direct_record_read"] is not False or item["original_image_found"] is not False or item["original_text_read"] is not False:
            fail("Austrian item falsely accessed")
        if key=="ARCH-IPO-ITEM-393786" and item["connected_to_lwl_ipo_ak"]!="UNRESOLVED":
            fail("IPO-AK identity falsely proven")
        if key=="ARCH-IPM-ITEM-1252067" and item["connected_to_lwl_ipo_ak"]!="NOT_APPLICABLE_DIFFERENT_TREATY":
            fail("IPM mislinked to IPO-AK")
    lwl=d["lwl_registrations"]
    if len(lwl)!=2 or {x["reference"] for x in lwl}!={"LWL:que2599","LWL:que2595"}:
        fail("LWL two catalog records lost")
    if any(x["same_as_austrian_393786"]!="UNRESOLVED" for x in lwl):
        fail("physical identity conclusion too early")
    edition=d["critical_edition"]
    if (edition["editor"],edition["year"],edition["pages_range"],edition["key"])!=("Antje Oschmann",1998,"95–170","IPO-EDN-APW-1998"):
        fail("APW critical edition bibliography wrong")
    if edition["primary_latin_page_directly_inspected"] is not False or not set(edition["source_keys"])<=set(src):
        fail("APW text falsely inspected")
    page=d["apw_indirect_page_leads"]
    if len(page)!=2 or {x["old_anchor_key"] for x in page}!=set(PAGES):
        fail("two preliminary page anchors required")
    for x in page:
        if (x["article"],x["paragraph"],x["reported_printed_page"])!=PAGES[x["old_anchor_key"]]:
            fail("candidate page/article mismatch")
        if x["reference_edition"]!=edition["key"] or x["evidence_source_key"] not in src:
            fail("APW book/source missing")
        if x["evidence_level"]!="SECONDARY_SEARCH_SNIPPET_ONLY_PDF_FETCH_BLOCKED" or x["editorial_status"]!="UNVERIFIED_CANDIDATE":
            fail("low confidence citation promoted")
        if x["direct_page_inspected"] is not False or x["verified_latin_words"] is not False:
            fail("uninspected edition page called verified")
    if len(d["unresolved"])<6 or any(x["status"]!="OPEN" for x in d["unresolved"]):
        fail("academic uncertainties hidden")
    doc=(ROOT/REPORT).read_text(encoding="utf-8")
    if len(doc)<4400 or doc.count("\n## ")<5 or "DRAFT_RESEARCH_NOT_PUBLIC" not in doc:
        fail("reader narrative missing/underdeveloped")
    for phrase in ["393786","1252067","95~170","121쪽","129쪽","UNVERIFIED_CANDIDATE"]:
        if phrase not in doc:
            fail("source warning absent in reader narrative: "+phrase)
    return {"archive_items":2,"source_records":13,"apw_page_leads":2,"public":0}

if __name__=="__main__":
    r=validate()
    print(f"PASS: IPO V0.3 {r['archive_items']} Austrian item leads, {r['source_records']} provenance sources, {r['apw_page_leads']} tentative APW pages, PUBLIC 0")
