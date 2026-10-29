#!/usr/bin/env python3
"""VOL05 V1.6 research-only audit: publishers' links and scholarly citations != inspected original records."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_kramergilde_1931_edition_access_audit_v16.json"
PARENT="data/deep/vol05_kramergilde_membership_1662_1797_v15.json"
ARTICLE="docs/01_CONTENT/VOL05/KRAMERGILDE_1931_EDITION_AND_ARCHIVE_ACCESS_V16.md"
GATES={"historian_approved","publisher_scan_p270_read","original_1719_guild_entry_read",
"current_kramergilde_register_shelfmark_confirmed","individual_confessional_V35_lawsuit_verified",
"original_image_rights_approved","can_publish"}
TASKS={"EA16-T-1931-P253","EA16-T-1931-P270","EA16-T-ARCHIVE-REGISTER","EA16-T-TREASURY"}
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def bad(why):raise ValueError(why)
def validate(d=None):
    d=read(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
      "VOL05_KRAMERGILDE_1931_EDITION_PRIMARY_SOURCE_ACCESS_AUDIT","DRAFT_RESEARCH_NOT_PUBLIC",
      "VOL-05","OV-E-024","OV-D-015"):
        bad("research identity or canonical reference changed")
    if d["parent"]!=PARENT or d["new_canonical_ids"]!=0 or d["main_modified"] is not False or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        bad("prior chain or main/web-app publication boundary broken")
    if set(d["publication_gate"])!=GATES or any(d["publication_gate"].values()):
        bad("unapproved original/source/right/release gate")
    parent=read(PARENT)
    if parent["canonical_event_id"]!=d["canonical_event_id"] or parent["canonical_document_id"]!=d["canonical_document_id"]:
        bad("V1.5 historical line incompatible")
    bib=d["bibliography"]
    if (bib["author"],bib["publication_year"],bib["printed_pages"],bib["person_page_to_inspect"],bib["implied_member_year_to_inspect"],bib["indirect_person"],bib["indirect_member_class"])!=(
      "Josef Ketteler",1931,[253,295],270,1719,"Anton Reinhard Neuhaus","Amtsohn"):
        bad("published 1931 and 1719 named secondhand citation corrupted")
    if bib["original_print_p270_read"] is not False or bib["original_member_register_read"] is not False:
        bad("print p270 or guild register falsely collated")
    src=d["sources"]
    if len(src)!=8 or len({x["id"] for x in src})!=8:
        bad("8 individually provenance-tagged links required")
    byid={x["id"]:x for x in src}
    for s in src:
        u=urlparse(s["url"])
        if u.scheme!="https" or not u.hostname or not s["supported"] or not s["access"]:
            bad("bad URL or ungraded source claim")
        if s["original_guild_read"] is not False or s["ketteler_1931_p270_read"] is not False:
            bad("unread source promoted to direct primary evidence")
    if byid["EA16-S01"]["type"]!="PUBLISHER_OFFICIAL_SERIES_CATALOG_P70":
        bad("official publisher catalog access confused")
    if byid["EA16-S02"]["access"]!="WEB_DIRECT_OPEN_FAILED":
        bad("Archive.org published scan link could not be opened")
    if byid["EA16-S03"]["access"]!="SEARCH_RESULT_INDEX_PDF_DIRECT_OPEN_CACHE_MISS":
        bad("Saxon Academy PDF original or Ketteler 1931 p270 falsely visually verified")
    if byid["EA16-S04"]["access"]!="FULL_HTML_READ" or "uni-muenster.de" not in byid["EA16-S04"]["url"]:
        bad("archive institutional history source lost")
    if bib["main_source"]!="EA16-S01" or bib["secondary_bio_source"]!="EA16-S03":
        bad("bibliographical vs biographical source confusion")
    tasks=d["reading_tasks"]
    if len(tasks)!=4 or {x["id"] for x in tasks}!=TASKS:
        bad("four exact primary or printed source tasks must remain")
    bytask={x["id"]:x for x in tasks}
    if bytask["EA16-T-1931-P270"]["result"]!="NOT_READ":
        bad("Ketteler 1931 p270 remains visually unverified")
    if bytask["EA16-T-ARCHIVE-REGISTER"]["result"]!="NOT_LOCATED" or bytask["EA16-T-TREASURY"]["result"]!="NOT_READ":
        bad("guild and treasury original not yet located/read")
    for task in tasks:
        if not task["evidence_required"] or not task["no_substitute"]:
            bad("exact acceptance criteria missing")
    edges=d["provenance_edges"]
    if len(edges)!=7:
        bad("seven separate source-provenance relations required")
    byedge={x["edge"]:x["status"] for x in edges}
    if byedge.get("Ketteler 1931 printed member names -> physical surviving original guild book current accession")!="UNRESOLVED":
        bad("old edition falsely relinked with original modern register")
    if byedge.get("1719 Neuhaus admission -> confessional denial under IPO V §35")!="NOT_PROVEN":
        bad("successful admission falsely promoted to religious-exclusion judgment")
    archive=d["archival_history"]
    if archive["historian"]!="Josef Ketteler" or archive["number_of_judicial_catalog_units_minimum"]!=8000 or archive["prior_schema"]!="Loculamenta":
        bad("university history of 8000 judicial catalog entries corrupted")
    if archive["archive_evacuated_year"]!=1942 or archive["archive_returned_year"]!=1953 or not archive["interim_city_archive_building"].startswith("Krameramtshaus"):
        bad("evacuation and return chronology malformed")
    if archive["never_claimed_same_kramergilde_book_located"] is not True:
        bad("judicial archive organization cannot prove specific guild-book survival")
    ch=d["access_channels"]
    if len(ch)!=3 or len({c["id"] for c in ch})!=3:
        bad("three separate archive access methods needed")
    statuses={c["id"]:c["status"] for c in ch}
    if (statuses.get("EA16-C-PUBLIC_SCAN"),statuses.get("EA16-C-ARCHIVE_PORTAL"),statuses.get("EA16-C-ARCHIVE_REQUEST"))!=(
      "BLOCKED_BY_WEB_READER","ENTRY_POINT_CONFIRMED_NOT_ITEM_LOCATED","CONTACT_VERIFIED_NOT_SENT"):
        bad("direct scan, archival item listing and contact verification are not the same")
    if len(d["editorial_limits"])<9:
        bad("the source uncertainty/publication safeguards are missing")
    text=(ROOT/ARTICLE).read_text(encoding="utf-8")
    if len(text)<5000 or text.count("\n## ")<6 or "DRAFT_RESEARCH_NOT_PUBLIC" not in text:
        bad("readable Korean analytic research chapter absent")
    for word in ("1719","1931년","270쪽","8,000","Loculamenta","1953","§35","직접 확인하지 못했다","미확인"):
        if word not in text:bad("substantive source boundary or finding missing: "+word)
    return {"sources":8,"reading_tasks":4,"provenance_edges":7,"publisher_scan_read":0,"individual_V35_case":0,"public":0}
if __name__=="__main__":
    x=validate()
    print("PASS VOL05 V1.6: 8 graded sources, 4 primary/edition checks, 7 provenance links; Ketteler p270 unread, 1719 original 0, PUBLIC 0")
