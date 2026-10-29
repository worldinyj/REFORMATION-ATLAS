#!/usr/bin/env python3
"""1649 Münster canonesses versus civic guild: cited council folios, not directly read originals."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_muenster_1649_chorfrauen_guild_v18.json"
PARENT="data/deep/vol05_kramergilde_three_people_v17.json"
STORY="docs/01_CONTENT/VOL05/MUENSTER_1649_CHORFRAUEN_GUILD_AUTONOMY_V18.md"
GATES={"historian_review","council_1649_feb_original_read","guild_1649_mar_original_read",
"episcopal_1647_mandate_original_read","APW_III_D1_pages_original_read",
"red_book_original_read","individual_IPO_V35_lawsuit_confirmed",
"visual_rights_cleared","public_approved"}
LOC={
"FEB25":("1649-02-25","Stadtarchiv Münster A II 20 Bd. 79 fol. 5v"),
"MAR03":("1649-03-03","Stadtarchiv Münster A II 20 Bd. 79 fol. 13v"),
"MANDATE":("1647-04-08","Stadtarchiv Münster A VIII 226, Beilage"),
"RED_BOOK":("1410/1565","Stadtarchiv Münster A XI 53")}
EV={
"E1643":"1643","E1647":"1647-04-08","E1648":"1648-10-24",
"E1649FEB":"1649-02-25","E1649MAR":"1649-03-03",
"E1649AUT":"1649-autumn","E1661":"1661-08-22"}
POSITIONS={
"City council":("1649-02-25","CONDITIONAL_POSSIBLE_SETTLEMENT"),
"Gesamtgilde":("1649-03-03","REJECTED_SETTLEMENT_AND_CIVIC_TAX_EXEMPTION"),
"Fabio Chigi and Alvise Contarini":("1649","SUPPORTED_CANONESSES_RELOCATION"),
"Prince Bishop Ferdinand":("1647-04-08","ISSUED_EARLIER_APPROVAL_MANDATE")}
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def error(msg):raise ValueError(msg)

def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_MUENSTER_1649_CANONESSES_GUILD_AUTONOMY_CASE",
        "DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        error("research and canonical reference identity changed")
    if d["parent"]!=PARENT or d["new_canonical_ids"]!=0 or d["main_modified"] is not False or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        error("unapproved production release, canonical ID or parent changed")
    if set(d["gates"])!=GATES or any(d["gates"].values()):
        error("originals, scholarly verification, legal lawsuit or release prematurely approved")
    parent=load(PARENT)
    if parent["canonical_event_id"]!=d["canonical_event_id"] or parent["canonical_document_id"]!=d["canonical_document_id"]:
        error("staged parent research inconsistent")
    src=d["sources"]
    if len(src)!=8 or len({x["id"] for x in src})!=8:
        error("eight independent graded source records mandatory")
    sources={s["id"]:s for s in src}
    if sources["JAKOBI1998"]["tier"]!="FULL_PUBLISHED_SCHOLARLY_HTML_READ":
        error("Jakobi 1998 web HTML was read, but archival original was not")
    if sources["OUP_CHAPTER"]["tier"]!="ABSTRACT_ONLY_MODERN_BOOK_FULL_CHAPTER_UNREAD":
        error("2014 academic monograph has not been completely read")
    for s in src:
        url=urlparse(s["url"])
        if url.scheme!="https" or not url.hostname or not s["tier"]:
            error("invalid research URL or evidence level")
        if s["original_17c_document_read"] is not False or s["media_rights_approved"] is not False:
            error("source image or seventeenth century folio falsely read or licensed")
    fol=d["folios"]
    if len(fol)!=4 or {x["key"] for x in fol}!=set(LOC):
        error("four city archive leads are individually required")
    for f in fol:
        if (f["date"],f["scholar_locator"])!=LOC[f["key"]]:
            error("1649 guild/council folio and 1647 mandate locations must be exact")
        if f["original_read"] is not False or f["current_item_signature_confirmed"] is not False or f["critical_edition_directly_read"] is not False:
            error("old scholarly locator is not verified original or modern accession")
    feb=next(f for f in fol if f["key"]=="FEB25")
    if feb["edition"]!="APW III D 1, pp. 237–238 (Lahrkamp, not read)":
        error("APW III D1 edition not directly read and citation lost")
    dates=d["events"]
    if len(dates)!=7 or {x["id"] for x in dates}!=set(EV):
        error("historical dated sequence incomplete")
    for x in dates:
        if x["date"]!=EV[x["id"]] or x["dated_original_folio_read"] is not False or not x["summary"]:
            error("wrong date or fabricated original record")
    parties=d["positions"]
    if len(parties)!=4 or {x["actor"] for x in parties}!=set(POSITIONS):
        error("council/guild/mediators/episcopal positions must remain separate")
    for x in parties:
        if (x["date"],x["position"])!=POSITIONS[x["actor"]] or x["source"]!="JAKOBI1998" or x["original_read"] is not False:
            error("conflated 1649 actors or historical position")
    widows=d["guild_house_widow_participation"]
    if (widows["inauguration"],widows["guild_members_present"],widows["widows_of_masters_present"])!=(
        "1589-11-12",82,24):
        error("1589 guild-house attendance and widows historical count changed")
    if widows["independent_member_rights_proven"] is not False or widows["does_not_confirm_Maria_Schuerman_1670_membership"] is not True:
        error("widows at 1589 festival are not proven independent guild members")
    law=d["legal_distinctions"]
    if len(law)!=4 or {x["key"] for x in law}!={"LOCAL_GOV","IPO_V35","TEMP_CITY","GUILD1661"}:
        error("separate municipal consent, private right, neutrality and later guild rule")
    for l in law:
        if l["individual_IPO_V35_case"] is not False:
            error("religious personal litigation not proved")
        if l["verified_as_regional_governance_case"] is not (l["key"]=="LOCAL_GOV"):
            error("guild consent proves local governance not a V35 verdict")
    if len(d["caveats"])<8 or len(d["next_original_work"])!=5:
        error("critical contextual limits or archival followups removed")
    md=(ROOT/STORY).read_text(encoding="utf-8")
    if len(md)<6000 or md.count("\n## ")<8 or "DRAFT_RESEARCH_NOT_PUBLIC" not in md:
        error("full Korean historical context article missing")
    for term in ("1649년 2월 25일","1649년 3월 3일","A II 20","fol. 5v","fol. 13v","A XI 53","A VIII 226","APW III D 1","82명","24명","§35","미확인"):
        if term not in md:error("research evidence or responsible caution missing: "+term)
    return {"sources":8,"dated_events":7,"exact_folio_leads":4,"positions":4,
            "original_photographs_read":0,"individual_V35_cases":0,"published":0}
if __name__=="__main__":
    x=validate()
    print("PASS VOL05 V1.8: 8 sources, 7 history events, 4 specific original-folio leads, 4 civic actor positions, IPO V35 individual judgments 0, PUBLIC 0")
