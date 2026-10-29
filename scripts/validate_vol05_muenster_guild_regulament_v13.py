#!/usr/bin/env python3
"""V1.3 documentary provenance: catalog and published scholarship only, not original folio proof."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_muenster_guild_regulament_1681_elections_v13.json"
PARENT="data/deep/vol05_muenster_1648_1681_governance_v12.json"
DOC="docs/01_CONTENT/VOL05/MUENSTER_1661_GUILD_REGULAMENT_1681_ELECTIONS_V13.md"
GATE_KEYS={"historian_signed_off","original_1661_guild_regulament_read",
"original_1681_council_edict_read","modern_1926_Bischof_original_read",
"post_1648_individual_v35_case_verified","artwork_rights_cleared","can_publish"}
DATES={"VG13-E1536":"1536","VG13-E1553":"1553","VG13-E1661C":"1661-01-18",
"VG13-E1661R":"1661-08-22","VG13-E1681":"1681-10-10","VG13-E1690":"1690-08-30",
"VG13-E1731":"1731-08-14","VG13-E1732":"1732-01-04"}
WITNESS_DATES={"VG13-W1661G":"1661-08-22","VG13-W1661CR":"1661-01-18",
"VG13-W1681E":"1681-10-10","VG13-W1661D":"1661-08-18"}
LEGAL_KEYS={"VG13-G-NOPOLITICS","VG13-G-PERMISSION","VG13-G-OATH",
"VG13-G-BOOKS","VG13-G-SURVIVAL","VG13-ELECT-REVOCABLE"}
def read(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
def err(msg):raise ValueError(msg)
def validate(d=None):
    d=read(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_MUENSTER_GUILD_1661_REGULAMENT_AND_1681_ELECTION_SOURCES",
        "DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        err("wrong provisional historical document identity")
    if d["parent_registry"]!=PARENT or d["new_canonical_ids"]!=0 or d["main_modified"] is not False or d["ai_studio_modified"] is not False:
        err("release boundary or research lineage changed")
    if set(d["release_gate"])!=GATE_KEYS or any(d["release_gate"].values()):
        err("unapproved original, historical scholar, V35 or media publication gate")
    p=read(PARENT)
    if p["event_id"]!=d["canonical_event_id"] or p["document_id"]!=d["canonical_document_id"]:
        err("previous verified canonical linkage missing")
    src=d["sources"]
    if len(src)!=8 or len({x["key"] for x in src})!=8:
        err("eight source records required")
    s={x["key"]:x for x in src}
    for x in src:
        url=urlparse(x["url"])
        if url.scheme!="https" or not url.hostname or not x["kind"] or not x["access_level"] or not x["claim_scope"]:
            err("untrusted historical source")
        if x["primary_1661_or_1681_manuscript_read"] is not False or x["cleared_for_image_reuse"] is not False or x["approved_public_content"] is not False:
            err("false manuscript or publishing claim")
    if s["V13-S01"]["kind"]!="DETER_1999_FULL_HTML_LEGAL_HISTORY" or s["V13-S02"]["access_level"]!="SEARCHABLE_PDF_TEXT_READ_SCREENSHOT_CACHE_MISS":
        err("direct open Deter vs unverified Weidner screenshot source tiers swapped")
    if s["V13-S03"]["kind"]!="MUENSTER_CITY_MUSEUM_EXHIBIT":
        err("independent official museum evidence lost")
    rows=d["chronology"]
    if len(rows)!=8 or {x["key"] for x in rows}!=set(DATES):
        err("the 1536–1732 historical periods are distinct")
    for x in rows:
        if x["date"]!=DATES[x["key"]] or x["source_key"] not in s or x["actual_dated_primary_text_read"] is not False:
            err("false event date, orphan source or original read")
        if not x["claim"] or not x["classification"]:
            err("history lacks interpretation and evidence class")
    w=d["primary_witness_leads"]
    if len(w)!=4 or {x["key"] for x in w}!=set(WITNESS_DATES):
        err("four original investigation leads required")
    ww={x["key"]:x for x in w}
    for x in w:
        if x["act_date"]!=WITNESS_DATES[x["key"]] or x["source_key"] not in s:
            err("original witness act date/source changed")
        if x["original_firsthand_transcription"] is not False or x["full_regulation_read"] is not False:
            err("unread historical manuscript falsely collated")
        if not x["provenance"] or not x["label"]:
            err("unidentified source lineage")
    if ww["VG13-W1661G"]["actual_17th_century_archive_shelfmark"] is not None or ww["VG13-W1661G"]["secondhand_original_excerpt"] is not True:
        err("1661-08-22 original signature unknown; Deter excerpt via Bischof")
    if "Franz Bischof 1926 p22" not in ww["VG13-W1661G"]["provenance"]:
        err("indirect quotation not tracked")
    if "92v/93r" not in ww["VG13-W1661CR"]["label"] or "96r" not in ww["VG13-W1681E"]["label"]:
        err("Ratswahlbuch 1661/1681 folios conflated")
    if ww["VG13-W1661D"]["actual_17th_century_archive_shelfmark"]!="MLA 413–4 (cited draft only)":
        err("1661-08-18 council draft mistakenly called 1661-08-22 guild norm")
    effects=d["legal_effects"]
    if len(effects)!=6 or {x["key"] for x in effects}!=LEGAL_KEYS:
        err("six distinct effects required")
    for x in effects:
        if x["source_key"] not in s or x["direct_original_confirmation"] is not False:
            err("guild controls or revocable election falsely original-verified")
    if "1661-08-22" not in next(x["instrument"] for x in effects if x["key"]=="VG13-G-NOPOLITICS"):
        err("guild and council regulations have distinct act dates")
    if "1690-08-30" not in next(x["instrument"] for x in effects if x["key"]=="VG13-G-SURVIVAL"):
        err("1690 jurisdiction cannot be 1661 guild rule")
    if "1681-10-10" not in next(x["instrument"] for x in effects if x["key"]=="VG13-ELECT-REVOCABLE"):
        err("revocable elections must be 1681")
    check=d["independent_check"]
    if check["source_key"]!="V13-S03" or check["confirm_1681_council_elections"] is not True or check["confirm_continued_princely_supervision"] is not True or check["confirm_exact_1681_folio"] is not False or check["confirm_full_1661_guild_law"] is not False:
        err("city museum confirms conditional institution but not Weidner folio or full guild law")
    if not d["historical_legal_boundary"].startswith("Political control of corporate guilds"):
        err("IPO V35 individual claim illegally replaced with corporate rule")
    if len(d["unresolved"])<7:
        err("original text/rights caveats deleted")
    text=(ROOT/DOC).read_text(encoding="utf8")
    if len(text)<6500 or text.count("\n## ")<9 or "DRAFT_RESEARCH_NOT_PUBLIC" not in text:
        err("reader Korean chapter incomplete")
    for term in ("1661년 8월 22일","1681년 10월 10일","1690년 8월 30일",
        "1926년","MLA 413–4","fol.96r","fol.92v/93r","§35","미확인"):
        if term not in text:err("missing essential critical fact: "+term)
    return {"source_count":8,"events":8,"witness_leads":4,"distinct_legal_effects":6,"verified_individual_v35":0,"public":0}

if __name__=="__main__":
    t=validate()
    print("PASS VOL05 V1.3: 8 scholarly sources, 8 chronological anchors, 4 folio/document leads, 6 legal functions, IPO V35 individual cases 0, PUBLIC 0")
