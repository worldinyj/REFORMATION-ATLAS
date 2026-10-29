#!/usr/bin/env python3
"""VOL05 V1.4: check a single old baker-guild paper booklet, dated additions, and legal boundaries.
No firsthand transcription of 1639, 1660, 1661 or 1681 originals.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_muenster_bakers_guild_1639_1661_v14.json"
PARENT="data/deep/vol05_muenster_guild_regulament_1681_elections_v13.json"
CHAPTER="docs/01_CONTENT/VOL05/MUENSTER_BAKERS_GUILD_1639_1660_TO_1661_V14.md"
DATES={"DOC1639":("1639-04-04","Nr. 1527","S1"),"DOC1661":("1661-08-22",None,"S2"),
       "DOC1681":("1681-10-10","AA II 0 fol. 96r (SECONDARY_CITATION_ONLY)","S4"),
       "DOC1718":("1718-02-18","Nr. 1861","S5")}
CLAIMS={"C1":("DOC1639","1639-04-04"),"C2":("DOC1639","1660-01-12"),
        "C3":("DOC1639","1660-01-18"),"C4":("DOC1639","1641-09-23"),
        "C5":("DOC1661","1661-08-22"),"C6":("DOC1681","1681-10-10"),
        "C7":("DOC1718","1718-02-18")}
GATES={"historian_approved","original_baker_book_read","original_1661_guild_regulament_found",
       "Bischof_1926_p22_read","AAII0_1681_folio_read",
       "individual_V35_case_proved","media_rights_approved","can_publish"}

def load(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def err(msg):raise ValueError(msg)

def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_BAKERS_GUILD_ARCHIVE_V14","DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        err("research identity or canonical ID altered")
    if d["parent"]!=PARENT or d["new_canonical_ids"]!=0 or d["overview_modified"] is not False or d["main_modified"] is not False or d["ai_studio_modified"] is not False:
        err("main/overview/app invariant or parent violated")
    if set(d["gate"])!=GATES or any(d["gate"].values()):
        err("unapproved manuscript, scholarship, rights or publish gate")
    par=load(PARENT)
    if par["canonical_event_id"]!=d["canonical_event_id"] or par["canonical_document_id"]!=d["canonical_document_id"]:
        err("prior regional research disconnected")
    src=d["sources"]
    if len(src)!=9 or len({x["key"] for x in src})!=9:
        err("nine distinct evidence links needed")
    sources={x["key"]:x for x in src}
    for s in src:
        u=urlparse(s["url"])
        if u.scheme!="https" or not u.hostname or not s["evidence_tier"] or not s["scope"]:
            err("evidence source description/URL invalid")
        if s["original_document_read"] is not False or s["media_rights_approved"] is not False:
            err("primary reading or image rights fabricated")
    if "112746" not in sources["S1"]["url"] or "113079" not in sources["S5"]["url"]:
        err("wrong archival regest items")
    if "PADERBORN" not in sources["S3"]["evidence_tier"] and "BIBLIOGRAPHY" not in sources["S3"]["evidence_tier"]:
        err("Bischof bibliography not original 1926 reading")
    docs=d["documents"]
    if len(docs)!=4 or {x["key"] for x in docs}!=set(DATES):
        err("four distinct source units required")
    document={x["key"]:x for x in docs}
    for x in docs:
        if (x["date"],x["shelfmark"],x["source_key"])!=DATES[x["key"]]:
            err("dated source witness conflated or invented shelfmark")
        if x["firsthand_original_read"] is not False or x["individual_V35_suit_confirmed"] is not False:
            err("original not read or V35 litigation not found")
    if document["DOC1639"]["witness_type"]!="ONE_PAPER_BOOKLET_WITH_1660_ADDITIONS":
        err("one 1639 book with 1660 additions cannot become three originals")
    if document["DOC1661"]["witness_type"]!="ORIGINAL_GUILD_NORM_NOT_LOCATED":
        err("1661 guild rule original location still unknown")
    if document["DOC1718"]["witness_type"]!="LATER_1790_APPEAL_CONTEXT_INCLUDED":
        err("1718 issuance and 1790 appeal copy conflated")
    claims=d["claims"]
    if len(claims)!=7 or {x["key"] for x in claims}!=set(CLAIMS):
        err("exact seven dated historical claims required")
    for x in claims:
        if (x["document_key"],x["date"])!=CLAIMS[x["key"]]:
            err("unverified or chronologically wrong claim")
        if x["original_text_read"] is not False or x["IPO_V35_enforcement_proved"] is not False or not x["claim"]:
            err("claim false promotion to original reading or V35 judgment")
    claim={x["key"]:x["claim"] for x in claims}
    for key,word in [("C1","33"),("C2","600 Reichstaler"),("C3","1660"),("C4","Bernd Beckmann"),("C5","1661"),("C6","fol96r"),("C7","1790")]:
        if word not in claim[key]:
            err("source detail removed: "+key)
    b=d["bibliography"]
    if (b["author"],b["year"],b["pages"],b["scholarly_quote_location"])!=(
       "Franz Bischof",1926,82,"p.22, cited by Deter 1999 note 126"):
        err("Bischof 1926 reference lost")
    if b["book_1926_read"] is not False or b["original_1661_archival_signature"] is not None:
        err("Bischof original page or underlying seventeenth-century shelfmark invented")
    if d["grouping"]["nr1527_physical_booklets"]!=1 or d["grouping"]["appendix_dates"]!=["1660-01-12","1660-01-18"]:
        err("one physical guild rule booklet has precisely two identified 1660 later decisions")
    if d["grouping"]["NOT_PROOF_OF_1648_V35_APPLICATION"] is not True:
        err("prewar guild rules are not private V35 judgment")
    if len(d["uncertainties"])<9:
        err("archival/rights uncertainty deleted")
    chapter=(ROOT/CHAPTER).read_text(encoding="utf-8")
    if len(chapter)<6200 or chapter.count("\n## ")<8 or "DRAFT_RESEARCH_NOT_PUBLIC" not in chapter:
        err("Korean readable regional research chapter absent")
    for word in ["Nr.1527","600제국탈러","1660년 1월 12일","1660년 1월 18일","1661년 8월 22일","Nr.1861","비쇼프","fol.96r","§35","미확인"]:
        if word not in chapter:
            err("historical fact/provenance caution missing from narrative: "+word)
    return {"sources":9,"distinct_documents":4,"booklets1639_1660":1,"dated_claims":7,"verified_V35_personal_cases":0,"public":0}
if __name__=="__main__":
    x=validate()
    print("PASS VOL05 V1.4: 9 links, 4 source units, one 1639 paper booklet, 7 dated claims, individual IPO V35 cases 0, PUBLIC 0")
