#!/usr/bin/env python3
"""VOL-04 edition-comparison read-only review adapter.

Research files are NOT production data. No public exporter exists here.
By default only validate/count; optional --review-output writes outside repo.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = {
    "contract": "data/contracts/vol04_document_edition_ui_v02.json",
    "bib": "data/deep/vol04_witness_bibliography_v02.json",
    "split": "data/deep/vol04_split_proposals_v01.json",
    "comparisons": "data/deep/vol04_edition_comparison_v01.json",
    "ui_v01": "data/contracts/vol04_document_edition_ui_v01.json",
}
# Explicit research-only linkage; never infer a canonical ID from year/language alone.
EDITION_LINKS = {
    "VOL04-CMP-001": ["EDN-PROP-V04-004", None, "EDN-PROP-V04-005"],
    "VOL04-CMP-002": ["DOC-PROP-V04-008-S01", "DOC-PROP-V04-008-S02"],
    "VOL04-CMP-003": ["EDN-PROP-V04-001-S02", "EDN-PROP-V04-003"],
}
TABS = {
    "STRUCTURAL": "structure",
    "ICONOGRAPHIC_VARIANT": "iconography",
    "DOCTRINAL_WORDING_DISPUTE": "textual_wording",
}

def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def inputs() -> dict:
    return {key: read(path) for key, path in INPUT.items()}

def validate_sources(d: dict) -> None:
    c, b, s, comp, v01 = (d[k] for k in ("contract", "bib", "split", "comparisons", "ui_v01"))
    if c["status"] != "DESIGN_AND_READ_ONLY_REVIEW_IMPLEMENTATION" or c["public_release_authorized"] is not False:
        raise ValueError("research-only contract invariant")
    if v01["status"] != "DESIGN_ONLY" or v01["public_projection_generated"] is not False:
        raise ValueError("existing UI contract gate changed")
    if b["release"]["approved"] or b["release"]["can_ship"] or comp["publication_approved"] or comp["source_text_collated"]:
        raise ValueError("source publication/text approval state changed")
    parents = {x["proposal_id"]: x for x in b["items"]}
    if len(parents) != len(b["items"]) or len(parents) != 17:
        raise ValueError("bibliographic parent registry integrity")
    groups = s["groups"]
    split_parents = {g["parent_proposal_id"] for g in groups}
    expected = {key for key, v in parents.items() if v["split_required_before_promotion"]}
    if len(groups) != 5 or split_parents != expected:
        raise ValueError("split parent integrity")
    children = [ch for g in groups for ch in g["children"]]
    if len(children) != 10 or len({ch["split_key"] for ch in children}) != 10:
        raise ValueError("split child integrity")
    if any(ch["canonical_id"] is not None or ch["publication_approved"] for ch in children):
        raise ValueError("candidate illegally promoted")
    if any(x["canonical_id"] is not None or x["publish"] for x in parents.values()):
        raise ValueError("bibliography illegally promoted")
    cases = comp["comparison_cases"]
    if len(cases) != 3 or {x["case_id"] for x in cases} != set(EDITION_LINKS):
        raise ValueError("comparison case registry")
    if {x["research_case_id"] for x in v01["research_examples"]} != set(EDITION_LINKS):
        raise ValueError("contract V0.1 case mismatch")
    child_to_group = {ch["split_key"]:g for g in groups for ch in g["children"]}
    seen = set()
    for case in cases:
        key = case["case_id"]
        if key in seen: raise ValueError("duplicate comparison id")
        seen.add(key)
        refs = EDITION_LINKS[key]
        if len(refs) != len(case["editions"]):
            raise ValueError("comparison/edition cardinality mismatch")
        if case["type"] not in TABS:
            raise ValueError("unknown comparison type")
        for ref, ed in zip(refs, case["editions"]):
            if ref is None:
                if key != "VOL04-CMP-001" or ed["year"] != 1539:
                    raise ValueError("unsupported unregistered edition")
                continue
            if ref in parents:
                p = parents[ref]
                year, langs, family = p["year_start"], p["languages"], p["work_family"]
            elif ref in child_to_group:
                g = child_to_group[ref]
                ch = next(x for x in g["children"] if x["split_key"] == ref)
                year, langs, family = ch["year"], [ch["language"]], g["work_family"]
            else: raise ValueError("unknown edition proposal reference")
            if year != ed["year"] or ed["language"] not in langs or family != case["work_family"]:
                raise ValueError("year/language/work identity mismatch")
    if c["review_counts"] != {
        "parent_candidates":17, "split_parent_candidates":5,
        "split_child_candidates":10, "comparison_cases":3, "approved_cases":0
    }: raise ValueError("review inventory does not match")
    if not c["guardrails"]["requires_explicit_separate_human_release_manifest"]:
        raise ValueError("release manifest prerequisite missing")

def make_review_view(d: dict) -> dict:
    validate_sources(d)
    comps = d["comparisons"]["comparison_cases"]
    result = []
    for case in comps:
        editions = []
        for ed, ref in zip(case["editions"], EDITION_LINKS[case["case_id"]]):
            date = str(ed["year"])
            if "month" in ed:
                month = ed["month"]
                if not isinstance(month, int) or not 1 <= month <= 12:
                    raise ValueError("invalid month")
                date += "-" + f"{month:02d}"
            editions.append({
                "proposal_key_review_only": ref,
                "label": ed.get("kind", date),
                "date_label": date,
                "date_precision": "month" if "month" in ed else "year",
                "language": ed["language"],
                "material_type_review_only": ed.get("kind", "historical_edition_unspecified"),
                "copy_holding_if_reported": ed.get("holding"),
                "canonical_edition_id": None,
            })
        result.append({
            "research_case_key":case["case_id"],
            "work_reference_review_only":case["work_family"],
            "route":None,
            "tab":TABS[case["type"]],
            "editions":editions,
            "observation_ko":case["observation_ko"],
            "interpretation_ko":case["interpretation_ko"],
            "evidence_level":case["evidence_level"],
            "source_urls_review_only":case["sources"],
            "source_ids_approved":[],
            "original_text_collated":False,
            "media_usable":False,
            "public_visible":False,
            "editorial_state":"RESEARCH_DRAFT",
        })
    return {
        "schema_version":"0.2",
        "kind":"RESEARCH_REVIEW_ONLY",
        "web_import_allowed":False,
        "approval_granted":False,
        "cases":result,
    }

def make_public_projection(d: dict) -> dict:
    """Contractually closed until a separate approval-manifest exporter exists."""
    validate_sources(d)
    return {
        "schema_version":"0.2",
        "kind":"PUBLIC_PROJECTION",
        "release_approved":False,
        "records":[],
    }

def safe_review_destination(path: str) -> Path:
    target = Path(path).expanduser().resolve()
    if target == ROOT or ROOT in target.parents:
        raise ValueError("Review JSON must NOT be written into the repository")
    if target.suffix.lower() != ".json":
        raise ValueError("Review output must be a JSON path")
    return target

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-output", default=None,
                        help="Explicit non-repo local draft only; NEVER deploy")
    a = parser.parse_args()
    d = inputs()
    review, public = make_review_view(d), make_public_projection(d)
    assert len(review["cases"]) == 3 and len(public["records"]) == 0
    if a.review_output:
        output = safe_review_destination(a.review_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(review, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print("REVIEW_ONLY:", output)
    print("PASS 17 parent candidates, 10 provisional children, 3 review cases; PUBLIC 0")

if __name__ == "__main__":
    main()
