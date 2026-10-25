#!/usr/bin/env python3
"""Validate Calvin deep research ID, provenance and publication gates.
PASS is a draft data-structure check, NOT source collation or web permission.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
def j(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    data=j("data/deep/vol04_calvin_v01.json")
    people=j("data/overview/volumes_and_people_v01.json")
    events_base=j("data/overview/events_documents_v01.json")
    tracks=j("data/deep/research_tracks_v01.json")
    md=(ROOT/"docs/01_CONTENT/VOL04/CALVIN_DEEP_RESEARCH_V01.md").read_text(encoding="utf-8")
    source,claims,timeline,images=(data[x] for x in ("sources","claims","events","visual_candidates"))
    sid={s["id"] for s in source}
    cid={c["id"] for c in claims}
    n=fail=0
    def ck(ok, label):
        nonlocal n,fail
        n+=1;fail+=int(not ok)
        print(("PASS " if ok else "FAIL ")+label)
    ck(data["person_id"]=="OV-P-016" and any(p["id"]=="OV-P-016" and p["name_en"]=="John Calvin" for p in people["people"]),"canonical person OV-P-016 retained")
    ck(data["volume_id"]=="VOL-04","volume correct")
    ck(data["depth_block"]["id"]=="DEPTH-V04-P016-001" and data["depth_block"]["kind"]=="DEEP_RESEARCH","deep block compatible")
    ck(len(source)==16 and len(sid)==16,"16 keyed historical references")
    ck(all(urlparse(s["url"]).scheme=="https" and urlparse(s["url"]).netloc for s in source),"all source URLs https")
    ck(all(not s["full_text_copied"] and s["access_status"] and s["kind"] for s in source),"citation types and no full-text copying")
    ck(len(claims)==16 and len(cid)==16,"16 distinct history claims")
    ck(all(c["source_ids"] and set(c["source_ids"])<=sid for c in claims),"claim sources referenced and registered")
    ck(all(c["review_status"]=="DRAFT" and not c["approved"] and not c["publication_approved"] for c in claims),"all claims unapproved")
    ck(len(timeline)==12 and len({e["id"] for e in timeline})==12,"12 new research time anchors")
    ck(all(e["claim_id"] in cid and e["date_precision"] in {"day","year","approximate_year","approximate_period"} for e in timeline),"time events claim refs and precision valid")
    ck(all(not e["public_visible"] for e in timeline),"no new events publicly visible")
    ck("1536년" in md and "1559년" in md and "4권" in md,"1536 and 1559 edition structures distinguished")
    ck("시의회" in md and "목사" in md and "장로" in md,"Geneva government and ministries included")
    ck("세르베투스" in md and "카스텔리오" in md,"historical coercion and contemporary dissent covered")
    ck("1549년" in md and "불링거" in md,"1549 Zurich Consensus not incorrectly ascribed to Zwingli")
    ck(len(images)==3 and {i["role"] for i in images}=={"portrait","scene","schematic_map"},"3 distinct image/map draft roles")
    ck(all(not i["approved"] and not i["publication_approved"] and not i["binary_in_github"] for i in images),"visuals staged and NOT claimed uploaded to GitHub")
    ck(len(data["media_archive_sha256"])==64,"visual package hash recorded")
    ck(all(s["id"] in md for s in source),"all 16 citations listed in manuscript appendix")
    ck(data["web_handoff"]["app_modified"] is False and data["web_handoff"]["attach_to_existing_person"]=="OV-P-016","web app unchanged; ID stable")
    ck(not data["release_gate"]["approved"] and not data["release_gate"]["can_ship"],"research release denied")
    ct=next((t for t in tracks["tracks"] if t["id"]=="TRACK-V04-CALVIN"),None)
    ck(ct is not None and ct["status"].startswith("DRAFT_") and ct["public_visible"] is False and ct["claims"]==16,"research registry updated")
    print(f"RESULT {n-fail}/{n} passed; not a peer review or authorization to publish")
    return int(bool(fail))
if __name__=="__main__":
    raise SystemExit(main())
