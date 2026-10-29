#!/usr/bin/env python3
"""Check V1.9 treaty-era Munich/Muenster women's schooling and conditional settlement source tiers."""
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_chorfrauen_1653_revers_v19.json"
PARENT="data/deep/vol05_muenster_1649_chorfrauen_guild_v18.json"
DOC="docs/01_CONTENT/VOL05/MUENSTER_CHORFRAUEN_1649_TO_1655_SETTLEMENT_V19.md"
GATE_KEYS={"historian_approved","APW_pages_237_238_read","Feb1649_folio5v_read",
"Mar1649_folio13v_read","Sept1649_compromise_original_read","July1653_Revers_original_read",
"year1655_purchase_deed_read","IPO_V35_individual_verdict_found","media_rights_cleared","publish"}
DATE_MAP={"ARRIVE":"1642","SCHOOL":"1644","MANDATE":"1647-04-08","FEB49":"1649-02-25",
"MAR49":"1649-03-03","SEP49":"1649-09-20","REVERS":"1653-07-04","HOUSE":"1655","EXPAND":"1661"}
def load(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def fail(s):raise ValueError(s)
def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_CHORFRAUEN_1653_REVERS_AND_1655_SETTLEMENT_AUDIT","DRAFT_RESEARCH_NOT_PUBLIC",
        "OV-E-024","OV-D-015"):fail("release identity or historic canonical IDs changed")
    if d["parent"]!=PARENT or d["new_canonical_ids"]!=0 or any(d[k] is not False for k in ("main_modified","overview_modified","ai_studio_modified")):
        fail("main, overview, AI app or parent lineage changed")
    p=load(PARENT)
    if p["canonical_event_id"]!=d["canonical_event_id"] or p["canonical_document_id"]!=d["canonical_document_id"]:
        fail("previous V1.8 historical document chain mismatch")
    if set(d["gates"])!=GATE_KEYS or any(d["gates"].values()):
        fail("unapproved publication, manuscript-reading or V35 claim")
    ss=d["sources"]
    if len(ss)!=9 or len({s["id"] for s in ss})!=9:fail("nine distinct tiers required")
    sources={x["id"]:x for x in ss}
    for s in ss:
        u=urlparse(s["url"])
        if u.scheme!="https" or not u.hostname or not s["tier"] or not s["scope"]:
            fail("broken provenance or insecure source")
        if any(s[k] is not False for k in ("original_1649_or_1653_read","printed_APW_page_read","image_rights_approved")):
            fail("original page and image status cannot be fabricated")
    if sources["KLOSTERBUCH"]["tier"]!="1994_MONASTERY_LEXICON_2024_SCAN_SEARCH_EXCERPT_ONLY":
        fail("1994 history digitalized 2024, PDF page not visually read")
    if sources["APW_SITE"]["tier"]!="DIRECT_ACCESS_DENIED_ANUBIS" or sources["OUP"]["tier"]!="PUBLISHER_BOOK_CHAPTER_ABSTRACT":
        fail("direct APW unverified or publisher excerpt overstated")
    if sources["MIRROR"]["tier"]!="UNOFFICIAL_TEXT_SEARCH_EXCERPT_ONLY":
        fail("1649 Sept20 must not be graded as authenticated book/primary source")
    ev=d["chronology"]
    if len(ev)!=9 or {x["id"] for x in ev}!=set(DATE_MAP):fail("precise nine-stage chronology needed")
    for x in ev:
        if x["date"]!=DATE_MAP[x["id"]] or x["original_record_read"] is not False or not x["description"]:
            fail("invented dates, unseen original or empty history")
    r=d["revers"]
    if (r["date"],r["sisters_cap"],r["source"])!=("1653-07-04",12,"KLOSTERBUCH"):
        fail("exact 1653 twelve-sister undertaking changed")
    if not all(r[x] is True for x in ("one_house_allowed","additional_land_restricted",
        "local_sisters_inheritance_waiver_reported","German_secular_confessor_reported",
        "papal_mendicant_order_condition_reported")):
        fail("important and non-contradictory conditional rights omitted")
    if r["contemporaneous_original_read"] is not False or r["archive_shelfmark"] is not None or r["identical_to_permanent_residence_act_proven"] is not False:
        fail("1653 reversal falsely treated as same original residence concession")
    e=d["edition"]
    if (e["editor"],e["year"],e["APW_series"],e["pages"],e["digital_access"])!=(
        "Helmut Lahrkamp",1964,"III D 1","237–238","ANUBIS_BLOCKED"):
        fail("APW printed critical edition bibliographic identity/access status changed")
    if e["original_city_folio"]!="A II 20 Bd.79 fol.5v" or e["APW_full_text_read"] is not False:
        fail("APW p237–238 has not been read nor manually collated with original fol5v")
    leads=d["original_leads"]
    if len(leads)!=5 or [x["date"] for x in leads]!=[
        "1649-02-25","1649-03-03","1647-04-08","1651-11-20","1653-07-04"]:
        fail("precise 1649/1651/1653 archival task dates lost")
    if any(x["original_read"] is not False for x in leads) or leads[4]["locator"] is not None:
        fail("1653 original signature unknown and no originals directly read")
    if len(d["legal_boundaries"])<8 or len(d["next_tasks"])!=5:
        fail("source limitation or next archival tasks suppressed")
    body=(ROOT/DOC).read_text(encoding="utf8")
    if len(body)<5500 or body.count("\n## ")<9 or "DRAFT_RESEARCH_NOT_PUBLIC" not in body:
        fail("substantive Korean reader narrative missing")
    for term in ("1653년 7월 4일","1655년","12명","Revers","APW III D 1","237~238","§35","미확인"):
        if term not in body:fail("essential documentary distinction missing from Korean manuscript: "+term)
    return {"sources":9,"events":9,"primary_leads":5,"APW_pages_direct_read":0,
            "individual_IPO_V35_cases":0,"public":0}
if __name__=="__main__":
    x=validate()
    print("PASS VOL05 V1.9: 9 sources, 9 historic stages, 5 archive leads, 1653 conditional Revers; original APW 0, V35 cases 0, PUBLIC 0")
