#!/usr/bin/env python3
"""Research-only IPO manuscript image access and online Latin interpretation QA.

Distinguishes catalog hrefs, actual manuscript pixels, unknown-edition online
transcriptions, and APW critical-edition pages. No original text validation.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_ipo_image_access_latin_text_v05.json"
PARENT="data/deep/vol05_ipo_direct_austrian_catalog_v04.json"
EXPECTED={
 "IPO-TEXT-V05-V-1":("V","1","IPO-LAT-V-1"),
 "IPO-TEXT-V05-V-2":("V","2","IPO-LAT-V-2"),
 "IPO-TEXT-V05-V-34":("V","34","IPO-LAT-V-34"),
 "IPO-TEXT-V05-V-35":("V","35",None),
 "IPO-TEXT-V05-V-36":("V","36","IPO-LAT-V-36"),
 "IPO-TEXT-V05-V-37":("V","37","IPO-LAT-V-37"),
 "IPO-TEXT-V05-VII-1":("VII","1","IPO-LAT-VII-1"),
 "IPO-TEXT-V05-VII-2":("VII","2","IPO-LAT-VII-2"),
 "IPO-TEXT-V05-VIII-2":("VIII","2","IPO-LAT-VIII-2"),
}
GATES={"original_image_pixels_reviewed","original_manuscript_folios_collated",
"apw_1998_printed_pages_reviewed","scholar_signed_off","image_redistribution_licensed",
"publication_approved"}

def load(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def bad(message):raise ValueError(message)

def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_IPO_MANUSCRIPT_IMAGE_ACCESS_AND_ONLINE_LATIN_READING",
        "DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        bad("invalid historical research object")
    if d["parent_registry"]!=PARENT or d["main_modified"] is not False or d["ai_studio_modified"] is not False or d["canonical_ids_created"]!=0:
        bad("research/public boundary crossed")
    if set(d["release_gate"])!=GATES or any(d["release_gate"].values()):
        bad("unauthorized scholarly collation/image rights/publication")
    base=load(PARENT)
    if base["canonical_document_id"]!=d["canonical_document_id"]:
        bad("previous direct catalog not linked")
    allowed={2594303,2594304,2594302}
    if {x["archive_item_id"] for x in base["direct_archival_catalogs"]}!=allowed:
        bad("archive catalog identity drift")
    images=d["archive_image_access_tests"]
    if len(images)!=3 or {x["image_index_observed"] for x in images}!={1,31,66}:
        bad("image lookup audit missing")
    for x in images:
        if x["archive_item_id"]!=2594303 or x["web_fetch_outcome"]!="CACHE_MISS":
            bad("unverified original image fetch promoted")
        url=urlparse(x["linked_preview_url_observed"])
        if url.scheme!="https" or url.hostname!="www.archivinformationssystem.at" or url.path!="/getimage.aspx":
            bad("preview image URL changed")
        expected="sqnznr="+str(x["image_index_observed"])
        if expected not in url.query or "veid=2594303" not in url.query or "width=200" not in url.query:
            bad("archive item/image index link mismatch")
        if x["image_pixels_verified"] is not False or x["clause_found_on_image"] is not None or x["folio_number"] is not None:
            bad("fabricated manuscript original physical folio reading")
    editions=d["edition_access_tests"]
    if len(editions)!=3 or {x["test_key"] for x in editions}!={"APW-PORTAL-PRIMARY","APW-PORTAL-SUPPLEMENT","APW-GOOGLE-BOOKS-1998"}:
        bad("edition access audit incomplete")
    ev={x["test_key"]:x for x in editions}
    if ev["APW-PORTAL-PRIMARY"]["outcome"]!="ACCESS_DENIED_ANUBIS" or ev["APW-PORTAL-SUPPLEMENT"]["outcome"]!="HTTP_TIMEOUT":
        bad("critical text falsely accessed")
    if ev["APW-GOOGLE-BOOKS-1998"]["outcome"]!="BIBLIOGRAPHIC_PAGE_ONLY" or ev["APW-GOOGLE-BOOKS-1998"]["year"]!=1998:
        bad("bibliographic listing mistaken for full edition")
    if any(x["printed_pages_read"] for x in editions):
        bad("APW critical edition pages not read")
    original=d["online_latin_source"]
    second=d["second_latin_source"]
    if original["source_type"]!="UNKNOWN_EDITION_MODERN_VOLUNTEER_TRANSCRIPTION" or original["text_access"]!="ONLINE_TEXT_READ" or original["not_authenticated_1648_witness"] is not True or original["not_apw_1998_text"] is not True:
        bad("online volunteer transcript falsely authenticated")
    if second["text_access"]!="SEARCH_EXCERPT_ONLY_AFTER_OPEN_502" or second["text_independence_unproven"] is not True:
        bad("second transcription wrongly treated as independently collated original")
    clauses=d["latin_clause_review"]
    if len(clauses)!=9 or {x["key"] for x in clauses}!=set(EXPECTED):
        bad("nine online Latin references including new V35 required")
    for c in clauses:
        if (c["article"],c["paragraph"],c["prior_anchor"])!=EXPECTED[c["key"]]:
            bad("clause/previous anchor crosswalk wrong")
        if not c["short_latin"] or len(c["short_latin"].split())>6 or not c["web_line_numbers"] or not c["interpretation_ko"]:
            bad("Latin location/brief interpretation missing")
        if c["original_printed_text_checked"] is not False or c["original_image_page"] is not None or c["apw_edition_page_directly_read"] is not None or c["original_witness_variants_checked"] is not False or c["publication_approved"] is not False:
            bad("false manuscript/APW/rights confirmation")
        if "NOT_ORIGINAL" not in c["status"] and c["status"]!="NEW_RESEARCH_CLAUSE_WEB_TRANSCRIPTION_NOT_CANONICAL":
            bad("evidence level upgraded improperly")
    if d["new_historical_insight"]["key"]!="IPO-V-35-CIVIC-EQUALITY" or d["new_historical_insight"]["old_canonical_article_modified"] is not False:
        bad("new civic rights theme confused with approved canonical record")
    if len(d["unresolved"])<6:
        bad("source limits hidden")
    report=(ROOT/"docs/01_CONTENT/VOL05/IPO_IMAGE_ACCESS_AND_CIVIC_RIGHTS_LATIN_V05.md").read_text(encoding="utf-8")
    if len(report)<6000 or report.count("\n## ")<4 or "DRAFT_RESEARCH_NOT_PUBLIC" not in report:
        bad("reader narrative missing")
    for word in ("제5조 §35","길드","상속","장례","§36","§37","121","129","이미지 픽셀"):
        if word not in report:
            bad("key content missing from deep narrative: "+word)
    return {"clauses":9,"image_requests":3,"edition_access_attempts":3,"new_civic_rights_topics":1,"released":0}

if __name__=="__main__":
    r=validate()
    print("PASS IPO V0.5: 9 online Latin clause readings including V35, 3 blocked archive images, 3 edition access attempts, PUBLIC 0")
