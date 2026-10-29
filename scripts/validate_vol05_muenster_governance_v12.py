#!/usr/bin/env python3
"""Validate VOL05 V1.2 researched Münster civic governance, not original manuscript text."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_muenster_1648_1681_governance_v12.json"
PREV="data/deep/vol05_muenster_archival_fonds_crosswalk_v11.json"
REPORT="docs/01_CONTENT/VOL05/MUENSTER_1648_1681_GUILDS_AND_CIVIC_GOVERNANCE_V12.md"
TIMES={"T1657":"1657-10-21","T1661S":"1661-03-26","T1661A":"1661-08-13",
"T1661B":"1661-08-18","T1661C":"1661-08-19","T1661G":"1661",
"T1677":"1677-05-15","T1681":"1681-10-10"}
ARCHIVES={"A":("MLA 413–4","1661-08-18 administrative council draft"),
"B":("MLA 413–5, fol.126r–128r","1661 town judge rule"),
"C":("AA II 23, RP 19.08.1661 (Vorform)","1661 council replacement"),
"D":("AA II 0, fol.96r","1681 council election edict")}
GATES={"historian_approved","original_manuscripts_read","individual_V35_case_proven",
"media_reuse_approved","publication_approved"}
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def bad(msg):raise ValueError(msg)

def validate(d=None):
    d=read(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["event_id"],d["document_id"])!=(
        "VOL05_MUENSTER_GUILD_AND_ELECTION_TIMELINE","DRAFT_RESEARCH_NOT_PUBLIC",
        "VOL-05","OV-E-024","OV-D-015"):
        bad("wrong research type or canonical work")
    if d["parent"]!=PREV or d["new_canonical_ids"]!=0 or d["main_modified"] is not False or d["ai_studio_modified"] is not False:
        bad("unauthorized main / app / canonical modification")
    g={key:d[key] for key in GATES}
    if any(g.values()):
        bad("human scholarship, media or publication flag must remain false")
    if d["primary_originals_read"] is not False or d["individual_V35_case_proven"] is not False or d["media_used_in_app"] is not False:
        bad("catalog and secondary notes do not prove originals or V35 enforcement")
    parent=read(PREV)
    if parent["canonical_event_id"]!=d["event_id"] or parent["canonical_document_id"]!=d["document_id"]:
        bad("historical parent chain mismatch")
    t=d["timeline"]
    if len(t)!=len(TIMES) or {x["key"] for x in t}!=set(TIMES):
        bad("eight exact historical phases needed")
    for x in t:
        if x["date"]!=TIMES[x["key"]] or x["contemporaneous_manuscript_read"] is not False or not x["evidence"]:
            bad("date incorrect, manuscript falsely read or source kind omitted")
    if next(x["label"] for x in t if x["key"]=="T1677")!="Greiteke Brinkmans citizenship admitted":
        bad("1677 positive admission cannot be converted to a rejection")
    for id,term in (("T1657","first siege"),("T1661S","second siege"),
                    ("T1661G","Gesamtgilde"),("T1677","Greiteke"),("T1681","conditional")):
        if term not in next(x["label"] for x in t if x["key"]==id):
            bad("critical history distinction erased")
    targets=d["archival_locators"]
    if len(targets)!=4 or {x["key"] for x in targets}!=set(ARCHIVES):
        bad("four precise original location leads required")
    for x in targets:
        if (x["locator"],x["use"])!=ARCHIVES[x["key"]]:
            bad("manuscript draft/judge/council/election locations conflated")
        if x["original_text_read"] is not False or x["modern_shelfmark_confirmed"] is not False:
            bad("publication-grade archive original falsely examined")
    urls=d["source_urls"]
    if len(urls)!=6 or len(set(urls))!=6:
        bad("six distinct evidence source URLs required")
    for url in urls:
        p=urlparse(url)
        if p.scheme!="https" or not p.hostname:
            bad("bad provenance URL")
    if "txt1213.pdf" not in urls[0] or "beitrwff-9745.pdf" not in urls[1]:
        bad("independent academic sources lost")
    if "241308" not in urls[2] or "77030" not in urls[3] or "2016645785" not in urls[4]:
        bad("distinct visual item/source identities changed")
    if len(d["unresolved"])<5:
        bad("limits hidden")
    if not any("V35" in v for v in d["unresolved"]):
        bad("explicit Article V35 nonproof missing")
    narrative=(ROOT/REPORT).read_text(encoding="utf-8")
    if len(narrative)<6500 or narrative.count("\n## ")<8 or "DRAFT_RESEARCH_NOT_PUBLIC" not in narrative:
        bad("detailed Korean regional narrative incomplete")
    for term in ("§35","1657","1661","1677","1681","MLA 413–4","MLA 413–5",
            "AA II 23","AA II 0","길드","시민권","미확인"):
        if term not in narrative:
            bad("critical evidence or context missing: "+term)
    return {"phases":8,"archival_leads":4,"source_urls":6,"verified_v35_judgments":0,"public":0}

if __name__=="__main__":
    s=validate()
    print("PASS VOL05 V1.2: 8 civic timeline phases, 4 archived folio leads, 6 source URLs, V35 lawsuits 0, PUBLIC 0")
