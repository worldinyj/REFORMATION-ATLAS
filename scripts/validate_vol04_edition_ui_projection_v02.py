#!/usr/bin/env python3
"""Regression and negative-path tests for the VOL-04 review-only projection."""
from __future__ import annotations
import copy
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from build_vol04_edition_ui_review_v02 import (  # noqa: E402
    inputs, validate_sources, make_review_view, make_public_projection,
    safe_review_destination
)

def must_reject(d, label):
    try: validate_sources(d)
    except ValueError: return
    raise AssertionError("unsafe change accepted: "+label)

def main():
    baseline=inputs()
    validate_sources(baseline)
    review=make_review_view(baseline)
    public=make_public_projection(baseline)
    assert review["kind"]=="RESEARCH_REVIEW_ONLY"
    assert review["web_import_allowed"] is False
    assert public == {"schema_version":"0.2","kind":"PUBLIC_PROJECTION",
                      "release_approved":False,"records":[]}
    assert len(review["cases"])==3
    assert {x["tab"] for x in review["cases"]}=={
        "structure","textual_wording","iconography"}
    assert all(x["route"] is None and x["public_visible"] is False and
               x["media_usable"] is False and x["original_text_collated"] is False and
               not x["source_ids_approved"] for x in review["cases"])
    assert all(e["canonical_edition_id"] is None
               for c in review["cases"] for e in c["editions"])
    luther=next(x for x in review["cases"] if x["research_case_key"]=="VOL04-CMP-002")
    assert [e["date_label"] for e in luther["editions"]]==["1522-09","1522-12"]
    calvin=next(x for x in review["cases"] if x["research_case_key"]=="VOL04-CMP-001")
    assert calvin["editions"][1]["proposal_key_review_only"] is None
    assert all(e["date_precision"]=="year" for e in calvin["editions"])

    mutations = [
        ("release approval",lambda d:d["bib"]["release"].__setitem__("approved",True)),
        ("draft publication",lambda d:d["comparisons"].__setitem__("publication_approved",True)),
        ("text collated false positive",lambda d:d["comparisons"].__setitem__("source_text_collated",True)),
        ("canonical ID mint",lambda d:d["bib"]["items"][0].__setitem__("canonical_id","DOC-V04-1000")),
        ("child publication",lambda d:d["split"]["groups"][0]["children"][0].__setitem__("publication_approved",True)),
        ("wrong year",lambda d:d["comparisons"]["comparison_cases"][0]["editions"][0].__setitem__("year",1537)),
        ("wrong language",lambda d:d["comparisons"]["comparison_cases"][0]["editions"][0].__setitem__("language","de")),
        ("wrong work",lambda d:d["comparisons"]["comparison_cases"][0].__setitem__("work_family","OV-D-011")),
        ("contract authorized",lambda d:d["contract"].__setitem__("public_release_authorized",True)),
        ("orphan child",lambda d:d["split"]["groups"][0]["children"][0].__setitem__("split_key","UNLINKED")),
    ]
    for name, mutate in mutations:
        d=copy.deepcopy(baseline)
        mutate(d)
        must_reject(d,name)
    for destination in [str(ROOT/"data"/"unsafe.json"),
                        str(ROOT/"scripts"/".."/"dist"/"unsafe.json")]:
        try: safe_review_destination(destination)
        except ValueError: pass
        else: raise AssertionError("in-repo output destination was allowed")
    print("PASS: 3 review-only cases, 0 public; 10 unsafe mutations rejected; repo output rejected")

if __name__=="__main__":
    main()
