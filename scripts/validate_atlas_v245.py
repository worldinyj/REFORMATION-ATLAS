#!/usr/bin/env python3
"""Check V245 provenance, page boundaries and source independence.

This is structural QA, not historical approval. Optional source-byte verification:
  python3 scripts/validate_atlas_v245.py --evidence-dir /path/to/downloads
No source image/PDF is required in the repository.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = "data/deep/atlas_v245_kawerau_print_florentina_title_and_gess_dependency.json"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def indexed(rows):
    result = {row["id"]: row for row in rows}
    require(len(result) == len(rows), "duplicate ID")
    return result

def validate(d):
    require(d["version"] == "2.45" and d["status"] == "DRAFT", "version/status")
    require(d["parent_commit"] == "f24b14afbc2f9ed5e9add05ae86d8a6adae497cf", "parent")
    require(all(flag is False for flag in d["publication_gate"].values()), "publication HOLD")
    for row in d["preserved_files"]:
        require(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"],
                "immutable inherited file changed: " + row["path"])
    core = json.loads((ROOT / d["preserved_files"][0]["path"]).read_text())
    require(core["metrics"]["chapters"] == 10 and core["metrics"]["sentences"] == 543, "core size")
    require(d["baseline"] == d["preserved_files"][1]["path"], "baseline linkage")
    sources = indexed(d["sources"])
    pages = indexed(d["page_readings"])
    artifacts = indexed(d["retrieved_artifacts"])
    for source in sources.values():
        require(source["url"].startswith("https://") and source["reading_level"] and source["scope"],
                "incomplete source")
    for artifact in artifacts.values():
        require(artifact["source_id"] in sources and artifact["bytes"] > 0, "artifact provenance")
        require(re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"]), "artifact SHA256")
        require(artifact["repository_binary_included"] is False, "external image copied to repo")

    edition = d["edition"]
    require((edition["volume"], edition["volume_year"], edition["issue_year_visually_read"]) ==
            (13, 1880, 1881), "series metadata confused with physical imprint")
    require(edition["title_pdf_page"] == 7, "title face mapping")
    require(sorted(p["printed_page"] for p in pages.values()) == list(range(330, 339)), "article range")
    for row in pages.values():
        require(row["source_id"] == "KAW-IA" and row["visually_read"] is True, "page provenance")
        require(row["pdf_page"] == row["printed_page"] + 8, "PDF index mistaken for print page")
        require(row["scan_leaf"] == row["printed_page"] + 8, "scan leaf mapping")
    require(edition["article_print_pages"] == sorted(p["printed_page"] for p in pages.values()), "page list")
    require(edition["article_pdf_pages"] == sorted(p["pdf_page"] for p in pages.values()), "PDF list")
    require(edition["sophia_letter_body_print_pages"] == list(range(331, 336)), "Sophia body boundary")
    require(edition["petition_body_print_pages"] == list(range(336, 339)), "petition body boundary")
    require(edition["all_nine_pages_are_letter_body"] is False, "editorial text counted as letter")
    require("SOPHIA_END" in pages["K335"]["layer"] and "EDITORIAL" in pages["K336"]["layer"],
            "voice boundary lost")

    anchors = indexed(d["short_anchors"])
    require(sum(len(x["text"].split()) for x in anchors.values()) <= 25, "excessive print quotations")
    for anchor in anchors.values():
        require(anchor["page_id"] in pages, "unknown anchor page")
        body_range = (edition["sophia_letter_body_print_pages"] if anchor["voice"] == "SOPHIA"
                      else edition["petition_body_print_pages"])
        require(pages[anchor["page_id"]]["printed_page"] in body_range, "speaker assigned to editorial page")
    require(anchors["A01"]["text"] == "nicht flüchgen", "curse/flee confusion")
    numbers = indexed(d["numeric_context"])
    require([(numbers[k]["value"], numbers[k]["role"]) for k in ("N14", "N16", "N17", "N5")] ==
            [(14, "PLACED_WITH_RELATIVES_OR_LOCAL_CONNECTIONS"), (16, "REMAINING_WITH_SOPHIA"),
             (17, "MOUTHS_TO_FEED"), (5, "GULDEN_AVAILABLE")], "distinct numeric contexts conflated")
    require(numbers["N17"]["includes_sophia_hypothesis"] == "PLAUSIBLE_NOT_EXPLICIT", "inference overstated")
    require(all(x["page_id"] == "K334" for x in numbers.values()), "numeric locus")
    for anchor_id, number in (("A02", 14), ("A03", 16), ("A06", 17)):
        roman = anchors[anchor_id]["text"].lower().replace("j", "i")
        values = {"i": 1, "v": 5, "x": 10}
        total = sum(-values[ch] if i + 1 < len(roman) and values[ch] < values[roman[i + 1]]
                    else values[ch] for i, ch in enumerate(roman))
        require(total == number, "Roman numeral transcription does not match interpretation")

    chain = indexed(d["transmission"])
    petition = chain["PETITION-CHAIN"]
    require(petition["date"] == "1526-11-12" and petition["intended_addressee"] == "Charles V", "date/addressee")
    require(petition["current_catalogue_identity_verified"] is False and petition["original_autograph_found"] is False,
            "historic copy shelfmark promoted to original")
    require(petition["emperor_receipt_proven"] is False and
            petition["delivery_doubt_layer"] == "KAWERAU_EDITORIAL_COMMENTARY_P336", "receipt evidence overstated")
    sophia = chain["SOPHIA-CHAIN"]
    require(not sophia["autograph_visually_read_this_version"] and
            not sophia["copy_visually_collated_this_version"], "print read promoted to autograph collation")
    regest = chain["GESS-DEPENDENCY"]
    require((regest["document_number"], regest["printed_page"], regest["pdf_page"]) == (1346, 645, 669),
            "dependent regest locus")
    require(regest["form"] == "REGEST_NOT_FULL_TRANSCRIPTION" and
            regest["independent_manuscript_witness"] is False and
            regest["independent_confirmation_of_petition_accusations"] is False,
            "derivative regest counted as independent witness")
    require((regest["edition_original_year"], regest["edition_scanned_reprint_year"]) == (1917, 1985),
            "reprint confused with original edition")

    flo = d["florentina_collation"]
    require(flo["title_face_visually_read"] and flo["title_reading"] == "geschicht", "title observation")
    require(flo["body_faces_visually_read"] == flo["hab_O90_faces_visually_read"] ==
            flo["hab_O91_faces_visually_read"] == 0 and not flo["A3r_A4r_collated"], "title-only overclaim")
    require(not flo["emory_copy_definitively_assigned_to_vd16_O91"], "title used for full edition identity")
    require(flo["canvas_is_pdf_wrapper"] and not flo["manifest_canvas_count_is_book_page_count"],
            "IIIF wrapper counted as book extent")
    require(not flo["extent14_means_fourteen_text_bearing_faces"], "extent metadata overstated")
    require(not flo["wa15_reported_press_state_sequence_secure"] and
            flo["wa15_Aa_Ab_online_label_internal_inconsistency_requires_facsimile"],
            "unverified editorial sigla silently normalized")
    require(not flo["rights"]["conflict_resolved"] and not flo["rights"]["reusable_image_uploaded_to_git"],
            "rights gate bypass")

    for finding in d["claim_findings"]:
        require(set(finding.get("page_ids", [])) <= pages.keys(), "unknown finding page")
        require(set(finding.get("source_ids", [])) <= sources.keys(), "unknown finding source")
        require(finding["independent_event_truth_established"] is False, "document claim turned into proven event")
    for section in d["reader_sections"]:
        require(len(section["body_ko"]) > 100 and set(section["sources"]) <= sources.keys(), "reader references")
    indexed(d["claim_findings"])
    indexed(d["reader_sections"])
    require(len(d["open_issues"]) > 0, "unresolved source work erased")
    m = d["metrics"]
    require(m["source_records"] == len(sources) and m["korean_reader_sections"] == len(d["reader_sections"]),
            "derived record counts")
    require(m["kawerau_article_print_faces_visually_read"] == len(pages) and
            m["sophia_letter_print_body_faces"] == len(edition["sophia_letter_body_print_pages"]) and
            m["abbesses_petition_print_body_faces"] == len(edition["petition_body_print_pages"]), "face counts")
    require(m["original_1524_title_faces_visually_read"] == 1 and
            m["original_1524_body_faces_visually_read"] == m["original_1525_autograph_faces_visually_read"] ==
            m["original_1526_manuscript_faces_visually_read"] == m["hab_O90_O91_A4r_pairs_collated"] ==
            m["new_independent_1526_manuscript_witnesses"] == m["published_web_items"] == 0,
            "evidence level overclaim in metrics")
    require(m["old_core_essays"] == 10 and m["old_core_search_sentences"] == 543, "baseline metrics")
    return artifacts

def verify_source_bytes(directory, artifacts):
    names = {"ART-KAW": "harz13.pdf", "ART-SCAN": "harz13_scandata.xml",
             "ART-TITLE": "florentina_title.jpg", "ART-MANIFEST": "emory2691_manifest.json",
             "ART-GESS": "gess2.pdf", "ART-GESS-TOC": "gess2_contents.pdf"}
    for key, name in names.items():
        path = directory / name
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        require(path.stat().st_size == artifacts[key]["bytes"] and
                digest.hexdigest() == artifacts[key]["sha256"], "download mismatch: " + name)
    rows = [p for p in ET.parse(directory / "harz13_scandata.xml").findall(".//pageData/page")
            if p.findtext("addToAccessFormats") != "false"]
    require(len(rows) == artifacts["ART-KAW"]["pdf_pages"], "PDF/scan page count")
    for print_page in range(330, 339):
        page = rows[print_page + 7]
        require(page.findtext("pageNumber") == str(print_page), "print-page XML locus")
    print("PASS V245: source bytes SHA256/size verified for all 6 retrieved artifacts; scan page mapping checked")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path)
    args = parser.parse_args()
    payload = json.loads((ROOT / DATA_PATH).read_text(encoding="utf-8"))
    artifacts = validate(payload)
    if args.evidence_dir:
        verify_source_bytes(args.evidence_dir, artifacts)
    print("PASS V245: 9 Kawerau print faces; title1880/1881; letter331–335 versus petition336–338")
    print("PASS V245: 14 entrusted / 16 remaining / 17 fed / 5 gulden; no silent numeral correction")
    print("PASS V245: chancery copy, editorial delivery doubt and dependent Gess1346 regest kept distinct")
    print("PASS V245: 1524 title1/body0; no A4r or autograph collation claimed; 10 essays/543 sentences immutable; HOLD")
