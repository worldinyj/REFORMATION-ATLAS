#!/usr/bin/env python3
"""Read-only integrity checks for Melanchthon VOL-04 deep research drafts.

This verifies references, document presence, media safety and the review gate.
PASS never authorizes historical publication. Standard library only.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse
import sys

ROOT=Path(__file__).resolve().parents[1]
j=lambda p:json.loads((ROOT/p).read_text(encoding="utf-8"))

def main()->int:
    data=j("data/deep/vol04_melanchthon_v01.json")
    base=j("data/overview/volumes_and_people_v01.json")
    texts=j("data/overview/events_documents_v01.json")
    tracks=j("data/deep/research_tracks_v01.json")
    article=(ROOT/"docs/01_CONTENT/VOL04/MELANCHTHON_DEEP_RESEARCH_V01.md").read_text(encoding="utf-8")
    sources,claims,events,media=(data[k] for k in ("sources","claims","events","visual_candidates"))
    sid={s["id"] for s in sources};cid={c["id"] for c in claims}
    valid_entities={x["id"] for x in base["people"]+base["volumes"]+texts["events"]+texts["documents"]}
    success=0;errors=0
    def check(ok,label):
        nonlocal success,errors
        success+=int(bool(ok));errors+=int(not ok)
        print(("PASS " if ok else "FAIL ")+label)
    check(data["person_id"]=="OV-P-014" and any(x["id"]=="OV-P-014" for x in base["people"]), "existing person canonical ID")
    check(data["volume_id"]=="VOL-04" and data["depth_block"]["id"]=="DEPTH-V04-P014-001","versioned research block linked to VOL-04")
    check(data["depth_block"]["review_status"]=="DRAFT" and not data["depth_block"]["publication_approved"],"deep content unapproved")
    check(len(sources)==17 and len(sid)==17,"17 independent keyed source registrations")
    check(all(s["url"].startswith("https://") and urlparse(s["url"]).netloc for s in sources),"HTTPS source links")
    check(all(s["access_level"] and s["source_kind"] and not s["full_text_copied"] for s in sources),"source evidence tier and no full-text copying")
    check(len(claims)==16 and len(cid)==16,"16 unique claims")
    check(all(c["source_ids"] and set(c["source_ids"])<=sid for c in claims),"all claims cite registered source IDs")
    check(all(c["review_status"]=="DRAFT" and not c["approved"] and not c["publication_approved"] for c in claims),"claims remain drafts")
    check(len(events)==11 and len(set(x["id"] for x in events))==11,"11 unique research timeline anchors")
    check(all(e["claim_id"] in cid and e["date_precision"] in {"day","year","approximate_period","approximate_year"} and not e["public_visible"] for e in events),"timeline claim refs, precision and no public dates")
    check("1518년 8월 28일" in article and "8월 29일" in article, "date discrepancy on inauguration retained")
    check("1540년" in article and "1530년" in article and "Variata" in article,"Confession recension distinctions visible")
    check("1548년" in article and "12월 22일" in article and "24일" in article,"Leipzig regesta approximate date issue visible")
    check(len(media)==3 and {m["role"] for m in media}=={"portrait","scene","schematic_map"},"portrait/scene/diagram visual candidates")
    check(all(not x["approved"] and not x["publication_approved"] and not x["binary_in_github"] for x in media),"all media are staged unapproved, binaries not claimed pushed")
    check(len(data["media_archive_sha256"])==64,"local ZIP SHA-256 supplied")
    check(all(s["id"] in article for s in sources),"all 17 sources in manuscript source list")
    check(not data["release_gate"]["approved"] and not data["release_gate"]["can_ship"] and not data["web_handoff"]["app_modified"],"web code unchanged, publication closed")
    a=next((x for x in tracks["tracks"] if x["id"]=="TRACK-V04-MELANCHTHON"),None)
    check(a is not None and a["status"].startswith("DRAFT_") and a.get("public_visible") is False,"research tracker updated")
    print(f"RESULT {success}/{success+errors}; historic publication NOT approved")
    return int(bool(errors))

if __name__=="__main__":
    raise SystemExit(main())
