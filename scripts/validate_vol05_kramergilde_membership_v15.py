#!/usr/bin/env python3
"""VOL05 Kramergilde published-source and admission workflow scholarly guard V1.5.
No published 1931 article folios or original guild admission book viewed in this research.
"""
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_kramergilde_membership_1662_1797_v15.json"
PARENT="data/deep/vol05_muenster_bakers_guild_1639_1661_v14.json"
ARTICLE="docs/01_CONTENT/VOL05/MUENSTER_KRAMERGILDE_1662_1797_MEMBERSHIP_V15.md"
GATES={"historian_approved","ketteler_1931_article_pages_read","original_kramergilde_member_book_read",
       "anton_neuhaus_original_admission_read","confessional_exclusion_individual_verdict_verified",
       "visual_reuse_rights_approved","can_publish"}
YEARS={"K15-T-1589":"1589","K15-T-1648":"1648","K15-T-1662":"1662","K15-T-1670":"1670",
       "K15-T-1719":"1719","K15-T-1777":"1777","K15-T-1797":"1797",
       "K15-T-1810":"1810-02-20","K15-T-1823":"1823-06-12","K15-T-1824":"1824-04-12"}
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def bad(why):raise ValueError(why)
def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_MUENSTER_KRAMERGILDE_ADMISSIONS_1662_1797_CROSSWALK","DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        bad("incorrect research register or canonical IDs")
    if d["parent_registry"]!=PARENT or d["new_canonical_ids"]!=0 or d["main_modified"] is not False or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        bad("main, overview, app or parent lineage corrupted")
    if set(d["publication_gate"])!=GATES or any(d["publication_gate"].values()):
        bad("scholar, manuscript reading, rights, legal proof or release prematurely asserted")
    parent=load(PARENT)
    if parent["canonical_event_id"]!=d["canonical_event_id"] or parent["canonical_document_id"]!=d["canonical_document_id"]:
        bad("parent volume crosslink broken")
    ss=d["sources"]
    if len(ss)!=8 or len({x["id"] for x in ss})!=8:
        bad("8 independent source descriptions required")
    sources={s["id"]:s for s in ss}
    for s in ss:
        u=urlparse(s["url"])
        if u.scheme!="https" or not u.hostname or not s["kind"] or not s["access"] or not s["claim_scope"]:
            bad("unverified source or access evidence")
        if any(s[k] is not False for k in ("original_guild_admissions_register_read","full_ketteler_1931_pages_read",
                    "source_image_reuse_cleared","public_content_approved")):
            bad("secondary citation falsely treated as original full text or licensed media")
    if sources["K15-S06"]["access"]!="OFFICIAL_BIBLIOGRAPHY_SAYS_ONLINE_BUT_WEB_OPEN_ACCESS_FAILED":
        bad("Archive.org viewer not successfully opened")
    b=d["bibliographic_correction"]
    if (b["author"],b["year"],b["start_year"],b["end_year"],b["erroneous_prior_end_year"],
        b["pages_start"],b["pages_end"])!=("Josef Ketteler",1931,1662,1797,1779,253,295):
        bad("Ketteler official 1662–1797 chronology and pagination corrupted")
    if b["full_scanned_article_text_directly_read"] is not False or b["direct_1931_article_person_level_transcription"] is not False:
        bad("1931 full article not read by image or downloaded")
    if b["official_bibliography_source"]!="K15-S01" or "K15-S06"!=b["full_scanned_volume_4_source"]:
        bad("official bibliographic source/digital viewer crosswalk wrong")
    p=d["individual_candidates"]
    if len(p)!=1 or p[0]["research_id"]!="K15-P-1719-NEUHAUS":
        bad("one specific 1719 successful admission registered")
    n=p[0]
    if (n["name"],n["admission_year"],n["admission_day"],n["admission_mode_original_reported"],n["source_page_in_ketteler"])!=(
        "Anton Reinhard Neuhaus",1719,None,"Amtsohn",270):
        bad("1719 enrolled Neuhaus person or Ketteler page altered")
    if n["religious_confession"]!="UNKNOWN" or n["religious_exclusion_claim"] is not False or n["IPO_article_V35_invoked"] is not False:
        bad("religion, denial or V35 legal right fabricated from accepted guild member")
    if n["original_1719_entry_read"] is not False or n["original_shelfmark"] is not None or n["bio_person_identity_still_to_compare"] is not True:
        bad("unverified original 1719 admission or workplace identification")
    if n["source_ids"]!=["K15-S03"] or "Ketteler 1931 p270" not in n["supporting_publication"]:
        bad("academy's explicit secondary source chain lost")
    admin=d["administrative_process"]
    if admin["citizen_oath_before_guild_membership"]!="REPORTED_AS_REQUIRED_BY_GIMPEL_1982" or admin["guild_vs_treasury_register_timing_gap_years_max_reported"]!=2:
        bad("civic oath and lag documentation changed")
    if admin["underlying_treasury_series_cited"]!="StdAM, A VIII, 277 (Kämmereirechnungen in Gimpel's note 6)":
        bad("false treasury archive locator")
    if admin["year_1777_eight_neukramer"].startswith("Gimpel reports eight") is False:
        bad("eight 1777 merchant records not total individual admissions")
    if admin["oath_admission_procedure_direct_read"] is not False:
        bad("citizenship oath original not directly read")
    t=d["chronology"]
    if len(t)!=10 or {x["key"] for x in t}!=set(YEARS):
        bad("ten separate guild, treaty and property chronology points required")
    for x in t:
        if x["date"]!=YEARS[x["key"]] or x["source_id"] not in sources or x["primary_contemporary_text_read"] is not False:
            bad("incorrect historical date/source or read original claim")
    house=d["guild_house"]
    if (house["original_construction_year"],house["abolition_date"],house["number_members_1810_from_1823_list"],
        house["final_community_meeting"],house["building_sale"])!=(1589,"1810-02-20",142,"1823-06-12","1824-04-12"):
        bad("guild house year, retrospective count, or dissolution and property events mixed")
    if house["media_assets_downloaded"]!=0 or house["visual_copyright_approved"] is not False:
        bad("rights-free historic photo reuse assumed")
    if d["research_schema_proposal"]["grain"]!="ONE_PERSON_ONE_ADMISSION_ENTRY_WITH_SOURCE_RECORD_ID":
        bad("future extraction must separate person and source")
    if len(d["research_schema_proposal"]["prohibited_inferences"])<7:
        bad("individual-denial, religion and registry-lag safeguards missing")
    follows=d["original_investigations"]
    if len(follows)!=5 or {x["key"] for x in follows}!={"K15-N1","K15-N2","K15-N3","K15-N4","K15-N5"}:
        bad("precise followup investigations required")
    if len(d["editorial_holds"])<9:
        bad("critical rights and archival access limitations erased")
    report=(ROOT/ARTICLE).read_text(encoding="utf-8")
    if len(report)<6500 or report.count("\n## ")<9 or "DRAFT_RESEARCH_NOT_PUBLIC" not in report:
        bad("substantive Korean member-history narrative absent")
    for token in ("1797","1779","1719","Neuhaus","Amtsohn","270쪽","1810","1823","1824","§35","미확인"):
        if token not in report:bad("essential membership/source qualification missing: "+token)
    return {"sources":8,"named_member_entries":1,"chronology":10,"followups":5,"original_guild_book_read":0,"individual_V35_rulings":0,"public":0}
if __name__=="__main__":
    x=validate()
    print("PASS VOL05 V1.5: 8 sources, Ketteler 1662–1797, 1 named 1719 admitted member, 10 separate chronology dates, original folio 0, PUBLIC 0")
