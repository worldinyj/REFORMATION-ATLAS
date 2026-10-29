#!/usr/bin/env python3
"""Münster 1661 MLA acronym and 1677 Bürgerbrief provenance V1.1.

Catalog and academic notes are not a seventeenth-century primary collation.
Fail closed on unknown individual item, physical identity and publication rights.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_muenster_archival_fonds_crosswalk_v11.json"
PREV="data/deep/vol05_muenster_citizenship_1677_v10.json"
DOC="docs/01_CONTENT/VOL05/MUENSTER_1661_1677_ARCHIVE_MLA_ZUMBUSCH_V11.md"
GATES={"historian_approved","MLA_original_folio_read","Urkunden_1626_copy_read",
       "original_1677_letter_located_currently","original_1677_letter_read",
       "V35_individual_case_proven","images_rights_cleared","can_publish"}
IDS={"M11-A-MLA","M11-A-4135","M11-A-ZUMB-HISTORIC","M11-A-ZUMB-MODERN"}
LINKS={("MLA 413–5 fol. 126r–128r","Verein Urkunden Nr. 1626"),
("1982 Zumbusch unlisted letter","modern C-Arm Zumbusch collection"),
("AA II Nr23 1661-08-19 council record","MLA 413–5 judge regulation")}
TASKS={"M11-F-LETTER","M11-F-MLA","M11-F-COUNCIL"}

def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def fail(reason): raise ValueError(reason)

def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
       "VOL05_MUENSTER_MLA_AND_1677_LETTER_CROSSWALK","DRAFT_RESEARCH_NOT_PUBLIC",
       "VOL-05","OV-E-024","OV-D-015"):
        fail("draft research identity or canonical work changed")
    if d["parent_registry"]!=PREV or d["new_canonical_ids"]!=0 or d["main_modified"] is not False or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        fail("main/overview/AI Studio identity and source lineage must remain unchanged")
    if set(d["publication_gate"])!=GATES or any(d["publication_gate"].values()):
        fail("original, V35, historian, image or publication approved without evidence")
    parent=load(PREV)
    if parent["canonical_document_id"]!=d["canonical_document_id"] or parent["canonical_event_id"]!=d["canonical_event_id"]:
        fail("previous V1.0 study missing")
    src=d["sources"]
    if len(src)!=12 or len({s["id"] for s in src})!=12:
        fail("need 12 unique source records")
    ss={}
    for s in src:
        u=urlparse(s["url"])
        if not s["id"].startswith("M11-S") or u.scheme!="https" or not u.hostname:
            fail("insecure/invalid source URL")
        if not s["kind"] or not s["access"] or not s["scope"]:
            fail("source access tier missing")
        if any(s[x] is not False for x in ("original_physical_document_read","complete_PDF_visual_verified",
                  "redistribution_rights_cleared","public_approved")):
            fail("secondary or catalog source prematurely claimed original/release")
        ss[s["id"]]=s
    if ss["M11-S05"]["access"]!="SEARCH_EXCERPTS_BIG_PDF_UNAVAILABLE":
        fail("Gimpel PDF is still inaccessible as complete page")
    if ss["M11-S06"]["kind"]!="DDB_MUENSTER_MODERN_FONDS" or ss["M11-S07"]["kind"]!="DDB_MUENSTER_MODERN_FONDS":
        fail("current fonds confirmation lost")
    x=d["archive_links"]
    if len(x)!=4 or {r["key"] for r in x}!=IDS:
        fail("four documentary/archival crosslinks required")
    ids={r["key"]:r for r in x}
    for r in x:
        if not r["source_ids"] or not set(r["source_ids"])<=set(ss):
            fail("archival hypothesis missing evidence")
    mla=ids["M11-A-MLA"]
    if mla["expanded"]!="Münstersches Landesarchiv" or mla["abbreviation_resolved"] is not True or mla["original_folio_read"] is not False:
        fail("MLA abbreviation must be resolved without manuscript read")
    ref=ids["M11-A-4135"]
    if ref["label"]!="MLA 413–5 fol. 126r–128r" or ref["witness_directly_read"] is not False or ref["identical_to_LWL1626"]!="UNRESOLVED":
        fail("MLA primary and later copy identity not verified")
    g=ids["M11-A-ZUMB-HISTORIC"]
    if (g["label"],g["year_referred"],g["old_catalog_state"])!=(
        "StdAM, Stiftungsarchiv Armenhaus Zumbusch unverzeichnet",1982,"UNLISTED_AT_PUBLICATION"):
        fail("Gimpel footnote 16 lost or historically misdated")
    if g["current_individual_shelfmark"] is not None or g["original_relocated_or_recataloged"]!="UNKNOWN":
        fail("specific 1677 letter has no confirmed current archival identifier")
    modern=ids["M11-A-ZUMB-MODERN"]
    if modern["label"]!="C-Arm Zumbusch / Armenhaus Zumbusch-Üding" or modern["archive"]!="Stadtarchiv Münster":
        fail("modern fonds identification wrong")
    if modern["specific_1677_letter_in_modern_catalog"]!="NOT_FOUND" or len(modern["examples"])!=2:
        fail("modern fonds does not identify the 1677 Bürgerbrief")
    ex={v["key"]:v for v in modern["examples"]}
    if set(ex)!={"Akten Nr. 28","Urk. Nr. 37"} or ex["Akten Nr. 28"]["date"]!="1661–1670" or ex["Urk. Nr. 37"]["date"]!="1412":
        fail("source examples incorrectly matched")
    if any(v["is_1677_letter"] is not False for v in modern["examples"]):
        fail("unrelated fonds example falsely merged into 1677 letter")
    letter=d["letter_metadata"]
    if (letter["person"],letter["date"],letter["location_1982"])!=(
        "Greiteke Brinkmans","1677-05-15",g["label"]):
        fail("named successful civic admission or old location mismatch")
    if letter["current_shelfmark"] is not None or letter["physical_original_read"] is not False or letter["manuscript_page_image_verified"] is not False:
        fail("original letter sighting/shelfmark fabricated")
    if letter["secondary_claim_only"] is not True or letter["unlawful_citizenship_denial_established"] is not False or letter["IPO_V35_cited"] is not False:
        fail("secondary approved citizen case made into a proven exclusion or V35 verdict")
    if not set(letter["source_ids"])<=set(ss) or not letter["reported_material"] or not letter["reported_seal"]:
        fail("1677 physical description lacks secondary provenance")
    relationships=d["crosswalk_tests"]
    if len(relationships)!=3 or {(r["from"],r["to"]) for r in relationships}!=LINKS:
        fail("three distinct archive relations mandatory")
    for r in relationships:
        if not r["source_ids"] or not set(r["source_ids"])<=set(ss):
            fail("archive relationship lost evidence")
    ri={r["from"]:r for r in relationships}
    if ri["MLA 413–5 fol. 126r–128r"]["same_physical_copy"]!="UNRESOLVED" or ri["MLA 413–5 fol. 126r–128r"]["verbatim_collation"] is not False:
        fail("two 1661 witnesses have not been collated")
    if ri["1982 Zumbusch unlisted letter"]["individual_letter_item_found"] is not False:
        fail("modern specific letter not proven")
    if ri["AA II Nr23 1661-08-19 council record"]["same_physical_record"] is not False:
        fail("city council and prince-bishop rule records conflated")
    targets=d["next_target"]
    if len(targets)!=3 or {t["key"] for t in targets}!=TASKS or any(t["found"] is not False for t in targets):
        fail("three precise archive followups must remain pending")
    if len(d["editorial_holds"])<8:
        fail("historical source/copyright uncertainty erased")
    md=(ROOT/DOC).read_text(encoding="utf-8")
    if len(md)<5700 or md.count("\n## ")<7 or "DRAFT_RESEARCH_NOT_PUBLIC" not in md:
        fail("Korean detailed regional narrative missing")
    for q in ("Münstersches Landesarchiv","413–5","126r–128r","Zumbusch","unverzeichnet","C-Arm","Akten Nr.28","Urk. Nr.37","1677","§35"):
        if q not in md:fail("essential exact historical disclaimer absent: "+q)
    return {"MLA_expansions":1,"archive_links":4,"source_records":12,"original_Buergerbrief_read":0,"V35_verdicts":0,"published":0}

if __name__=="__main__":
    v=validate()
    print(f"PASS VOL05 V1.1: MLA definition {v['MLA_expansions']}, {v['archive_links']} archive links, {v['source_records']} sources; citizen original 0, V35 cases 0, PUBLIC 0")
