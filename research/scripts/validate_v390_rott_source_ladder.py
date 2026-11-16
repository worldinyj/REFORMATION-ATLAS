#!/usr/bin/env python3
"""V3.90 research-only source ladder integrity checks. No network, no mutation."""
import argparse
import copy
import json
from pathlib import Path

EXPECTED = {468: 1531, 482: 1531, 489: 1536, 491: 1536}
def validate(d):
    errors = []
    if d.get("version") != "V3.90" or d.get("status") != "RESEARCH_DRAFT":
        errors.append("draft_version")
    r = d.get("release", {})
    if r.get("can_ship") is not False or any(r.get(k) is not False for k in
       ("main_modified","essays_513_modified","ai_studio_modified","external_messages_sent")):
        errors.append("release_guard")
    a = d.get("article", {})
    if a.get("legacy_url") != "https://www.zwingliana.ch/index.php/zwa/article/view/910/820":
        errors.append("historical_url")
    if a.get("legacy_second_token_semantics") != "UNCONFIRMED":
        errors.append("legacy_galley_id_inferred")
    if a.get("current_article_url") is not None or a.get("current_pdf_url") is not None:
        errors.append("fabricated_active_url")
    if a.get("original_pdf_bytes_retrieved") is not False or a.get("pdf_sha256") is not None:
        errors.append("fabricated_pdf_acquisition")
    sources = d.get("evidence", [])
    ids = [x.get("id") for x in sources]
    if len(ids) < 7 or len(ids) != len(set(ids)):
        errors.append("source_uniqueness")
    if any(x.get("direct_article_text") is True or x.get("direct_manuscript_image") is True
           for x in sources):
        errors.append("unearned_direct_evidence")
    cites = d.get("cross_citations", [])
    pages = [x.get("page") for x in cites]
    if set(pages) != set(EXPECTED) or len(pages) != len(EXPECTED):
        errors.append("page_coverage")
    for x in cites:
        if x.get("page") in EXPECTED:
            if x.get("context_year") != EXPECTED[x["page"]]:
                errors.append("year_page_conflation")
            if x.get("original_page_1978_seen") is not False:
                errors.append("page_visual_claim")
            if "ONLY" not in str(x.get("certainty", "")):
                errors.append("certainty_promotion")
    acq = d.get("acquisition", {})
    for key in ("legacy_910_820_successor_verified", "modern_article_link_retrieved",
                "modern_pdf_link_retrieved", "parker_original_images_199_200_205_206_seen",
                "publisher_1978_print_pages_489_491_seen", "external_editor_contact_sent"):
        if acq.get(key) is not False:
            errors.append("acquisition_guard:" + key)
    dates = d.get("date_constraints", {})
    if (dates.get("july_23_equals_july_25") != "UNRESOLVED" or
        dates.get("august_4_same_as_july_letter") != "UNPROVEN" or
        dates.get("date_line_manuscript_directly_read") is not False or
        dates.get("correct_zurich_catalog_id") != "CH-002121-2-991170608445805501" or
        dates.get("can_promote_original_letter_claim") is not False):
        errors.append("letter_identity_guard")
    return sorted(set(errors))

def self_test(d):
    assert not validate(d), validate(d)
    modifications = [
        ("ship", lambda x: x["release"].update(can_ship=True)),
        ("fake_pdf", lambda x: x["article"].update(original_pdf_bytes_retrieved=True)),
        ("fake_pages", lambda x: x["cross_citations"][2].update(original_page_1978_seen=True)),
        ("year_mix", lambda x: x["cross_citations"][0].update(context_year=1536)),
        ("date_merge", lambda x: x["date_constraints"].update(july_23_equals_july_25="PROVEN")),
        ("url_guess", lambda x: x["article"].update(current_pdf_url="https://zwingliana.ch/article/download/910/820")),
        ("image_claim", lambda x: x["acquisition"].update(parker_original_images_199_200_205_206_seen=True)),
    ]
    for name, change in modifications:
        bad = copy.deepcopy(d)
        change(bad)
        assert validate(bad), "undetected injected failure: " + name
    return len(modifications)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="research/data/V3_90_ROTT_SOURCE_TRIANGULATION_DRAFT.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    d = json.loads(Path(args.path).read_text(encoding="utf-8"))
    errors = validate(d)
    if errors:
        print("FAIL:", ", ".join(errors))
        raise SystemExit(1)
    print("PASS: V3.90 claims and release hard gates")
    if args.self_test:
        print("PASS:", self_test(d), "fault-injection cases")
if __name__ == "__main__":
    main()
