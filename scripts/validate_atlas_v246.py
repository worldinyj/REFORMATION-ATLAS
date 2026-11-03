#!/usr/bin/env python3
"""V246 selected photographic collation QA; never substitutes for paleography."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = "data/deep/atlas_v246_florentina_o91_photographs_sophia_autograph_selected_collation.json"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def index(rows, key="id"):
    result = {r[key]: r for r in rows}
    require(len(result) == len(rows), "duplicate " + key)
    return result

def validate(d):
    require(d["version"] == "2.46" and d["status"] == "DRAFT", "version/status")
    require(d["parent_commit"] == "81eb5bd007c3b7a454304ebe7fd4fcfe817641bf", "parent")
    require(all(x is False for x in d["publication_gate"].values()), "publication/paleography gate")
    for row in d["preserved_files"]:
        require(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"],
                "inherited snapshot changed: " + row["path"])
    require(d["baseline"] == d["preserved_files"][1]["path"], "baseline")
    sources = index(d["sources"])
    for row in sources.values():
        require(row["url"].startswith("https://") and row["reading"] and row["scope"], "source provenance")
    assets = index(d["retrieved_artifacts"], "filename")
    for row in assets.values():
        require(row["bytes"] > 0 and re.fullmatch(r"[a-f0-9]{64}", row["sha256"]), "source digest")

    mapping = index(d["sophia_folio_map"], "scan")
    expected_folios = ["254r", "254v", "255r", "255v", "256r", "256v",
                       "257r", "257v", "258r", "258v", "259r", "259v",
                       "260r", "260v", "260ar", "260av", "260br", "260bv"]
    require([mapping[i]["folio"] for i in range(525, 543)] == expected_folios, "scan/folio offset")
    original = index(d["sophia_original_faces"], "scan")
    require(sorted(original) == list(range(525, 531)), "original surface range")
    for scan, row in original.items():
        require(mapping[scan]["folio"] == row["folio"], "original folio reference")
    require(original[530]["role"] == "VERSO_NOTES", "sixth main-text page invented")
    require(sum(x["role"].startswith("MAIN_TEXT") for x in original.values()) == 5, "main-text face count")
    copy = d["sophia_copy"]
    require(copy["inventory_faces"] == 12 and copy["written_faces_in_contact"] == 8 and
            copy["blank_extension_faces_in_contact"] == 4, "copy extent")
    require([mapping[n]["folio"] for n in copy["detailed_scans"]] == copy["detailed_folios"],
            "detailed copy locus")
    require(copy["full_collation_complete"] is False and copy["independent_witness"] is False and
            copy["new_copy_date_proven"] is False, "copy scope exaggerated")
    require(copy["record_document_date"] == "1525-05-03" and
            copy["record_document_date_is_proven_copy_execution_date"] is False,
            "underlying letter date promoted to copy execution date")
    for row in d["sophia_comparisons"]:
        require(row["scan"] in original and mapping[row["scan"]]["folio"] == row["folio"], "lexical locus")
    words = index(d["sophia_comparisons"])
    require((words["S01"]["lemma"], words["S01"]["sense"]) == ("flüchgen", "CURSE_NOT_FLEE"),
            "curse/flee")
    require((words["S02"]["lemma"], words["S02"]["sense"]) == ("flygen", "FLEE_PHYSICAL_DANGER"),
            "flee/cursing conflation")
    numbers = d["numeric_review"]
    require((numbers["autograph_folio"], numbers["copy_folio"], numbers["print_page"]) ==
            ("255v", "260r", 334), "numeric target locus")
    require(mapping[numbers["autograph_scan"]]["folio"] == numbers["autograph_folio"] and
            mapping[numbers["copy_scan"]]["folio"] == numbers["copy_folio"], "numeric image reference")
    require([(x["print_value"], x["role"]) for x in numbers["targets"]] ==
            [(14, "PLACED_WITH_RELATIVES"), (16, "REMAINING_WITH_SOPHIA"),
             (17, "MOUTHS_TO_FEED"), (5, "GULDEN_AVAILABLE")], "inherited print roles")
    require(all(x["autograph_final_value"] is None and x["copy_final_value"] is None
                for x in numbers["targets"]), "unapproved numeral promoted to final reading")
    require(not numbers["print_emended"] and not numbers["new_numeric_variant_declared"] and
            not numbers["palaeography_approved"], "numeric review bypassed")

    f = d["florentina"]
    require((f["digital_object"], f["vd16"], f["bibliographic_id"]) ==
            ("bsb00027618", "O91", "BV009122474"), "wrong physical print witness")
    require(f["vd16_basis"] == "INSTITUTIONAL_MANIFEST_NOT_TITLE_ONLY_GUESS", "edition identity from title only")
    require(f["manifest_canvases"] == 22 and f["book_canvases"] == list(range(5, 21)), "book/image extent")
    groups = [set(f[k]) for k in ("title_canvases", "body_canvases", "blank_canvases")]
    require(set.union(*groups) == set(f["book_canvases"]) and
            sum(len(x) for x in groups) == len(f["book_canvases"]), "surface count overlap")
    require(f["body_canvases"] == list(range(7, 19)) and f["blank_canvases"] == [6, 19, 20],
            "blank pages counted as main text")
    require(set(f["luther_cover_canvases"]) | set(f["florentina_body_canvases"]) == groups[1],
            "speaker coverage")
    require(f["luther_postscript_canvas"] == 18, "postscript locus")
    require(not f["all_text_diplomatically_transcribed"] and not f["all_letters_individually_verified"],
            "photographic inspection promoted to full transcription")
    require(f["O90_counterpart_faces_seen"] == 0 and not f["O90_O91_pair_complete"] and
            f["emory_body_faces_newly_seen"] == 0 and not f["same_physical_copy_as_emory"],
            "one O91 holding promoted to other copies/pair")
    leaves = index(f["folio_map"], "canvas")
    require(leaves[11]["basis"] == "INFERRED_FROM_SIGNED_A3_AND_B1_NEIGHBOURS", "unsigned A4 falsely signed")
    collations = index(d["florentina_collations"])
    for row in collations.values():
        require(row["canvas"] in leaves and leaves[row["canvas"]]["folio"] == row["folio"], "print locus")
    require(collations["F03"]["observed"] == "klosters" and collations["F04"]["observed"] == "schrifftlich",
            "observed A4 spelling")
    require(collations["F05"]["canvas"] == collations["F06"]["canvas"] == 17 and
            collations["F07"]["canvas"] == collations["F08"]["canvas"] == 18, "escape/postscript locus")
    require("SELF_REPORT" in collations["F05"]["scope"] and "SELF_REPORT" in collations["F06"]["scope"],
            "self-report promoted to independent evidence")
    require(collations["F09"]["observed"] == "Jhesus" and "NOT_ALL_O91" in collations["F09"]["scope"],
            "local marginal reading generalized")
    require(sum(len(x["observed"].split()) for x in collations.values() if x["observed"]) <= 25,
            "excessive quotations")
    guards = d["inference_guards"]
    require(guards["photo_confirmation_not_independent_event_corroboration"] is True, "witness independence")
    require(all(value is False for key, value in guards.items()
                if key != "photo_confirmation_not_independent_event_corroboration" and
                key != "new_1526_manuscript_faces"), "historical overclaim")
    require(guards["new_1526_manuscript_faces"] == 0, "unread1526 manuscript claimed")
    require(not d["rights"]["image_binaries_added_to_repository"] and
            not d["rights"]["open_access_equals_historical_publication_approval"] and
            not d["rights"]["emory_prior_rights_conflict_resolved"], "rights scope")
    index(d["reader_sections"])
    for row in d["reader_sections"]:
        require(len(row["body"]) > 100 and set(row["sources"]) <= sources.keys(), "reader references")
    m = d["metrics"]
    require(m["source_records"] == len(sources) and m["retrieved_artifacts"] == len(assets) == 39, "source counts")
    require((m["new_1524_book_faces"], m["new_1524_title_faces"], m["new_1524_body_faces"],
             m["new_1524_blank_faces"]) == (16, 1, 12, 3), "print face metrics")
    require((m["new_1525_autograph_faces"], m["new_1525_main_text_faces"],
             m["new_1525_verso_notes_faces"]) == (6, 5, 1), "autograph face metrics")
    require(m["copy_inventory_faces"] == copy["inventory_faces"] and
            m["copy_detailed_faces"] == len(copy["detailed_scans"]), "copy scope metrics")
    require(m["sophia_comparisons"] == len(d["sophia_comparisons"]) and
            m["florentina_loci"] == len(collations) and m["reader_sections"] == len(d["reader_sections"]),
            "derived comparison counts")
    require(m["new_1526_original_faces"] == m["new_O90_O91_pairs"] ==
            m["new_approved_numeric_readings"] == m["published_web_items"] == 0, "overclaimed metrics")
    require((m["old_core_essays"], m["old_core_search_sentences"]) == (10, 543), "core")
    return assets

def verify_downloads(directory, assets, d):
    for name, row in assets.items():
        path = directory / name
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        require(path.stat().st_size == row["bytes"] and digest.hexdigest() == row["sha256"],
                "source-byte mismatch: " + name)
    ns = {"m": "http://www.loc.gov/METS/"}
    root = ET.parse(directory / "sophia_mets.xml").getroot()
    physical = {int(p.attrib["ID"].rsplit("_", 1)[1]): p.attrib.get("ORDERLABEL")
                for p in root.findall('.//m:structMap[@TYPE="PHYSICAL"]//m:div[@TYPE="page"]', ns)}
    for row in d["sophia_folio_map"]:
        require(physical[row["scan"]] == row["folio"], "METS folio mismatch")
    manifest = json.loads((directory / "bsb27618_manifest.json").read_text())
    require(len(manifest["sequences"][0]["canvases"]) == 22, "BSB manifest extent")
    meta = " ".join(str(x["value"]) for x in manifest["metadata"])
    require("VD16 O 91" in meta and "BV009122474" in meta and "Res/H.mon. 734 w" in meta,
            "BSB institutional identification")
    require(manifest["license"] == d["rights"]["BSB_manifest_license"], "BSB rights")
    print("PASS V246: 39 source files SHA256/size; 18 METS face labels; BSB22-canvas identity checked")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path)
    args = parser.parse_args()
    d = json.loads((ROOT / DATA_PATH).read_text(encoding="utf-8"))
    assets = validate(d)
    if args.evidence_dir:
        verify_downloads(args.evidence_dir, assets, d)
    print("PASS V246: BSB O91 title1/body12/blank3, local A4 and B3 readings; no O90 pair or Emory-body claim")
    print("PASS V246: Sophia6 faces =5 main+1 notes; 0526=254v; derivative copy12 inventory/3 detailed")
    print("PASS V246: selected lexical/context comparison only; all4 numeric targets await paleographic approval")
    print("PASS V246: immutable V219/V245 snapshots,10 essays/543 sentences, publication HOLD")
