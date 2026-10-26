#!/usr/bin/env python3
"""Regression/negative path checks: 7 sources and 3 comparison graph cases."""
from __future__ import annotations
import copy
from build_vol04_edition_ui_review_v02 import inputs
from build_vol04_provenance_graph_v03 import build_review_graph, read, REGISTRY

def reject(data, reg, reason):
    try:
        build_review_graph(data, reg)
    except (ValueError, KeyError, TypeError):
        return
    raise AssertionError("unsafe provenance mutation accepted: " + reason)

def main():
    d = inputs()
    reg = read(REGISTRY)
    graph = build_review_graph(d, reg)
    assert graph["kind"] == "RESEARCH_PROVENANCE_GRAPH_ONLY"
    assert graph["web_import_allowed"] is False
    assert graph["publication_approved"] is False and graph["public_records"] == []
    assert len(graph["cases"]) == 3
    assert sum(len(c["source_links_review_only"]) for c in graph["cases"]) == 7
    assert {c["tab"] for c in graph["cases"]} == {
        "structure", "textual_wording", "iconography"}
    assert all(c["route"] is None and c["public_visible"] is False
               for c in graph["cases"])
    assert all(not e["verified_in_this_revision"]
               for c in graph["cases"] for e in c["source_links_review_only"])
    cases = {c["research_case_key"]: c for c in graph["cases"]}
    assert cases["VOL04-CMP-001"]["people_context"][0]["id"] == "OV-P-016"
    assert cases["VOL04-CMP-002"]["events_context"] == []
    assert cases["VOL04-CMP-003"]["events_context"][0]["id"] == "OV-E-019"

    attacks = [
        ("publication", lambda x: x.__setitem__("publication_approved", True)),
        ("source access claim", lambda x: x.__setitem__("access_verified_this_revision", True)),
        ("source collated", lambda x: x.__setitem__("source_text_collated", True)),
        ("human approval", lambda x: x.__setitem__("human_approved", True)),
        ("web release", lambda x: x["release_gate"].__setitem__("allow_web_import", True)),
        ("missing source", lambda x: x["comparisons"][0]["source_keys"].pop()),
        ("foreign source", lambda x: x["comparisons"][0]["source_keys"].__setitem__(0, "OTHER")),
        ("wrong URL", lambda x: x["source_records"][0].__setitem__("url", "https://example.org/")),
        ("source approval", lambda x: x["source_records"][0].__setitem__("publication_approved", True)),
        ("canonical source ID", lambda x: x["source_records"][0].__setitem__("canonical_source_id", "SRC-999")),
        ("fake manuscript", lambda x: x["source_records"][0].__setitem__("original_witness", True)),
        ("unknown person", lambda x: x["comparisons"][0]["related_people"][0].__setitem__("id", "OV-P-999")),
        ("unknown event", lambda x: x["comparisons"][0]["related_events"][0].__setitem__("id", "OV-E-999")),
        ("wrong work", lambda x: x["comparisons"][0].__setitem__("work_reference", "OV-D-011")),
        ("missing caution", lambda x: x["comparisons"][0].__setitem__("caution_ko", "")),
    ]
    for label, mutate in attacks:
        changed = copy.deepcopy(reg)
        mutate(changed)
        reject(d, changed, label)
    modified = copy.deepcopy(d)
    modified["comparisons"]["comparison_cases"][0]["sources"][0] = "https://wrong.example.org"
    reject(modified, reg, "source edits in underlying comparison")
    print("PASS: provenance graph 3 cases, 7 sources, 16 unsafe mutations rejected; public=0")

if __name__ == "__main__":
    main()
