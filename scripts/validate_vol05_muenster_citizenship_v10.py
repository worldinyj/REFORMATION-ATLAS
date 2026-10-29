#!/usr/bin/env python3
"""Münster named 1677 citizenship letter (secondary report) and 1661 copy references.

Checks historiographic source levels; cannot authenticate seventeenth-century
manuscripts, verify MLA expansion, or prove IPO Article V §35 verdicts.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_muenster_citizenship_1677_v10.json"
PREV="data/deep/vol05_muenster_reichshofrat_case_inventory_v09.json"
REPORT="docs/01_CONTENT/VOL05/MUENSTER_1661_1677_CITIZENSHIP_DEEP_V10.md"
GATES={"human_scholar_approved","copy_1626_primary_transcribed","archival_MLA_413_5_identified",
       "original_1677_citizen_letter_read","explicit_V35_case_adjudicated",
       "contemporary_art_rights_verified","can_publish"}
ARTIFACTS={
"MUE10-A-1661-0813":("1661-08-13","18TH_CENTURY_PAPER_COPY","MUE10-S04"),
"MUE10-A-1661-0819":("1661-08-19","SCHOLAR_CITES_MUNICIPAL_PROVISIONAL_COUNCIL_MINUTES","MUE10-S03"),
"MUE10-A-1661-MLA-413-5":("1661-08-13","ACADEMIC_FOOTNOTE_TO_POSSIBLE_ADDITIONAL_ARCHIVE_WITNESS","MUE10-S03"),
"MUE10-A-1677-0515-CITIZEN":("1677-05-15","SECONDARY_SCHOLARLY_REPRODUCTION_OF_CITIZEN_LETTER_NOT_ORIGINAL_MANUSCRIPT","MUE10-S02")
}
FOLLOWUPS={"MUE10-F-MLA","MUE10-F-AAII23","MUE10-F-BRINKMANS","MUE10-F-NR1626"}

def read(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def bad(reason):raise ValueError(reason)

def validate(d=None):
    d=read(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_MUENSTER_1661_RULE_AND_1677_CITIZENSHIP_RECEPTION",
        "DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        bad("historical record parent or evidence type changed")
    if d["parent_research"]!=PREV or d["new_canonical_ids"]!=0 or d["overview_changed"] is not False or d["ai_studio_changed"] is not False:
        bad("AI Studio/public canonical records cannot be changed by unpublished historical research")
    gates=d["publication_gate"]
    if set(gates)!=GATES or any(gates.values()):
        bad("premature primary-reading, V35 ruling, media, or public release gate")
    previous=read(PREV)
    if previous["canonical_event_id"]!=d["canonical_event_id"] or previous["canonical_document_id"]!=d["canonical_document_id"]:
        bad("breaks prior scholarly research lineage")
    sources=d["sources"]
    if len(sources)!=11 or len({x["key"] for x in sources})!=11:
        bad("eleven distinct evidence source records expected")
    si={}
    for s in sources:
        url=urlparse(s["url"])
        if url.scheme!="https" or not url.netloc or not s["key"].startswith("MUE10-S"):
            bad("untrusted or duplicate historical source")
        if not s["type"] or not s["scope"] or not s["access"]:
            bad("source type/access/claim scope not specified")
        if any(s[p] is not False for p in ("primary_17th_century_object_read","full_secondary_pdf_verified","media_reuse_cleared","public_approved")):
            bad("unread original, incomplete PDF or unapproved image rights claimed")
        si[s["key"]]=s
    if si["MUE10-S02"]["access"]!="INDEXED_PDF_TEXT_EXCERPTS_ONLY_DOWNLOAD_TOO_LARGE" or si["MUE10-S03"]["access"]!="PDF_MACHINE_TEXT_P95_96_98_READ_SCREENSHOT_FAILED":
        bad("indexed and visually unread PDF access exaggerated")
    if si["MUE10-S04"]["type"]!="DWUD_REGEST_18TH_C_COPY" or si["MUE10-S05"]["type"]!="DWUD_REGEST_18TH_C_COPY":
        bad("1661 later copies misclassified as 1661 originals")
    records=d["artifact_records"]
    if len(records)!=4 or {x["key"] for x in records}!=set(ARTIFACTS):
        bad("four distinct witness/catalog records mandatory")
    for x in records:
        date,medium,required=ARTIFACTS[x["key"]]
        if (x["original_act_date"],x["material_witness"])!=(date,medium):
            bad("1661 legal document vs 1677 citizenship or later copy conflated")
        if required not in x["source_keys"] or not set(x["source_keys"])<=set(si):
            bad("not supported by catalog/scholar reference")
        if x["full_witness_transcription_read"] is not False or x["actual_noncatholic_person_sanctioned"] is not False:
            bad("unverified original or actual non-Catholic sanction invented")
        if not x["holding"] and x["key"]!="MUE10-A-1677-0515-CITIZEN":
            bad("archival or scholarly folio locator missing")
    byid={x["key"]:x for x in records}
    if "Urkunden, Nr. 1626" not in byid["MUE10-A-1661-0813"]["holding"]:
        bad("1661 judge regulation 18th-century copy shelfmark lost")
    if byid["MUE10-A-1661-0813"]["reporting_non_catholics"]!="IN_REGEST_SUMMARY":
        bad("non-Catholic notification class changed")
    if "AA II 23" not in byid["MUE10-A-1661-0819"]["holding"]:
        bad("1661-08-19 provisional council record cannot be replaced with imaginary manuscript")
    if byid["MUE10-A-1661-MLA-413-5"]["holding"]!="MLA 413–5, fol. 126r–128r (institution expansion not yet checked)":
        bad("MLA shelfmark guessed or misidentified")
    if byid["MUE10-A-1677-0515-CITIZEN"]["citizenship_application_outcome_proved"] is not True:
        bad("positive 1677 named citizenship case omitted")
    citizen=d["citizenship_1677"]
    if (citizen["person_name_original_reported"],citizen["secondary_spelling"],citizen["date"])!=(
        "Greiteke Brinkmans","Grete Brinkmanns","1677-05-15"):
        bad("the named 1677 civilian record corrupted")
    if citizen["reported_magistrate"]!="Johann Dietrich Rave" or len(citizen["witnesses_reported"])!=2:
        bad("1677 citizen oath actors missing")
    if citizen["religious_exclusion_of_non_catholics_directly_proved"] is not False or citizen["IPO_V35_explicitly_invoked"] is not False:
        bad("admitted Catholic applicant falsely turned into rejected non-Catholic/V35 lawsuit")
    if citizen["individual_folio_signature_verified"] is not None or citizen["handwriting_or_seal_read"] is not False:
        bad("unknown original 1677 manuscript folio falsely identified")
    if citizen["scholar_secondary_transcription_not_full_book_review"] is not True:
        bad("secondary published excerpt access overstated")
    if not set(citizen["source_keys"])<=set(si) or len(citizen["conditions_interpreted"])<4:
        bad("1677 scholarly corroboration or citizenship procedure missing")
    f=d["archival_followups"]
    if len(f)!=4 or {x["key"] for x in f}!=FOLLOWUPS:
        bad("four precise next manuscript investigations required")
    for entry in f:
        if entry["source_key"] not in si or entry["direct_source_read"] is not False or not entry["question"]:
            bad("document access/identity prematurely confirmed")
    follow={x["key"]:x for x in f}
    if follow["MUE10-F-MLA"]["copy_or_original_status"]!="UNKNOWN" or "413–5" not in follow["MUE10-F-MLA"]["target"]:
        bad("MLA copy/original status must stay unknown")
    if len(d["historical_interpretation"])<9 or not any("PDF" in s for s in d["historical_interpretation"]):
        bad("critical source caveats or access failures hidden")
    visual=d["visual_reference_candidate"]
    if (visual["historical_event_year"],visual["linked_to_1677_civic_letter"])!=(1661,False) or visual["downloaded"] is not False or visual["cleared_for_webapp"] is not False:
        bad("incorrect or prematurely published historical art")
    if "2016645785" not in visual["url"]:
        bad("US LOC 1661 image catalog provenance missing")
    if d["research_certification"]!="PUBLISHED_SECONDARY_CITIZEN_LETTER_STUDY_AND_PRECISE_FOLIO_LEAD_NOT_ORIGINAL_TEXT_COLLATION":
        bad("research access level promoted without inspection")
    text=(ROOT/REPORT).read_text(encoding="utf-8")
    if len(text)<6200 or text.count("\n## ")<7 or "DRAFT_RESEARCH_NOT_PUBLIC" not in text:
        bad("reader narrative missing")
    for phrase in ("1661","1677","Greiteke","Brinkmans","MLA 413–5","126r–128r","1626","§35","미확인","직접"):
        if phrase not in text:bad("essential ethical or documentary qualification omitted: "+phrase)
    return {"sources":11,"named_citizenship":1,"archival_locator_leads":2,"document_contexts":4,"direct_v35_verdicts":0,"public":0}

if __name__=="__main__":
    x=validate()
    print("PASS VOL05 V1.0: 11 sources, named citizen document 1, 1661 source crosswalk 2, directly proved V35 verdicts 0, PUBLIC 0")
