#!/usr/bin/env python3
"""Research-only Trent Latin anchor and 1564 physical witness checks.

This tests provenance claims and ID consistency. It does not authenticate
historical statements, collate physical folios, or grant publication permission.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATH = "data/deep/vol05_trent_latin_witness_alignment_v01.json"
OLD = "data/deep/vol05_trent_catholic_reform_registry_v01.json"
EXPECTED = {
    "TR-TEXT-PROP-VI-7": (6, "1547-01-13", 7, "DOCTRINAL_DECREE_CHAPTER"),
    "TR-TEXT-PROP-VI-8": (6, "1547-01-13", 8, "DOCTRINAL_DECREE_CHAPTER"),
    "TR-TEXT-PROP-XIII-4": (13, "1551-10-11", 4, "DOCTRINAL_DECREE_CHAPTER"),
    "TR-TEXT-PROP-XXIII-18": (23, "1563-07-15", 18, "DISCIPLINARY_REFORM_DECREE_CHAPTER"),
}
EXPECTED_COPIES = {
    "TR-COPY-PROP-MORGAN-1564": ("PML 1214", 1564, "folio"),
    "TR-COPY-PROP-TRENTO-1564": (None, 1564, "folio"),
    "TR-COPY-PROP-VALENCIA-1564": ("XVI/233", 1564, "quarto"),
    "TR-COPY-PROP-PISA-1564": ("G h. 10. 48", 1564, "quarto"),
    "TR-COPY-PROP-PADERBORN-1621": (None, 1621, "later_annotated_edition"),
}
ACCESS_LEVELS = {
    "INSTITUTIONAL_CATALOG_READ", "INSTITUTIONAL_DESCRIPTION_READ",
    "DIGITAL_TABLE_OF_CONTENTS_READ_ONLY", "DISPLAYED_LATIN_TEXT_READ",
    "SEARCH_EXCERPT_READ", "ONLINE_1848_TRANSLATION_READ",
    "ONLINE_TRANSLATION_REFERENCE",
}
BIBLIO_ROLES = {
    "PHYSICAL_PRINT_WITNESS","LATER_ANNOTATED_EDITION",
    "MODERN_DIGITAL_TRANSCRIPTION","MODERN_LATIN_EDITED_TEXT","HISTORICAL_TRANSLATION",
}

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def bad(message):
    raise ValueError(message)

def validate(data=None):
    d = read(PATH) if data is None else data
    if d["kind"] != "VOL05_TRENT_LATIN_ANCHOR_AND_PRINT_WITNESSES" or d["status"] != "DRAFT_RESEARCH_NOT_PUBLIC":
        bad("not a research-only Latin witness registry")
    if (d["volume_id"],d["event_id"],d["work_id"]) != ("VOL-05","OV-E-021","OV-D-014"):
        bad("canonical parent crosswalk changed")
    if d["created_canonical_ids"] != 0 or d["ai_studio_modified"] is not False or d["overview_modified"] is not False:
        bad("canonical/public code altered")
    if set(d["publication_gate"]) != {
        "human_approved","latin_print_collated","parallel_translation_collated",
        "copy_image_rights_approved","can_ship"
    } or any(d["publication_gate"].values()):
        bad("release permission falsely asserted")
    old = read(OLD)
    if (old["canonical_event_id"],old["canonical_document_id"]) != (d["event_id"],d["work_id"]):
        bad("parent research canonical mapping mismatch")
    sessions = {s["number"]:s for s in old["sessions"]}
    if not {6,13,23} <= set(sessions):
        bad("missing baseline sessions")
    if {i["number"] for i in d["session_inventory"]} != {6,13,23} or len(d["session_inventory"]) != 3:
        bad("three-session inventory drift")
    for item in d["session_inventory"]:
        num = item["number"]
        if item["key"] != sessions[num]["key"] or item["year"] != int(sessions[num]["date"][:4]):
            bad("session inventory not linked to source research")
    sources = d["source_records"]
    if len(sources) != 10:
        bad("source inventory must be 10")
    index = {}
    for s in sources:
        key = s["key"]
        u = urlparse(s["url"])
        if not key.startswith("TR-LAT-SRC-PROP-") or key in index:
            bad("duplicate or unscoped source key")
        if u.scheme != "https" or not u.hostname:
            bad("unsafe URL")
        if not s["source_type"] or s["access"] not in ACCESS_LEVELS or s["bibliography_role"] not in BIBLIO_ROLES:
            bad("source kind or access missing")
        if (s["canonical_source_id"] is not None or s["rights_approved"] is not False or
            s["primary_print_folio_verified"] is not False or s["public_visible"] is not False):
            bad("source prematurely authorized/verified")
        if s["text_read"] and s["access"] not in {"DISPLAYED_LATIN_TEXT_READ","ONLINE_1848_TRANSLATION_READ"}:
            bad("text read claim not substantiated by access class")
        index[key] = s
    if sum(s["bibliography_role"]=="PHYSICAL_PRINT_WITNESS" for s in sources) != 4:
        bad("original holding source inventory drift")
    copies = d["print_copies"]
    if len(copies) != 5 or {x["copy_key"] for x in copies} != set(EXPECTED_COPIES):
        bad("five physical/historical print candidates required")
    copyidx = {}
    for c in copies:
        name = c["copy_key"]
        if (c["shelfmark"],c["printing_year"],c["format"]) != EXPECTED_COPIES[name]:
            bad("date/format/shelfmark false equivalence")
        if c["source_key"] not in index or not c["repository"] or not c["imprint"] or not c["status"]:
            bad("physical copy lacks catalog")
        expected_kind = "LATER_ANNOTATED_EDITION" if c["printing_year"]==1621 else "PHYSICAL_PRINT_WITNESS"
        if index[c["source_key"]]["bibliography_role"] != expected_kind:
            bad("copy confused with translation or later edition")
        if not c["status"] in {
            "CATALOG_CONFIRMED_BUT_LEAVES_NOT_INSPECTED","MUSEUM_DESCRIPTION_ONLY",
            "TOC_ONLY_NOT_1564_ORIGINAL"
        }:
            bad("falsely verified original text")
        if name.endswith("1621") != (c["printing_year"]==1621):
            bad("post-Tridentine edition treated as original")
        copyidx[name] = c
    if copies[0]["format"] == copies[2]["format"]:
        bad("folio vs quarto distinction erased")
    anchors = d["anchors"]
    if len(anchors) != 4 or {x["anchor_key"] for x in anchors} != set(EXPECTED):
        bad("four exact Latin anchors required")
    used_source_keys = set()
    for item in anchors:
        key = item["anchor_key"]
        if (item["session_number"],item["session_date"],item["section_number"],item["section_kind"]) != EXPECTED[key]:
            bad("wrong session, section or doctrine/discipline type")
        if item["session_date"] != sessions[item["session_number"]]["date"]:
            bad("Trent parent session date mismatch")
        if not item["latin_lemma"] or len(item["latin_lemma"].split()) > 7 or not item["ko_gloss"] or not item["interpretation_guard"]:
            bad("no short Latin search anchor/interpretive guard")
        if not item["section_title_latin"] or item["latin_lemma_kind"] != "BRIEF_SEARCH_ANCHOR":
            bad("Latin entry not merely a search reference")
        if item["physical_text_line_verified"] is not False or item["full_latin_english_parallel_collation"] is not False:
            bad("false original Latin or English collation")
        if item["approved"] is not False or item["public_visible"] is not False:
            bad("public release of unreviewed wording")
        if item["evidence_state"] != "EDITORIAL_CROSS_REFERENCE_ONLY":
            bad("evidence status promoted")
        s1,s2 = item["latin_display_source_key"],item["translation_source_key"]
        if s1 not in index or s2 not in index:
            bad("missing Latin or translation source")
        if index[s1]["bibliography_role"] != "MODERN_DIGITAL_TRANSCRIPTION":
            bad("Latin transcript role confusion")
        if index[s2]["bibliography_role"] != "HISTORICAL_TRANSLATION":
            bad("English translation role confusion")
        used_source_keys.update([s1,s2])
        if not item["physical_copy_keys"] or any(c not in copyidx for c in item["physical_copy_keys"]):
            bad("invalid physical witness associations")
        if item["session_number"]==23 and item["section_kind"]!="DISCIPLINARY_REFORM_DECREE_CHAPTER":
            bad("seminary decree incorrectly doctrinal")
    if "TR-ISSUE-1564-FORMAT" not in {i["issue_key"] for i in d["relation_issues"]} or len(d["relation_issues"]) < 6:
        bad("edition relationship caveats lost")
    if any(i["status"] != "OPEN" for i in d["relation_issues"]):
        bad("historical issue prematurely closed")
    return {"copy_records":len(copies),"source_records":len(index),"latin_anchors":len(anchors),"released":0}

if __name__ == "__main__":
    result = validate()
    print("PASS VOL05 Latin witness research:",
          f"{result['copy_records']} print copy records,",
          f"{result['source_records']} sources,",
          f"{result['latin_anchors']} anchors,",
          "PUBLIC 0")
