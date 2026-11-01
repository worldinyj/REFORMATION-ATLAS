#!/usr/bin/env python3
"""V2.03 research navigation bridge: structural consistency, not historical approval."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

nav = load("data/contracts/atlas_v203_ten_reader_navigation.json")
src = load("data/deep/atlas_v202_unified_ten_revised_readers.json")
legacy = load("data/contracts/atlas_v179_ten_reader_claim_evidence.json")
people = load("data/overview/volumes_and_people_v01.json")
overview = load("data/overview/events_documents_v01.json")
places = load("data/overview/places_v01.json")
cities = load("data/contracts/atlas_v157_historical_city_map.json")
spatial = load("data/contracts/atlas_v157_spatiotemporal_links.json")
rights = load("data/contracts/atlas_v158_visual_rights_registry.json")
evidence = load("data/contracts/atlas_v163_source_evidence_cards.json")
editions = load("data/contracts/atlas_v161_edition_comparison_cards.json")
sources = load("data/overview/source_register_v01.json")

assert nav["version"] == "2.03"
assert nav["origin"]["reader_version"] == src["version"] == "2.02"
assert nav["origin"]["base_commit"] == "1eef207549ed04f65818e2bf76ddd52a6d6d1665"
assert all(flag is False for flag in nav["publication_gate"].values())
assert len(src["chapters"]) == len(nav["readers"]) == len(nav["claims"]) == 10
assert nav["coverage"]["reader_count"] == nav["coverage"]["representative_claim_count"] == 10

originals = {r["key"]: r for r in src["chapters"]}
legacy_claims = {c["reader_key"]: c for c in legacy["claims"]}
people_ids = {p["id"] for p in people["people"]}
event_ids = {e["id"] for e in overview["events"]}
document_ids = {d["id"] for d in overview["documents"]}
place_ids = {p["id"] for p in places["places"]}
city_ids = {c["id"] for c in cities["places"]}
ed_ids = {e["id"] for w in editions["works"] for e in w["editions"]}
evidence_ids = {e["id"] for e in evidence["cards"]}
visuals = {a["id"]: a for a in rights["assets"]}
url_to_source = {s["url"]: s["id"] for s in sources["sources"]}
keys = {r["key"] for r in nav["readers"]}
assert keys == set(originals) == set(legacy_claims)

section_count = city_count = visual_count = 0
for reader in nav["readers"]:
    key = reader["key"]
    body = originals[key]["body"]
    assert reader["reader_page_id"] == originals[key]["source_id"]
    assert reader["title"] == originals[key]["title"]
    assert reader["body_source_path"] == nav["origin"]["reader_file"]
    assert reader["body_storage"] == "REFERENCED_NOT_COPIED"
    assert reader["body_length_chars"] == len(body)
    assert reader["editorial_status"] == "HOLD_REQUIRES_HUMAN_REVIEW"
    assert reader["original_collated"] is False
    assert set(reader["person_ids"]) <= people_ids
    assert set(reader["primary_event_ids"]) <= event_ids
    assert set(reader["canonical_document_ids"]) <= document_ids
    assert set(reader["edition_ids"]) <= ed_ids
    assert set(reader["related_reader_keys"]) <= keys
    assert reader["representative_claim_id"] == legacy_claims[key]["id"]
    assert len(reader["section_anchors"]) == len(set(s["id"] for s in reader["section_anchors"]))
    match_list = list(re.finditer(r"^(#{2,3})[ \t]+(.+)$", body, re.M))
    cuts = ([(0, "도입", 0)] if match_list and match_list[0].start() > 0 else [])
    cuts += [(m.start(), m.group(2).strip(), len(m.group(1))) for m in match_list]
    if not cuts:
        cuts = [(0, "본문", 0)]
    assert len(cuts) == len(reader["section_anchors"])
    for i, (start, heading, level) in enumerate(cuts):
        s = reader["section_anchors"][i]
        end = cuts[i + 1][0] if i + 1 < len(cuts) else len(body)
        assert s["heading"] == heading and s["level"] == level
        assert s["start_char"] == start and s["end_char"] == end
        assert s["id"] == "SEC-V203-" + key + "-" + str(i + 1).zfill(2)
    section_count += len(cuts)
    all_city_links = [l for l in spatial["links"] if l["reader_page_id"] == reader["reader_page_id"]]
    assert len(reader["map_contexts"]) == len(all_city_links)
    for link in reader["map_contexts"]:
        assert link["city_map_id"] in city_ids
        if link["overview_place_id"] is not None:
            assert link["overview_place_id"] in place_ids
        assert link["site_precision"] == "CITY_ONLY"
        assert link["geometry_publishable"] is False
        assert link["editorial_link_status"] == "CONTEXT_ONLY"
        assert any(l["place_id"] == link["city_map_id"] and l["relation"] == link["relation"] and l["period"] == link["period"] for l in all_city_links)
    city_count += len(reader["map_contexts"])
    expected_assets = {a["id"] for a in rights["assets"] if a["reader_page_id"] == reader["reader_page_id"]}
    assert set(reader["visual_candidate_ids"]) == expected_assets
    assert all(visuals[a]["approved_to_publish"] is False for a in reader["visual_candidate_ids"])
    visual_count += len(reader["visual_candidate_ids"])

assert nav["coverage"]["section_anchor_count"] == section_count
assert nav["coverage"]["city_context_count"] == city_count == 11
assert nav["coverage"]["candidate_visual_count"] == visual_count == 14
assert nav["coverage"]["reader_count"] == 10

for claim in nav["claims"]:
    baseline = legacy_claims[claim["reader_key"]]
    r = next(x for x in nav["readers"] if x["key"] == claim["reader_key"])
    assert claim["id"] == baseline["id"] == r["representative_claim_id"]
    assert claim["reader_page_id"] == r["reader_page_id"]
    assert claim["section_id"] in {s["id"] for s in r["section_anchors"]}
    assert claim["claim_text"] == baseline["claim"]
    assert claim["source_class"] == baseline["source_class"]
    assert [s["url"] for s in claim["source_references"]] == baseline["urls"]
    for s in claim["source_references"]:
        assert s["overview_source_id"] == url_to_source.get(s["url"])
        assert s["claim_specific_web_rechecked"] is False
        assert s["source_scope"] == "RESEARCH_LEAD_NOT_PASSAGE_PROOF"
    assert claim["preexisting_explicit_evidence_ids"] == baseline["linked_evidence_cards"]
    assert set(claim["preexisting_explicit_evidence_ids"]) <= evidence_ids
    assert set(e["id"] for e in claim["related_evidence_cards"]) <= evidence_ids
    assert all(e["primary_original_collated"] is False for e in claim["related_evidence_cards"])
    assert claim["existing_unverified_note"] == baseline["unverified"]
    assert claim["original_folio_checked"] is False
    assert claim["human_review"] == "PENDING"
    assert claim["can_publish"] is False
    assert claim["support_state"] == "BIBLIOGRAPHIC_LEAD_NOT_VERIFIED_AT_PASSAGE_LEVEL"

bykey = {r["key"]: r for r in nav["readers"]}
assert "WRK-V03-WYCLIFFE-DE-ECCLESIA" in bykey["WYCLIFFE"]["provisional_work_ids"]
assert bykey["WYCLIFFE"]["canonical_document_ids"] == []
assert bykey["HUS"]["canonical_document_ids"] == ["OV-D-005"]
assert bykey["CALVIN1559"]["primary_event_ids"] == []
assert bykey["ZWINGLI"]["primary_event_ids"] == []
assert {x["city_map_id"] for x in bykey["MARBURG"]["map_contexts"]} == {"marburg"}
assert bykey["MARBURG"]["map_contexts"][0]["overview_place_id"] is None
assert bykey["CALVIN1536"]["map_contexts"][0]["overview_place_id"] is None
assert bykey["AUGSBURG"]["edition_ids"] == ["EDN-V161-AC-1530", "EDN-V161-AC-1531", "EDN-V161-AC-1540"]
assert bykey["CALVIN1536"]["edition_ids"] == ["EDN-V161-INST-1536"]
assert bykey["CALVIN1559"]["edition_ids"] == ["EDN-V161-INST-1559"]
assert any(x["code"] == "CLAIM_GRANULARITY" for x in nav["unresolved"])

print(f"PASS V203: {len(bykey)} readers, {section_count} anchored sections, {len(nav['claims'])} representative claims, {city_count} city contexts, {visual_count} unpublished visual candidates, publication HOLD")
